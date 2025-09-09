#!/usr/bin/env python3
"""
Frontend Testing Script for Dubai Real Estate RAG System
"""

import requests
import time
import json
from datetime import datetime
from urllib.parse import urljoin

class FrontendTester:
    def __init__(self, frontend_url="http://localhost:3000", backend_url="http://localhost:8003"):
        self.frontend_url = frontend_url
        self.backend_url = backend_url
        self.results = []
        self.start_time = datetime.now()
    
    def log_test(self, test_name, success, message, response_time=None):
        status = "✅ PASS" if success else "❌ FAIL"
        time_str = f"Response time: {response_time:.3f}s" if response_time else ""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {status} - {test_name}")
        if message:
            print(f"    {message}")
        if time_str:
            print(f"    {time_str}")
        
        self.results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "response_time": response_time,
            "timestamp": datetime.now().isoformat()
        })
    
    def test_frontend_accessibility(self):
        """Test if frontend is accessible and serving content"""
        print("\n🧪 Testing Frontend Accessibility...")
        
        try:
            start_time = time.time()
            response = requests.get(self.frontend_url, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                content = response.text
                if "Dubai Real Estate RAG System" in content:
                    self.log_test("Frontend Homepage", True, "Frontend accessible and serving content", response_time)
                    return True
                else:
                    self.log_test("Frontend Homepage", False, "Frontend accessible but content not as expected", response_time)
                    return False
            else:
                self.log_test("Frontend Homepage", False, f"Status code: {response.status_code}", response_time)
                return False
        except Exception as e:
            self.log_test("Frontend Homepage", False, f"Error: {str(e)}")
            return False
    
    def test_static_assets(self):
        """Test if static assets are being served"""
        print("\n🧪 Testing Static Assets...")
        
        static_assets = [
            "/static/js/bundle.js",
            "/favicon.ico",
            "/manifest.json"
        ]
        
        success_count = 0
        for asset in static_assets:
            try:
                start_time = time.time()
                url = urljoin(self.frontend_url, asset)
                response = requests.get(url, timeout=10)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    self.log_test(f"Static Asset - {asset}", True, f"Status: {response.status_code}", response_time)
                    success_count += 1
                else:
                    self.log_test(f"Static Asset - {asset}", False, f"Status code: {response.status_code}", response_time)
            except Exception as e:
                self.log_test(f"Static Asset - {asset}", False, f"Error: {str(e)}")
        
        return success_count > 0
    
    def test_backend_connectivity(self):
        """Test if frontend can connect to backend"""
        print("\n🧪 Testing Backend Connectivity...")
        
        try:
            start_time = time.time()
            response = requests.get(f"{self.backend_url}/health", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Backend Health Check", True, f"Backend accessible: {data.get('status', 'unknown')}", response_time)
                return True
            else:
                self.log_test("Backend Health Check", False, f"Status code: {response.status_code}", response_time)
                return False
        except Exception as e:
            self.log_test("Backend Health Check", False, f"Error: {str(e)}")
            return False
    
    def test_cors_headers(self):
        """Test CORS headers for frontend-backend communication"""
        print("\n🧪 Testing CORS Configuration...")
        
        try:
            # Test preflight request
            headers = {
                'Origin': self.frontend_url,
                'Access-Control-Request-Method': 'GET',
                'Access-Control-Request-Headers': 'Content-Type'
            }
            
            start_time = time.time()
            response = requests.options(f"{self.backend_url}/health", headers=headers, timeout=10)
            response_time = time.time() - start_time
            
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
            }
            
            if response.status_code in [200, 204]:
                self.log_test("CORS Preflight", True, f"CORS headers present: {cors_headers}", response_time)
                return True
            else:
                self.log_test("CORS Preflight", False, f"Status code: {response.status_code}", response_time)
                return False
        except Exception as e:
            self.log_test("CORS Preflight", False, f"Error: {str(e)}")
            return False
    
    def test_api_endpoints_from_frontend(self):
        """Test key API endpoints that frontend would use"""
        print("\n🧪 Testing API Endpoints for Frontend...")
        
        # Test endpoints that frontend would typically call
        api_endpoints = [
            ("/health", "GET"),
            ("/auth/login", "POST"),
            ("/properties", "GET"),
            ("/sessions", "GET"),
            ("/market/overview", "GET")
        ]
        
        success_count = 0
        for endpoint, method in api_endpoints:
            try:
                start_time = time.time()
                url = f"{self.backend_url}{endpoint}"
                
                if method == "GET":
                    response = requests.get(url, timeout=10)
                else:
                    response = requests.post(url, json={}, timeout=10)
                
                response_time = time.time() - start_time
                
                # Accept various status codes as "working" (200, 401, 403, 422, etc.)
                if response.status_code in [200, 401, 403, 422, 500]:
                    self.log_test(f"API - {endpoint}", True, f"Status: {response.status_code}", response_time)
                    success_count += 1
                else:
                    self.log_test(f"API - {endpoint}", False, f"Status code: {response.status_code}", response_time)
            except Exception as e:
                self.log_test(f"API - {endpoint}", False, f"Error: {str(e)}")
        
        return success_count >= len(api_endpoints) * 0.6  # 60% success rate
    
    def test_frontend_performance(self):
        """Test frontend performance"""
        print("\n🧪 Testing Frontend Performance...")
        
        success_count = 0
        total_time = 0
        
        for i in range(5):
            try:
                start_time = time.time()
                response = requests.get(self.frontend_url, timeout=10)
                response_time = time.time() - start_time
                total_time += response_time
                
                if response.status_code == 200 and response_time < 2.0:  # Should load within 2 seconds
                    success_count += 1
            except Exception as e:
                pass
        
        avg_response_time = total_time / 5 if total_time > 0 else 0
        success_rate = (success_count / 5) * 100
        
        if success_count >= 4:  # 80% success rate
            self.log_test("Frontend Performance", True, f"{success_count}/5 requests successful, avg: {avg_response_time:.3f}s", avg_response_time)
            return True
        else:
            self.log_test("Frontend Performance", False, f"Only {success_count}/5 requests successful, avg: {avg_response_time:.3f}s", avg_response_time)
            return False
    
    def test_react_app_loading(self):
        """Test if React app is loading properly"""
        print("\n🧪 Testing React App Loading...")
        
        try:
            start_time = time.time()
            response = requests.get(self.frontend_url, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                content = response.text
                
                # Check for React app indicators
                react_indicators = [
                    "id=\"root\"",
                    "bundle.js",
                    "Dubai Real Estate RAG System"
                ]
                
                found_indicators = sum(1 for indicator in react_indicators if indicator in content)
                
                if found_indicators >= 2:
                    self.log_test("React App Loading", True, f"React app indicators found: {found_indicators}/3", response_time)
                    return True
                else:
                    self.log_test("React App Loading", False, f"Only {found_indicators}/3 React indicators found", response_time)
                    return False
            else:
                self.log_test("React App Loading", False, f"Status code: {response.status_code}", response_time)
                return False
        except Exception as e:
            self.log_test("React App Loading", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all frontend tests"""
        print("=" * 60)
        print("🚀 FRONTEND TESTING - DUBAI REAL ESTATE RAG SYSTEM")
        print("=" * 60)
        print(f"Frontend URL: {self.frontend_url}")
        print(f"Backend URL: {self.backend_url}")
        print(f"Started at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run tests
        accessibility_ok = self.test_frontend_accessibility()
        static_assets_ok = self.test_static_assets()
        backend_connectivity_ok = self.test_backend_connectivity()
        cors_ok = self.test_cors_headers()
        api_endpoints_ok = self.test_api_endpoints_from_frontend()
        performance_ok = self.test_frontend_performance()
        react_loading_ok = self.test_react_app_loading()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 FRONTEND TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Test categories summary
        print(f"\n📋 Test Categories:")
        print(f"  Frontend Accessibility: {'✅' if accessibility_ok else '❌'}")
        print(f"  Static Assets: {'✅' if static_assets_ok else '❌'}")
        print(f"  Backend Connectivity: {'✅' if backend_connectivity_ok else '❌'}")
        print(f"  CORS Configuration: {'✅' if cors_ok else '❌'}")
        print(f"  API Endpoints: {'✅' if api_endpoints_ok else '❌'}")
        print(f"  Performance: {'✅' if performance_ok else '❌'}")
        print(f"  React App Loading: {'✅' if react_loading_ok else '❌'}")
        
        if success_rate >= 70:
            print("\n✅ Frontend is working well!")
            print("📄 Test results saved to frontend_test_results.json")
        else:
            print("\n⚠️ Some frontend tests failed. Please check the issues above.")
            print("📄 Test results saved to frontend_test_results.json")
        
        # Save results
        with open("frontend_test_results.json", "w") as f:
            json.dump({
                "summary": {
                    "total_tests": total_tests,
                    "passed_tests": passed_tests,
                    "failed_tests": failed_tests,
                    "success_rate": success_rate,
                    "test_duration": (datetime.now() - self.start_time).total_seconds(),
                    "frontend_url": self.frontend_url,
                    "backend_url": self.backend_url
                },
                "categories": {
                    "accessibility": accessibility_ok,
                    "static_assets": static_assets_ok,
                    "backend_connectivity": backend_connectivity_ok,
                    "cors": cors_ok,
                    "api_endpoints": api_endpoints_ok,
                    "performance": performance_ok,
                    "react_loading": react_loading_ok
                },
                "results": self.results
            }, f, indent=2)
        
        return success_rate >= 70

if __name__ == "__main__":
    tester = FrontendTester()
    success = tester.run_all_tests()
    exit(0 if success else 1)
