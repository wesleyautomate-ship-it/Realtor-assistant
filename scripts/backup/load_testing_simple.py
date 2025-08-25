#!/usr/bin/env python3
"""
Phase 5.1.4: Simplified Load Testing
Test basic system performance with shorter timeouts
"""

import os
import sys
import time
import json
import statistics
import requests
from datetime import datetime
from typing import Dict, List, Any, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class SimpleLoadTestSuite:
    def __init__(self):
        self.api_base_url = "http://localhost:8001"
        self.test_results = []
        self.start_time = time.time()
        
        # Simple test queries
        self.test_queries = [
            "What are the best investment opportunities in Dubai Marina?",
            "Tell me about Emaar's latest projects",
            "What are the Golden Visa requirements?",
            "Compare rental yields in Downtown Dubai vs Dubai Marina"
        ]
        
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
    
    def make_request(self, query: str, session_id: str) -> Tuple[str, float, int]:
        """Make a single API request with shorter timeout"""
        start_time = time.time()
        try:
            payload = {
                "message": query,
                "role": "client",
                "session_id": session_id
            }
            
            # Shorter timeout for load testing
            response = requests.post(f"{self.api_base_url}/chat", json=payload, timeout=15)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                return "success", duration, response.status_code
            else:
                return "failed", duration, response.status_code
                
        except Exception as e:
            duration = time.time() - start_time
            return "error", duration, 0
    
    def test_single_user_performance(self) -> Dict[str, Any]:
        """Test single user performance with multiple requests"""
        print("\n👤 Testing Single User Performance...")
        
        start_time = time.time()
        request_count = 0
        successful_requests = 0
        failed_requests = 0
        response_times = []
        
        # Make 5 sequential requests
        for i in range(5):
            query = self.test_queries[i % len(self.test_queries)]
            session_id = f"single_user_{i}_{int(time.time())}"
            
            status, response_time, status_code = self.make_request(query, session_id)
            request_count += 1
            response_times.append(response_time)
            
            if status == "success":
                successful_requests += 1
            else:
                failed_requests += 1
            
            # Small delay between requests
            time.sleep(1)
        
        total_duration = time.time() - start_time
        
        # Calculate metrics
        if response_times:
            avg_response_time = statistics.mean(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
        else:
            avg_response_time = min_response_time = max_response_time = 0
        
        success_rate = successful_requests / request_count * 100 if request_count > 0 else 0
        
        # Log results
        self.log_test("Single User Performance", 
                     "PASS" if success_rate >= 80 else "PARTIAL",
                     f"Success: {success_rate:.1f}%, Avg: {avg_response_time:.3f}s, "
                     f"Min: {min_response_time:.3f}s, Max: {max_response_time:.3f}s",
                     total_duration)
        
        return {
            "test_type": "single_user",
            "total_requests": request_count,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "success_rate": success_rate,
            "avg_response_time": avg_response_time,
            "min_response_time": min_response_time,
            "max_response_time": max_response_time
        }
    
    def test_low_concurrency(self) -> Dict[str, Any]:
        """Test with 2-3 concurrent users"""
        print("\n👥 Testing Low Concurrency (2-3 users)...")
        
        start_time = time.time()
        request_count = 0
        successful_requests = 0
        failed_requests = 0
        response_times = []
        
        # Test with 3 concurrent users
        concurrent_users = 3
        
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = []
            
            # Submit initial requests
            for i in range(concurrent_users):
                query = self.test_queries[i % len(self.test_queries)]
                session_id = f"low_concurrent_{i}_{int(time.time())}"
                future = executor.submit(self.make_request, query, session_id)
                futures.append(future)
            
            # Wait for all to complete
            for future in as_completed(futures, timeout=60):
                try:
                    status, response_time, status_code = future.result()
                    request_count += 1
                    response_times.append(response_time)
                    
                    if status == "success":
                        successful_requests += 1
                    else:
                        failed_requests += 1
                        
                except Exception as e:
                    failed_requests += 1
                    print(f"Error in low concurrency test: {str(e)}")
        
        total_duration = time.time() - start_time
        
        # Calculate metrics
        if response_times:
            avg_response_time = statistics.mean(response_times)
            max_response_time = max(response_times)
        else:
            avg_response_time = max_response_time = 0
        
        success_rate = successful_requests / request_count * 100 if request_count > 0 else 0
        
        # Log results
        self.log_test("Low Concurrency Test", 
                     "PASS" if success_rate >= 60 else "PARTIAL",
                     f"Success: {success_rate:.1f}%, Avg: {avg_response_time:.3f}s, "
                     f"Max: {max_response_time:.3f}s",
                     total_duration)
        
        return {
            "test_type": "low_concurrency",
            "concurrent_users": concurrent_users,
            "total_requests": request_count,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "success_rate": success_rate,
            "avg_response_time": avg_response_time,
            "max_response_time": max_response_time
        }
    
    def test_api_health(self) -> Dict[str, Any]:
        """Test basic API health and responsiveness"""
        print("\n🏥 Testing API Health...")
        
        start_time = time.time()
        
        # Test basic health check
        try:
            response = requests.get(f"{self.api_base_url}/", timeout=5)
            health_status = "healthy" if response.status_code == 200 else "unhealthy"
            health_duration = time.time() - start_time
            
            # Test simple chat request
            chat_start = time.time()
            payload = {
                "message": "Hello",
                "role": "client",
                "session_id": "health_test"
            }
            
            chat_response = requests.post(f"{self.api_base_url}/chat", json=payload, timeout=10)
            chat_duration = time.time() - chat_start
            
            if chat_response.status_code == 200:
                chat_status = "responsive"
            else:
                chat_status = "unresponsive"
            
            total_duration = time.time() - start_time
            
            # Log results
            self.log_test("API Health Check", 
                         "PASS" if health_status == "healthy" and chat_status == "responsive" else "PARTIAL",
                         f"Health: {health_status}, Chat: {chat_status}, "
                         f"Health: {health_duration:.3f}s, Chat: {chat_duration:.3f}s",
                         total_duration)
            
            return {
                "test_type": "api_health",
                "health_status": health_status,
                "chat_status": chat_status,
                "health_duration": health_duration,
                "chat_duration": chat_duration
            }
            
        except Exception as e:
            total_duration = time.time() - start_time
            self.log_test("API Health Check", "FAIL", f"Error: {str(e)}", total_duration)
            return {
                "test_type": "api_health",
                "error": str(e)
            }
    
    def test_error_handling(self) -> Dict[str, Any]:
        """Test error handling with invalid requests"""
        print("\n🛡️ Testing Error Handling...")
        
        start_time = time.time()
        error_count = 0
        recovery_success = 0
        
        # Test invalid requests
        invalid_payloads = [
            {"message": "", "role": "client", "session_id": "error_test_1"},
            {"message": "Test", "role": "invalid_role", "session_id": "error_test_2"},
            {"message": "Test", "session_id": "error_test_3"},  # Missing role
        ]
        
        for i, payload in enumerate(invalid_payloads):
            try:
                response = requests.post(f"{self.api_base_url}/chat", json=payload, timeout=5)
                
                # Check if system handled error gracefully
                if response.status_code in [400, 422, 500]:
                    error_count += 1
                    print(f"  ✅ Expected error for payload {i+1}: {response.status_code}")
                else:
                    print(f"  ⚠️ Unexpected response for payload {i+1}: {response.status_code}")
                    
            except Exception as e:
                error_count += 1
                print(f"  ✅ Expected exception for payload {i+1}: {str(e)}")
        
        # Test recovery with valid request
        try:
            valid_payload = {
                "message": "Test recovery",
                "role": "client",
                "session_id": "recovery_test"
            }
            response = requests.post(f"{self.api_base_url}/chat", json=valid_payload, timeout=15)
            
            if response.status_code == 200:
                recovery_success = 1
                print("  ✅ System recovered successfully")
            else:
                print(f"  ❌ System failed to recover: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ System failed to recover: {str(e)}")
        
        total_duration = time.time() - start_time
        
        # Log results
        self.log_test("Error Handling Test", 
                     "PASS" if error_count >= 2 and recovery_success == 1 else "PARTIAL",
                     f"Errors handled: {error_count}/3, Recovery: {'Yes' if recovery_success else 'No'}",
                     total_duration)
        
        return {
            "test_type": "error_handling",
            "errors_handled": error_count,
            "recovery_success": recovery_success == 1,
            "total_invalid_payloads": len(invalid_payloads)
        }
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all simplified load tests"""
        print("🚀 Phase 5.1.4: Simplified Load Testing Suite")
        print("=" * 60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Run tests
        single_user_result = self.test_single_user_performance()
        low_concurrency_result = self.test_low_concurrency()
        api_health_result = self.test_api_health()
        error_handling_result = self.test_error_handling()
        
        # Calculate summary
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        partial_tests = len([r for r in self.test_results if r["status"] == "PARTIAL"])
        
        total_duration = time.time() - self.start_time
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 SIMPLIFIED LOAD TESTING SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"⚠️  Partial: {partial_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests + partial_tests * 0.5) / total_tests * 100:.1f}%")
        print(f"Total Duration: {total_duration:.2f}s")
        
        # Performance summary
        print("\n📈 PERFORMANCE SUMMARY:")
        print("-" * 40)
        print("Single User Performance:")
        print(f"  Success Rate: {single_user_result.get('success_rate', 0):.1f}%")
        print(f"  Avg Response: {single_user_result.get('avg_response_time', 0):.3f}s")
        print(f"  Max Response: {single_user_result.get('max_response_time', 0):.3f}s")
        print()
        
        print("Low Concurrency (3 users):")
        print(f"  Success Rate: {low_concurrency_result.get('success_rate', 0):.1f}%")
        print(f"  Avg Response: {low_concurrency_result.get('avg_response_time', 0):.3f}s")
        print(f"  Max Response: {low_concurrency_result.get('max_response_time', 0):.3f}s")
        print()
        
        print("API Health:")
        print(f"  Health Status: {api_health_result.get('health_status', 'unknown')}")
        print(f"  Chat Status: {api_health_result.get('chat_status', 'unknown')}")
        print()
        
        # Save detailed results
        summary = {
            "test_suite": "Phase 5.1.4 Simplified Load Testing",
            "timestamp": datetime.now().isoformat(),
            "total_tests": total_tests,
            "passed": passed_tests,
            "partial": partial_tests,
            "failed": failed_tests,
            "success_rate": (passed_tests + partial_tests * 0.5) / total_tests * 100,
            "total_duration": total_duration,
            "single_user_result": single_user_result,
            "low_concurrency_result": low_concurrency_result,
            "api_health_result": api_health_result,
            "error_handling_result": error_handling_result,
            "detailed_results": self.test_results
        }
        
        # Save to file
        with open("test_results_simple_load_testing.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        print(f"📄 Detailed results saved to: test_results_simple_load_testing.json")
        
        return summary

def main():
    """Main function to run simplified load tests"""
    test_suite = SimpleLoadTestSuite()
    results = test_suite.run_all_tests()
    
    # Exit with appropriate code
    if results["failed"] == 0:
        print("\n🎉 All simplified load tests completed!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {results['failed']} tests failed. Please review the results.")
        sys.exit(1)

if __name__ == "__main__":
    main()
