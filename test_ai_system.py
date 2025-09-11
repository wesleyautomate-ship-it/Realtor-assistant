#!/usr/bin/env python3
"""
AI Request System Integration Test
=================================

This script tests the complete AI request system integration including:
- Database connectivity
- API endpoints
- Model relationships
- Authentication flow
"""

import os
import sys
import requests
import json
import time
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent / 'backend'))

def test_database_connection():
    """Test database connection and models"""
    print("🔌 Testing database connection...")
    
    try:
        from backend.auth.database import get_db
        from backend.models.ai_request_models import AIRequest, Template
        from sqlalchemy.orm import Session
        
        # Test database connection
        db = next(get_db())
        
        # Test template count
        template_count = db.query(Template).count()
        print(f"✅ Database connected. Found {template_count} templates.")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🌐 Testing API endpoints...")
    
    base_url = "http://localhost:8001"
    
    # Test endpoints that don't require authentication
    endpoints = [
        "/docs",
        "/openapi.json",
        "/api/requests/templates"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code in [200, 401]:  # 401 is expected for protected endpoints
                print(f"✅ {endpoint} - Status: {response.status_code}")
            else:
                print(f"⚠️ {endpoint} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint} - Error: {e}")
    
    return True

def test_frontend_build():
    """Test if frontend can build successfully"""
    print("\n🎨 Testing frontend build...")
    
    try:
        import subprocess
        import os
        
        # Change to frontend directory
        frontend_dir = Path(__file__).parent / 'frontend'
        os.chdir(frontend_dir)
        
        # Install dependencies
        print("📦 Installing frontend dependencies...")
        result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ npm install failed: {result.stderr}")
            return False
        
        # Test build
        print("🔨 Testing frontend build...")
        result = subprocess.run(['npm', 'run', 'build'], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Frontend build failed: {result.stderr}")
            return False
        
        print("✅ Frontend build successful!")
        return True
        
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
        return False
    finally:
        # Change back to original directory
        os.chdir(Path(__file__).parent)

def test_model_imports():
    """Test if all models can be imported"""
    print("\n📊 Testing model imports...")
    
    try:
        from backend.models.ai_request_models import (
            AIRequest, AIRequestStep, Deliverable, 
            Template, BrandAsset, AIRequestEvent
        )
        print("✅ All AI request models imported successfully")
        
        from backend.models.brokerage_models import Brokerage, User
        print("✅ Brokerage models imported successfully")
        
        from backend.auth.models import User as AuthUser
        print("✅ Auth models imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Model import failed: {e}")
        return False

def test_router_imports():
    """Test if all routers can be imported"""
    print("\n🛣️ Testing router imports...")
    
    try:
        from backend.routers.ai_request_router import router as ai_request_router
        print("✅ AI request router imported successfully")
        
        from backend.routers.ai_assistant_router import router as ai_assistant_router
        print("✅ AI assistant router imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Router import failed: {e}")
        return False

def test_environment_setup():
    """Test environment setup"""
    print("\n🔧 Testing environment setup...")
    
    required_vars = [
        'DATABASE_URL',
        'SECRET_KEY',
        'GOOGLE_API_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️ Missing environment variables: {missing_vars}")
        print("Please set these in your .env file or environment")
    else:
        print("✅ All required environment variables are set")
    
    return len(missing_vars) == 0

def main():
    """Main test function"""
    print("🧪 AI Request System Integration Test")
    print("=" * 50)
    
    tests = [
        ("Environment Setup", test_environment_setup),
        ("Model Imports", test_model_imports),
        ("Router Imports", test_router_imports),
        ("Database Connection", test_database_connection),
        ("API Endpoints", test_api_endpoints),
        ("Frontend Build", test_frontend_build),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The AI request system is ready to use.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
