#!/usr/bin/env python3
"""
Intelligent Data Processor for Dubai Real Estate RAG System
Handles document classification, content extraction, and data quality
"""

import logging
import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
import os

# Database integration
try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    DB_AVAILABLE = True
    engine = None
    SessionLocal = None
except ImportError:
    DB_AVAILABLE = False
    engine = None
    SessionLocal = None

# ChromaDB Integration - Lazy initialization
try:
    import chromadb
    from app.core.settings import CHROMA_HOST, CHROMA_PORT
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False

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

# AI Integration
try:
    import google.generativeai as genai
    from app.core.settings import GOOGLE_API_KEY, AI_MODEL
    AI_AVAILABLE = True
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(AI_MODEL)
except ImportError:
    AI_AVAILABLE = False
    model = None

logger = logging.getLogger(__name__)

class IntelligentDataProcessor:
    """Intelligent data processor with proper classification and duplicate detection"""
    
    def __init__(self):
        # Initialize ChromaDB client lazily
        self._chroma_client = None
        
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
                r'AED\s*[\d,]+(?:\.\d{2})?',
                r'[\d,]+(?:\.\d{2})?\s*AED',
                r'[\d,]+(?:\.\d{2})?\s*million',
                r'[\d,]+(?:\.\d{2})?\s*M'
            ],
            'phone_patterns': [
                r'\+971\s*\d{2}\s*\d{3}\s*\d{4}',
                r'0\d{2}\s*\d{3}\s*\d{4}',
                r'\d{3}-\d{3}-\d{4}'
            ]
        }
    
    @property
    def chroma_client(self):
        """Lazy initialization of ChromaDB client"""
        if self._chroma_client is None and CHROMA_AVAILABLE:
            try:
                self._chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
                logger.info("ChromaDB client initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize ChromaDB client: {e}")
                self._chroma_client = None
        return self._chroma_client

    def _get_document_category(self, text_content: str) -> dict:
        """
        Uses AI to classify the document into a specific category.
        """
        if not AI_AVAILABLE or not model:
            logger.warning("AI model not available, falling back to rule-based classification")
            return self.classify_document(text_content, "text")
        
        # We only use the first 4000 characters for a quick and cheap classification
        prompt = f"""
You are a document classification specialist for a Dubai real estate company. Your task is to accurately classify the document based on its content.

**Classification Categories:**
- **transaction_sheet**: Contains tables or lists of property sales data (e.g., dates, addresses, prices).
- **legal_handbook**: Contains legal clauses, contract terms, or regulatory information (e.g., RERA rules).
- **market_report**: Contains analysis of market trends, statistics, charts, and forecasts for a specific area.
- **property_brochure**: A marketing document describing a single property for sale or rent, focusing on features and lifestyle.
- **unknown**: The document does not clearly fit any of the above categories.

Analyze the following content and respond ONLY with a single, clean JSON object in the format:
{{"category": "your_choice", "confidence": <a number between 0.0 and 1.0>}}

**Content Snippet:**
---
{text_content[:4000]}
---
"""
        try:
            response = model.generate_content(prompt)
            
            # Handle different response formats
            if hasattr(response, 'text'):
                response_text = response.text
            elif hasattr(response, 'parts'):
                response_text = response.parts[0].text if response.parts else ""
            else:
                response_text = str(response)
            
            # Clean the response text
            response_text = response_text.strip()
            
            # Try to extract JSON from the response
            if response_text.startswith('{') and response_text.endswith('}'):
                result = json.loads(response_text)
            else:
                # Try to find JSON in the response
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    # Fallback to rule-based classification
                    logger.warning(f"Could not parse AI response: {response_text}")
                    return self.classify_document(text_content, "text")
            
            return result
        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"Error in AI classification: {e}")
            # Fallback to rule-based classification
            return self.classify_document(text_content, "text")

    def classify_document(self, content: str, content_type: str = "text") -> dict:
        """
        Rule-based document classification as fallback
        """
        content_lower = content.lower()
        scores = {}
        
        for doc_type, pattern in self.classification_patterns.items():
            score = 0
            for keyword in pattern['keywords']:
                if keyword in content_lower:
                    score += pattern['weight']
            
            if score > 0:
                scores[doc_type] = score
        
        if scores:
            best_type = max(scores, key=scores.get)
            confidence = min(scores[best_type] / 100.0, 0.95)  # Cap confidence at 95%
            return {"category": best_type, "confidence": confidence}
        else:
            return {"category": "unknown", "confidence": 0.1}

    def extract_content(self, file_path: str, file_type: str) -> Optional[str]:
        """
        Extract text content from various file types
        """
        try:
            if file_type.lower() == 'pdf':
                return self._extract_pdf_content(file_path)
            elif file_type.lower() in ['txt', 'text']:
                return self._extract_text_content(file_path)
            elif file_type.lower() in ['docx', 'doc']:
                return self._extract_docx_content(file_path)
            else:
                logger.warning(f"Unsupported file type: {file_type}")
                return None
        except Exception as e:
            logger.error(f"Error extracting content from {file_path}: {e}")
            return None

    def _extract_pdf_content(self, file_path: str) -> str:
        """Extract text content from PDF files"""
        content = ""
        
        if PDFPLUMBER_AVAILABLE:
            try:
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            content += page_text + "\n"
            except Exception as e:
                logger.warning(f"pdfplumber failed, trying PyPDF2: {e}")
        
        if not content and PDF_AVAILABLE:
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        content += page.extract_text() + "\n"
            except Exception as e:
                logger.error(f"PyPDF2 extraction failed: {e}")
        
        return content.strip()

    def _extract_text_content(self, file_path: str) -> str:
        """Extract text content from text files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    return file.read()
            except Exception as e:
                logger.error(f"Text file extraction failed: {e}")
                return ""

    def _extract_docx_content(self, file_path: str) -> str:
        """Extract text content from DOCX files"""
        try:
            from docx import Document
            doc = Document(file_path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except ImportError:
            logger.warning("python-docx not available for DOCX extraction")
            return ""
        except Exception as e:
            logger.error(f"DOCX extraction failed: {e}")
            return ""

    def process_uploaded_document(self, file_path: str, file_type: str):
        """
        Orchestrates the full processing of an uploaded document.
        """
        try:
            # 1. Extract content from the document
            content = self.extract_content(file_path, file_type)
            if not content:
                raise ValueError("Could not extract content from the document.")

            # 2. Triage: Get the document category
            classification = self._get_document_category(content)
            category = classification.get("category")
            confidence = classification.get("confidence", 0.0)
            
            logger.info(f"Document classified as: {category} with confidence {confidence}")

            # 3. Route to the correct specialized extractor
            if category == 'transaction_sheet':
                return self._extract_transaction_data(content)
            elif category == 'legal_handbook':
                return self._process_legal_document(content)
            elif category == 'market_report':
                return self._process_market_report(content)
            elif category == 'property_brochure':
                return self._process_property_brochure(content)
            else:
                # Handle other categories or unknown types
                return {
                    "status": "classified", 
                    "category": category, 
                    "confidence": confidence,
                    "content_length": len(content),
                    "extracted_at": datetime.now().isoformat()
                }

        except Exception as e:
            logger.error(f"Document processing failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _extract_transaction_data(self, content: str) -> dict:
        """Extract transaction data from transaction sheets"""
        # Implementation for transaction data extraction
        return {
            "status": "extracted",
            "category": "transaction_sheet",
            "data_type": "transaction_data",
            "extracted_at": datetime.now().isoformat()
        }

    def _process_legal_document(self, content: str) -> dict:
        """Process legal documents and extract key information"""
        # Implementation for legal document processing
        return {
            "status": "processed",
            "category": "legal_handbook",
            "data_type": "legal_information",
            "extracted_at": datetime.now().isoformat()
        }

    def _process_market_report(self, content: str) -> dict:
        """Process market reports and extract market insights"""
        # Implementation for market report processing
        return {
            "status": "processed",
            "category": "market_report",
            "data_type": "market_insights",
            "extracted_at": datetime.now().isoformat()
        }

    def _process_property_brochure(self, content: str) -> dict:
        """Process property brochures and extract property details"""
        # Implementation for property brochure processing
        return {
            "status": "processed",
            "category": "property_brochure",
            "data_type": "property_details",
            "extracted_at": datetime.now().isoformat()
        }

    def detect_duplicates(self, new_content: str, existing_contents: List[str]) -> List[dict]:
        """
        Detect potential duplicates using fuzzy matching
        """
        if not FUZZY_AVAILABLE:
            logger.warning("Fuzzy matching not available")
            return []
        
        duplicates = []
        for i, existing_content in enumerate(existing_contents):
            similarity = fuzz.ratio(new_content.lower(), existing_content.lower())
            if similarity > 80:  # 80% similarity threshold
                duplicates.append({
                    "index": i,
                    "similarity": similarity,
                    "content_preview": existing_content[:100] + "..."
                })
        
        return duplicates

    def validate_data_quality(self, data: dict) -> dict:
        """
        Validate data quality and return quality metrics
        """
        quality_score = 0
        issues = []
        
        # Check for required fields
        required_fields = ['title', 'content', 'category']
        for field in required_fields:
            if field not in data or not data[field]:
                issues.append(f"Missing required field: {field}")
                quality_score -= 20
        
        # Check content length
        if 'content' in data and data['content']:
            content_length = len(data['content'])
            if content_length < 50:
                issues.append("Content too short (less than 50 characters)")
                quality_score -= 15
            elif content_length > 10000:
                issues.append("Content very long (over 10,000 characters)")
                quality_score -= 5
        
        # Check for price patterns
        if 'content' in data and data['content']:
            price_matches = re.findall(r'AED\s*[\d,]+(?:\.\d{2})?', data['content'])
            if price_matches:
                quality_score += 10
        
        # Normalize score to 0-100 range
        quality_score = max(0, min(100, quality_score + 50))
        
        return {
            "quality_score": quality_score,
            "issues": issues,
            "recommendations": self._get_quality_recommendations(issues)
        }

    def _get_quality_recommendations(self, issues: List[str]) -> List[str]:
        """Generate recommendations based on quality issues"""
        recommendations = []
        
        for issue in issues:
            if "Missing required field" in issue:
                recommendations.append("Ensure all required fields are populated")
            elif "Content too short" in issue:
                recommendations.append("Add more descriptive content")
            elif "Content very long" in issue:
                recommendations.append("Consider breaking content into smaller sections")
        
        if not recommendations:
            recommendations.append("Data quality is good, no immediate actions needed")
        
        return recommendations
