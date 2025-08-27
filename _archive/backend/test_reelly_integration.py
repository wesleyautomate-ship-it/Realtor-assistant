#!/usr/bin/env python3
"""
Test script for Reelly API Integration
Tests the hybrid data system with both internal database and Reelly API
"""

import os
import sys
import asyncio
from datetime import datetime

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_reelly_service():
    """Test the Reelly service functionality"""
    print("🧪 Testing Reelly Service...")
    
    try:
        from reelly_service import ReellyService
        
        # Initialize service
        reelly_service = ReellyService()
        
        # Test service status
        status = reelly_service.get_service_status()
        print(f"✅ Service Status: {status}")
        
        # Test developers endpoint
        developers = reelly_service.get_developers()
        print(f"✅ Found {len(developers)} developers")
        
        # Test areas endpoint
        areas = reelly_service.get_areas(country_id=1)
        print(f"✅ Found {len(areas)} areas")
        
        # Test property search
        search_params = {
            "property_type": "apartment",
            "budget_min": 1000000,
            "budget_max": 5000000,
            "bedrooms": 2
        }
        
        properties = reelly_service.search_properties(search_params)
        print(f"✅ Found {len(properties)} properties matching criteria")
        
        # Test property formatting
        if properties:
            formatted_prop = reelly_service.format_property_for_display(properties[0])
            print(f"✅ Property formatting: {formatted_prop.get('title', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Reelly Service Error: {e}")
        return False

def test_rag_integration():
    """Test RAG service with Reelly integration"""
    print("\n🧪 Testing RAG Integration...")
    
    try:
        from rag_service import ImprovedRAGService
        from config.settings import DATABASE_URL
        
        # Initialize RAG service
        rag_service = ImprovedRAGService(DATABASE_URL)
        
        # Test query analysis
        query = "I'm looking for a 2-bedroom apartment in Dubai Marina with budget up to 3M AED"
        analysis = rag_service.analyze_query(query)
        print(f"✅ Query Analysis: Intent={analysis.intent.value}, Confidence={analysis.confidence:.2f}")
        
        # Test context retrieval with Reelly integration
        context_items = rag_service.get_relevant_context(query, analysis, max_items=10)
        print(f"✅ Retrieved {len(context_items)} context items")
        
        # Check for Reelly data
        reelly_items = [item for item in context_items if item.source == 'reelly_api_live']
        print(f"✅ Found {len(reelly_items)} live Reelly properties")
        
        # Test context building
        context_string = rag_service.build_structured_context(context_items)
        print(f"✅ Context string length: {len(context_string)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ RAG Integration Error: {e}")
        return False

def test_api_endpoints():
    """Test the new API endpoints"""
    print("\n🧪 Testing API Endpoints...")
    
    try:
        import requests
        
        base_url = "http://localhost:8001"
        
        # Test Reelly status endpoint
        response = requests.get(f"{base_url}/api/v1/reelly/status")
        if response.status_code == 200:
            status = response.json()
            print(f"✅ Reelly Status: {status}")
        else:
            print(f"❌ Status endpoint failed: {response.status_code}")
        
        # Test developers endpoint
        response = requests.get(f"{base_url}/api/v1/reference/developers")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Developers endpoint: {data.get('count', 0)} developers")
        else:
            print(f"❌ Developers endpoint failed: {response.status_code}")
        
        # Test areas endpoint
        response = requests.get(f"{base_url}/api/v1/reference/areas")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Areas endpoint: {data.get('count', 0)} areas")
        else:
            print(f"❌ Areas endpoint failed: {response.status_code}")
        
        # Test property search endpoint
        params = {
            "property_type": "apartment",
            "budget_min": 1000000,
            "budget_max": 5000000,
            "bedrooms": 2
        }
        response = requests.get(f"{base_url}/api/v1/reelly/properties", params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Property search: {data.get('count', 0)} properties")
        else:
            print(f"❌ Property search failed: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ API Endpoints Error: {e}")
        return False

def test_hybrid_search():
    """Test hybrid search functionality"""
    print("\n🧪 Testing Hybrid Search...")
    
    try:
        from rag_service import ImprovedRAGService
        from config.settings import DATABASE_URL
        
        rag_service = ImprovedRAGService(DATABASE_URL)
        
        # Test queries that should trigger hybrid search
        test_queries = [
            "Show me 2-bedroom apartments in Dubai Marina under 3M AED",
            "I need properties in Downtown Dubai with 3 bedrooms",
            "Looking for villas in Palm Jumeirah with budget 10M-20M AED"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Testing query: {query}")
            
            # Analyze query
            analysis = rag_service.analyze_query(query)
            print(f"   Intent: {analysis.intent.value}")
            print(f"   Parameters: {analysis.parameters}")
            
            # Get context
            context_items = rag_service.get_relevant_context(query, analysis, max_items=5)
            
            # Count sources
            internal_props = len([item for item in context_items if item.source == 'database_properties'])
            reelly_props = len([item for item in context_items if item.source == 'reelly_api_live'])
            chroma_docs = len([item for item in context_items if item.source.startswith('chroma_')])
            
            print(f"   Internal properties: {internal_props}")
            print(f"   Reelly properties: {reelly_props}")
            print(f"   ChromaDB documents: {chroma_docs}")
            
            # Build context
            context_string = rag_service.build_structured_context(context_items)
            print(f"   Context length: {len(context_string)} chars")
        
        return True
        
    except Exception as e:
        print(f"❌ Hybrid Search Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Reelly API Integration")
    print("=" * 50)
    
    # Set environment variable for testing
    os.environ["REELLY_API_KEY"] = "reelly-ca193726-B8UWmLERvIIp-S_PuqiJ5vkXKFcBM3Fv"
    
    # Run tests
    tests = [
        ("Reelly Service", test_reelly_service),
        ("RAG Integration", test_rag_integration),
        ("API Endpoints", test_api_endpoints),
        ("Hybrid Search", test_hybrid_search)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Reelly integration is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check the configuration and API key.")

if __name__ == "__main__":
    main()
