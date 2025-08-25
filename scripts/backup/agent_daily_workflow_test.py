#!/usr/bin/env python3
"""
Agent Daily Workflow Test Script
Simulates how a real estate agent would interact with the app on a daily basis
Tests all features and analyzes response quality and data retrieval effectiveness
"""

import requests
import json
import time
from typing import Dict, List
from datetime import datetime

class AgentDailyWorkflowTester:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.test_results = []
        self.session_id = f"agent_workflow_{int(time.time())}"
    
    def test_agent_interaction(self, query: str, expected_features: List[str], test_name: str) -> Dict:
        """Test a specific agent interaction"""
        print(f"\n{'='*70}")
        print(f"👨‍💼 AGENT WORKFLOW: {test_name}")
        print(f"📝 Query: {query}")
        print(f"{'='*70}")
        
        try:
            # Send query to the RAG system as an agent
            response = requests.post(
                f"{self.base_url}/chat",
                json={
                    "message": query,
                    "role": "agent",
                    "session_id": self.session_id
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('response', '')
                
                print(f"🤖 AI Response:")
                print(f"{ai_response}")
                
                # Analyze response quality and data retrieval
                analysis = self._analyze_agent_response(ai_response, expected_features, query)
                
                test_result = {
                    'test_name': test_name,
                    'query': query,
                    'response': ai_response,
                    'quality_score': analysis['quality_score'],
                    'data_retrieval_score': analysis['data_retrieval_score'],
                    'value_provided_score': analysis['value_provided_score'],
                    'overall_score': analysis['overall_score'],
                    'status': 'PASS' if analysis['overall_score'] >= 0.7 else 'FAIL',
                    'features_detected': analysis['features_detected'],
                    'issues': analysis['issues'],
                    'data_sources_used': analysis['data_sources_used']
                }
                
                print(f"\n📊 ANALYSIS RESULTS:")
                print(f"   Quality Score: {analysis['quality_score']:.2f}/1.0")
                print(f"   Data Retrieval: {analysis['data_retrieval_score']:.2f}/1.0")
                print(f"   Value Provided: {analysis['value_provided_score']:.2f}/1.0")
                print(f"   Overall Score: {analysis['overall_score']:.2f}/1.0")
                print(f"   Status: {test_result['status']}")
                
                if analysis['features_detected']:
                    print(f"   ✅ Features Detected: {', '.join(analysis['features_detected'])}")
                
                if analysis['data_sources_used']:
                    print(f"   📊 Data Sources: {', '.join(analysis['data_sources_used'])}")
                
                if analysis['issues']:
                    print(f"   ⚠️ Issues: {', '.join(analysis['issues'])}")
                
            else:
                test_result = {
                    'test_name': test_name,
                    'query': query,
                    'response': f"Error: {response.status_code}",
                    'quality_score': 0.0,
                    'data_retrieval_score': 0.0,
                    'value_provided_score': 0.0,
                    'overall_score': 0.0,
                    'status': 'ERROR',
                    'features_detected': [],
                    'issues': [f"HTTP {response.status_code} error"],
                    'data_sources_used': []
                }
                print(f"❌ Error: HTTP {response.status_code}")
                
        except Exception as e:
            test_result = {
                'test_name': test_name,
                'query': query,
                'response': f"Exception: {str(e)}",
                'quality_score': 0.0,
                'data_retrieval_score': 0.0,
                'value_provided_score': 0.0,
                'overall_score': 0.0,
                'status': 'ERROR',
                'features_detected': [],
                'issues': [f"Exception: {str(e)}"],
                'data_sources_used': []
            }
            print(f"❌ Exception: {str(e)}")
        
        self.test_results.append(test_result)
        return test_result
    
    def _analyze_agent_response(self, response: str, expected_features: List[str], query: str) -> Dict:
        """Analyze agent response for quality, data retrieval, and value provided"""
        
        # Quality Score Analysis
        quality_score = 0.0
        word_count = len(response.split())
        
        # Response length appropriateness
        if word_count <= 100:  # Concise
            quality_score += 0.3
        elif word_count <= 200:  # Good length
            quality_score += 0.2
        elif word_count <= 300:  # Acceptable
            quality_score += 0.1
        else:  # Too verbose
            quality_score -= 0.1
        
        # Professional tone
        professional_indicators = ['recommend', 'suggest', 'advise', 'analysis', 'market', 'property']
        if any(indicator in response.lower() for indicator in professional_indicators):
            quality_score += 0.2
        
        # Dubai-specific content
        dubai_indicators = ['dubai', 'aed', 'emirates', 'uae', 'dubai marina', 'downtown', 'rera']
        if any(indicator in response.lower() for indicator in dubai_indicators):
            quality_score += 0.2
        
        # No generic phrases
        generic_phrases = ['this might seem complex', 'don\'t worry', 'let me break it down']
        if not any(phrase in response.lower() for phrase in generic_phrases):
            quality_score += 0.2
        
        quality_score = min(max(quality_score, 0.0), 1.0)
        
        # Data Retrieval Score Analysis
        data_retrieval_score = 0.0
        data_sources_used = []
        
        # Check for specific data indicators
        if any(char.isdigit() for char in response):
            data_retrieval_score += 0.3
            data_sources_used.append('numerical_data')
        
        # Check for property-specific data
        property_indicators = ['bedroom', 'bathroom', 'price', 'location', 'amenities', 'developer']
        if any(indicator in response.lower() for indicator in property_indicators):
            data_retrieval_score += 0.2
            data_sources_used.append('property_data')
        
        # Check for market data
        market_indicators = ['market', 'trend', 'rental', 'yield', 'investment', 'roi']
        if any(indicator in response.lower() for indicator in market_indicators):
            data_retrieval_score += 0.2
            data_sources_used.append('market_data')
        
        # Check for neighborhood data
        neighborhood_indicators = ['neighborhood', 'area', 'community', 'amenities', 'schools']
        if any(indicator in response.lower() for indicator in neighborhood_indicators):
            data_retrieval_score += 0.2
            data_sources_used.append('neighborhood_data')
        
        # Check for legal/regulatory data
        legal_indicators = ['legal', 'regulation', 'rera', 'dld', 'visa', 'freehold']
        if any(indicator in response.lower() for indicator in legal_indicators):
            data_retrieval_score += 0.1
            data_sources_used.append('regulatory_data')
        
        data_retrieval_score = min(data_retrieval_score, 1.0)
        
        # Value Provided Score Analysis
        value_provided_score = 0.0
        features_detected = []
        
        # Check for actionable advice
        action_indicators = ['recommend', 'suggest', 'consider', 'contact', 'visit', 'view']
        if any(indicator in response.lower() for indicator in action_indicators):
            value_provided_score += 0.3
            features_detected.append('actionable_advice')
        
        # Check for specific recommendations
        if 'recommend' in response.lower() or 'suggest' in response.lower():
            value_provided_score += 0.2
            features_detected.append('specific_recommendations')
        
        # Check for market insights
        if any(word in response.lower() for word in ['market', 'trend', 'analysis']):
            value_provided_score += 0.2
            features_detected.append('market_insights')
        
        # Check for client guidance
        guidance_indicators = ['guide', 'help', 'assist', 'support', 'advice']
        if any(indicator in response.lower() for indicator in guidance_indicators):
            value_provided_score += 0.2
            features_detected.append('client_guidance')
        
        # Check for sales support features
        sales_indicators = ['deal', 'close', 'negotiate', 'commission', 'strategy']
        if any(indicator in response.lower() for indicator in sales_indicators):
            value_provided_score += 0.1
            features_detected.append('sales_support')
        
        value_provided_score = min(value_provided_score, 1.0)
        
        # Overall Score
        overall_score = (quality_score * 0.3 + data_retrieval_score * 0.4 + value_provided_score * 0.3)
        
        # Identify issues
        issues = []
        if word_count > 300:
            issues.append("Response too verbose")
        if not any(char.isdigit() for char in response):
            issues.append("No specific data provided")
        if any(phrase in response.lower() for phrase in generic_phrases):
            issues.append("Contains generic phrases")
        if not data_sources_used:
            issues.append("No data sources utilized")
        
        return {
            'quality_score': quality_score,
            'data_retrieval_score': data_retrieval_score,
            'value_provided_score': value_provided_score,
            'overall_score': overall_score,
            'features_detected': features_detected,
            'issues': issues,
            'data_sources_used': data_sources_used
        }
    
    def run_agent_daily_workflow(self):
        """Run comprehensive agent daily workflow tests"""
        print("🚀 STARTING AGENT DAILY WORKFLOW SIMULATION")
        print("="*70)
        print(f"👨‍💼 Simulating Real Estate Agent Daily Tasks")
        print(f"📅 Session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        
        # Agent daily workflow scenarios
        workflow_scenarios = [
            # Morning Routine
            ("Good morning! I need to check today's market updates", 
             ['market_insights', 'data_retrieval'], 
             "Morning Market Check"),
            
            ("Show me the latest property listings in Dubai Marina", 
             ['property_search', 'data_retrieval', 'specific_data'], 
             "Property Listings Search"),
            
            ("What are the current rental yields in Downtown Dubai?", 
             ['market_analysis', 'investment_data', 'specific_data'], 
             "Rental Yield Analysis"),
            
            # Client Interactions
            ("I have a client looking for a 3-bedroom apartment in Dubai Marina under 2 million AED", 
             ['client_support', 'property_search', 'budget_analysis'], 
             "Client Property Search"),
            
            ("My client wants to know about the Golden Visa requirements for property investment", 
             ['legal_guidance', 'regulatory_data', 'client_support'], 
             "Golden Visa Guidance"),
            
            ("How do I explain the benefits of buying vs renting to my client?", 
             ['client_guidance', 'market_insights', 'comparative_analysis'], 
             "Buy vs Rent Analysis"),
            
            # Market Analysis
            ("What are the best investment opportunities in Dubai right now?", 
             ['investment_analysis', 'market_insights', 'specific_recommendations'], 
             "Investment Opportunities"),
            
            ("Show me the market trends for villas in Emirates Hills", 
             ['market_analysis', 'trend_data', 'specific_location'], 
             "Emirates Hills Market Trends"),
            
            ("What's the current state of the off-plan market in Dubai?", 
             ['market_analysis', 'off_plan_data', 'market_insights'], 
             "Off-Plan Market Analysis"),
            
            # Sales Support
            ("How do I handle a difficult client who's hesitant about the price?", 
             ['sales_support', 'negotiation_advice', 'client_guidance'], 
             "Difficult Client Handling"),
            
            ("What are the best sales techniques for luxury properties?", 
             ['sales_support', 'technique_advice', 'luxury_market'], 
             "Luxury Sales Techniques"),
            
            ("How do I close a deal with a foreign investor?", 
             ['sales_support', 'international_client', 'deal_closing'], 
             "Foreign Investor Deal"),
            
            # Property Research
            ("Tell me about the amenities and lifestyle in Dubai Hills Estate", 
             ['neighborhood_analysis', 'lifestyle_data', 'amenities_info'], 
             "Dubai Hills Estate Research"),
            
            ("What are the pros and cons of investing in Palm Jumeirah?", 
             ['investment_analysis', 'pros_cons', 'location_analysis'], 
             "Palm Jumeirah Investment"),
            
            ("Show me recent transactions in Business Bay", 
             ['transaction_data', 'market_analysis', 'specific_location'], 
             "Business Bay Transactions"),
            
            # Legal & Compliance
            ("What are the RERA requirements for property transactions?", 
             ['legal_guidance', 'regulatory_compliance', 'rera_info'], 
             "RERA Requirements"),
            
            ("How do I verify a property's title deed?", 
             ['legal_guidance', 'due_diligence', 'verification_process'], 
             "Title Deed Verification"),
            
            ("What are the tax implications for foreign property buyers?", 
             ['legal_guidance', 'tax_advice', 'foreign_buyer'], 
             "Tax Implications"),
            
            # Developer Information
            ("Tell me about Emaar's latest projects", 
             ['developer_info', 'project_data', 'company_analysis'], 
             "Emaar Projects"),
            
            ("How reliable is DAMAC as a developer?", 
             ['developer_analysis', 'reputation_data', 'reliability_assessment'], 
             "DAMAC Reliability"),
            
            # End of Day
            ("Summarize today's key market insights for my team meeting", 
             ['market_summary', 'insights_compilation', 'team_support'], 
             "Daily Market Summary"),
            
            ("What should I focus on tomorrow based on today's market activity?", 
             ['strategic_planning', 'next_steps', 'priority_guidance'], 
             "Tomorrow's Focus")
        ]
        
        for query, expected_features, test_name in workflow_scenarios:
            self.test_agent_interaction(query, expected_features, test_name)
        
        self.print_comprehensive_analysis()
    
    def print_comprehensive_analysis(self):
        """Print comprehensive analysis of agent workflow test results"""
        print(f"\n{'='*70}")
        print("📊 COMPREHENSIVE AGENT WORKFLOW ANALYSIS")
        print(f"{'='*70}")
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed_tests = len([r for r in self.test_results if r['status'] == 'FAIL'])
        error_tests = len([r for r in self.test_results if r['status'] == 'ERROR'])
        
        avg_quality = sum(r['quality_score'] for r in self.test_results) / total_tests
        avg_data_retrieval = sum(r['data_retrieval_score'] for r in self.test_results) / total_tests
        avg_value = sum(r['value_provided_score'] for r in self.test_results) / total_tests
        avg_overall = sum(r['overall_score'] for r in self.test_results) / total_tests
        
        print(f"📈 TEST SUMMARY:")
        print(f"   Total Tests: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   🚨 Errors: {error_tests}")
        print(f"   📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n📊 SCORE ANALYSIS:")
        print(f"   Quality Score: {avg_quality:.2f}/1.0")
        print(f"   Data Retrieval: {avg_data_retrieval:.2f}/1.0")
        print(f"   Value Provided: {avg_value:.2f}/1.0")
        print(f"   Overall Score: {avg_overall:.2f}/1.0")
        
        # Feature Analysis
        all_features = []
        all_data_sources = []
        for result in self.test_results:
            all_features.extend(result['features_detected'])
            all_data_sources.extend(result['data_sources_used'])
        
        print(f"\n🔧 FEATURES UTILIZED:")
        feature_counts = {}
        for feature in all_features:
            feature_counts[feature] = feature_counts.get(feature, 0) + 1
        
        for feature, count in sorted(feature_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_tests) * 100
            print(f"   • {feature}: {count} times ({percentage:.1f}%)")
        
        print(f"\n📊 DATA SOURCES USED:")
        source_counts = {}
        for source in all_data_sources:
            source_counts[source] = source_counts.get(source, 0) + 1
        
        for source, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_tests) * 100
            print(f"   • {source}: {count} times ({percentage:.1f}%)")
        
        # Value Assessment
        print(f"\n💼 VALUE ASSESSMENT:")
        if avg_overall >= 0.8:
            print("   🎉 EXCELLENT: App provides high value to agents")
        elif avg_overall >= 0.7:
            print("   ✅ GOOD: App provides solid value to agents")
        elif avg_overall >= 0.6:
            print("   ⚠️ FAIR: App provides moderate value to agents")
        else:
            print("   ❌ POOR: App needs significant improvement for agent value")
        
        if avg_data_retrieval >= 0.7:
            print("   📊 STRONG: Effective data retrieval from databases")
        else:
            print("   📊 WEAK: Limited data retrieval from databases")
        
        # Detailed Results
        print(f"\n🔍 DETAILED RESULTS:")
        for result in self.test_results:
            status_emoji = "✅" if result['status'] == 'PASS' else "❌" if result['status'] == 'FAIL' else "🚨"
            print(f"{status_emoji} {result['test_name']}: {result['overall_score']:.2f}/1.0")
            if result['issues']:
                for issue in result['issues']:
                    print(f"   ⚠️ {issue}")
        
        # Common Issues
        all_issues = []
        for result in self.test_results:
            all_issues.extend(result['issues'])
        
        if all_issues:
            print(f"\n🚨 COMMON ISSUES:")
            issue_counts = {}
            for issue in all_issues:
                issue_counts[issue] = issue_counts.get(issue, 0) + 1
            
            for issue, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total_tests) * 100
                print(f"   • {issue}: {count} times ({percentage:.1f}%)")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if avg_data_retrieval < 0.6:
            print("   • Improve data retrieval from comprehensive databases")
        if avg_quality < 0.6:
            print("   • Enhance response quality and conciseness")
        if avg_value < 0.6:
            print("   • Increase actionable value and specific recommendations")
        if len(all_features) < total_tests * 0.5:
            print("   • Expand feature utilization across more scenarios")
        
        print(f"\n🎯 CONCLUSION:")
        if avg_overall >= 0.7 and avg_data_retrieval >= 0.6:
            print("   🚀 The app is READY for agent use and provides significant value!")
        elif avg_overall >= 0.6:
            print("   ⚠️ The app is MOSTLY READY but needs some improvements")
        else:
            print("   🔧 The app needs MAJOR improvements before agent deployment")

def main():
    """Main function to run agent daily workflow tests"""
    tester = AgentDailyWorkflowTester()
    tester.run_agent_daily_workflow()

if __name__ == "__main__":
    main()
