"""
Example Usage of Advanced AI Features

This file demonstrates how to integrate the advanced features into the existing
Real Estate RAG Chat System. It shows various use cases and integration patterns.
"""

import logging
from datetime import datetime
from typing import Dict, Any

from .integration_manager import AdvancedFeaturesIntegrationManager
from .predictive_analytics import PredictiveAnalyticsEngine
from .financial_tools import FinancialCalculatorSuite
from .content_generation import ContentGenerationEngine
from .sentiment_analysis import SentimentAnalyzer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def example_basic_integration():
    """Example of basic integration with the chat system"""
    print("=== Basic Integration Example ===")
    
    # Initialize the integration manager
    manager = AdvancedFeaturesIntegrationManager()
    
    # Example user messages
    test_messages = [
        "What will this Downtown Dubai apartment be worth in 2 years?",
        "Calculate ROI for this 2M AED property with 8K monthly rent",
        "Calculate commission for 3M AED property sale",
        "Convert 100,000 AED to USD",
        "Tell me about the Dubai Marina neighborhood",
        "Create a property brochure for this villa"
    ]
    
    for message in test_messages:
        print(f"\nUser: {message}")
        
        # Process the message
        result = manager.process_message(
            user_message=message,
            conversation_context={},
            user_data={}
        )
        
        # Display results
        if result.intent_detected:
            print(f"✅ Intent Detected: {result.detected_intent.intent_type}")
            print(f"📊 Confidence: {result.detected_intent.confidence:.2f}")
            print(f"💬 Response: {result.adjusted_response}")
            if result.suggestions:
                print(f"💡 Suggestions: {', '.join(result.suggestions)}")
        else:
            print("❌ No intent detected - using standard RAG response")
        
        print("-" * 50)

def example_sentiment_analysis():
    """Example of sentiment analysis integration"""
    print("\n=== Sentiment Analysis Example ===")
    
    sentiment_analyzer = SentimentAnalyzer()
    
    # Test different sentiment scenarios
    test_scenarios = [
        {
            "message": "I'm really excited about this property! It's perfect for my family.",
            "expected_sentiment": "positive"
        },
        {
            "message": "I'm frustrated with the high prices in this area.",
            "expected_sentiment": "negative"
        },
        {
            "message": "I'm not sure about this investment. Can you tell me more?",
            "expected_sentiment": "hesitant"
        },
        {
            "message": "I need this information urgently for my meeting tomorrow!",
            "expected_sentiment": "urgent"
        }
    ]
    
    for scenario in test_scenarios:
        message = scenario["message"]
        expected = scenario["expected_sentiment"]
        
        print(f"\nUser: {message}")
        
        # Analyze sentiment
        result = sentiment_analyzer.analyze_sentiment(message)
        
        if result:
            print(f"🎭 Detected Sentiment: {result.sentiment_label}")
            print(f"😊 Dominant Emotion: {result.dominant_emotion}")
            print(f"📈 Confidence: {result.confidence:.2f}")
            print(f"💬 Response Adjustment: {result.response_adjustment}")
            
            # Test response adjustment
            original_response = "Here is the information you requested."
            adjusted_response = sentiment_analyzer.adjust_response_tone(original_response, result)
            print(f"🔄 Adjusted Response: {adjusted_response}")
        else:
            print("❌ No sentiment detected")
        
        print("-" * 50)

def example_financial_calculations():
    """Example of financial tools usage"""
    print("\n=== Financial Tools Example ===")
    
    financial_tools = FinancialCalculatorSuite()
    
    # Example 1: ROI Calculation
    print("\n1. ROI Calculation:")
    roi_data = {
        'property_value': 2000000,
        'investment_amount': 2000000,
        'monthly_rent': 8000,
        'annual_expenses_rate': 0.15,
        'appreciation_rate': 0.05
    }
    
    roi_result = financial_tools.calculate_roi(roi_data)
    if roi_result:
        print(f"💰 Annual ROI: {roi_result.annual_roi:.1f}%")
        print(f"📈 5-Year ROI: {roi_result.five_year_roi:.1f}%")
        print(f"🏠 Monthly Rent: AED {roi_result.monthly_rental_income:,.0f}")
        print(f"📊 Rental Yield: {roi_result.rental_yield:.1f}%")
    
    # Example 2: Commission Calculation
    print("\n2. Commission Calculation:")
    commission_result = financial_tools.calculate_commission(
        property_value=3000000,
        commission_rate=0.025,
        agency_split=0.5
    )
    
    if commission_result:
        print(f"💵 Property Value: AED {commission_result.property_value:,.0f}")
        print(f"📋 Commission Rate: {commission_result.commission_rate*100:.1f}%")
        print(f"💰 Gross Commission: AED {commission_result.gross_commission:,.0f}")
        print(f"🏢 Net Commission: AED {commission_result.net_commission:,.0f}")
    
    # Example 3: Currency Conversion
    print("\n3. Currency Conversion:")
    conversion_result = financial_tools.convert_currency(100000, 'AED', 'USD')
    
    if conversion_result:
        print(f"💱 {conversion_result.amount:,.0f} {conversion_result.from_currency} = {conversion_result.converted_amount:,.2f} {conversion_result.to_currency}")
        print(f"📊 Exchange Rate: 1 {conversion_result.from_currency} = {conversion_result.exchange_rate:.4f} {conversion_result.to_currency}")
    
    print("-" * 50)

def example_content_generation():
    """Example of content generation"""
    print("\n=== Content Generation Example ===")
    
    content_engine = ContentGenerationEngine()
    
    # Sample property data
    property_data = {
        'property_id': 'PROP001',
        'location': 'Downtown Dubai',
        'property_type': 'apartment',
        'size_sqft': 1200,
        'bedrooms': 2,
        'bathrooms': 2,
        'price': 1500000,
        'monthly_rent': 6000,
        'amenities': ['gym', 'pool', 'parking', 'security'],
        'agent_name': 'Sarah Johnson',
        'agent_phone': '+971 50 123 4567',
        'agent_email': 'sarah@realestate.com'
    }
    
    # Generate property brochure
    print("\n1. Property Brochure:")
    brochure = content_engine.generate_property_brochure(property_data)
    if brochure:
        print(f"📋 Title: {brochure.title}")
        print(f"📝 Description: {brochure.description[:100]}...")
        print(f"✨ Key Features: {', '.join(brochure.key_features[:3])}")
        print(f"🏢 Amenities: {', '.join(brochure.amenities[:3])}")
    
    # Generate listing description
    print("\n2. Listing Description:")
    listing = content_engine.generate_listing_description(property_data)
    if listing:
        print(f"📋 Title: {listing.title}")
        print(f"📊 Word Count: {listing.word_count}")
        print(f"🎯 Target Audience: {listing.target_audience}")
        print(f"🔍 SEO Keywords: {', '.join(listing.seo_keywords[:3])}")
    
    print("-" * 50)

def example_predictive_analytics():
    """Example of predictive analytics"""
    print("\n=== Predictive Analytics Example ===")
    
    predictive_engine = PredictiveAnalyticsEngine()
    
    # Example 1: Price Prediction
    print("\n1. Price Prediction:")
    property_data = {
        'location': 'downtown dubai',
        'property_type': 'apartment',
        'size_sqft': 1200,
        'bedrooms': 2,
        'bathrooms': 2,
        'floor_number': 15,
        'age_years': 5,
        'parking_spaces': 1
    }
    
    prediction = predictive_engine.predict_property_price(property_data)
    if prediction:
        print(f"🏠 Predicted Price: AED {prediction.predicted_price:,.0f}")
        print(f"📊 Confidence: {prediction.confidence_score*100:.1f}%")
        print(f"📈 Market Trend: {prediction.market_trend}")
        print(f"🔍 Factors: {', '.join(prediction.factors_considered[:3])}")
    
    # Example 2: Market Forecast
    print("\n2. Market Forecast:")
    forecast = predictive_engine.forecast_market_trends('Downtown Dubai', 'apartment', 6)
    if forecast:
        print(f"📊 Area: {forecast.area}")
        print(f"🏠 Property Type: {forecast.property_type}")
        print(f"📈 Predicted Trend: {forecast.predicted_trend}")
        print(f"⚠️ Risk Level: {forecast.risk_level}")
        print(f"💡 Recommendations: {', '.join(forecast.recommendations[:2])}")
    
    print("-" * 50)

def example_integration_with_chat_system():
    """Example of how to integrate with the existing chat system"""
    print("\n=== Chat System Integration Example ===")
    
    # This would be integrated into your existing chat endpoint
    def enhanced_chat_endpoint(user_message: str, conversation_history: list, user_data: dict):
        """
        Enhanced chat endpoint that integrates advanced features
        """
        # Initialize the integration manager
        manager = AdvancedFeaturesIntegrationManager()
        
        # Process message with advanced features
        result = manager.process_message(
            user_message=user_message,
            conversation_context={'history': conversation_history},
            user_data=user_data
        )
        
        # If advanced feature was triggered
        if result.intent_detected and result.feature_response:
            return {
                'response': result.adjusted_response,
                'feature_used': result.detected_intent.intent_type,
                'confidence': result.detected_intent.confidence,
                'suggestions': result.suggestions,
                'sentiment': result.sentiment_analysis.sentiment_label if result.sentiment_analysis else None
            }
        
        # Fallback to standard RAG response
        return {
            'response': "I understand your request. Let me help you with that.",
            'feature_used': None,
            'confidence': 0.0,
            'suggestions': [],
            'sentiment': None
        }
    
    # Test the enhanced endpoint
    test_cases = [
        {
            'message': "What will this property be worth in 2 years?",
            'history': [],
            'user_data': {'role': 'client'}
        },
        {
            'message': "Calculate ROI for 2M AED property",
            'history': [],
            'user_data': {'role': 'agent'}
        }
    ]
    
    for case in test_cases:
        print(f"\nUser: {case['message']}")
        result = enhanced_chat_endpoint(case['message'], case['history'], case['user_data'])
        
        print(f"🤖 Response: {result['response']}")
        if result['feature_used']:
            print(f"⚡ Feature Used: {result['feature_used']}")
            print(f"📊 Confidence: {result['confidence']:.2f}")
        if result['suggestions']:
            print(f"💡 Suggestions: {', '.join(result['suggestions'])}")
        if result['sentiment']:
            print(f"🎭 Sentiment: {result['sentiment']}")
        
        print("-" * 50)

def example_feature_management():
    """Example of feature management and configuration"""
    print("\n=== Feature Management Example ===")
    
    manager = AdvancedFeaturesIntegrationManager()
    
    # Check feature status
    print("📋 Current Feature Status:")
    status = manager.get_feature_status()
    for feature, enabled in status.items():
        status_icon = "✅" if enabled else "❌"
        print(f"  {status_icon} {feature}: {'Enabled' if enabled else 'Disabled'}")
    
    # Enable/disable features
    print("\n🔧 Feature Management:")
    
    # Disable a feature
    success = manager.disable_feature('price_prediction')
    print(f"Disable price prediction: {'✅ Success' if success else '❌ Failed'}")
    
    # Enable a feature
    success = manager.enable_feature('price_prediction')
    print(f"Enable price prediction: {'✅ Success' if success else '❌ Failed'}")
    
    print("-" * 50)

def main():
    """Run all examples"""
    print("🚀 Advanced AI Features - Example Usage")
    print("=" * 60)
    
    try:
        # Run all examples
        example_basic_integration()
        example_sentiment_analysis()
        example_financial_calculations()
        example_content_generation()
        example_predictive_analytics()
        example_integration_with_chat_system()
        example_feature_management()
        
        print("\n✅ All examples completed successfully!")
        print("\n📝 Next Steps:")
        print("1. Install required dependencies: pip install -r requirements.txt")
        print("2. Set up environment variables in .env file")
        print("3. Integrate AdvancedFeaturesIntegrationManager into your chat system")
        print("4. Test with real user messages")
        print("5. Monitor performance and adjust configurations")
        
    except Exception as e:
        logger.error(f"Error running examples: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()