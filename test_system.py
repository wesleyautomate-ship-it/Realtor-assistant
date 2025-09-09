#!/usr/bin/env python3
"""
System Testing Script
====================

Automated testing script for the AI-Powered Real Estate Assistant Platform.
"""

import requests
import time
import sys
import json
from datetime import datetime

class SystemTester:
    def __init__(self, base_url="http://localhost:8003"):
        self.base_url = base_url
        self.test_results = []
    
    def log_test(self, test_name, success, message="", response_time=None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "response_time": response_time,
            "timestamp": timestamp
        }
        
        self.test_results.append(result)
        print(f"[{timestamp}] {status} - {test_name}")
        if message:
            print(f"    {message}")
        if response_time:
            print(f"    Response time: {response_time:.3f}s")
        print()
    
    def test_health_endpoint(self):
        """Test basic health endpoint"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/health", timeout=5)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_test("Health Endpoint", True, "Server is healthy", response_time)
                return True
            else:
                self.log_test("Health Endpoint", False, f"Status code: {response.status_code}", response_time)
                return False
        except Exception as e:
            self.log_test("Health Endpoint", False, f"Error: {str(e)}")
            return False
    
    def test_phase3_endpoints(self):
        """Test Phase 3 advanced endpoints"""
        endpoints = [
            "/api/phase3/developer/health",
            "/api/phase3/developer/performance-analytics",
            "/api/phase3/dubai/areas",
            "/api/phase3/dubai/property-types"
        ]
        
        success_count = 0
        for endpoint in endpoints:
            try:
                start_time = time.time()
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    self.log_test(f"Phase 3 - {endpoint}", True, "Endpoint responding", response_time)
                    success_count += 1
                else:
                    self.log_test(f"Phase 3 - {endpoint}", False, f"Status code: {response.status_code}", response_time)
            except Exception as e:
                self.log_test(f"Phase 3 - {endpoint}", False, f"Error: {str(e)}")
        
        return success_count == len(endpoints)
    
    def test_ai_assistant_endpoints(self):
        """Test AI Assistant endpoints"""
        endpoints = [
            "/api/ai-assistant/requests",
            "/api/ai-assistant/experts"
        ]
        
        success_count = 0
        for endpoint in endpoints:
            try:
                start_time = time.time()
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                response_time = time.time() - start_time
                
                if response.status_code in [200, 401, 403]:  # 401/403 are expected for unauthenticated requests
                    self.log_test(f"AI Assistant - {endpoint}", True, "Endpoint responding", response_time)
                    success_count += 1
                else:
                    self.log_test(f"AI Assistant - {endpoint}", False, f"Status code: {response.status_code}", response_time)
            except Exception as e:
                self.log_test(f"AI Assistant - {endpoint}", False, f"Error: {str(e)}")
        
        return success_count == len(endpoints)
    
    def test_team_management_endpoints(self):
        """Test team management endpoints"""
        endpoints = [
            "/api/team/brokerages",
            "/api/team/performance"
        ]
        
        success_count = 0
        for endpoint in endpoints:
            try:
                start_time = time.time()
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                response_time = time.time() - start_time
                
                if response.status_code in [200, 401, 403]:  # 401/403 are expected for unauthenticated requests
                    self.log_test(f"Team Management - {endpoint}", True, "Endpoint responding", response_time)
                    success_count += 1
                else:
                    self.log_test(f"Team Management - {endpoint}", False, f"Status code: {response.status_code}", response_time)
            except Exception as e:
                self.log_test(f"Team Management - {endpoint}", False, f"Error: {str(e)}")
        
        return success_count == len(endpoints)
    
    def test_dubai_data_endpoints(self):
        """Test Dubai data integration endpoints"""
        try:
            # Test market data endpoint with parameters
            start_time = time.time()
            response = requests.get(
                f"{self.base_url}/api/phase3/dubai/market-data",
                params={
                    "area_name": "Dubai Marina",
                    "property_type": "apartment"
                },
                timeout=10
            )
            response_time = time.time() - start_time
            
            if response.status_code in [200, 401, 403]:
                self.log_test("Dubai Market Data", True, "Market data endpoint responding", response_time)
                return True
            else:
                self.log_test("Dubai Market Data", False, f"Status code: {response.status_code}", response_time)
                return False
        except Exception as e:
            self.log_test("Dubai Market Data", False, f"Error: {str(e)}")
            return False
    
    def test_performance(self):
        """Test system performance with concurrent requests"""
        try:
            import concurrent.futures
            import threading
            
            def make_request():
                try:
                    response = requests.get(f"{self.base_url}/health", timeout=5)
                    return response.status_code == 200
                except:
                    return False
            
            # Test with 10 concurrent requests
            start_time = time.time()
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(make_request) for _ in range(10)]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]
            
            response_time = time.time() - start_time
            success_count = sum(results)
            
            if success_count >= 8:  # Allow for some failures
                self.log_test("Performance Test", True, f"{success_count}/10 requests successful", response_time)
                return True
            else:
                self.log_test("Performance Test", False, f"Only {success_count}/10 requests successful", response_time)
                return False
        except Exception as e:
            self.log_test("Performance Test", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("=" * 60)
        print("🚀 AI-POWERED REAL ESTATE ASSISTANT - SYSTEM TESTING")
        print("=" * 60)
        print(f"Testing server at: {self.base_url}")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Run all tests
        tests = [
            ("Health Check", self.test_health_endpoint),
            ("Phase 3 Endpoints", self.test_phase3_endpoints),
            ("AI Assistant Endpoints", self.test_ai_assistant_endpoints),
            ("Team Management Endpoints", self.test_team_management_endpoints),
            ("Dubai Data Integration", self.test_dubai_data_endpoints),
            ("Performance Test", self.test_performance)
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            print(f"🧪 Running {test_name}...")
            try:
                if test_func():
                    passed_tests += 1
            except Exception as e:
                self.log_test(test_name, False, f"Test failed with exception: {str(e)}")
            print()
        
        # Print summary
        print("=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print()
        
        if passed_tests == total_tests:
            print("🎉 ALL TESTS PASSED! System is ready for production.")
            return True
        else:
            print("⚠️ Some tests failed. Please check the issues above.")
            return False
    
    def save_results(self, filename="test_results.json"):
        """Save test results to file"""
        with open(filename, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        print(f"📄 Test results saved to {filename}")

def main():
    """Main function"""
    tester = SystemTester()
    
    try:
        success = tester.run_all_tests()
        tester.save_results()
        
        if success:
            print("\n🚀 System is ready for staging and production!")
            sys.exit(0)
        else:
            print("\n❌ System needs fixes before production deployment.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️ Testing interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Testing failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
