"""
Test utilities and helpers for Dubai Real Estate RAG Chat System
"""
import json
import time
import hashlib
import random
import string
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import jwt
from unittest.mock import Mock, patch
import requests
from fastapi.testclient import TestClient

class TestDataGenerator:
    """Generate test data for various scenarios."""
    
    @staticmethod
    def generate_user_data(role: str = "client", **kwargs) -> Dict[str, Any]:
        """Generate user data for testing."""
        base_data = {
            "first_name": f"Test{random.randint(1000, 9999)}",
            "last_name": f"User{random.randint(1000, 9999)}",
            "email": f"test{random.randint(1000, 9999)}@example.com",
            "password": "TestPassword123!",
            "role": role
        }
        base_data.update(kwargs)
        return base_data
    
    @staticmethod
    def generate_property_data(**kwargs) -> Dict[str, Any]:
        """Generate property data for testing."""
        locations = ["Dubai Marina", "Palm Jumeirah", "Downtown Dubai", "JBR", "Emirates Hills"]
        property_types = ["apartment", "villa", "townhouse", "penthouse"]
        
        base_data = {
            "title": f"Luxury {random.choice(property_types).title()} in {random.choice(locations)}",
            "description": f"Beautiful {random.randint(2, 5)}-bedroom property with amazing views",
            "price": random.randint(1000000, 10000000),
            "location": random.choice(locations),
            "property_type": random.choice(property_types),
            "bedrooms": random.randint(1, 5),
            "bathrooms": random.randint(1, 4),
            "area_sqft": random.randint(1000, 5000),
            "amenities": random.sample(["pool", "gym", "parking", "balcony", "garden"], random.randint(2, 4)),
            "status": random.choice(["available", "sold", "under_contract"])
        }
        base_data.update(kwargs)
        return base_data
    
    @staticmethod
    def generate_chat_data(**kwargs) -> Dict[str, Any]:
        """Generate chat data for testing."""
        messages = [
            "I'm looking for properties in Dubai Marina under 3 million AED",
            "Show me luxury villas in Palm Jumeirah",
            "What are the best investment properties in Downtown Dubai?",
            "I need a 2-bedroom apartment with sea view",
            "What's the market trend for properties in JBR?"
        ]
        
        base_data = {
            "message": random.choice(messages),
            "context": "property_search",
            "user_preferences": {
                "location": random.choice(["Dubai Marina", "Palm Jumeirah", "Downtown Dubai"]),
                "max_price": random.randint(2000000, 8000000),
                "property_type": random.choice(["apartment", "villa", "penthouse"])
            }
        }
        base_data.update(kwargs)
        return base_data
    
    @staticmethod
    def generate_file_content(file_type: str = "pdf") -> bytes:
        """Generate mock file content for testing."""
        if file_type == "pdf":
            return b"%PDF-1.4\nMock PDF content for testing\n%%EOF"
        elif file_type == "image":
            return b"Mock image content for testing"
        elif file_type == "document":
            return b"Mock document content for testing"
        else:
            return b"Mock file content for testing"

class AuthenticationHelper:
    """Helper for authentication testing."""
    
    @staticmethod
    def create_test_token(user_id: int, email: str, role: str = "client") -> str:
        """Create a test JWT token."""
        payload = {
            "sub": str(user_id),
            "email": email,
            "role": role,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        return jwt.encode(payload, "test_secret_key", algorithm="HS256")
    
    @staticmethod
    def get_auth_headers(token: str) -> Dict[str, str]:
        """Get authentication headers."""
        return {"Authorization": f"Bearer {token}"}
    
    @staticmethod
    def login_user(client: TestClient, email: str, password: str) -> Optional[str]:
        """Login user and return access token."""
        response = client.post("/auth/login", json={
            "email": email,
            "password": password
        })
        if response.status_code == 200:
            return response.json().get("access_token")
        return None

class PerformanceHelper:
    """Helper for performance testing."""
    
    @staticmethod
    def measure_response_time(func, *args, **kwargs) -> float:
        """Measure function execution time."""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        return end_time - start_time
    
    @staticmethod
    def concurrent_requests(client: TestClient, endpoint: str, num_requests: int, 
                          data: Dict = None, headers: Dict = None) -> List[Dict]:
        """Make concurrent requests and return results."""
        import threading
        import queue
        
        results = queue.Queue()
        
        def make_request():
            try:
                if data:
                    response = client.post(endpoint, json=data, headers=headers)
                else:
                    response = client.get(endpoint, headers=headers)
                results.put({
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "success": response.status_code < 400
                })
            except Exception as e:
                results.put({
                    "status_code": 500,
                    "response_time": 0,
                    "success": False,
                    "error": str(e)
                })
        
        threads = []
        for _ in range(num_requests):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        return list(results.queue)
    
    @staticmethod
    def calculate_performance_metrics(results: List[Dict]) -> Dict[str, float]:
        """Calculate performance metrics from test results."""
        if not results:
            return {}
        
        response_times = [r.get("response_time", 0) for r in results]
        success_count = sum(1 for r in results if r.get("success", False))
        
        return {
            "total_requests": len(results),
            "successful_requests": success_count,
            "success_rate": success_count / len(results) * 100,
            "average_response_time": sum(response_times) / len(response_times),
            "min_response_time": min(response_times),
            "max_response_time": max(response_times),
            "median_response_time": sorted(response_times)[len(response_times) // 2]
        }

class SecurityHelper:
    """Helper for security testing."""
    
    @staticmethod
    def generate_sql_injection_payloads() -> List[str]:
        """Generate SQL injection test payloads."""
        return [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "' UNION SELECT * FROM users --",
            "admin'--",
            "1' OR '1' = '1' --",
            "'; INSERT INTO users VALUES ('hacker', 'password'); --"
        ]
    
    @staticmethod
    def generate_xss_payloads() -> List[str]:
        """Generate XSS test payloads."""
        return [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "';alert('XSS');//",
            "<svg onload=alert('XSS')>",
            "&#60;script&#62;alert('XSS')&#60;/script&#62;"
        ]
    
    @staticmethod
    def generate_path_traversal_payloads() -> List[str]:
        """Generate path traversal test payloads."""
        return [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "....//....//....//etc/passwd",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
            "..%252f..%252f..%252fetc%252fpasswd"
        ]
    
    @staticmethod
    def test_rate_limiting(client: TestClient, endpoint: str, max_requests: int) -> Dict[str, Any]:
        """Test rate limiting on an endpoint."""
        results = []
        for i in range(max_requests + 5):  # Try a few more than the limit
            response = client.get(endpoint)
            results.append({
                "request_number": i + 1,
                "status_code": response.status_code,
                "headers": dict(response.headers)
            })
            if response.status_code == 429:  # Too Many Requests
                break
        
        return {
            "total_requests": len(results),
            "rate_limited_at": next((i for i, r in enumerate(results) if r["status_code"] == 429), None),
            "results": results
        }

class DatabaseHelper:
    """Helper for database testing."""
    
    @staticmethod
    def clean_database(session):
        """Clean all tables in the database."""
        from auth.models import User, Role, Permission, UserSession, AuditLog
        
        tables = [UserSession, AuditLog, User, Role, Permission]
        for table in tables:
            session.query(table).delete()
        session.commit()
    
    @staticmethod
    def create_test_data(session):
        """Create test data in the database."""
        from auth.models import User, Role, Permission
        from auth.utils import hash_password
        
        # Create roles
        roles = {
            "client": Role(name="client", description="Client role"),
            "agent": Role(name="agent", description="Agent role"),
            "employee": Role(name="employee", description="Employee role"),
            "admin": Role(name="admin", description="Admin role")
        }
        
        for role in roles.values():
            session.add(role)
        session.commit()
        
        # Create permissions
        permissions = [
            Permission(name="property_read", description="Read property data"),
            Permission(name="property_write", description="Write property data"),
            Permission(name="chat_read", description="Read chat messages"),
            Permission(name="chat_write", description="Write chat messages"),
            Permission(name="user_read", description="Read user data"),
            Permission(name="user_write", description="Write user data"),
            Permission(name="admin_access", description="Admin access")
        ]
        
        for permission in permissions:
            session.add(permission)
        session.commit()
        
        # Create test users
        users = [
            User(
                first_name="Test",
                last_name="Client",
                email="client@test.com",
                password_hash=hash_password("TestPassword123!"),
                is_active=True
            ),
            User(
                first_name="Test",
                last_name="Agent",
                email="agent@test.com",
                password_hash=hash_password("TestPassword123!"),
                is_active=True
            ),
            User(
                first_name="Test",
                last_name="Admin",
                email="admin@test.com",
                password_hash=hash_password("TestPassword123!"),
                is_active=True
            )
        ]
        
        for user in users:
            session.add(user)
        session.commit()
        
        return {"roles": roles, "users": users, "permissions": permissions}

class FileHelper:
    """Helper for file upload testing."""
    
    @staticmethod
    def create_test_file(filename: str, content: bytes = None) -> tuple:
        """Create a test file for upload testing."""
        if content is None:
            content = b"Test file content"
        
        return (filename, content, "application/octet-stream")
    
    @staticmethod
    def create_test_files() -> Dict[str, tuple]:
        """Create various test files."""
        return {
            "pdf": ("test.pdf", b"%PDF-1.4\nTest PDF content", "application/pdf"),
            "image": ("test.jpg", b"Test image content", "image/jpeg"),
            "document": ("test.docx", b"Test document content", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
            "text": ("test.txt", b"Test text content", "text/plain")
        }

class ValidationHelper:
    """Helper for input validation testing."""
    
    @staticmethod
    def generate_invalid_emails() -> List[str]:
        """Generate invalid email addresses for testing."""
        return [
            "invalid-email",
            "@example.com",
            "test@",
            "test..test@example.com",
            "test@example..com",
            "test@example",
            "test@.com",
            "test@example.com.",
            "test@example.com..",
            "test@@example.com"
        ]
    
    @staticmethod
    def generate_weak_passwords() -> List[str]:
        """Generate weak passwords for testing."""
        return [
            "123456",
            "password",
            "qwerty",
            "abc123",
            "password123",
            "admin",
            "letmein",
            "welcome",
            "monkey",
            "123456789"
        ]
    
    @staticmethod
    def generate_valid_passwords() -> List[str]:
        """Generate valid passwords for testing."""
        return [
            "StrongPassword123!",
            "SecurePass456@",
            "MyPassword789#",
            "ComplexPass2023$",
            "SafePassword321%"
        ]

class MockHelper:
    """Helper for creating mocks."""
    
    @staticmethod
    def mock_google_ai_response(response_text: str = "Mock AI response"):
        """Mock Google AI response."""
        mock_response = Mock()
        mock_response.text = response_text
        return mock_response
    
    @staticmethod
    def mock_redis_connection():
        """Mock Redis connection."""
        mock_redis = Mock()
        mock_redis.get.return_value = None
        mock_redis.set.return_value = True
        mock_redis.delete.return_value = True
        mock_redis.exists.return_value = False
        return mock_redis
    
    @staticmethod
    def mock_chroma_collection():
        """Mock ChromaDB collection."""
        mock_collection = Mock()
        mock_collection.add.return_value = {"ids": ["test_id"]}
        mock_collection.query.return_value = {
            "documents": [["Test document"]],
            "metadatas": [[{"source": "test"}]],
            "distances": [[0.1]]
        }
        return mock_collection
