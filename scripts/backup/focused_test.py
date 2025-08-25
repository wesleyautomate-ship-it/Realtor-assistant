#!/usr/bin/env python3
"""
Focused Test Script for Emirates Hills Query
Tests the specific query that was showing poor quality responses
"""

import requests
import json
import time

def test_emirates_hills_query():
    """Test the specific Emirates Hills query that was problematic"""
    print("🧪 FOCUSED TEST: Emirates Hills Golf Course Properties")
    print("="*60)
    
    query = "Find properties with golf course views in Emirates Hills with 4+ bedrooms"
    
    try:
        # Send query to the RAG system
        response = requests.post(
            "http://localhost:8001/chat",
            json={
                "message": query,
                "role": "client",
                "session_id": f"focused_test_{int(time.time())}"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('response', '')
            
            print(f"📝 Query: {query}")
            print(f"\n🤖 AI Response:")
            print(f"{ai_response}")
            
            # Analyze the response
            print(f"\n📊 ANALYSIS:")
            
            # Check for specific data indicators
            specific_indicators = ['emirates hills', 'golf course', '4+', 'bedroom', 'villa', 'price', 'aed']
            found_indicators = [ind for ind in specific_indicators if ind.lower() in ai_response.lower()]
            print(f"✅ Found indicators: {found_indicators}")
            
            # Check for generic phrases
            generic_phrases = [
                'this might seem complex',
                'don\'t worry',
                'let me break it down',
                'highly specific',
                'potentially challenging'
            ]
            found_generic = [phrase for phrase in generic_phrases if phrase.lower() in ai_response.lower()]
            if found_generic:
                print(f"⚠️ Generic phrases found: {found_generic}")
            else:
                print(f"✅ No generic phrases detected")
            
            # Check for specific data
            has_numbers = any(char.isdigit() for char in ai_response)
            print(f"📊 Contains numerical data: {'✅ Yes' if has_numbers else '❌ No'}")
            
            # Check for specific property details
            property_details = ['bedroom', 'bathroom', 'price', 'location', 'amenities', 'developer']
            found_details = [detail for detail in property_details if detail.lower() in ai_response.lower()]
            print(f"🏠 Property details mentioned: {found_details}")
            
            # Check response length
            word_count = len(ai_response.split())
            print(f"📏 Response length: {word_count} words")
            
            # Overall assessment
            if len(found_indicators) >= 4 and not found_generic and has_numbers:
                print(f"\n🎉 EXCELLENT: Response is specific and data-driven!")
            elif len(found_indicators) >= 3 and not found_generic:
                print(f"\n✅ GOOD: Response is specific but could use more data")
            elif not found_generic:
                print(f"\n⚠️ FAIR: Response is not generic but lacks specific data")
            else:
                print(f"\n❌ POOR: Response is too generic")
                
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    test_emirates_hills_query()
