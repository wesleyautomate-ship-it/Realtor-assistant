#!/usr/bin/env python3
"""
Focused Fix Test Script
Tests the specific fixes for verbose responses and property search
"""

import requests
import json
import time

def test_simple_greeting():
    """Test simple greeting to check if response is concise"""
    print("🧪 TESTING: Simple Greeting Fix")
    print("="*50)
    
    query = "hi"
    
    try:
        response = requests.post(
            "http://localhost:8001/chat",
            json={
                "message": query,
                "role": "client",
                "session_id": f"greeting_test_{int(time.time())}"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('response', '')
            
            print(f"📝 Query: {query}")
            print(f"🤖 AI Response: {ai_response}")
            
            word_count = len(ai_response.split())
            print(f"📏 Word count: {word_count}")
            
            if word_count <= 20:
                print("✅ SUCCESS: Response is concise!")
            else:
                print("❌ FAILED: Response is still too verbose")
                
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def test_property_search():
    """Test property search to check if specific properties are returned"""
    print("\n🧪 TESTING: Property Search Fix")
    print("="*50)
    
    query = "Find properties with golf course views in Emirates Hills with 4+ bedrooms"
    
    try:
        response = requests.post(
            "http://localhost:8001/chat",
            json={
                "message": query,
                "role": "client",
                "session_id": f"property_test_{int(time.time())}"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('response', '')
            
            print(f"📝 Query: {query}")
            print(f"🤖 AI Response: {ai_response}")
            
            # Check for specific indicators
            has_properties = any(word in ai_response.lower() for word in ['property', 'villa', 'apartment', 'bedroom'])
            has_prices = any(char.isdigit() for char in ai_response)
            has_emirates_hills = 'emirates hills' in ai_response.lower()
            
            print(f"📊 Analysis:")
            print(f"   - Mentions properties: {'✅' if has_properties else '❌'}")
            print(f"   - Contains prices: {'✅' if has_prices else '❌'}")
            print(f"   - Mentions Emirates Hills: {'✅' if has_emirates_hills else '❌'}")
            
            word_count = len(ai_response.split())
            print(f"   - Word count: {word_count}")
            
            if has_properties and has_prices and word_count <= 150:
                print("✅ SUCCESS: Property search returns specific data!")
            else:
                print("❌ FAILED: Property search needs improvement")
                
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def test_simple_property_query():
    """Test simple property query"""
    print("\n🧪 TESTING: Simple Property Query")
    print("="*50)
    
    query = "I am looking for a property"
    
    try:
        response = requests.post(
            "http://localhost:8001/chat",
            json={
                "message": query,
                "role": "client",
                "session_id": f"simple_property_test_{int(time.time())}"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('response', '')
            
            print(f"📝 Query: {query}")
            print(f"🤖 AI Response: {ai_response}")
            
            word_count = len(ai_response.split())
            print(f"📏 Word count: {word_count}")
            
            if word_count <= 100:
                print("✅ SUCCESS: Simple property query is concise!")
            else:
                print("❌ FAILED: Simple property query is too verbose")
                
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    test_simple_greeting()
    test_property_search()
    test_simple_property_query()
