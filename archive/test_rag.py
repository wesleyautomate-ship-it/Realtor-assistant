#!/usr/bin/env python3
"""
Test script for the new RAG system
"""

import os
import sys
from dotenv import load_dotenv
from rag_service import RAGService, QueryIntent

# Load environment variables
load_dotenv()

def test_rag_system():
    """Test the new RAG system with various queries"""
    
    # Initialize RAG service
    rag_service = RAGService(
        db_url=os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/real_estate_db"),
        chroma_host=os.getenv("CHROMA_HOST", "localhost"),
        chroma_port=int(os.getenv("CHROMA_PORT", "8000"))
    )
    
    # Test queries
    test_queries = [
        "I want to buy a 3-bedroom apartment in Dubai Marina for under $500,000",
        "What are the current market trends in Dubai?",
        "How do I submit an offer for a property?",
        "I need help closing a deal with a difficult client",
        "Show me properties in downtown Dubai",
        "What's the commission structure for luxury properties?",
        "I'm looking for a villa with 4 bedrooms and a pool",
        "What are the best investment areas in Dubai?",
        "How do I handle client objections during negotiations?",
        "Tell me about the Golden Visa program"
    ]
    
    print("🧪 Testing New RAG System")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: {query}")
        print("-" * 30)
        
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
            
            # Build context string
            context = rag_service.build_context_string(context_items)
            print(f"Context length: {len(context)} characters")
            
            # Create prompt
            prompt = rag_service.create_dynamic_prompt(query, analysis, context, "client")
            print(f"Prompt length: {len(prompt)} characters")
            
            print("✅ Test passed")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    print("\n🎉 RAG System Testing Complete!")

if __name__ == "__main__":
    test_rag_system()
