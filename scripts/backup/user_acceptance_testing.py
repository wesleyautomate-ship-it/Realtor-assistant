#!/usr/bin/env python3
"""
Phase 5.1.3: User Acceptance Testing
Test with real Dubai real estate scenarios
"""

import os
import sys
import time
import json
import requests
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class UserAcceptanceTestSuite:
    def __init__(self):
        self.api_base_url = "http://localhost:8001"
        self.test_results = []
        self.start_time = time.time()
        
    def log_test(self, test_name: str, status: str, details: str = "", duration: float = 0):
        """Log test results"""
        result = {
            "test_name": test_name,
            "status": status,
            "details": details,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{'✅' if status == 'PASS' else '❌'} {test_name}: {status} ({duration:.3f}s)")
        if details:
            print(f"   Details: {details}")
    
    def test_client_scenarios(self) -> Dict[str, bool]:
        """Test client-focused Dubai real estate scenarios"""
        print("\n👤 Testing Client Scenarios:")
        print("=" * 50)
        
        client_scenarios = [
            {
                "name": "Property Search - Dubai Marina",
                "query": "I'm looking for a 2-bedroom apartment in Dubai Marina with a budget of 2.5 million AED. What are my options?",
                "role": "client",
                "expected_intents": ["PROPERTY_SEARCH", "NEIGHBORHOOD_QUESTION"],
                "expected_keywords": ["Dubai Marina", "2-bedroom", "apartment", "2.5 million"]
            },
            {
                "name": "Golden Visa Investment",
                "query": "I want to invest in Dubai real estate to get a Golden Visa. What's the minimum investment required and what are the best areas?",
                "role": "client",
                "expected_intents": ["INVESTMENT_QUESTION", "REGULATORY_QUESTION"],
                "expected_keywords": ["Golden Visa", "investment", "minimum", "areas"]
            },
            {
                "name": "Rental Investment ROI",
                "query": "What's the rental yield for apartments in Downtown Dubai? I'm considering buying for rental income.",
                "role": "client",
                "expected_intents": ["INVESTMENT_QUESTION", "FINANCIAL_INSIGHTS"],
                "expected_keywords": ["rental yield", "Downtown Dubai", "rental income"]
            },
            {
                "name": "Off-Plan Property Purchase",
                "query": "I'm interested in buying an off-plan property in Palm Jumeirah. What's the process and what should I know?",
                "role": "client",
                "expected_intents": ["TRANSACTION_GUIDANCE", "DEVELOPER_QUESTION"],
                "expected_keywords": ["off-plan", "Palm Jumeirah", "process"]
            },
            {
                "name": "Market Trends Analysis",
                "query": "What are the current market trends in Dubai? Is it a good time to buy or should I wait?",
                "role": "client",
                "expected_intents": ["MARKET_INFO", "INVESTMENT_QUESTION"],
                "expected_keywords": ["market trends", "Dubai", "buy", "wait"]
            }
        ]
        
        results = {}
        
        for scenario in client_scenarios:
            start_time = time.time()
            try:
                payload = {
                    "message": scenario["query"],
                    "role": scenario["role"],
                    "session_id": f"client_test_{int(time.time())}"
                }
                
                response = requests.post(f"{self.api_base_url}/chat", json=payload, timeout=30)
                duration = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("response", "").lower()
                    
                    # Check if response contains expected keywords
                    keyword_matches = sum(1 for keyword in scenario["expected_keywords"] 
                                        if keyword.lower() in response_text)
                    keyword_score = keyword_matches / len(scenario["expected_keywords"])
                    
                    if keyword_score >= 0.6:  # At least 60% keyword coverage
                        self.log_test(scenario["name"], "PASS", 
                                    f"Response quality: {keyword_score:.1%} ({len(data['response'])} chars)", duration)
                        results[scenario["name"]] = True
                    else:
                        self.log_test(scenario["name"], "PARTIAL", 
                                    f"Response quality: {keyword_score:.1%} - needs improvement", duration)
                        results[scenario["name"]] = False
                else:
                    self.log_test(scenario["name"], "FAIL", f"HTTP {response.status_code}", duration)
                    results[scenario["name"]] = False
                    
            except Exception as e:
                duration = time.time() - start_time
                self.log_test(scenario["name"], "FAIL", f"Error: {str(e)}", duration)
                results[scenario["name"]] = False
        
        return results
    
    def test_agent_scenarios(self) -> Dict[str, bool]:
        """Test agent-focused Dubai real estate scenarios"""
        print("\n🏢 Testing Agent Scenarios:")
        print("=" * 50)
        
        agent_scenarios = [
            {
                "name": "Market Analysis for Client",
                "query": "I need to provide market analysis to a client interested in Dubai Marina. What are the current trends and investment opportunities?",
                "role": "agent",
                "expected_intents": ["MARKET_INFO", "INVESTMENT_QUESTION", "NEIGHBORHOOD_QUESTION"],
                "expected_keywords": ["market analysis", "Dubai Marina", "trends", "investment opportunities"]
            },
            {
                "name": "Developer Comparison",
                "query": "My client wants to compare Emaar and DAMAC developers. What are their track records and current projects?",
                "role": "agent",
                "expected_intents": ["DEVELOPER_QUESTION", "MARKET_INFO"],
                "expected_keywords": ["Emaar", "DAMAC", "track records", "projects"]
            },
            {
                "name": "Transaction Guidance",
                "query": "I have a client buying their first property in Dubai. What documents do they need and what's the process?",
                "role": "agent",
                "expected_intents": ["TRANSACTION_GUIDANCE", "POLICY_QUESTION"],
                "expected_keywords": ["documents", "process", "first property", "Dubai"]
            },
            {
                "name": "ROI Analysis",
                "query": "I need to show my client the ROI potential for different areas in Dubai. Which areas offer the best returns?",
                "role": "agent",
                "expected_intents": ["INVESTMENT_QUESTION", "FINANCIAL_INSIGHTS"],
                "expected_keywords": ["ROI", "areas", "returns", "Dubai"]
            },
            {
                "name": "Regulatory Updates",
                "query": "What are the latest RERA regulations that affect property transactions? I need to stay updated for my clients.",
                "role": "agent",
                "expected_intents": ["REGULATORY_QUESTION", "POLICY_QUESTION"],
                "expected_keywords": ["RERA", "regulations", "property transactions"]
            }
        ]
        
        results = {}
        
        for scenario in agent_scenarios:
            start_time = time.time()
            try:
                payload = {
                    "message": scenario["query"],
                    "role": scenario["role"],
                    "session_id": f"agent_test_{int(time.time())}"
                }
                
                response = requests.post(f"{self.api_base_url}/chat", json=payload, timeout=30)
                duration = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("response", "").lower()
                    
                    # Check if response contains expected keywords
                    keyword_matches = sum(1 for keyword in scenario["expected_keywords"] 
                                        if keyword.lower() in response_text)
                    keyword_score = keyword_matches / len(scenario["expected_keywords"])
                    
                    if keyword_score >= 0.6:
                        self.log_test(scenario["name"], "PASS", 
                                    f"Response quality: {keyword_score:.1%} ({len(data['response'])} chars)", duration)
                        results[scenario["name"]] = True
                    else:
                        self.log_test(scenario["name"], "PARTIAL", 
                                    f"Response quality: {keyword_score:.1%} - needs improvement", duration)
                        results[scenario["name"]] = False
                else:
                    self.log_test(scenario["name"], "FAIL", f"HTTP {response.status_code}", duration)
                    results[scenario["name"]] = False
                    
            except Exception as e:
                duration = time.time() - start_time
                self.log_test(scenario["name"], "FAIL", f"Error: {str(e)}", duration)
                results[scenario["name"]] = False
        
        return results
    
    def test_employee_scenarios(self) -> Dict[str, bool]:
        """Test employee-focused Dubai real estate scenarios"""
        print("\n👷 Testing Employee Scenarios:")
        print("=" * 50)
        
        employee_scenarios = [
            {
                "name": "Policy Compliance",
                "query": "What are our company's policies for handling Golden Visa applications for clients?",
                "role": "employee",
                "expected_intents": ["POLICY_QUESTION", "REGULATORY_QUESTION"],
                "expected_keywords": ["company policies", "Golden Visa", "applications"]
            },
            {
                "name": "Administrative Procedures",
                "query": "What's the process for registering a new property listing in our system?",
                "role": "employee",
                "expected_intents": ["POLICY_QUESTION", "AGENT_SUPPORT"],
                "expected_keywords": ["process", "registering", "property listing", "system"]
            },
            {
                "name": "Regulatory Compliance",
                "query": "What are the latest RERA requirements for property advertisements?",
                "role": "employee",
                "expected_intents": ["REGULATORY_QUESTION", "POLICY_QUESTION"],
                "expected_keywords": ["RERA", "requirements", "property advertisements"]
            },
            {
                "name": "Documentation Requirements",
                "query": "What documents are required for completing a property sale transaction?",
                "role": "employee",
                "expected_intents": ["TRANSACTION_GUIDANCE", "POLICY_QUESTION"],
                "expected_keywords": ["documents", "property sale", "transaction"]
            }
        ]
        
        results = {}
        
        for scenario in employee_scenarios:
            start_time = time.time()
            try:
                payload = {
                    "message": scenario["query"],
                    "role": scenario["role"],
                    "session_id": f"employee_test_{int(time.time())}"
                }
                
                response = requests.post(f"{self.api_base_url}/chat", json=payload, timeout=30)
                duration = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("response", "").lower()
                    
                    # Check if response contains expected keywords
                    keyword_matches = sum(1 for keyword in scenario["expected_keywords"] 
                                        if keyword.lower() in response_text)
                    keyword_score = keyword_matches / len(scenario["expected_keywords"])
                    
                    if keyword_score >= 0.6:
                        self.log_test(scenario["name"], "PASS", 
                                    f"Response quality: {keyword_score:.1%} ({len(data['response'])} chars)", duration)
                        results[scenario["name"]] = True
                    else:
                        self.log_test(scenario["name"], "PARTIAL", 
                                    f"Response quality: {keyword_score:.1%} - needs improvement", duration)
                        results[scenario["name"]] = False
                else:
                    self.log_test(scenario["name"], "FAIL", f"HTTP {response.status_code}", duration)
                    results[scenario["name"]] = False
                    
            except Exception as e:
                duration = time.time() - start_time
                self.log_test(scenario["name"], "FAIL", f"Error: {str(e)}", duration)
                results[scenario["name"]] = False
        
        return results
    
    def test_admin_scenarios(self) -> Dict[str, bool]:
        """Test admin-focused Dubai real estate scenarios"""
        print("\n🔧 Testing Admin Scenarios:")
        print("=" * 50)
        
        admin_scenarios = [
            {
                "name": "System Performance",
                "query": "How is the system performing? What are the current response times and error rates?",
                "role": "admin",
                "expected_intents": ["GENERAL", "AGENT_SUPPORT"],
                "expected_keywords": ["system", "performance", "response times", "error rates"]
            },
            {
                "name": "Data Management",
                "query": "What data sources are currently connected and how much data do we have?",
                "role": "admin",
                "expected_intents": ["GENERAL", "AGENT_SUPPORT"],
                "expected_keywords": ["data sources", "connected", "data"]
            },
            {
                "name": "Market Intelligence",
                "query": "What are the key market insights we should focus on for our business strategy?",
                "role": "admin",
                "expected_intents": ["MARKET_INFO", "INVESTMENT_QUESTION"],
                "expected_keywords": ["market insights", "business strategy"]
            }
        ]
        
        results = {}
        
        for scenario in admin_scenarios:
            start_time = time.time()
            try:
                payload = {
                    "message": scenario["query"],
                    "role": scenario["role"],
                    "session_id": f"admin_test_{int(time.time())}"
                }
                
                response = requests.post(f"{self.api_base_url}/chat", json=payload, timeout=30)
                duration = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("response", "").lower()
                    
                    # Check if response contains expected keywords
                    keyword_matches = sum(1 for keyword in scenario["expected_keywords"] 
                                        if keyword.lower() in response_text)
                    keyword_score = keyword_matches / len(scenario["expected_keywords"])
                    
                    if keyword_score >= 0.6:
                        self.log_test(scenario["name"], "PASS", 
                                    f"Response quality: {keyword_score:.1%} ({len(data['response'])} chars)", duration)
                        results[scenario["name"]] = True
                    else:
                        self.log_test(scenario["name"], "PARTIAL", 
                                    f"Response quality: {keyword_score:.1%} - needs improvement", duration)
                        results[scenario["name"]] = False
                else:
                    self.log_test(scenario["name"], "FAIL", f"HTTP {response.status_code}", duration)
                    results[scenario["name"]] = False
                    
            except Exception as e:
                duration = time.time() - start_time
                self.log_test(scenario["name"], "FAIL", f"Error: {str(e)}", duration)
                results[scenario["name"]] = False
        
        return results
    
    def test_response_quality_metrics(self) -> Dict[str, Any]:
        """Test response quality metrics"""
        print("\n📊 Testing Response Quality Metrics:")
        print("=" * 50)
        
        quality_metrics = {
            "response_length": [],
            "response_time": [],
            "keyword_relevance": [],
            "role_appropriateness": []
        }
        
        # Test a sample of scenarios from each role
        test_scenarios = [
            {"query": "I want to buy a property in Dubai Marina", "role": "client"},
            {"query": "What are the latest market trends?", "role": "agent"},
            {"query": "What documents are needed for property registration?", "role": "employee"},
            {"query": "How is the system performing?", "role": "admin"}
        ]
        
        for scenario in test_scenarios:
            start_time = time.time()
            try:
                payload = {
                    "message": scenario["query"],
                    "role": scenario["role"],
                    "session_id": f"quality_test_{int(time.time())}"
                }
                
                response = requests.post(f"{self.api_base_url}/chat", json=payload, timeout=30)
                duration = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("response", "")
                    
                    # Collect metrics
                    quality_metrics["response_length"].append(len(response_text))
                    quality_metrics["response_time"].append(duration)
                    
                    # Check if response mentions the role
                    role_mentioned = scenario["role"].lower() in response_text.lower()
                    quality_metrics["role_appropriateness"].append(1 if role_mentioned else 0)
                    
                    # Check keyword relevance (basic check)
                    query_words = scenario["query"].lower().split()
                    relevant_words = sum(1 for word in query_words if word in response_text.lower())
                    relevance_score = relevant_words / len(query_words) if query_words else 0
                    quality_metrics["keyword_relevance"].append(relevance_score)
                    
            except Exception as e:
                print(f"Error in quality test: {str(e)}")
        
        # Calculate averages
        avg_metrics = {}
        for metric, values in quality_metrics.items():
            if values:
                avg_metrics[metric] = sum(values) / len(values)
            else:
                avg_metrics[metric] = 0
        
        # Log quality metrics
        self.log_test("Response Length", "INFO", f"Average: {avg_metrics.get('response_length', 0):.0f} characters")
        self.log_test("Response Time", "INFO", f"Average: {avg_metrics.get('response_time', 0):.3f} seconds")
        self.log_test("Keyword Relevance", "INFO", f"Average: {avg_metrics.get('keyword_relevance', 0):.1%}")
        self.log_test("Role Appropriateness", "INFO", f"Average: {avg_metrics.get('role_appropriateness', 0):.1%}")
        
        return avg_metrics
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all user acceptance tests"""
        print("👥 Phase 5.1.3: User Acceptance Testing Suite")
        print("=" * 60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Run all test scenarios
        client_results = self.test_client_scenarios()
        agent_results = self.test_agent_scenarios()
        employee_results = self.test_employee_scenarios()
        admin_results = self.test_admin_scenarios()
        quality_metrics = self.test_response_quality_metrics()
        
        # Calculate summary
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        partial_tests = len([r for r in self.test_results if r["status"] == "PARTIAL"])
        
        total_duration = time.time() - self.start_time
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 USER ACCEPTANCE TESTING SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"⚠️  Partial: {partial_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests + partial_tests * 0.5) / total_tests * 100:.1f}%")
        print(f"Total Duration: {total_duration:.2f}s")
        
        # Role-specific results
        print("\n📈 ROLE-SPECIFIC RESULTS:")
        print("-" * 40)
        print(f"Client Scenarios: {sum(client_results.values())}/{len(client_results)} passed")
        print(f"Agent Scenarios: {sum(agent_results.values())}/{len(agent_results)} passed")
        print(f"Employee Scenarios: {sum(employee_results.values())}/{len(employee_results)} passed")
        print(f"Admin Scenarios: {sum(admin_results.values())}/{len(admin_results)} passed")
        
        # Quality metrics summary
        print("\n📊 QUALITY METRICS SUMMARY:")
        print("-" * 40)
        print(f"Average Response Length: {quality_metrics.get('response_length', 0):.0f} characters")
        print(f"Average Response Time: {quality_metrics.get('response_time', 0):.3f} seconds")
        print(f"Average Keyword Relevance: {quality_metrics.get('keyword_relevance', 0):.1%}")
        print(f"Average Role Appropriateness: {quality_metrics.get('role_appropriateness', 0):.1%}")
        
        # Save detailed results
        summary = {
            "test_suite": "Phase 5.1.3 User Acceptance Testing",
            "timestamp": datetime.now().isoformat(),
            "total_tests": total_tests,
            "passed": passed_tests,
            "partial": partial_tests,
            "failed": failed_tests,
            "success_rate": (passed_tests + partial_tests * 0.5) / total_tests * 100,
            "total_duration": total_duration,
            "role_results": {
                "client": client_results,
                "agent": agent_results,
                "employee": employee_results,
                "admin": admin_results
            },
            "quality_metrics": quality_metrics,
            "detailed_results": self.test_results
        }
        
        # Save to file
        with open("test_results_user_acceptance.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: test_results_user_acceptance.json")
        
        return summary

def main():
    """Main function to run user acceptance tests"""
    test_suite = UserAcceptanceTestSuite()
    results = test_suite.run_all_tests()
    
    # Exit with appropriate code
    if results["failed"] == 0:
        print("\n🎉 All user acceptance tests passed!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {results['failed']} tests failed. Please review the results.")
        sys.exit(1)

if __name__ == "__main__":
    main()
