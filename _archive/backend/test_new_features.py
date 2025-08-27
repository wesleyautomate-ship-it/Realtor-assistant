#!/usr/bin/env python3
"""
Test script for new Dubai Real Estate RAG System features
Tests the daily briefing and content generation features
"""

import os
import sys
import asyncio
from datetime import datetime

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_manager import AIEnhancementManager
from scheduler import DailyBriefingScheduler
from advanced_features.intent_recognition import IntentRecognitionEngine
from config.settings import DATABASE_URL, GOOGLE_API_KEY, AI_MODEL
import google.generativeai as genai

def test_intent_recognition():
    """Test the new intent recognition patterns"""
    print("🧪 Testing Intent Recognition...")
    
    intent_engine = IntentRecognitionEngine()
    
    test_commands = [
        "/create post for property #1 targeting young professionals",
        "/draft email for client Sarah Johnson",
        "/generate whatsapp for all clients about new listings",
        "What's the market trend in Dubai Marina?",
        "Calculate ROI for a 2M AED investment"
    ]
    
    for command in test_commands:
        detected_intent = intent_engine.detect_intent(command)
        if detected_intent:
            print(f"✅ '{command}' -> {detected_intent.intent_type} (confidence: {detected_intent.confidence:.2f})")
        else:
            print(f"❌ '{command}' -> No intent detected")
    
    print()

def test_content_generation():
    """Test content generation features"""
    print("🧪 Testing Content Generation...")
    
    # Configure Google Gemini
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(AI_MODEL)
    
    # Initialize AI Manager
    ai_manager = AIEnhancementManager(DATABASE_URL, model)
    
    test_commands = [
        ("/create post for property #1 targeting young professionals", "create_instagram_post"),
        ("/draft email for client Sarah Johnson", "draft_follow_up_email"),
        ("/generate whatsapp for all clients about new listings", "generate_whatsapp_broadcast")
    ]
    
    for command, intent in test_commands:
        try:
            response = ai_manager.handle_content_generation_command(command, intent, 3)  # agent_id = 3
            print(f"✅ {intent}: {response[:100]}...")
        except Exception as e:
            print(f"❌ {intent}: Error - {e}")
    
    print()

def test_daily_briefing():
    """Test daily briefing generation"""
    print("🧪 Testing Daily Briefing Generation...")
    
    try:
        # Configure Google Gemini
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel(AI_MODEL)
        
        # Initialize AI Manager
        ai_manager = AIEnhancementManager(DATABASE_URL, model)
        
        # Test briefing for agent 3
        briefing = ai_manager.generate_daily_briefing_for_agent(3)
        print(f"✅ Daily Briefing for Agent 3: {briefing[:200]}...")
        
    except Exception as e:
        print(f"❌ Daily Briefing Error: {e}")
    
    print()

async def test_scheduler():
    """Test the scheduler functionality"""
    print("🧪 Testing Scheduler...")
    
    try:
        scheduler = DailyBriefingScheduler()
        
        # Test getting active agents
        active_agents = scheduler._get_active_agents()
        print(f"✅ Found {len(active_agents)} active agents")
        
        # Test sending briefings
        await scheduler.send_daily_briefings()
        print("✅ Daily briefings sent successfully")
        
    except Exception as e:
        print(f"❌ Scheduler Error: {e}")
    
    print()

def main():
    """Run all tests"""
    print("🚀 Testing New Dubai Real Estate RAG System Features")
    print("=" * 60)
    
    # Test intent recognition
    test_intent_recognition()
    
    # Test content generation
    test_content_generation()
    
    # Test daily briefing
    test_daily_briefing()
    
    # Test scheduler
    asyncio.run(test_scheduler())
    
    print("✅ All tests completed!")

if __name__ == "__main__":
    main()
