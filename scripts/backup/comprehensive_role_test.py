#!/usr/bin/env python3
"""
Comprehensive Role-Based RAG System Test Script
Tests different user roles with various scenarios including simple queries and property searches
"""

import requests
import json
import time
from typing import Dict, List

class RoleBasedRAGTester:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.test_results = []
    
    def test_query_with_role(self, query: str, role: str, expected_indicators: List[str], test_name: str) -> Dict:
        """Test a specific query with a specific role"""
        print(f"\n{'='*60}")
        print(f"🧪 TESTING: {test_name}")
        print(f"👤 Role: {role}")
        print(f"📝 Query: {query}")
        print(f"{'='*60}")
        
        try:
            # Send query to the RAG system
            response = requests.post(
                f"{self.base_url}/chat",
                json={
                    "message": query,
                    "role": role,
                    "session_id": f"role_test_{role}_{int(time.time())}"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('response', '')
                
                print(f"🤖 AI Response:")
                print(f"{ai_response}")
                
                # Analyze response quality
                quality_score = self._analyze_response_quality(ai_response, expected_indicators, query)
                
                test_result = {
                    'test_name': test_name,
                    'role': role,
                    'query': query,
                    'response': ai_response,
                    'quality_score': quality_score,
                    'status': 'PASS' if quality_score >= 0.6 else 'FAIL',
                    'issues': self._identify_issues(ai_response, expected_indicators, query)
                }
                
                print(f"\n📊 Quality Score: {quality_score:.2f}/1.0")
                print(f"✅ Status: {test_result['status']}")
                
                if test_result['issues']:
                    print(f"⚠️ Issues Found:")
                    for issue in test_result['issues']:
                        print(f"   - {issue}")
                
            else:
                test_result = {
                    'test_name': test_name,
                    'role': role,
                    'query': query,
                    'response': f"Error: {response.status_code}",
                    'quality_score': 0.0,
                    'status': 'ERROR',
                    'issues': [f"HTTP {response.status_code} error"]
                }
                print(f"❌ Error: HTTP {response.status_code}")
                
        except Exception as e:
            test_result = {
                'test_name': test_name,
                'role': role,
                'query': query,
                'response': f"Exception: {str(e)}",
                'quality_score': 0.0,
                'status': 'ERROR',
                'issues': [f"Exception: {str(e)}"]
            }
            print(f"❌ Exception: {str(e)}")
        
        self.test_results.append(test_result)
        return test_result
    
    def _analyze_response_quality(self, response: str, expected_indicators: List[str], query: str) -> float:
        """Analyze the quality of the AI response"""
        score = 0.0
        
        # Check for appropriate response length
        word_count = len(response.split())
        if word_count <= 50:  # Very concise
            score += 0.3
        elif word_count <= 150:  # Good length
            score += 0.2
        elif word_count <= 300:  # Acceptable
            score += 0.1
        else:  # Too verbose
            score -= 0.1
        
        # Check for specific data indicators
        if any(indicator.lower() in response.lower() for indicator in expected_indicators):
            score += 0.3
        
        # Check for Dubai-specific content
        dubai_indicators = ['dubai', 'aed', 'emirates', 'uae', 'dubai marina', 'downtown']
        if any(indicator.lower() in response.lower() for indicator in dubai_indicators):
            score += 0.2
        
        # Check for specific property information
        property_indicators = ['bedroom', 'bathroom', 'price', 'location', 'amenities', 'developer']
        if any(indicator.lower() in response.lower() for indicator in property_indicators):
            score += 0.2
        
        # Check for role-appropriate content
        if 'admin' in query.lower() or 'analytics' in query.lower():
            if any(word in response.lower() for word in ['data', 'analytics', 'metrics', 'performance']):
                score += 0.1
        
        # Check for simple query appropriateness
        if query.lower() in ['hi', 'hello', 'hey']:
            if word_count <= 20 and 'hello' in response.lower():
                score += 0.2
        
        return min(max(score, 0.0), 1.0)
    
    def _identify_issues(self, response: str, expected_indicators: List[str], query: str) -> List[str]:
        """Identify specific issues with the response"""
        issues = []
        
        # Check if response is too verbose for simple queries
        word_count = len(response.split())
        if query.lower() in ['hi', 'hello', 'hey'] and word_count > 30:
            issues.append("Response too verbose for simple greeting")
        
        if word_count > 300:
            issues.append("Response too long and overwhelming")
        
        # Check if response is too generic
        generic_phrases = [
            'this might seem complex',
            'don\'t worry',
            'let me break it down',
            'highly specific',
            'potentially challenging'
        ]
        
        if any(phrase.lower() in response.lower() for phrase in generic_phrases):
            issues.append("Response is too generic and lacks specific data")
        
        # Check if missing expected indicators
        missing_indicators = []
        for indicator in expected_indicators:
            if indicator.lower() not in response.lower():
                missing_indicators.append(indicator)
        
        if missing_indicators:
            issues.append(f"Missing expected indicators: {', '.join(missing_indicators)}")
        
        # Check if no specific data provided for property searches
        if 'property' in query.lower() or 'find' in query.lower():
            if not any(char.isdigit() for char in response):
                issues.append("No specific numerical data provided for property search")
        
        return issues
    
    def run_comprehensive_role_tests(self):
        """Run comprehensive tests with different roles"""
        print("🚀 Starting Comprehensive Role-Based RAG System Tests")
        print("="*60)
        
        # Test scenarios for each role
        test_scenarios = [
            # Simple greetings
            ("hi", "client", [], "Simple Greeting - Client"),
            ("hello", "agent", [], "Simple Greeting - Agent"),
            ("hey", "employee", [], "Simple Greeting - Employee"),
            ("hi there", "admin", [], "Simple Greeting - Admin"),
            
            # Property searches
            ("Find properties with golf course views in Emirates Hills with 4+ bedrooms", "client", 
             ['emirates hills', 'golf course', '4+', 'bedroom', 'villa', 'price'], 
             "Emirates Hills Golf Course Properties - Client"),
            
            ("Show me luxury apartments in Dubai Marina under 3 million AED", "client",
             ['dubai marina', 'luxury', 'apartment', '3 million', 'aed', 'price'],
             "Luxury Apartments Dubai Marina - Client"),
            
            ("Find villas in Emirates Hills with 4+ bedrooms", "agent",
             ['emirates hills', '4+', 'bedroom', 'villa', 'price'],
             "Emirates Hills Villas - Agent"),
            
            # Market analysis
            ("Show me the latest market trends", "client",
             ['market', 'trend', 'dubai'],
             "Market Trends - Client"),
            
            ("What are the current rental yields in Dubai Marina?", "agent",
             ['rental', 'yield', 'dubai marina'],
             "Rental Yields Dubai Marina - Agent"),
            
            # Developer information
            ("Who are the best developers in Dubai?", "client",
             ['developer', 'dubai', 'emaar', 'damac'],
             "Best Developers - Client"),
            
            # Legal requirements
            ("What are the legal requirements for foreign buyers?", "client",
             ['legal', 'foreign', 'buyer', 'requirement'],
             "Legal Requirements - Client"),
            
            # Admin-specific queries
            ("Show me system performance metrics", "admin",
             ['performance', 'metrics', 'data'],
             "System Performance - Admin"),
            
            ("What are the sales analytics for this month?", "admin",
             ['sales', 'analytics', 'month'],
             "Sales Analytics - Admin"),
            
            # Employee-specific queries
            ("How do I process a property transaction?", "employee",
             ['process', 'transaction', 'property'],
             "Property Transaction Process - Employee"),
            
            ("What are the company policies for client meetings?", "employee",
             ['policy', 'client', 'meeting'],
             "Company Policies - Employee"),
            
            # Agent-specific queries
            ("How do I close a deal with a difficult client?", "agent",
             ['close', 'deal', 'client'],
             "Closing Deals - Agent"),
            
            ("What are the best sales techniques for luxury properties?", "agent",
             ['sales', 'technique', 'luxury'],
             "Sales Techniques - Agent"),
            
            # Simple property queries
            ("I am looking for a property", "client",
             ['property', 'dubai'],
             "Simple Property Search - Client"),
            
            ("Show me some properties", "client",
             ['property', 'dubai'],
             "General Property Request - Client"),
        ]
        
        for query, role, expected_indicators, test_name in test_scenarios:
            self.test_query_with_role(query, role, expected_indicators, test_name)
        
        self.print_summary()
    
    def print_summary(self):
        """Print comprehensive test summary"""
        print(f"\n{'='*60}")
        print("📊 COMPREHENSIVE ROLE-BASED TEST SUMMARY")
        print(f"{'='*60}")
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed_tests = len([r for r in self.test_results if r['status'] == 'FAIL'])
        error_tests = len([r for r in self.test_results if r['status'] == 'ERROR'])
        
        avg_quality_score = sum(r['quality_score'] for r in self.test_results) / total_tests
        
        print(f"📈 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"🚨 Errors: {error_tests}")
        print(f"📊 Average Quality Score: {avg_quality_score:.2f}/1.0")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Role-specific analysis
        roles = ['client', 'agent', 'employee', 'admin']
        print(f"\n👥 ROLE-SPECIFIC ANALYSIS:")
        for role in roles:
            role_tests = [r for r in self.test_results if r['role'] == role]
            if role_tests:
                role_avg = sum(r['quality_score'] for r in role_tests) / len(role_tests)
                role_passed = len([r for r in role_tests if r['status'] == 'PASS'])
                print(f"   {role.title()}: {role_passed}/{len(role_tests)} passed, avg score: {role_avg:.2f}")
        
        print(f"\n🔍 DETAILED RESULTS:")
        for result in self.test_results:
            status_emoji = "✅" if result['status'] == 'PASS' else "❌" if result['status'] == 'FAIL' else "🚨"
            print(f"{status_emoji} [{result['role'].upper()}] {result['test_name']}: {result['quality_score']:.2f}/1.0")
            if result['issues']:
                for issue in result['issues']:
                    print(f"   ⚠️ {issue}")
        
        # Identify common issues
        all_issues = []
        for result in self.test_results:
            all_issues.extend(result['issues'])
        
        if all_issues:
            print(f"\n🚨 COMMON ISSUES:")
            issue_counts = {}
            for issue in all_issues:
                issue_counts[issue] = issue_counts.get(issue, 0) + 1
            
            for issue, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"   • {issue} (appeared {count} times)")

def main():
    """Main function to run comprehensive role-based tests"""
    tester = RoleBasedRAGTester()
    tester.run_comprehensive_role_tests()

if __name__ == "__main__":
    main()
