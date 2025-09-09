#!/usr/bin/env python3
"""
Performance Testing Script for Dubai Real Estate RAG System
Tests system performance, load handling, and optimization
"""

import requests
import time
import json
import threading
import statistics
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import psutil
import os

class PerformanceTester:
    def __init__(self, frontend_url="http://localhost:3000", backend_url="http://localhost:8003"):
        self.frontend_url = frontend_url
        self.backend_url = backend_url
        self.results = []
        self.start_time = datetime.now()
        self.session = requests.Session()
    
    def log_test(self, test_name, success, message, response_time=None, additional_data=None):
        status = "✅ PASS" if success else "❌ FAIL"
        time_str = f"Response time: {response_time:.3f}s" if response_time else ""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {status} - {test_name}")
        if message:
            print(f"    {message}")
        if time_str:
            print(f"    {time_str}")
        if additional_data:
            for key, value in additional_data.items():
                print(f"    {key}: {value}")
        
        self.results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "response_time": response_time,
            "additional_data": additional_data,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_system_resources(self):
        """Get current system resource usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": memory.available / (1024**3),
                "disk_percent": disk.percent,
                "disk_free_gb": disk.free / (1024**3)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def test_single_request_performance(self):
        """Test performance of single requests"""
        print("\n🧪 Testing Single Request Performance...")
        
        endpoints = [
            ("/health", "GET", "Health Check"),
            ("/properties", "GET", "Properties API"),
            ("/market/overview", "GET", "Market Data"),
            ("/auth/login", "POST", "Auth Login"),
            ("/sessions", "GET", "Sessions API")
        ]
        
        performance_data = []
        
        for endpoint, method, description in endpoints:
            try:
                start_time = time.time()
                url = f"{self.backend_url}{endpoint}"
                
                if method == "GET":
                    response = self.session.get(url, timeout=10)
                else:
                    response = self.session.post(url, json={}, timeout=10)
                
                response_time = time.time() - start_time
                
                performance_data.append({
                    "endpoint": endpoint,
                    "description": description,
                    "response_time": response_time,
                    "status_code": response.status_code,
                    "content_length": len(response.content)
                })
                
                if response_time < 1.0:  # Good performance threshold
                    self.log_test(f"Single Request - {description}", True, 
                                f"Status: {response.status_code}, Size: {len(response.content)} bytes", 
                                response_time)
                else:
                    self.log_test(f"Single Request - {description}", False, 
                                f"Slow response: {response.status_code}", response_time)
                
            except Exception as e:
                self.log_test(f"Single Request - {description}", False, f"Error: {str(e)}")
        
        return performance_data
    
    def test_concurrent_requests(self, num_requests=10):
        """Test performance under concurrent load"""
        print(f"\n🧪 Testing Concurrent Requests ({num_requests} requests)...")
        
        def make_request():
            try:
                start_time = time.time()
                response = self.session.get(f"{self.backend_url}/health", timeout=10)
                response_time = time.time() - start_time
                return {
                    "success": response.status_code == 200,
                    "response_time": response_time,
                    "status_code": response.status_code
                }
            except Exception as e:
                return {
                    "success": False,
                    "response_time": 0,
                    "error": str(e)
                }
        
        # Execute concurrent requests
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [executor.submit(make_request) for _ in range(num_requests)]
            results = [future.result() for future in as_completed(futures)]
        
        total_time = time.time() - start_time
        
        # Analyze results
        successful_requests = [r for r in results if r["success"]]
        failed_requests = [r for r in results if not r["success"]]
        
        if successful_requests:
            response_times = [r["response_time"] for r in successful_requests]
            avg_response_time = statistics.mean(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            median_response_time = statistics.median(response_times)
        else:
            avg_response_time = min_response_time = max_response_time = median_response_time = 0
        
        success_rate = (len(successful_requests) / num_requests) * 100
        requests_per_second = num_requests / total_time
        
        additional_data = {
            "Total requests": num_requests,
            "Successful requests": len(successful_requests),
            "Failed requests": len(failed_requests),
            "Success rate": f"{success_rate:.1f}%",
            "Requests per second": f"{requests_per_second:.2f}",
            "Total time": f"{total_time:.3f}s",
            "Avg response time": f"{avg_response_time:.3f}s",
            "Min response time": f"{min_response_time:.3f}s",
            "Max response time": f"{max_response_time:.3f}s",
            "Median response time": f"{median_response_time:.3f}s"
        }
        
        if success_rate >= 90 and avg_response_time < 2.0:
            self.log_test("Concurrent Requests", True, f"Good performance under load", 
                         avg_response_time, additional_data)
            return True
        else:
            self.log_test("Concurrent Requests", False, f"Performance issues under load", 
                         avg_response_time, additional_data)
            return False
    
    def test_load_testing(self, num_requests=50):
        """Test system under higher load"""
        print(f"\n🧪 Testing Load Performance ({num_requests} requests)...")
        
        def make_request():
            try:
                start_time = time.time()
                response = self.session.get(f"{self.backend_url}/properties", timeout=15)
                response_time = time.time() - start_time
                return {
                    "success": response.status_code == 200,
                    "response_time": response_time,
                    "status_code": response.status_code,
                    "content_size": len(response.content)
                }
            except Exception as e:
                return {
                    "success": False,
                    "response_time": 0,
                    "error": str(e)
                }
        
        # Get system resources before test
        resources_before = self.get_system_resources()
        
        # Execute load test
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=20) as executor:  # Limit concurrent workers
            futures = [executor.submit(make_request) for _ in range(num_requests)]
            results = [future.result() for future in as_completed(futures)]
        
        total_time = time.time() - start_time
        
        # Get system resources after test
        resources_after = self.get_system_resources()
        
        # Analyze results
        successful_requests = [r for r in results if r["success"]]
        failed_requests = [r for r in results if not r["success"]]
        
        if successful_requests:
            response_times = [r["response_time"] for r in successful_requests]
            avg_response_time = statistics.mean(response_times)
            p95_response_time = sorted(response_times)[int(len(response_times) * 0.95)]
            p99_response_time = sorted(response_times)[int(len(response_times) * 0.99)]
        else:
            avg_response_time = p95_response_time = p99_response_time = 0
        
        success_rate = (len(successful_requests) / num_requests) * 100
        requests_per_second = num_requests / total_time
        
        additional_data = {
            "Total requests": num_requests,
            "Successful requests": len(successful_requests),
            "Failed requests": len(failed_requests),
            "Success rate": f"{success_rate:.1f}%",
            "Requests per second": f"{requests_per_second:.2f}",
            "Total time": f"{total_time:.3f}s",
            "Avg response time": f"{avg_response_time:.3f}s",
            "95th percentile": f"{p95_response_time:.3f}s",
            "99th percentile": f"{p99_response_time:.3f}s",
            "CPU before": f"{resources_before.get('cpu_percent', 0):.1f}%",
            "CPU after": f"{resources_after.get('cpu_percent', 0):.1f}%",
            "Memory before": f"{resources_before.get('memory_percent', 0):.1f}%",
            "Memory after": f"{resources_after.get('memory_percent', 0):.1f}%"
        }
        
        if success_rate >= 80 and avg_response_time < 3.0:
            self.log_test("Load Testing", True, f"System handles load well", 
                         avg_response_time, additional_data)
            return True
        else:
            self.log_test("Load Testing", False, f"System struggles under load", 
                         avg_response_time, additional_data)
            return False
    
    def test_frontend_performance(self):
        """Test frontend performance"""
        print("\n🧪 Testing Frontend Performance...")
        
        def test_frontend_request():
            try:
                start_time = time.time()
                response = self.session.get(self.frontend_url, timeout=10)
                response_time = time.time() - start_time
                return {
                    "success": response.status_code == 200,
                    "response_time": response_time,
                    "content_size": len(response.content)
                }
            except Exception as e:
                return {
                    "success": False,
                    "response_time": 0,
                    "error": str(e)
                }
        
        # Test multiple frontend requests
        num_requests = 10
        results = []
        
        for _ in range(num_requests):
            results.append(test_frontend_request())
        
        successful_requests = [r for r in results if r["success"]]
        
        if successful_requests:
            response_times = [r["response_time"] for r in successful_requests]
            avg_response_time = statistics.mean(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
        else:
            avg_response_time = min_response_time = max_response_time = 0
        
        success_rate = (len(successful_requests) / num_requests) * 100
        
        additional_data = {
            "Total requests": num_requests,
            "Successful requests": len(successful_requests),
            "Success rate": f"{success_rate:.1f}%",
            "Avg response time": f"{avg_response_time:.3f}s",
            "Min response time": f"{min_response_time:.3f}s",
            "Max response time": f"{max_response_time:.3f}s",
            "Avg content size": f"{statistics.mean([r['content_size'] for r in successful_requests]):.0f} bytes" if successful_requests else "0 bytes"
        }
        
        if success_rate >= 90 and avg_response_time < 2.0:
            self.log_test("Frontend Performance", True, f"Frontend performs well", 
                         avg_response_time, additional_data)
            return True
        else:
            self.log_test("Frontend Performance", False, f"Frontend performance issues", 
                         avg_response_time, additional_data)
            return False
    
    def test_memory_usage(self):
        """Test memory usage patterns"""
        print("\n🧪 Testing Memory Usage...")
        
        # Get initial memory usage
        initial_resources = self.get_system_resources()
        
        # Make several requests to see memory impact
        for i in range(20):
            try:
                self.session.get(f"{self.backend_url}/health", timeout=5)
                self.session.get(f"{self.backend_url}/properties", timeout=5)
            except:
                pass
        
        # Get memory usage after requests
        final_resources = self.get_system_resources()
        
        memory_increase = final_resources.get('memory_percent', 0) - initial_resources.get('memory_percent', 0)
        
        additional_data = {
            "Initial memory": f"{initial_resources.get('memory_percent', 0):.1f}%",
            "Final memory": f"{final_resources.get('memory_percent', 0):.1f}%",
            "Memory increase": f"{memory_increase:.1f}%",
            "Available memory": f"{final_resources.get('memory_available_gb', 0):.2f} GB"
        }
        
        if memory_increase < 5.0:  # Less than 5% increase
            self.log_test("Memory Usage", True, f"Memory usage is stable", 
                         0, additional_data)
            return True
        else:
            self.log_test("Memory Usage", False, f"Memory usage increased significantly", 
                         0, additional_data)
            return False
    
    def test_error_handling_performance(self):
        """Test performance of error handling"""
        print("\n🧪 Testing Error Handling Performance...")
        
        error_endpoints = [
            ("/nonexistent", "GET", "404 Error"),
            ("/auth/login", "POST", "422 Validation Error"),
            ("/sessions", "GET", "403 Auth Error")
        ]
        
        error_times = []
        
        for endpoint, method, description in error_endpoints:
            try:
                start_time = time.time()
                url = f"{self.backend_url}{endpoint}"
                
                if method == "GET":
                    response = self.session.get(url, timeout=5)
                else:
                    response = self.session.post(url, json={}, timeout=5)
                
                response_time = time.time() - start_time
                error_times.append(response_time)
                
                if response_time < 1.0:
                    self.log_test(f"Error Handling - {description}", True, 
                                f"Status: {response.status_code}", response_time)
                else:
                    self.log_test(f"Error Handling - {description}", False, 
                                f"Slow error response: {response.status_code}", response_time)
                
            except Exception as e:
                self.log_test(f"Error Handling - {description}", False, f"Error: {str(e)}")
        
        if error_times:
            avg_error_time = statistics.mean(error_times)
            if avg_error_time < 0.5:
                self.log_test("Error Handling Performance", True, 
                            f"Error responses are fast", avg_error_time)
                return True
            else:
                self.log_test("Error Handling Performance", False, 
                            f"Error responses are slow", avg_error_time)
                return False
        else:
            self.log_test("Error Handling Performance", False, "No error responses tested")
            return False
    
    def run_all_tests(self):
        """Run all performance tests"""
        print("=" * 70)
        print("🚀 PERFORMANCE TESTING - DUBAI REAL ESTATE RAG SYSTEM")
        print("=" * 70)
        print(f"Frontend URL: {self.frontend_url}")
        print(f"Backend URL: {self.backend_url}")
        print(f"Started at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Get initial system resources
        initial_resources = self.get_system_resources()
        print(f"Initial System Resources: CPU: {initial_resources.get('cpu_percent', 0):.1f}%, Memory: {initial_resources.get('memory_percent', 0):.1f}%")
        
        # Run tests
        single_request_ok = self.test_single_request_performance()
        concurrent_ok = self.test_concurrent_requests(10)
        load_test_ok = self.test_load_testing(30)
        frontend_perf_ok = self.test_frontend_performance()
        memory_ok = self.test_memory_usage()
        error_handling_ok = self.test_error_handling_performance()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 PERFORMANCE TEST SUMMARY")
        print("=" * 70)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Test categories summary
        print(f"\n📋 Performance Test Categories:")
        print(f"  Single Request Performance: {'✅' if single_request_ok else '❌'}")
        print(f"  Concurrent Requests: {'✅' if concurrent_ok else '❌'}")
        print(f"  Load Testing: {'✅' if load_test_ok else '❌'}")
        print(f"  Frontend Performance: {'✅' if frontend_perf_ok else '❌'}")
        print(f"  Memory Usage: {'✅' if memory_ok else '❌'}")
        print(f"  Error Handling Performance: {'✅' if error_handling_ok else '❌'}")
        
        # Get final system resources
        final_resources = self.get_system_resources()
        print(f"\n📊 System Resource Summary:")
        print(f"  Initial CPU: {initial_resources.get('cpu_percent', 0):.1f}%")
        print(f"  Final CPU: {final_resources.get('cpu_percent', 0):.1f}%")
        print(f"  Initial Memory: {initial_resources.get('memory_percent', 0):.1f}%")
        print(f"  Final Memory: {final_resources.get('memory_percent', 0):.1f}%")
        print(f"  Available Memory: {final_resources.get('memory_available_gb', 0):.2f} GB")
        
        if success_rate >= 70:
            print("\n✅ Performance testing successful!")
            print("📄 Test results saved to performance_test_results.json")
        else:
            print("\n⚠️ Some performance tests failed. Please check the issues above.")
            print("📄 Test results saved to performance_test_results.json")
        
        # Save results
        with open("performance_test_results.json", "w") as f:
            json.dump({
                "summary": {
                    "total_tests": total_tests,
                    "passed_tests": passed_tests,
                    "failed_tests": failed_tests,
                    "success_rate": success_rate,
                    "test_duration": (datetime.now() - self.start_time).total_seconds(),
                    "frontend_url": self.frontend_url,
                    "backend_url": self.backend_url,
                    "initial_resources": initial_resources,
                    "final_resources": final_resources
                },
                "categories": {
                    "single_request": single_request_ok,
                    "concurrent_requests": concurrent_ok,
                    "load_testing": load_test_ok,
                    "frontend_performance": frontend_perf_ok,
                    "memory_usage": memory_ok,
                    "error_handling": error_handling_ok
                },
                "results": self.results
            }, f, indent=2)
        
        return success_rate >= 70

if __name__ == "__main__":
    tester = PerformanceTester()
    success = tester.run_all_tests()
    exit(0 if success else 1)
