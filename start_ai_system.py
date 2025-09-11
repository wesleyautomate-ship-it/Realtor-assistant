#!/usr/bin/env python3
"""
AI Request System Startup Script
===============================

This script starts the complete AI request system including:
- Database migration
- Backend server
- Frontend development server
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

def run_command(command, cwd=None, background=False):
    """Run a command and return the process"""
    print(f"🚀 Running: {command}")
    
    if background:
        process = subprocess.Popen(
            command,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return process
    else:
        result = subprocess.run(command, shell=True, cwd=cwd)
        return result.returncode == 0

def check_dependencies():
    """Check if all dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python dependencies
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        print("✅ Python dependencies OK")
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        return False
    
    # Check Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js version: {result.stdout.strip()}")
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found")
        return False
    
    # Check npm
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm version: {result.stdout.strip()}")
        else:
            print("❌ npm not found")
            return False
    except FileNotFoundError:
        print("❌ npm not found")
        return False
    
    return True

def setup_environment():
    """Setup environment variables"""
    print("🔧 Setting up environment...")
    
    # Set default environment variables if not set
    env_vars = {
        'DATABASE_URL': 'postgresql://postgres:password@localhost:5432/dubai_real_estate',
        'SECRET_KEY': 'your-secret-key-change-in-production',
        'GOOGLE_API_KEY': 'your-google-api-key',
        'UPLOAD_PATH': 'uploads',
        'REACT_APP_API_URL': 'http://localhost:8001'
    }
    
    for key, default_value in env_vars.items():
        if not os.getenv(key):
            os.environ[key] = default_value
            print(f"⚠️ Set {key} to default value")
        else:
            print(f"✅ {key} is set")
    
    return True

def run_database_migration():
    """Run database migration"""
    print("🗄️ Running database migration...")
    
    try:
        result = subprocess.run([sys.executable, 'run_ai_migration.py'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Database migration completed")
            return True
        else:
            print(f"❌ Database migration failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Database migration error: {e}")
        return False

def install_frontend_dependencies():
    """Install frontend dependencies"""
    print("📦 Installing frontend dependencies...")
    
    frontend_dir = Path(__file__).parent / 'frontend'
    
    try:
        result = subprocess.run(['npm', 'install'], cwd=frontend_dir, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Frontend dependencies installed")
            return True
        else:
            print(f"❌ Frontend dependency installation failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Frontend dependency installation error: {e}")
        return False

def start_backend():
    """Start the backend server"""
    print("🔧 Starting backend server...")
    
    backend_dir = Path(__file__).parent / 'backend'
    
    try:
        process = subprocess.Popen(
            [sys.executable, '-m', 'uvicorn', 'main:app', '--host', '0.0.0.0', '--port', '8001', '--reload'],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a moment to see if it starts successfully
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ Backend server started on http://localhost:8001")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Backend server failed to start: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Backend server error: {e}")
        return None

def start_frontend():
    """Start the frontend development server"""
    print("🎨 Starting frontend server...")
    
    frontend_dir = Path(__file__).parent / 'frontend'
    
    try:
        process = subprocess.Popen(
            ['npm', 'start'],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a moment to see if it starts successfully
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ Frontend server started on http://localhost:3000")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Frontend server failed to start: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Frontend server error: {e}")
        return None

def main():
    """Main function"""
    print("🎯 AI Request System Startup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed. Please install missing dependencies.")
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        print("❌ Environment setup failed.")
        sys.exit(1)
    
    # Run database migration
    if not run_database_migration():
        print("❌ Database migration failed.")
        sys.exit(1)
    
    # Install frontend dependencies
    if not install_frontend_dependencies():
        print("❌ Frontend dependency installation failed.")
        sys.exit(1)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend server.")
        sys.exit(1)
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Failed to start frontend server.")
        backend_process.terminate()
        sys.exit(1)
    
    print("\n🎉 AI Request System is running!")
    print("=" * 50)
    print("🌐 Frontend: http://localhost:3000")
    print("🔧 Backend API: http://localhost:8001")
    print("📚 API Docs: http://localhost:8001/docs")
    print("=" * 50)
    print("Press Ctrl+C to stop all services")
    
    try:
        # Wait for processes
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("❌ Backend server stopped unexpectedly")
                break
            
            if frontend_process.poll() is not None:
                print("❌ Frontend server stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        
        # Terminate processes
        if backend_process:
            backend_process.terminate()
            print("✅ Backend server stopped")
        
        if frontend_process:
            frontend_process.terminate()
            print("✅ Frontend server stopped")
        
        print("👋 AI Request System stopped")

if __name__ == "__main__":
    main()
