#!/usr/bin/env python3
"""
API Processor for Dubai Real Estate Research
Handles JSON data from real estate APIs, developer profiles, market data APIs
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import json
import re
from pathlib import Path
import time

# Try to import API processing libraries
try:
    import requests
    API_LIBRARY = "requests"
except ImportError:
    try:
        import urllib.request
        API_LIBRARY = "urllib"
    except ImportError:
        API_LIBRARY = None

logger = logging.getLogger(__name__)

class APIProcessor:
    """Processor for API data containing Dubai real estate information"""
    
    def __init__(self):
        self.api_types = {
            "developer_profiles": {
                "keywords": ["developer", "company", "profile", "portfolio", "projects"],
                "collections": ["developer_profiles", "market_analysis"]
            },
            "neighborhood_data": {
                "keywords": ["neighborhood", "area", "community", "location", "amenities"],
                "collections": ["neighborhood_profiles", "market_analysis"]
            },
            "market_data": {
                "keywords": ["market", "price", "trend", "analysis", "forecast"],
                "collections": ["market_analysis", "financial_insights"]
            },
            "property_listings": {
                "keywords": ["property", "listing", "address", "price", "bedrooms"],
                "collections": ["market_analysis", "properties"]
            },
            "transaction_data": {
                "keywords": ["transaction", "sale", "purchase", "amount", "date"],
                "collections": ["market_analysis", "transaction_guidance"]
            }
        }
        
        # Common Dubai real estate API endpoints
        self.known_apis = {
            "dubai_land_department": "https://www.dubailand.gov.ae/api/",
            "rera_api": "https://www.rera.gov.ae/api/",
            "property_finder": "https://www.propertyfinder.ae/api/",
            "bayut_api": "https://www.bayut.com/api/",
            "emaar_api": "https://www.emaar.com/api/",
            "damac_api": "https://www.damacproperties.com/api/"
        }
        
        if not API_LIBRARY:
            logger.warning("No API processing library available. Install requests.")
    
    def process(self, api_url_or_file: str, api_key: str = None, headers: Dict = None) -> Dict[str, Any]:
        """Process API data from URL or JSON file"""
        logger.info(f"Processing API data: {api_url_or_file}")
        
        try:
            # Determine if it's a URL or file
            if api_url_or_file.startswith(('http://', 'https://')):
                data = self._fetch_api_data(api_url_or_file, api_key, headers)
                source_type = "api_url"
            else:
                data = self._read_json_file(api_url_or_file)
                source_type = "json_file"
            
            if not data:
                raise ValueError("Could not extract data from source")
            
            # Classify API type
            api_type = self._classify_api_data(data, api_url_or_file)
            logger.info(f"Classified API data as: {api_type}")
            
            # Extract structured data
            structured_data = self._extract_structured_data(data, api_type, api_url_or_file)
            
            # Generate metadata
            metadata = self._generate_metadata(api_url_or_file, api_type, source_type, data)
            
            return {
                "content_type": "api",
                "source": api_url_or_file,
                "source_type": source_type,
                "api_type_classified": api_type,
                "processed_at": datetime.now().isoformat(),
                "data_size": len(str(data)),
                "structured_data": structured_data,
                "metadata": metadata,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error processing API data {api_url_or_file}: {e}")
            return {
                "content_type": "api",
                "source": api_url_or_file,
                "status": "failed",
                "error": str(e)
            }
    
    def _fetch_api_data(self, api_url: str, api_key: str = None, headers: Dict = None) -> Dict[str, Any]:
        """Fetch data from API endpoint"""
        if not API_LIBRARY:
            raise ImportError("No API processing library available")
        
        try:
            # Prepare headers
            request_headers = {
                'User-Agent': 'Dubai-Real-Estate-Research/1.0',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            if api_key:
                request_headers['Authorization'] = f'Bearer {api_key}'
            
            if headers:
                request_headers.update(headers)
            
            if API_LIBRARY == "requests":
                response = requests.get(api_url, headers=request_headers, timeout=30)
                response.raise_for_status()
                return response.json()
            
            elif API_LIBRARY == "urllib":
                req = urllib.request.Request(api_url, headers=request_headers)
                with urllib.request.urlopen(req, timeout=30) as response:
                    data = response.read().decode('utf-8')
                    return json.loads(data)
            
        except Exception as e:
            logger.error(f"Error fetching API data from {api_url}: {e}")
            raise
    
    def _read_json_file(self, file_path: str) -> Dict[str, Any]:
        """Read data from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            logger.error(f"Error reading JSON file {file_path}: {e}")
            raise
    
    def _classify_api_data(self, data: Dict[str, Any], source: str) -> str:
        """Classify API data type based on content and structure"""
        # Convert data to string for keyword analysis
        data_str = json.dumps(data).lower()
        source_lower = source.lower()
        
        # Count keyword matches for each API type
        type_scores = {}
        
        for api_type, config in self.api_types.items():
            score = 0
            
            # Check keywords in source URL and data
            for keyword in config["keywords"]:
                score += source_lower.count(keyword)
                score += data_str.count(keyword)
            
            # Bonus for known API patterns
            for known_api in self.known_apis.keys():
                if known_api in source_lower:
                    score += 3  # Higher weight for known APIs
            
            type_scores[api_type] = score
        
        # Return the API type with highest score
        if type_scores:
            return max(type_scores, key=type_scores.get)
        else:
            return "general_api_data"
    
    def _extract_structured_data(self, data: Dict[str, Any], api_type: str, source: str) -> Dict[str, Any]:
        """Extract structured data based on API type"""
        structured_data = {
            "api_type": api_type,
            "key_entities": [],
            "key_metrics": {},
            "data_summary": {},
            "endpoints": []
        }
        
        # Extract key entities
        structured_data["key_entities"] = self._extract_entities(data)
        
        # Extract key metrics based on API type
        if api_type == "developer_profiles":
            structured_data["key_metrics"] = self._extract_developer_metrics(data)
        elif api_type == "neighborhood_data":
            structured_data["key_metrics"] = self._extract_neighborhood_metrics(data)
        elif api_type == "market_data":
            structured_data["key_metrics"] = self._extract_market_metrics(data)
        elif api_type == "property_listings":
            structured_data["key_metrics"] = self._extract_property_metrics(data)
        elif api_type == "transaction_data":
            structured_data["key_metrics"] = self._extract_transaction_metrics(data)
        
        # Extract endpoints if it's an API URL
        if source.startswith(('http://', 'https://')):
            structured_data["endpoints"] = self._extract_endpoints(data, source)
        
        # Generate data summary
        structured_data["data_summary"] = self._generate_data_summary(data)
        
        return structured_data
    
    def _extract_entities(self, data: Dict[str, Any]) -> List[str]:
        """Extract key entities from API data"""
        entities = []
        
        # Dubai neighborhoods
        neighborhoods = [
            "Dubai Marina", "Downtown Dubai", "Palm Jumeirah", "JBR", "Jumeirah Beach",
            "Arabian Ranches", "Emirates Hills", "Dubai Hills Estate", "Meydan",
            "Business Bay", "Dubai Creek Harbour", "Dubai South", "Dubai Silicon Oasis"
        ]
        
        # Major developers
        developers = [
            "Emaar Properties", "DAMAC Properties", "Nakheel", "Meraas", "Dubai Properties",
            "Sobha Realty", "Azizi Developments", "Omniyat", "Select Group"
        ]
        
        # Convert data to string for entity search
        data_str = json.dumps(data).lower()
        
        for entity in neighborhoods + developers:
            if entity.lower() in data_str:
                entities.append(entity)
        
        return list(set(entities))
    
    def _extract_developer_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract developer-related metrics"""
        metrics = {}
        
        # Count developers in data
        if isinstance(data, dict):
            # Look for developer-related fields
            developer_fields = ["developers", "companies", "profiles", "portfolio"]
            for field in developer_fields:
                if field in data:
                    if isinstance(data[field], list):
                        metrics[f"{field}_count"] = len(data[field])
                    elif isinstance(data[field], dict):
                        metrics[f"{field}_count"] = 1
        
        # Extract project counts
        if isinstance(data, dict) and "projects" in data:
            if isinstance(data["projects"], list):
                metrics["total_projects"] = len(data["projects"])
        
        # Extract market share data
        if isinstance(data, dict) and "market_share" in data:
            metrics["market_share_data"] = True
        
        return metrics
    
    def _extract_neighborhood_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract neighborhood-related metrics"""
        metrics = {}
        
        # Count neighborhoods in data
        if isinstance(data, dict):
            neighborhood_fields = ["neighborhoods", "areas", "communities", "locations"]
            for field in neighborhood_fields:
                if field in data:
                    if isinstance(data[field], list):
                        metrics[f"{field}_count"] = len(data[field])
                    elif isinstance(data[field], dict):
                        metrics[f"{field}_count"] = 1
        
        # Extract amenity data
        if isinstance(data, dict) and "amenities" in data:
            metrics["amenities_data"] = True
        
        # Extract price data
        if isinstance(data, dict) and "prices" in data:
            metrics["price_data"] = True
        
        return metrics
    
    def _extract_market_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract market-related metrics"""
        metrics = {}
        
        # Count market data points
        if isinstance(data, dict):
            market_fields = ["prices", "trends", "forecasts", "analysis"]
            for field in market_fields:
                if field in data:
                    if isinstance(data[field], list):
                        metrics[f"{field}_count"] = len(data[field])
                    elif isinstance(data[field], dict):
                        metrics[f"{field}_count"] = 1
        
        # Extract price ranges
        if isinstance(data, dict) and "price_range" in data:
            metrics["price_range_data"] = True
        
        # Extract trend data
        if isinstance(data, dict) and "trends" in data:
            metrics["trend_data"] = True
        
        return metrics
    
    def _extract_property_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract property-related metrics"""
        metrics = {}
        
        # Count properties in data
        if isinstance(data, dict):
            property_fields = ["properties", "listings", "units", "apartments"]
            for field in property_fields:
                if field in data:
                    if isinstance(data[field], list):
                        metrics[f"{field}_count"] = len(data[field])
                    elif isinstance(data[field], dict):
                        metrics[f"{field}_count"] = 1
        
        # Extract property types
        if isinstance(data, dict) and "property_types" in data:
            if isinstance(data["property_types"], list):
                metrics["property_types_count"] = len(data["property_types"])
        
        # Extract price data
        if isinstance(data, dict) and "prices" in data:
            metrics["price_data"] = True
        
        return metrics
    
    def _extract_transaction_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract transaction-related metrics"""
        metrics = {}
        
        # Count transactions in data
        if isinstance(data, dict):
            transaction_fields = ["transactions", "sales", "purchases", "deals"]
            for field in transaction_fields:
                if field in data:
                    if isinstance(data[field], list):
                        metrics[f"{field}_count"] = len(data[field])
                    elif isinstance(data[field], dict):
                        metrics[f"{field}_count"] = 1
        
        # Extract transaction amounts
        if isinstance(data, dict) and "amounts" in data:
            metrics["amount_data"] = True
        
        # Extract date ranges
        if isinstance(data, dict) and "date_range" in data:
            metrics["date_range_data"] = True
        
        return metrics
    
    def _extract_endpoints(self, data: Dict[str, Any], source: str) -> List[str]:
        """Extract API endpoints from data"""
        endpoints = []
        
        # Look for endpoint patterns in the data
        if isinstance(data, dict):
            # Common endpoint patterns
            endpoint_patterns = ["endpoints", "routes", "apis", "urls"]
            
            for pattern in endpoint_patterns:
                if pattern in data:
                    if isinstance(data[pattern], list):
                        endpoints.extend(data[pattern])
                    elif isinstance(data[pattern], dict):
                        endpoints.extend(data[pattern].keys())
        
        # Add the base endpoint
        base_url = source.rstrip('/')
        endpoints.append(base_url)
        
        return list(set(endpoints))  # Remove duplicates
    
    def _generate_data_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary statistics for the API data"""
        summary = {
            "data_type": type(data).__name__,
            "structure": self._analyze_structure(data)
        }
        
        if isinstance(data, dict):
            summary["key_count"] = len(data.keys())
            summary["top_level_keys"] = list(data.keys())
        elif isinstance(data, list):
            summary["item_count"] = len(data)
            if data:
                summary["first_item_type"] = type(data[0]).__name__
        
        return summary
    
    def _analyze_structure(self, data: Any) -> str:
        """Analyze the structure of the data"""
        if isinstance(data, dict):
            return "object"
        elif isinstance(data, list):
            return "array"
        elif isinstance(data, (str, int, float, bool)):
            return "primitive"
        else:
            return "unknown"
    
    def _generate_metadata(self, source: str, api_type: str, source_type: str, data: Any) -> Dict[str, Any]:
        """Generate metadata for the API data"""
        metadata = {
            "source": source,
            "source_type": source_type,
            "api_type": api_type,
            "processing_library": API_LIBRARY,
            "data_size": len(str(data)),
            "extraction_timestamp": datetime.now().isoformat()
        }
        
        # Add API information if it's a URL
        if source_type == "api_url":
            try:
                from urllib.parse import urlparse
                parsed_url = urlparse(source)
                metadata["domain"] = parsed_url.netloc
                metadata["path"] = parsed_url.path
                
                # Check if it's a known API
                for known_api, known_url in self.known_apis.items():
                    if known_api in source.lower():
                        metadata["known_api"] = known_api
                        break
            except:
                pass
        
        return metadata
