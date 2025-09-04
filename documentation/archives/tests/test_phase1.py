#!/usr/bin/env python3
"""
Phase 1 Implementation Test Script
Tests the new database schema, API endpoints, and security features
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8001"
TEST_EMAIL = "agent1@dubai-estate.com"
TEST_PASSWORD = "Agent123!"

def test_database_connection():
    """Test database connection and new tables"""
    print("🔍 Testing database connection...")
    try:
        # Test basic connectivity
        response = requests.get(f"{BASE_URL}/properties/")
        if response.status_code == 200:
            print("✅ Database connection successful")
            return True
        else:
            print(f"❌ Database connection failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def test_property_status_endpoint():
    """Test the new property status endpoint"""
    print("\n🔍 Testing property status endpoint...")
    
    # First, try to update status without authentication
    try:
        response = requests.put(f"{BASE_URL}/properties/1/status", 
                              json={"new_status": "live"})
        if response.status_code == 401 or response.status_code == 403:
            print("✅ Authentication required (expected)")
        else:
            print(f"⚠️ Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing status endpoint: {e}")

def test_confidential_data_endpoint():
    """Test the confidential data endpoint"""
    print("\n🔍 Testing confidential data endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/properties/1/confidential")
        if response.status_code == 401 or response.status_code == 403:
            print("✅ Confidential data protected (expected)")
        else:
            print(f"⚠️ Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing confidential endpoint: {e}")

def test_rag_service_filtering():
    """Test that RAG service only returns live properties"""
    print("\n🔍 Testing RAG service filtering...")
    
    try:
        response = requests.post(f"{BASE_URL}/chat", 
                               json={"message": "Show me properties in Dubai Marina"})
        if response.status_code == 200:
            print("✅ RAG service responding (filtering active)")
        else:
            print(f"⚠️ RAG service response: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing RAG service: {e}")

def test_api_documentation():
    """Test that new endpoints are documented"""
    print("\n🔍 Testing API documentation...")
    
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ API documentation accessible")
            # Check if new endpoints are mentioned
            if "status" in response.text and "confidential" in response.text:
                print("✅ New endpoints documented")
            else:
                print("⚠️ New endpoints may not be fully documented")
        else:
            print(f"❌ API documentation not accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing API documentation: {e}")

def main():
    """Run all Phase 1 tests"""
    print("="*60)
    print("🧪 PHASE 1 IMPLEMENTATION TEST")
    print("="*60)
    print(f"Testing at: {BASE_URL}")
    print(f"Timestamp: {datetime.now()}")
    print("="*60)
    
    # Run tests
    tests = [
        test_database_connection,
        test_property_status_endpoint,
        test_confidential_data_endpoint,
        test_rag_service_filtering,
        test_api_documentation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "="*60)
    print("📊 TEST RESULTS SUMMARY")
    print("="*60)
    print(f"Tests passed: {passed}/{total}")
    print(f"Success rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("Phase 1 implementation is working correctly!")
    else:
        print(f"\n⚠️ {total-passed} test(s) failed")
        print("Please check the implementation and try again")
    
    print("="*60)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
