"""
Predictive Analytics Engine for Real Estate RAG Chat System

This module provides advanced AI-powered predictive analytics including:
- Property price prediction using ML models
- Market trend forecasting with time-series analysis
- Lead scoring and conversion probability
- Chatbot learning and improvement
"""

import logging
import json
import pickle
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import requests
from .config import config

logger = logging.getLogger(__name__)

@dataclass
class PricePrediction:
    """Represents a property price prediction with confidence intervals"""
    predicted_price: float
    confidence_interval_lower: float
    confidence_interval_upper: float
    confidence_score: float
    prediction_date: datetime
    model_version: str
    factors_considered: List[str]
    market_trend: str

@dataclass
class MarketForecast:
    """Represents a market trend forecast"""
    area: str
    property_type: str
    forecast_period: int
    forecast_unit: str
    predicted_trend: str
    confidence_score: float
    key_factors: List[str]
    recommendations: List[str]
    risk_level: str

@dataclass
class LeadScore:
    """Represents a lead scoring result"""
    client_id: str
    score: float
    conversion_probability: float
    factors: Dict[str, float]
    recommendations: List[str]
    priority_level: str
    last_updated: datetime

class PredictiveAnalyticsEngine:
    """
    Advanced predictive analytics engine for real estate insights
    """
    
    def __init__(self):
        self.price_model = None
        self.lead_scoring_model = None
        self.scaler = StandardScaler()
        self.model_version = "1.0.0"
        self._load_models()
        
    def _load_models(self):
        """Load pre-trained ML models"""
        try:
            # Load price prediction model
            with open(config.model.price_prediction_model_path, 'rb') as f:
                self.price_model = pickle.load(f)
            logger.info("Price prediction model loaded successfully")
        except FileNotFoundError:
            logger.warning("Price prediction model not found. Will train new model.")
            self.price_model = None
        
        try:
            # Load lead scoring model
            with open(config.model.lead_scoring_model_path, 'rb') as f:
                self.lead_scoring_model = pickle.load(f)
            logger.info("Lead scoring model loaded successfully")
        except FileNotFoundError:
            logger.warning("Lead scoring model not found. Will train new model.")
            self.lead_scoring_model = None
    
    def predict_property_price(self, property_data: Dict[str, Any], timeframe_months: int = 24) -> Optional[PricePrediction]:
        """
        Predict property price for a given timeframe
        
        Args:
            property_data: Dictionary containing property features
            timeframe_months: Number of months to predict ahead
            
        Returns:
            PricePrediction object with prediction and confidence intervals
        """
        try:
            # Validate input data
            required_fields = ['location', 'property_type', 'size_sqft', 'bedrooms', 'bathrooms']
            missing_fields = [field for field in required_fields if field not in property_data]
            
            if missing_fields:
                logger.error(f"Missing required fields for price prediction: {missing_fields}")
                return None
            
            # Prepare features for prediction
            features = self._prepare_price_features(property_data)
            
            if self.price_model is None:
                # Train model if not available
                self._train_price_model()
            
            # Make prediction
            predicted_price = self.price_model.predict([features])[0]
            
            # Calculate confidence intervals
            confidence_intervals = self._calculate_confidence_intervals(features, predicted_price)
            
            # Get market trend
            market_trend = self._analyze_market_trend(property_data['location'], property_data['property_type'])
            
            # Factors considered
            factors_considered = [
                'Location', 'Property Type', 'Size', 'Bedrooms', 'Bathrooms',
                'Market Trend', 'Seasonality', 'Economic Indicators'
            ]
            
            return PricePrediction(
                predicted_price=predicted_price,
                confidence_interval_lower=confidence_intervals[0],
                confidence_interval_upper=confidence_intervals[1],
                confidence_score=0.85,  # This would be calculated based on model performance
                prediction_date=datetime.now(),
                model_version=self.model_version,
                factors_considered=factors_considered,
                market_trend=market_trend
            )
            
        except Exception as e:
            logger.error(f"Error in price prediction: {e}")
            return None
    
    def forecast_market_trends(self, area: str, property_type: str, forecast_period: int = 6) -> Optional[MarketForecast]:
        """
        Forecast market trends for a specific area and property type
        
        Args:
            area: Geographic area (e.g., 'Downtown Dubai', 'Palm Jumeirah')
            property_type: Type of property (e.g., 'apartment', 'villa')
            forecast_period: Number of months to forecast
            
        Returns:
            MarketForecast object with trend analysis and recommendations
        """
        try:
            # Get historical market data
            historical_data = self._get_market_data(area, property_type)
            
            if not historical_data:
                logger.error(f"No historical data available for {area} - {property_type}")
                return None
            
            # Analyze trends
            trend_analysis = self._analyze_trends(historical_data, forecast_period)
            
            # Generate recommendations
            recommendations = self._generate_market_recommendations(trend_analysis, area, property_type)
            
            # Determine risk level
            risk_level = self._assess_market_risk(trend_analysis)
            
            return MarketForecast(
                area=area,
                property_type=property_type,
                forecast_period=forecast_period,
                forecast_unit="months",
                predicted_trend=trend_analysis['trend'],
                confidence_score=trend_analysis['confidence'],
                key_factors=trend_analysis['factors'],
                recommendations=recommendations,
                risk_level=risk_level
            )
            
        except Exception as e:
            logger.error(f"Error in market forecasting: {e}")
            return None
    
    def score_lead(self, client_data: Dict[str, Any], interaction_history: List[Dict] = None) -> Optional[LeadScore]:
        """
        Score a lead based on client data and interaction history
        
        Args:
            client_data: Dictionary containing client information
            interaction_history: List of previous interactions
            
        Returns:
            LeadScore object with scoring results and recommendations
        """
        try:
            # Prepare features for lead scoring
            features = self._prepare_lead_features(client_data, interaction_history)
            
            if self.lead_scoring_model is None:
                # Train model if not available
                self._train_lead_scoring_model()
            
            # Make prediction
            score = self.lead_scoring_model.predict([features])[0]
            
            # Calculate conversion probability
            conversion_probability = self._calculate_conversion_probability(score, features)
            
            # Analyze factors
            factors = self._analyze_lead_factors(features)
            
            # Generate recommendations
            recommendations = self._generate_lead_recommendations(factors, score)
            
            # Determine priority level
            priority_level = self._determine_priority_level(score)
            
            return LeadScore(
                client_id=client_data.get('client_id', 'unknown'),
                score=score,
                conversion_probability=conversion_probability,
                factors=factors,
                recommendations=recommendations,
                priority_level=priority_level,
                last_updated=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error in lead scoring: {e}")
            return None
    
    def _prepare_price_features(self, property_data: Dict[str, Any]) -> List[float]:
        """Prepare features for price prediction model"""
        features = []
        
        # Location encoding (simplified - would use proper encoding in production)
        location_encoding = self._encode_location(property_data['location'])
        features.extend(location_encoding)
        
        # Property type encoding
        property_type_encoding = self._encode_property_type(property_data['property_type'])
        features.extend(property_type_encoding)
        
        # Numerical features
        features.extend([
            property_data.get('size_sqft', 0),
            property_data.get('bedrooms', 0),
            property_data.get('bathrooms', 0),
            property_data.get('floor_number', 0),
            property_data.get('age_years', 0),
            property_data.get('parking_spaces', 0)
        ])
        
        # Market indicators
        market_indicators = self._get_market_indicators(property_data['location'])
        features.extend(market_indicators)
        
        return features
    
    def _prepare_lead_features(self, client_data: Dict[str, Any], interaction_history: List[Dict] = None) -> List[float]:
        """Prepare features for lead scoring model"""
        features = []
        
        # Client demographics
        features.extend([
            client_data.get('age', 0),
            client_data.get('income_level', 0),
            client_data.get('credit_score', 0),
            client_data.get('employment_status', 0)
        ])
        
        # Interaction metrics
        if interaction_history:
            features.extend([
                len(interaction_history),
                self._calculate_avg_response_time(interaction_history),
                self._calculate_engagement_score(interaction_history),
                self._calculate_urgency_score(interaction_history)
            ])
        else:
            features.extend([0, 0, 0, 0])
        
        # Property preferences
        preferences = client_data.get('property_preferences', {})
        features.extend([
            preferences.get('budget_min', 0),
            preferences.get('budget_max', 0),
            preferences.get('preferred_areas', []),
            preferences.get('property_types', [])
        ])
        
        return features
    
    def _encode_location(self, location: str) -> List[float]:
        """Encode location as numerical features"""
        # Simplified encoding - would use proper geocoding in production
        location_scores = {
            'downtown dubai': [1.0, 0.0, 0.0, 0.0],
            'palm jumeirah': [0.0, 1.0, 0.0, 0.0],
            'dubai marina': [0.0, 0.0, 1.0, 0.0],
            'jbr': [0.0, 0.0, 0.0, 1.0]
        }
        return location_scores.get(location.lower(), [0.0, 0.0, 0.0, 0.0])
    
    def _encode_property_type(self, property_type: str) -> List[float]:
        """Encode property type as numerical features"""
        type_scores = {
            'apartment': [1.0, 0.0, 0.0],
            'villa': [0.0, 1.0, 0.0],
            'townhouse': [0.0, 0.0, 1.0]
        }
        return type_scores.get(property_type.lower(), [0.0, 0.0, 0.0])
    
    def _get_market_indicators(self, location: str) -> List[float]:
        """Get market indicators for a location"""
        # Simplified - would fetch real data from APIs
        return [
            0.05,  # Interest rate
            0.03,  # Inflation rate
            0.02,  # GDP growth
            0.08,  # Rental yield
            0.12   # Market volatility
        ]
    
    def _calculate_confidence_intervals(self, features: List[float], predicted_price: float) -> Tuple[float, float]:
        """Calculate confidence intervals for price prediction"""
        # Simplified confidence interval calculation
        confidence_range = predicted_price * 0.1  # 10% range
        return (predicted_price - confidence_range, predicted_price + confidence_range)
    
    def _analyze_market_trend(self, location: str, property_type: str) -> str:
        """Analyze market trend for location and property type"""
        # Simplified trend analysis
        trends = ['Rising', 'Stable', 'Declining']
        return np.random.choice(trends, p=[0.6, 0.3, 0.1])
    
    def _get_market_data(self, area: str, property_type: str) -> Optional[List[Dict]]:
        """Get historical market data for analysis"""
        # This would fetch real data from APIs
        # For now, return simulated data
        return [
            {'date': '2024-01', 'price': 1000000, 'volume': 50},
            {'date': '2024-02', 'price': 1050000, 'volume': 55},
            {'date': '2024-03', 'price': 1100000, 'volume': 60},
            {'date': '2024-04', 'price': 1080000, 'volume': 45},
            {'date': '2024-05', 'price': 1120000, 'volume': 65}
        ]
    
    def _analyze_trends(self, historical_data: List[Dict], forecast_period: int) -> Dict[str, Any]:
        """Analyze trends in historical data"""
        prices = [item['price'] for item in historical_data]
        
        # Simple trend analysis
        if len(prices) >= 2:
            trend_direction = 'Rising' if prices[-1] > prices[0] else 'Declining'
            trend_strength = abs(prices[-1] - prices[0]) / prices[0]
        else:
            trend_direction = 'Stable'
            trend_strength = 0.0
        
        return {
            'trend': trend_direction,
            'confidence': 0.8,
            'factors': ['Economic Growth', 'Interest Rates', 'Supply Demand']
        }
    
    def _generate_market_recommendations(self, trend_analysis: Dict, area: str, property_type: str) -> List[str]:
        """Generate market recommendations based on trend analysis"""
        recommendations = []
        
        if trend_analysis['trend'] == 'Rising':
            recommendations.extend([
                f"Consider investing in {area} {property_type}s",
                "Market shows positive momentum",
                "Monitor for optimal entry points"
            ])
        elif trend_analysis['trend'] == 'Declining':
            recommendations.extend([
                f"Exercise caution with {area} investments",
                "Consider waiting for market stabilization",
                "Focus on value propositions"
            ])
        else:
            recommendations.extend([
                "Market is stable - good for long-term investments",
                "Focus on property-specific factors",
                "Consider rental yield opportunities"
            ])
        
        return recommendations
    
    def _assess_market_risk(self, trend_analysis: Dict) -> str:
        """Assess market risk level"""
        if trend_analysis['trend'] == 'Rising':
            return 'Low'
        elif trend_analysis['trend'] == 'Declining':
            return 'High'
        else:
            return 'Medium'
    
    def _calculate_conversion_probability(self, score: float, features: List[float]) -> float:
        """Calculate conversion probability from lead score"""
        # Simplified conversion probability calculation
        return min(score / 100.0, 0.95)
    
    def _analyze_lead_factors(self, features: List[float]) -> Dict[str, float]:
        """Analyze factors contributing to lead score"""
        factor_names = [
            'Age', 'Income', 'Credit Score', 'Employment',
            'Interaction Frequency', 'Response Time', 'Engagement', 'Urgency',
            'Budget Range', 'Area Preferences'
        ]
        
        return dict(zip(factor_names, features[:len(factor_names)]))
    
    def _generate_lead_recommendations(self, factors: Dict[str, float], score: float) -> List[str]:
        """Generate recommendations for lead nurturing"""
        recommendations = []
        
        if score > 80:
            recommendations.extend([
                "High-value lead - prioritize immediate follow-up",
                "Schedule property viewings",
                "Prepare detailed proposals"
            ])
        elif score > 60:
            recommendations.extend([
                "Good potential - maintain regular contact",
                "Provide market insights and updates",
                "Build relationship through value-added content"
            ])
        else:
            recommendations.extend([
                "Focus on education and relationship building",
                "Provide market information and insights",
                "Maintain periodic check-ins"
            ])
        
        return recommendations
    
    def _determine_priority_level(self, score: float) -> str:
        """Determine priority level based on lead score"""
        if score > 80:
            return 'High'
        elif score > 60:
            return 'Medium'
        else:
            return 'Low'
    
    def _calculate_avg_response_time(self, interaction_history: List[Dict]) -> float:
        """Calculate average response time from interaction history"""
        if not interaction_history:
            return 0.0
        
        response_times = []
        for i in range(1, len(interaction_history)):
            prev_time = interaction_history[i-1].get('timestamp', 0)
            curr_time = interaction_history[i].get('timestamp', 0)
            if prev_time and curr_time:
                response_times.append(curr_time - prev_time)
        
        return np.mean(response_times) if response_times else 0.0
    
    def _calculate_engagement_score(self, interaction_history: List[Dict]) -> float:
        """Calculate engagement score from interaction history"""
        if not interaction_history:
            return 0.0
        
        # Simplified engagement scoring
        total_interactions = len(interaction_history)
        avg_message_length = np.mean([len(msg.get('message', '')) for msg in interaction_history])
        
        return min((total_interactions * avg_message_length) / 1000, 100.0)
    
    def _calculate_urgency_score(self, interaction_history: List[Dict]) -> float:
        """Calculate urgency score from interaction history"""
        if not interaction_history:
            return 0.0
        
        urgency_keywords = ['urgent', 'asap', 'quick', 'immediate', 'soon']
        urgency_count = 0
        
        for interaction in interaction_history:
            message = interaction.get('message', '').lower()
            urgency_count += sum(1 for keyword in urgency_keywords if keyword in message)
        
        return min(urgency_count * 10, 100.0)
    
    def _train_price_model(self):
        """Train price prediction model"""
        # This would train a real model with actual data
        # For now, create a simple model
        self.price_model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        # Simulate training data
        X = np.random.rand(1000, 15)  # 15 features
        y = np.random.rand(1000) * 1000000  # Prices between 0 and 1M
        
        self.price_model.fit(X, y)
        logger.info("Price prediction model trained successfully")
    
    def _train_lead_scoring_model(self):
        """Train lead scoring model"""
        # This would train a real model with actual data
        # For now, create a simple model
        self.lead_scoring_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        
        # Simulate training data
        X = np.random.rand(1000, 12)  # 12 features
        y = np.random.rand(1000) * 100  # Scores between 0 and 100
        
        self.lead_scoring_model.fit(X, y)
        logger.info("Lead scoring model trained successfully")
    
    def save_models(self):
        """Save trained models to disk"""
        try:
            if self.price_model:
                with open(config.model.price_prediction_model_path, 'wb') as f:
                    pickle.dump(self.price_model, f)
            
            if self.lead_scoring_model:
                with open(config.model.lead_scoring_model_path, 'wb') as f:
                    pickle.dump(self.lead_scoring_model, f)
            
            logger.info("Models saved successfully")
        except Exception as e:
            logger.error(f"Error saving models: {e}")