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

# Import the new property detection service
try:
    from services.property_detection_service import PropertyDetectionService
except ImportError:
    logger.warning("PropertyDetectionService not available, using fallback detection")
    PropertyDetectionService = None

class ChatReportIntegration:
    """Integration class for handling report generation requests in chat"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        # Initialize property detection service
        self.property_detector = PropertyDetectionService() if PropertyDetectionService else None
        
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
        
        # CMA report patterns - Enhanced for better detection
        cma_patterns = [
            r'create.*cma.*for\s+(.+)',
            r'generate.*cma.*(.+)',
            r'comparative.*market.*analysis.*(.+)',
            r'property.*valuation.*(.+)',
            r'cma.*for\s+(.+)',
            r'i\s+need.*cma.*for\s+(.+)',
            r'can\s+you.*cma.*for\s+(.+)',
            r'help\s+me.*cma.*for\s+(.+)',
            r'make.*cma.*for\s+(.+)',
            r'build.*cma.*for\s+(.+)',
            r'prepare.*cma.*for\s+(.+)',
            r'draft.*cma.*for\s+(.+)',
            r'cma.*(.+?)(?:\s+apartment|\s+building|\s+property|\s+villa|\s+house)',
            r'comparative.*analysis.*for\s+(.+)',
            r'market.*analysis.*for\s+(.+)',
            r'valuation.*for\s+(.+)',
            r'price.*analysis.*for\s+(.+)'
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
                
                # Use enhanced property detection service if available
                if self.property_detector:
                    property_info = self.property_detector.detect_property_from_request(message)
                    
                    # Query database for specific property details
                    db_property = self.property_detector.query_property_from_database(property_info)
                    
                    # Get building-specific transactions for CMA
                    building_transactions = []
                    if property_info.get('building_name'):
                        building_transactions = self.property_detector.get_building_specific_transactions(
                            property_info['building_name'], 
                            property_info.get('community')
                        )
                    
                    return {
                        "type": "cma_report",
                        "property_address": property_address,
                        "detected_property": property_info,
                        "database_property": db_property,
                        "building_transactions": building_transactions,
                        "location": property_info.get('community', self._extract_location(message)),
                        "property_type": property_info.get('property_type', self._extract_property_type(message)),
                        "bedrooms": property_info.get('bedrooms', self._extract_bedrooms(message)),
                        "bathrooms": property_info.get('bathrooms', self._extract_bathrooms(message)),
                        "size_sqft": property_info.get('size_sqft', self._extract_size(message)),
                        "confidence": property_info.get('confidence', 0.0)
                    }
                else:
                    # Fallback to original detection
                    location = self._extract_location(message)
                return {
                    "type": "cma_report",
                    "property_address": property_address,
                        "location": location,
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
        """Extract property type from message - Enhanced detection"""
        message_lower = message.lower()
        
        # Apartment variations
        if any(word in message_lower for word in ['apartment', 'apt', 'flat', 'unit', 'condo', 'condominium']):
            return 'apartment'
        # Villa variations  
        elif any(word in message_lower for word in ['villa', 'house', 'detached', 'standalone']):
            return 'villa'
        # Townhouse variations
        elif any(word in message_lower for word in ['townhouse', 'townhouse', 'terrace', 'row house']):
            return 'townhouse'
        # Penthouse variations
        elif any(word in message_lower for word in ['penthouse', 'duplex', 'maisonette']):
            return 'penthouse'
        # Studio variations
        elif any(word in message_lower for word in ['studio', 'efficiency', 'bachelor']):
            return 'studio'
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
    
    def _extract_location(self, message: str) -> str:
        """Extract location/area from message - Enhanced detection"""
        message_lower = message.lower()
        
        # Dubai areas and neighborhoods
        dubai_areas = [
            'dubai marina', 'marina', 'downtown dubai', 'downtown', 'palm jumeirah', 'palm',
            'business bay', 'jbr', 'jumeirah beach residence', 'dubai hills estate', 'dubai hills',
            'arabian ranches', 'emirates hills', 'jumeirah', 'dubai sports city', 'sports city',
            'international city', 'discovery gardens', 'jumeirah village circle', 'jvc',
            'jumeirah village triangle', 'jvt', 'motor city', 'dubai silicon oasis', 'dso',
            'dubai investment park', 'dip', 'dubai land', 'dubai production city', 'dpc',
            'dubai media city', 'dmc', 'dubai internet city', 'dic', 'dubai knowledge village', 'dkv',
            'dubai international financial centre', 'difc', 'dubai world trade centre', 'dwtc',
            'burj khalifa', 'burj al arab', 'jumeirah lake towers', 'jlt', 'dubai festival city',
            'dubai healthcare city', 'dhcc', 'dubai autodrome', 'dubai motor city'
        ]
        
        # Check for specific areas
        for area in dubai_areas:
            if area in message_lower:
                return area.title()
        
        # Check for building names (common patterns)
        building_patterns = [
            r'(\w+)\s+building',
            r'(\w+)\s+tower',
            r'(\w+)\s+residence',
            r'(\w+)\s+apartments',
            r'(\w+)\s+complex'
        ]
        
        for pattern in building_patterns:
            match = re.search(pattern, message_lower)
            if match:
                return match.group(1).title()
        
        # Default to Dubai if no specific location found
        return "Dubai"
    
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
        """Generate a CMA report with enhanced parameters and building-specific data"""
        try:
            # Enhanced payload with building-specific data
            payload = {
                "property_address": request["property_address"],
                "location": request.get("location", "Dubai"),
                "property_type": request["property_type"],
                "bedrooms": request["bedrooms"] or 2,
                "bathrooms": request["bathrooms"] or 2,
                "size_sqft": request["size_sqft"] or 1500,
                "current_price": None,
                "comparable_count": 5,
                "include_market_trends": True,
                "include_rental_analysis": True,
                "include_investment_metrics": True,
                "report_format": "html",
                "include_charts": True,
                # Enhanced data from property detection
                "detected_property": request.get("detected_property", {}),
                "database_property": request.get("database_property", {}),
                "building_transactions": request.get("building_transactions", []),
                "confidence": request.get("confidence", 0.0)
            }
            
            # Try to get community market data if available
            if self.property_detector and request.get("location"):
                community_data = self.property_detector.get_community_market_data(request["location"])
                payload["community_market_data"] = community_data
            
            response = requests.post(f"{self.base_url}/reports/cma-report", json=payload)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to generate CMA report: {response.status_code}")
                # Fallback: Generate enhanced CMA using AI manager with building data
                return self._generate_enhanced_fallback_cma(request)
                
        except Exception as e:
            logger.error(f"Error generating CMA report: {e}")
            # Fallback: Generate enhanced CMA using AI manager with building data
            return self._generate_enhanced_fallback_cma(request)
    
    def _generate_enhanced_fallback_cma(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced fallback CMA generation using AI manager with building-specific data"""
        try:
            from ai_manager import AIEnhancementManager
            import google.generativeai as genai
            import os
            
            # Initialize AI model
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Create AI manager
            ai_manager = AIEnhancementManager(os.getenv("DATABASE_URL"), model)
            
            # Create enhanced subject property data
            subject_property = {
                "address": request["property_address"],
                "location": request.get("location", "Dubai"),
                "property_type": request["property_type"],
                "bedrooms": request["bedrooms"] or 2,
                "bathrooms": request["bathrooms"] or 2,
                "size_sqft": request["size_sqft"] or 1500,
                "current_price": None,
                # Enhanced data from property detection
                "building_name": request.get("detected_property", {}).get("building_name"),
                "unit_number": request.get("detected_property", {}).get("unit_number"),
                "community": request.get("detected_property", {}).get("community"),
                "confidence": request.get("confidence", 0.0)
            }
            
            # Use building-specific transactions if available
            comparable_properties = request.get("building_transactions", [])
            
            # Add database property data if available
            db_property = request.get("database_property", {})
            if db_property:
                subject_property.update({
                    "database_id": db_property.get("id"),
                    "title": db_property.get("title"),
                    "description": db_property.get("description"),
                    "price": db_property.get("price"),
                    "price_per_sqft": db_property.get("price_per_sqft")
                })
            
            # Generate enhanced CMA content
            cma_content = ai_manager.generate_cma_content(subject_property, comparable_properties)
            
            # Add building-specific insights if available
            if comparable_properties:
                building_insights = self._generate_building_insights(comparable_properties, subject_property)
                cma_content += f"\n\n## Building-Specific Analysis\n{building_insights}"
            
            return {
                "report_type": "CMA Report",
                "title": f"Comparative Market Analysis - {request['property_address']}",
                "content": cma_content,
                "web_url": f"/reports/cma/{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "generated_at": datetime.now().isoformat(),
                "status": "generated",
                "building_specific": len(comparable_properties) > 0,
                "data_confidence": request.get("confidence", 0.0),
                "comparable_count": len(comparable_properties)
            }
            
        except Exception as e:
            logger.error(f"Error in enhanced fallback CMA generation: {e}")
            return {
                "report_type": "CMA Report",
                "title": f"Comparative Market Analysis - {request['property_address']}",
                "content": "CMA report generation is temporarily unavailable. Please try again later.",
                "web_url": "",
                "generated_at": datetime.now().isoformat(),
                "status": "error"
            }
    
    def _generate_fallback_cma(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback CMA generation using AI manager"""
        try:
            from ai_manager import AIEnhancementManager
            import google.generativeai as genai
            import os
            
            # Initialize AI model
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Create AI manager
            ai_manager = AIEnhancementManager(os.getenv("DATABASE_URL"), model)
            
            # Create subject property data
            subject_property = {
                "address": request["property_address"],
                "location": request.get("location", "Dubai"),
                "property_type": request["property_type"],
                "bedrooms": request["bedrooms"] or 2,
                "bathrooms": request["bathrooms"] or 2,
                "size_sqft": request["size_sqft"] or 1500,
                "current_price": None
            }
            
            # Generate CMA content
            cma_content = ai_manager.generate_cma_content(subject_property, [])
            
            return {
                "report_type": "CMA Report",
                "title": f"Comparative Market Analysis - {request['property_address']}",
                "content": cma_content,
                "web_url": f"/reports/cma/{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "generated_at": datetime.now().isoformat(),
                "status": "generated"
            }
            
        except Exception as e:
            logger.error(f"Error in fallback CMA generation: {e}")
            return {
                "report_type": "CMA Report",
                "title": f"Comparative Market Analysis - {request['property_address']}",
                "content": "CMA report generation is temporarily unavailable. Please try again later.",
                "web_url": "",
                "generated_at": datetime.now().isoformat(),
                "status": "error"
            }
    
    def _generate_building_insights(self, comparable_properties: List[Dict], subject_property: Dict) -> str:
        """Generate building-specific insights from comparable properties"""
        try:
            if not comparable_properties:
                return "No building-specific data available."
            
            # Calculate building statistics
            prices = [p.get('price', 0) for p in comparable_properties if p.get('price')]
            sizes = [p.get('square_feet', 0) for p in comparable_properties if p.get('square_feet')]
            bedrooms = [p.get('bedrooms', 0) for p in comparable_properties if p.get('bedrooms')]
            
            insights = []
            
            if prices:
                avg_price = sum(prices) / len(prices)
                min_price = min(prices)
                max_price = max(prices)
                insights.append(f"**Building Price Range:** AED {min_price:,.0f} - AED {max_price:,.0f} (Average: AED {avg_price:,.0f})")
            
            if sizes:
                avg_size = sum(sizes) / len(sizes)
                insights.append(f"**Average Unit Size:** {avg_size:,.0f} sqft")
            
            if bedrooms:
                avg_bedrooms = sum(bedrooms) / len(bedrooms)
                insights.append(f"**Average Bedrooms:** {avg_bedrooms:.1f}")
            
            # Price per sqft analysis
            price_per_sqft_data = []
            for prop in comparable_properties:
                if prop.get('price') and prop.get('square_feet'):
                    ppsf = prop['price'] / prop['square_feet']
                    price_per_sqft_data.append(ppsf)
            
            if price_per_sqft_data:
                avg_ppsf = sum(price_per_sqft_data) / len(price_per_sqft_data)
                insights.append(f"**Average Price per Sqft:** AED {avg_ppsf:,.0f}")
            
            insights.append(f"**Total Comparable Units:** {len(comparable_properties)}")
            
            return "\n".join(insights)
            
        except Exception as e:
            logger.error(f"Error generating building insights: {e}")
            return "Building-specific analysis unavailable."
    
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
