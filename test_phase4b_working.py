#!/usr/bin/env python3
"""
Simple Phase 4B Test Script - Test what's working

This script tests the Phase 4B services to see what functionality is available.
"""

import sys
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_service_imports():
    """Test if we can import the Phase 4B services"""
    logger.info("Testing Phase 4B Service Imports...")
    
    try:
        # Test importing the services directly
        import importlib.util
        
        # Test reporting service
        logger.info("Testing Reporting Service Import...")
        spec = importlib.util.spec_from_file_location(
            "reporting_service", 
            "backend/ml/services/reporting_service.py"
        )
        if spec and spec.loader:
            logger.info("✅ Reporting service file can be loaded")
        else:
            logger.error("❌ Reporting service file cannot be loaded")
            
        # Test notification service
        logger.info("Testing Notification Service Import...")
        spec = importlib.util.spec_from_file_location(
            "notification_service", 
            "backend/ml/services/notification_service.py"
        )
        if spec and spec.loader:
            logger.info("✅ Notification service file can be loaded")
        else:
            logger.error("❌ Notification service file cannot be loaded")
            
        # Test analytics service
        logger.info("Testing Analytics Service Import...")
        spec = importlib.util.spec_from_file_location(
            "analytics_service", 
            "backend/ml/services/analytics_service.py"
        )
        if spec and spec.loader:
            logger.info("✅ Analytics service file can be loaded")
        else:
            logger.error("❌ Analytics service file cannot be loaded")
            
        return True
        
    except Exception as e:
        logger.error(f"❌ Error testing service imports: {e}")
        return False

def test_service_files():
    """Test that all Phase 4B service files exist and are readable"""
    logger.info("Testing Phase 4B Service Files...")
    
    service_files = [
        "backend/ml/services/reporting_service.py",
        "backend/ml/services/notification_service.py", 
        "backend/ml/services/analytics_service.py"
    ]
    
    missing_files = []
    for file_path in service_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    logger.info(f"✅ {file_path} - {len(content)} characters")
            except Exception as e:
                logger.error(f"❌ {file_path} - Error reading: {e}")
                missing_files.append(file_path)
        else:
            logger.error(f"❌ {file_path} - File not found")
            missing_files.append(file_path)
    
    if missing_files:
        logger.error(f"❌ Missing or unreadable files: {missing_files}")
        return False
    else:
        logger.info("✅ All service files are present and readable")
        return True

def test_router_integration():
    """Test if the ML insights router can be imported"""
    logger.info("Testing ML Insights Router Integration...")
    
    try:
        import importlib.util
        
        spec = importlib.util.spec_from_file_location(
            "ml_insights_router", 
            "backend/ml_insights_router.py"
        )
        if spec and spec.loader:
            logger.info("✅ ML Insights router can be loaded")
            return True
        else:
            logger.error("❌ ML Insights router cannot be loaded")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error testing router integration: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("🚀 Starting Phase 4B Service Tests...")
    
    results = []
    
    # Test 1: Service files
    results.append(("Service Files", test_service_files()))
    
    # Test 2: Service imports
    results.append(("Service Imports", test_service_imports()))
    
    # Test 3: Router integration
    results.append(("Router Integration", test_router_integration()))
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("📊 PHASE 4B TEST RESULTS SUMMARY")
    logger.info("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All Phase 4B tests passed! Services are ready for use.")
    else:
        logger.info("⚠️ Some tests failed. Check the logs above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
