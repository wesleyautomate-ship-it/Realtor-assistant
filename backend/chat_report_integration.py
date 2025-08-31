"""
Chat Report Integration for Dubai Real Estate RAG System

This module provides integration between the chat system and report generation,
allowing users to request reports through natural language in the chat.
"""

import re
import json
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ChatReportIntegration:
    """Integration class for handling report generation requests in chat"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        
    def detect_report_request(self, message: str) -> Optional[Dict[str, Any]]:
        """Detect if a message contains a report generation request"""
        
        # Market report patterns
        market_report_patterns = [
            r'create.*market.*report.*for\s+(\w+)',
            r'generate.*market.*report.*(\w+)',
            r'market.*report.*(\w+)',
            r'(\w+).*market.*analysis',
            r'(\w+).*market.*trends'
        ]
        
        # CMA report patterns
        cma_patterns = [
            r'create.*cma.*for\s+(.+)',
            r'generate.*cma.*(.+)',
            r'comparative.*market.*analysis.*(.+)',
            r'property.*valuation.*(.+)'
        ]
        
        # Listing presentation patterns
        presentation_patterns = [
            r'create.*listing.*presentation',
            r'generate.*property.*brochure',
            r'listing.*presentation.*for\s+(.+)',
            r'property.*presentation'
        ]
        
        # Terms and conditions patterns
        terms_patterns = [
            r'create.*terms.*conditions',
            r'generate.*agreement',
            r'draft.*contract',
            r'terms.*and.*conditions.*for\s+(.+)'
        ]
        
        message_lower = message.lower()
        
        # Check for market report requests
        for pattern in market_report_patterns:
            match = re.search(pattern, message_lower)
            if match:
                area = match.group(1) if match.groups() else "Dubai"
                return {
                    "type": "market_report",
                    "area": area,
                    "property_type": self._extract_property_type(message),
                    "time_period": self._extract_time_period(message),
                    "bedrooms": self._extract_bedrooms(message),
                    "transaction_type": self._extract_transaction_type(message)
                }
        
        # Check for CMA requests
        for pattern in cma_patterns:
            match = re.search(pattern, message_lower)
            if match:
                property_address = match.group(1) if match.groups() else "Dubai"
                return {
                    "type": "cma_report",
                    "property_address": property_address,
                    "property_type": self._extract_property_type(message),
                    "bedrooms": self._extract_bedrooms(message),
                    "bathrooms": self._extract_bathrooms(message),
                    "size_sqft": self._extract_size(message)
                }
        
        # Check for listing presentation requests
        for pattern in presentation_patterns:
            match = re.search(pattern, message_lower)
            if match:
                return {
                    "type": "listing_presentation",
                    "property_details": self._extract_property_details(message)
                }
        
        # Check for terms and conditions requests
        for pattern in terms_patterns:
            match = re.search(pattern, message_lower)
            if match:
                return {
                    "type": "terms_conditions",
                    "deal_type": self._extract_deal_type(message),
                    "property_type": self._extract_property_type(message),
                    "client_type": self._extract_client_type(message)
                }
        
        return None
    
    def _extract_property_type(self, message: str) -> str:
        """Extract property type from message"""
        message_lower = message.lower()
        
        if 'apartment' in message_lower:
            return 'apartment'
        elif 'villa' in message_lower:
            return 'villa'
        elif 'townhouse' in message_lower:
            return 'townhouse'
        elif 'penthouse' in message_lower:
            return 'penthouse'
        else:
            return 'apartment'  # default
    
    def _extract_time_period(self, message: str) -> str:
        """Extract time period from message"""
        message_lower = message.lower()
        
        if 'last 3 months' in message_lower or '3 months' in message_lower:
            return 'Last 3 Months'
        elif 'last 6 months' in message_lower or '6 months' in message_lower:
            return 'Last 6 Months'
        elif 'last year' in message_lower or '12 months' in message_lower:
            return 'Last 12 Months'
        elif 'q1' in message_lower or 'quarter 1' in message_lower:
            return 'Q1 2024'
        elif 'q2' in message_lower or 'quarter 2' in message_lower:
            return 'Q2 2024'
        elif 'q3' in message_lower or 'quarter 3' in message_lower:
            return 'Q3 2024'
        elif 'q4' in message_lower or 'quarter 4' in message_lower:
            return 'Q4 2024'
        else:
            return 'Last 6 Months'  # default
    
    def _extract_bedrooms(self, message: str) -> Optional[int]:
        """Extract number of bedrooms from message"""
        message_lower = message.lower()
        
        # Look for patterns like "2 bedroom", "2-bedroom", "2br", etc.
        bedroom_patterns = [
            r'(\d+)\s*bedroom',
            r'(\d+)\s*br',
            r'(\d+)\s*bed'
        ]
        
        for pattern in bedroom_patterns:
            match = re.search(pattern, message_lower)
            if match:
                return int(match.group(1))
        
        return None
    
    def _extract_bathrooms(self, message: str) -> Optional[int]:
        """Extract number of bathrooms from message"""
        message_lower = message.lower()
        
        # Look for patterns like "2 bathroom", "2-bathroom", "2ba", etc.
        bathroom_patterns = [
            r'(\d+)\s*bathroom',
            r'(\d+)\s*ba',
            r'(\d+)\s*bath'
        ]
        
        for pattern in bathroom_patterns:
            match = re.search(pattern, message_lower)
            if match:
                return int(match.group(1))
        
        return None
    
    def _extract_size(self, message: str) -> Optional[float]:
        """Extract property size from message"""
        message_lower = message.lower()
        
        # Look for patterns like "1500 sqft", "1500 sq ft", etc.
        size_patterns = [
            r'(\d+)\s*sqft',
            r'(\d+)\s*sq\s*ft',
            r'(\d+)\s*square\s*feet'
        ]
        
        for pattern in size_patterns:
            match = re.search(pattern, message_lower)
            if match:
                return float(match.group(1))
        
        return None
    
    def _extract_transaction_type(self, message: str) -> str:
        """Extract transaction type from message"""
        message_lower = message.lower()
        
        if 'sale' in message_lower and 'rent' not in message_lower:
            return 'sale'
        elif 'rent' in message_lower and 'sale' not in message_lower:
            return 'rent'
        else:
            return 'both'
    
    def _extract_property_details(self, message: str) -> Dict[str, Any]:
        """Extract property details from message"""
        return {
            "title": "Property Listing",
            "type": self._extract_property_type(message),
            "bedrooms": self._extract_bedrooms(message) or 2,
            "bathrooms": self._extract_bathrooms(message) or 2,
            "size_sqft": self._extract_size(message) or 1500,
            "location": "Dubai",
            "price": "Price on request"
        }
    
    def _extract_deal_type(self, message: str) -> str:
        """Extract deal type from message"""
        message_lower = message.lower()
        
        if 'sale' in message_lower:
            return 'sale'
        elif 'rent' in message_lower:
            return 'rent'
        elif 'investment' in message_lower:
            return 'investment'
        else:
            return 'sale'  # default
    
    def _extract_client_type(self, message: str) -> str:
        """Extract client type from message"""
        message_lower = message.lower()
        
        if 'buyer' in message_lower:
            return 'buyer'
        elif 'seller' in message_lower:
            return 'seller'
        elif 'tenant' in message_lower:
            return 'tenant'
        elif 'landlord' in message_lower:
            return 'landlord'
        else:
            return 'buyer'  # default
    
    def generate_report(self, report_request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate a report based on the request"""
        try:
            report_type = report_request["type"]
            
            if report_type == "market_report":
                return self._generate_market_report(report_request)
            elif report_type == "cma_report":
                return self._generate_cma_report(report_request)
            elif report_type == "listing_presentation":
                return self._generate_listing_presentation(report_request)
            elif report_type == "terms_conditions":
                return self._generate_terms_conditions(report_request)
            else:
                logger.error(f"Unknown report type: {report_type}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return None
    
    def _generate_market_report(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate a market report"""
        try:
            payload = {
                "area": request["area"],
                "property_type": request["property_type"],
                "time_period": request["time_period"],
                "bedrooms": request.get("bedrooms"),
                "transaction_type": request["transaction_type"],
                "include_charts": True,
                "include_comparisons": True
            }
            
            response = requests.post(f"{self.base_url}/reports/market-report", json=payload)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to generate market report: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating market report: {e}")
            return None
    
    def _generate_cma_report(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate a CMA report"""
        try:
            payload = {
                "property_address": request["property_address"],
                "property_type": request["property_type"],
                "bedrooms": request["bedrooms"] or 2,
                "bathrooms": request["bathrooms"] or 2,
                "size_sqft": request["size_sqft"] or 1500,
                "current_price": None,
                "comparable_count": 5
            }
            
            response = requests.post(f"{self.base_url}/reports/cma-report", json=payload)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to generate CMA report: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating CMA report: {e}")
            return None
    
    def _generate_listing_presentation(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate a listing presentation"""
        try:
            payload = {
                "property_id": None,
                "property_details": request["property_details"],
                "presentation_type": "standard",
                "include_market_data": True,
                "include_comparables": True
            }
            
            response = requests.post(f"{self.base_url}/reports/listing-presentation", json=payload)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to generate listing presentation: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating listing presentation: {e}")
            return None
    
    def _generate_terms_conditions(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate terms and conditions"""
        try:
            payload = {
                "deal_type": request["deal_type"],
                "property_type": request["property_type"],
                "client_type": request["client_type"],
                "special_terms": []
            }
            
            response = requests.post(f"{self.base_url}/reports/terms-conditions", json=payload)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to generate terms and conditions: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating terms and conditions: {e}")
            return None
    
    def format_report_response(self, report_data: Dict[str, Any]) -> str:
        """Format the report response for chat"""
        try:
            report_type = report_data.get("report_type", "Report")
            title = report_data.get("title", "Generated Report")
            web_url = report_data.get("web_url", "")
            
            response = f"""
## 📊 {report_type} Generated Successfully!

**Title:** {title}

I've created a comprehensive {report_type.lower()} for you. You can view the full report at the link below:

🔗 **View Report:** {web_url}

The report includes:
- Detailed market analysis
- Professional formatting
- Interactive elements
- Downloadable content

You can share this link with clients or colleagues. The report is automatically generated with current market data and professional styling.

Would you like me to generate any other reports or modify this one?
            """
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error formatting report response: {e}")
            return "I've generated your report successfully! You can view it at the provided link."

# Global instance for use in chat
chat_report_integration = ChatReportIntegration()
