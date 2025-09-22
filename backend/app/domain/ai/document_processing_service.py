"""
Document Processing Service for Dubai Real Estate RAG System

This service handles document uploads and extracts property information
including unit numbers, communities, building names, and property types.
"""

import re
import logging
from typing import Dict, List, Optional, Any, Tuple
from sqlalchemy import create_engine, text
import os
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class DocumentProcessingService:
    """Service for processing uploaded documents and extracting property information"""
    
    def __init__(self, db_url: str = None):
        self.db_url = db_url or os.getenv("DATABASE_URL", "postgresql://admin:password123@postgres:5432/real_estate_db")
        self.engine = create_engine(self.db_url)
        
        # Property information patterns for document extraction
        self.unit_patterns = [
            r'unit\s+(\d+)',
            r'apartment\s+(\d+)',
            r'apt\s+(\d+)',
            r'flat\s+(\d+)',
            r'unit\s+no\.?\s*(\d+)',
            r'apartment\s+no\.?\s*(\d+)',
            r'flat\s+no\.?\s*(\d+)',
            r'(\d+)\s+bedroom',
            r'(\d+)\s+br',
            r'(\d+)\s+bed'
        ]
        
        self.building_patterns = [
            r'(\d+)\s+(\w+)\s+(tower|building|residence|apartments|complex|plaza|center|towers)',
            r'(\w+)\s+(tower|building|residence|apartments|complex|plaza|center|towers)',
            r'(\w+)\s+(\d+)\s+(tower|building|residence|apartments|complex|plaza|center|towers)',
            r'(\w+)\s+(\w+)\s+(tower|building|residence|apartments|complex|plaza|center|towers)',
        ]
        
        self.community_patterns = [
            r'dubai\s+marina',
            r'downtown\s+dubai',
            r'palm\s+jumeirah',
            r'business\s+bay',
            r'jumeirah\s+beach\s+residence',
            r'dubai\s+hills\s+estate',
            r'arabian\s+ranches',
            r'emirates\s+hills',
            r'jumeirah\s+village\s+circle',
            r'jumeirah\s+village\s+triangle',
            r'motor\s+city',
            r'dubai\s+silicon\s+oasis',
            r'dubai\s+investment\s+park',
            r'dubai\s+media\s+city',
            r'dubai\s+internet\s+city',
            r'dubai\s+knowledge\s+village',
            r'dubai\s+international\s+financial\s+centre',
            r'jumeirah\s+lake\s+towers',
            r'dubai\s+festival\s+city',
            r'dubai\s+healthcare\s+city'
        ]
        
        self.property_type_patterns = {
            'apartment': [r'apartment', r'apt', r'flat', r'unit', r'condo', r'condominium'],
            'villa': [r'villa', r'house', r'detached', r'standalone'],
            'townhouse': [r'townhouse', r'terrace', r'row\s+house'],
            'penthouse': [r'penthouse', r'duplex', r'maisonette'],
            'studio': [r'studio', r'efficiency', r'bachelor']
        }
        
        self.price_patterns = [
            r'aed\s+(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s+aed',
            r'usd\s+(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s+usd',
            r'price\s*:?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'value\s*:?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
        ]
        
        self.size_patterns = [
            r'(\d+)\s*sqft',
            r'(\d+)\s*sq\s*ft',
            r'(\d+)\s*square\s*feet',
            r'(\d+)\s*sqm',
            r'(\d+)\s*square\s*meters',
            r'area\s*:?\s*(\d+)',
            r'size\s*:?\s*(\d+)'
        ]
    
    def process_document(self, document_content: str, document_type: str = None) -> Dict[str, Any]:
        """
        Process uploaded document and extract property information
        
        Args:
            document_content: Content of the uploaded document
            document_type: Type of document (optional)
            
        Returns:
            Extracted property information and metadata
        """
        try:
            # Clean and normalize document content
            cleaned_content = self._clean_document_content(document_content)
            
            # Extract property information
            extracted_info = self._extract_property_information(cleaned_content)
            
            # Determine document type if not provided
            if not document_type:
                document_type = self._detect_document_type(cleaned_content)
            
            # Create processing result
            result = {
                'document_type': document_type,
                'extracted_property': extracted_info,
                'processing_timestamp': datetime.now().isoformat(),
                'content_length': len(document_content),
                'confidence_score': self._calculate_confidence_score(extracted_info),
                'processing_status': 'success'
            }
            
            # Store in database if significant information was extracted
            if extracted_info.get('confidence', 0) > 0.3:
                self._store_extracted_data(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            return {
                'document_type': document_type or 'unknown',
                'extracted_property': {},
                'processing_timestamp': datetime.now().isoformat(),
                'processing_status': 'error',
                'error': str(e)
            }
    
    def _clean_document_content(self, content: str) -> str:
        """Clean and normalize document content for better extraction"""
        try:
            # Remove extra whitespace and normalize
            cleaned = re.sub(r'\s+', ' ', content.strip())
            
            # Remove special characters that might interfere with pattern matching
            cleaned = re.sub(r'[^\w\s\d.,-]', ' ', cleaned)
            
            # Normalize common abbreviations
            cleaned = re.sub(r'\bapt\b', 'apartment', cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(r'\bbr\b', 'bedroom', cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(r'\bba\b', 'bathroom', cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(r'\bsqft\b', 'sqft', cleaned, flags=re.IGNORECASE)
            
            return cleaned.lower()
            
        except Exception as e:
            logger.error(f"Error cleaning document content: {e}")
            return content.lower()
    
    def _extract_property_information(self, content: str) -> Dict[str, Any]:
        """Extract property information from document content"""
        try:
            extracted = {
                'unit_number': None,
                'building_name': None,
                'community': None,
                'property_type': None,
                'bedrooms': None,
                'bathrooms': None,
                'size_sqft': None,
                'price': None,
                'address': None,
                'confidence': 0.0,
                'extracted_entities': []
            }
            
            # Extract unit number
            unit_number = self._extract_unit_number(content)
            if unit_number:
                extracted['unit_number'] = unit_number
                extracted['confidence'] += 0.2
                extracted['extracted_entities'].append(f"Unit: {unit_number}")
            
            # Extract building name
            building_name = self._extract_building_name(content)
            if building_name:
                extracted['building_name'] = building_name
                extracted['confidence'] += 0.3
                extracted['extracted_entities'].append(f"Building: {building_name}")
            
            # Extract community
            community = self._extract_community(content)
            if community:
                extracted['community'] = community
                extracted['confidence'] += 0.2
                extracted['extracted_entities'].append(f"Community: {community}")
            
            # Extract property type
            property_type = self._extract_property_type(content)
            if property_type:
                extracted['property_type'] = property_type
                extracted['confidence'] += 0.1
                extracted['extracted_entities'].append(f"Type: {property_type}")
            
            # Extract bedrooms
            bedrooms = self._extract_bedrooms(content)
            if bedrooms:
                extracted['bedrooms'] = bedrooms
                extracted['confidence'] += 0.1
                extracted['extracted_entities'].append(f"Bedrooms: {bedrooms}")
            
            # Extract bathrooms
            bathrooms = self._extract_bathrooms(content)
            if bathrooms:
                extracted['bathrooms'] = bathrooms
                extracted['confidence'] += 0.1
                extracted['extracted_entities'].append(f"Bathrooms: {bathrooms}")
            
            # Extract size
            size = self._extract_size(content)
            if size:
                extracted['size_sqft'] = size
                extracted['confidence'] += 0.1
                extracted['extracted_entities'].append(f"Size: {size} sqft")
            
            # Extract price
            price = self._extract_price(content)
            if price:
                extracted['price'] = price
                extracted['confidence'] += 0.1
                extracted['extracted_entities'].append(f"Price: AED {price:,.0f}")
            
            # Build address from extracted components
            address_parts = []
            if extracted['building_name']:
                address_parts.append(extracted['building_name'])
            if extracted['community']:
                address_parts.append(extracted['community'])
            if extracted['unit_number']:
                address_parts.append(f"Unit {extracted['unit_number']}")
            
            if address_parts:
                extracted['address'] = ', '.join(address_parts)
            
            return extracted
            
        except Exception as e:
            logger.error(f"Error extracting property information: {e}")
            return {'confidence': 0.0, 'error': str(e)}
    
    def _extract_unit_number(self, content: str) -> Optional[str]:
        """Extract unit number from content"""
        try:
            for pattern in self.unit_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    return match.group(1)
            return None
        except Exception as e:
            logger.error(f"Error extracting unit number: {e}")
            return None
    
    def _extract_building_name(self, content: str) -> Optional[str]:
        """Extract building name from content"""
        try:
            for pattern in self.building_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    groups = match.groups()
                    if len(groups) >= 2:
                        return ' '.join(groups).title()
            return None
        except Exception as e:
            logger.error(f"Error extracting building name: {e}")
            return None
    
    def _extract_community(self, content: str) -> Optional[str]:
        """Extract community from content"""
        try:
            for pattern in self.community_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    return match.group(0).title()
            return None
        except Exception as e:
            logger.error(f"Error extracting community: {e}")
            return None
    
    def _extract_property_type(self, content: str) -> Optional[str]:
        """Extract property type from content"""
        try:
            for prop_type, patterns in self.property_type_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        return prop_type
            return None
        except Exception as e:
            logger.error(f"Error extracting property type: {e}")
            return None
    
    def _extract_bedrooms(self, content: str) -> Optional[int]:
        """Extract number of bedrooms from content"""
        try:
            bedroom_patterns = [
                r'(\d+)\s*bedroom',
                r'(\d+)\s*br',
                r'(\d+)\s*bed'
            ]
            
            for pattern in bedroom_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    return int(match.group(1))
            return None
        except Exception as e:
            logger.error(f"Error extracting bedrooms: {e}")
            return None
    
    def _extract_bathrooms(self, content: str) -> Optional[int]:
        """Extract number of bathrooms from content"""
        try:
            bathroom_patterns = [
                r'(\d+)\s*bathroom',
                r'(\d+)\s*ba',
                r'(\d+)\s*bath'
            ]
            
            for pattern in bathroom_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    return int(match.group(1))
            return None
        except Exception as e:
            logger.error(f"Error extracting bathrooms: {e}")
            return None
    
    def _extract_size(self, content: str) -> Optional[float]:
        """Extract property size from content"""
        try:
            for pattern in self.size_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    size = float(match.group(1))
                    # Convert sqm to sqft if needed
                    if 'sqm' in pattern or 'square meters' in pattern:
                        size = size * 10.764  # Convert sqm to sqft
                    return size
            return None
        except Exception as e:
            logger.error(f"Error extracting size: {e}")
            return None
    
    def _extract_price(self, content: str) -> Optional[float]:
        """Extract price from content"""
        try:
            for pattern in self.price_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    price_str = match.group(1).replace(',', '')
                    price = float(price_str)
                    
                    # Convert USD to AED if needed (approximate rate)
                    if 'usd' in pattern:
                        price = price * 3.67  # Approximate USD to AED conversion
                    
                    return price
            return None
        except Exception as e:
            logger.error(f"Error extracting price: {e}")
            return None
    
    def _detect_document_type(self, content: str) -> str:
        """Detect the type of document based on content"""
        try:
            content_lower = content.lower()
            
            # Check for specific document types
            if any(word in content_lower for word in ['sale', 'purchase', 'buy', 'sell', 'transaction']):
                return 'sale_agreement'
            elif any(word in content_lower for word in ['rent', 'lease', 'tenancy', 'rental']):
                return 'rental_agreement'
            elif any(word in content_lower for word in ['title', 'deed', 'ownership', 'property deed']):
                return 'title_deed'
            elif any(word in content_lower for word in ['valuation', 'appraisal', 'assessment', 'cma']):
                return 'valuation_report'
            elif any(word in content_lower for word in ['contract', 'agreement', 'terms', 'conditions']):
                return 'contract_document'
            else:
                return 'property_document'
                
        except Exception as e:
            logger.error(f"Error detecting document type: {e}")
            return 'unknown'
    
    def _calculate_confidence_score(self, extracted_info: Dict[str, Any]) -> float:
        """Calculate confidence score for extracted information"""
        try:
            base_confidence = extracted_info.get('confidence', 0.0)
            
            # Boost confidence for complete information
            if extracted_info.get('building_name') and extracted_info.get('community'):
                base_confidence += 0.1
            
            if extracted_info.get('unit_number') and extracted_info.get('property_type'):
                base_confidence += 0.1
            
            if extracted_info.get('bedrooms') and extracted_info.get('bathrooms'):
                base_confidence += 0.1
            
            # Cap at 1.0
            return min(base_confidence, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating confidence score: {e}")
            return 0.0
    
    def _store_extracted_data(self, result: Dict[str, Any]) -> bool:
        """Store extracted property data in database"""
        try:
            with self.engine.connect() as conn:
                # Create or update property record
                extracted = result['extracted_property']
                
                if extracted.get('address'):
                    # Check if property already exists
                    existing = conn.execute(text("""
                        SELECT id FROM properties WHERE LOWER(address) = LOWER(:address)
                    """), {"address": extracted['address']}).fetchone()
                    
                    if existing:
                        # Update existing property
                        conn.execute(text("""
                            UPDATE properties SET
                                property_type = COALESCE(:property_type, property_type),
                                bedrooms = COALESCE(:bedrooms, bedrooms),
                                bathrooms = COALESCE(:bathrooms, bathrooms),
                                square_feet = COALESCE(:size_sqft, square_feet),
                                price = COALESCE(:price, price),
                                updated_at = CURRENT_TIMESTAMP
                            WHERE id = :id
                        """), {
                            "id": existing[0],
                            "property_type": extracted.get('property_type'),
                            "bedrooms": extracted.get('bedrooms'),
                            "bathrooms": extracted.get('bathrooms'),
                            "size_sqft": extracted.get('size_sqft'),
                            "price": extracted.get('price')
                        })
                    else:
                        # Insert new property
                        conn.execute(text("""
                            INSERT INTO properties (
                                address, property_type, bedrooms, bathrooms, 
                                square_feet, price, description, created_at
                            ) VALUES (
                                :address, :property_type, :bedrooms, :bathrooms,
                                :size_sqft, :price, :description, CURRENT_TIMESTAMP
                            )
                        """), {
                            "address": extracted['address'],
                            "property_type": extracted.get('property_type', 'apartment'),
                            "bedrooms": extracted.get('bedrooms'),
                            "bathrooms": extracted.get('bathrooms'),
                            "size_sqft": extracted.get('size_sqft'),
                            "price": extracted.get('price'),
                            "description": f"Property extracted from {result['document_type']} document"
                        })
                    
                    conn.commit()
                    logger.info(f"Stored extracted property data: {extracted['address']}")
                    return True
                
                return False
                
        except Exception as e:
            logger.error(f"Error storing extracted data: {e}")
            return False
    
    def get_property_by_extracted_info(self, extracted_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get property from database based on extracted information"""
        try:
            with self.engine.connect() as conn:
                query_parts = []
                params = {}
                
                if extracted_info.get('address'):
                    query_parts.append("LOWER(address) LIKE LOWER(:address)")
                    params['address'] = f"%{extracted_info['address']}%"
                
                if extracted_info.get('building_name'):
                    query_parts.append("(LOWER(address) LIKE LOWER(:building_name) OR LOWER(title) LIKE LOWER(:building_name))")
                    params['building_name'] = f"%{extracted_info['building_name']}%"
                
                if extracted_info.get('community'):
                    query_parts.append("LOWER(location) LIKE LOWER(:community)")
                    params['community'] = f"%{extracted_info['community']}%"
                
                if not query_parts:
                    return None
                
                query = f"""
                    SELECT id, title, address, price, bedrooms, bathrooms, square_feet, 
                           property_type, description, location, created_at
                    FROM properties 
                    WHERE {' AND '.join(query_parts)}
                    ORDER BY created_at DESC
                    LIMIT 1
                """
                
                result = conn.execute(text(query), params)
                row = result.fetchone()
                
                if row:
                    return dict(row._mapping)
                
                return None
                
        except Exception as e:
            logger.error(f"Error getting property by extracted info: {e}")
            return None
