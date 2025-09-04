#!/usr/bin/env python3
"""
Test script for backend endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8003"

def test_endpoint(endpoint, method="GET", data=None, auth_required=False):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    headers = {}
    
    if auth_required:
        # For now, we'll test without auth to see the 401 response
        pass
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=10)
        else:
            return {"endpoint": endpoint, "error": f"Unsupported method: {method}"}
        
        return {
            "endpoint": endpoint,
            "method": method,
            "status_code": response.status_code,
            "response_time": response.elapsed.total_seconds(),
            "success": response.status_code < 400,
            "response_body": response.text[:200] if response.text else None
        }
        
    except requests.exceptions.ConnectionError:
        return {"endpoint": endpoint, "error": "Connection refused"}
    except requests.exceptions.Timeout:
        return {"endpoint": endpoint, "error": "Request timeout"}
    except Exception as e:
        return {"endpoint": endpoint, "error": str(e)}

def create_test_task():
    """Create a test task to test the task status endpoint"""
    url = f"{BASE_URL}/async/analyze-file"
    
    # Create a simple test file
    test_file_content = b"This is a test file for testing async processing"
    
    try:
        # Use multipart form data to simulate file upload
        files = {'file': ('test.txt', test_file_content, 'text/plain')}
        data = {'instructions': 'Test processing'}
        
        response = requests.post(url, files=files, data=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('task_id')
        else:
            print(f"Failed to create test task: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error creating test task: {e}")
        return None

def main():
    """Test all endpoints"""
    print("🔍 Testing Backend Endpoints")
    print("=" * 50)
    
    # Test basic health endpoint
    print("\n1. Testing Health Endpoint:")
    result = test_endpoint("/health")
    print(f"   {result}")
    
    # Test agenda endpoint (should return 401 without auth)
    print("\n2. Testing Agenda Endpoint (No Auth):")
    result = test_endpoint("/users/me/agenda")
    print(f"   {result}")
    
    # Create a test task and test task status endpoint
    print("\n3. Testing Task Status Endpoint:")
    print("   Creating test task...")
    task_id = create_test_task()
    
    if task_id:
        print(f"   Test task created with ID: {task_id}")
        result = test_endpoint(f"/async/processing-status/{task_id}")
        print(f"   Task status result: {result}")
    else:
        print("   Failed to create test task, testing with dummy ID...")
        result = test_endpoint("/async/processing-status/test-task-id")
        print(f"   Dummy task result: {result}")
    
    # Test Phase 3 endpoints
    print("\n4. Testing Phase 3 Endpoints:")
    phase3_endpoints = [
        ("/phase3/health", "GET"),
        ("/phase3/ai/detect-entities", "POST"),  # Should be POST
        ("/phase3/context/property/test-id", "GET"),
        ("/phase3/properties/test-id/details", "GET"),
        ("/phase3/clients/test-id", "GET"),
        ("/phase3/market/context", "GET")
    ]
    
    for endpoint, method in phase3_endpoints:
        result = test_endpoint(endpoint, method=method)
        print(f"   {endpoint} ({method}): {result}")
    
    # Test authentication endpoints
    print("\n5. Testing Auth Endpoints:")
    auth_endpoints = [
        ("/auth/login", "POST"),  # Should be POST
        ("/auth/register", "POST"),  # Should be POST
        ("/auth/me", "GET")
    ]
    
    for endpoint, method in auth_endpoints:
        result = test_endpoint(endpoint, method=method)
        print(f"   {endpoint} ({method}): {result}")
    
    print("\n" + "=" * 50)
    print("✅ Endpoint testing completed!")

if __name__ == "__main__":
    main()
