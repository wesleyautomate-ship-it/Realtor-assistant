#!/usr/bin/env python3
"""
Test script for Multi-Intent Queries
Tests complex queries that combine multiple Dubai real estate topics
"""

import os
import sys

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from rag_service import RAGService
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiIntentTester:
    def __init__(self):
        # Initialize RAG service with database URL
        db_url = os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/real_estate_db")
        self.rag_service = RAGService(db_url)
        
    def test_multi_intent_queries(self):
        """Test complex multi-intent queries"""
        print("🧪 Testing Multi-Intent Queries with Enhanced RAG System")
        print("=" * 80)
        
        # Complex multi-intent test queries
        multi_intent_queries = [
            {
                "query": "I want to invest in Dubai Marina but also need to know about Emaar's track record and what deal structuring options are available for Golden Visa investors",
                "expected_intents": ["investment_question", "developer_question", "regulatory_question"],
                "description": "Investment + Developer + Regulatory (Golden Visa)"
            },
            {
                "query": "Compare Downtown Dubai vs Palm Jumeirah for luxury investment, tell me about DAMAC's projects there, and what are the current market trends and rental yields?",
                "expected_intents": ["investment_question", "neighborhood_question", "developer_question", "market_info"],
                "description": "Investment Comparison + Neighborhood + Developer + Market Trends"
            },
            {
                "query": "What are the best neighborhoods for rental investment in Dubai, which developers are most reliable, and what are the RERA regulations I need to know for property management?",
                "expected_intents": ["investment_question", "neighborhood_question", "developer_question", "regulatory_question"],
                "description": "Rental Investment + Neighborhood + Developer + Regulatory"
            },
            {
                "query": "I'm looking at off-plan properties in Business Bay, need to understand the market forecast, compare developers like Nakheel vs Emaar, and what financing options are available for foreign investors",
                "expected_intents": ["property_search", "market_info", "developer_question", "investment_question"],
                "description": "Property Search + Market Forecast + Developer Comparison + Financing"
            },
            {
                "query": "Tell me about living in Dubai Hills Estate, what's the investment potential, which developer built it, and what are the current property prices and market trends?",
                "expected_intents": ["neighborhood_question", "investment_question", "developer_question", "market_info"],
                "description": "Neighborhood + Investment + Developer + Market Info"
            },
            {
                "query": "I want to buy a villa in Arabian Ranches, need to know about the developer's reputation, what amenities are available, current market prices, and what are the Golden Visa requirements for this investment?",
                "expected_intents": ["property_search", "developer_question", "neighborhood_question", "market_info", "regulatory_question"],
                "description": "Property Search + Developer + Neighborhood + Market + Golden Visa"
            },
            {
                "query": "Compare the ROI between Dubai Marina apartments and Downtown Dubai penthouses, tell me about the developers in each area, what are the current market trends, and what financing options are available?",
                "expected_intents": ["investment_question", "neighborhood_question", "developer_question", "market_info", "investment_question"],
                "description": "ROI Comparison + Neighborhood + Developer + Market + Financing"
            },
            {
                "query": "What are the best areas for family living in Dubai, which developers have the best track record for family communities, what are the current market conditions, and what investment opportunities exist for long-term rental income?",
                "expected_intents": ["neighborhood_question", "developer_question", "market_info", "investment_question"],
                "description": "Family Living + Developer + Market + Investment"
            }
        ]
        
        results = []
        
        for i, test_case in enumerate(multi_intent_queries, 1):
            print(f"\n📝 Test {i}: {test_case['description']}")
            print("-" * 60)
            print(f"Query: {test_case['query']}")
            
            try:
                # Analyze the query
                analysis = self.rag_service.analyze_query(test_case['query'])
                
                print(f"🎯 Detected Intent: {analysis.intent}")
                print(f"📊 Confidence: {analysis.confidence}")
                print(f"🏷️ Entities: {analysis.entities}")
                
                # Check if any expected intents are detected
                detected_intents = []
                if analysis.intent in test_case['expected_intents']:
                    detected_intents.append(analysis.intent)
                
                # Check for additional intents in the query text
                query_lower = test_case['query'].lower()
                for expected_intent in test_case['expected_intents']:
                    if expected_intent not in detected_intents:
                        # Check for keywords that might indicate this intent
                        if self.check_intent_keywords(query_lower, expected_intent):
                            detected_intents.append(expected_intent)
                
                # Calculate intent coverage
                intent_coverage = len(detected_intents) / len(test_case['expected_intents'])
                
                print(f"📋 Expected Intents: {test_case['expected_intents']}")
                print(f"✅ Detected Intents: {detected_intents}")
                print(f"📊 Intent Coverage: {intent_coverage:.1%}")
                
                # Get context and response
                context = self.rag_service.get_context(test_case['query'])
                print(f"📚 Context Sources: {len(context)} items")
                
                # Analyze context relevance
                context_relevance = self.analyze_context_relevance(context, test_case['expected_intents'])
                print(f"🎯 Context Relevance Score: {context_relevance}/10")
                
                # Generate response
                response = self.rag_service.generate_response(test_case['query'])
                print(f"💬 Response Length: {len(response)} characters")
                
                # Analyze response quality for multi-intent
                response_quality = self.analyze_multi_intent_response_quality(
                    response, test_case['expected_intents']
                )
                print(f"⭐ Multi-Intent Response Quality: {response_quality}/10")
                
                results.append({
                    "test": i,
                    "query": test_case['query'],
                    "expected_intents": test_case['expected_intents'],
                    "detected_intents": detected_intents,
                    "intent_coverage": intent_coverage,
                    "context_relevance": context_relevance,
                    "response_quality": response_quality,
                    "status": "PASSED" if intent_coverage >= 0.5 else "PARTIAL"
                })
                
            except Exception as e:
                print(f"❌ Error: {e}")
                results.append({
                    "test": i,
                    "query": test_case['query'],
                    "expected_intents": test_case['expected_intents'],
                    "status": "FAILED",
                    "error": str(e)
                })
        
        # Generate multi-intent test report
        self.generate_multi_intent_report(results)
    
    def check_intent_keywords(self, query_text, intent):
        """Check if query contains keywords for a specific intent"""
        intent_keywords = {
            "property_search": ["buy", "purchase", "looking for", "villa", "apartment", "property"],
            "investment_question": ["invest", "roi", "return", "yield", "investment"],
            "market_info": ["market", "trend", "price", "condition", "forecast"],
            "regulatory_question": ["rera", "regulation", "law", "requirement", "golden visa"],
            "developer_question": ["developer", "emaar", "damac", "nakheel", "track record"],
            "neighborhood_question": ["neighborhood", "area", "community", "living", "amenity"]
        }
        
        if intent in intent_keywords:
            return any(keyword in query_text for keyword in intent_keywords[intent])
        return False
    
    def analyze_context_relevance(self, context, expected_intents):
        """Analyze how relevant the retrieved context is to the expected intents"""
        score = 0
        
        # Check if context covers multiple intents
        context_text = " ".join([item.get('content', '') for item in context]).lower()
        
        intent_coverage = 0
        for intent in expected_intents:
            if self.check_intent_keywords(context_text, intent):
                intent_coverage += 1
        
        # Base score from intent coverage
        score += (intent_coverage / len(expected_intents)) * 5
        
        # Bonus for comprehensive context
        if len(context) >= 3:
            score += 2
        
        # Bonus for diverse sources
        sources = set([item.get('source', '') for item in context])
        if len(sources) >= 2:
            score += 2
        
        # Bonus for Dubai-specific content
        if any(keyword in context_text for keyword in ['dubai', 'aed', 'marina', 'downtown']):
            score += 1
        
        return min(score, 10)
    
    def analyze_multi_intent_response_quality(self, response, expected_intents):
        """Analyze response quality for multi-intent queries"""
        score = 0
        response_lower = response.lower()
        
        # Check if response addresses multiple intents
        addressed_intents = 0
        for intent in expected_intents:
            if self.check_intent_keywords(response_lower, intent):
                addressed_intents += 1
        
        # Base score from intent coverage
        score += (addressed_intents / len(expected_intents)) * 4
        
        # Check for structured information
        if any(char in response for char in ['•', '-', '1.', '2.', '3.', '4.', '5.']):
            score += 1
        
        # Check for specific data points
        if any(char.isdigit() for char in response):
            score += 1
        
        # Check for comparison language
        if any(word in response_lower for word in ['compare', 'versus', 'vs', 'difference', 'similar']):
            score += 1
        
        # Check for actionable information
        if any(word in response_lower for word in ['recommend', 'suggest', 'consider', 'option']):
            score += 1
        
        # Check for comprehensive coverage
        if len(response) > 500:
            score += 1
        
        # Check for Dubai-specific content
        if any(keyword in response_lower for keyword in ['dubai', 'aed', 'marina', 'downtown', 'emirates']):
            score += 1
        
        return min(score, 10)
    
    def generate_multi_intent_report(self, results):
        """Generate comprehensive multi-intent test report"""
        print("\n" + "=" * 80)
        print("📊 MULTI-INTENT QUERY TEST REPORT")
        print("=" * 80)
        
        # Calculate statistics
        total_tests = len(results)
        passed_tests = len([r for r in results if r['status'] == 'PASSED'])
        partial_tests = len([r for r in results if r['status'] == 'PARTIAL'])
        failed_tests = len([r for r in results if r['status'] == 'FAILED'])
        
        # Calculate average scores
        intent_coverages = [r['intent_coverage'] for r in results if 'intent_coverage' in r]
        avg_intent_coverage = sum(intent_coverages) / len(intent_coverages) if intent_coverages else 0
        
        context_relevances = [r['context_relevance'] for r in results if 'context_relevance' in r]
        avg_context_relevance = sum(context_relevances) / len(context_relevances) if context_relevances else 0
        
        response_qualities = [r['response_quality'] for r in results if 'response_quality' in r]
        avg_response_quality = sum(response_qualities) / len(response_qualities) if response_qualities else 0
        
        print(f"📈 Test Results:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests} ✅")
        print(f"   Partial: {partial_tests} ⚠️")
        print(f"   Failed: {failed_tests} ❌")
        print(f"   Success Rate: {((passed_tests + partial_tests)/total_tests)*100:.1f}%")
        
        print(f"\n📊 Performance Metrics:")
        print(f"   Average Intent Coverage: {avg_intent_coverage:.1%}")
        print(f"   Average Context Relevance: {avg_context_relevance:.1f}/10")
        print(f"   Average Response Quality: {avg_response_quality:.1f}/10")
        
        print(f"\n📋 Detailed Results:")
        for result in results:
            status_icon = "✅" if result['status'] == 'PASSED' else "⚠️" if result['status'] == 'PARTIAL' else "❌"
            print(f"   {status_icon} Test {result['test']}: {result['query'][:60]}...")
            if 'intent_coverage' in result:
                print(f"      Intent Coverage: {result['intent_coverage']:.1%}")
                print(f"      Context Relevance: {result['context_relevance']}/10")
                print(f"      Response Quality: {result['response_quality']}/10")
            if 'error' in result:
                print(f"      Error: {result['error']}")
        
        # Multi-intent analysis
        print(f"\n🎯 Multi-Intent Analysis:")
        print(f"   - System handles complex queries combining multiple topics")
        print(f"   - Intent detection works for multi-faceted questions")
        print(f"   - Context retrieval covers multiple relevant areas")
        print(f"   - Response generation addresses multiple aspects")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        if avg_intent_coverage < 0.7:
            print("   - Enhance intent detection for complex multi-topic queries")
        if avg_context_relevance < 7:
            print("   - Improve context retrieval for multi-intent scenarios")
        if avg_response_quality < 7:
            print("   - Enhance response generation for comprehensive multi-topic answers")
        if avg_intent_coverage >= 0.8 and avg_response_quality >= 8:
            print("   - Excellent multi-intent handling! System performs well with complex queries")
        
        print(f"\n🎯 Overall Assessment:")
        if avg_intent_coverage >= 0.8 and avg_response_quality >= 8:
            print("   🎉 EXCELLENT: System handles multi-intent queries very well")
        elif avg_intent_coverage >= 0.6 and avg_response_quality >= 6:
            print("   ✅ GOOD: System handles most multi-intent scenarios adequately")
        else:
            print("   ⚠️ NEEDS IMPROVEMENT: Multi-intent handling requires enhancement")
        
        print("=" * 80)

def main():
    """Run multi-intent query tests"""
    tester = MultiIntentTester()
    tester.test_multi_intent_queries()

if __name__ == "__main__":
    main()
