#!/usr/bin/env python3
"""
Staging Startup Script
======================

This script helps start the staging environment and run basic tests.
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def run_command(command, description, check=True):
    """Run a command and return success status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            return True
        else:
            print(f"❌ {description} - Failed")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False

def check_docker():
    """Check if Docker is running"""
    print("🐳 Checking Docker...")
    try:
        result = subprocess.run("docker --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker is available")
            return True
        else:
            print("❌ Docker is not available")
            return False
    except:
        print("❌ Docker is not available")
        return False

def start_services():
    """Start Docker services"""
    print("🚀 Starting Docker services...")
    
    # Start PostgreSQL
    if not run_command("docker-compose up postgres -d", "Starting PostgreSQL"):
        return False
    
    # Wait for PostgreSQL to be ready
    print("⏳ Waiting for PostgreSQL to be ready...")
    time.sleep(10)
    
    # Start Redis
    if not run_command("docker-compose up redis -d", "Starting Redis"):
        return False
    
    # Start ChromaDB
    if not run_command("docker-compose up chromadb -d", "Starting ChromaDB"):
        return False
    
    # Wait for services to be ready
    print("⏳ Waiting for services to be ready...")
    time.sleep(15)
    
    return True

def check_services():
    """Check if services are running"""
    print("🔍 Checking service status...")
    
    # Check Docker containers
    result = subprocess.run("docker ps", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Docker containers status:")
        print(result.stdout)
    else:
        print("❌ Failed to check Docker containers")
        return False
    
    return True

def test_database():
    """Test database connection"""
    print("🗄️ Testing database connection...")
    
    # Test if database exists and has tables
    command = 'docker exec real-estate-rag-chat-system-postgres-1 psql -U admin -d real_estate_db -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = \'public\';"'
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        # Extract table count from output
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if line.strip().isdigit():
                table_count = int(line.strip())
                print(f"✅ Database connected - Found {table_count} tables")
                if table_count >= 30:  # We expect 32 tables
                    return True
                else:
                    print(f"⚠️ Expected 32 tables, found {table_count}")
                    return False
        
        print("❌ Could not determine table count")
        return False
    else:
        print("❌ Database connection failed")
        print(f"   Error: {result.stderr}")
        return False

def start_backend():
    """Start backend server"""
    print("🔧 Starting backend server...")
    
    # Check if backend directory exists
    if not Path("backend").exists():
        print("❌ Backend directory not found")
        return False
    
    # Check if main.py exists
    if not Path("backend/main.py").exists():
        print("❌ backend/main.py not found")
        return False
    
    print("✅ Backend files found")
    print("📝 To start the backend server, run:")
    print("   cd backend")
    print("   python main.py")
    
    return True

def start_frontend():
    """Check frontend setup"""
    print("🎨 Checking frontend setup...")
    
    # Check if frontend directory exists
    if not Path("frontend").exists():
        print("❌ Frontend directory not found")
        return False
    
    # Check if package.json exists
    if not Path("frontend/package.json").exists():
        print("❌ frontend/package.json not found")
        return False
    
    print("✅ Frontend files found")
    print("📝 To start the frontend, run:")
    print("   cd frontend")
    print("   npm install")
    print("   npm start")
    
    return True

def main():
    """Main staging startup function"""
    print("=" * 60)
    print("🚀 AI-POWERED REAL ESTATE ASSISTANT - STAGING STARTUP")
    print("=" * 60)
    print()
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is required but not available. Please install Docker and try again.")
        return False
    
    # Start services
    if not start_services():
        print("❌ Failed to start services")
        return False
    
    # Check services
    if not check_services():
        print("❌ Services are not running properly")
        return False
    
    # Test database
    if not test_database():
        print("❌ Database test failed")
        return False
    
    # Check backend
    if not start_backend():
        print("❌ Backend setup failed")
        return False
    
    # Check frontend
    if not start_frontend():
        print("❌ Frontend setup failed")
        return False
    
    print()
    print("=" * 60)
    print("🎉 STAGING ENVIRONMENT READY!")
    print("=" * 60)
    print()
    print("📋 Next Steps:")
    print("1. Start the backend server:")
    print("   cd backend && python main.py")
    print()
    print("2. Start the frontend (in a new terminal):")
    print("   cd frontend && npm install && npm start")
    print()
    print("3. Run system tests:")
    print("   python test_system.py")
    print()
    print("4. Access the application:")
    print("   Frontend: http://localhost:3000")
    print("   Backend API: http://localhost:8001")
    print()
    print("📖 For detailed testing instructions, see STAGING_TESTING_GUIDE.md")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Startup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Startup failed with error: {e}")
        sys.exit(1)
