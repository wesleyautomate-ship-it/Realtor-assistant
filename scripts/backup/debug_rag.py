#!/usr/bin/env python3
"""
Debug script to test the improved RAG service directly
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from rag_service_improved import ImprovedRAGService, QueryIntent, QueryAnalysis

def test_improved_rag():
    """Test the improved RAG service directly"""
    
    print("🧪 Testing Improved RAG Service Directly")
    print("=" * 50)
    
    try:
        # Initialize the improved RAG service
        rag_service = ImprovedRAGService(
            db_url="postgresql://postgres:password123@localhost:5432/real_estate_db",
            chroma_host="localhost",
            chroma_port=8000
        )
        
        print("✅ RAG Service initialized successfully")
        
        # Test query analysis
        test_query = "Find properties in Dubai Marina under 3 million AED"
        print(f"\n📝 Testing query: {test_query}")
        
        analysis = rag_service.analyze_query(test_query)
        print(f"✅ Query analysis successful:")
        print(f"   Intent: {analysis.intent}")
        print(f"   Confidence: {analysis.confidence}")
        print(f"   Entities: {analysis.entities}")
        print(f"   Parameters: {analysis.parameters}")
        
        # Test context retrieval
        print(f"\n🔍 Testing context retrieval...")
        context_items = rag_service.get_relevant_context(test_query, analysis, max_items=3)
        print(f"✅ Context retrieval successful: {len(context_items)} items found")
        
        for i, item in enumerate(context_items):
            print(f"   Item {i+1}: {item.source} (score: {item.relevance_score:.2f})")
            print(f"   Content preview: {item.content[:100]}...")
        
        # Test context building
        print(f"\n📋 Testing context building...")
        context = rag_service.build_context_string(context_items)
        print(f"✅ Context building successful:")
        print(f"   Context length: {len(context)} characters")
        print(f"   Context preview: {context[:200]}...")
        
        # Test prompt creation
        print(f"\n🎯 Testing prompt creation...")
        prompt = rag_service.create_improved_prompt(
            query=test_query,
            analysis=analysis,
            context=context,
            user_role="agent"
        )
        print(f"✅ Prompt creation successful:")
        print(f"   Prompt length: {len(prompt)} characters")
        print(f"   Prompt preview: {prompt[:300]}...")
        
        print("\n🎉 All tests passed! The improved RAG service is working correctly.")
        
    except Exception as e:
        print(f"❌ Error testing improved RAG service: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_improved_rag()
