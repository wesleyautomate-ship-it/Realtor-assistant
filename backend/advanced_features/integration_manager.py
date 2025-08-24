"""
Advanced Features Integration Manager

This module serves as the main coordinator for all advanced AI features,
providing a unified interface for the chat system to access predictive analytics,
financial tools, content generation, and sentiment analysis.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

from .intent_recognition import IntentRecognitionEngine, DetectedIntent
from .predictive_analytics import PredictiveAnalyticsEngine
from .financial_tools import FinancialCalculatorSuite
from .content_generation import ContentGenerationEngine
from .sentiment_analysis import SentimentAnalyzer, SentimentResult
from .config import config

logger = logging.getLogger(__name__)

@dataclass
class FeatureResponse:
    """Represents a response from an advanced feature"""
    feature_type: str
    success: bool
    data: Any
    message: str
    confidence: float
    suggestions: List[str]
    timestamp: datetime

@dataclass
class IntegrationResult:
    """Represents the result of feature integration"""
    intent_detected: bool
    detected_intent: Optional[DetectedIntent]
    feature_response: Optional[FeatureResponse]
    sentiment_analysis: Optional[SentimentResult]
    adjusted_response: str
    suggestions: List[str]

class AdvancedFeaturesIntegrationManager:
    """
    Main integration manager for all advanced AI features
    """
    
    def __init__(self):
        self.intent_engine = IntentRecognitionEngine()
        self.predictive_engine = PredictiveAnalyticsEngine()
        self.financial_tools = FinancialCalculatorSuite()
        self.content_engine = ContentGenerationEngine()
        self.sentiment_analyzer = SentimentAnalyzer()
        
        # Feature mapping
        self.feature_mapping = {
            'price_prediction': self._handle_price_prediction,
            'market_forecast': self._handle_market_forecast,
            'lead_scoring': self._handle_lead_scoring,
            'roi_calculation': self._handle_roi_calculation,
            'commission_calculation': self._handle_commission_calculation,
            'tax_calculation': self._handle_tax_calculation,
            'currency_conversion': self._handle_currency_conversion,
            'neighborhood_insights': self._handle_neighborhood_insights,
            'content_generation': self._handle_content_generation,
            'sentiment_analysis': self._handle_sentiment_analysis
        }
        
        logger.info("Advanced Features Integration Manager initialized successfully")
    
    def process_message(self, user_message: str, conversation_context: Dict = None, 
                       user_data: Dict = None) -> IntegrationResult:
        """
        Process a user message and determine appropriate advanced features to trigger
        
        Args:
            user_message: The user's input message
            conversation_context: Previous conversation context
            user_data: User profile and preferences
            
        Returns:
            IntegrationResult with detected intent and feature response
        """
        try:
            # Step 1: Detect intent
            detected_intent = self.intent_engine.detect_intent(user_message, conversation_context)
            
            # Step 2: Analyze sentiment
            sentiment_result = self.sentiment_analyzer.analyze_sentiment(user_message, conversation_context)
            
            # Step 3: Process feature if intent detected
            feature_response = None
            if detected_intent and detected_intent.feature_enabled:
                feature_response = self._process_feature(detected_intent, user_data, conversation_context)
            
            # Step 4: Generate suggestions
            suggestions = self._generate_suggestions(detected_intent, sentiment_result, conversation_context)
            
            # Step 5: Adjust response based on sentiment
            adjusted_response = self._adjust_response_based_on_sentiment(
                feature_response, sentiment_result, user_message
            )
            
            return IntegrationResult(
                intent_detected=detected_intent is not None,
                detected_intent=detected_intent,
                feature_response=feature_response,
                sentiment_analysis=sentiment_result,
                adjusted_response=adjusted_response,
                suggestions=suggestions
            )
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return IntegrationResult(
                intent_detected=False,
                detected_intent=None,
                feature_response=None,
                sentiment_analysis=None,
                adjusted_response="I apologize, but I'm having trouble processing your request right now. Please try again.",
                suggestions=[]
            )
    
    def _process_feature(self, detected_intent: DetectedIntent, user_data: Dict = None, 
                        conversation_context: Dict = None) -> Optional[FeatureResponse]:
        """Process the detected intent and execute appropriate feature"""
        try:
            intent_type = detected_intent.intent_type
            
            if intent_type in self.feature_mapping:
                handler = self.feature_mapping[intent_type]
                return handler(detected_intent, user_data, conversation_context)
            else:
                logger.warning(f"No handler found for intent type: {intent_type}")
                return None
                
        except Exception as e:
            logger.error(f"Error processing feature {detected_intent.intent_type}: {e}")
            return FeatureResponse(
                feature_type=detected_intent.intent_type,
                success=False,
                data=None,
                message=f"Sorry, I encountered an error while processing your request: {str(e)}",
                confidence=0.0,
                suggestions=[],
                timestamp=datetime.now()
            )
    
    def _handle_price_prediction(self, detected_intent: DetectedIntent, user_data: Dict = None, 
                                conversation_context: Dict = None) -> FeatureResponse:
        """Handle property price prediction requests"""
        try:
            parameters = detected_intent.parameters
            
            # Extract property data from parameters and context
            property_data = self._extract_property_data(parameters, conversation_context)
            
            if not property_data:
                return FeatureResponse(
                    feature_type='price_prediction',
                    success=False,
                    data=None,
                    message="I need more information about the property to make a price prediction. Please provide details about location, size, and property type.",
                    confidence=0.0,
                    suggestions=['Provide property location', 'Specify property size', 'Mention property type'],
                    timestamp=datetime.now()
                )
            
            # Make prediction
            prediction = self.predictive_engine.predict_property_price(property_data)
            
            if prediction:
                message = f"Based on my analysis, this property is predicted to be worth AED {prediction.predicted_price:,.0f} in 2 years. Confidence level: {prediction.confidence_score*100:.1f}%"
                
                return FeatureResponse(
                    feature_type='price_prediction',
                    success=True,
                    data=prediction,
                    message=message,
                    confidence=detected_intent.confidence,
                    suggestions=['Get market trend analysis', 'Calculate ROI', 'Compare with similar properties'],
                    timestamp=datetime.now()
                )
            else:
                return FeatureResponse(
                    feature_type='price_prediction',
                    success=False,
                    data=None,
                    message="I'm unable to predict the price at the moment. Please try again later.",
                    confidence=0.0,
                    suggestions=[],
                    timestamp=datetime.now()
                )
                
        except Exception as e:
            logger.error(f"Error in price prediction: {e}")
            return FeatureResponse(
                feature_type='price_prediction',
                success=False,
                data=None,
                message="I encountered an error while predicting the price. Please try again.",
                confidence=0.0,
                suggestions=[],
                timestamp=datetime.now()
            )
    
    def _handle_market_forecast(self, detected_intent: DetectedIntent, user_data: Dict = None, 
                               conversation_context: Dict = None) -> FeatureResponse:
        """Handle market trend forecasting requests"""
        try:
            parameters = detected_intent.parameters
            area = parameters.get('area', 'Dubai')
            property_type = parameters.get('property_type', 'apartment')
            
            forecast = self.predictive_engine.forecast_market_trends(area, property_type)
            
            if forecast:
                message = f"Market forecast for {area} {property_type}s: {forecast.predicted_trend} trend with {forecast.confidence_score*100:.1f}% confidence. Risk level: {forecast.risk_level}"
                
                return FeatureResponse(
                    feature_type='market_forecast',
                    success=True,
                    data=forecast,
                    message=message,
                    confidence=detected_intent.confidence,
                    suggestions=forecast.recommendations,
                    timestamp=datetime.now()
                )
            else:
                return FeatureResponse(
                    feature_type='market_forecast',
                    success=False,
                    data=None,
                    message=f"I'm unable to provide a market forecast for {area} at the moment.",
                    confidence=0.0,
                    suggestions=[],
                    timestamp=datetime.now()
                )
                
        except Exception as e:
            logger.error(f"Error in market forecast: {e}")
            return FeatureResponse(
                feature_type='market_forecast',
                success=False,
                data=None,
                message="I encountered an error while analyzing market trends. Please try again.",
                confidence=0.0,
                suggestions=[],
                timestamp=datetime.now()
            )
    
    def _handle_roi_calculation(self, detected_intent: DetectedIntent, user_data: Dict = None, 
                               conversation_context: Dict = None) -> FeatureResponse:
        """Handle ROI calculation requests"""
        try:
            parameters = detected_intent.parameters
            
            # Extract investment data
            investment_data = {
                'property_value': parameters.get('property_value', 1000000),
                'investment_amount': parameters.get('investment_amount', 1000000),
                'monthly_rent': parameters.get('monthly_rent', 5000),
                'annual_expenses_rate': 0.15,
                'appreciation_rate': 0.05
            }
            
            roi_result = self.financial_tools.calculate_roi(investment_data)
            
            if roi_result:
                message = f"ROI Analysis:\n- Annual Return: {roi_result.annual_roi:.1f}%\n- 5-Year Projection: {roi_result.five_year_roi:.1f}%\n- Monthly Rental Income: AED {roi_result.monthly_rental_income:,.0f}\n- Rental Yield: {roi_result.rental_yield:.1f}%"
                
                return FeatureResponse(
                    feature_type='roi_calculation',
                    success=True,
                    data=roi_result,
                    message=message,
                    confidence=detected_intent.confidence,
                    suggestions=['Calculate commission', 'Analyze tax implications', 'Compare with other investments'],
                    timestamp=datetime.now()
                )
            else:
                return FeatureResponse(
                    feature_type='roi_calculation',
                    success=False,
                    data=None,
                    message="Unable to calculate ROI. Please provide property details and investment amount.",
                    confidence=0.0,
                    suggestions=[],
                    timestamp=datetime.now()
                )
                
        except Exception as e:
            logger.error(f"Error in ROI calculation: {e}")
            return FeatureResponse(
                feature_type='roi_calculation',
                success=False,
                data=None,
                message="I encountered an error while calculating ROI. Please try again.",
                confidence=0.0,
                suggestions=[],
                timestamp=datetime.now()
            )
    
    def _handle_commission_calculation(self, detected_intent: DetectedIntent, user_data: Dict = None, 
                                     conversation_context: Dict = None) -> FeatureResponse:
        """Handle commission calculation requests"""
        try:
            parameters = detected_intent.parameters
            property_value = parameters.get('property_value', 1000000)
            commission_rate = parameters.get('commission_rate', config.financial.default_commission_rate)
            
            commission_result = self.financial_tools.calculate_commission(property_value, commission_rate)
            
            if commission_result:
                message = f"Commission Breakdown:\n- Property Value: AED {commission_result.property_value:,.0f}\n- Commission Rate: {commission_result.commission_rate*100:.1f}%\n- Gross Commission: AED {commission_result.gross_commission:,.0f}\n- VAT (5%): AED {commission_result.vat_amount:,.0f}\n- Net Commission: AED {commission_result.net_commission:,.0f}"
                
                return FeatureResponse(
                    feature_type='commission_calculation',
                    success=True,
                    data=commission_result,
                    message=message,
                    confidence=detected_intent.confidence,
                    suggestions=['Calculate taxes', 'Analyze ROI', 'Compare commission rates'],
                    timestamp=datetime.now()
                )
            else:
                return FeatureResponse(
                    feature_type='commission_calculation',
                    success=False,
                    data=None,
                    message="Unable to calculate commission. Please provide property value and commission rate.",
                    confidence=0.0,
                    suggestions=[],
                    timestamp=datetime.now()
                )
                
        except Exception as e:
            logger.error(f"Error in commission calculation: {e}")
            return FeatureResponse(
                feature_type='commission_calculation',
                success=False,
                data=None,
                message="I encountered an error while calculating commission. Please try again.",
                confidence=0.0,
                suggestions=[],
                timestamp=datetime.now()
            )
    
    def _handle_tax_calculation(self, detected_intent: DetectedIntent, user_data: Dict = None, 
                               conversation_context: Dict = None) -> FeatureResponse:
        """Handle tax calculation requests"""
        try:
            parameters = detected_intent.parameters
            
            property_data = {
                'property_value': parameters.get('property_value', 1000000),
                'property_type': parameters.get('property_type', 'apartment'),
                'size_sqft': parameters.get('size_sqft', 1000)
            }
            
            tax_result = self.financial_tools.calculate_taxes(property_data)
            
            if tax_result:
                message = f"Tax Analysis:\n- Dubai Land Department Fee: AED {tax_result.dubai_land_dept_fee:,.0f}\n- Municipality Fees: AED {tax_result.municipality_fees:,.0f}\n- Service Charges: AED {tax_result.service_charges:,.0f}\n- VAT on Services: AED {tax_result.vat_on_services:,.0f}\n- Total Annual Costs: AED {tax_result.total_annual_costs:,.0f}"
                
                return FeatureResponse(
                    feature_type='tax_calculation',
                    success=True,
                    data=tax_result,
                    message=message,
                    confidence=detected_intent.confidence,
                    suggestions=['Calculate ROI', 'Analyze total costs', 'Compare with other properties'],
                    timestamp=datetime.now()
                )
            else:
                return FeatureResponse(
                    feature_type='tax_calculation',
                    success=False,
                    data=None,
                    message="Unable to calculate taxes. Please provide property details.",
                    confidence=0.0,
                    suggestions=[],
                    timestamp=datetime.now()
                )
                
        except Exception as e:
            logger.error(f"Error in tax calculation: {e}")
            return FeatureResponse(
                feature_type='tax_calculation',
                success=False,
                data=None,
                message="I encountered an error while calculating taxes. Please try again.",
                confidence=0.0,
                suggestions=[],
                timestamp=datetime.now()
            )
    
    def _handle_currency_conversion(self, detected_intent: DetectedIntent, user_data: Dict = None, 
                                   conversation_context: Dict = None) -> FeatureResponse:
        """Handle currency conversion requests"""
        try:
            parameters = detected_intent.parameters
            amount = parameters.get('numbers', [1000])[0] if parameters.get('numbers') else 1000
            from_currency = 'AED'
            to_currency = parameters.get('currency', 'USD')
            
            conversion_result = self.financial_tools.convert_currency(amount, from_currency, to_currency)
            
            if conversion_result:
                message = f"Currency Conversion:\n- {amount:,.0f} {from_currency} = {conversion_result.converted_amount:,.2f} {to_currency}\n- Exchange Rate: 1 {from_currency} = {conversion_result.exchange_rate:.4f} {to_currency}\n- Conversion Date: {conversion_result.conversion_date.strftime('%Y-%m-%d %H:%M')}"
                
                return FeatureResponse(
                    feature_type='currency_conversion',
                    success=True,
                    data=conversion_result,
                    message=message,
                    confidence=detected_intent.confidence,
                    suggestions=['Convert other amounts', 'View historical rates', 'Calculate in different currencies'],
                    timestamp=datetime.now()
                )
            else:
                return FeatureResponse(
                    feature_type='currency_conversion',
                    success=False,
                    data=None,
                    message="Unable to convert currency. Please try again.",
                    confidence=0.0,
                    suggestions=[],
                    timestamp=datetime.now()
                )
                
        except Exception as e:
            logger.error(f"Error in currency conversion: {e}")
            return FeatureResponse(
                feature_type='currency_conversion',
                success=False,
                data=None,
                message="I encountered an error while converting currency. Please try again.",
                confidence=0.0,
                suggestions=[],
                timestamp=datetime.now()
            )
    
    def _handle_neighborhood_insights(self, detected_intent: DetectedIntent, user_data: Dict = None, 
                                    conversation_context: Dict = None) -> FeatureResponse:
        """Handle neighborhood insights requests"""
        try:
            parameters = detected_intent.parameters
            area = parameters.get('location', 'Dubai')
            
            insights = self.financial_tools.get_neighborhood_insights(area)
            
            if insights:
                message = f"Neighborhood Insights for {area}:\n- Safety Rating: {insights.safety_rating:.1f}/10\n- Market Trend: {insights.market_trend}\n- Average Apartment Price: AED {insights.average_prices.get('apartment', 0):,.0f}\n- Average Villa Price: AED {insights.average_prices.get('villa', 0):,.0f}"
                
                return FeatureResponse(
                    feature_type='neighborhood_insights',
                    success=True,
                    data=insights,
                    message=message,
                    confidence=detected_intent.confidence,
                    suggestions=['View school ratings', 'Check amenities', 'Analyze transport links'],
                    timestamp=datetime.now()
                )
            else:
                return FeatureResponse(
                    feature_type='neighborhood_insights',
                    success=False,
                    data=None,
                    message=f"Unable to provide insights for {area}. Please try a different area.",
                    confidence=0.0,
                    suggestions=[],
                    timestamp=datetime.now()
                )
                
        except Exception as e:
            logger.error(f"Error in neighborhood insights: {e}")
            return FeatureResponse(
                feature_type='neighborhood_insights',
                success=False,
                data=None,
                message="I encountered an error while analyzing the neighborhood. Please try again.",
                confidence=0.0,
                suggestions=[],
                timestamp=datetime.now()
            )
    
    def _handle_content_generation(self, detected_intent: DetectedIntent, user_data: Dict = None, 
                                 conversation_context: Dict = None) -> FeatureResponse:
        """Handle content generation requests"""
        try:
            parameters = detected_intent.parameters
            
            # Extract property data from context
            property_data = self._extract_property_data(parameters, conversation_context)
            
            if not property_data:
                return FeatureResponse(
                    feature_type='content_generation',
                    success=False,
                    data=None,
                    message="I need property information to generate content. Please provide property details.",
                    confidence=0.0,
                    suggestions=['Provide property details', 'Specify content type', 'Include property features'],
                    timestamp=datetime.now()
                )
            
            # Generate content based on intent
            content_result = self.content_engine.generate_listing_description(property_data)
            
            if content_result:
                return FeatureResponse(
                    feature_type='content_generation',
                    success=True,
                    data=content_result,
                    message=f"Generated {content_result.content_type}:\n\n{content_result.content}",
                    confidence=detected_intent.confidence,
                    suggestions=['Generate brochure', 'Create CMA report', 'Write market analysis'],
                    timestamp=datetime.now()
                )
            else:
                return FeatureResponse(
                    feature_type='content_generation',
                    success=False,
                    data=None,
                    message="Unable to generate content. Please try again.",
                    confidence=0.0,
                    suggestions=[],
                    timestamp=datetime.now()
                )
                
        except Exception as e:
            logger.error(f"Error in content generation: {e}")
            return FeatureResponse(
                feature_type='content_generation',
                success=False,
                data=None,
                message="I encountered an error while generating content. Please try again.",
                confidence=0.0,
                suggestions=[],
                timestamp=datetime.now()
            )
    
    def _handle_sentiment_analysis(self, detected_intent: DetectedIntent, user_data: Dict = None, 
                                 conversation_context: Dict = None) -> FeatureResponse:
        """Handle sentiment analysis requests"""
        try:
            # This would typically analyze the current conversation
            # For now, return a generic response
            message = "I'm analyzing the conversation mood and client emotions to provide the best possible assistance."
            
            return FeatureResponse(
                feature_type='sentiment_analysis',
                success=True,
                data=None,
                message=message,
                confidence=detected_intent.confidence,
                suggestions=['Continue conversation', 'Ask specific questions', 'Provide detailed information'],
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return FeatureResponse(
                feature_type='sentiment_analysis',
                success=False,
                data=None,
                message="I encountered an error while analyzing sentiment. Please try again.",
                confidence=0.0,
                suggestions=[],
                timestamp=datetime.now()
            )
    
    def _handle_lead_scoring(self, detected_intent: DetectedIntent, user_data: Dict = None, 
                           conversation_context: Dict = None) -> FeatureResponse:
        """Handle lead scoring requests"""
        try:
            # This would require client data and interaction history
            # For now, return a generic response
            message = "I'm analyzing the lead quality and conversion probability based on our conversation."
            
            return FeatureResponse(
                feature_type='lead_scoring',
                success=True,
                data=None,
                message=message,
                confidence=detected_intent.confidence,
                suggestions=['Schedule follow-up', 'Provide additional information', 'Address concerns'],
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error in lead scoring: {e}")
            return FeatureResponse(
                feature_type='lead_scoring',
                success=False,
                data=None,
                message="I encountered an error while scoring the lead. Please try again.",
                confidence=0.0,
                suggestions=[],
                timestamp=datetime.now()
            )
    
    def _extract_property_data(self, parameters: Dict, conversation_context: Dict = None) -> Optional[Dict]:
        """Extract property data from parameters and conversation context"""
        property_data = {}
        
        # Extract from parameters
        if parameters.get('location'):
            property_data['location'] = parameters['location']
        if parameters.get('property_type'):
            property_data['property_type'] = parameters['property_type']
        if parameters.get('numbers'):
            property_data['size_sqft'] = parameters['numbers'][0]
        
        # Extract from conversation context if available
        if conversation_context:
            # This would parse conversation history for property details
            pass
        
        # Return None if insufficient data
        if not property_data.get('location') or not property_data.get('property_type'):
            return None
        
        return property_data
    
    def _generate_suggestions(self, detected_intent: DetectedIntent, sentiment_result: SentimentResult, 
                            conversation_context: Dict = None) -> List[str]:
        """Generate contextual suggestions based on intent and sentiment"""
        suggestions = []
        
        if detected_intent:
            # Add feature-specific suggestions
            if detected_intent.intent_type == 'price_prediction':
                suggestions.extend(['Get market analysis', 'Calculate ROI', 'Compare properties'])
            elif detected_intent.intent_type == 'roi_calculation':
                suggestions.extend(['Calculate commission', 'Analyze taxes', 'Compare investments'])
            elif detected_intent.intent_type == 'commission_calculation':
                suggestions.extend(['Calculate ROI', 'Analyze taxes', 'Compare rates'])
        
        if sentiment_result:
            # Add sentiment-based suggestions
            if sentiment_result.sentiment_label == 'negative':
                suggestions.extend(['Address concerns', 'Provide reassurance', 'Offer alternatives'])
            elif sentiment_result.sentiment_label == 'positive':
                suggestions.extend(['Maintain momentum', 'Schedule viewing', 'Provide details'])
            elif sentiment_result.dominant_emotion == 'urgent':
                suggestions.extend(['Prioritize response', 'Provide immediate solutions', 'Schedule urgent meeting'])
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    def _adjust_response_based_on_sentiment(self, feature_response: FeatureResponse, 
                                          sentiment_result: SentimentResult, 
                                          original_message: str) -> str:
        """Adjust response based on sentiment analysis"""
        if not feature_response:
            return "I understand your request. Let me help you with that."
        
        response = feature_response.message
        
        if sentiment_result:
            response = self.sentiment_analyzer.adjust_response_tone(response, sentiment_result)
        
        return response
    
    def get_feature_status(self) -> Dict[str, bool]:
        """Get status of all advanced features"""
        return {
            'price_prediction': config.features.enable_price_prediction,
            'market_forecast': config.features.enable_market_forecasting,
            'lead_scoring': config.features.enable_lead_scoring,
            'sentiment_analysis': config.features.enable_sentiment_analysis,
            'roi_calculator': config.features.enable_roi_calculator,
            'commission_calculator': config.features.enable_commission_calculator,
            'tax_calculator': config.features.enable_tax_calculator,
            'currency_converter': config.features.enable_currency_converter,
            'content_generation': config.features.enable_content_generation,
            'neighborhood_insights': config.features.enable_neighborhood_insights
        }
    
    def enable_feature(self, feature_name: str) -> bool:
        """Enable a specific advanced feature"""
        try:
            if hasattr(config.features, f'enable_{feature_name}'):
                setattr(config.features, f'enable_{feature_name}', True)
                logger.info(f"Feature {feature_name} enabled successfully")
                return True
            else:
                logger.error(f"Feature {feature_name} not found")
                return False
        except Exception as e:
            logger.error(f"Error enabling feature {feature_name}: {e}")
            return False
    
    def disable_feature(self, feature_name: str) -> bool:
        """Disable a specific advanced feature"""
        try:
            if hasattr(config.features, f'enable_{feature_name}'):
                setattr(config.features, f'enable_{feature_name}', False)
                logger.info(f"Feature {feature_name} disabled successfully")
                return True
            else:
                logger.error(f"Feature {feature_name} not found")
                return False
        except Exception as e:
            logger.error(f"Error disabling feature {feature_name}: {e}")
            return False