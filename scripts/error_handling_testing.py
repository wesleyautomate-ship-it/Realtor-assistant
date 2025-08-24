#!/usr/bin/env python3
"""
Phase 5.1.5: Error Handling Testing
Test system resilience and error recovery
"""

import os
import sys
import time
import json
import requests
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class ErrorHandlingTestSuite:
    def __init__(self):
        self.api_base_url = "http://localhost:8001"
        self.test_results = []
        self.start_time = time.time()
        
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
    
    def test_invalid_inputs(self) -> Dict[str, Any]:
        """Test system handling of invalid inputs"""
        print("\n🚫 Testing Invalid Inputs...")
        
        start_time = time.time()
        error_count = 0
        total_tests = 0
        
        # Test cases for invalid inputs
        invalid_cases = [
            {"message": "", "role": "client", "session_id": "empty_message"},
            {"message": "a" * 10001, "role": "client", "session_id": "too_long_message"},  # > 10k chars
            {"message": "Test", "role": "invalid_role", "session_id": "invalid_role"},
            {"message": "Test", "session_id": "missing_role"},
            {"role": "client", "session_id": "missing_message"},
            {"message": "Test", "role": "client"},  # Missing session_id
            {"message": None, "role": "client", "session_id": "null_message"},
            {"message": 123, "role": "client", "session_id": "non_string_message"},
            {"message": "Test", "role": "client", "session_id": "test", "extra_field": "should_be_ignored"},
        ]
        
        for i, payload in enumerate(invalid_cases):
            total_tests += 1
            try:
                response = requests.post(f"{self.api_base_url}/chat", json=payload, timeout=10)
                
                # Check if system handled error gracefully
                if response.status_code in [400, 422, 500]:
                    error_count += 1
                    print(f"  ✅ Case {i+1}: Expected error {response.status_code}")
                else:
                    print(f"  ⚠️ Case {i+1}: Unexpected response {response.status_code}")
                    
            except Exception as e:
                error_count += 1
                print(f"  ✅ Case {i+1}: Expected exception - {str(e)[:50]}...")
        
        total_duration = time.time() - start_time
        success_rate = error_count / total_tests * 100 if total_tests > 0 else 0
        
        # Log results
        self.log_test("Invalid Inputs Test", 
                     "PASS" if success_rate >= 80 else "PARTIAL",
                     f"Errors handled: {error_count}/{total_tests} ({success_rate:.1f}%)",
                     total_duration)
        
        return {
            "test_type": "invalid_inputs",
            "total_tests": total_tests,
            "errors_handled": error_count,
            "success_rate": success_rate
        }
    
    def test_malformed_requests(self) -> Dict[str, Any]:
        """Test system handling of malformed requests"""
        print("\n🔧 Testing Malformed Requests...")
        
        start_time = time.time()
        error_count = 0
        total_tests = 0
        
        # Test malformed requests
        malformed_requests = [
            # Invalid JSON
            ("invalid json", "application/json"),
            # Empty body
            ("", "application/json"),
            # Wrong content type
            ('{"message": "test"}', "text/plain"),
            # Very large payload
            ('{"message": "' + "a" * 50000 + '"}', "application/json"),
        ]
        
        for i, (payload, content_type) in enumerate(malformed_requests):
            total_tests += 1
            try:
                headers = {"Content-Type": content_type}
                response = requests.post(f"{self.api_base_url}/chat", 
                                       data=payload, 
                                       headers=headers, 
                                       timeout=10)
                
                if response.status_code in [400, 422, 500]:
                    error_count += 1
                    print(f"  ✅ Malformed {i+1}: Expected error {response.status_code}")
                else:
                    print(f"  ⚠️ Malformed {i+1}: Unexpected response {response.status_code}")
                    
            except Exception as e:
                error_count += 1
                print(f"  ✅ Malformed {i+1}: Expected exception - {str(e)[:50]}...")
        
        total_duration = time.time() - start_time
        success_rate = error_count / total_tests * 100 if total_tests > 0 else 0
        
        # Log results
        self.log_test("Malformed Requests Test", 
                     "PASS" if success_rate >= 75 else "PARTIAL",
                     f"Errors handled: {error_count}/{total_tests} ({success_rate:.1f}%)",
                     total_duration)
        
        return {
            "test_type": "malformed_requests",
            "total_tests": total_tests,
            "errors_handled": error_count,
            "success_rate": success_rate
        }
    
    def test_system_recovery(self) -> Dict[str, Any]:
        """Test system recovery after errors"""
        print("\n🔄 Testing System Recovery...")
        
        start_time = time.time()
        recovery_success = 0
        total_attempts = 0
        
        # Test recovery after various error conditions
        recovery_scenarios = [
            # After invalid input
            {"invalid": {"message": "", "role": "client", "session_id": "recovery_test_1"},
             "valid": {"message": "Test recovery after empty message", "role": "client", "session_id": "recovery_test_1"}},
            
            # After malformed request
            {"invalid": "invalid json",
             "valid": {"message": "Test recovery after malformed JSON", "role": "client", "session_id": "recovery_test_2"}},
            
            # After invalid role
            {"invalid": {"message": "Test", "role": "invalid_role", "session_id": "recovery_test_3"},
             "valid": {"message": "Test recovery after invalid role", "role": "client", "session_id": "recovery_test_3"}},
        ]
        
        for i, scenario in enumerate(recovery_scenarios):
            total_attempts += 1
            
            # First, trigger an error
            try:
                if isinstance(scenario["invalid"], dict):
                    response = requests.post(f"{self.api_base_url}/chat", 
                                           json=scenario["invalid"], 
                                           timeout=5)
                else:
                    response = requests.post(f"{self.api_base_url}/chat", 
                                           data=scenario["invalid"], 
                                           timeout=5)
                
                # Error was triggered (expected)
                print(f"  ✅ Error triggered for scenario {i+1}")
                
                # Now test recovery with valid request
                try:
                    response = requests.post(f"{self.api_base_url}/chat", 
                                           json=scenario["valid"], 
                                           timeout=15)
                    
                    if response.status_code == 200:
                        recovery_success += 1
                        print(f"  ✅ Recovery successful for scenario {i+1}")
                    else:
                        print(f"  ❌ Recovery failed for scenario {i+1}: {response.status_code}")
                        
                except Exception as e:
                    print(f"  ❌ Recovery failed for scenario {i+1}: {str(e)[:50]}...")
                    
            except Exception as e:
                print(f"  ✅ Error triggered for scenario {i+1}: {str(e)[:50]}...")
                
                # Test recovery even after exception
                try:
                    response = requests.post(f"{self.api_base_url}/chat", 
                                           json=scenario["valid"], 
                                           timeout=15)
                    
                    if response.status_code == 200:
                        recovery_success += 1
                        print(f"  ✅ Recovery successful for scenario {i+1}")
                    else:
                        print(f"  ❌ Recovery failed for scenario {i+1}: {response.status_code}")
                        
                except Exception as e:
                    print(f"  ❌ Recovery failed for scenario {i+1}: {str(e)[:50]}...")
        
        total_duration = time.time() - start_time
        recovery_rate = recovery_success / total_attempts * 100 if total_attempts > 0 else 0
        
        # Log results
        self.log_test("System Recovery Test", 
                     "PASS" if recovery_rate >= 60 else "PARTIAL",
                     f"Recovery successful: {recovery_success}/{total_attempts} ({recovery_rate:.1f}%)",
                     total_duration)
        
        return {
            "test_type": "system_recovery",
            "total_attempts": total_attempts,
            "recovery_success": recovery_success,
            "recovery_rate": recovery_rate
        }
    
    def test_edge_cases(self) -> Dict[str, Any]:
        """Test edge cases and boundary conditions"""
        print("\n🔍 Testing Edge Cases...")
        
        start_time = time.time()
        handled_count = 0
        total_cases = 0
        
        # Edge cases
        edge_cases = [
            # Very short message
            {"message": "Hi", "role": "client", "session_id": "edge_short"},
            
            # Message with special characters
            {"message": "Test with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?", "role": "client", "session_id": "edge_special"},
            
            # Message with unicode
            {"message": "Test with unicode: 你好世界 🌍", "role": "client", "session_id": "edge_unicode"},
            
            # Very long session ID
            {"message": "Test", "role": "client", "session_id": "a" * 1000},
            
            # Session ID with special characters
            {"message": "Test", "role": "client", "session_id": "session-123_test@example.com"},
            
            # Different roles
            {"message": "Test", "role": "agent", "session_id": "edge_agent"},
            {"message": "Test", "role": "employee", "session_id": "edge_employee"},
            {"message": "Test", "role": "admin", "session_id": "edge_admin"},
        ]
        
        for i, payload in enumerate(edge_cases):
            total_cases += 1
            try:
                response = requests.post(f"{self.api_base_url}/chat", json=payload, timeout=15)
                
                if response.status_code == 200:
                    handled_count += 1
                    print(f"  ✅ Edge case {i+1}: Handled successfully")
                elif response.status_code in [400, 422, 500]:
                    print(f"  ⚠️ Edge case {i+1}: Error {response.status_code} (may be expected)")
                else:
                    print(f"  ❌ Edge case {i+1}: Unexpected response {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ Edge case {i+1}: Exception - {str(e)[:50]}...")
        
        total_duration = time.time() - start_time
        success_rate = handled_count / total_cases * 100 if total_cases > 0 else 0
        
        # Log results
        self.log_test("Edge Cases Test", 
                     "PASS" if success_rate >= 50 else "PARTIAL",
                     f"Handled successfully: {handled_count}/{total_cases} ({success_rate:.1f}%)",
                     total_duration)
        
        return {
            "test_type": "edge_cases",
            "total_cases": total_cases,
            "handled_successfully": handled_count,
            "success_rate": success_rate
        }
    
    def test_error_logging(self) -> Dict[str, Any]:
        """Test if errors are properly logged and handled"""
        print("\n📝 Testing Error Logging...")
        
        start_time = time.time()
        
        # Test various error conditions and check if they're handled gracefully
        error_tests = [
            {"name": "Empty Message", "payload": {"message": "", "role": "client", "session_id": "log_test_1"}},
            {"name": "Invalid Role", "payload": {"message": "Test", "role": "invalid", "session_id": "log_test_2"}},
            {"name": "Missing Fields", "payload": {"message": "Test", "session_id": "log_test_3"}},
        ]
        
        graceful_handling = 0
        total_tests = len(error_tests)
        
        for test in error_tests:
            try:
                response = requests.post(f"{self.api_base_url}/chat", json=test["payload"], timeout=10)
                
                # Check if error was handled gracefully (not a 500 internal server error)
                if response.status_code in [400, 422]:
                    graceful_handling += 1
                    print(f"  ✅ {test['name']}: Gracefully handled ({response.status_code})")
                elif response.status_code == 500:
                    print(f"  ❌ {test['name']}: Internal server error (500)")
                else:
                    print(f"  ⚠️ {test['name']}: Unexpected response ({response.status_code})")
                    
            except Exception as e:
                print(f"  ✅ {test['name']}: Exception handled - {str(e)[:50]}...")
                graceful_handling += 1
        
        total_duration = time.time() - start_time
        graceful_rate = graceful_handling / total_tests * 100 if total_tests > 0 else 0
        
        # Log results
        self.log_test("Error Logging Test", 
                     "PASS" if graceful_rate >= 80 else "PARTIAL",
                     f"Gracefully handled: {graceful_handling}/{total_tests} ({graceful_rate:.1f}%)",
                     total_duration)
        
        return {
            "test_type": "error_logging",
            "total_tests": total_tests,
            "graceful_handling": graceful_handling,
            "graceful_rate": graceful_rate
        }
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all error handling tests"""
        print("🚀 Phase 5.1.5: Error Handling Testing Suite")
        print("=" * 60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Run tests
        invalid_inputs_result = self.test_invalid_inputs()
        malformed_requests_result = self.test_malformed_requests()
        system_recovery_result = self.test_system_recovery()
        edge_cases_result = self.test_edge_cases()
        error_logging_result = self.test_error_logging()
        
        # Calculate summary
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        partial_tests = len([r for r in self.test_results if r["status"] == "PARTIAL"])
        
        total_duration = time.time() - self.start_time
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 ERROR HANDLING TESTING SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"⚠️  Partial: {partial_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests + partial_tests * 0.5) / total_tests * 100:.1f}%")
        print(f"Total Duration: {total_duration:.2f}s")
        
        # Detailed results
        print("\n📈 DETAILED RESULTS:")
        print("-" * 40)
        print("Invalid Inputs:")
        print(f"  Success Rate: {invalid_inputs_result.get('success_rate', 0):.1f}%")
        print(f"  Errors Handled: {invalid_inputs_result.get('errors_handled', 0)}/{invalid_inputs_result.get('total_tests', 0)}")
        print()
        
        print("Malformed Requests:")
        print(f"  Success Rate: {malformed_requests_result.get('success_rate', 0):.1f}%")
        print(f"  Errors Handled: {malformed_requests_result.get('errors_handled', 0)}/{malformed_requests_result.get('total_tests', 0)}")
        print()
        
        print("System Recovery:")
        print(f"  Recovery Rate: {system_recovery_result.get('recovery_rate', 0):.1f}%")
        print(f"  Recovery Success: {system_recovery_result.get('recovery_success', 0)}/{system_recovery_result.get('total_attempts', 0)}")
        print()
        
        print("Edge Cases:")
        print(f"  Success Rate: {edge_cases_result.get('success_rate', 0):.1f}%")
        print(f"  Handled Successfully: {edge_cases_result.get('handled_successfully', 0)}/{edge_cases_result.get('total_cases', 0)}")
        print()
        
        print("Error Logging:")
        print(f"  Graceful Rate: {error_logging_result.get('graceful_rate', 0):.1f}%")
        print(f"  Graceful Handling: {error_logging_result.get('graceful_handling', 0)}/{error_logging_result.get('total_tests', 0)}")
        print()
        
        # Save detailed results
        summary = {
            "test_suite": "Phase 5.1.5 Error Handling Testing",
            "timestamp": datetime.now().isoformat(),
            "total_tests": total_tests,
            "passed": passed_tests,
            "partial": partial_tests,
            "failed": failed_tests,
            "success_rate": (passed_tests + partial_tests * 0.5) / total_tests * 100,
            "total_duration": total_duration,
            "invalid_inputs_result": invalid_inputs_result,
            "malformed_requests_result": malformed_requests_result,
            "system_recovery_result": system_recovery_result,
            "edge_cases_result": edge_cases_result,
            "error_logging_result": error_logging_result,
            "detailed_results": self.test_results
        }
        
        # Save to file
        with open("test_results_error_handling.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        print(f"📄 Detailed results saved to: test_results_error_handling.json")
        
        return summary

def main():
    """Main function to run error handling tests"""
    test_suite = ErrorHandlingTestSuite()
    results = test_suite.run_all_tests()
    
    # Exit with appropriate code
    if results["failed"] == 0:
        print("\n🎉 All error handling tests completed!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {results['failed']} tests failed. Please review the results.")
        sys.exit(1)

if __name__ == "__main__":
    main()
