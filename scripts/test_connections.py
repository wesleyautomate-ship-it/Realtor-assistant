#!/usr/bin/env python3
"""
Comprehensive Connection Test Script
Tests all service connections in the RAG system
"""

import os
import sys
import time
import requests
import psycopg2
import redis
import chromadb
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.append(str(backend_path))

from config.settings import DATABASE_URL, CHROMA_HOST, CHROMA_PORT, REDIS_URL

def test_postgresql_connection():
    """Test PostgreSQL connection"""
    print("🔍 Testing PostgreSQL connection...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        print("✅ PostgreSQL connection successful")
        return True
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False

def test_redis_connection():
    """Test Redis connection"""
    print("🔍 Testing Redis connection...")
    try:
        r = redis.from_url(REDIS_URL)
        r.ping()
        print("✅ Redis connection successful")
        return True
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        return False

def test_chromadb_connection():
    """Test ChromaDB connection"""
    print("🔍 Testing ChromaDB connection...")
    try:
        client = chromadb.HttpClient(
            host=CHROMA_HOST,
            port=int(CHROMA_PORT)
        )
        client.heartbeat()
        print("✅ ChromaDB connection successful")
        return True
    except Exception as e:
        print(f"❌ ChromaDB connection failed: {e}")
        return False

def test_backend_api():
    """Test Backend API health endpoint"""
    print("🔍 Testing Backend API...")
    try:
        response = requests.get("http://localhost:8003/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend API connection successful")
            return True
        else:
            print(f"❌ Backend API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend API connection failed: {e}")
        return False

def test_frontend_api():
    """Test Frontend API endpoint"""
    print("🔍 Testing Frontend API endpoint...")
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend connection successful")
            return True
        else:
            print(f"❌ Frontend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend connection failed: {e}")
        return False

def test_environment_variables():
    """Test environment variable configuration"""
    print("🔍 Testing environment variables...")
    required_vars = [
        "DATABASE_URL",
        "CHROMA_HOST", 
        "CHROMA_PORT",
        "REDIS_URL",
        "GOOGLE_API_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def main():
    """Run all connection tests"""
    print("🚀 Starting comprehensive connection tests...")
    print("=" * 50)
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("PostgreSQL", test_postgresql_connection),
        ("Redis", test_redis_connection),
        ("ChromaDB", test_chromadb_connection),
        ("Backend API", test_backend_api),
        ("Frontend", test_frontend_api),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All connections are working properly!")
        return 0
    else:
        print("⚠️ Some connections failed. Check the logs above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
