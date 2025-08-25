#!/usr/bin/env python3
"""
Test script for Chat Functionality with Enhanced RAG System
Tests Dubai-specific queries and responses
"""

import os
import sys
import requests
import json
from datetime import datetime
import time

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

class ChatFunctionalityTester:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.session_id = f"test_session_{int(time.time())}"
        
    def test_chat_endpoint(self):
        """Test the chat endpoint with Dubai-specific queries"""
        print("🧪 Testing Chat Functionality with Enhanced RAG System")
        print("=" * 70)
        
        # Test queries covering different Dubai real estate scenarios
        test_queries = [
            {
                "query": "I want to buy a 2-bedroom apartment in Dubai Marina for under AED 2 million. What are my options?",
                "expected_intent": "property_search",
                "description": "Property search with specific requirements"
            },
            {
                "query": "What are the Golden Visa requirements for property investment in Dubai?",
                "expected_intent": "investment_question",
                "description": "Golden Visa investment inquiry"
            },
            {
                "query": "Tell me about the current market trends in Downtown Dubai",
                "expected_intent": "market_info",
                "description": "Market trend inquiry"
            },
            {
                "query": "What are the RERA regulations for off-plan property purchases?",
                "expected_intent": "regulatory_question",
                "description": "Regulatory compliance question"
            },
            {
                "query": "Compare Dubai Marina vs Downtown Dubai for rental investment",
                "expected_intent": "investment_question",
                "description": "Investment comparison"
            },
            {
                "query": "Tell me about Emaar Properties and their track record",
                "expected_intent": "developer_question",
                "description": "Developer information request"
            },
            {
                "query": "What amenities are available in Palm Jumeirah?",
                "expected_intent": "neighborhood_question",
                "description": "Neighborhood amenities inquiry"
            }
        ]
        
        results = []
        
        for i, test_case in enumerate(test_queries, 1):
            print(f"\n📝 Test {i}: {test_case['description']}")
            print("-" * 50)
            print(f"Query: {test_case['query']}")
            
            try:
                # Make request to chat endpoint
                response = self.make_chat_request(test_case['query'])
                
                if response:
                    print(f"✅ Response received (Length: {len(response)} characters)")
                    print(f"📊 Response preview: {response[:200]}...")
                    
                    # Analyze response quality
                    quality_score = self.analyze_response_quality(response, test_case['expected_intent'])
                    print(f"🎯 Quality Score: {quality_score}/10")
                    
                    results.append({
                        "test": i,
                        "query": test_case['query'],
                        "expected_intent": test_case['expected_intent'],
                        "response_length": len(response),
                        "quality_score": quality_score,
                        "status": "PASSED"
                    })
                else:
                    print("❌ No response received")
                    results.append({
                        "test": i,
                        "query": test_case['query'],
                        "expected_intent": test_case['expected_intent'],
                        "status": "FAILED",
                        "error": "No response"
                    })
                    
            except Exception as e:
                print(f"❌ Error: {e}")
                results.append({
                    "test": i,
                    "query": test_case['query'],
                    "expected_intent": test_case['expected_intent'],
                    "status": "FAILED",
                    "error": str(e)
                })
        
        # Generate test report
        self.generate_test_report(results)
    
    def make_chat_request(self, query):
        """Make a request to the chat endpoint"""
        try:
            url = f"{self.base_url}/chat"
            payload = {
                "message": query,
                "session_id": self.session_id,
                "role": "client"
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('response', '')
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return None
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: Make sure the backend server is running")
            return None
        except requests.exceptions.Timeout:
            print("❌ Timeout Error: Request took too long")
            return None
        except Exception as e:
            print(f"❌ Request Error: {e}")
            return None
    
    def analyze_response_quality(self, response, expected_intent):
        """Analyze the quality of the response"""
        score = 0
        
        # Check for Dubai-specific content
        dubai_keywords = ['dubai', 'aed', 'marina', 'downtown', 'palm', 'emirates', 'uae']
        dubai_content = any(keyword in response.lower() for keyword in dubai_keywords)
        if dubai_content:
            score += 2
        
        # Check for intent-specific content
        intent_keywords = {
            'property_search': ['apartment', 'villa', 'property', 'bedroom', 'price', 'location'],
            'investment_question': ['investment', 'roi', 'yield', 'golden visa', 'return'],
            'market_info': ['market', 'trend', 'price', 'growth', 'demand'],
            'regulatory_question': ['rera', 'regulation', 'law', 'legal', 'compliance'],
            'developer_question': ['developer', 'emaar', 'damac', 'nakheel', 'project'],
            'neighborhood_question': ['amenity', 'area', 'neighborhood', 'community', 'lifestyle']
        }
        
        if expected_intent in intent_keywords:
            relevant_keywords = intent_keywords[expected_intent]
            relevant_content = any(keyword in response.lower() for keyword in relevant_keywords)
            if relevant_content:
                score += 3
        
        # Check for structured information
        if any(char in response for char in ['•', '-', '1.', '2.', '3.']):
            score += 1
        
        # Check for specific data points
        if any(char.isdigit() for char in response):
            score += 1
        
        # Check for helpful tone
        helpful_indicators = ['here', 'available', 'option', 'recommend', 'suggest']
        helpful_tone = any(indicator in response.lower() for indicator in helpful_indicators)
        if helpful_tone:
            score += 1
        
        # Check for actionable information
        action_indicators = ['contact', 'visit', 'call', 'schedule', 'book']
        actionable = any(indicator in response.lower() for indicator in action_indicators)
        if actionable:
            score += 1
        
        return min(score, 10)
    
    def generate_test_report(self, results):
        """Generate a comprehensive test report"""
        print("\n" + "=" * 70)
        print("📊 CHAT FUNCTIONALITY TEST REPORT")
        print("=" * 70)
        
        # Calculate statistics
        total_tests = len(results)
        passed_tests = len([r for r in results if r['status'] == 'PASSED'])
        failed_tests = total_tests - passed_tests
        
        # Calculate average quality score
        quality_scores = [r['quality_score'] for r in results if 'quality_score' in r]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        print(f"📈 Test Results:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests} ✅")
        print(f"   Failed: {failed_tests} ❌")
        print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print(f"   Average Quality Score: {avg_quality:.1f}/10")
        
        print(f"\n📋 Detailed Results:")
        for result in results:
            status_icon = "✅" if result['status'] == 'PASSED' else "❌"
            print(f"   {status_icon} Test {result['test']}: {result['query'][:50]}...")
            if 'quality_score' in result:
                print(f"      Quality: {result['quality_score']}/10")
            if 'error' in result:
                print(f"      Error: {result['error']}")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        if avg_quality < 7:
            print("   - Consider enhancing response quality with more specific Dubai data")
        if failed_tests > 0:
            print("   - Investigate failed tests and improve error handling")
        if avg_quality >= 8:
            print("   - Excellent response quality! System is performing well")
        
        print(f"\n🎯 Overall Assessment:")
        if passed_tests == total_tests and avg_quality >= 7:
            print("   🎉 EXCELLENT: All tests passed with high quality responses")
        elif passed_tests >= total_tests * 0.8 and avg_quality >= 5:
            print("   ✅ GOOD: Most tests passed with acceptable quality")
        else:
            print("   ⚠️ NEEDS IMPROVEMENT: Several issues detected")
        
        print("=" * 70)

def main():
    """Main test function"""
    tester = ChatFunctionalityTester()
    
    # Check if backend is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running")
            tester.test_chat_endpoint()
        else:
            print("❌ Backend server is not responding properly")
    except requests.exceptions.ConnectionError:
        print("❌ Backend server is not running. Please start the server first:")
        print("   cd backend && python main.py")
    except Exception as e:
        print(f"❌ Error checking backend: {e}")

if __name__ == "__main__":
    main()
