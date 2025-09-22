#!/usr/bin/env python3
"""
Test script for MCP (Model Context Protocol) integration

This script tests the MCP server integration with the FastAPI application
to ensure all endpoints are properly exposed as MCP tools.
"""

import requests
import json
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8003"
MCP_ENDPOINT = f"{BASE_URL}/mcp"
MCP_INFO_ENDPOINT = f"{BASE_URL}/mcp/info"
MCP_HEALTH_ENDPOINT = f"{BASE_URL}/mcp/health"

def test_mcp_health() -> Dict[str, Any]:
    """Test MCP server health check"""
    print("🔍 Testing MCP server health...")
    try:
        response = requests.get(MCP_HEALTH_ENDPOINT, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ MCP Health Check: {data['status']}")
            return data
        else:
            print(f"❌ MCP Health Check failed: {response.status_code}")
            return {"status": "error", "code": response.status_code}
    except Exception as e:
        print(f"❌ MCP Health Check error: {e}")
        return {"status": "error", "message": str(e)}

def test_mcp_info() -> Dict[str, Any]:
    """Test MCP server information endpoint"""
    print("🔍 Testing MCP server info...")
    try:
        response = requests.get(MCP_INFO_ENDPOINT, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ MCP Info: {data['status']}")
            print(f"📋 Server: {data.get('server_name', 'Unknown')}")
            print(f"📋 Total Tools: {data.get('total_tools', 0)}")
            print(f"📋 MCP Endpoint: {data.get('mcp_endpoint', 'Unknown')}")
            return data
        else:
            print(f"❌ MCP Info failed: {response.status_code}")
            return {"status": "error", "code": response.status_code}
    except Exception as e:
        print(f"❌ MCP Info error: {e}")
        return {"status": "error", "message": str(e)}

def test_mcp_endpoint() -> Dict[str, Any]:
    """Test the main MCP endpoint"""
    print("🔍 Testing main MCP endpoint...")
    try:
        response = requests.get(MCP_ENDPOINT, timeout=10)
        if response.status_code == 200:
            print(f"✅ MCP Endpoint accessible: {response.status_code}")
            return {"status": "accessible", "code": response.status_code}
        else:
            print(f"⚠️ MCP Endpoint returned: {response.status_code}")
            return {"status": "warning", "code": response.status_code}
    except Exception as e:
        print(f"❌ MCP Endpoint error: {e}")
        return {"status": "error", "message": str(e)}

def test_key_endpoints() -> Dict[str, Any]:
    """Test key endpoints that should be exposed as MCP tools"""
    print("🔍 Testing key endpoints for MCP integration...")
    
    endpoints_to_test = [
        ("/chat", "POST", "Chat endpoint"),
        ("/properties", "GET", "Properties endpoint"),
        ("/ml-insights/analytics/market-performance", "GET", "Market analysis endpoint"),
        ("/mcp/info", "GET", "MCP info endpoint")
    ]
    
    results = {}
    
    for endpoint, method, description in endpoints_to_test:
        try:
            url = f"{BASE_URL}{endpoint}"
            if method == "GET":
                response = requests.get(url, timeout=5)
            else:
                # For POST endpoints, send a minimal request
                response = requests.post(url, json={}, timeout=5)
            
            if response.status_code in [200, 422, 401]:  # 422 is validation error, 401 is auth required
                print(f"✅ {description}: {response.status_code}")
                results[endpoint] = {"status": "accessible", "code": response.status_code}
            else:
                print(f"⚠️ {description}: {response.status_code}")
                results[endpoint] = {"status": "warning", "code": response.status_code}
                
        except Exception as e:
            print(f"❌ {description}: {e}")
            results[endpoint] = {"status": "error", "message": str(e)}
    
    return results

def main():
    """Main test function"""
    print("🚀 Starting MCP Integration Tests for Laura AI Real Estate Assistant")
    print("=" * 70)
    
    # Test MCP server health
    health_result = test_mcp_health()
    print()
    
    # Test MCP server info
    info_result = test_mcp_info()
    print()
    
    # Test main MCP endpoint
    mcp_result = test_mcp_endpoint()
    print()
    
    # Test key endpoints
    endpoints_result = test_key_endpoints()
    print()
    
    # Summary
    print("📊 Test Summary:")
    print("=" * 30)
    
    if health_result.get("status") == "healthy":
        print("✅ MCP Server: Healthy")
    else:
        print("❌ MCP Server: Unhealthy")
    
    if info_result.get("status") == "available":
        print(f"✅ MCP Tools: {info_result.get('total_tools', 0)} available")
    else:
        print("❌ MCP Tools: Not available")
    
    accessible_endpoints = sum(1 for r in endpoints_result.values() if r.get("status") == "accessible")
    total_endpoints = len(endpoints_result)
    print(f"✅ Endpoints: {accessible_endpoints}/{total_endpoints} accessible")
    
    print()
    print("🌐 MCP Server Information:")
    if info_result.get("status") == "available":
        print(f"   Server: {info_result.get('server_name', 'Unknown')}")
        print(f"   Endpoint: {info_result.get('mcp_endpoint', 'Unknown')}")
        print(f"   Tools: {info_result.get('total_tools', 0)}")
        print(f"   Tags: {', '.join(info_result.get('included_tags', []))}")
    
    print()
    print("🎯 Next Steps:")
    print("1. Install fastapi-mcp: pip install fastapi-mcp")
    print("2. Restart the backend server")
    print("3. Test MCP tools with AI models")
    print("4. Integrate MCP tools into your AI workflows")

if __name__ == "__main__":
    main()



