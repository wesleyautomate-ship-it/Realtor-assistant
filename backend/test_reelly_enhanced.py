#!/usr/bin/env python3
"""
Test script for enhanced chat functionality with Reelly API integration
"""

import requests
import json
from datetime import datetime

# Use internal container URL
BASE_URL = "http://localhost:8001"  # Internal container port

def test_reelly_integration():
    """Test the Reelly API integration endpoint"""
    print("🧪 Testing Reelly API Integration...")
    
    try:
        response = requests.post(f"{BASE_URL}/sessions/test-reelly")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Reelly API Test Result: {data}")
            return data
        else:
            print(f"❌ Reelly API Test Failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error testing Reelly API: {e}")
        return None

def test_enhanced_chat():
    """Test the enhanced chat functionality"""
    print("\n🧪 Testing Enhanced Chat Functionality...")
    
    # Test property search query
    test_queries = [
        "I am looking for a villa in Dubai Marina for 5 million 3 bedroom 4 bath",
        "Show me 2-bedroom apartments in Downtown Dubai under 3 million AED",
        "What are the current market trends in Palm Jumeirah?",
        "Find properties in Business Bay with rental yields above 6%"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test Query {i}: {query}")
        
        try:
            # Create a test chat session
            session_data = {
                "title": f"Test Session {i}",
                "role": "client"
            }
            
            session_response = requests.post(
                f"{BASE_URL}/sessions",
                json=session_data
            )
            
            if session_response.status_code == 200:
                session = session_response.json()
                session_id = session['session_id']
                
                # Send chat message
                chat_data = {
                    "message": query,
                    "role": "client"
                }
                
                chat_response = requests.post(
                    f"{BASE_URL}/sessions/{session_id}/chat",
                    json=chat_data
                )
                
                if chat_response.status_code == 200:
                    chat_result = chat_response.json()
                    print(f"✅ Response received in {chat_result['metadata']['response_time']:.2f}s")
                    print(f"📊 Confidence: {chat_result['confidence']}")
                    print(f"🎯 Intent: {chat_result['intent']}")
                    print(f"📚 Sources: {[s['source'] for s in chat_result['sources']]}")
                    
                    # Check if Reelly API was used
                    if any("Reelly" in s['source'] for s in chat_result['sources']):
                        print("🟢 Reelly API integration detected!")
                    else:
                        print("🟡 Using local data only")
                    
                    # Show first 200 characters of response
                    response_preview = chat_result['response'][:200] + "..." if len(chat_result['response']) > 200 else chat_result['response']
                    print(f"💬 Response Preview: {response_preview}")
                    
                else:
                    print(f"❌ Chat request failed: {chat_response.status_code} - {chat_response.text}")
                    
            else:
                print(f"❌ Session creation failed: {session_response.status_code} - {session_response.text}")
                
        except Exception as e:
            print(f"❌ Error in test {i}: {e}")

def main():
    """Main test function"""
    print("🚀 Dubai Real Estate RAG - Enhanced Chat Testing")
    print("=" * 60)
    
    # Test 1: Reelly API Integration
    reelly_result = test_reelly_integration()
    
    # Test 2: Enhanced Chat Functionality
    test_enhanced_chat()
    
    print("\n" + "=" * 60)
    print("🏁 Testing Complete!")
    
    if reelly_result and reelly_result.get('enabled'):
        print("✅ Reelly API integration is working")
    else:
        print("⚠️ Reelly API integration may not be fully functional")

if __name__ == "__main__":
    main()
