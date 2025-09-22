"""
Property Detection Service for Dubai Real Estate RAG System

This service handles intelligent property detection from user requests,
database queries for specific buildings, and property data extraction.
"""

import re
import logging
from typing import Dict, List, Optional, Any, Tuple
from sqlalchemy import create_engine, text
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class PropertyDetectionService:
    """Service for detecting and querying property information from user requests"""
    
    def __init__(self, db_url: str = None):
        self.db_url = db_url or os.getenv("DATABASE_URL", "postgresql://admin:password123@postgres:5432/real_estate_db")
        self.engine = create_engine(self.db_url)
        
        # Dubai building and community patterns
        self.building_patterns = [
            r'(\d+)\s+(\w+)\s+(tower|building|residence|apartments|complex|plaza|center|towers)',
            r'(\w+)\s+(tower|building|residence|apartments|complex|plaza|center|towers)',
            r'(\w+)\s+(\d+)\s+(tower|building|residence|apartments|complex|plaza|center|towers)',
            r'(\w+)\s+(\w+)\s+(tower|building|residence|apartments|complex|plaza|center|towers)',
        ]
        
        # Unit number patterns
        self.unit_patterns = [
            r'unit\s+(\d+)',
            r'apartment\s+(\d+)',
            r'apt\s+(\d+)',
            r'flat\s+(\d+)',
            r'(\d+)\s+bedroom',
            r'(\d+)\s+br',
            r'(\d+)\s+bed'
        ]
        
        # Dubai communities and areas
        self.dubai_communities = [
            'dubai marina', 'marina', 'downtown dubai', 'downtown', 'palm jumeirah', 'palm',
            'business bay', 'jbr', 'jumeirah beach residence', 'dubai hills estate', 'dubai hills',
            'arabian ranches', 'emirates hills', 'jumeirah', 'dubai sports city', 'sports city',
            'international city', 'discovery gardens', 'jumeirah village circle', 'jvc',
            'jumeirah village triangle', 'jvt', 'motor city', 'dubai silicon oasis', 'dso',
            'dubai investment park', 'dip', 'dubai land', 'dubai production city', 'dpc',
            'dubai media city', 'dmc', 'dubai internet city', 'dic', 'dubai knowledge village', 'dkv',
            'dubai international financial centre', 'difc', 'dubai world trade centre', 'dwtc',
            'burj khalifa', 'burj al arab', 'jumeirah lake towers', 'jlt', 'dubai festival city',
            'dubai healthcare city', 'dhcc', 'dubai autodrome', 'dubai motor city', 'collective',
            'collective tower', '413 collective', '413 collective tower'
        ]
        
        # Property type variations
        self.property_types = {
            'apartment': ['apartment', 'apt', 'flat', 'unit', 'condo', 'condominium', 'residential unit'],
            'villa': ['villa', 'house', 'detached', 'standalone', 'independent villa'],
            'townhouse': ['townhouse', 'townhouse', 'terrace', 'row house', 'linked villa'],
            'penthouse': ['penthouse', 'duplex', 'maisonette', 'penthouse apartment'],
            'studio': ['studio', 'efficiency', 'bachelor', 'studio apartment']
        }
    
    def detect_property_from_request(self, user_message: str) -> Dict[str, Any]:
        """
        Detect property information from user request
        
        Args:
            user_message: User's message containing property request
            
        Returns:
            Dictionary with detected property information
        """
        try:
            message_lower = user_message.lower()
            
            # Initialize result
            result = {
                'building_name': None,
                'unit_number': None,
                'community': None,
                'property_type': None,
                'bedrooms': None,
                'bathrooms': None,
                'size_sqft': None,
                'confidence': 0.0,
                'detected_entities': []
            }
            
            # Detect building name
            building_info = self._detect_building_name(message_lower)
            if building_info:
                result['building_name'] = building_info['name']
                result['community'] = building_info.get('community')
                result['confidence'] += 0.3
                result['detected_entities'].append(f"Building: {building_info['name']}")
            
            # Detect unit number
            unit_number = self._detect_unit_number(message_lower)
            if unit_number:
                result['unit_number'] = unit_number
                result['confidence'] += 0.2
                result['detected_entities'].append(f"Unit: {unit_number}")
            
            # Detect property type
            property_type = self._detect_property_type(message_lower)
            if property_type:
                result['property_type'] = property_type
                result['confidence'] += 0.2
                result['detected_entities'].append(f"Type: {property_type}")
            
            # Detect bedrooms
            bedrooms = self._detect_bedrooms(message_lower)
            if bedrooms:
                result['bedrooms'] = bedrooms
                result['confidence'] += 0.1
                result['detected_entities'].append(f"Bedrooms: {bedrooms}")
            
            # Detect bathrooms
            bathrooms = self._detect_bathrooms(message_lower)
            if bathrooms:
                result['bathrooms'] = bathrooms
                result['confidence'] += 0.1
                result['detected_entities'].append(f"Bathrooms: {bathrooms}")
            
            # Detect size
            size = self._detect_size(message_lower)
            if size:
                result['size_sqft'] = size
                result['confidence'] += 0.1
                result['detected_entities'].append(f"Size: {size} sqft")
            
            return result
            
        except Exception as e:
            logger.error(f"Error detecting property from request: {e}")
            return {'confidence': 0.0, 'error': str(e)}
    
    def _detect_building_name(self, message: str) -> Optional[Dict[str, str]]:
        """Detect building name from message"""
        try:
            # Check for specific building patterns
            for pattern in self.building_patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    groups = match.groups()
                    if len(groups) >= 2:
                        building_name = ' '.join(groups).title()
                        
                        # Determine community
                        community = self._detect_community_from_building(building_name, message)
                        
                        return {
                            'name': building_name,
                            'community': community
                        }
            
            # Check for known Dubai buildings
            for community in self.dubai_communities:
                if community in message:
                    return {
                        'name': community.title(),
                        'community': community.title()
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error detecting building name: {e}")
            return None
    
    def _detect_community_from_building(self, building_name: str, message: str) -> str:
        """Detect community from building name and context"""
        try:
            # Check if community is mentioned in the message
            for community in self.dubai_communities:
                if community in message and community != building_name.lower():
                    return community.title()
            
            # Default community based on building name
            if 'collective' in building_name.lower():
                return 'Business Bay'
            elif 'marina' in building_name.lower():
                return 'Dubai Marina'
            elif 'downtown' in building_name.lower():
                return 'Downtown Dubai'
            elif 'palm' in building_name.lower():
                return 'Palm Jumeirah'
            else:
                return 'Dubai'
                
        except Exception as e:
            logger.error(f"Error detecting community: {e}")
            return 'Dubai'
    
    def _detect_unit_number(self, message: str) -> Optional[str]:
        """Detect unit number from message"""
        try:
            for pattern in self.unit_patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    return match.group(1)
            return None
        except Exception as e:
            logger.error(f"Error detecting unit number: {e}")
            return None
    
    def _detect_property_type(self, message: str) -> Optional[str]:
        """Detect property type from message"""
        try:
            for prop_type, variations in self.property_types.items():
                for variation in variations:
                    if variation in message:
                        return prop_type
            return None
        except Exception as e:
            logger.error(f"Error detecting property type: {e}")
            return None
    
    def _detect_bedrooms(self, message: str) -> Optional[int]:
        """Detect number of bedrooms from message"""
        try:
            bedroom_patterns = [
                r'(\d+)\s*bedroom',
                r'(\d+)\s*br',
                r'(\d+)\s*bed'
            ]
            
            for pattern in bedroom_patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    return int(match.group(1))
            return None
        except Exception as e:
            logger.error(f"Error detecting bedrooms: {e}")
            return None
    
    def _detect_bathrooms(self, message: str) -> Optional[int]:
        """Detect number of bathrooms from message"""
        try:
            bathroom_patterns = [
                r'(\d+)\s*bathroom',
                r'(\d+)\s*ba',
                r'(\d+)\s*bath'
            ]
            
            for pattern in bathroom_patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    return int(match.group(1))
            return None
        except Exception as e:
            logger.error(f"Error detecting bathrooms: {e}")
            return None
    
    def _detect_size(self, message: str) -> Optional[float]:
        """Detect property size from message"""
        try:
            size_patterns = [
                r'(\d+)\s*sqft',
                r'(\d+)\s*sq\s*ft',
                r'(\d+)\s*square\s*feet'
            ]
            
            for pattern in size_patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    return float(match.group(1))
            return None
        except Exception as e:
            logger.error(f"Error detecting size: {e}")
            return None
    
    def query_property_from_database(self, property_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Query property details from database based on detected information
        
        Args:
            property_info: Detected property information
            
        Returns:
            Property details from database or None if not found
        """
        try:
            with self.engine.connect() as conn:
                # Build query based on available information
                query_parts = []
                params = {}
                
                if property_info.get('building_name'):
                    # Search for building name in address or title
                    query_parts.append("(LOWER(address) LIKE LOWER(:building_name) OR LOWER(title) LIKE LOWER(:building_name))")
                    params['building_name'] = f"%{property_info['building_name']}%"
                
                if property_info.get('community'):
                    query_parts.append("LOWER(location) LIKE LOWER(:community)")
                    params['community'] = f"%{property_info['community']}%"
                
                if property_info.get('property_type'):
                    query_parts.append("LOWER(property_type) = LOWER(:property_type)")
                    params['property_type'] = property_info['property_type']
                
                if property_info.get('bedrooms'):
                    query_parts.append("bedrooms = :bedrooms")
                    params['bedrooms'] = property_info['bedrooms']
                
                if property_info.get('bathrooms'):
                    query_parts.append("bathrooms = :bathrooms")
                    params['bathrooms'] = property_info['bathrooms']
                
                if not query_parts:
                    return None
                
                # Execute query
                query = f"""
                    SELECT id, title, address, price, bedrooms, bathrooms, square_feet, 
                           property_type, description, location, created_at
                    FROM properties 
                    WHERE {' AND '.join(query_parts)}
                    ORDER BY created_at DESC
                    LIMIT 5
                """
                
                result = conn.execute(text(query), params)
                rows = result.fetchall()
                
                if rows:
                    # Return the most relevant property
                    property_data = dict(rows[0]._mapping)
                    
                    # Add additional context
                    property_data['query_confidence'] = property_info.get('confidence', 0.0)
                    property_data['detected_entities'] = property_info.get('detected_entities', [])
                    property_data['search_criteria'] = property_info
                    
                    return property_data
                
                return None
                
        except Exception as e:
            logger.error(f"Error querying property from database: {e}")
            return None
    
    def get_building_specific_transactions(self, building_name: str, community: str = None) -> List[Dict[str, Any]]:
        """
        Get building-specific transaction data for CMA generation
        
        Args:
            building_name: Name of the building
            community: Community/area of the building
            
        Returns:
            List of transaction data for the building
        """
        try:
            with self.engine.connect() as conn:
                # Query for similar properties in the same building/community
                query = """
                    SELECT id, title, address, price, bedrooms, bathrooms, square_feet, 
                           property_type, description, location, created_at,
                           price / NULLIF(square_feet, 0) as price_per_sqft
                    FROM properties 
                    WHERE (LOWER(address) LIKE LOWER(:building_name) 
                           OR LOWER(title) LIKE LOWER(:building_name))
                """
                
                params = {'building_name': f"%{building_name}%"}
                
                if community:
                    query += " AND LOWER(location) LIKE LOWER(:community)"
                    params['community'] = f"%{community}%"
                
                query += " ORDER BY created_at DESC LIMIT 10"
                
                result = conn.execute(text(query), params)
                rows = result.fetchall()
                
                transactions = []
                for row in rows:
                    transaction = dict(row._mapping)
                    transactions.append(transaction)
                
                return transactions
                
        except Exception as e:
            logger.error(f"Error getting building-specific transactions: {e}")
            return []
    
    def get_community_market_data(self, community: str) -> Dict[str, Any]:
        """
        Get market data for a specific community
        
        Args:
            community: Community/area name
            
        Returns:
            Market data for the community
        """
        try:
            with self.engine.connect() as conn:
                # Get market statistics for the community
                query = """
                    SELECT 
                        COUNT(*) as total_properties,
                        AVG(price) as avg_price,
                        MIN(price) as min_price,
                        MAX(price) as max_price,
                        AVG(price / NULLIF(square_feet, 0)) as avg_price_per_sqft,
                        AVG(bedrooms) as avg_bedrooms,
                        AVG(bathrooms) as avg_bathrooms,
                        AVG(square_feet) as avg_size
                    FROM properties 
                    WHERE LOWER(location) LIKE LOWER(:community)
                """
                
                result = conn.execute(text(query), {'community': f"%{community}%"})
                row = result.fetchone()
                
                if row:
                    market_data = dict(row._mapping)
                    market_data['community'] = community
                    market_data['last_updated'] = datetime.now().isoformat()
                    return market_data
                
                return {}
                
        except Exception as e:
            logger.error(f"Error getting community market data: {e}")
            return {}
    
    def process_document_upload(self, document_content: str) -> Dict[str, Any]:
        """
        Process uploaded document to extract property information
        
        Args:
            document_content: Content of the uploaded document
            
        Returns:
            Extracted property information
        """
        try:
            # Use the same detection logic for document content
            property_info = self.detect_property_from_request(document_content)
            
            # Additional document-specific extraction
            document_info = {
                'document_type': self._detect_document_type(document_content),
                'extracted_data': property_info,
                'processing_timestamp': datetime.now().isoformat()
            }
            
            return document_info
            
        except Exception as e:
            logger.error(f"Error processing document upload: {e}")
            return {'error': str(e)}
    
    def _detect_document_type(self, content: str) -> str:
        """Detect the type of document uploaded"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['sale', 'purchase', 'buy', 'sell']):
            return 'sale_agreement'
        elif any(word in content_lower for word in ['rent', 'lease', 'tenancy']):
            return 'rental_agreement'
        elif any(word in content_lower for word in ['title', 'deed', 'ownership']):
            return 'title_deed'
        elif any(word in content_lower for word in ['valuation', 'appraisal', 'assessment']):
            return 'valuation_report'
        else:
            return 'property_document'
