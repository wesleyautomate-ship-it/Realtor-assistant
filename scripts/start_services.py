#!/usr/bin/env python3
"""
Service startup script for Dubai Real Estate RAG System
"""

import subprocess
import sys
import os
import time
import signal
import psutil
from typing import List, Dict

class ServiceManager:
    def __init__(self):
        self.processes: Dict[str, subprocess.Popen] = {}
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
    def start_postgresql(self) -> bool:
        """Start PostgreSQL service"""
        print("🗄️  Starting PostgreSQL...")
        
        try:
            # Check if PostgreSQL is already running
            if self.is_service_running("postgresql"):
                print("✅ PostgreSQL is already running")
                return True
            
            # Start PostgreSQL service
            if os.name == 'nt':  # Windows
                result = subprocess.run(
                    ["net", "start", "postgresql-x64-17"],
                    capture_output=True,
                    text=True
                )
            else:  # Linux/Mac
                result = subprocess.run(
                    ["sudo", "systemctl", "start", "postgresql"],
                    capture_output=True,
                    text=True
                )
            
            if result.returncode == 0:
                print("✅ PostgreSQL started successfully")
                return True
            else:
                print(f"❌ Failed to start PostgreSQL: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error starting PostgreSQL: {e}")
            return False
    
    def start_chromadb(self) -> bool:
        """Start ChromaDB service"""
        print("🔍 Starting ChromaDB...")
        
        try:
            # Check if ChromaDB is already running
            if self.is_port_in_use(8000):
                print("✅ ChromaDB is already running on port 8000")
                return True
            
            # Start ChromaDB using Docker
            cmd = [
                "docker", "run", "-d",
                "--name", "chromadb",
                "-p", "8000:8000",
                "chromadb/chroma:latest"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ ChromaDB started successfully")
                return True
            else:
                print(f"❌ Failed to start ChromaDB: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error starting ChromaDB: {e}")
            return False
    
    def start_backend(self) -> bool:
        """Start backend service"""
        print("⚙️  Starting Backend...")
        
        try:
            backend_dir = os.path.join(self.project_root, "backend")
            
            # Check if backend is already running
            if self.is_port_in_use(8001):
                print("✅ Backend is already running on port 8001")
                return True
            
            # Start backend
            cmd = [sys.executable, "main.py"]
            process = subprocess.Popen(
                cmd,
                cwd=backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes["backend"] = process
            
            # Wait a moment for startup
            time.sleep(3)
            
            if process.poll() is None:
                print("✅ Backend started successfully")
                return True
            else:
                stdout, stderr = process.communicate()
                print(f"❌ Backend failed to start: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error starting Backend: {e}")
            return False
    
    def start_frontend(self) -> bool:
        """Start frontend service"""
        print("🌐 Starting Frontend...")
        
        try:
            frontend_dir = os.path.join(self.project_root, "frontend")
            
            # Check if frontend is already running
            if self.is_port_in_use(3000):
                print("✅ Frontend is already running on port 3000")
                return True
            
            # Start frontend
            cmd = ["npm", "start"]
            process = subprocess.Popen(
                cmd,
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes["frontend"] = process
            
            # Wait a moment for startup
            time.sleep(5)
            
            if process.poll() is None:
                print("✅ Frontend started successfully")
                return True
            else:
                stdout, stderr = process.communicate()
                print(f"❌ Frontend failed to start: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error starting Frontend: {e}")
            return False
    
    def is_service_running(self, service_name: str) -> bool:
        """Check if a service is running"""
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(
                    ["sc", "query", service_name],
                    capture_output=True,
                    text=True
                )
                return "RUNNING" in result.stdout
            else:  # Linux/Mac
                result = subprocess.run(
                    ["systemctl", "is-active", service_name],
                    capture_output=True,
                    text=True
                )
                return result.stdout.strip() == "active"
        except:
            return False
    
    def is_port_in_use(self, port: int) -> bool:
        """Check if a port is in use"""
        try:
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return False
        except OSError:
            return True
    
    def wait_for_service(self, url: str, timeout: int = 30) -> bool:
        """Wait for a service to be ready"""
        import requests
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    return True
            except:
                pass
            time.sleep(1)
        return False
    
    def start_all_services(self) -> bool:
        """Start all services"""
        print("🚀 Starting Dubai Real Estate RAG System...")
        print("=" * 50)
        
        services = [
            ("PostgreSQL", self.start_postgresql),
            ("ChromaDB", self.start_chromadb),
            ("Backend", self.start_backend),
            ("Frontend", self.start_frontend)
        ]
        
        for service_name, start_func in services:
            if not start_func():
                print(f"❌ Failed to start {service_name}")
                return False
        
        print("\n" + "=" * 50)
        print("🎉 All services started successfully!")
        print("\n📋 Service URLs:")
        print("   Frontend: http://localhost:3000")
        print("   Backend:  http://localhost:8001")
        print("   ChromaDB: http://localhost:8000")
        print("\n💡 Press Ctrl+C to stop all services")
        
        return True
    
    def stop_all_services(self):
        """Stop all services"""
        print("\n🛑 Stopping services...")
        
        # Stop managed processes
        for name, process in self.processes.items():
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ Stopped {name}")
            except:
                try:
                    process.kill()
                    print(f"⚠️  Force killed {name}")
                except:
                    pass
        
        # Stop ChromaDB container
        try:
            subprocess.run(["docker", "stop", "chromadb"], capture_output=True)
            print("✅ Stopped ChromaDB")
        except:
            pass
        
        print("✅ All services stopped")

def signal_handler(signum, frame):
    """Handle Ctrl+C"""
    print("\n🛑 Received interrupt signal")
    if hasattr(signal_handler, 'manager'):
        signal_handler.manager.stop_all_services()
    sys.exit(0)

def main():
    """Main function"""
    manager = ServiceManager()
    signal_handler.manager = manager
    
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        if manager.start_all_services():
            print("\n🔄 Services are running. Press Ctrl+C to stop.")
            
            # Keep the script running
            while True:
                time.sleep(1)
        else:
            print("❌ Failed to start all services")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        manager.stop_all_services()

if __name__ == "__main__":
    main()
