#!/usr/bin/env python3
"""
Complete System Integration Test
===============================

This script tests the complete AI request system including:
- Database connectivity
- API endpoints
- File uploads
- AI processing
- Frontend integration
"""

import os
import sys
import requests
import json
import time
import asyncio
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
        ("/docs", "API Documentation"),
        ("/openapi.json", "OpenAPI Schema"),
        ("/api/requests/templates", "Templates Endpoint")
    ]
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code in [200, 401]:  # 401 is expected for protected endpoints
                print(f"✅ {description} - Status: {response.status_code}")
            else:
                print(f"⚠️ {description} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {description} - Error: {e}")
    
    return True

def test_authentication():
    """Test authentication flow"""
    print("\n🔐 Testing authentication...")
    
    base_url = "http://localhost:8001"
    
    # Test login endpoint
    try:
        login_data = {
            "username": "test@example.com",
            "password": "testpassword"
        }
        
        response = requests.post(f"{base_url}/api/auth/login", json=login_data, timeout=5)
        
        if response.status_code == 200:
            print("✅ Authentication endpoint accessible")
            return True
        elif response.status_code == 401:
            print("✅ Authentication endpoint working (invalid credentials)")
            return True
        else:
            print(f"⚠️ Authentication endpoint - Status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Authentication test failed: {e}")
        return False

def test_file_storage():
    """Test file storage service"""
    print("\n📁 Testing file storage...")
    
    try:
        from backend.services.file_storage_service import file_storage
        
        # Test directory creation
        if file_storage.audio_path.exists():
            print("✅ Audio directory exists")
        else:
            print("❌ Audio directory not found")
            return False
        
        if file_storage.deliverables_path.exists():
            print("✅ Deliverables directory exists")
        else:
            print("❌ Deliverables directory not found")
            return False
        
        if file_storage.previews_path.exists():
            print("✅ Previews directory exists")
        else:
            print("❌ Previews directory not found")
            return False
        
        if file_storage.brand_assets_path.exists():
            print("✅ Brand assets directory exists")
        else:
            print("❌ Brand assets directory not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ File storage test failed: {e}")
        return False

def test_ai_processing():
    """Test AI processing service"""
    print("\n🤖 Testing AI processing...")
    
    try:
        from backend.services.ai_processing_service import AIProcessingService
        from backend.auth.database import get_db
        
        # Test service initialization
        db = next(get_db())
        service = AIProcessingService(db)
        
        if service.gemini_model:
            print("✅ AI model configured")
        else:
            print("⚠️ AI model not configured (using mock responses)")
        
        # Test team processors
        teams = ['marketing', 'analytics', 'social', 'strategy', 'packages', 'transactions']
        for team in teams:
            processor = service.get_team_processor(team)
            if processor:
                print(f"✅ {team.title()} processor available")
            else:
                print(f"❌ {team.title()} processor not found")
                return False
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ AI processing test failed: {e}")
        return False

def test_frontend_build():
    """Test if frontend can build successfully"""
    print("\n🎨 Testing frontend build...")
    
    try:
        import subprocess
        import os
        
        # Change to frontend directory
        frontend_dir = Path(__file__).parent / 'frontend'
        os.chdir(frontend_dir)
        
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
        'SECRET_KEY'
    ]
    
    optional_vars = [
        'GOOGLE_API_KEY',
        'UPLOAD_PATH'
    ]
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
    
    for var in optional_vars:
        if not os.getenv(var):
            missing_optional.append(var)
    
    if missing_required:
        print(f"❌ Missing required environment variables: {missing_required}")
        return False
    else:
        print("✅ All required environment variables are set")
    
    if missing_optional:
        print(f"⚠️ Missing optional environment variables: {missing_optional}")
    else:
        print("✅ All optional environment variables are set")
    
    return True

def test_integration_flow():
    """Test a complete integration flow"""
    print("\n🔄 Testing integration flow...")
    
    try:
        # This would test a complete flow from request creation to delivery
        # For now, just verify the components are available
        
        from backend.services.ai_processing_service import AIProcessingService
        from backend.services.file_storage_service import file_storage
        from backend.auth.database import get_db
        
        db = next(get_db())
        
        # Test service initialization
        ai_service = AIProcessingService(db)
        file_service = file_storage
        
        print("✅ AI processing service initialized")
        print("✅ File storage service initialized")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Integration flow test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Complete AI Request System Integration Test")
    print("=" * 60)
    
    tests = [
        ("Environment Setup", test_environment_setup),
        ("Model Imports", test_model_imports),
        ("Router Imports", test_router_imports),
        ("Database Connection", test_database_connection),
        ("File Storage", test_file_storage),
        ("AI Processing", test_ai_processing),
        ("API Endpoints", test_api_endpoints),
        ("Authentication", test_authentication),
        ("Frontend Build", test_frontend_build),
        ("Integration Flow", test_integration_flow),
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
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
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
        print("\n🚀 Next steps:")
        print("1. Run: python start_ai_system.py")
        print("2. Open: http://localhost:3000")
        print("3. Create your first AI request!")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure all dependencies are installed")
        print("2. Check environment variables")
        print("3. Verify database connection")
        print("4. Run database migration if needed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
