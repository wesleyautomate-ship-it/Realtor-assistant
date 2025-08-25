#!/usr/bin/env python3
"""
Test script for the enhanced RAG system with Dubai real estate collections
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.rag_service import RAGService, QueryIntent

# Load environment variables
load_dotenv()

def test_enhanced_rag_system():
    """Test the enhanced RAG system with Dubai-specific queries"""
    
    # Initialize RAG service
    rag_service = RAGService(
        db_url=os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/real_estate_db"),
        chroma_host=os.getenv("CHROMA_HOST", "localhost"),
        chroma_port=int(os.getenv("CHROMA_PORT", "8000"))
    )
    
    # Dubai-specific test queries
    test_queries = [
        # Property search queries
        "I want to buy a 3-bedroom apartment in Dubai Marina for under AED 2 million",
        "Show me luxury villas in Palm Jumeirah",
        "Looking for properties in Downtown Dubai with Golden Visa eligibility",
        
        # Market information queries
        "What are the current property market trends in Dubai?",
        "How have Dubai property prices changed since 2020?",
        "What's the average rental yield in Business Bay?",
        
        # Investment queries  
        "What are the Golden Visa property investment requirements?",
        "Which Dubai areas offer the best ROI for foreign investors?",
        "Tell me about rental yields in different Dubai neighborhoods",
        
        # Regulatory queries
        "What are the RERA regulations for off-plan purchases?",
        "How does the Dubai freehold ownership system work?",
        "What are the legal requirements for property purchase in Dubai?",
        
        # Neighborhood queries
        "Tell me about living in Dubai Marina",
        "Compare Downtown Dubai vs Business Bay for investment",
        "What amenities are available in Palm Jumeirah?",
        
        # Developer queries
        "Tell me about Emaar Properties and their projects",
        "Which developer is best for luxury properties in Dubai?",
        "What's DAMAC's track record for project delivery?",
        
        # Agent support queries
        "How do I handle Golden Visa objections from clients?",
        "What are the best closing techniques for Dubai properties?",
        "How to present Dubai investment benefits to international clients?"
    ]
    
    print("🧪 Testing Enhanced RAG System with Dubai Real Estate Collections")
    print("=" * 80)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: {query}")
        print("-" * 60)
        
        try:
            # Analyze query
            analysis = rag_service.analyze_query(query)
            print(f"Intent: {analysis.intent.value}")
            print(f"Confidence: {analysis.confidence:.2f}")
            print(f"Entities: {analysis.entities}")
            print(f"Parameters: {analysis.parameters}")
            
            # Get context
            context_items = rag_service.get_relevant_context(query, analysis, max_items=3)
            print(f"Context items found: {len(context_items)}")
            
            for item in context_items:
                print(f"  - Source: {item.source} (Score: {item.relevance_score:.2f})")
            
            # Build context string
            context = rag_service.build_context_string(context_items)
            print(f"Context length: {len(context)} characters")
            
            # Create prompt
            prompt = rag_service.create_dynamic_prompt(query, analysis, context, "client")
            print(f"Prompt type: {analysis.intent.value} prompt")
            print(f"Prompt length: {len(prompt)} characters")
            
            print("✅ Test passed")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            import traceback
            print(traceback.format_exc())
    
    print("\n🎉 Enhanced RAG System Testing Complete!")
    
    # Test intent classification accuracy
    print("\n📊 Intent Classification Summary:")
    intent_counts = {}
    for query in test_queries:
        try:
            analysis = rag_service.analyze_query(query)
            intent = analysis.intent.value
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
        except:
            pass
    
    for intent, count in intent_counts.items():
        print(f"  - {intent}: {count} queries")

def test_specific_intents():
    """Test specific intent recognition"""
    
    rag_service = RAGService(
        db_url=os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/real_estate_db"),
        chroma_host=os.getenv("CHROMA_HOST", "localhost"),
        chroma_port=int(os.getenv("CHROMA_PORT", "8000"))
    )
    
    intent_tests = {
        QueryIntent.PROPERTY_SEARCH: [
            "Find me a 2-bedroom apartment in Dubai Marina",
            "Looking for villas in Arabian Ranches"
        ],
        QueryIntent.MARKET_INFO: [
            "What are the current market trends in Dubai?",
            "How are property prices performing?"
        ],
        QueryIntent.INVESTMENT_QUESTION: [
            "What's the ROI for Dubai Marina properties?",
            "Golden Visa investment requirements"
        ],
        QueryIntent.REGULATORY_QUESTION: [
            "RERA regulations for off-plan sales",
            "Dubai freehold ownership laws"
        ],
        QueryIntent.NEIGHBORHOOD_QUESTION: [
            "Tell me about Downtown Dubai amenities",
            "Compare Business Bay vs DIFC"
        ],
        QueryIntent.DEVELOPER_QUESTION: [
            "Emaar Properties track record",
            "Which developer builds in Palm Jumeirah?"
        ]
    }
    
    print("\n🎯 Testing Intent Classification Accuracy")
    print("=" * 50)
    
    correct_predictions = 0
    total_predictions = 0
    
    for expected_intent, queries in intent_tests.items():
        print(f"\n{expected_intent.value.upper()}:")
        
        for query in queries:
            analysis = rag_service.analyze_query(query)
            predicted_intent = analysis.intent
            
            is_correct = predicted_intent == expected_intent
            correct_predictions += is_correct
            total_predictions += 1
            
            status = "✅" if is_correct else "❌"
            print(f"  {status} '{query}' → {predicted_intent.value} (conf: {analysis.confidence:.2f})")
    
    accuracy = correct_predictions / total_predictions * 100
    print(f"\n📈 Intent Classification Accuracy: {accuracy:.1f}% ({correct_predictions}/{total_predictions})")

if __name__ == "__main__":
    test_enhanced_rag_system()
    test_specific_intents()
