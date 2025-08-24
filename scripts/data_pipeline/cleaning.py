"""
Data Cleaning & Validation Layer

Handles data cleaning, validation, and standardization for real estate data.
"""

import pandas as pd
import re
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

class DataCleaner:
    """Handles data cleaning and validation"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def clean_property_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Clean property listing data"""
        cleaned_data = []
        
        for item in data:
            cleaned_item = {}
            
            # Clean address
            if 'address' in item:
                cleaned_item['address'] = self._clean_address(item['address'])
            
            # Clean price
            if 'price' in item:
                cleaned_item['price_aed'] = self._clean_price(item['price'])
            elif 'price_aed' in item:
                cleaned_item['price_aed'] = self._clean_price(item['price_aed'])
            
            # Clean bedrooms/bathrooms
            if 'bedrooms' in item:
                cleaned_item['bedrooms'] = self._extract_number(item['bedrooms'])
            if 'bathrooms' in item:
                cleaned_item['bathrooms'] = self._extract_number(item['bathrooms'])
            
            # Clean square footage
            if 'square_feet' in item:
                cleaned_item['square_feet'] = self._extract_number(item['square_feet'])
            elif 'sqft' in item:
                cleaned_item['square_feet'] = self._extract_number(item['sqft'])
            elif 'area_sqft' in item:
                cleaned_item['square_feet'] = self._extract_number(item['area_sqft'])
            
            # Standardize property type
            if 'property_type' in item:
                cleaned_item['property_type'] = self._standardize_property_type(item['property_type'])
            elif 'type' in item:
                cleaned_item['property_type'] = self._standardize_property_type(item['type'])
            
            # Clean area/neighborhood
            if 'area' in item:
                cleaned_item['area'] = self._standardize_area(item['area'])
            elif 'neighborhood' in item:
                cleaned_item['area'] = self._standardize_area(item['neighborhood'])
            elif 'location' in item:
                cleaned_item['area'] = self._standardize_area(item['location'])
            
            # Clean developer
            if 'developer' in item:
                cleaned_item['developer'] = self._clean_developer(item['developer'])
            
            # Clean amenities
            if 'amenities' in item:
                cleaned_item['amenities'] = self._clean_amenities(item['amenities'])
            
            # Clean description
            if 'description' in item:
                cleaned_item['description'] = self._clean_description(item['description'])
            
            # Add validation flags
            cleaned_item['validation_flags'] = self._validate_property_data(cleaned_item)
            
            # Add cleaning metadata
            cleaned_item['cleaned_at'] = datetime.now().isoformat()
            
            cleaned_data.append(cleaned_item)
        
        return cleaned_data
    
    def _clean_address(self, address: str) -> str:
        """Clean and standardize address"""
        if not address:
            return ""
        
        # Remove extra whitespace
        address = re.sub(r'\s+', ' ', address.strip())
        
        # Standardize common abbreviations
        address = re.sub(r'\bSt\b', 'Street', address)
        address = re.sub(r'\bAve\b', 'Avenue', address)
        address = re.sub(r'\bRd\b', 'Road', address)
        address = re.sub(r'\bBlvd\b', 'Boulevard', address)
        address = re.sub(r'\bDr\b', 'Drive', address)
        
        # Remove special characters but keep essential ones
        address = re.sub(r'[^\w\s\-\.\,\#]', '', address)
        
        return address
    
    def _clean_price(self, price: Any) -> Optional[float]:
        """Extract and clean price in AED"""
        if not price:
            return None
        
        price_str = str(price)
        
        # Remove currency symbols, commas, and spaces
        price_str = re.sub(r'[^\d\.]', '', price_str)
        
        try:
            price_float = float(price_str)
            
            # Validate reasonable price range for Dubai
            if price_float < 100000 or price_float > 100000000:
                self.logger.warning(f"Price {price_float} seems outside reasonable range")
            
            return price_float
        except ValueError:
            return None
    
    def _extract_number(self, value: Any) -> Optional[int]:
        """Extract numeric value"""
        if not value:
            return None
        
        value_str = str(value)
        numbers = re.findall(r'\d+', value_str)
        
        if numbers:
            return int(numbers[0])
        return None
    
    def _standardize_property_type(self, prop_type: str) -> str:
        """Standardize property type"""
        if not prop_type:
            return "Unknown"
        
        prop_type_lower = prop_type.lower()
        
        type_mapping = {
            'apartment': 'Apartment',
            'flat': 'Apartment',
            'condo': 'Apartment',
            'condominium': 'Apartment',
            'villa': 'Villa',
            'house': 'Villa',
            'townhouse': 'Townhouse',
            'penthouse': 'Penthouse',
            'studio': 'Studio',
            'duplex': 'Duplex',
            'maisonette': 'Maisonette',
            'loft': 'Loft'
        }
        
        for key, value in type_mapping.items():
            if key in prop_type_lower:
                return value
        
        return prop_type.title()
    
    def _standardize_area(self, area: str) -> str:
        """Standardize Dubai area names"""
        if not area:
            return "Unknown"
        
        area_lower = area.lower()
        
        area_mapping = {
            'dubai marina': 'Dubai Marina',
            'downtown dubai': 'Downtown Dubai',
            'palm jumeirah': 'Palm Jumeirah',
            'business bay': 'Business Bay',
            'dubai hills estate': 'Dubai Hills Estate',
            'jbr': 'Jumeirah Beach Residence',
            'jumeirah beach residence': 'Jumeirah Beach Residence',
            'dubai silicon oasis': 'Dubai Silicon Oasis',
            'dubai sports city': 'Dubai Sports City',
            'dubai production city': 'Dubai Production City',
            'dubai creek harbour': 'Dubai Creek Harbour',
            'dubai land': 'Dubai Land',
            'dubai internet city': 'Dubai Internet City',
            'dubai media city': 'Dubai Media City',
            'dubai knowledge park': 'Dubai Knowledge Park',
            'dubai healthcare city': 'Dubai Healthcare City',
            'dubai international city': 'Dubai International City',
            'dubai motor city': 'Dubai Motor City',
            'dubai studio city': 'Dubai Studio City',
            'dubai academic city': 'Dubai Academic City'
        }
        
        for key, value in area_mapping.items():
            if key in area_lower:
                return value
        
        return area.title()
    
    def _clean_developer(self, developer: str) -> str:
        """Clean developer name"""
        if not developer:
            return "Unknown"
        
        # Remove extra whitespace and standardize
        developer = re.sub(r'\s+', ' ', developer.strip())
        
        # Common developer name mappings
        developer_mapping = {
            'emaar properties': 'Emaar Properties',
            'nakheel': 'Nakheel',
            'damac': 'DAMAC',
            'sobek': 'Sobek',
            'meydan': 'Meydan',
            'mashreq': 'Mashreq',
            'union properties': 'Union Properties',
            'dubai properties': 'Dubai Properties',
            'dubai holding': 'Dubai Holding'
        }
        
        developer_lower = developer.lower()
        for key, value in developer_mapping.items():
            if key in developer_lower:
                return value
        
        return developer.title()
    
    def _clean_amenities(self, amenities: Any) -> List[str]:
        """Clean and standardize amenities"""
        if not amenities:
            return []
        
        if isinstance(amenities, str):
            # Split by common delimiters
            amenities_list = re.split(r'[,;|]', amenities)
        elif isinstance(amenities, list):
            amenities_list = amenities
        else:
            return []
        
        cleaned_amenities = []
        for amenity in amenities_list:
            cleaned = amenity.strip().lower()
            if cleaned:
                # Standardize common amenities
                amenity_mapping = {
                    'pool': 'Swimming Pool',
                    'gym': 'Gymnasium',
                    'parking': 'Parking',
                    'elevator': 'Elevator',
                    'ac': 'Air Conditioning',
                    'balcony': 'Balcony',
                    'garden': 'Garden',
                    'security': 'Security',
                    'concierge': 'Concierge',
                    'playground': 'Playground',
                    'bbq': 'BBQ Area',
                    'tennis': 'Tennis Court',
                    'basketball': 'Basketball Court',
                    'football': 'Football Field'
                }
                
                found = False
                for key, value in amenity_mapping.items():
                    if key in cleaned:
                        cleaned_amenities.append(value)
                        found = True
                        break
                
                if not found:
                    cleaned_amenities.append(amenity.strip().title())
        
        return list(set(cleaned_amenities))  # Remove duplicates
    
    def _clean_description(self, description: str) -> str:
        """Clean property description"""
        if not description:
            return ""
        
        # Remove extra whitespace
        description = re.sub(r'\s+', ' ', description.strip())
        
        # Remove HTML tags if present
        description = re.sub(r'<[^>]+>', '', description)
        
        # Limit length
        if len(description) > 1000:
            description = description[:1000] + "..."
        
        return description
    
    def _validate_property_data(self, data: Dict[str, Any]) -> Dict[str, bool]:
        """Validate property data and return flags"""
        flags = {
            'has_address': bool(data.get('address')),
            'has_price': data.get('price_aed') is not None,
            'has_bedrooms': data.get('bedrooms') is not None,
            'has_bathrooms': data.get('bathrooms') is not None,
            'has_square_feet': data.get('square_feet') is not None,
            'has_area': bool(data.get('area')),
            'has_property_type': bool(data.get('property_type')),
            'price_reasonable': self._validate_price_reasonableness(data.get('price_aed')),
            'bedrooms_reasonable': self._validate_bedrooms_reasonableness(data.get('bedrooms')),
            'bathrooms_reasonable': self._validate_bathrooms_reasonableness(data.get('bathrooms')),
            'square_feet_reasonable': self._validate_square_feet_reasonableness(data.get('square_feet'))
        }
        
        return flags
    
    def _validate_price_reasonableness(self, price: Optional[float]) -> bool:
        """Validate if price is reasonable for Dubai market"""
        if not price:
            return False
        
        # Dubai property prices typically range from 200K to 50M AED
        return 200000 <= price <= 50000000
    
    def _validate_bedrooms_reasonableness(self, bedrooms: Optional[int]) -> bool:
        """Validate if bedroom count is reasonable"""
        if not bedrooms:
            return False
        
        return 0 <= bedrooms <= 10
    
    def _validate_bathrooms_reasonableness(self, bathrooms: Optional[int]) -> bool:
        """Validate if bathroom count is reasonable"""
        if not bathrooms:
            return False
        
        return 1 <= bathrooms <= 8
    
    def _validate_square_feet_reasonableness(self, square_feet: Optional[int]) -> bool:
        """Validate if square footage is reasonable"""
        if not square_feet:
            return False
        
        return 300 <= square_feet <= 20000
    
    def remove_duplicates(self, data: List[Dict[str, Any]], key_fields: List[str] = None) -> List[Dict[str, Any]]:
        """Remove duplicate records based on key fields"""
        if key_fields is None:
            key_fields = ['address', 'price_aed', 'bedrooms']
        
        seen = set()
        unique_data = []
        
        for item in data:
            # Create a key based on specified fields
            key_parts = []
            for field in key_fields:
                value = item.get(field)
                if value is not None:
                    key_parts.append(str(value))
            
            key = '|'.join(key_parts)
            
            if key not in seen:
                seen.add(key)
                unique_data.append(item)
        
        return unique_data
    
    def generate_cleaning_report(self, original_count: int, cleaned_count: int, validation_flags: List[Dict[str, bool]]) -> Dict[str, Any]:
        """Generate a report on data cleaning results"""
        total_flags = len(validation_flags)
        if total_flags == 0:
            return {}
        
        # Count validation results
        flag_counts = {}
        for flag_name in validation_flags[0].keys():
            flag_counts[flag_name] = sum(1 for flags in validation_flags if flags.get(flag_name, False))
        
        # Calculate quality metrics
        quality_metrics = {
            'total_records': original_count,
            'cleaned_records': cleaned_count,
            'duplicates_removed': original_count - cleaned_count,
            'completeness_score': sum(flag_counts.values()) / (len(flag_counts) * total_flags),
            'data_quality_score': sum(1 for flags in validation_flags if all(flags.values())) / total_flags
        }
        
        return {
            'quality_metrics': quality_metrics,
            'validation_summary': flag_counts,
            'cleaning_timestamp': datetime.now().isoformat()
        }
