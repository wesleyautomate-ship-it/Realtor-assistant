#!/usr/bin/env python3
"""
Test Script for Improved RAG Service
Demonstrates the improved responses that address conversational tone, data presentation, and information architecture
"""

import requests
import json
import time
from typing import Dict, List

class ImprovedRAGTester:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.session_id = f"improved_test_{int(time.time())}"
    
    def test_improved_response(self, query: str, test_name: str) -> Dict:
        """Test the improved RAG response"""
        print(f"\n{'='*60}")
        print(f"🧪 TESTING IMPROVED RAG: {test_name}")
        print(f"📝 Query: {query}")
        print(f"{'='*60}")
        
        try:
            # Send query to the RAG system
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
                
                # Analyze the response quality
                analysis = self._analyze_improved_response(ai_response, query)
                
                print(f"\n📊 IMPROVEMENT ANALYSIS:")
                print(f"   Conversational Fillers Removed: {'✅' if analysis['no_fillers'] else '❌'}")
                print(f"   Structured Formatting: {'✅' if analysis['structured'] else '❌'}")
                print(f"   Specific Data Presented: {'✅' if analysis['specific_data'] else '❌'}")
                print(f"   Appropriate Length: {'✅' if analysis['appropriate_length'] else '❌'}")
                print(f"   Actionable Next Steps: {'✅' if analysis['actionable_steps'] else '❌'}")
                print(f"   Overall Quality Score: {analysis['quality_score']:.2f}/1.0")
                
                return {
                    'test_name': test_name,
                    'query': query,
                    'response': ai_response,
                    'analysis': analysis
                }
                
            else:
                print(f"❌ Error: HTTP {response.status_code}")
                return {'error': f"HTTP {response.status_code}"}
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            return {'error': str(e)}
    
    def _analyze_improved_response(self, response: str, query: str) -> Dict:
        """Analyze if the response addresses the core issues"""
        
        # Check for conversational fillers
        conversational_fillers = [
            'i understand this might seem complex',
            'don\'t worry',
            'let me break it down for you',
            'this might seem overwhelming',
            'let me explain'
        ]
        no_fillers = not any(filler in response.lower() for filler in conversational_fillers)
        
        # Check for structured formatting
        structured_indicators = [
            '**',  # Bold text
            '•',   # Bullet points
            '##',  # Headers
            '|',   # Tables
            '1.',  # Numbered lists
            '2.',
            '3.'
        ]
        structured = any(indicator in response for indicator in structured_indicators)
        
        # Check for specific data
        specific_data_indicators = [
            'aed', 'dollars', '$', 'price', 'bedroom', 'bathroom',
            '%', 'percent', 'yield', 'roi', 'rental'
        ]
        specific_data = any(indicator in response.lower() for indicator in specific_data_indicators)
        
        # Check for appropriate length
        word_count = len(response.split())
        appropriate_length = 50 <= word_count <= 300
        
        # Check for actionable next steps
        actionable_indicators = [
            'next steps', 'next:', 'action items', 'recommendations',
            'suggest', 'consider', 'contact', 'visit', 'view'
        ]
        actionable_steps = any(indicator in response.lower() for indicator in actionable_indicators)
        
        # Calculate overall quality score
        quality_score = 0.0
        if no_fillers:
            quality_score += 0.2
        if structured:
            quality_score += 0.2
        if specific_data:
            quality_score += 0.2
        if appropriate_length:
            quality_score += 0.2
        if actionable_steps:
            quality_score += 0.2
        
        return {
            'no_fillers': no_fillers,
            'structured': structured,
            'specific_data': specific_data,
            'appropriate_length': appropriate_length,
            'actionable_steps': actionable_steps,
            'quality_score': quality_score,
            'word_count': word_count
        }
    
    def run_improvement_tests(self):
        """Run tests to demonstrate improved responses"""
        print("🚀 TESTING IMPROVED RAG RESPONSES")
        print("="*60)
        print("Testing responses that address core issues:")
        print("1. Conversational tone elimination")
        print("2. Structured data presentation")
        print("3. Specific data inclusion")
        print("4. Appropriate response length")
        print("5. Actionable next steps")
        print("="*60)
        
        # Test scenarios that should demonstrate improvements
        test_scenarios = [
            ("Show me recent transactions in Business Bay", "Business Bay Transactions"),
            ("What are the RERA requirements for property transactions?", "RERA Requirements"),
            ("Find properties with golf course views in Emirates Hills with 4+ bedrooms", "Emirates Hills Golf Properties"),
            ("What are the current rental yields in Dubai Marina?", "Dubai Marina Rental Yields"),
            ("Tell me about the amenities and lifestyle in Dubai Hills Estate", "Dubai Hills Estate Amenities"),
            ("How do I verify a property's title deed?", "Title Deed Verification"),
            ("What are the tax implications for foreign property buyers?", "Foreign Buyer Tax Implications"),
            ("Show me luxury apartments in Dubai Marina under 3 million AED", "Luxury Apartments Dubai Marina")
        ]
        
        results = []
        for query, test_name in test_scenarios:
            result = self.test_improved_response(query, test_name)
            results.append(result)
        
        self.print_improvement_summary(results)
    
    def print_improvement_summary(self, results: List[Dict]):
        """Print summary of improvement test results"""
        print(f"\n{'='*60}")
        print("📊 IMPROVEMENT TEST SUMMARY")
        print(f"{'='*60}")
        
        valid_results = [r for r in results if 'error' not in r]
        
        if not valid_results:
            print("❌ No valid test results to analyze")
            return
        
        # Calculate improvement metrics
        total_tests = len(valid_results)
        no_fillers_count = sum(1 for r in valid_results if r['analysis']['no_fillers'])
        structured_count = sum(1 for r in valid_results if r['analysis']['structured'])
        specific_data_count = sum(1 for r in valid_results if r['analysis']['specific_data'])
        appropriate_length_count = sum(1 for r in valid_results if r['analysis']['appropriate_length'])
        actionable_steps_count = sum(1 for r in valid_results if r['analysis']['actionable_steps'])
        
        avg_quality_score = sum(r['analysis']['quality_score'] for r in valid_results) / total_tests
        avg_word_count = sum(r['analysis']['word_count'] for r in valid_results) / total_tests
        
        print(f"📈 IMPROVEMENT METRICS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   No Conversational Fillers: {no_fillers_count}/{total_tests} ({no_fillers_count/total_tests*100:.1f}%)")
        print(f"   Structured Formatting: {structured_count}/{total_tests} ({structured_count/total_tests*100:.1f}%)")
        print(f"   Specific Data Presented: {specific_data_count}/{total_tests} ({specific_data_count/total_tests*100:.1f}%)")
        print(f"   Appropriate Length: {appropriate_length_count}/{total_tests} ({appropriate_length_count/total_tests*100:.1f}%)")
        print(f"   Actionable Next Steps: {actionable_steps_count}/{total_tests} ({actionable_steps_count/total_tests*100:.1f}%)")
        print(f"   Average Quality Score: {avg_quality_score:.2f}/1.0")
        print(f"   Average Word Count: {avg_word_count:.0f} words")
        
        # Overall assessment
        print(f"\n🎯 OVERALL ASSESSMENT:")
        if avg_quality_score >= 0.8:
            print("   🎉 EXCELLENT: Core issues have been successfully addressed!")
        elif avg_quality_score >= 0.6:
            print("   ✅ GOOD: Most core issues have been addressed")
        elif avg_quality_score >= 0.4:
            print("   ⚠️ FAIR: Some core issues remain")
        else:
            print("   ❌ POOR: Core issues still need significant work")
        
        # Specific recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if no_fillers_count < total_tests * 0.8:
            print("   • Continue eliminating conversational fillers")
        if structured_count < total_tests * 0.8:
            print("   • Improve structured formatting implementation")
        if specific_data_count < total_tests * 0.8:
            print("   • Enhance specific data presentation")
        if appropriate_length_count < total_tests * 0.8:
            print("   • Better length control needed")
        if actionable_steps_count < total_tests * 0.8:
            print("   • Add more actionable next steps")
        
        print(f"\n🚀 NEXT STEPS:")
        if avg_quality_score >= 0.8:
            print("   • System is ready for production deployment")
            print("   • Monitor real-world usage for further refinements")
        else:
            print("   • Implement the improved RAG service")
            print("   • Test with real agent workflows")
            print("   • Iterate based on feedback")

def main():
    """Main function to run improvement tests"""
    tester = ImprovedRAGTester()
    tester.run_improvement_tests()

if __name__ == "__main__":
    main()
