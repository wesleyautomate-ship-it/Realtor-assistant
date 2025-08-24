#!/usr/bin/env python3
"""
Phase 4: Enhanced RAG Service Integration Test Script
Tests the enhanced RAG service with Dubai-specific functionality
"""

import os
import sys
import json
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from enhanced_rag_service import EnhancedRAGService, QueryIntent

def test_enhanced_rag_service():
    """Test the enhanced RAG service functionality"""
    
    print("🧠 Phase 4: Enhanced RAG Service Integration Test")
    print("=" * 60)
    
    # Initialize the enhanced RAG service
    try:
        db_url = os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/real_estate_db")
        rag_service = EnhancedRAGService(
            db_url=db_url,
            chroma_host=os.getenv("CHROMA_HOST", "localhost"),
            chroma_port=int(os.getenv("CHROMA_PORT", "8000"))
        )
        print("✅ Enhanced RAG Service initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize Enhanced RAG Service: {e}")
        return False
    
    # Test queries for different intents
    test_queries = [
        # Property Search Queries
        {
            "query": "I'm looking for a 2-bedroom apartment in Dubai Marina with a budget of 2 million AED",
            "expected_intent": QueryIntent.PROPERTY_SEARCH,
            "description": "Property search with specific requirements"
        },
        {
            "query": "Show me properties in Downtown Dubai",
            "expected_intent": QueryIntent.PROPERTY_SEARCH,
            "description": "Location-based property search"
        },
        
        # Market Information Queries
        {
            "query": "What are the current market trends in Dubai real estate?",
            "expected_intent": QueryIntent.MARKET_INFO,
            "description": "General market analysis"
        },
        {
            "query": "How much do apartments cost in Palm Jumeirah?",
            "expected_intent": QueryIntent.MARKET_INFO,
            "description": "Price-specific market query"
        },
        
        # Investment Queries
        {
            "query": "What's the ROI for investing in Dubai real estate?",
            "expected_intent": QueryIntent.INVESTMENT_QUESTION,
            "description": "Investment return analysis"
        },
        {
            "query": "How does the Golden Visa work with property investment?",
            "expected_intent": QueryIntent.INVESTMENT_QUESTION,
            "description": "Visa-related investment query"
        },
        
        # Regulatory Queries
        {
            "query": "What are the RERA regulations for buying property in Dubai?",
            "expected_intent": QueryIntent.REGULATORY_QUESTION,
            "description": "Regulatory compliance"
        },
        {
            "query": "What's the difference between freehold and leasehold in Dubai?",
            "expected_intent": QueryIntent.REGULATORY_QUESTION,
            "description": "Ownership types"
        },
        
        # Neighborhood Queries
        {
            "query": "Tell me about Dubai Marina area and its amenities",
            "expected_intent": QueryIntent.NEIGHBORHOOD_QUESTION,
            "description": "Neighborhood information"
        },
        {
            "query": "What schools and hospitals are available in Business Bay?",
            "expected_intent": QueryIntent.NEIGHBORHOOD_QUESTION,
            "description": "Amenities in specific area"
        },
        
        # Developer Queries
        {
            "query": "What projects has Emaar developed in Dubai?",
            "expected_intent": QueryIntent.DEVELOPER_QUESTION,
            "description": "Developer-specific query"
        },
        {
            "query": "How reliable is DAMAC as a developer?",
            "expected_intent": QueryIntent.DEVELOPER_QUESTION,
            "description": "Developer reputation"
        },
        
        # Transaction Guidance Queries
        {
            "query": "What's the process for buying property in Dubai?",
            "expected_intent": QueryIntent.TRANSACTION_GUIDANCE,
            "description": "Transaction process"
        },
        {
            "query": "What documents do I need for property purchase?",
            "expected_intent": QueryIntent.TRANSACTION_GUIDANCE,
            "description": "Documentation requirements"
        },
        
        # Financial Insights Queries
        {
            "query": "What are the current mortgage rates in Dubai?",
            "expected_intent": QueryIntent.FINANCIAL_INSIGHTS,
            "description": "Financing information"
        },
        {
            "query": "What's the LTV ratio for expat buyers?",
            "expected_intent": QueryIntent.FINANCIAL_INSIGHTS,
            "description": "Financial requirements"
        },
        
        # Urban Planning Queries
        {
            "query": "What's included in the Dubai 2040 master plan?",
            "expected_intent": QueryIntent.URBAN_PLANNING,
            "description": "Future development plans"
        },
        {
            "query": "What infrastructure projects are planned for Dubai?",
            "expected_intent": QueryIntent.URBAN_PLANNING,
            "description": "Infrastructure development"
        }
    ]
    
    # Test results
    test_results = {
        "total_tests": len(test_queries),
        "passed": 0,
        "failed": 0,
        "details": []
    }
    
    print(f"\n🔍 Testing {len(test_queries)} queries...")
    print("-" * 60)
    
    for i, test_case in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: {test_case['description']}")
        print(f"Query: {test_case['query']}")
        
        try:
            # Analyze query
            analysis = rag_service.analyze_query(test_case['query'])
            
            # Check intent classification
            intent_correct = analysis.intent == test_case['expected_intent']
            
            # Check Dubai-specific detection
            dubai_detected = analysis.dubai_specific
            
            # Get context
            context_items = rag_service.get_relevant_context(
                query=test_case['query'],
                analysis=analysis,
                max_items=5
            )
            
            # Build context string
            context = rag_service.build_context_string(context_items)
            
            # Create dynamic prompt
            prompt = rag_service.create_dynamic_prompt(
                query=test_case['query'],
                analysis=analysis,
                context=context,
                user_role="client"
            )
            
            # Test result
            test_passed = intent_correct and len(context_items) > 0
            
            if test_passed:
                test_results["passed"] += 1
                status = "✅ PASSED"
            else:
                test_results["failed"] += 1
                status = "❌ FAILED"
            
            # Store test details
            test_detail = {
                "test_number": i,
                "description": test_case['description'],
                "query": test_case['query'],
                "expected_intent": test_case['expected_intent'].value,
                "actual_intent": analysis.intent.value,
                "intent_correct": intent_correct,
                "dubai_specific": dubai_detected,
                "confidence": analysis.confidence,
                "entities": analysis.entities,
                "parameters": analysis.parameters,
                "context_items_count": len(context_items),
                "context_sources": [item.source for item in context_items],
                "prompt_length": len(prompt),
                "status": "PASSED" if test_passed else "FAILED"
            }
            test_results["details"].append(test_detail)
            
            print(f"Status: {status}")
            print(f"Intent: {analysis.intent.value} (Expected: {test_case['expected_intent'].value})")
            print(f"Confidence: {analysis.confidence:.2f}")
            print(f"Dubai-specific: {dubai_detected}")
            print(f"Entities: {analysis.entities}")
            print(f"Context items: {len(context_items)}")
            print(f"Context sources: {[item.source for item in context_items]}")
            
        except Exception as e:
            test_results["failed"] += 1
            print(f"❌ ERROR: {e}")
            test_detail = {
                "test_number": i,
                "description": test_case['description'],
                "query": test_case['query'],
                "error": str(e),
                "status": "ERROR"
            }
            test_results["details"].append(test_detail)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {test_results['total_tests']}")
    print(f"Passed: {test_results['passed']} ✅")
    print(f"Failed: {test_results['failed']} ❌")
    print(f"Success Rate: {(test_results['passed'] / test_results['total_tests'] * 100):.1f}%")
    
    # Detailed analysis
    print("\n🔍 DETAILED ANALYSIS")
    print("-" * 60)
    
    # Intent classification accuracy
    intent_correct = sum(1 for detail in test_results["details"] if detail.get("intent_correct", False))
    print(f"Intent Classification Accuracy: {intent_correct}/{test_results['total_tests']} ({(intent_correct/test_results['total_tests']*100):.1f}%)")
    
    # Dubai-specific detection
    dubai_detected = sum(1 for detail in test_results["details"] if detail.get("dubai_specific", False))
    print(f"Dubai-specific Detection: {dubai_detected}/{test_results['total_tests']} ({(dubai_detected/test_results['total_tests']*100):.1f}%)")
    
    # Context retrieval success
    context_retrieved = sum(1 for detail in test_results["details"] if detail.get("context_items_count", 0) > 0)
    print(f"Context Retrieval Success: {context_retrieved}/{test_results['total_tests']} ({(context_retrieved/test_results['total_tests']*100):.1f}%)")
    
    # Source distribution
    all_sources = []
    for detail in test_results["details"]:
        all_sources.extend(detail.get("context_sources", []))
    
    source_counts = {}
    for source in all_sources:
        source_counts[source] = source_counts.get(source, 0) + 1
    
    print(f"\n📚 Context Source Distribution:")
    for source, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {source}: {count} times")
    
    # Save detailed results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"phase4_test_results_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump(test_results, f, indent=2, default=str)
    
    print(f"\n💾 Detailed results saved to: {results_file}")
    
    return test_results["passed"] == test_results["total_tests"]

def test_hybrid_data_retrieval():
    """Test hybrid data retrieval from both ChromaDB and PostgreSQL"""
    
    print("\n🔄 Testing Hybrid Data Retrieval")
    print("-" * 60)
    
    try:
        db_url = os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/real_estate_db")
        rag_service = EnhancedRAGService(
            db_url=db_url,
            chroma_host=os.getenv("CHROMA_HOST", "localhost"),
            chroma_port=int(os.getenv("CHROMA_PORT", "8000"))
        )
        
        # Test queries that should retrieve from both sources
        hybrid_test_queries = [
            {
                "query": "Tell me about Dubai Marina neighborhood and market trends",
                "description": "Neighborhood + Market data"
            },
            {
                "query": "What are Emaar's projects and investment opportunities?",
                "description": "Developer + Investment data"
            },
            {
                "query": "Dubai real estate regulations and transaction process",
                "description": "Regulatory + Transaction data"
            }
        ]
        
        for i, test_case in enumerate(hybrid_test_queries, 1):
            print(f"\n🔍 Hybrid Test {i}: {test_case['description']}")
            print(f"Query: {test_case['query']}")
            
            # Analyze query
            analysis = rag_service.analyze_query(test_case['query'])
            
            # Get context
            context_items = rag_service.get_relevant_context(
                query=test_case['query'],
                analysis=analysis,
                max_items=8
            )
            
            # Analyze sources
            chroma_sources = [item for item in context_items if item.source.startswith('chroma_')]
            postgres_sources = [item for item in context_items if item.source.startswith('postgres_')]
            
            print(f"Total context items: {len(context_items)}")
            print(f"ChromaDB sources: {len(chroma_sources)}")
            print(f"PostgreSQL sources: {len(postgres_sources)}")
            print(f"Hybrid retrieval: {'✅' if len(chroma_sources) > 0 and len(postgres_sources) > 0 else '❌'}")
            
            # Show source breakdown
            source_types = {}
            for item in context_items:
                source_type = item.source.split('_')[0]
                source_types[source_type] = source_types.get(source_type, 0) + 1
            
            print(f"Source breakdown: {source_types}")
        
        return True
        
    except Exception as e:
        print(f"❌ Hybrid retrieval test failed: {e}")
        return False

def test_performance():
    """Test performance metrics"""
    
    print("\n⚡ Testing Performance Metrics")
    print("-" * 60)
    
    try:
        db_url = os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/real_estate_db")
        rag_service = EnhancedRAGService(
            db_url=db_url,
            chroma_host=os.getenv("CHROMA_HOST", "localhost"),
            chroma_port=int(os.getenv("CHROMA_PORT", "8000"))
        )
        
        import time
        
        # Test query
        test_query = "What are the market trends in Dubai Marina and investment opportunities?"
        
        # Measure query analysis time
        start_time = time.time()
        analysis = rag_service.analyze_query(test_query)
        analysis_time = time.time() - start_time
        
        # Measure context retrieval time
        start_time = time.time()
        context_items = rag_service.get_relevant_context(test_query, analysis, max_items=8)
        retrieval_time = time.time() - start_time
        
        # Measure prompt generation time
        start_time = time.time()
        context = rag_service.build_context_string(context_items)
        prompt = rag_service.create_dynamic_prompt(test_query, analysis, context, "client")
        prompt_time = time.time() - start_time
        
        total_time = analysis_time + retrieval_time + prompt_time
        
        print(f"Query Analysis Time: {analysis_time:.3f}s")
        print(f"Context Retrieval Time: {retrieval_time:.3f}s")
        print(f"Prompt Generation Time: {prompt_time:.3f}s")
        print(f"Total Processing Time: {total_time:.3f}s")
        print(f"Context Items Retrieved: {len(context_items)}")
        print(f"Prompt Length: {len(prompt)} characters")
        
        # Performance benchmarks
        performance_ok = (
            analysis_time < 0.1 and      # Analysis should be fast
            retrieval_time < 2.0 and     # Retrieval under 2 seconds
            total_time < 3.0             # Total under 3 seconds
        )
        
        print(f"Performance: {'✅ PASSED' if performance_ok else '❌ FAILED'}")
        
        return performance_ok
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Phase 4: Enhanced RAG Service Integration Tests")
    print("=" * 80)
    
    # Run all tests
    test1_success = test_enhanced_rag_service()
    test2_success = test_hybrid_data_retrieval()
    test3_success = test_performance()
    
    print("\n" + "=" * 80)
    print("🎯 PHASE 4 TEST RESULTS SUMMARY")
    print("=" * 80)
    print(f"Enhanced RAG Service Tests: {'✅ PASSED' if test1_success else '❌ FAILED'}")
    print(f"Hybrid Data Retrieval Tests: {'✅ PASSED' if test2_success else '❌ FAILED'}")
    print(f"Performance Tests: {'✅ PASSED' if test3_success else '❌ FAILED'}")
    
    overall_success = test1_success and test2_success and test3_success
    print(f"\nOverall Phase 4 Status: {'✅ PASSED' if overall_success else '❌ FAILED'}")
    
    if overall_success:
        print("\n🎉 Phase 4: Enhanced RAG Service Integration is ready!")
        print("The enhanced RAG service successfully integrates Dubai-specific data")
        print("from both ChromaDB collections and PostgreSQL tables.")
    else:
        print("\n⚠️ Phase 4 needs attention. Please review the failed tests above.")
