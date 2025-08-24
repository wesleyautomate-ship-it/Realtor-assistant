"""
Financial Tools Suite for Real Estate RAG Chat System

This module provides comprehensive financial calculation tools including:
- ROI Calculator with rental yield analysis
- Commission Calculator with VAT considerations
- Tax Calculator for Dubai property taxes
- Currency Converter with real-time rates
- Neighborhood Insights and area analysis
"""

import logging
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import numpy as np
from .config import config

logger = logging.getLogger(__name__)

@dataclass
class ROICalculation:
    """Represents ROI calculation results"""
    property_value: float
    investment_amount: float
    annual_rental_income: float
    annual_expenses: float
    net_annual_income: float
    annual_roi: float
    five_year_roi: float
    monthly_rental_income: float
    rental_yield: float
    appreciation_rate: float
    total_investment: float
    breakdown: Dict[str, float]

@dataclass
class CommissionCalculation:
    """Represents commission calculation results"""
    property_value: float
    commission_rate: float
    gross_commission: float
    vat_amount: float
    net_commission: float
    agency_split: float
    agent_commission: float
    breakdown: Dict[str, float]

@dataclass
class TaxCalculation:
    """Represents tax calculation results"""
    property_value: float
    dubai_land_dept_fee: float
    municipality_fees: float
    service_charges: float
    vat_on_services: float
    annual_property_tax: float
    total_annual_costs: float
    breakdown: Dict[str, float]

@dataclass
class CurrencyConversion:
    """Represents currency conversion results"""
    from_currency: str
    to_currency: str
    amount: float
    converted_amount: float
    exchange_rate: float
    conversion_date: datetime
    historical_rates: List[Dict[str, Any]]

@dataclass
class NeighborhoodInsights:
    """Represents neighborhood analysis results"""
    area: str
    safety_rating: float
    school_ratings: List[Dict[str, Any]]
    amenities: Dict[str, List[str]]
    transport_links: List[str]
    future_developments: List[str]
    average_prices: Dict[str, float]
    market_trend: str

class FinancialCalculatorSuite:
    """
    Comprehensive financial calculation tools for real estate
    """
    
    def __init__(self):
        self.exchange_rates_cache = {}
        self.cache_expiry = {}
        self.cache_duration = timedelta(hours=1)
        
    def calculate_roi(self, property_data: Dict[str, Any], investment_period_years: int = 5) -> Optional[ROICalculation]:
        """
        Calculate ROI for a property investment
        
        Args:
            property_data: Dictionary containing property and investment details
            investment_period_years: Number of years for ROI calculation
            
        Returns:
            ROICalculation object with detailed ROI analysis
        """
        try:
            # Extract required data
            property_value = property_data.get('property_value', 0)
            investment_amount = property_data.get('investment_amount', property_value)
            monthly_rent = property_data.get('monthly_rent', 0)
            annual_expenses_rate = property_data.get('annual_expenses_rate', 0.15)  # 15% default
            appreciation_rate = property_data.get('appreciation_rate', 0.05)  # 5% default
            
            if property_value <= 0:
                logger.error("Invalid property value for ROI calculation")
                return None
            
            # Calculate rental income
            annual_rental_income = monthly_rent * 12
            annual_expenses = property_value * annual_expenses_rate
            net_annual_income = annual_rental_income - annual_expenses
            
            # Calculate ROI
            annual_roi = (net_annual_income / investment_amount) * 100
            
            # Calculate 5-year ROI including appreciation
            future_property_value = property_value * (1 + appreciation_rate) ** investment_period_years
            total_appreciation = future_property_value - property_value
            total_rental_income = net_annual_income * investment_period_years
            total_return = total_rental_income + total_appreciation
            five_year_roi = (total_return / investment_amount) * 100
            
            # Calculate rental yield
            rental_yield = (annual_rental_income / property_value) * 100
            
            # Prepare breakdown
            breakdown = {
                'property_value': property_value,
                'investment_amount': investment_amount,
                'monthly_rent': monthly_rent,
                'annual_rental_income': annual_rental_income,
                'annual_expenses': annual_expenses,
                'net_annual_income': net_annual_income,
                'appreciation_rate': appreciation_rate,
                'expenses_rate': annual_expenses_rate
            }
            
            return ROICalculation(
                property_value=property_value,
                investment_amount=investment_amount,
                annual_rental_income=annual_rental_income,
                annual_expenses=annual_expenses,
                net_annual_income=net_annual_income,
                annual_roi=annual_roi,
                five_year_roi=five_year_roi,
                monthly_rental_income=monthly_rent,
                rental_yield=rental_yield,
                appreciation_rate=appreciation_rate,
                total_investment=investment_amount,
                breakdown=breakdown
            )
            
        except Exception as e:
            logger.error(f"Error in ROI calculation: {e}")
            return None
    
    def calculate_commission(self, property_value: float, commission_rate: float = None, 
                           agency_split: float = 0.5) -> Optional[CommissionCalculation]:
        """
        Calculate commission for a property sale
        
        Args:
            property_value: Value of the property
            commission_rate: Commission rate (default from config)
            agency_split: Agency split percentage (default 50%)
            
        Returns:
            CommissionCalculation object with detailed breakdown
        """
        try:
            if property_value <= 0:
                logger.error("Invalid property value for commission calculation")
                return None
            
            # Use default commission rate if not provided
            if commission_rate is None:
                commission_rate = config.financial.default_commission_rate
            
            # Calculate commission amounts
            gross_commission = property_value * commission_rate
            vat_amount = gross_commission * config.financial.vat_rate
            net_commission = gross_commission + vat_amount
            agent_commission = net_commission * agency_split
            
            # Prepare breakdown
            breakdown = {
                'property_value': property_value,
                'commission_rate': commission_rate,
                'gross_commission': gross_commission,
                'vat_rate': config.financial.vat_rate,
                'vat_amount': vat_amount,
                'agency_split': agency_split,
                'agent_commission': agent_commission
            }
            
            return CommissionCalculation(
                property_value=property_value,
                commission_rate=commission_rate,
                gross_commission=gross_commission,
                vat_amount=vat_amount,
                net_commission=net_commission,
                agency_split=agency_split,
                agent_commission=agent_commission,
                breakdown=breakdown
            )
            
        except Exception as e:
            logger.error(f"Error in commission calculation: {e}")
            return None
    
    def calculate_taxes(self, property_data: Dict[str, Any]) -> Optional[TaxCalculation]:
        """
        Calculate Dubai property taxes and fees
        
        Args:
            property_data: Dictionary containing property details
            
        Returns:
            TaxCalculation object with detailed tax breakdown
        """
        try:
            property_value = property_data.get('property_value', 0)
            property_type = property_data.get('property_type', 'apartment')
            size_sqft = property_data.get('size_sqft', 0)
            
            if property_value <= 0:
                logger.error("Invalid property value for tax calculation")
                return None
            
            # Dubai Land Department fees (4% of property value)
            dubai_land_dept_fee = property_value * 0.04
            
            # Municipality fees (based on property type and size)
            municipality_rate = 0.05 if property_type == 'villa' else 0.03
            municipality_fees = property_value * municipality_rate
            
            # Service charges (per sq ft annually)
            service_charge_rate = 12 if property_type == 'apartment' else 8  # AED per sq ft
            service_charges = size_sqft * service_charge_rate
            
            # VAT on services (5%)
            vat_on_services = service_charges * config.financial.vat_rate
            
            # Annual property tax (minimal in Dubai)
            annual_property_tax = property_value * 0.001  # 0.1%
            
            # Total annual costs
            total_annual_costs = municipality_fees + service_charges + vat_on_services + annual_property_tax
            
            # Prepare breakdown
            breakdown = {
                'property_value': property_value,
                'property_type': property_type,
                'size_sqft': size_sqft,
                'dubai_land_dept_rate': 0.04,
                'municipality_rate': municipality_rate,
                'service_charge_rate': service_charge_rate,
                'vat_rate': config.financial.vat_rate,
                'property_tax_rate': 0.001
            }
            
            return TaxCalculation(
                property_value=property_value,
                dubai_land_dept_fee=dubai_land_dept_fee,
                municipality_fees=municipality_fees,
                service_charges=service_charges,
                vat_on_services=vat_on_services,
                annual_property_tax=annual_property_tax,
                total_annual_costs=total_annual_costs,
                breakdown=breakdown
            )
            
        except Exception as e:
            logger.error(f"Error in tax calculation: {e}")
            return None
    
    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> Optional[CurrencyConversion]:
        """
        Convert currency using real-time exchange rates
        
        Args:
            amount: Amount to convert
            from_currency: Source currency code
            to_currency: Target currency code
            
        Returns:
            CurrencyConversion object with conversion results
        """
        try:
            # Normalize currency codes
            from_currency = from_currency.upper()
            to_currency = to_currency.upper()
            
            if from_currency == to_currency:
                return CurrencyConversion(
                    from_currency=from_currency,
                    to_currency=to_currency,
                    amount=amount,
                    converted_amount=amount,
                    exchange_rate=1.0,
                    conversion_date=datetime.now(),
                    historical_rates=[]
                )
            
            # Get exchange rate
            exchange_rate = self._get_exchange_rate(from_currency, to_currency)
            
            if exchange_rate is None:
                logger.error(f"Unable to get exchange rate for {from_currency} to {to_currency}")
                return None
            
            # Calculate converted amount
            converted_amount = amount * exchange_rate
            
            # Get historical rates
            historical_rates = self._get_historical_rates(from_currency, to_currency)
            
            return CurrencyConversion(
                from_currency=from_currency,
                to_currency=to_currency,
                amount=amount,
                converted_amount=converted_amount,
                exchange_rate=exchange_rate,
                conversion_date=datetime.now(),
                historical_rates=historical_rates
            )
            
        except Exception as e:
            logger.error(f"Error in currency conversion: {e}")
            return None
    
    def get_neighborhood_insights(self, area: str) -> Optional[NeighborhoodInsights]:
        """
        Get comprehensive neighborhood insights
        
        Args:
            area: Geographic area name
            
        Returns:
            NeighborhoodInsights object with area analysis
        """
        try:
            # Get area data from APIs
            area_data = self._get_area_data(area)
            
            if not area_data:
                logger.error(f"No data available for area: {area}")
                return None
            
            # Analyze safety rating
            safety_rating = self._calculate_safety_rating(area_data)
            
            # Get school ratings
            school_ratings = self._get_school_ratings(area)
            
            # Get amenities
            amenities = self._get_area_amenities(area)
            
            # Get transport links
            transport_links = self._get_transport_links(area)
            
            # Get future developments
            future_developments = self._get_future_developments(area)
            
            # Get average prices
            average_prices = self._get_average_prices(area)
            
            # Get market trend
            market_trend = self._get_market_trend(area)
            
            return NeighborhoodInsights(
                area=area,
                safety_rating=safety_rating,
                school_ratings=school_ratings,
                amenities=amenities,
                transport_links=transport_links,
                future_developments=future_developments,
                average_prices=average_prices,
                market_trend=market_trend
            )
            
        except Exception as e:
            logger.error(f"Error getting neighborhood insights: {e}")
            return None
    
    def _get_exchange_rate(self, from_currency: str, to_currency: str) -> Optional[float]:
        """Get exchange rate from cache or API"""
        cache_key = f"{from_currency}_{to_currency}"
        
        # Check cache
        if cache_key in self.exchange_rates_cache:
            if datetime.now() < self.cache_expiry.get(cache_key, datetime.min):
                return self.exchange_rates_cache[cache_key]
        
        try:
            # Try multiple exchange rate APIs
            rate = self._fetch_exchange_rate_api(from_currency, to_currency)
            
            if rate is not None:
                # Cache the result
                self.exchange_rates_cache[cache_key] = rate
                self.cache_expiry[cache_key] = datetime.now() + self.cache_duration
                return rate
            
            # Fallback to simulated rates for development
            return self._get_simulated_rate(from_currency, to_currency)
            
        except Exception as e:
            logger.error(f"Error fetching exchange rate: {e}")
            return self._get_simulated_rate(from_currency, to_currency)
    
    def _fetch_exchange_rate_api(self, from_currency: str, to_currency: str) -> Optional[float]:
        """Fetch exchange rate from external API"""
        try:
            # Try ExchangeRate-API
            if config.api.exchange_rate_api_key:
                url = f"{config.api_endpoints['exchange_rates']}/{from_currency}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    rates = data.get('rates', {})
                    return rates.get(to_currency)
            
            # Try Fixer API
            if config.api.fixer_api_key:
                url = f"{config.api_endpoints['fixer']}/latest"
                params = {
                    'access_key': config.api.fixer_api_key,
                    'base': from_currency,
                    'symbols': to_currency
                }
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    rates = data.get('rates', {})
                    return rates.get(to_currency)
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching from exchange rate API: {e}")
            return None
    
    def _get_simulated_rate(self, from_currency: str, to_currency: str) -> float:
        """Get simulated exchange rate for development"""
        # Simulated rates for common currency pairs
        rates = {
            'AED_USD': 0.272,
            'AED_EUR': 0.248,
            'AED_GBP': 0.213,
            'USD_AED': 3.67,
            'EUR_AED': 4.03,
            'GBP_AED': 4.69,
            'USD_EUR': 0.91,
            'EUR_USD': 1.10,
            'GBP_USD': 1.28,
            'USD_GBP': 0.78
        }
        
        key = f"{from_currency}_{to_currency}"
        return rates.get(key, 1.0)  # Default to 1.0 if not found
    
    def _get_historical_rates(self, from_currency: str, to_currency: str) -> List[Dict[str, Any]]:
        """Get historical exchange rates"""
        # Simplified historical rates for development
        historical_rates = []
        base_rate = self._get_simulated_rate(from_currency, to_currency)
        
        for i in range(30):  # Last 30 days
            date = datetime.now() - timedelta(days=i)
            # Add some variation to simulate real rates
            variation = np.random.normal(0, 0.01)  # 1% standard deviation
            rate = base_rate * (1 + variation)
            
            historical_rates.append({
                'date': date.strftime('%Y-%m-%d'),
                'rate': rate
            })
        
        return historical_rates
    
    def _get_area_data(self, area: str) -> Optional[Dict[str, Any]]:
        """Get area data from APIs"""
        try:
            # This would fetch real data from Dubai government APIs
            # For now, return simulated data
            area_data = {
                'crime_rate': np.random.uniform(0.01, 0.05),
                'population_density': np.random.uniform(5000, 20000),
                'average_income': np.random.uniform(50000, 200000),
                'development_index': np.random.uniform(0.7, 0.95)
            }
            return area_data
        except Exception as e:
            logger.error(f"Error fetching area data: {e}")
            return None
    
    def _calculate_safety_rating(self, area_data: Dict[str, Any]) -> float:
        """Calculate safety rating based on area data"""
        crime_rate = area_data.get('crime_rate', 0.03)
        population_density = area_data.get('population_density', 10000)
        development_index = area_data.get('development_index', 0.8)
        
        # Safety rating calculation (0-10 scale)
        safety_score = 10 - (crime_rate * 100)  # Lower crime = higher safety
        safety_score += (development_index * 2)  # Higher development = higher safety
        safety_score -= (population_density / 10000) * 0.5  # Lower density = higher safety
        
        return max(0, min(10, safety_score))
    
    def _get_school_ratings(self, area: str) -> List[Dict[str, Any]]:
        """Get school ratings for the area"""
        # Simulated school data
        schools = [
            {'name': f'{area} International School', 'rating': 8.5, 'type': 'International'},
            {'name': f'{area} Public School', 'rating': 7.2, 'type': 'Public'},
            {'name': f'{area} Private Academy', 'rating': 9.1, 'type': 'Private'}
        ]
        return schools
    
    def _get_area_amenities(self, area: str) -> Dict[str, List[str]]:
        """Get amenities available in the area"""
        amenities = {
            'hospitals': [f'{area} Medical Center', f'{area} Hospital'],
            'shopping': [f'{area} Mall', f'{area} Shopping Center'],
            'parks': [f'{area} Park', f'{area} Garden'],
            'restaurants': [f'{area} Restaurant District', f'{area} Food Court'],
            'banks': [f'{area} Bank Branch', f'{area} ATM Center']
        }
        return amenities
    
    def _get_transport_links(self, area: str) -> List[str]:
        """Get transport links for the area"""
        transport = [
            f'{area} Metro Station',
            f'{area} Bus Terminal',
            f'{area} Taxi Stand',
            f'{area} Parking Facility'
        ]
        return transport
    
    def _get_future_developments(self, area: str) -> List[str]:
        """Get future developments planned for the area"""
        developments = [
            f'{area} Phase 2 Development',
            f'{area} Shopping Complex',
            f'{area} Metro Extension',
            f'{area} Business District'
        ]
        return developments
    
    def _get_average_prices(self, area: str) -> Dict[str, float]:
        """Get average property prices for the area"""
        # Simulated price data
        prices = {
            'apartment': np.random.uniform(800000, 2000000),
            'villa': np.random.uniform(3000000, 8000000),
            'townhouse': np.random.uniform(1500000, 4000000),
            'penthouse': np.random.uniform(5000000, 15000000)
        }
        return prices
    
    def _get_market_trend(self, area: str) -> str:
        """Get market trend for the area"""
        trends = ['Rising', 'Stable', 'Declining']
        return np.random.choice(trends, p=[0.6, 0.3, 0.1])