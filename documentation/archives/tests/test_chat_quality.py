#!/usr/bin/env python3
"""
Focused Chat Quality and Agentic Features Test
==============================================

This test specifically evaluates the chat quality, response accuracy,
and agentic features of the Dubai Real Estate RAG system.
"""

import requests
import json
import time
from typing import Dict, List, Any

class ChatQualityTest:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.test_results = {}
        
    def run_chat_quality_tests(self):
        """Run focused chat quality tests"""
        print("🎯 CHAT QUALITY & AGENTIC FEATURES TEST")
        print("=" * 50)
        
        # Create a test session
        session_id = self.create_test_session()
        if not session_id:
            print("❌ Failed to create test session")
            return
            
        print(f"✅ Test session created: {session_id}")
        
        # Test 1: Basic Chat Functionality
        self.test_basic_chat(session_id)
        
        # Test 2: Dubai-Specific Knowledge
        self.test_dubai_knowledge(session_id)
        
        # Test 3: Role-Based Responses
        self.test_role_based_responses(session_id)
        
        # Test 4: Conversation Memory
        self.test_conversation_memory(session_id)
        
        # Test 5: Response Quality Metrics
        self.test_response_quality_metrics(session_id)
        
        # Generate report
        self.generate_quality_report()
        
    def create_test_session(self) -> str:
        """Create a test session"""
        try:
            response = requests.post(f"{self.base_url}/sessions", json={
                "title": "Chat Quality Test Session",
                "role": "client",
                "user_preferences": {
                    "test_session": True,
                    "budget_range": [500000, 2000000],
                    "preferred_locations": ["Dubai Marina", "Downtown Dubai"]
                }
            })
            
            if response.status_code == 200:
                return response.json()["session_id"]
            else:
                print(f"❌ Session creation failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Session creation error: {e}")
            return None
            
    def test_basic_chat(self, session_id: str):
        """Test basic chat functionality"""
        print("\n🔍 Test 1: Basic Chat Functionality")
        print("-" * 30)
        
        test_queries = [
            "Hello, I'm interested in Dubai real estate",
            "What are the best areas to invest in?",
            "Tell me about property prices in Dubai Marina"
        ]
        
        results = []
        for i, query in enumerate(test_queries):
            try:
                response = requests.post(f"{self.base_url}/sessions/{session_id}/chat", json={
                    "message": query,
                    "role": "client"
                })
                
                if response.status_code == 200:
                    data = response.json()
                    results.append({
                        "query": query,
                        "status": "PASS",
                        "response_length": len(data["response"]),
                        "has_response": len(data["response"]) > 0,
                        "has_sources": len(data.get("sources", [])) > 0
                    })
                    print(f"✅ Query {i+1}: PASS (Response length: {len(data['response'])})")
                else:
                    results.append({
                        "query": query,
                        "status": "FAIL",
                        "error": f"HTTP {response.status_code}"
                    })
                    print(f"❌ Query {i+1}: FAIL (HTTP {response.status_code})")
                    
            except Exception as e:
                results.append({
                    "query": query,
                    "status": "ERROR",
                    "error": str(e)
                })
                print(f"⚠️ Query {i+1}: ERROR ({e})")
        
        self.test_results["basic_chat"] = results
        
    def test_dubai_knowledge(self, session_id: str):
        """Test Dubai-specific knowledge"""
        print("\n🔍 Test 2: Dubai-Specific Knowledge")
        print("-" * 30)
        
        dubai_queries = [
            "What are the current property prices in Dubai Marina?",
            "Tell me about the Golden Visa program in Dubai",
            "What are the rental yields in Downtown Dubai?",
            "Compare Dubai Marina vs Palm Jumeirah for investment"
        ]
        
        results = []
        for i, query in enumerate(dubai_queries):
            try:
                response = requests.post(f"{self.base_url}/sessions/{session_id}/chat", json={
                    "message": query,
                    "role": "client"
                })
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data["response"]
                    
                    # Analyze Dubai-specific content
                    quality_metrics = self.analyze_dubai_content(response_text)
                    
                    results.append({
                        "query": query,
                        "status": "PASS",
                        "response_length": len(response_text),
                        "has_dubai_keywords": quality_metrics["has_dubai_keywords"],
                        "has_specific_data": quality_metrics["has_specific_data"],
                        "has_structure": quality_metrics["has_structure"],
                        "has_sources": quality_metrics["has_sources"]
                    })
                    
                    print(f"✅ Dubai Query {i+1}: PASS")
                    print(f"   - Dubai keywords: {quality_metrics['has_dubai_keywords']}")
                    print(f"   - Specific data: {quality_metrics['has_specific_data']}")
                    print(f"   - Structured: {quality_metrics['has_structure']}")
                    
                else:
                    results.append({
                        "query": query,
                        "status": "FAIL",
                        "error": f"HTTP {response.status_code}"
                    })
                    print(f"❌ Dubai Query {i+1}: FAIL")
                    
            except Exception as e:
                results.append({
                    "query": query,
                    "status": "ERROR",
                    "error": str(e)
                })
                print(f"⚠️ Dubai Query {i+1}: ERROR")
        
        self.test_results["dubai_knowledge"] = results
        
    def test_role_based_responses(self, session_id: str):
        """Test role-based response differences"""
        print("\n🔍 Test 3: Role-Based Responses")
        print("-" * 30)
        
        # Test same query with different roles
        test_query = "What are the best investment opportunities in Dubai?"
        roles = ["client", "agent", "employee"]
        
        results = {}
        for role in roles:
            try:
                response = requests.post(f"{self.base_url}/sessions/{session_id}/chat", json={
                    "message": test_query,
                    "role": role
                })
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data["response"]
                    
                    # Analyze role-specific content
                    role_metrics = self.analyze_role_content(response_text, role)
                    
                    results[role] = {
                        "status": "PASS",
                        "response_length": len(response_text),
                        "has_role_specific_content": role_metrics["has_role_specific_content"],
                        "content_type": role_metrics["content_type"]
                    }
                    
                    print(f"✅ {role.upper()} role: PASS")
                    print(f"   - Length: {len(response_text)} chars")
                    print(f"   - Role-specific: {role_metrics['has_role_specific_content']}")
                    
                else:
                    results[role] = {
                        "status": "FAIL",
                        "error": f"HTTP {response.status_code}"
                    }
                    print(f"❌ {role.upper()} role: FAIL")
                    
            except Exception as e:
                results[role] = {
                    "status": "ERROR",
                    "error": str(e)
                }
                print(f"⚠️ {role.upper()} role: ERROR")
        
        self.test_results["role_based_responses"] = results
        
    def test_conversation_memory(self, session_id: str):
        """Test conversation memory and context retention"""
        print("\n🔍 Test 4: Conversation Memory")
        print("-" * 30)
        
        conversation_flow = [
            "I'm looking for a 2-bedroom apartment in Dubai Marina",
            "What's my budget range?",
            "Can you suggest properties within that budget?",
            "What about the ROI on these properties?"
        ]
        
        responses = []
        for i, message in enumerate(conversation_flow):
            try:
                response = requests.post(f"{self.base_url}/sessions/{session_id}/chat", json={
                    "message": message,
                    "role": "client"
                })
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data["response"]
                    
                    # Check if response maintains context
                    context_retention = self.check_context_retention(response_text, conversation_flow[:i])
                    
                    responses.append({
                        "message": message,
                        "status": "PASS",
                        "response_length": len(response_text),
                        "has_context": context_retention["has_context"],
                        "context_keywords": context_retention["context_keywords"]
                    })
                    
                    print(f"✅ Message {i+1}: PASS")
                    print(f"   - Context retention: {context_retention['has_context']}")
                    
                else:
                    responses.append({
                        "message": message,
                        "status": "FAIL",
                        "error": f"HTTP {response.status_code}"
                    })
                    print(f"❌ Message {i+1}: FAIL")
                    
            except Exception as e:
                responses.append({
                    "message": message,
                    "status": "ERROR",
                    "error": str(e)
                })
                print(f"⚠️ Message {i+1}: ERROR")
        
        self.test_results["conversation_memory"] = responses
        
    def test_response_quality_metrics(self, session_id: str):
        """Test response quality metrics"""
        print("\n🔍 Test 5: Response Quality Metrics")
        print("-" * 30)
        
        # Test performance metrics
        try:
            perf_response = requests.get(f"{self.base_url}/performance/report")
            if perf_response.status_code == 200:
                perf_data = perf_response.json()
                print("✅ Performance metrics retrieved")
                print(f"   - Avg response time: {perf_data.get('performance', {}).get('avg_response_time', 'N/A')}")
                print(f"   - Cache hit rate: {perf_data.get('performance', {}).get('cache_hit_rate', 'N/A')}")
                
                self.test_results["performance_metrics"] = perf_data
            else:
                print(f"❌ Performance metrics failed: HTTP {perf_response.status_code}")
                
        except Exception as e:
            print(f"⚠️ Performance metrics error: {e}")
            
        # Test feedback system
        try:
            feedback_response = requests.post(f"{self.base_url}/feedback/submit", json={
                "session_id": session_id,
                "query": "Test query for quality assessment",
                "response": "Test response for quality assessment",
                "feedback_type": "thumbs_up",
                "rating": 5,
                "text_feedback": "Excellent response with specific Dubai data and insights",
                "category": "accuracy"
            })
            
            if feedback_response.status_code == 200:
                print("✅ Feedback submitted successfully")
                self.test_results["feedback_submission"] = {"status": "PASS"}
            else:
                print(f"❌ Feedback submission failed: HTTP {feedback_response.status_code}")
                
        except Exception as e:
            print(f"⚠️ Feedback submission error: {e}")
            
    def analyze_dubai_content(self, response: str) -> Dict[str, bool]:
        """Analyze Dubai-specific content quality"""
        dubai_keywords = ["dubai", "marina", "downtown", "palm", "emaar", "aed", "dirham", "uae"]
        specific_data_indicators = ["aed", "dirham", "sq ft", "sqft", "bedroom", "apartment", "villa", "million"]
        structure_indicators = ["•", "-", "1.", "2.", "3.", "**", "##", "first", "second", "third"]
        source_indicators = ["according", "source", "report", "data", "market", "analysis"]
        
        return {
            "has_dubai_keywords": any(keyword in response.lower() for keyword in dubai_keywords),
            "has_specific_data": any(indicator in response.lower() for indicator in specific_data_indicators),
            "has_structure": any(indicator in response for indicator in structure_indicators),
            "has_sources": any(indicator in response.lower() for indicator in source_indicators)
        }
        
    def analyze_role_content(self, response: str, role: str) -> Dict[str, Any]:
        """Analyze role-specific content"""
        role_keywords = {
            "client": ["investment", "property", "price", "area", "budget", "roi"],
            "agent": ["commission", "market", "analysis", "comparison", "sales", "listing"],
            "employee": ["internal", "report", "data", "analysis", "company", "policy"]
        }
        
        content_types = {
            "client": "investment-focused",
            "agent": "sales-focused", 
            "employee": "internal-focused"
        }
        
        if role in role_keywords:
            has_role_content = any(keyword in response.lower() for keyword in role_keywords[role])
        else:
            has_role_content = False
            
        return {
            "has_role_specific_content": has_role_content,
            "content_type": content_types.get(role, "general")
        }
        
    def check_context_retention(self, response: str, previous_messages: List[str]) -> Dict[str, Any]:
        """Check if response retains context from previous messages"""
        context_keywords = ["dubai marina", "2-bedroom", "apartment", "budget", "roi", "investment"]
        found_keywords = [keyword for keyword in context_keywords if keyword in response.lower()]
        
        return {
            "has_context": len(found_keywords) > 0,
            "context_keywords": found_keywords
        }
        
    def generate_quality_report(self):
        """Generate quality test report"""
        print("\n" + "=" * 50)
        print("📊 CHAT QUALITY TEST REPORT")
        print("=" * 50)
        
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        
        for test_category, results in self.test_results.items():
            print(f"\n🔍 {test_category.upper()}")
            print("-" * 20)
            
            if isinstance(results, list):
                for result in results:
                    total_tests += 1
                    if result["status"] == "PASS":
                        passed_tests += 1
                        print(f"✅ PASS: {result.get('query', result.get('message', 'Test'))}")
                    else:
                        failed_tests += 1
                        print(f"❌ FAIL: {result.get('error', 'Unknown error')}")
                        
            elif isinstance(results, dict):
                for key, result in results.items():
                    if isinstance(result, dict) and "status" in result:
                        total_tests += 1
                        if result["status"] == "PASS":
                            passed_tests += 1
                            print(f"✅ {key}: PASS")
                        else:
                            failed_tests += 1
                            print(f"❌ {key}: FAIL")
        
        print(f"\n📈 QUALITY SUMMARY")
        print("-" * 20)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "N/A")
        
        # Save detailed report
        report_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "success_rate": (passed_tests/total_tests*100) if total_tests > 0 else 0
            },
            "detailed_results": self.test_results
        }
        
        with open("chat_quality_report.json", "w") as f:
            json.dump(report_data, f, indent=2)
            
        print(f"\n📄 Detailed report saved to: chat_quality_report.json")

def main():
    """Run chat quality tests"""
    tester = ChatQualityTest()
    tester.run_chat_quality_tests()

if __name__ == "__main__":
    main()
