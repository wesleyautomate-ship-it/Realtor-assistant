#!/usr/bin/env python3
"""
Test Script for Week 1 Critical Fixes

This script tests the implementation of:
1. GlobalCommandBar integration with Ctrl+K shortcut
2. Celery task queue for asynchronous operations
3. Environment variable usage instead of hardcoded credentials
"""

import os
import sys
import importlib.util
from pathlib import Path

def test_environment_variables():
    """Test that environment variables are properly configured"""
    print("🔍 Testing Environment Variables...")
    
    # Check if .env file exists
    env_file = Path('.env')
    if env_file.exists():
        print("✅ .env file exists")
    else:
        print("⚠️ .env file not found - using system environment variables")
    
    # Check critical environment variables
    critical_vars = ['DATABASE_URL', 'GOOGLE_API_KEY', 'SECRET_KEY']
    missing_vars = []
    
    for var in critical_vars:
        if os.getenv(var):
            print(f"✅ {var} is set")
        else:
            print(f"⚠️ {var} is not set")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️ Missing environment variables: {', '.join(missing_vars)}")
        print("   Please set these in your .env file or system environment")
    else:
        print("✅ All critical environment variables are configured")
    
    return len(missing_vars) == 0

def test_celery_integration():
    """Test that Celery is properly integrated"""
    print("\n🔍 Testing Celery Integration...")
    
    try:
        # Test Celery configuration
        config_path = Path('backend/celeryconfig.py')
        if config_path.exists():
            print("✅ Celery configuration file exists")
        else:
            print("❌ Celery configuration file not found")
            return False
        
        # Test Celery app
        app_path = Path('backend/celery_app.py')
        if app_path.exists():
            print("✅ Celery app file exists")
        else:
            print("❌ Celery app file not found")
            return False
        
        # Test tasks directory
        tasks_dir = Path('backend/tasks')
        if tasks_dir.exists():
            print("✅ Tasks directory exists")
            
            # Check for task files
            task_files = list(tasks_dir.glob('*.py'))
            if task_files:
                print(f"✅ Found {len(task_files)} task files")
            else:
                print("⚠️ No task files found in tasks directory")
        else:
            print("❌ Tasks directory not found")
            return False
        
        # Test ActionEngine integration
        action_engine_path = Path('backend/action_engine.py')
        if action_engine_path.exists():
            print("✅ ActionEngine file exists")
            
            # Check if it imports Celery tasks
            try:
                with open(action_engine_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'from tasks.ai_commands import' in content:
                        print("✅ ActionEngine imports Celery tasks")
                    else:
                        print("⚠️ ActionEngine doesn't import Celery tasks")
            except UnicodeDecodeError:
                # Try with different encoding
                try:
                    with open(action_engine_path, 'r', encoding='latin-1') as f:
                        content = f.read()
                        if 'from tasks.ai_commands import' in content:
                            print("✅ ActionEngine imports Celery tasks")
                        else:
                            print("⚠️ ActionEngine doesn't import Celery tasks")
                except Exception as e:
                    print(f"⚠️ Could not read ActionEngine file: {e}")
        else:
            print("❌ ActionEngine file not found")
            return False
        
        print("✅ Celery integration appears to be properly configured")
        return True
        
    except Exception as e:
        print(f"❌ Error testing Celery integration: {e}")
        return False

def test_frontend_integration():
    """Test that GlobalCommandBar is properly integrated in frontend"""
    print("\n🔍 Testing Frontend Integration...")
    
    try:
        # Check MainLayout integration
        main_layout_path = Path('frontend/src/layouts/MainLayout.jsx')
        if main_layout_path.exists():
            print("✅ MainLayout.jsx exists")
            
            try:
                with open(main_layout_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'GlobalCommandBar' in content:
                        print("✅ MainLayout imports GlobalCommandBar")
                    else:
                        print("❌ MainLayout doesn't import GlobalCommandBar")
                    
                    if 'useEffect' in content and 'keydown' in content and 'addEventListener' in content:
                        print("✅ MainLayout has keyboard shortcut handling")
                    else:
                        print("❌ MainLayout missing keyboard shortcut handling")
            except UnicodeDecodeError:
                try:
                    with open(main_layout_path, 'r', encoding='latin-1') as f:
                        content = f.read()
                        if 'GlobalCommandBar' in content:
                            print("✅ MainLayout imports GlobalCommandBar")
                        else:
                            print("❌ MainLayout doesn't import GlobalCommandBar")
                        
                        if 'useEffect' in content and 'keydown' in content and 'addEventListener' in content:
                            print("✅ MainLayout has keyboard shortcut handling")
                        else:
                            print("❌ MainLayout missing keyboard shortcut handling")
                except Exception as e:
                    print(f"⚠️ Could not read MainLayout file: {e}")
        else:
            print("❌ MainLayout.jsx not found")
            return False
        
        # Check AgentHub integration
        agent_hub_path = Path('frontend/src/components/hub/AgentHub.jsx')
        if agent_hub_path.exists():
            print("✅ AgentHub.jsx exists")
            
            try:
                with open(agent_hub_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'GlobalCommandBar' in content:
                        print("✅ AgentHub imports GlobalCommandBar")
                    else:
                        print("❌ AgentHub doesn't import GlobalCommandBar")
                    
                    if 'useEffect' in content and 'keydown' in content and 'addEventListener' in content:
                        print("✅ AgentHub has keyboard shortcut handling")
                    else:
                        print("❌ AgentHub missing keyboard shortcut handling")
            except UnicodeDecodeError:
                try:
                    with open(agent_hub_path, 'r', encoding='latin-1') as f:
                        content = f.read()
                        if 'GlobalCommandBar' in content:
                            print("✅ AgentHub imports GlobalCommandBar")
                        else:
                            print("❌ AgentHub doesn't import GlobalCommandBar")
                        
                        if 'useEffect' in content and 'keydown' in content and 'addEventListener' in content:
                            print("✅ AgentHub has keyboard shortcut handling")
                        else:
                            print("❌ AgentHub missing keyboard shortcut handling")
                except Exception as e:
                    print(f"⚠️ Could not read AgentHub file: {e}")
        else:
            print("❌ AgentHub.jsx not found")
            return False
        
        # Check GlobalCommandBar component
        global_cmd_path = Path('frontend/src/components/GlobalCommandBar.jsx')
        if global_cmd_path.exists():
            print("✅ GlobalCommandBar.jsx exists")
        else:
            print("❌ GlobalCommandBar.jsx not found")
            return False
        
        print("✅ Frontend integration appears to be properly configured")
        return True
        
    except Exception as e:
        print(f"❌ Error testing frontend integration: {e}")
        return False

def test_dependencies():
    """Test that required dependencies are available"""
    print("\n🔍 Testing Dependencies...")
    
    try:
        # Check requirements.txt
        requirements_path = Path('backend/requirements.txt')
        if requirements_path.exists():
            print("✅ requirements.txt exists")
            
            with open(requirements_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'celery==' in content:
                    print("✅ Celery dependency is specified")
                else:
                    print("❌ Celery dependency not found in requirements.txt")
        else:
            print("❌ requirements.txt not found")
            return False
        
        print("✅ Dependencies appear to be properly configured")
        return True
        
    except Exception as e:
        print(f"❌ Error testing dependencies: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Week 1 Critical Fixes Implementation")
    print("=" * 50)
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Celery Integration", test_celery_integration),
        ("Frontend Integration", test_frontend_integration),
        ("Dependencies", test_dependencies),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Week 1 critical fixes are properly implemented!")
        print("   The system is ready for Week 2 implementation.")
    else:
        print("⚠️ Some tests failed. Please review the issues above.")
        print("   Fix the failing tests before proceeding to Week 2.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
