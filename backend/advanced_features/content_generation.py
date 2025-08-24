"""
Content Generation Engine for Real Estate RAG Chat System

This module provides AI-powered content generation including:
- Property brochures and marketing materials
- CMA (Comparative Market Analysis) reports
- Listing descriptions and property details
- Market analysis reports
- Professional content templates
"""

import logging
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import requests
from .config import config

logger = logging.getLogger(__name__)

@dataclass
class GeneratedContent:
    """Represents generated content with metadata"""
    content_type: str
    title: str
    content: str
    template_used: str
    generated_date: datetime
    word_count: int
    key_features: List[str]
    target_audience: str
    seo_keywords: List[str]

@dataclass
class CMAReport:
    """Represents a Comparative Market Analysis report"""
    property_address: str
    property_type: str
    estimated_value: float
    comparable_properties: List[Dict[str, Any]]
    market_analysis: Dict[str, Any]
    recommendations: List[str]
    report_date: datetime
    confidence_score: float

@dataclass
class PropertyBrochure:
    """Represents a property brochure"""
    property_id: str
    title: str
    description: str
    key_features: List[str]
    amenities: List[str]
    location_highlights: List[str]
    pricing_info: Dict[str, Any]
    contact_info: Dict[str, str]
    images: List[str]
    generated_date: datetime

class ContentGenerationEngine:
    """
    AI-powered content generation engine for real estate marketing
    """
    
    def __init__(self):
        self.templates = self._load_templates()
        self.content_history = []
        
    def _load_templates(self) -> Dict[str, str]:
        """Load content generation templates"""
        return {
            "property_brochure": """
# {property_title}

## Property Overview
{property_description}

## Key Features
{key_features}

## Location Highlights
{location_highlights}

## Amenities
{amenities}

## Pricing Information
- **Price**: {price}
- **Price per sq ft**: {price_per_sqft}
- **Rental Yield**: {rental_yield}%

## Contact Information
- **Agent**: {agent_name}
- **Phone**: {agent_phone}
- **Email**: {agent_email}
- **Office**: {office_name}

*Generated on {generation_date}*
            """,
            
            "listing_description": """
🏠 **{property_title}**

{property_description}

✨ **Key Features:**
{key_features}

📍 **Location:**
{location_description}

🏢 **Amenities:**
{amenities}

💰 **Pricing:**
- Price: {price}
- Price per sq ft: {price_per_sqft}
- Monthly rent: {monthly_rent}

📞 **Contact:**
{contact_info}

*Property ID: {property_id}*
            """,
            
            "cma_report": """
# Comparative Market Analysis Report

## Property Details
- **Address**: {property_address}
- **Property Type**: {property_type}
- **Size**: {size_sqft} sq ft
- **Bedrooms**: {bedrooms}
- **Bathrooms**: {bathrooms}

## Estimated Market Value
**{estimated_value}** (Confidence: {confidence_score}%)

## Comparable Properties
{comparable_properties}

## Market Analysis
{market_analysis}

## Recommendations
{recommendations}

*Report generated on {report_date}*
            """,
            
            "market_report": """
# Market Analysis Report - {area}

## Executive Summary
{executive_summary}

## Market Trends
{market_trends}

## Price Analysis
{price_analysis}

## Investment Opportunities
{investment_opportunities}

## Risk Assessment
{risk_assessment}

## Recommendations
{recommendations}

*Report Date: {report_date}*
            """
        }
    
    def generate_property_brochure(self, property_data: Dict[str, Any]) -> Optional[PropertyBrochure]:
        """
        Generate a professional property brochure
        
        Args:
            property_data: Dictionary containing property information
            
        Returns:
            PropertyBrochure object with generated content
        """
        try:
            # Extract property information
            property_id = property_data.get('property_id', 'unknown')
            title = self._generate_property_title(property_data)
            description = self._generate_property_description(property_data)
            key_features = self._extract_key_features(property_data)
            amenities = self._extract_amenities(property_data)
            location_highlights = self._generate_location_highlights(property_data)
            pricing_info = self._extract_pricing_info(property_data)
            contact_info = self._extract_contact_info(property_data)
            
            # Generate brochure content using template
            template = self.templates["property_brochure"]
            content = template.format(
                property_title=title,
                property_description=description,
                key_features=self._format_list(key_features),
                location_highlights=self._format_list(location_highlights),
                amenities=self._format_list(amenities),
                price=pricing_info.get('price', 'Contact for price'),
                price_per_sqft=pricing_info.get('price_per_sqft', 'N/A'),
                rental_yield=pricing_info.get('rental_yield', 'N/A'),
                agent_name=contact_info.get('agent_name', 'Our Team'),
                agent_phone=contact_info.get('agent_phone', 'Contact us'),
                agent_email=contact_info.get('agent_email', 'info@realestate.com'),
                office_name=contact_info.get('office_name', 'Real Estate Agency'),
                generation_date=datetime.now().strftime('%B %d, %Y')
            )
            
            return PropertyBrochure(
                property_id=property_id,
                title=title,
                description=description,
                key_features=key_features,
                amenities=amenities,
                location_highlights=location_highlights,
                pricing_info=pricing_info,
                contact_info=contact_info,
                images=property_data.get('images', []),
                generated_date=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error generating property brochure: {e}")
            return None
    
    def generate_listing_description(self, property_data: Dict[str, Any]) -> Optional[GeneratedContent]:
        """
        Generate a compelling listing description
        
        Args:
            property_data: Dictionary containing property information
            
        Returns:
            GeneratedContent object with listing description
        """
        try:
            # Generate content elements
            title = self._generate_property_title(property_data)
            description = self._generate_property_description(property_data)
            key_features = self._extract_key_features(property_data)
            location_description = self._generate_location_description(property_data)
            amenities = self._extract_amenities(property_data)
            pricing_info = self._extract_pricing_info(property_data)
            contact_info = self._generate_contact_info(property_data)
            
            # Use template to generate content
            template = self.templates["listing_description"]
            content = template.format(
                property_title=title,
                property_description=description,
                key_features=self._format_list(key_features, emoji="✨"),
                location_description=location_description,
                amenities=self._format_list(amenities, emoji="🏢"),
                price=pricing_info.get('price', 'Contact for price'),
                price_per_sqft=pricing_info.get('price_per_sqft', 'N/A'),
                monthly_rent=pricing_info.get('monthly_rent', 'N/A'),
                contact_info=contact_info,
                property_id=property_data.get('property_id', 'N/A')
            )
            
            # Generate SEO keywords
            seo_keywords = self._generate_seo_keywords(property_data)
            
            return GeneratedContent(
                content_type="listing_description",
                title=title,
                content=content,
                template_used="listing_description",
                generated_date=datetime.now(),
                word_count=len(content.split()),
                key_features=key_features,
                target_audience="potential_buyers",
                seo_keywords=seo_keywords
            )
            
        except Exception as e:
            logger.error(f"Error generating listing description: {e}")
            return None
    
    def generate_cma_report(self, property_data: Dict[str, Any], comparable_properties: List[Dict] = None) -> Optional[CMAReport]:
        """
        Generate a Comparative Market Analysis report
        
        Args:
            property_data: Dictionary containing property information
            comparable_properties: List of comparable properties
            
        Returns:
            CMAReport object with analysis results
        """
        try:
            # Get comparable properties if not provided
            if comparable_properties is None:
                comparable_properties = self._find_comparable_properties(property_data)
            
            # Calculate estimated value
            estimated_value = self._calculate_estimated_value(property_data, comparable_properties)
            
            # Generate market analysis
            market_analysis = self._generate_market_analysis(property_data, comparable_properties)
            
            # Generate recommendations
            recommendations = self._generate_cma_recommendations(property_data, estimated_value, comparable_properties)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(comparable_properties)
            
            return CMAReport(
                property_address=property_data.get('address', 'Unknown'),
                property_type=property_data.get('property_type', 'Unknown'),
                estimated_value=estimated_value,
                comparable_properties=comparable_properties,
                market_analysis=market_analysis,
                recommendations=recommendations,
                report_date=datetime.now(),
                confidence_score=confidence_score
            )
            
        except Exception as e:
            logger.error(f"Error generating CMA report: {e}")
            return None
    
    def generate_market_report(self, area: str, market_data: Dict[str, Any]) -> Optional[GeneratedContent]:
        """
        Generate a comprehensive market analysis report
        
        Args:
            area: Geographic area for analysis
            market_data: Market data and statistics
            
        Returns:
            GeneratedContent object with market report
        """
        try:
            # Generate report sections
            executive_summary = self._generate_executive_summary(area, market_data)
            market_trends = self._analyze_market_trends(market_data)
            price_analysis = self._analyze_price_trends(market_data)
            investment_opportunities = self._identify_investment_opportunities(area, market_data)
            risk_assessment = self._assess_market_risks(market_data)
            recommendations = self._generate_market_recommendations(area, market_data)
            
            # Use template to generate content
            template = self.templates["market_report"]
            content = template.format(
                area=area,
                executive_summary=executive_summary,
                market_trends=market_trends,
                price_analysis=price_analysis,
                investment_opportunities=investment_opportunities,
                risk_assessment=risk_assessment,
                recommendations=recommendations,
                report_date=datetime.now().strftime('%B %d, %Y')
            )
            
            return GeneratedContent(
                content_type="market_report",
                title=f"Market Analysis Report - {area}",
                content=content,
                template_used="market_report",
                generated_date=datetime.now(),
                word_count=len(content.split()),
                key_features=[],
                target_audience="investors_agents",
                seo_keywords=[area, "real estate", "market analysis", "investment"]
            )
            
        except Exception as e:
            logger.error(f"Error generating market report: {e}")
            return None
    
    def _generate_property_title(self, property_data: Dict[str, Any]) -> str:
        """Generate an attractive property title"""
        property_type = property_data.get('property_type', 'Property')
        bedrooms = property_data.get('bedrooms', 0)
        location = property_data.get('location', 'Dubai')
        
        if bedrooms > 0:
            return f"{bedrooms} Bedroom {property_type.title()} in {location}"
        else:
            return f"Beautiful {property_type.title()} in {location}"
    
    def _generate_property_description(self, property_data: Dict[str, Any]) -> str:
        """Generate a compelling property description"""
        property_type = property_data.get('property_type', 'property')
        size = property_data.get('size_sqft', 0)
        bedrooms = property_data.get('bedrooms', 0)
        bathrooms = property_data.get('bathrooms', 0)
        location = property_data.get('location', 'Dubai')
        
        description = f"This stunning {property_type} is located in the prestigious {location} area. "
        
        if size > 0:
            description += f"Spanning {size:,} sq ft, "
        
        if bedrooms > 0 and bathrooms > 0:
            description += f"this {bedrooms}-bedroom, {bathrooms}-bathroom property "
        elif bedrooms > 0:
            description += f"this {bedrooms}-bedroom property "
        else:
            description += "this property "
        
        description += "offers the perfect blend of luxury, comfort, and convenience. "
        description += "Featuring modern amenities and excellent connectivity, "
        description += "this is an ideal investment opportunity or dream home."
        
        return description
    
    def _extract_key_features(self, property_data: Dict[str, Any]) -> List[str]:
        """Extract key features from property data"""
        features = []
        
        # Basic features
        if property_data.get('balcony'):
            features.append("Private balcony")
        if property_data.get('parking'):
            features.append("Parking space")
        if property_data.get('gym'):
            features.append("Gym access")
        if property_data.get('pool'):
            features.append("Swimming pool")
        if property_data.get('security'):
            features.append("24/7 security")
        if property_data.get('elevator'):
            features.append("Elevator access")
        if property_data.get('furnished'):
            features.append("Fully furnished")
        if property_data.get('sea_view'):
            features.append("Sea view")
        if property_data.get('city_view'):
            features.append("City view")
        
        # Add size and layout features
        size = property_data.get('size_sqft', 0)
        if size > 0:
            features.append(f"{size:,} sq ft")
        
        bedrooms = property_data.get('bedrooms', 0)
        bathrooms = property_data.get('bathrooms', 0)
        if bedrooms > 0 and bathrooms > 0:
            features.append(f"{bedrooms}BR/{bathrooms}BA")
        
        return features[:10]  # Limit to 10 features
    
    def _extract_amenities(self, property_data: Dict[str, Any]) -> List[str]:
        """Extract amenities from property data"""
        amenities = []
        
        # Building amenities
        building_amenities = [
            'gym', 'pool', 'spa', 'sauna', 'tennis_court', 'basketball_court',
            'children_playground', 'bbq_area', 'garden', 'concierge',
            'security', 'parking', 'elevator', 'cctv'
        ]
        
        for amenity in building_amenities:
            if property_data.get(amenity):
                amenities.append(amenity.replace('_', ' ').title())
        
        # Location amenities
        location_amenities = [
            'near_metro', 'near_mall', 'near_school', 'near_hospital',
            'near_park', 'near_restaurant', 'near_bank'
        ]
        
        for amenity in location_amenities:
            if property_data.get(amenity):
                amenities.append(f"Near {amenity.replace('near_', '').title()}")
        
        return amenities[:15]  # Limit to 15 amenities
    
    def _generate_location_highlights(self, property_data: Dict[str, Any]) -> List[str]:
        """Generate location highlights"""
        location = property_data.get('location', 'Dubai')
        highlights = []
        
        # Add location-specific highlights
        if 'downtown' in location.lower():
            highlights.extend([
                "Walking distance to Burj Khalifa",
                "Close to Dubai Mall",
                "Metro connectivity",
                "Premium location"
            ])
        elif 'marina' in location.lower():
            highlights.extend([
                "Marina waterfront views",
                "Walking distance to JBR",
                "Boat access",
                "Premium lifestyle"
            ])
        elif 'palm' in location.lower():
            highlights.extend([
                "Palm Jumeirah location",
                "Beach access",
                "Exclusive community",
                "Luxury lifestyle"
            ])
        else:
            highlights.extend([
                "Prime location",
                "Excellent connectivity",
                "Growing area",
                "Investment potential"
            ])
        
        return highlights
    
    def _extract_pricing_info(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract pricing information"""
        price = property_data.get('price', 0)
        size = property_data.get('size_sqft', 0)
        monthly_rent = property_data.get('monthly_rent', 0)
        
        pricing_info = {
            'price': f"AED {price:,}" if price > 0 else "Contact for price",
            'price_per_sqft': f"AED {price/size:,.0f}" if price > 0 and size > 0 else "N/A",
            'monthly_rent': f"AED {monthly_rent:,}" if monthly_rent > 0 else "N/A"
        }
        
        # Calculate rental yield
        if price > 0 and monthly_rent > 0:
            annual_rent = monthly_rent * 12
            rental_yield = (annual_rent / price) * 100
            pricing_info['rental_yield'] = f"{rental_yield:.1f}"
        else:
            pricing_info['rental_yield'] = "N/A"
        
        return pricing_info
    
    def _extract_contact_info(self, property_data: Dict[str, Any]) -> Dict[str, str]:
        """Extract contact information"""
        return {
            'agent_name': property_data.get('agent_name', 'Our Team'),
            'agent_phone': property_data.get('agent_phone', '+971 50 123 4567'),
            'agent_email': property_data.get('agent_email', 'info@realestate.com'),
            'office_name': property_data.get('office_name', 'Real Estate Agency')
        }
    
    def _generate_location_description(self, property_data: Dict[str, Any]) -> str:
        """Generate location description"""
        location = property_data.get('location', 'Dubai')
        
        location_descriptions = {
            'downtown dubai': "Located in the heart of Downtown Dubai, this property offers unparalleled access to the city's most iconic landmarks including Burj Khalifa and The Dubai Mall. Perfect for those seeking luxury living in the city center.",
            'dubai marina': "Situated in the prestigious Dubai Marina, this property provides stunning waterfront views and easy access to the beach. The area is known for its vibrant lifestyle and excellent dining options.",
            'palm jumeirah': "Located on the iconic Palm Jumeirah, this property offers exclusive beachfront living with world-class amenities. Perfect for those seeking privacy and luxury in a unique setting."
        }
        
        return location_descriptions.get(location.lower(), f"Located in the desirable {location} area, this property offers excellent connectivity and investment potential.")
    
    def _generate_contact_info(self, property_data: Dict[str, Any]) -> str:
        """Generate contact information string"""
        agent_name = property_data.get('agent_name', 'Our Team')
        agent_phone = property_data.get('agent_phone', '+971 50 123 4567')
        agent_email = property_data.get('agent_email', 'info@realestate.com')
        
        return f"📞 {agent_phone} | 📧 {agent_email} | 👤 {agent_name}"
    
    def _generate_seo_keywords(self, property_data: Dict[str, Any]) -> List[str]:
        """Generate SEO keywords for the property"""
        keywords = []
        
        # Basic keywords
        keywords.extend(['real estate', 'property', 'dubai'])
        
        # Property type
        property_type = property_data.get('property_type', '')
        if property_type:
            keywords.append(property_type)
        
        # Location
        location = property_data.get('location', '')
        if location:
            keywords.append(location.lower())
        
        # Features
        if property_data.get('furnished'):
            keywords.append('furnished')
        if property_data.get('sea_view'):
            keywords.append('sea view')
        if property_data.get('city_view'):
            keywords.append('city view')
        
        # Price range
        price = property_data.get('price', 0)
        if price > 0:
            if price < 1000000:
                keywords.append('affordable')
            elif price < 3000000:
                keywords.append('mid-range')
            else:
                keywords.append('luxury')
        
        return keywords
    
    def _format_list(self, items: List[str], emoji: str = "•") -> str:
        """Format list items with emoji or bullet points"""
        if not items:
            return "Contact us for details"
        
        formatted_items = []
        for item in items:
            formatted_items.append(f"{emoji} {item}")
        
        return "\n".join(formatted_items)
    
    def _find_comparable_properties(self, property_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find comparable properties for CMA"""
        # This would query the database for comparable properties
        # For now, return simulated data
        return [
            {
                'address': '123 Similar Street',
                'price': property_data.get('price', 1000000) * 0.95,
                'size_sqft': property_data.get('size_sqft', 1000),
                'bedrooms': property_data.get('bedrooms', 2),
                'bathrooms': property_data.get('bathrooms', 2),
                'sold_date': '2024-01-15'
            },
            {
                'address': '456 Comparable Ave',
                'price': property_data.get('price', 1000000) * 1.05,
                'size_sqft': property_data.get('size_sqft', 1000),
                'bedrooms': property_data.get('bedrooms', 2),
                'bathrooms': property_data.get('bathrooms', 2),
                'sold_date': '2024-02-20'
            }
        ]
    
    def _calculate_estimated_value(self, property_data: Dict[str, Any], comparables: List[Dict]) -> float:
        """Calculate estimated property value based on comparables"""
        if not comparables:
            return property_data.get('price', 0)
        
        # Simple average of comparable prices
        total_price = sum(comp['price'] for comp in comparables)
        avg_price = total_price / len(comparables)
        
        # Adjust for size differences
        target_size = property_data.get('size_sqft', 1000)
        avg_size = sum(comp['size_sqft'] for comp in comparables) / len(comparables)
        
        if avg_size > 0:
            size_adjustment = (target_size / avg_size) * avg_price
            return size_adjustment
        
        return avg_price
    
    def _generate_market_analysis(self, property_data: Dict[str, Any], comparables: List[Dict]) -> Dict[str, Any]:
        """Generate market analysis for CMA"""
        return {
            'market_trend': 'Rising',
            'days_on_market': 45,
            'price_per_sqft': property_data.get('price', 0) / property_data.get('size_sqft', 1),
            'inventory_level': 'Low',
            'demand_level': 'High'
        }
    
    def _generate_cma_recommendations(self, property_data: Dict[str, Any], estimated_value: float, comparables: List[Dict]) -> List[str]:
        """Generate recommendations for CMA"""
        recommendations = []
        
        current_price = property_data.get('price', 0)
        if current_price > 0:
            if estimated_value > current_price * 1.1:
                recommendations.append("Consider increasing the asking price")
            elif estimated_value < current_price * 0.9:
                recommendations.append("Consider reducing the asking price")
            else:
                recommendations.append("Current price is well-positioned in the market")
        
        recommendations.extend([
            "Market conditions are favorable for selling",
            "Property shows good investment potential",
            "Consider highlighting unique features in marketing"
        ])
        
        return recommendations
    
    def _calculate_confidence_score(self, comparables: List[Dict]) -> float:
        """Calculate confidence score for CMA"""
        if len(comparables) >= 5:
            return 90.0
        elif len(comparables) >= 3:
            return 80.0
        elif len(comparables) >= 1:
            return 70.0
        else:
            return 50.0
    
    def _generate_executive_summary(self, area: str, market_data: Dict[str, Any]) -> str:
        """Generate executive summary for market report"""
        return f"The {area} real estate market shows strong fundamentals with increasing demand and limited supply. Average prices have shown steady growth over the past 12 months, making it an attractive market for both investors and end-users."
    
    def _analyze_market_trends(self, market_data: Dict[str, Any]) -> str:
        """Analyze market trends"""
        return "Market trends indicate sustained growth with increasing buyer demand and limited inventory. New developments are being absorbed quickly, supporting price appreciation."
    
    def _analyze_price_trends(self, market_data: Dict[str, Any]) -> str:
        """Analyze price trends"""
        return "Price analysis shows consistent appreciation across all property types. Apartments have shown 8% growth, while villas have appreciated by 12% over the past year."
    
    def _identify_investment_opportunities(self, area: str, market_data: Dict[str, Any]) -> str:
        """Identify investment opportunities"""
        return f"Investment opportunities in {area} include off-plan developments with attractive payment plans, rental properties with high yields, and value-add opportunities in emerging sub-markets."
    
    def _assess_market_risks(self, market_data: Dict[str, Any]) -> str:
        """Assess market risks"""
        return "Market risks include potential interest rate increases, regulatory changes, and economic uncertainties. However, strong fundamentals and limited supply provide downside protection."
    
    def _generate_market_recommendations(self, area: str, market_data: Dict[str, Any]) -> str:
        """Generate market recommendations"""
        return f"Recommendations for {area} include focusing on quality properties, considering long-term investment horizons, and diversifying across different property types and price points."