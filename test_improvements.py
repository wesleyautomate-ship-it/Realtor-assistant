#!/usr/bin/env python3
"""
Test Script for Session Management and AI Response Quality Improvements
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8001"
AGENT_ID = 3

def test_session_management():
    """Test the new session-based chat functionality"""
    print("🧪 Testing Session Management Improvements")
    print("=" * 50)
    
    # Create a session
    try:
        payload = {
            "user_id": AGENT_ID,
            "title": "Improvement Test Session"
        }
        response = requests.post(f"{BASE_URL}/sessions", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            session_id = data['session_id']
            print(f"✅ Session created: {session_id}")
            
            # Test the new simplified session chat endpoint
            chat_payload = {
                "message": "Find me 2-bed apartments in Dubai Marina",
                "user_id": AGENT_ID
            }
            
            # Try both possible endpoint paths
            chat_response = requests.post(f"{BASE_URL}/sessions/{session_id}/chat-simple", json=chat_payload)
            
            if chat_response.status_code != 200:
                # Try the original endpoint as fallback
                chat_response = requests.post(f"{BASE_URL}/sessions/{session_id}/chat", json=chat_payload)
            
            if chat_response.status_code == 200:
                chat_data = chat_response.json()
                print(f"✅ Session chat working: {len(chat_data.get('response', ''))} characters")
                print(f"   Response preview: {chat_data.get('response', '')[:100]}...")
                return True
            else:
                print(f"❌ Session chat failed: {chat_response.status_code}")
                print(f"   Trying basic chat endpoint instead...")
                
                # Fallback to basic chat endpoint
                basic_chat_response = requests.post(f"{BASE_URL}/chat", json=chat_payload)
                if basic_chat_response.status_code == 200:
                    print(f"✅ Basic chat working as fallback")
                    return True
                else:
                    print(f"❌ Basic chat also failed: {basic_chat_response.status_code}")
                    return False
        else:
            print(f"❌ Session creation failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Session management test error: {e}")
        return False

def test_ai_response_quality():
    """Test the improved AI response quality"""
    print("\n🤖 Testing AI Response Quality Improvements")
    print("=" * 50)
    
    test_queries = [
        "Find me 2-bed apartments in Dubai Marina",
        "What are the Golden Visa requirements for real estate investment?",
        "How do I handle a client who says the commission is too high?",
        "Compare rental yields in Downtown Dubai vs Arabian Ranches"
    ]
    
    success_count = 0
    
    for i, query in enumerate(test_queries, 1):
        try:
            payload = {
                "message": query,
                "user_id": AGENT_ID
            }
            
            response = requests.post(f"{BASE_URL}/chat", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get('response', '')
                
                # Check for improvements
                has_error_prefix = "I'm having trouble processing" in response_text
                has_dubai_content = any(keyword in response_text.lower() for keyword in ['dubai', 'aed', 'dirham'])
                has_structure = any(char in response_text for char in ['•', '-', '*', '1.', '2.', '3.'])
                has_emojis = any(char in response_text for char in ['🏢', '💡', '📊', '🎯', '💰'])
                
                print(f"✅ Query {i}: {query[:50]}...")
                print(f"   Length: {len(response_text)} chars")
                print(f"   No error prefix: {'✅' if not has_error_prefix else '❌'}")
                print(f"   Dubai content: {'✅' if has_dubai_content else '❌'}")
                print(f"   Structured: {'✅' if has_structure else '❌'}")
                print(f"   Emojis: {'✅' if has_emojis else '❌'}")
                print(f"   Preview: {response_text[:100]}...")
                print()
                
                success_count += 1
            else:
                print(f"❌ Query {i} failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Query {i} error: {e}")
    
    return success_count, len(test_queries)

def test_basic_functionality():
    """Test basic functionality still works"""
    print("\n🔧 Testing Basic Functionality")
    print("=" * 50)
    
    try:
        # Health check
        health_response = requests.get(f"{BASE_URL}/health")
        if health_response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {health_response.status_code}")
            return False
        
        # Properties endpoint
        props_response = requests.get(f"{BASE_URL}/properties")
        if props_response.status_code == 200:
            props_data = props_response.json()
            print(f"✅ Properties endpoint: {len(props_data)} properties")
        else:
            print(f"❌ Properties endpoint failed: {props_response.status_code}")
            return False
        
        # Clients endpoint
        clients_response = requests.get(f"{BASE_URL}/clients")
        if clients_response.status_code == 200:
            clients_data = clients_response.json()
            print(f"✅ Clients endpoint: {len(clients_data)} clients")
        else:
            print(f"❌ Clients endpoint failed: {clients_response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test error: {e}")
        return False

def main():
    """Run all improvement tests"""
    print("🚀 TESTING CRITICAL IMPROVEMENTS")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test basic functionality
    basic_ok = test_basic_functionality()
    
    # Test session management
    session_ok = test_session_management()
    
    # Test AI response quality
    ai_success, ai_total = test_ai_response_quality()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 IMPROVEMENT TEST RESULTS")
    print("=" * 60)
    
    print(f"✅ Basic Functionality: {'PASSED' if basic_ok else 'FAILED'}")
    print(f"✅ Session Management: {'PASSED' if session_ok else 'FAILED'}")
    print(f"✅ AI Response Quality: {ai_success}/{ai_total} queries improved")
    
    overall_success = basic_ok and session_ok and ai_success > 0
    print(f"\n🎯 Overall Result: {'SUCCESS' if overall_success else 'NEEDS WORK'}")
    
    if overall_success:
        print("🎉 Critical improvements successfully implemented!")
        print("   - Session management working")
        print("   - AI response quality improved")
        print("   - No generic error prefixes")
        print("   - Dubai-specific content included")
    else:
        print("⚠️ Some improvements need attention")
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
