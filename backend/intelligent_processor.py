#!/usr/bin/env python3
"""
Intelligent Data Processor for Real Estate Files
Handles proper document classification, duplicate detection, and data rectification
"""

import os
import re
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple
import pandas as pd
from pathlib import Path
from collections import defaultdict

# Text processing
try:
    from fuzzywuzzy import fuzz, process
    FUZZY_AVAILABLE = True
except ImportError:
    FUZZY_AVAILABLE = False

# PDF Processing
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

logger = logging.getLogger(__name__)

class IntelligentDataProcessor:
    """Intelligent data processor with proper classification and duplicate detection"""
    
    def __init__(self):
        # Document classification patterns
        self.classification_patterns = {
            'legal_document': {
                'keywords': [
                    'contract', 'agreement', 'terms and conditions', 'clause', 'party', 'parties',
                    'legal', 'law', 'regulation', 'compliance', 'liability', 'indemnity',
                    'breach', 'termination', 'enforcement', 'jurisdiction', 'governing law',
                    'signature', 'witness', 'notary', 'legal counsel', 'attorney'
                ],
                'weight': 10
            },
            'property_listing': {
                'keywords': [
                    'for sale', 'for rent', 'available', 'listing', 'property details',
                    'bedroom', 'bathroom', 'sq ft', 'square feet', 'square meters',
                    'floor plan', 'amenities', 'features', 'description', 'photos',
                    'price', 'asking price', 'offers', 'viewing', 'contact agent'
                ],
                'weight': 8
            },
            'market_report': {
                'keywords': [
                    'market analysis', 'market report', 'market trends', 'market overview',
                    'quarterly report', 'annual report', 'market forecast', 'market outlook',
                    'demand', 'supply', 'inventory', 'absorption', 'market performance',
                    'growth', 'decline', 'stable', 'market indicators', 'market data'
                ],
                'weight': 9
            },
            'neighborhood_guide': {
                'keywords': [
                    'neighborhood', 'community', 'area guide', 'location overview',
                    'amenities', 'schools', 'hospitals', 'shopping', 'restaurants',
                    'transportation', 'metro', 'bus', 'parking', 'parks', 'recreation',
                    'lifestyle', 'residential area', 'commercial area', 'mixed use'
                ],
                'weight': 7
            },
            'transaction_record': {
                'keywords': [
                    'transaction', 'sale record', 'purchase record', 'transfer record',
                    'closing date', 'settlement date', 'completion date', 'deal value',
                    'buyer', 'seller', 'agent', 'broker', 'commission', 'fees',
                    'mortgage', 'financing', 'payment', 'escrow', 'title transfer'
                ],
                'weight': 8
            },
            'agent_profile': {
                'keywords': [
                    'agent profile', 'broker profile', 'real estate agent', 'license',
                    'experience', 'specialization', 'certifications', 'awards',
                    'performance', 'sales record', 'client testimonials', 'contact',
                    'office', 'team', 'agency', 'brokerage'
                ],
                'weight': 6
            },
            'developer_profile': {
                'keywords': [
                    'developer', 'development company', 'project portfolio', 'projects',
                    'construction', 'development', 'master plan', 'phase', 'completion',
                    'handover', 'warranty', 'maintenance', 'facilities', 'services'
                ],
                'weight': 7
            }
        }
        
        # Building name variations for duplicate detection
        self.building_variations = {
            'dubai marina': ['dubai marina', 'marina', 'marina district', 'marina area'],
            'downtown dubai': ['dubai downtown', 'downtown', 'downtown dubai', 'burj area'],
            'palm jumeirah': ['palm', 'palm jumeirah', 'palm island', 'the palm'],
            'business bay': ['business bay', 'bay area', 'business district'],
            'jbr': ['jbr', 'jumeirah beach residences', 'beach residences'],
            'dubai hills': ['dubai hills', 'hills estate', 'hills community'],
            'emirates hills': ['emirates hills', 'emirates hills estate'],
            'springs': ['springs', 'the springs', 'springs community'],
            'meadows': ['meadows', 'the meadows', 'meadows community'],
            'lakes': ['lakes', 'the lakes', 'lakes community']
        }
        
        # Data quality patterns
        self.data_quality_patterns = {
            'price_patterns': [
                r'AED\s*([\d,]+(?:\.\d{2})?)',
                r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*AED',
                r'USD\s*([\d,]+(?:\.\d{2})?)',
                r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*USD'
            ],
            'date_patterns': [
                r'\d{1,2}[-/]\d{1,2}[-/]\d{4}',
                r'\d{4}[-/]\d{1,2}[-/]\d{1,2}',
                r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}'
            ],
            'phone_patterns': [
                r'\+971\s*\d{2}\s*\d{3}\s*\d{4}',
                r'0\d{2}\s*\d{3}\s*\d{4}',
                r'\d{3}-\d{3}-\d{4}'
            ]
        }
    
    def classify_document(self, content: str, file_type: str) -> Dict[str, Any]:
        """Intelligently classify document based on content"""
        content_lower = content.lower()
        
        # Calculate scores for each category
        scores = {}
        for category, pattern in self.classification_patterns.items():
            score = 0
            for keyword in pattern['keywords']:
                if keyword in content_lower:
                    score += pattern['weight']
            
            # Additional scoring based on file type
            if file_type == 'csv' and category == 'transaction_record':
                score += 5
            elif file_type == 'excel' and category in ['market_report', 'transaction_record']:
                score += 5
            elif file_type == 'pdf' and category in ['legal_document', 'market_report', 'neighborhood_guide']:
                score += 3
            
            scores[category] = score
        
        # Get the category with highest score
        if scores:
            best_category = max(scores, key=scores.get)
            confidence = min(100, scores[best_category] / 10)  # Normalize to 0-100
        else:
            best_category = 'general_document'
            confidence = 50
        
        return {
            'category': best_category,
            'confidence': confidence,
            'scores': scores,
            'file_type': file_type
        }
    
    def extract_content(self, file_path: str, file_type: str) -> str:
        """Extract content from different file types"""
        try:
            if file_type == 'pdf':
                return self._extract_pdf_content(file_path)
            elif file_type in ['csv', 'excel']:
                return self._extract_structured_content(file_path, file_type)
            elif file_type == 'text':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                return ""
        except Exception as e:
            logger.error(f"Error extracting content from {file_path}: {e}")
            return ""
    
    def _extract_pdf_content(self, file_path: str) -> str:
        """Extract text from PDF using multiple methods"""
        content = ""
        
        # Method 1: PyPDF2
        if PDF_AVAILABLE:
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        content += page.extract_text() + "\n"
                if content.strip():
                    return content
            except Exception as e:
                logger.warning(f"PyPDF2 extraction failed: {e}")
        
        # Method 2: pdfplumber
        if PDFPLUMBER_AVAILABLE:
            try:
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            content += text + "\n"
                if content.strip():
                    return content
            except Exception as e:
                logger.warning(f"pdfplumber extraction failed: {e}")
        
        return content
    
    def _extract_structured_content(self, file_path: str, file_type: str) -> str:
        """Extract content from structured files"""
        try:
            if file_type == 'csv':
                df = pd.read_csv(file_path)
            elif file_type == 'excel':
                df = pd.read_excel(file_path)
            else:
                return ""
            
            # Convert dataframe to text representation
            content = f"Columns: {', '.join(df.columns)}\n"
            content += f"Records: {len(df)}\n"
            content += f"Sample data:\n{df.head(10).to_string()}\n"
            
            return content
        except Exception as e:
            logger.error(f"Error extracting structured content: {e}")
            return ""
    
    def detect_duplicate_transactions(self, transactions: List[Dict]) -> List[Dict]:
        """Detect duplicate transactions using fuzzy matching"""
        if not FUZZY_AVAILABLE:
            return []
        
        duplicates = []
        processed = set()
        
        for i, transaction1 in enumerate(transactions):
            if i in processed:
                continue
            
            duplicate_group = []
            
            for j, transaction2 in enumerate(transactions[i+1:], i+1):
                if j in processed:
                    continue
                
                # Check for exact duplicates
                if self._is_exact_duplicate(transaction1, transaction2):
                    duplicate_group.append({
                        'index': j,
                        'transaction': transaction2,
                        'similarity': 100,
                        'type': 'exact'
                    })
                    processed.add(j)
                
                # Check for fuzzy duplicates
                elif self._is_fuzzy_duplicate(transaction1, transaction2):
                    similarity = self._calculate_similarity(transaction1, transaction2)
                    if similarity > 85:  # 85% similarity threshold
                        duplicate_group.append({
                            'index': j,
                            'transaction': transaction2,
                            'similarity': similarity,
                            'type': 'fuzzy'
                        })
                        processed.add(j)
            
            if duplicate_group:
                duplicates.append({
                    'group_id': f"group_{i}",
                    'original_index': i,
                    'original_transaction': transaction1,
                    'duplicates': duplicate_group,
                    'total_duplicates': len(duplicate_group)
                })
                processed.add(i)
        
        return duplicates
    
    def _is_exact_duplicate(self, trans1: Dict, trans2: Dict) -> bool:
        """Check if two transactions are exact duplicates"""
        key_fields = ['transaction_date', 'transaction_value', 'building_name', 'apartment_number']
        
        for field in key_fields:
            if field in trans1 and field in trans2:
                if str(trans1[field]).strip() != str(trans2[field]).strip():
                    return False
            elif field in trans1 or field in trans2:
                return False
        
        return True
    
    def _is_fuzzy_duplicate(self, trans1: Dict, trans2: Dict) -> bool:
        """Check if two transactions are fuzzy duplicates"""
        # Check building name similarity
        building1 = str(trans1.get('building_name', '')).lower()
        building2 = str(trans2.get('building_name', '')).lower()
        
        if building1 and building2:
            building_similarity = fuzz.ratio(building1, building2)
            if building_similarity > 80:
                return True
        
        # Check other key fields
        key_fields = ['transaction_date', 'transaction_value', 'apartment_number']
        matching_fields = 0
        
        for field in key_fields:
            if field in trans1 and field in trans2:
                val1 = str(trans1[field]).strip()
                val2 = str(trans2[field]).strip()
                if val1 and val2:
                    similarity = fuzz.ratio(val1, val2)
                    if similarity > 90:
                        matching_fields += 1
        
        return matching_fields >= 2  # At least 2 fields must match
    
    def _calculate_similarity(self, trans1: Dict, trans2: Dict) -> float:
        """Calculate overall similarity between two transactions"""
        similarities = []
        
        for field in ['building_name', 'apartment_number', 'transaction_value']:
            if field in trans1 and field in trans2:
                val1 = str(trans1[field]).strip()
                val2 = str(trans2[field]).strip()
                if val1 and val2:
                    similarity = fuzz.ratio(val1, val2)
                    similarities.append(similarity)
        
        return sum(similarities) / len(similarities) if similarities else 0
    
    def standardize_building_name(self, building_name: str) -> str:
        """Standardize building names to handle variations"""
        building_lower = building_name.lower().strip()
        
        # Check against known variations
        for standard_name, variations in self.building_variations.items():
            if building_lower in variations:
                return standard_name.title()
        
        # Try fuzzy matching
        if FUZZY_AVAILABLE:
            all_variations = []
            for variations in self.building_variations.values():
                all_variations.extend(variations)
            
            best_match = process.extractOne(building_lower, all_variations)
            if best_match and best_match[1] > 80:
                # Find the standard name for this variation
                for standard_name, variations in self.building_variations.items():
                    if best_match[0] in variations:
                        return standard_name.title()
        
        # Return cleaned original name
        return building_name.strip().title()
    
    def clean_transaction_data(self, transactions: List[Dict]) -> List[Dict]:
        """Clean and standardize transaction data"""
        cleaned = []
        
        for transaction in transactions:
            cleaned_transaction = {}
            
            for key, value in transaction.items():
                if key == 'building_name':
                    cleaned_transaction[key] = self.standardize_building_name(str(value))
                elif key == 'transaction_value':
                    cleaned_transaction[key] = self._clean_numeric_value(value)
                elif key == 'transaction_date':
                    cleaned_transaction[key] = self._clean_date_value(value)
                else:
                    cleaned_transaction[key] = self._clean_general_value(value)
            
            cleaned.append(cleaned_transaction)
        
        return cleaned
    
    def _clean_numeric_value(self, value) -> float:
        """Clean numeric values"""
        if pd.isna(value):
            return 0.0
        
        value_str = str(value).strip()
        # Remove currency symbols and commas
        value_str = re.sub(r'[AED$,€£]', '', value_str)
        value_str = value_str.replace(',', '')
        
        try:
            return float(value_str)
        except:
            return 0.0
    
    def _clean_date_value(self, value) -> str:
        """Clean date values"""
        if pd.isna(value):
            return ""
        
        try:
            # Try to parse as datetime
            if isinstance(value, str):
                # Handle various date formats
                date_formats = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y']
                for fmt in date_formats:
                    try:
                        parsed_date = pd.to_datetime(value, format=fmt)
                        return parsed_date.strftime('%Y-%m-%d')
                    except:
                        continue
            
            # Fallback to pandas parsing
            parsed_date = pd.to_datetime(value)
            return parsed_date.strftime('%Y-%m-%d')
        except:
            return str(value)
    
    def _clean_general_value(self, value) -> str:
        """Clean general text values"""
        if pd.isna(value):
            return ""
        
        return str(value).strip()
    
    def generate_insights(self, transactions: List[Dict]) -> Dict[str, Any]:
        """Generate insights from transaction data"""
        if not transactions:
            return {}
        
        insights = {
            'total_transactions': len(transactions),
            'total_value': 0,
            'average_value': 0,
            'top_buildings': [],
            'top_buyer_countries': [],
            'date_range': {}
        }
        
        # Calculate total and average values
        values = [t.get('transaction_value', 0) for t in transactions if t.get('transaction_value', 0) > 0]
        if values:
            insights['total_value'] = sum(values)
            insights['average_value'] = sum(values) / len(values)
        
        # Top buildings
        building_counts = defaultdict(int)
        for t in transactions:
            building = t.get('building_name', '')
            if building:
                building_counts[building] += 1
        
        insights['top_buildings'] = sorted(building_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Top buyer countries
        country_counts = defaultdict(int)
        for t in transactions:
            country = t.get('buyer_country', '')
            if country:
                country_counts[country] += 1
        
        insights['top_buyer_countries'] = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return insights
    
    def generate_recommendations(self, duplicates: List[Dict], transactions: List[Dict]) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if duplicates:
            recommendations.append(f"Found {len(duplicates)} groups of duplicate transactions")
            recommendations.append("Review and merge duplicate records to maintain data integrity")
        
        if transactions:
            total_value = sum([t.get('transaction_value', 0) for t in transactions])
            if total_value > 0:
                recommendations.append(f"Total transaction value: AED {total_value:,.0f}")
                recommendations.append("Consider market trends and investment opportunities")
        
        return recommendations
