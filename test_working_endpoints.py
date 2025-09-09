#!/usr/bin/env python3
"""
Quick test to check which endpoints are actually working
"""

import requests
import json
from datetime import datetime

def test_endpoint(method, url, data=None, headers=None):
    """Test a single endpoint"""
    try:
        if method.upper() == 'GET':
            response = requests.get(url, timeout=5)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers=headers, timeout=5)
        else:
            return f"❌ Unknown method: {method}"
        
        if response.status_code == 200:
            return f"✅ {method} {url} - Status: {response.status_code}"
        elif response.status_code == 404:
            return f"❌ {method} {url} - Not Found (404)"
        elif response.status_code == 405:
            return f"⚠️ {method} {url} - Method Not Allowed (405) - Endpoint exists but wrong method"
        else:
            return f"⚠️ {method} {url} - Status: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"❌ {method} {url} - Error: {str(e)}"

def main():
    base_url = "http://localhost:8003"
    
    print("=" * 60)
    print("🔍 TESTING WORKING ENDPOINTS")
    print("=" * 60)
    print(f"Testing server at: {base_url}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test basic endpoints
    endpoints_to_test = [
        # Health and docs
        ("GET", "/health"),
        ("GET", "/docs"),
        ("GET", "/openapi.json"),
        
        # Auth endpoints
        ("GET", "/auth/register"),
        ("POST", "/auth/register"),
        ("GET", "/auth/login"),
        ("POST", "/auth/login"),
        
        # Chat endpoints
        ("GET", "/api/chat/sessions"),
        ("GET", "/sessions"),
        ("GET", "/chat/sessions"),
        
        # Data endpoints
        ("GET", "/api/data/properties"),
        ("GET", "/data/properties"),
        
        # Admin endpoints
        ("GET", "/api/admin/dashboard"),
        ("GET", "/admin/dashboard"),
        
        # File processing
        ("GET", "/api/files/upload"),
        ("GET", "/files/upload"),
        
        # Performance
        ("GET", "/api/performance/metrics"),
        ("GET", "/performance/metrics"),
    ]
    
    results = []
    for method, endpoint in endpoints_to_test:
        url = f"{base_url}{endpoint}"
        result = test_endpoint(method, url)
        results.append(result)
        print(result)
    
    print()
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    working = [r for r in results if r.startswith("✅")]
    method_wrong = [r for r in results if r.startswith("⚠️") and "405" in r]
    not_found = [r for r in results if r.startswith("❌") and "404" in r]
    errors = [r for r in results if r.startswith("❌") and "Error:" in r]
    
    print(f"✅ Working endpoints: {len(working)}")
    print(f"⚠️ Endpoints with wrong method: {len(method_wrong)}")
    print(f"❌ Not found endpoints: {len(not_found)}")
    print(f"❌ Error endpoints: {len(errors)}")
    
    if working:
        print("\n🎉 WORKING ENDPOINTS:")
        for result in working:
            print(f"  {result}")
    
    if method_wrong:
        print("\n⚠️ ENDPOINTS WITH WRONG METHOD (endpoint exists):")
        for result in method_wrong:
            print(f"  {result}")

if __name__ == "__main__":
    main()
