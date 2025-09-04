#!/usr/bin/env python3
"""
Simple Test for Reporting Service - Test basic functionality
"""

import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_reporting_service_basic():
    """Test basic reporting service functionality"""
    logger.info("Testing Reporting Service Basic Functionality...")
    
    try:
        # Add backend to Python path
        sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))
        
        # Try to import the service
        from ml.services.reporting_service import AutomatedReportingService
        
        logger.info("✅ Reporting service class imported successfully")
        
        # Test instantiation
        service = AutomatedReportingService()
        logger.info("✅ Reporting service instantiated successfully")
        
        # Test report templates
        templates = service.report_templates
        logger.info(f"✅ Report templates loaded: {len(templates)} types")
        logger.info(f"✅ Available templates: {list(templates.keys())}")
        
        # Test basic methods
        market_sentiment = service._generate_market_sentiment()
        activity_level = service._generate_activity_level()
        price_movement = service._generate_price_movement()
        
        logger.info(f"✅ Market sentiment: {market_sentiment}")
        logger.info(f"✅ Activity level: {activity_level}")
        logger.info(f"✅ Price movement: {price_movement}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Reporting service test failed: {e}")
        return False

def test_notification_service():
    """Test notification service"""
    logger.info("Testing Notification Service...")
    
    try:
        sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))
        
        from ml.services.notification_service import SmartNotificationService
        
        service = SmartNotificationService()
        rules = service.notification_rules
        
        logger.info(f"✅ Notification rules loaded: {len(rules)} types")
        logger.info(f"✅ Available rules: {list(rules.keys())}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Notification service test failed: {e}")
        return False

def test_analytics_service():
    """Test analytics service"""
    logger.info("Testing Analytics Service...")
    
    try:
        sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))
        
        from ml.services.analytics_service import PerformanceAnalyticsService
        
        service = PerformanceAnalyticsService()
        
        # Test basic attributes
        assert hasattr(service, 'metrics_data')
        assert hasattr(service, 'goals_data')
        assert hasattr(service, 'performance_history')
        assert hasattr(service, 'analytics_cache')
        
        logger.info("✅ Analytics service attributes verified")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Analytics service test failed: {e}")
        return False

def main():
    """Main test function"""
    logger.info("🚀 Starting Basic Service Tests")
    logger.info("=" * 50)
    
    tests = [
        ("Reporting Service", test_reporting_service_basic),
        ("Notification Service", test_notification_service),
        ("Analytics Service", test_analytics_service)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n🔍 Running {test_name}...")
        if test_func():
            logger.info(f"✅ {test_name} PASSED")
            passed += 1
        else:
            logger.info(f"❌ {test_name} FAILED")
    
    logger.info(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All basic service tests passed!")
    else:
        logger.info("⚠️ Some tests failed. Check the implementation.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
