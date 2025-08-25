#!/usr/bin/env python3
"""
Comprehensive RAG System Test Script
Tests the enhanced RAG system with specific scenarios to validate response quality
"""

import requests
import json
import time
from typing import Dict, List

class RAGSystemTester:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.test_results = []
    
    def test_query(self, query: str, expected_indicators: List[str], test_name: str) -> Dict:
        """Test a specific query and validate response quality"""
        print(f"\n{'='*60}")
        print(f"🧪 TESTING: {test_name}")
        print(f"📝 Query: {query}")
        print(f"{'='*60}")
        
        try:
            # Send query to the RAG system
            response = requests.post(
                f"{self.base_url}/chat",
                json={
                    "message": query,
                    "role": "client",
                    "session_id": f"test_session_{int(time.time())}"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('response', '')
                
                print(f"🤖 AI Response:")
                print(f"{ai_response}")
                
                # Analyze response quality
                quality_score = self._analyze_response_quality(ai_response, expected_indicators)
                
                test_result = {
                    'test_name': test_name,
                    'query': query,
                    'response': ai_response,
                    'quality_score': quality_score,
                    'status': 'PASS' if quality_score >= 0.7 else 'FAIL',
                    'issues': self._identify_issues(ai_response, expected_indicators)
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
                'query': query,
                'response': f"Exception: {str(e)}",
                'quality_score': 0.0,
                'status': 'ERROR',
                'issues': [f"Exception: {str(e)}"]
            }
            print(f"❌ Exception: {str(e)}")
        
        self.test_results.append(test_result)
        return test_result
    
    def _analyze_response_quality(self, response: str, expected_indicators: List[str]) -> float:
        """Analyze the quality of the AI response"""
        score = 0.0
        
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
        
        # Check for actionable information
        action_indicators = ['recommend', 'suggest', 'consider', 'contact', 'visit', 'view']
        if any(indicator.lower() in response.lower() for indicator in action_indicators):
            score += 0.1
        
        # Check for source citations
        if 'source' in response.lower() or 'database' in response.lower():
            score += 0.1
        
        # Check for follow-up questions
        if '?' in response:
            score += 0.1
        
        return min(score, 1.0)
    
    def _identify_issues(self, response: str, expected_indicators: List[str]) -> List[str]:
        """Identify specific issues with the response"""
        issues = []
        
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
        
        # Check if response is too short
        if len(response.split()) < 50:
            issues.append("Response is too short and lacks detail")
        
        # Check if no specific data provided
        if not any(char.isdigit() for char in response):
            issues.append("No specific numerical data provided")
        
        return issues
    
    def run_comprehensive_tests(self):
        """Run all comprehensive tests"""
        print("🚀 Starting Comprehensive RAG System Tests")
        print("="*60)
        
        # Test 1: Emirates Hills Query (the problematic one)
        self.test_query(
            query="Find properties with golf course views in Emirates Hills with 4+ bedrooms",
            expected_indicators=['emirates hills', 'golf course', '4+', 'bedroom', 'villa', 'price'],
            test_name="Emirates Hills Golf Course Properties"
        )
        
        # Test 2: Budget-specific query
        self.test_query(
            query="my budget is 10 million villa, ready to move in",
            expected_indicators=['10 million', 'aed', 'villa', 'ready', 'emirates hills', 'price'],
            test_name="10 Million AED Villa Budget"
        )
        
        # Test 3: Specific location and requirements
        self.test_query(
            query="no in Emirates Hills with 4+ bedrooms",
            expected_indicators=['emirates hills', '4+', 'bedroom', 'villa', 'price', 'amenities'],
            test_name="Emirates Hills 4+ Bedrooms"
        )
        
        # Test 4: Market analysis
        self.test_query(
            query="Show me the latest market trends and rental yields for Q4 2024",
            expected_indicators=['market', 'trend', 'rental', 'yield', 'q4', '2024', 'percentage'],
            test_name="Market Trends Q4 2024"
        )
        
        # Test 5: Developer information
        self.test_query(
            query="What are the best developers in Dubai for luxury properties?",
            expected_indicators=['emaar', 'damac', 'nakheel', 'developer', 'luxury', 'reputation'],
            test_name="Best Developers for Luxury Properties"
        )
        
        # Test 6: Neighborhood comparison
        self.test_query(
            query="Compare Dubai Marina vs Downtown Dubai for investment",
            expected_indicators=['dubai marina', 'downtown', 'compare', 'investment', 'roi', 'price'],
            test_name="Dubai Marina vs Downtown Comparison"
        )
        
        # Test 7: Property search with specific criteria
        self.test_query(
            query="Find me luxury apartments in Dubai Marina under 3 million AED",
            expected_indicators=['dubai marina', 'luxury', 'apartment', '3 million', 'aed', 'price'],
            test_name="Luxury Apartments Dubai Marina Under 3M AED"
        )
        
        # Test 8: Legal requirements
        self.test_query(
            query="What are the legal requirements for foreign property buyers in Dubai?",
            expected_indicators=['legal', 'foreign', 'buyer', 'requirement', 'rera', 'dld'],
            test_name="Legal Requirements for Foreign Buyers"
        )
        
        # Test 9: Transaction data
        self.test_query(
            query="Show me recent transactions in Dubai Marina with prices above 2 million AED",
            expected_indicators=['transaction', 'dubai marina', '2 million', 'aed', 'recent', 'price'],
            test_name="Recent Transactions Dubai Marina"
        )
        
        # Test 10: Neighborhood amenities
        self.test_query(
            query="Compare amenities and lifestyle between Dubai Marina and Downtown Dubai",
            expected_indicators=['amenities', 'lifestyle', 'dubai marina', 'downtown', 'compare'],
            test_name="Amenities Comparison Dubai Marina vs Downtown"
        )
        
        self.print_summary()
    
    def print_summary(self):
        """Print comprehensive test summary"""
        print(f"\n{'='*60}")
        print("📊 COMPREHENSIVE TEST SUMMARY")
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
        
        print(f"\n🔍 DETAILED RESULTS:")
        for result in self.test_results:
            status_emoji = "✅" if result['status'] == 'PASS' else "❌" if result['status'] == 'FAIL' else "🚨"
            print(f"{status_emoji} {result['test_name']}: {result['quality_score']:.2f}/1.0")
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
    """Main function to run comprehensive tests"""
    tester = RAGSystemTester()
    tester.run_comprehensive_tests()

if __name__ == "__main__":
    main()
