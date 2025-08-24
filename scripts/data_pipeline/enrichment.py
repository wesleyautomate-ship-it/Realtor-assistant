"""
Data Enrichment Layer

Enriches data with additional context, calculated fields, and market intelligence.
"""

import pandas as pd
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

class DataEnricher:
    """Enriches data with additional context and calculations"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def enrich_property_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enrich property data with calculated fields and market context"""
        enriched_data = []
        
        for item in data:
            enriched_item = item.copy()
            
            # Calculate price per square foot
            if item.get('price_aed') and item.get('square_feet'):
                enriched_item['price_per_sqft'] = item['price_aed'] / item['square_feet']
            
            # Add market context
            enriched_item['market_context'] = self._get_market_context(item)
            
            # Add investment metrics
            enriched_item['investment_metrics'] = self._calculate_investment_metrics(item)
            
            # Add property classification
            enriched_item['property_classification'] = self._classify_property(item)
            
            # Add location intelligence
            enriched_item['location_intelligence'] = self._get_location_intelligence(item)
            
            # Add timestamp
            enriched_item['enriched_at'] = datetime.now().isoformat()
            
            enriched_data.append(enriched_item)
        
        return enriched_data
    
    def _get_market_context(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get market context for the property"""
        area = property_data.get('area', 'Unknown')
        
        # Market context based on area (this would come from your market data)
        market_context = {
            'area': area,
            'market_trend': self._get_area_market_trend(area),
            'average_price_per_sqft': self._get_area_average_price(area),
            'rental_yield': self._get_area_rental_yield(area),
            'demand_level': self._get_area_demand_level(area),
            'market_volatility': self._get_area_volatility(area),
            'investment_grade': self._get_area_investment_grade(area)
        }
        
        return market_context
    
    def _calculate_investment_metrics(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate investment-related metrics"""
        price = property_data.get('price_aed')
        price_per_sqft = property_data.get('price_per_sqft')
        
        if not price or not price_per_sqft:
            return {}
        
        # Calculate estimated rental income (based on area averages)
        area = property_data.get('area', 'Unknown')
        estimated_rental = self._estimate_rental_income(price, area)
        
        # Calculate potential yield
        potential_yield = (estimated_rental / price) * 100 if price > 0 else 0
        
        # Calculate ROI metrics
        roi_metrics = self._calculate_roi_metrics(price, estimated_rental, area)
        
        return {
            'estimated_rental_income': estimated_rental,
            'potential_yield': potential_yield,
            'investment_grade': self._grade_investment(potential_yield),
            'payback_period': self._calculate_payback_period(price, estimated_rental),
            'roi_metrics': roi_metrics,
            'capital_appreciation_potential': self._estimate_capital_appreciation(area),
            'risk_assessment': self._assess_investment_risk(property_data)
        }
    
    def _classify_property(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Classify property based on various criteria"""
        price = property_data.get('price_aed', 0)
        bedrooms = property_data.get('bedrooms', 0)
        area = property_data.get('area', 'Unknown')
        square_feet = property_data.get('square_feet', 0)
        
        # Price classification
        if price < 1000000:
            price_class = 'Affordable'
        elif price < 3000000:
            price_class = 'Mid-Market'
        elif price < 10000000:
            price_class = 'Luxury'
        else:
            price_class = 'Ultra-Luxury'
        
        # Size classification
        if bedrooms == 0:
            size_class = 'Studio'
        elif bedrooms == 1:
            size_class = '1-Bedroom'
        elif bedrooms == 2:
            size_class = '2-Bedroom'
        elif bedrooms == 3:
            size_class = '3-Bedroom'
        else:
            size_class = 'Large'
        
        # Area classification
        premium_areas = ['Palm Jumeirah', 'Downtown Dubai', 'Dubai Marina']
        area_class = 'Premium' if area in premium_areas else 'Standard'
        
        # Property type classification
        property_type = property_data.get('property_type', 'Unknown')
        type_class = self._classify_property_type(property_type)
        
        return {
            'price_class': price_class,
            'size_class': size_class,
            'area_class': area_class,
            'type_class': type_class,
            'overall_class': f"{price_class} {size_class}",
            'target_market': self._identify_target_market(price, bedrooms, area)
        }
    
    def _get_location_intelligence(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get location-specific intelligence"""
        area = property_data.get('area', 'Unknown')
        
        return {
            'area': area,
            'proximity_to_amenities': self._get_amenity_proximity(area),
            'transportation_score': self._get_transportation_score(area),
            'school_rating': self._get_school_rating(area),
            'safety_score': self._get_safety_score(area),
            'lifestyle_score': self._get_lifestyle_score(area),
            'future_development': self._get_future_development(area)
        }
    
    def _get_area_market_trend(self, area: str) -> str:
        """Get market trend for specific area"""
        trends = {
            'Dubai Marina': 'Stable',
            'Downtown Dubai': 'Growing',
            'Palm Jumeirah': 'Growing',
            'Business Bay': 'Stable',
            'Dubai Hills Estate': 'Growing',
            'Jumeirah Beach Residence': 'Stable',
            'Dubai Silicon Oasis': 'Growing',
            'Dubai Sports City': 'Stable',
            'Dubai Production City': 'Growing',
            'Dubai Creek Harbour': 'Growing'
        }
        return trends.get(area, 'Unknown')
    
    def _get_area_average_price(self, area: str) -> float:
        """Get average price per sqft for area"""
        averages = {
            'Dubai Marina': 1200,
            'Downtown Dubai': 1500,
            'Palm Jumeirah': 2000,
            'Business Bay': 1000,
            'Dubai Hills Estate': 1100,
            'Jumeirah Beach Residence': 1300,
            'Dubai Silicon Oasis': 800,
            'Dubai Sports City': 900,
            'Dubai Production City': 700,
            'Dubai Creek Harbour': 1400
        }
        return averages.get(area, 0)
    
    def _get_area_rental_yield(self, area: str) -> float:
        """Get average rental yield for area"""
        yields = {
            'Dubai Marina': 6.5,
            'Downtown Dubai': 5.8,
            'Palm Jumeirah': 4.2,
            'Business Bay': 7.1,
            'Dubai Hills Estate': 6.8,
            'Jumeirah Beach Residence': 6.0,
            'Dubai Silicon Oasis': 7.5,
            'Dubai Sports City': 6.2,
            'Dubai Production City': 8.0,
            'Dubai Creek Harbour': 5.5
        }
        return yields.get(area, 0)
    
    def _get_area_demand_level(self, area: str) -> str:
        """Get demand level for area"""
        demand = {
            'Dubai Marina': 'High',
            'Downtown Dubai': 'Very High',
            'Palm Jumeirah': 'High',
            'Business Bay': 'Medium',
            'Dubai Hills Estate': 'High',
            'Jumeirah Beach Residence': 'High',
            'Dubai Silicon Oasis': 'Medium',
            'Dubai Sports City': 'Medium',
            'Dubai Production City': 'Low',
            'Dubai Creek Harbour': 'High'
        }
        return demand.get(area, 'Unknown')
    
    def _get_area_volatility(self, area: str) -> str:
        """Get market volatility for area"""
        volatility = {
            'Dubai Marina': 'Low',
            'Downtown Dubai': 'Medium',
            'Palm Jumeirah': 'Low',
            'Business Bay': 'Medium',
            'Dubai Hills Estate': 'Low',
            'Jumeirah Beach Residence': 'Low',
            'Dubai Silicon Oasis': 'High',
            'Dubai Sports City': 'Medium',
            'Dubai Production City': 'High',
            'Dubai Creek Harbour': 'Medium'
        }
        return volatility.get(area, 'Unknown')
    
    def _get_area_investment_grade(self, area: str) -> str:
        """Get investment grade for area"""
        grades = {
            'Dubai Marina': 'A',
            'Downtown Dubai': 'A+',
            'Palm Jumeirah': 'A+',
            'Business Bay': 'B+',
            'Dubai Hills Estate': 'A',
            'Jumeirah Beach Residence': 'A',
            'Dubai Silicon Oasis': 'B',
            'Dubai Sports City': 'B',
            'Dubai Production City': 'C',
            'Dubai Creek Harbour': 'A'
        }
        return grades.get(area, 'Unknown')
    
    def _estimate_rental_income(self, price: float, area: str) -> float:
        """Estimate annual rental income"""
        yield_rate = self._get_area_rental_yield(area) / 100
        return price * yield_rate
    
    def _grade_investment(self, yield_rate: float) -> str:
        """Grade investment based on yield"""
        if yield_rate >= 7:
            return 'Excellent'
        elif yield_rate >= 6:
            return 'Good'
        elif yield_rate >= 5:
            return 'Average'
        else:
            return 'Below Average'
    
    def _calculate_payback_period(self, price: float, annual_rental: float) -> float:
        """Calculate payback period in years"""
        if annual_rental <= 0:
            return float('inf')
        return price / annual_rental
    
    def _calculate_roi_metrics(self, price: float, annual_rental: float, area: str) -> Dict[str, Any]:
        """Calculate comprehensive ROI metrics"""
        # Basic ROI
        basic_roi = (annual_rental / price) * 100 if price > 0 else 0
        
        # Capital appreciation potential
        appreciation_rate = self._get_area_appreciation_rate(area)
        annual_appreciation = price * (appreciation_rate / 100)
        
        # Total ROI (rental + appreciation)
        total_roi = ((annual_rental + annual_appreciation) / price) * 100 if price > 0 else 0
        
        return {
            'basic_roi': basic_roi,
            'appreciation_rate': appreciation_rate,
            'annual_appreciation': annual_appreciation,
            'total_roi': total_roi,
            'roi_grade': self._grade_roi(total_roi)
        }
    
    def _get_area_appreciation_rate(self, area: str) -> float:
        """Get annual appreciation rate for area"""
        rates = {
            'Dubai Marina': 3.5,
            'Downtown Dubai': 4.2,
            'Palm Jumeirah': 5.0,
            'Business Bay': 2.8,
            'Dubai Hills Estate': 3.8,
            'Jumeirah Beach Residence': 3.2,
            'Dubai Silicon Oasis': 2.5,
            'Dubai Sports City': 2.8,
            'Dubai Production City': 1.5,
            'Dubai Creek Harbour': 4.5
        }
        return rates.get(area, 2.0)
    
    def _grade_roi(self, total_roi: float) -> str:
        """Grade ROI performance"""
        if total_roi >= 10:
            return 'Exceptional'
        elif total_roi >= 8:
            return 'Excellent'
        elif total_roi >= 6:
            return 'Good'
        elif total_roi >= 4:
            return 'Average'
        else:
            return 'Below Average'
    
    def _estimate_capital_appreciation(self, area: str) -> Dict[str, Any]:
        """Estimate capital appreciation potential"""
        appreciation_rate = self._get_area_appreciation_rate(area)
        
        return {
            'annual_rate': appreciation_rate,
            '5_year_potential': appreciation_rate * 5,
            '10_year_potential': appreciation_rate * 10,
            'confidence_level': self._get_appreciation_confidence(area)
        }
    
    def _get_appreciation_confidence(self, area: str) -> str:
        """Get confidence level for appreciation estimates"""
        confidence = {
            'Dubai Marina': 'High',
            'Downtown Dubai': 'Very High',
            'Palm Jumeirah': 'High',
            'Business Bay': 'Medium',
            'Dubai Hills Estate': 'High',
            'Jumeirah Beach Residence': 'High',
            'Dubai Silicon Oasis': 'Medium',
            'Dubai Sports City': 'Medium',
            'Dubai Production City': 'Low',
            'Dubai Creek Harbour': 'High'
        }
        return confidence.get(area, 'Unknown')
    
    def _assess_investment_risk(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess investment risk factors"""
        area = property_data.get('area', 'Unknown')
        price = property_data.get('price_aed', 0)
        
        risk_factors = {
            'market_risk': self._assess_market_risk(area),
            'liquidity_risk': self._assess_liquidity_risk(area, price),
            'concentration_risk': self._assess_concentration_risk(area),
            'regulatory_risk': self._assess_regulatory_risk(),
            'overall_risk_score': 0
        }
        
        # Calculate overall risk score
        risk_scores = {
            'Low': 1,
            'Medium': 2,
            'High': 3
        }
        
        total_risk = sum(risk_scores.get(risk, 2) for risk in risk_factors.values() if risk != 'overall_risk_score')
        risk_factors['overall_risk_score'] = total_risk / 4  # Average of 4 risk factors
        
        return risk_factors
    
    def _assess_market_risk(self, area: str) -> str:
        """Assess market risk for area"""
        market_risk = {
            'Dubai Marina': 'Low',
            'Downtown Dubai': 'Low',
            'Palm Jumeirah': 'Low',
            'Business Bay': 'Medium',
            'Dubai Hills Estate': 'Low',
            'Jumeirah Beach Residence': 'Low',
            'Dubai Silicon Oasis': 'Medium',
            'Dubai Sports City': 'Medium',
            'Dubai Production City': 'High',
            'Dubai Creek Harbour': 'Medium'
        }
        return market_risk.get(area, 'Medium')
    
    def _assess_liquidity_risk(self, area: str, price: float) -> str:
        """Assess liquidity risk"""
        if price > 10000000:  # Very expensive properties
            return 'High'
        elif area in ['Dubai Marina', 'Downtown Dubai', 'Palm Jumeirah']:
            return 'Low'
        elif area in ['Dubai Production City', 'Dubai Silicon Oasis']:
            return 'Medium'
        else:
            return 'Medium'
    
    def _assess_concentration_risk(self, area: str) -> str:
        """Assess concentration risk"""
        # Areas with high supply concentration
        high_concentration = ['Dubai Marina', 'Business Bay', 'Dubai Silicon Oasis']
        if area in high_concentration:
            return 'Medium'
        else:
            return 'Low'
    
    def _assess_regulatory_risk(self) -> str:
        """Assess regulatory risk"""
        # Dubai has stable real estate regulations
        return 'Low'
    
    def _classify_property_type(self, property_type: str) -> str:
        """Classify property type"""
        if property_type in ['Studio']:
            return 'Entry Level'
        elif property_type in ['Apartment', '1-Bedroom', '2-Bedroom']:
            return 'Residential'
        elif property_type in ['Villa', 'Townhouse', '3-Bedroom', '4-Bedroom']:
            return 'Family'
        elif property_type in ['Penthouse', 'Duplex']:
            return 'Luxury'
        else:
            return 'Other'
    
    def _identify_target_market(self, price: float, bedrooms: int, area: str) -> List[str]:
        """Identify target market segments"""
        targets = []
        
        if price < 1000000:
            targets.append('First-time Buyers')
        elif price < 3000000:
            targets.append('Young Professionals')
        elif price < 10000000:
            targets.append('Established Professionals')
        else:
            targets.append('High Net Worth Individuals')
        
        if bedrooms == 0:
            targets.append('Singles')
        elif bedrooms == 1:
            targets.append('Couples')
        elif bedrooms >= 3:
            targets.append('Families')
        
        if area in ['Dubai Marina', 'Downtown Dubai']:
            targets.append('Urban Professionals')
        elif area in ['Dubai Hills Estate', 'Palm Jumeirah']:
            targets.append('Families')
        
        return list(set(targets))  # Remove duplicates
    
    def _get_amenity_proximity(self, area: str) -> Dict[str, str]:
        """Get proximity to amenities"""
        proximity_data = {
            'Dubai Marina': {
                'shopping': 'Excellent',
                'dining': 'Excellent',
                'entertainment': 'Excellent',
                'transportation': 'Excellent',
                'schools': 'Good'
            },
            'Downtown Dubai': {
                'shopping': 'Excellent',
                'dining': 'Excellent',
                'entertainment': 'Excellent',
                'transportation': 'Excellent',
                'schools': 'Good'
            }
        }
        return proximity_data.get(area, {
            'shopping': 'Good',
            'dining': 'Good',
            'entertainment': 'Good',
            'transportation': 'Good',
            'schools': 'Good'
        })
    
    def _get_transportation_score(self, area: str) -> int:
        """Get transportation accessibility score (1-10)"""
        scores = {
            'Dubai Marina': 9,
            'Downtown Dubai': 10,
            'Palm Jumeirah': 7,
            'Business Bay': 8,
            'Dubai Hills Estate': 6,
            'Jumeirah Beach Residence': 8,
            'Dubai Silicon Oasis': 7,
            'Dubai Sports City': 6,
            'Dubai Production City': 5,
            'Dubai Creek Harbour': 8
        }
        return scores.get(area, 5)
    
    def _get_school_rating(self, area: str) -> str:
        """Get school quality rating"""
        ratings = {
            'Dubai Marina': 'Good',
            'Downtown Dubai': 'Good',
            'Palm Jumeirah': 'Excellent',
            'Business Bay': 'Good',
            'Dubai Hills Estate': 'Excellent',
            'Jumeirah Beach Residence': 'Good',
            'Dubai Silicon Oasis': 'Good',
            'Dubai Sports City': 'Good',
            'Dubai Production City': 'Fair',
            'Dubai Creek Harbour': 'Good'
        }
        return ratings.get(area, 'Good')
    
    def _get_safety_score(self, area: str) -> int:
        """Get safety score (1-10)"""
        scores = {
            'Dubai Marina': 9,
            'Downtown Dubai': 10,
            'Palm Jumeirah': 10,
            'Business Bay': 9,
            'Dubai Hills Estate': 9,
            'Jumeirah Beach Residence': 9,
            'Dubai Silicon Oasis': 8,
            'Dubai Sports City': 8,
            'Dubai Production City': 7,
            'Dubai Creek Harbour': 9
        }
        return scores.get(area, 8)
    
    def _get_lifestyle_score(self, area: str) -> int:
        """Get lifestyle score (1-10)"""
        scores = {
            'Dubai Marina': 9,
            'Downtown Dubai': 10,
            'Palm Jumeirah': 10,
            'Business Bay': 8,
            'Dubai Hills Estate': 9,
            'Jumeirah Beach Residence': 9,
            'Dubai Silicon Oasis': 7,
            'Dubai Sports City': 8,
            'Dubai Production City': 6,
            'Dubai Creek Harbour': 9
        }
        return scores.get(area, 7)
    
    def _get_future_development(self, area: str) -> Dict[str, Any]:
        """Get future development plans"""
        developments = {
            'Dubai Marina': {
                'planned_projects': 3,
                'estimated_completion': '2026',
                'impact': 'Positive'
            },
            'Downtown Dubai': {
                'planned_projects': 5,
                'estimated_completion': '2027',
                'impact': 'Very Positive'
            },
            'Dubai Creek Harbour': {
                'planned_projects': 8,
                'estimated_completion': '2030',
                'impact': 'Very Positive'
            }
        }
        return developments.get(area, {
            'planned_projects': 0,
            'estimated_completion': 'N/A',
            'impact': 'Neutral'
        })
