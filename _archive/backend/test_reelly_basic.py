#!/usr/bin/env python3
"""
Basic test for Reelly service initialization
Tests configuration and basic functionality without API calls
"""

import os
import sys

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_reelly_initialization():
    """Test basic Reelly service initialization"""
    print("🧪 Testing Reelly Service Initialization...")
    
    try:
        from reelly_service import ReellyService
        
        # Set environment variable for testing
        os.environ["REELLY_API_KEY"] = "reelly-ca193726-B8UWmLERvIIp-S_PuqiJ5vkXKFcBM3Fv"
        
        # Initialize service
        reelly_service = ReellyService()
        
        # Test service status
        status = reelly_service.get_service_status()
        print(f"✅ Service Status: {status}")
        
        # Test if service is enabled
        if reelly_service.is_enabled():
            print("✅ Reelly service is enabled and configured")
        else:
            print("❌ Reelly service is disabled")
        
        # Test service configuration
        print(f"✅ Base URL: {reelly_service.base_url}")
        print(f"✅ API Key configured: {bool(reelly_service.api_key)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Reelly Service Error: {e}")
        return False

def test_rag_integration_basic():
    """Test basic RAG integration without API calls"""
    print("\n🧪 Testing Basic RAG Integration...")
    
    try:
        from rag_service import ImprovedRAGService
        from config.settings import DATABASE_URL
        
        # Initialize RAG service
        rag_service = ImprovedRAGService(DATABASE_URL)
        
        # Test if Reelly service is available
        if hasattr(rag_service, 'reelly_service') and rag_service.reelly_service:
            print("✅ Reelly service integrated into RAG service")
            
            if rag_service.reelly_service.is_enabled():
                print("✅ Reelly service is enabled in RAG")
            else:
                print("⚠️ Reelly service is disabled in RAG")
        else:
            print("❌ Reelly service not found in RAG service")
        
        # Test query analysis
        query = "I'm looking for a 2-bedroom apartment in Dubai Marina"
        analysis = rag_service.analyze_query(query)
        print(f"✅ Query Analysis: Intent={analysis.intent.value}, Confidence={analysis.confidence:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ RAG Integration Error: {e}")
        return False

def main():
    """Run basic tests"""
    print("🚀 Basic Reelly Integration Test")
    print("=" * 40)
    
    # Run tests
    tests = [
        ("Reelly Initialization", test_reelly_initialization),
        ("RAG Integration Basic", test_rag_integration_basic)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*15} {test_name} {'='*15}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*40}")
    print("📊 BASIC TEST RESULTS")
    print("=" * 40)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Basic integration is working! API connectivity can be tested separately.")
    else:
        print("⚠️ Some basic tests failed. Check configuration.")

if __name__ == "__main__":
    main()
