#!/usr/bin/env python3
"""
Test script for Phase 3: Conversational CRM & Workflow Automation
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported"""
    try:
        from rag_service import QueryIntent, ImprovedRAGService
        print("✅ RAG service imports successful")
        
        from action_engine import ActionEngine, ActionPlan
        print("✅ Action engine imports successful")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_intent_recognition():
    """Test intent recognition for action intents"""
    try:
        from rag_service import ImprovedRAGService
        
        # Initialize RAG service
        rag_service = ImprovedRAGService(
            db_url="postgresql://test:test@localhost/test",
            chroma_host="localhost",
            chroma_port=8002
        )
        
        # Test action intent patterns
        test_messages = [
            "Update John Doe's status to qualified",
            "Log that my call with Sarah Smith went well",
            "Schedule a follow-up with Mike Johnson tomorrow at 2pm"
        ]
        
        for message in test_messages:
            analysis = rag_service.analyze_query(message)
            print(f"Message: '{message}'")
            print(f"  Intent: {analysis.intent}")
            print(f"  Entities: {analysis.entities}")
            print(f"  Confidence: {analysis.confidence}")
            print()
        
        return True
    except Exception as e:
        print(f"❌ Intent recognition test error: {e}")
        return False

def test_action_engine():
    """Test ActionEngine class creation"""
    try:
        from action_engine import ActionEngine
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        
        # Create a mock database session
        engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Create ActionEngine instance
        action_engine = ActionEngine(session, agent_id=1)
        
        print("✅ ActionEngine created successfully")
        print(f"  Valid statuses: {action_engine.valid_statuses}")
        print(f"  Interaction types: {action_engine.interaction_types}")
        
        return True
    except Exception as e:
        print(f"❌ ActionEngine test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Phase 3: Conversational CRM & Workflow Automation")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("Intent Recognition Test", test_intent_recognition),
        ("Action Engine Test", test_action_engine)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            print(f"✅ {test_name} PASSED")
            passed += 1
        else:
            print(f"❌ {test_name} FAILED")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Phase 3 implementation is ready.")
    else:
        print("⚠️ Some tests failed. Please check the implementation.")

if __name__ == "__main__":
    main()

