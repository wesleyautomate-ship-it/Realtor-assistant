#!/usr/bin/env python3
"""
Test script to debug the AI manager directly
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

import google.generativeai as genai
from ai_manager import AIEnhancementManager

def test_ai_manager():
    """Test the AI manager directly"""
    
    print("🧪 Testing AI Manager Directly")
    print("=" * 50)
    
    try:
        # Initialize Google AI
        genai.configure(api_key="AIzaSyAocEBBwmq_eZ1Dy5RT9S7Kkfyw8nNibmM")
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        print("✅ Google AI initialized successfully")
        
        # Initialize AI manager
        ai_manager = AIEnhancementManager(
            db_url="postgresql://postgres:password123@localhost:5432/real_estate_db",
            model=model
        )
        
        print("✅ AI Manager initialized successfully")
        
        # Test chat request
        test_message = "Find properties in Dubai Marina under 3 million AED"
        test_session_id = "test_session_123"
        test_role = "agent"
        
        print(f"\n📝 Testing chat request:")
        print(f"   Message: {test_message}")
        print(f"   Session ID: {test_session_id}")
        print(f"   Role: {test_role}")
        
        result = ai_manager.process_chat_request(
            message=test_message,
            session_id=test_session_id,
            role=test_role
        )
        
        print(f"\n✅ Chat request successful:")
        print(f"   Response: {result['response'][:200]}...")
        print(f"   Intent: {result['query_analysis']['intent']}")
        print(f"   Sentiment: {result['query_analysis']['sentiment']}")
        
        print("\n🎉 AI Manager test passed!")
        
    except Exception as e:
        print(f"❌ Error testing AI manager: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ai_manager()
