"""
Intent Recognition Engine for Advanced AI Features

This module handles natural language intent detection to trigger advanced features
through the chat interface without requiring separate UI components.
"""

import re
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import spacy
from .config import config

logger = logging.getLogger(__name__)

@dataclass
class DetectedIntent:
    """Represents a detected intent with confidence and extracted parameters"""
    intent_type: str
    confidence: float
    parameters: Dict[str, Any]
    original_text: str
    feature_enabled: bool = True

class IntentRecognitionEngine:
    """
    Advanced intent recognition engine using pattern matching and NLP
    """
    
    def __init__(self):
        self.nlp = None
        self._load_nlp_model()
        self.intent_patterns = config.intent_patterns
        
    def _load_nlp_model(self):
        """Load spaCy NLP model for advanced text processing"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy model loaded successfully")
        except OSError:
            logger.warning("spaCy model not found. Installing...")
            try:
                import subprocess
                subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
                self.nlp = spacy.load("en_core_web_sm")
                logger.info("spaCy model installed and loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load spaCy model: {e}")
                self.nlp = None
    
    def detect_intent(self, user_message: str, conversation_context: Dict = None) -> Optional[DetectedIntent]:
        """
        Detect intent from user message using pattern matching and NLP
        
        Args:
            user_message: The user's input message
            conversation_context: Previous conversation context
            
        Returns:
            DetectedIntent object if intent is found, None otherwise
        """
        if not user_message:
            return None
            
        user_message = user_message.lower().strip()
        
        # Check each intent pattern
        for intent_type, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, user_message, re.IGNORECASE)
                if match:
                    confidence = self._calculate_confidence(user_message, intent_type, match)
                    parameters = self._extract_parameters(match, user_message, intent_type)
                    
                    # Check if feature is enabled
                    feature_enabled = self._is_feature_enabled(intent_type)
                    
                    return DetectedIntent(
                        intent_type=intent_type,
                        confidence=confidence,
                        parameters=parameters,
                        original_text=user_message,
                        feature_enabled=feature_enabled
                    )
        
        return None
    
    def _calculate_confidence(self, message: str, intent_type: str, match) -> float:
        """
        Calculate confidence score for detected intent
        
        Args:
            message: Original user message
            intent_type: Type of detected intent
            match: Regex match object
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        base_confidence = 0.7
        
        # Boost confidence based on match quality
        if match.group(0) == message:
            base_confidence += 0.2
        
        # Boost confidence for longer, more specific patterns
        pattern_length = len(match.group(0))
        if pattern_length > 20:
            base_confidence += 0.1
        
        # Use NLP for additional confidence if available
        if self.nlp:
            doc = self.nlp(message)
            
            # Check for relevant entities
            relevant_entities = self._get_relevant_entities(intent_type)
            entity_boost = 0.0
            
            for ent in doc.ents:
                if ent.label_ in relevant_entities:
                    entity_boost += 0.05
            
            base_confidence += min(entity_boost, 0.2)
        
        return min(base_confidence, 1.0)
    
    def _extract_parameters(self, match, message: str, intent_type: str) -> Dict[str, Any]:
        """
        Extract parameters from the matched intent
        
        Args:
            match: Regex match object
            message: Original user message
            intent_type: Type of detected intent
            
        Returns:
            Dictionary of extracted parameters
        """
        parameters = {}
        
        # Extract time periods
        time_match = re.search(r'(\d+)\s*(year|month|week|day)', message)
        if time_match:
            parameters['time_period'] = int(time_match.group(1))
            parameters['time_unit'] = time_match.group(2)
        
        # Extract currency codes
        currency_match = re.search(r'\b([A-Z]{3})\b', message.upper())
        if currency_match:
            parameters['currency'] = currency_match.group(1)
        
        # Extract property types
        property_types = ['apartment', 'villa', 'townhouse', 'penthouse', 'studio', 'duplex']
        for prop_type in property_types:
            if prop_type in message:
                parameters['property_type'] = prop_type
                break
        
        # Extract locations/areas
        if self.nlp:
            doc = self.nlp(message)
            locations = [ent.text for ent in doc.ents if ent.label_ in ['GPE', 'LOC']]
            if locations:
                parameters['location'] = locations[0]
        
        # Extract numbers (prices, percentages, etc.)
        numbers = re.findall(r'\d+(?:\.\d+)?', message)
        if numbers:
            parameters['numbers'] = [float(num) for num in numbers]
        
        # Extract specific parameters based on intent type
        if intent_type == "price_prediction":
            self._extract_price_prediction_params(message, parameters)
        elif intent_type == "roi_calculation":
            self._extract_roi_params(message, parameters)
        elif intent_type == "commission_calculation":
            self._extract_commission_params(message, parameters)
        elif intent_type == "market_forecast":
            self._extract_market_params(message, parameters)
        
        return parameters
    
    def _extract_price_prediction_params(self, message: str, parameters: Dict):
        """Extract parameters specific to price prediction"""
        # Look for property identifiers
        property_match = re.search(r'property\s+(?:id|#)?\s*(\d+)', message)
        if property_match:
            parameters['property_id'] = int(property_match.group(1))
        
        # Look for price ranges
        price_match = re.search(r'(\d+(?:,\d+)*)\s*(?:aed|usd|eur)', message, re.IGNORECASE)
        if price_match:
            parameters['current_price'] = float(price_match.group(1).replace(',', ''))
    
    def _extract_roi_params(self, message: str, parameters: Dict):
        """Extract parameters specific to ROI calculation"""
        # Look for investment amounts
        investment_match = re.search(r'investment\s+(?:of\s+)?(\d+(?:,\d+)*)', message)
        if investment_match:
            parameters['investment_amount'] = float(investment_match.group(1).replace(',', ''))
        
        # Look for rental income
        rental_match = re.search(r'rent(?:al)?\s+(?:income\s+)?(\d+(?:,\d+)*)', message)
        if rental_match:
            parameters['rental_income'] = float(rental_match.group(1).replace(',', ''))
    
    def _extract_commission_params(self, message: str, parameters: Dict):
        """Extract parameters specific to commission calculation"""
        # Look for property values
        value_match = re.search(r'(?:property\s+)?value\s+(?:of\s+)?(\d+(?:,\d+)*)', message)
        if value_match:
            parameters['property_value'] = float(value_match.group(1).replace(',', ''))
        
        # Look for commission rates
        rate_match = re.search(r'(\d+(?:\.\d+)?)\s*%\s*commission', message)
        if rate_match:
            parameters['commission_rate'] = float(rate_match.group(1)) / 100
    
    def _extract_market_params(self, message: str, parameters: Dict):
        """Extract parameters specific to market forecasting"""
        # Look for specific areas
        area_match = re.search(r'(downtown|palm\s+jumeirah|marina|jbr|business\s+bay)', message, re.IGNORECASE)
        if area_match:
            parameters['area'] = area_match.group(1).lower()
        
        # Look for property types
        type_match = re.search(r'(apartment|villa|townhouse|penthouse)', message, re.IGNORECASE)
        if type_match:
            parameters['property_type'] = type_match.group(1).lower()
    
    def _get_relevant_entities(self, intent_type: str) -> List[str]:
        """Get relevant entity types for each intent"""
        entity_mapping = {
            "price_prediction": ["MONEY", "CARDINAL", "GPE", "LOC"],
            "market_forecast": ["GPE", "LOC", "DATE", "TIME"],
            "lead_scoring": ["PERSON", "ORG", "MONEY"],
            "roi_calculation": ["MONEY", "PERCENT", "CARDINAL"],
            "commission_calculation": ["MONEY", "PERCENT", "CARDINAL"],
            "tax_calculation": ["MONEY", "PERCENT", "CARDINAL"],
            "currency_conversion": ["MONEY", "CARDINAL"],
            "neighborhood_insights": ["GPE", "LOC", "FAC"],
            "content_generation": ["PRODUCT", "ORG", "PERSON"],
            "sentiment_analysis": ["PERSON", "ORG"]
        }
        return entity_mapping.get(intent_type, [])
    
    def _is_feature_enabled(self, intent_type: str) -> bool:
        """Check if a feature is enabled based on configuration"""
        feature_mapping = {
            "price_prediction": config.features.enable_price_prediction,
            "market_forecast": config.features.enable_market_forecasting,
            "lead_scoring": config.features.enable_lead_scoring,
            "sentiment_analysis": config.features.enable_sentiment_analysis,
            "roi_calculation": config.features.enable_roi_calculator,
            "commission_calculation": config.features.enable_commission_calculator,
            "tax_calculation": config.features.enable_tax_calculator,
            "currency_conversion": config.features.enable_currency_converter,
            "content_generation": config.features.enable_content_generation,
            "create_instagram_post": config.features.enable_instagram_post_generation,
            "draft_follow_up_email": config.features.enable_email_generation,
            "generate_whatsapp_broadcast": config.features.enable_whatsapp_broadcast,
            "neighborhood_insights": config.features.enable_neighborhood_insights
        }
        return feature_mapping.get(intent_type, False)
    
    def get_suggested_features(self, conversation_history: List[Dict]) -> List[str]:
        """
        Get suggested features based on conversation context
        
        Args:
            conversation_history: List of previous messages
            
        Returns:
            List of suggested feature types
        """
        suggestions = []
        
        # Analyze conversation for context clues
        recent_messages = conversation_history[-5:] if len(conversation_history) > 5 else conversation_history
        
        for message in recent_messages:
            text = message.get('message', '').lower()
            
            # Check for financial discussions
            if any(word in text for word in ['price', 'cost', 'value', 'money']):
                suggestions.extend(['price_prediction', 'roi_calculation'])
            
            # Check for market discussions
            if any(word in text for word in ['market', 'trend', 'forecast', 'investment']):
                suggestions.extend(['market_forecast', 'neighborhood_insights'])
            
            # Check for client discussions
            if any(word in text for word in ['client', 'lead', 'customer', 'buyer']):
                suggestions.extend(['lead_scoring', 'sentiment_analysis'])
            
            # Check for commission discussions
            if any(word in text for word in ['commission', 'earnings', 'fee', 'agent']):
                suggestions.extend(['commission_calculation', 'tax_calculation'])
        
        # Remove duplicates and return unique suggestions
        return list(set(suggestions))
    
    def validate_intent(self, detected_intent: DetectedIntent) -> Tuple[bool, str]:
        """
        Validate detected intent and return validation result
        
        Args:
            detected_intent: The detected intent to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not detected_intent.feature_enabled:
            return False, f"Feature '{detected_intent.intent_type}' is currently disabled"
        
        if detected_intent.confidence < 0.6:
            return False, f"Low confidence in intent detection ({detected_intent.confidence:.2f})"
        
        # Validate required parameters for specific intents
        required_params = self._get_required_parameters(detected_intent.intent_type)
        missing_params = []
        
        for param in required_params:
            if param not in detected_intent.parameters:
                missing_params.append(param)
        
        if missing_params:
            return False, f"Missing required parameters: {', '.join(missing_params)}"
        
        return True, ""
    
    def _get_required_parameters(self, intent_type: str) -> List[str]:
        """Get required parameters for each intent type"""
        required_params = {
            "price_prediction": ["property_type", "location"],
            "roi_calculation": ["investment_amount"],
            "commission_calculation": ["property_value"],
            "currency_conversion": ["currency"],
            "market_forecast": ["area"],
            "neighborhood_insights": ["location"]
        }
        return required_params.get(intent_type, [])