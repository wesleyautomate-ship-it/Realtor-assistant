#!/usr/bin/env python3
"""
Comprehensive system test script for Dubai Real Estate RAG System
"""

import sys
import os
import requests
import json
import time
from typing import Dict, List, Any

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from config.settings import HOST, PORT

class SystemTester:
    def __init__(self):
        self.base_url = f"http://{HOST}:{PORT}"
        self.session_id = f"test_session_{int(time.time())}"
        self.test_results = []
    
    def run_all_tests(self):
        """Run all system tests"""
        print("🧪 Starting comprehensive system tests...")
        print(f"📍 Testing against: {self.base_url}")
        print("=" * 60)
        
        tests = [
            ("Health Check", self.test_health_check),
            ("Database Connection", self.test_database_connection),
            ("ChromaDB Connection", self.test_chromadb_connection),
            ("Basic Chat", self.test_basic_chat),
            ("Property Search", self.test_property_search),
            ("Market Analysis", self.test_market_analysis),
            ("Role-based Responses", self.test_role_based_responses),
            ("File Upload", self.test_file_upload),
            ("Performance", self.test_performance),
            ("Error Handling", self.test_error_handling)
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            print(f"\n🔍 Running: {test_name}")
            try:
                result = test_func()
                if result:
                    print(f"✅ {test_name}: PASSED")
                    passed += 1
                else:
                    print(f"❌ {test_name}: FAILED")
                    failed += 1
            except Exception as e:
                print(f"❌ {test_name}: ERROR - {e}")
                failed += 1
        
        self.print_summary(passed, failed)
        return passed, failed
    
    def test_health_check(self) -> bool:
        """Test health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            return response.status_code == 200 and "status" in response.json()
        except Exception as e:
            print(f"   Error: {e}")
            return False
    
    def test_database_connection(self) -> bool:
        """Test database connection"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            data = response.json()
            return "database" in data and data["database"] == "connected"
        except Exception as e:
            print(f"   Error: {e}")
            return False
    
    def test_chromadb_connection(self) -> bool:
        """Test ChromaDB connection"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            data = response.json()
            return "chromadb" in data and data["chromadb"] == "connected"
        except Exception as e:
            print(f"   Error: {e}")
            return False
    
    def test_basic_chat(self) -> bool:
        """Test basic chat functionality"""
        try:
            payload = {
                "message": "Hello, I'm looking for properties in Dubai Marina",
                "session_id": self.session_id,
                "role": "client"
            }
            
            response = requests.post(
                f"{self.base_url}/chat",
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"   Status code: {response.status_code}")
                return False
            
            data = response.json()
            return "response" in data and len(data["response"]) > 0
        except Exception as e:
            print(f"   Error: {e}")
            return False
    
    def test_property_search(self) -> bool:
        """Test property search functionality"""
        try:
            payload = {
                "message": "Find me 2-bedroom apartments in Dubai Marina under 3 million AED",
                "session_id": self.session_id,
                "role": "client"
            }
            
            response = requests.post(
                f"{self.base_url}/chat",
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"   Status code: {response.status_code}")
                return False
            
            data = response.json()
            response_text = data.get("response", "").lower()
            
            # Check for property-specific content
            property_indicators = ["dubai marina", "apartment", "bedroom", "aed", "price"]
            return any(indicator in response_text for indicator in property_indicators)
        except Exception as e:
            print(f"   Error: {e}")
            return False
    
    def test_market_analysis(self) -> bool:
        """Test market analysis functionality"""
        try:
            payload = {
                "message": "What are the current market trends in Downtown Dubai?",
                "session_id": self.session_id,
                "role": "agent"
            }
            
            response = requests.post(
                f"{self.base_url}/chat",
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"   Status code: {response.status_code}")
                return False
            
            data = response.json()
            response_text = data.get("response", "").lower()
            
            # Check for market analysis content
            market_indicators = ["market", "trend", "downtown", "dubai", "analysis"]
            return any(indicator in response_text for indicator in market_indicators)
        except Exception as e:
            print(f"   Error: {e}")
            return False
    
    def test_role_based_responses(self) -> bool:
        """Test role-based response functionality"""
        try:
            # Test client role
            client_payload = {
                "message": "I need help finding a property",
                "session_id": f"{self.session_id}_client",
                "role": "client"
            }
            
            client_response = requests.post(
                f"{self.base_url}/chat",
                json=client_payload,
                timeout=30
            )
            
            # Test agent role
            agent_payload = {
                "message": "Show me market analysis tools",
                "session_id": f"{self.session_id}_agent",
                "role": "agent"
            }
            
            agent_response = requests.post(
                f"{self.base_url}/chat",
                json=agent_payload,
                timeout=30
            )
            
            return client_response.status_code == 200 and agent_response.status_code == 200
        except Exception as e:
            print(f"   Error: {e}")
            return False
    
    def test_file_upload(self) -> bool:
        """Test file upload functionality"""
        try:
            # Create a simple test file
            test_content = "This is a test property document for Dubai Marina."
            test_file_path = "test_property.txt"
            
            with open(test_file_path, "w") as f:
                f.write(test_content)
            
            # Test file upload
            with open(test_file_path, "rb") as f:
                files = {"file": f}
                response = requests.post(
                    f"{self.base_url}/upload",
                    files=files,
                    timeout=30
                )
            
            # Clean up
            os.remove(test_file_path)
            
            return response.status_code in [200, 201]
        except Exception as e:
            print(f"   Error: {e}")
            return False
    
    def test_performance(self) -> bool:
        """Test system performance"""
        try:
            start_time = time.time()
            
            payload = {
                "message": "Quick property search test",
                "session_id": f"{self.session_id}_perf",
                "role": "client"
            }
            
            response = requests.post(
                f"{self.base_url}/chat",
                json=payload,
                timeout=30
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            print(f"   Response time: {response_time:.2f} seconds")
            
            # Consider it passed if response time is under 10 seconds
            return response.status_code == 200 and response_time < 10
        except Exception as e:
            print(f"   Error: {e}")
            return False
    
    def test_error_handling(self) -> bool:
        """Test error handling"""
        try:
            # Test with invalid payload
            invalid_payload = {"invalid": "data"}
            
            response = requests.post(
                f"{self.base_url}/chat",
                json=invalid_payload,
                timeout=10
            )
            
            # Should return an error status code
            return response.status_code in [400, 422]
        except Exception as e:
            print(f"   Error: {e}")
            return False
    
    def print_summary(self, passed: int, failed: int):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
        
        if failed == 0:
            print("\n🎉 All tests passed! System is ready for production.")
        else:
            print(f"\n⚠️  {failed} test(s) failed. Please review and fix issues.")

def main():
    """Main test runner"""
    tester = SystemTester()
    passed, failed = tester.run_all_tests()
    
    if failed > 0:
        sys.exit(1)
    else:
        print("\n🚀 System is production-ready!")

if __name__ == "__main__":
    main()
