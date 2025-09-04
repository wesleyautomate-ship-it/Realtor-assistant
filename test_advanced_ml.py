#!/usr/bin/env python3
"""
Test script for Advanced ML Service
Tests model initialization, training, and predictions
"""

import asyncio
import logging
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_advanced_ml_service():
    """Test the advanced ML service functionality"""
    try:
        logger.info("🚀 Testing Advanced ML Service...")
        
        # Import the service using importlib to avoid path issues
        import importlib.util
        
        # Load the advanced ML service
        spec = importlib.util.spec_from_file_location(
            "advanced_ml_service", 
            "backend/ml/services/advanced_ml_service.py"
        )
        advanced_ml_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(advanced_ml_module)
        
        # Get the service instance
        service = advanced_ml_module.advanced_ml_service
        
        logger.info("✅ Advanced ML Service imported successfully")
        
        # Test 1: Initialize models
        logger.info("\n📋 Test 1: Model Initialization")
        success = await service.initialize_models()
        if success:
            logger.info(f"✅ Models initialized: {len(service.current_models)} models loaded")
            for model_name in service.current_models.keys():
                logger.info(f"   - {model_name}")
        else:
            logger.error("❌ Model initialization failed")
            return False
        
        # Test 2: Generate training data
        logger.info("\n📊 Test 2: Training Data Generation")
        training_data = await service.generate_synthetic_training_data(1000)
        if not training_data.empty:
            logger.info(f"✅ Generated {len(training_data)} training samples")
            logger.info(f"   Features: {list(training_data.columns)}")
            logger.info(f"   Sample data: {training_data.head(3).to_dict('records')}")
        else:
            logger.error("❌ Failed to generate training data")
            return False
        
        # Test 3: Train a model
        logger.info("\n🏋️ Test 3: Model Training")
        model_name = "random_forest"
        if model_name in service.current_models:
            training_result = await service.train_model(model_name, training_data)
            if training_result.get('status') == 'success':
                logger.info(f"✅ {model_name} training completed successfully")
                logger.info(f"   R² Score: {training_result['metrics']['r2']:.4f}")
                logger.info(f"   RMSE: {training_result['metrics']['rmse']:.2f}")
                logger.info(f"   Training samples: {training_result['training_samples']}")
            else:
                logger.error(f"❌ {model_name} training failed: {training_result.get('error')}")
                return False
        else:
            logger.error(f"❌ Model {model_name} not found")
            return False
        
        # Test 4: Make predictions
        logger.info("\n🔮 Test 4: Property Price Predictions")
        
        # Test property features
        test_properties = [
            {
                'property_size': 200,
                'bedrooms': 3,
                'bathrooms': 2,
                'floor_number': 10,
                'age': 2,
                'distance_to_metro': 0.5,
                'distance_to_mall': 1.0,
                'distance_to_school': 0.8,
                'parking_spaces': 2,
                'balcony': True,
                'garden': False,
                'pool': True,
                'gym': True,
                'security': True,
                'maintenance_fee': 800,
                'service_charges': 300,
                'market_demand_score': 0.8,
                'economic_indicator': 1.1,
                'seasonality_factor': 1.05
            },
            {
                'property_size': 120,
                'bedrooms': 2,
                'bathrooms': 1,
                'floor_number': 5,
                'age': 8,
                'distance_to_metro': 2.0,
                'distance_to_mall': 3.0,
                'distance_to_school': 1.5,
                'parking_spaces': 1,
                'balcony': True,
                'garden': False,
                'pool': False,
                'gym': False,
                'security': True,
                'maintenance_fee': 400,
                'service_charges': 150,
                'market_demand_score': 0.6,
                'economic_indicator': 0.95,
                'seasonality_factor': 0.98
            }
        ]
        
        for i, property_features in enumerate(test_properties, 1):
            logger.info(f"\n   Property {i}:")
            logger.info(f"   - Size: {property_features['property_size']} sqm")
            logger.info(f"   - Bedrooms: {property_features['bedrooms']}")
            logger.info(f"   - Bathrooms: {property_features['bathrooms']}")
            
            # Test ensemble prediction
            prediction = await service.predict_property_price(property_features, 'ensemble')
            if 'error' not in prediction:
                logger.info(f"   ✅ Ensemble Prediction: AED {prediction['predicted_price_per_sqm']:.2f}/sqm")
                logger.info(f"      Confidence: {prediction['confidence_score']:.2f}")
                logger.info(f"      Model: {prediction['model_used']}")
                if prediction.get('explanation'):
                    logger.info(f"      Explanation: {prediction['explanation']}")
            else:
                logger.error(f"   ❌ Prediction failed: {prediction['error']}")
                return False
            
            # Test individual model prediction
            if model_name in service.current_models:
                individual_prediction = await service.predict_property_price(property_features, model_name)
                if 'error' not in individual_prediction:
                    logger.info(f"   ✅ {model_name} Prediction: AED {individual_prediction['predicted_price_per_sqm']:.2f}/sqm")
                    logger.info(f"      Confidence: {individual_prediction['confidence_score']:.2f}")
                else:
                    logger.error(f"   ❌ Individual prediction failed: {individual_prediction['error']}")
        
        # Test 5: Model performance
        logger.info("\n📈 Test 5: Model Performance")
        performance = await service.get_model_performance()
        if 'error' not in performance:
            logger.info(f"✅ Performance data retrieved:")
            logger.info(f"   Total models: {performance.get('total_models', 0)}")
            logger.info(f"   Active models: {performance.get('active_models', 0)}")
            
            for model_name, model_perf in performance.get('models', {}).items():
                status = model_perf.get('status', 'unknown')
                logger.info(f"   - {model_name}: {status}")
        else:
            logger.error(f"❌ Failed to get performance data: {performance['error']}")
        
        # Test 6: Model insights
        logger.info("\n💡 Test 6: Model Insights")
        insights = await service.get_model_insights()
        if 'error' not in insights:
            logger.info(f"✅ Insights retrieved:")
            logger.info(f"   Total models: {insights.get('total_models', 0)}")
            
            for model_name, status in insights.get('model_status', {}).items():
                logger.info(f"   - {model_name}: {status}")
            
            if insights.get('recommendations'):
                logger.info("   Recommendations:")
                for rec in insights['recommendations']:
                    logger.info(f"     • {rec}")
        else:
            logger.error(f"❌ Failed to get insights: {insights['error']}")
        
        logger.info("\n🎉 All Advanced ML Service tests completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error testing Advanced ML Service: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    logger.info("🧪 Starting Advanced ML Service Tests")
    logger.info("=" * 50)
    
    success = await test_advanced_ml_service()
    
    logger.info("=" * 50)
    if success:
        logger.info("✅ All tests passed!")
        sys.exit(0)
    else:
        logger.error("❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
