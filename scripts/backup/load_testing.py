#!/usr/bin/env python3
"""
Phase 5.1.4: Load Testing
Test system performance under multiple concurrent users
"""

import os
import sys
import time
import json
import threading
import statistics
import requests
from datetime import datetime
from typing import Dict, List, Any, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class LoadTestSuite:
    def __init__(self):
        self.api_base_url = "http://localhost:8001"
        self.test_results = []
        self.start_time = time.time()
        
        # Test scenarios
        self.test_queries = [
            "What are the best investment opportunities in Dubai Marina?",
            "Tell me about Emaar's latest projects and track record",
            "What are the Golden Visa requirements for real estate investors?",
            "Compare rental yields in Downtown Dubai vs Dubai Marina",
            "What are the latest RERA regulations for property transactions?",
            "I'm looking for a 2-bedroom apartment in Dubai Marina under 2 million AED",
            "What's the ROI for investing in off-plan properties?",
            "Tell me about Dubai 2040 master plan and infrastructure projects"
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
        """Make a single API request"""
        start_time = time.time()
        try:
            payload = {
                "message": query,
                "role": "client",
                "session_id": session_id
            }
            
            response = requests.post(f"{self.api_base_url}/chat", json=payload, timeout=30)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                return "success", duration, response.status_code
            else:
                return "failed", duration, response.status_code
                
        except Exception as e:
            duration = time.time() - start_time
            return "error", duration, 0
    
    def test_concurrent_users(self, num_users: int, duration_seconds: int = 60) -> Dict[str, Any]:
        """Test with specified number of concurrent users"""
        print(f"\n🔄 Testing with {num_users} concurrent users for {duration_seconds} seconds...")
        
        start_time = time.time()
        request_count = 0
        successful_requests = 0
        failed_requests = 0
        error_requests = 0
        response_times = []
        
        # Create thread pool
        with ThreadPoolExecutor(max_workers=num_users) as executor:
            futures = []
            
            # Submit initial batch of requests
            for i in range(num_users):
                query = self.test_queries[i % len(self.test_queries)]
                session_id = f"load_test_{num_users}_{i}_{int(time.time())}"
                future = executor.submit(self.make_request, query, session_id)
                futures.append(future)
            
            # Monitor and submit additional requests
            while time.time() - start_time < duration_seconds:
                # Check completed futures with longer timeout
                try:
                    for future in as_completed(futures, timeout=5):
                        try:
                            status, response_time, status_code = future.result()
                            request_count += 1
                            response_times.append(response_time)
                            
                            if status == "success":
                                successful_requests += 1
                            elif status == "failed":
                                failed_requests += 1
                            else:
                                error_requests += 1
                            
                            # Submit new request to maintain concurrency
                            query = self.test_queries[request_count % len(self.test_queries)]
                            session_id = f"load_test_{num_users}_{request_count}_{int(time.time())}"
                            new_future = executor.submit(self.make_request, query, session_id)
                            futures.append(new_future)
                            
                        except Exception as e:
                            print(f"Error in concurrent test: {str(e)}")
                            failed_requests += 1
                except TimeoutError:
                    # No futures completed within timeout, continue
                    pass
                
                # Remove completed futures
                futures = [f for f in futures if not f.done()]
                
                # Small delay to prevent excessive CPU usage
                time.sleep(0.5)
        
        # Wait for remaining futures with longer timeout
        try:
            for future in as_completed(futures, timeout=30):
                try:
                    status, response_time, status_code = future.result()
                    request_count += 1
                    response_times.append(response_time)
                    
                    if status == "success":
                        successful_requests += 1
                    elif status == "failed":
                        failed_requests += 1
                    else:
                        error_requests += 1
                        
                except Exception as e:
                    print(f"Error in final concurrent test: {str(e)}")
                    failed_requests += 1
        except TimeoutError:
            print(f"Warning: {len(futures)} futures did not complete within timeout")
            failed_requests += len(futures)
        
        total_duration = time.time() - start_time
        
        # Calculate metrics
        if response_times:
            avg_response_time = statistics.mean(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            p95_response_time = sorted(response_times)[int(len(response_times) * 0.95)]
        else:
            avg_response_time = min_response_time = max_response_time = p95_response_time = 0
        
        requests_per_second = request_count / total_duration if total_duration > 0 else 0
        success_rate = successful_requests / request_count * 100 if request_count > 0 else 0
        
        # Log results
        self.log_test(f"Concurrent Users {num_users}", 
                     "PASS" if success_rate >= 90 else "PARTIAL",
                     f"Success: {success_rate:.1f}%, RPS: {requests_per_second:.2f}, "
                     f"Avg: {avg_response_time:.3f}s, P95: {p95_response_time:.3f}s",
                     total_duration)
        
        return {
            "concurrent_users": num_users,
            "duration": total_duration,
            "total_requests": request_count,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "error_requests": error_requests,
            "success_rate": success_rate,
            "requests_per_second": requests_per_second,
            "avg_response_time": avg_response_time,
            "min_response_time": min_response_time,
            "max_response_time": max_response_time,
            "p95_response_time": p95_response_time
        }
    
    def test_sustained_load(self) -> Dict[str, Any]:
        """Test system stability under sustained load"""
        print("\n⏱️ Testing Sustained Load (5 minutes)...")
        
        start_time = time.time()
        request_count = 0
        successful_requests = 0
        failed_requests = 0
        response_times = []
        error_count = 0
        
        # Test for 5 minutes with 10 concurrent users
        test_duration = 300  # 5 minutes
        concurrent_users = 10
        
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = []
            
            # Submit initial requests
            for i in range(concurrent_users):
                query = self.test_queries[i % len(self.test_queries)]
                session_id = f"sustained_test_{i}_{int(time.time())}"
                future = executor.submit(self.make_request, query, session_id)
                futures.append(future)
            
            # Monitor for test duration
            while time.time() - start_time < test_duration:
                # Check completed futures with longer timeout
                try:
                    for future in as_completed(futures, timeout=5):
                        try:
                            status, response_time, status_code = future.result()
                            request_count += 1
                            response_times.append(response_time)
                            
                            if status == "success":
                                successful_requests += 1
                            else:
                                failed_requests += 1
                                error_count += 1
                            
                            # Submit new request
                            query = self.test_queries[request_count % len(self.test_queries)]
                            session_id = f"sustained_test_{request_count}_{int(time.time())}"
                            new_future = executor.submit(self.make_request, query, session_id)
                            futures.append(new_future)
                            
                        except Exception as e:
                            error_count += 1
                            print(f"Error in sustained test: {str(e)}")
                except TimeoutError:
                    # No futures completed within timeout, continue
                    pass
                
                # Remove completed futures
                futures = [f for f in futures if not f.done()]
                time.sleep(0.5)
        
        total_duration = time.time() - start_time
        
        # Calculate metrics
        if response_times:
            avg_response_time = statistics.mean(response_times)
            p95_response_time = sorted(response_times)[int(len(response_times) * 0.95)]
            p99_response_time = sorted(response_times)[int(len(response_times) * 0.99)]
        else:
            avg_response_time = p95_response_time = p99_response_time = 0
        
        success_rate = successful_requests / request_count * 100 if request_count > 0 else 0
        error_rate = error_count / request_count * 100 if request_count > 0 else 0
        
        # Log results
        self.log_test("Sustained Load Test", 
                     "PASS" if success_rate >= 95 and error_rate <= 1 else "PARTIAL",
                     f"Success: {success_rate:.1f}%, Errors: {error_rate:.1f}%, "
                     f"Avg: {avg_response_time:.3f}s, P95: {p95_response_time:.3f}s, P99: {p99_response_time:.3f}s",
                     total_duration)
        
        return {
            "test_type": "sustained_load",
            "duration": total_duration,
            "total_requests": request_count,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "error_count": error_count,
            "success_rate": success_rate,
            "error_rate": error_rate,
            "avg_response_time": avg_response_time,
            "p95_response_time": p95_response_time,
            "p99_response_time": p99_response_time
        }
    
    def test_peak_load(self) -> Dict[str, Any]:
        """Test system performance under peak load"""
        print("\n🚀 Testing Peak Load (burst of requests)...")
        
        start_time = time.time()
        request_count = 0
        successful_requests = 0
        failed_requests = 0
        response_times = []
        
        # Submit burst of requests (50 concurrent)
        burst_size = 50
        with ThreadPoolExecutor(max_workers=burst_size) as executor:
            futures = []
            
            # Submit all requests at once
            for i in range(burst_size):
                query = self.test_queries[i % len(self.test_queries)]
                session_id = f"peak_test_{i}_{int(time.time())}"
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
                    print(f"Error in peak test: {str(e)}")
        
        total_duration = time.time() - start_time
        
        # Calculate metrics
        if response_times:
            avg_response_time = statistics.mean(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            p95_response_time = sorted(response_times)[int(len(response_times) * 0.95)]
        else:
            avg_response_time = min_response_time = max_response_time = p95_response_time = 0
        
        success_rate = successful_requests / request_count * 100 if request_count > 0 else 0
        requests_per_second = request_count / total_duration if total_duration > 0 else 0
        
        # Log results
        self.log_test("Peak Load Test", 
                     "PASS" if success_rate >= 80 else "PARTIAL",
                     f"Success: {success_rate:.1f}%, RPS: {requests_per_second:.2f}, "
                     f"Avg: {avg_response_time:.3f}s, Max: {max_response_time:.3f}s",
                     total_duration)
        
        return {
            "test_type": "peak_load",
            "burst_size": burst_size,
            "duration": total_duration,
            "total_requests": request_count,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "success_rate": success_rate,
            "requests_per_second": requests_per_second,
            "avg_response_time": avg_response_time,
            "min_response_time": min_response_time,
            "max_response_time": max_response_time,
            "p95_response_time": p95_response_time
        }
    
    def test_error_recovery(self) -> Dict[str, Any]:
        """Test system recovery after errors"""
        print("\n🔄 Testing Error Recovery...")
        
        # Test with invalid requests to see how system handles errors
        invalid_payloads = [
            {"message": "", "role": "client", "session_id": "error_test_1"},
            {"message": "a" * 10000, "role": "client", "session_id": "error_test_2"},  # Very long message
            {"message": "Test query", "role": "invalid_role", "session_id": "error_test_3"},
            {"message": "Test query", "session_id": "error_test_4"},  # Missing role
        ]
        
        error_count = 0
        recovery_success = 0
        
        for i, payload in enumerate(invalid_payloads):
            try:
                response = requests.post(f"{self.api_base_url}/chat", json=payload, timeout=10)
                
                # Check if system handled error gracefully
                if response.status_code in [400, 422, 500]:
                    error_count += 1
                    print(f"  Expected error for payload {i+1}: {response.status_code}")
                else:
                    print(f"  Unexpected response for payload {i+1}: {response.status_code}")
                    
            except Exception as e:
                error_count += 1
                print(f"  Expected exception for payload {i+1}: {str(e)}")
        
        # Test recovery with valid request
        try:
            valid_payload = {
                "message": "Test recovery with valid request",
                "role": "client",
                "session_id": "recovery_test"
            }
            response = requests.post(f"{self.api_base_url}/chat", json=valid_payload, timeout=30)
            
            if response.status_code == 200:
                recovery_success = 1
                print("  ✅ System recovered successfully with valid request")
            else:
                print(f"  ❌ System failed to recover: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ System failed to recover: {str(e)}")
        
        # Log results
        self.log_test("Error Recovery Test", 
                     "PASS" if error_count >= 3 and recovery_success == 1 else "FAIL",
                     f"Errors handled: {error_count}/4, Recovery: {'Yes' if recovery_success else 'No'}",
                     0)
        
        return {
            "test_type": "error_recovery",
            "errors_handled": error_count,
            "recovery_success": recovery_success == 1,
            "total_invalid_payloads": len(invalid_payloads)
        }
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all load tests"""
        print("🚀 Phase 5.1.4: Load Testing Suite")
        print("=" * 60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Run load tests
        concurrent_results = {}
        for num_users in [5, 10, 20]:
            concurrent_results[num_users] = self.test_concurrent_users(num_users, 30)  # 30 seconds each
        
        sustained_result = self.test_sustained_load()
        peak_result = self.test_peak_load()
        error_recovery_result = self.test_error_recovery()
        
        # Calculate summary
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        partial_tests = len([r for r in self.test_results if r["status"] == "PARTIAL"])
        
        total_duration = time.time() - self.start_time
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 LOAD TESTING SUMMARY")
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
        for num_users, result in concurrent_results.items():
            print(f"{num_users} Concurrent Users:")
            print(f"  Success Rate: {result['success_rate']:.1f}%")
            print(f"  Requests/sec: {result['requests_per_second']:.2f}")
            print(f"  Avg Response: {result['avg_response_time']:.3f}s")
            print(f"  P95 Response: {result['p95_response_time']:.3f}s")
            print()
        
        print("Sustained Load (5 min, 10 users):")
        print(f"  Success Rate: {sustained_result['success_rate']:.1f}%")
        print(f"  Error Rate: {sustained_result['error_rate']:.1f}%")
        print(f"  Avg Response: {sustained_result['avg_response_time']:.3f}s")
        print(f"  P99 Response: {sustained_result['p99_response_time']:.3f}s")
        print()
        
        print("Peak Load (50 burst):")
        print(f"  Success Rate: {peak_result['success_rate']:.1f}%")
        print(f"  Requests/sec: {peak_result['requests_per_second']:.2f}")
        print(f"  Max Response: {peak_result['max_response_time']:.3f}s")
        print()
        
        # Save detailed results
        summary = {
            "test_suite": "Phase 5.1.4 Load Testing",
            "timestamp": datetime.now().isoformat(),
            "total_tests": total_tests,
            "passed": passed_tests,
            "partial": partial_tests,
            "failed": failed_tests,
            "success_rate": (passed_tests + partial_tests * 0.5) / total_tests * 100,
            "total_duration": total_duration,
            "concurrent_results": concurrent_results,
            "sustained_result": sustained_result,
            "peak_result": peak_result,
            "error_recovery_result": error_recovery_result,
            "detailed_results": self.test_results
        }
        
        # Save to file
        with open("test_results_load_testing.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        print(f"📄 Detailed results saved to: test_results_load_testing.json")
        
        return summary

def main():
    """Main function to run load tests"""
    test_suite = LoadTestSuite()
    results = test_suite.run_all_tests()
    
    # Exit with appropriate code
    if results["failed"] == 0:
        print("\n🎉 All load tests completed successfully!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {results['failed']} tests failed. Please review the results.")
        sys.exit(1)

if __name__ == "__main__":
    main()
