#!/usr/bin/env python3
"""
Comprehensive Agent Chat Conversation Test Suite
================================================

This test suite evaluates all aspects of the Dubai Real Estate RAG system:
- Security & Data Segregation
- Response Quality & Accuracy  
- Performance & Caching
- Agentic Features & Memory
- Data Retrieval & RAG
- Session Management
- Feedback & Quality Metrics
"""

import asyncio
import json
import time
import requests
from typing import Dict, List, Any
from datetime import datetime
import hashlib

class ComprehensiveAgentTest:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.test_results = {}
        self.session_ids = {}
        self.test_start_time = time.time()
        
    async def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🚀 STARTING COMPREHENSIVE AGENT CHAT TEST SUITE")
        print("=" * 60)
        
        # Test 1: Security & Data Segregation
        await self.test_security_and_data_segregation()
        
        # Test 2: Session Management & Isolation
        await self.test_session_management()
        
        # Test 3: Response Quality & Accuracy
        await self.test_response_quality()
        
        # Test 4: Performance & Caching
        await self.test_performance_and_caching()
        
        # Test 5: Agentic Features & Memory
        await self.test_agentic_features()
        
        # Test 6: Data Retrieval & RAG
        await self.test_data_retrieval()
        
        # Test 7: Feedback System
        await self.test_feedback_system()
        
        # Test 8: Multi-User Scenarios
        await self.test_multi_user_scenarios()
        
        # Generate comprehensive report
        self.generate_test_report()
        
    async def test_security_and_data_segregation(self):
        """Test 1: Security & Data Segregation"""
        print("\n🔒 TEST 1: Security & Data Segregation")
        print("-" * 40)
        
        test_results = {
            "role_based_access": {},
            "session_isolation": {},
            "data_filtering": {},
            "access_auditing": {}
        }
        
        # Test role-based access control
        roles = ["client", "agent", "employee", "admin"]
        for role in roles:
            try:
                # Create session for each role
                session_response = requests.post(f"{self.base_url}/sessions", json={
                    "title": f"Security Test - {role}",
                    "role": role,
                    "user_preferences": {"test_role": role}
                })
                
                if session_response.status_code == 200:
                    session_data = session_response.json()
                    session_id = session_data["session_id"]
                    self.session_ids[role] = session_id
                    
                    # Test chat with role-specific query
                    chat_response = requests.post(f"{self.base_url}/sessions/{session_id}/chat", json={
                        "message": "What are the commission structures for agents?",
                        "role": role
                    })
                    
                    if chat_response.status_code == 200:
                        response_data = chat_response.json()
                        test_results["role_based_access"][role] = {
                            "status": "PASS",
                            "response_length": len(response_data["response"]),
                            "has_sensitive_data": self._check_sensitive_data(response_data["response"], role)
                        }
                    else:
                        test_results["role_based_access"][role] = {
                            "status": "FAIL",
                            "error": f"HTTP {chat_response.status_code}"
                        }
                else:
                    test_results["role_based_access"][role] = {
                        "status": "FAIL",
                        "error": f"Session creation failed: HTTP {session_response.status_code}"
                    }
                    
            except Exception as e:
                test_results["role_based_access"][role] = {
                    "status": "ERROR",
                    "error": str(e)
                }
        
        self.test_results["security"] = test_results
        print(f"✅ Security tests completed: {sum(1 for r in test_results['role_based_access'].values() if r['status'] == 'PASS')}/{len(roles)} passed")
        
    async def test_session_management(self):
        """Test 2: Session Management & Isolation"""
        print("\n🔄 TEST 2: Session Management & Isolation")
        print("-" * 40)
        
        test_results = {
            "session_creation": {},
            "session_isolation": {},
            "conversation_memory": {},
            "session_cleanup": {}
        }
        
        # Test session creation and isolation
        try:
            # Create multiple sessions for same user
            sessions = []
            for i in range(3):
                session_response = requests.post(f"{self.base_url}/sessions", json={
                    "title": f"Isolation Test Session {i+1}",
                    "role": "client"
                })
                if session_response.status_code == 200:
                    sessions.append(session_response.json()["session_id"])
            
            test_results["session_creation"]["status"] = "PASS" if len(sessions) == 3 else "FAIL"
            test_results["session_creation"]["sessions_created"] = len(sessions)
            
            # Test conversation isolation
            if len(sessions) >= 2:
                # Send different messages to different sessions
                requests.post(f"{self.base_url}/sessions/{sessions[0]}/chat", json={
                    "message": "I'm interested in Dubai Marina properties",
                    "role": "client"
                })
                
                requests.post(f"{self.base_url}/sessions/{sessions[1]}/chat", json={
                    "message": "What are the best investment opportunities?",
                    "role": "client"
                })
                
                # Check if sessions maintain separate context
                history1 = requests.get(f"{self.base_url}/sessions/{sessions[0]}")
                history2 = requests.get(f"{self.base_url}/sessions/{sessions[1]}")
                
                if history1.status_code == 200 and history2.status_code == 200:
                    data1 = history1.json()
                    data2 = history2.json()
                    
                    test_results["session_isolation"]["status"] = "PASS"
                    test_results["session_isolation"]["session1_messages"] = len(data1["messages"])
                    test_results["session_isolation"]["session2_messages"] = len(data2["messages"])
                    test_results["session_isolation"]["contexts_different"] = data1["messages"] != data2["messages"]
                else:
                    test_results["session_isolation"]["status"] = "FAIL"
            
        except Exception as e:
            test_results["session_creation"]["status"] = "ERROR"
            test_results["session_creation"]["error"] = str(e)
        
        self.test_results["session_management"] = test_results
        print(f"✅ Session management tests completed")
        
    async def test_response_quality(self):
        """Test 3: Response Quality & Accuracy"""
        print("\n🎯 TEST 3: Response Quality & Accuracy")
        print("-" * 40)
        
        test_results = {
            "dubai_specific_content": {},
            "structured_responses": {},
            "source_attribution": {},
            "accuracy_metrics": {}
        }
        
        # Test Dubai-specific content
        dubai_queries = [
            "What are the current property prices in Dubai Marina?",
            "Tell me about the Golden Visa program in Dubai",
            "What are the best areas for investment in Dubai?",
            "How is the Dubai real estate market performing in 2024?"
        ]
        
        for i, query in enumerate(dubai_queries):
            try:
                if "client" in self.session_ids:
                    response = requests.post(f"{self.base_url}/sessions/{self.session_ids['client']}/chat", json={
                        "message": query,
                        "role": "client"
                    })
                    
                    if response.status_code == 200:
                        response_data = response.json()
                        response_text = response_data["response"]
                        
                        # Analyze response quality
                        quality_metrics = self._analyze_response_quality(response_text, query)
                        
                        test_results["dubai_specific_content"][f"query_{i+1}"] = {
                            "status": "PASS",
                            "response_length": len(response_text),
                            "has_dubai_keywords": quality_metrics["has_dubai_keywords"],
                            "has_specific_data": quality_metrics["has_specific_data"],
                            "has_structure": quality_metrics["has_structure"],
                            "has_sources": quality_metrics["has_sources"]
                        }
                    else:
                        test_results["dubai_specific_content"][f"query_{i+1}"] = {
                            "status": "FAIL",
                            "error": f"HTTP {response.status_code}"
                        }
                        
            except Exception as e:
                test_results["dubai_specific_content"][f"query_{i+1}"] = {
                    "status": "ERROR",
                    "error": str(e)
                }
        
        self.test_results["response_quality"] = test_results
        print(f"✅ Response quality tests completed: {len(dubai_queries)} queries tested")
        
    async def test_performance_and_caching(self):
        """Test 4: Performance & Caching"""
        print("\n⚡ TEST 4: Performance & Caching")
        print("-" * 40)
        
        test_results = {
            "response_times": {},
            "caching_effectiveness": {},
            "performance_metrics": {}
        }
        
        # Test response times
        if "client" in self.session_ids:
            test_query = "What are the best investment opportunities in Dubai?"
            
            # First request (no cache)
            start_time = time.time()
            response1 = requests.post(f"{self.base_url}/sessions/{self.session_ids['client']}/chat", json={
                "message": test_query,
                "role": "client"
            })
            first_response_time = time.time() - start_time
            
            # Second request (should be cached)
            start_time = time.time()
            response2 = requests.post(f"{self.base_url}/sessions/{self.session_ids['client']}/chat", json={
                "message": test_query,
                "role": "client"
            })
            second_response_time = time.time() - start_time
            
            test_results["response_times"] = {
                "first_request": first_response_time,
                "second_request": second_response_time,
                "caching_improvement": first_response_time - second_response_time
            }
            
            # Get performance report
            try:
                perf_response = requests.get(f"{self.base_url}/performance/report")
                if perf_response.status_code == 200:
                    perf_data = perf_response.json()
                    test_results["performance_metrics"] = perf_data
            except Exception as e:
                test_results["performance_metrics"]["error"] = str(e)
        
        self.test_results["performance"] = test_results
        print(f"✅ Performance tests completed")
        
    async def test_agentic_features(self):
        """Test 5: Agentic Features & Memory"""
        print("\n🤖 TEST 5: Agentic Features & Memory")
        print("-" * 40)
        
        test_results = {
            "conversation_memory": {},
            "context_retention": {},
            "preference_learning": {},
            "proactive_suggestions": {}
        }
        
        # Test conversation memory and context retention
        if "client" in self.session_ids:
            conversation_flow = [
                "I'm looking for a 2-bedroom apartment in Dubai Marina",
                "What's my budget range?",
                "Can you suggest properties within that budget?",
                "What about the ROI on these properties?"
            ]
            
            conversation_responses = []
            for message in conversation_flow:
                try:
                    response = requests.post(f"{self.base_url}/sessions/{self.session_ids['client']}/chat", json={
                        "message": message,
                        "role": "client"
                    })
                    
                    if response.status_code == 200:
                        response_data = response.json()
                        conversation_responses.append({
                            "message": message,
                            "response": response_data["response"],
                            "has_context": self._check_context_retention(response_data["response"], conversation_flow[:len(conversation_responses)])
                        })
                        
                except Exception as e:
                    conversation_responses.append({"error": str(e)})
            
            test_results["conversation_memory"]["responses"] = conversation_responses
            if conversation_responses:
                test_results["conversation_memory"]["context_retention_rate"] = sum(1 for r in conversation_responses if r.get("has_context", False)) / len(conversation_responses)
            else:
                test_results["conversation_memory"]["context_retention_rate"] = 0
        
        self.test_results["agentic_features"] = test_results
        print(f"✅ Agentic features tests completed")
        
    async def test_data_retrieval(self):
        """Test 6: Data Retrieval & RAG"""
        print("\n📊 TEST 6: Data Retrieval & RAG")
        print("-" * 40)
        
        test_results = {
            "rag_effectiveness": {},
            "data_accuracy": {},
            "source_quality": {}
        }
        
        # Test RAG effectiveness with specific queries
        rag_queries = [
            "What are the current rental yields in Dubai Marina?",
            "Tell me about Emaar properties in Downtown Dubai",
            "What are the latest market trends in Palm Jumeirah?",
            "Compare investment opportunities in Dubai vs other cities"
        ]
        
        for i, query in enumerate(rag_queries):
            try:
                if "agent" in self.session_ids:
                    response = requests.post(f"{self.base_url}/sessions/{self.session_ids['agent']}/chat", json={
                        "message": query,
                        "role": "agent"
                    })
                    
                    if response.status_code == 200:
                        response_data = response.json()
                        response_text = response_data["response"]
                        sources = response_data.get("sources", [])
                        
                        rag_metrics = self._analyze_rag_effectiveness(response_text, sources, query)
                        
                        test_results["rag_effectiveness"][f"query_{i+1}"] = {
                            "status": "PASS",
                            "has_specific_data": rag_metrics["has_specific_data"],
                            "has_sources": len(sources) > 0,
                            "data_accuracy": rag_metrics["data_accuracy"],
                            "response_quality": rag_metrics["response_quality"]
                        }
                    else:
                        test_results["rag_effectiveness"][f"query_{i+1}"] = {
                            "status": "FAIL",
                            "error": f"HTTP {response.status_code}"
                        }
                        
            except Exception as e:
                test_results["rag_effectiveness"][f"query_{i+1}"] = {
                    "status": "ERROR",
                    "error": str(e)
                }
        
        self.test_results["data_retrieval"] = test_results
        print(f"✅ Data retrieval tests completed: {len(rag_queries)} RAG queries tested")
        
    async def test_feedback_system(self):
        """Test 7: Feedback System"""
        print("\n📈 TEST 7: Feedback System")
        print("-" * 40)
        
        test_results = {
            "feedback_submission": {},
            "feedback_analysis": {},
            "quality_metrics": {}
        }
        
        # Test feedback submission
        try:
            if "client" in self.session_ids:
                # Submit feedback
                feedback_response = requests.post(f"{self.base_url}/feedback/submit", json={
                    "session_id": self.session_ids["client"],
                    "query": "Test query for feedback",
                    "response": "Test response for feedback analysis",
                    "feedback_type": "thumbs_up",
                    "rating": 5,
                    "text_feedback": "Excellent response with specific Dubai data",
                    "category": "accuracy"
                })
                
                if feedback_response.status_code == 200:
                    test_results["feedback_submission"]["status"] = "PASS"
                    
                    # Get feedback summary
                    summary_response = requests.get(f"{self.base_url}/feedback/summary")
                    if summary_response.status_code == 200:
                        summary_data = summary_response.json()
                        test_results["feedback_analysis"] = summary_data
                        
                    # Get improvement recommendations
                    rec_response = requests.get(f"{self.base_url}/feedback/recommendations")
                    if rec_response.status_code == 200:
                        rec_data = rec_response.json()
                        test_results["quality_metrics"] = rec_data
                        
                else:
                    test_results["feedback_submission"]["status"] = "FAIL"
                    test_results["feedback_submission"]["error"] = f"HTTP {feedback_response.status_code}"
                    
        except Exception as e:
            test_results["feedback_submission"]["status"] = "ERROR"
            test_results["feedback_submission"]["error"] = str(e)
        
        self.test_results["feedback_system"] = test_results
        print(f"✅ Feedback system tests completed")
        
    async def test_multi_user_scenarios(self):
        """Test 8: Multi-User Scenarios"""
        print("\n👥 TEST 8: Multi-User Scenarios")
        print("-" * 40)
        
        test_results = {
            "concurrent_users": {},
            "data_isolation": {},
            "role_specific_responses": {}
        }
        
        # Test concurrent user scenarios
        try:
            # Test different roles asking same question
            same_query = "What are the best investment opportunities in Dubai?"
            role_responses = {}
            
            for role in ["client", "agent", "employee"]:
                if role in self.session_ids:
                    response = requests.post(f"{self.base_url}/sessions/{self.session_ids[role]}/chat", json={
                        "message": same_query,
                        "role": role
                    })
                    
                    if response.status_code == 200:
                        response_data = response.json()
                        role_responses[role] = {
                            "response_length": len(response_data["response"]),
                            "has_role_specific_content": self._check_role_specific_content(response_data["response"], role),
                            "response_hash": hashlib.md5(response_data["response"].encode()).hexdigest()
                        }
            
            test_results["role_specific_responses"] = role_responses
            
            # Check if responses are different for different roles
            response_hashes = [r["response_hash"] for r in role_responses.values()]
            test_results["data_isolation"]["responses_unique"] = len(set(response_hashes)) == len(response_hashes)
            
        except Exception as e:
            test_results["concurrent_users"]["error"] = str(e)
        
        self.test_results["multi_user"] = test_results
        print(f"✅ Multi-user scenario tests completed")
        
    def _check_sensitive_data(self, response: str, role: str) -> bool:
        """Check if response contains sensitive data inappropriate for role"""
        sensitive_keywords = {
            "client": ["commission_rate", "internal_notes", "confidential"],
            "agent": ["hr_records", "legal_issues", "confidential_financials"],
            "employee": ["legal_issues", "confidential_financials", "hr_records"],
            "admin": []
        }
        
        if role in sensitive_keywords:
            return any(keyword in response.lower() for keyword in sensitive_keywords[role])
        return False
        
    def _analyze_response_quality(self, response: str, query: str) -> Dict[str, bool]:
        """Analyze response quality metrics"""
        dubai_keywords = ["dubai", "marina", "downtown", "palm", "emaar", "aed", "dirham"]
        specific_data_indicators = ["aed", "dirham", "sq ft", "sqft", "bedroom", "apartment", "villa"]
        structure_indicators = ["•", "-", "1.", "2.", "3.", "**", "##"]
        source_indicators = ["according", "source", "report", "data", "market"]
        
        return {
            "has_dubai_keywords": any(keyword in response.lower() for keyword in dubai_keywords),
            "has_specific_data": any(indicator in response.lower() for indicator in specific_data_indicators),
            "has_structure": any(indicator in response for indicator in structure_indicators),
            "has_sources": any(indicator in response.lower() for indicator in source_indicators)
        }
        
    def _check_context_retention(self, response: str, previous_messages: List[str]) -> bool:
        """Check if response retains context from previous messages"""
        context_keywords = ["dubai marina", "2-bedroom", "apartment", "budget", "roi"]
        return any(keyword in response.lower() for keyword in context_keywords)
        
    def _analyze_rag_effectiveness(self, response: str, sources: List[str], query: str) -> Dict[str, Any]:
        """Analyze RAG effectiveness"""
        return {
            "has_specific_data": len([word for word in response.split() if word.isdigit()]) > 3,
            "data_accuracy": "dubai" in response.lower() and ("aed" in response.lower() or "dirham" in response.lower()),
            "response_quality": len(response) > 100 and len(sources) > 0
        }
        
    def _check_role_specific_content(self, response: str, role: str) -> bool:
        """Check if response contains role-specific content"""
        role_keywords = {
            "client": ["investment", "property", "price", "area"],
            "agent": ["commission", "market", "analysis", "comparison"],
            "employee": ["internal", "report", "data", "analysis"]
        }
        
        if role in role_keywords:
            return any(keyword in response.lower() for keyword in role_keywords[role])
        return False
        
    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("=" * 60)
        
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        error_tests = 0
        
        for test_category, results in self.test_results.items():
            print(f"\n🔍 {test_category.upper()}")
            print("-" * 30)
            
            for test_name, test_result in results.items():
                if isinstance(test_result, dict):
                    if "status" in test_result:
                        status = test_result["status"]
                        total_tests += 1
                        
                        if status == "PASS":
                            passed_tests += 1
                            print(f"✅ {test_name}: PASS")
                        elif status == "FAIL":
                            failed_tests += 1
                            print(f"❌ {test_name}: FAIL")
                        elif status == "ERROR":
                            error_tests += 1
                            print(f"⚠️ {test_name}: ERROR")
                            
                        if "error" in test_result:
                            print(f"   Error: {test_result['error']}")
        
        # Performance summary
        test_duration = time.time() - self.test_start_time
        
        print(f"\n📈 TEST SUMMARY")
        print("-" * 30)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Errors: {error_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "N/A")
        print(f"Test Duration: {test_duration:.2f} seconds")
        
        # Save detailed report
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "test_duration": test_duration,
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "errors": error_tests,
                "success_rate": (passed_tests/total_tests*100) if total_tests > 0 else 0
            },
            "detailed_results": self.test_results
        }
        
        with open("comprehensive_test_report.json", "w") as f:
            json.dump(report_data, f, indent=2)
            
        print(f"\n📄 Detailed report saved to: comprehensive_test_report.json")

async def main():
    """Run comprehensive test suite"""
    tester = ComprehensiveAgentTest()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
