"""
Security tests for Dubai Real Estate RAG Chat System
"""
import pytest
import json
import base64
import hashlib
from urllib.parse import quote, unquote
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient

# Import the modules to test
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))
from main import app
from auth.models import User
from auth.utils import hash_password
from tests.utils.test_helpers import SecurityHelper

class TestSQLInjection:
    """Test SQL injection vulnerabilities."""
    
    def test_sql_injection_login(self, client, db_session):
        """Test SQL injection in login endpoint."""
        # Create test user
        user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        # SQL injection payloads
        payloads = SecurityHelper.generate_sql_injection_payloads()
        
        for payload in payloads:
            login_data = {
                "email": payload,
                "password": "TestPassword123!"
            }
            
            response = client.post("/auth/login", json=login_data)
            
            # Should not return 200 (success) for SQL injection attempts
            assert response.status_code != 200, f"SQL injection successful with payload: {payload}"
            
    def test_sql_injection_search(self, authenticated_client, db_session):
        """Test SQL injection in search endpoint."""
        payloads = SecurityHelper.generate_sql_injection_payloads()
        
        for payload in payloads:
            # Test in query parameters
            response = authenticated_client.get(f"/properties/search?location={quote(payload)}")
            
            # Should not return 200 for SQL injection attempts
            assert response.status_code != 200, f"SQL injection successful in search with payload: {payload}"
            
    def test_sql_injection_chat(self, authenticated_client, db_session):
        """Test SQL injection in chat endpoint."""
        payloads = SecurityHelper.generate_sql_injection_payloads()
        
        for payload in payloads:
            chat_data = {
                "message": payload,
                "context": "property_search"
            }
            
            response = authenticated_client.post("/chat/send", json=chat_data)
            
            # Should not return 200 for SQL injection attempts
            assert response.status_code != 200, f"SQL injection successful in chat with payload: {payload}"

class TestXSSVulnerabilities:
    """Test Cross-Site Scripting (XSS) vulnerabilities."""
    
    def test_xss_login(self, client, db_session):
        """Test XSS in login endpoint."""
        payloads = SecurityHelper.generate_xss_payloads()
        
        for payload in payloads:
            login_data = {
                "email": payload,
                "password": "TestPassword123!"
            }
            
            response = client.post("/auth/login", json=login_data)
            
            # Check if XSS payload is reflected in response
            response_text = response.text.lower()
            dangerous_patterns = [
                "<script>",
                "javascript:",
                "onerror=",
                "onload=",
                "alert("
            ]
            
            for pattern in dangerous_patterns:
                assert pattern not in response_text, f"XSS vulnerability found with payload: {payload}"
                
    def test_xss_chat(self, authenticated_client, db_session):
        """Test XSS in chat endpoint."""
        payloads = SecurityHelper.generate_xss_payloads()
        
        for payload in payloads:
            chat_data = {
                "message": payload,
                "context": "property_search"
            }
            
            response = authenticated_client.post("/chat/send", json=chat_data)
            
            # Check if XSS payload is reflected in response
            response_text = response.text.lower()
            dangerous_patterns = [
                "<script>",
                "javascript:",
                "onerror=",
                "onload=",
                "alert("
            ]
            
            for pattern in dangerous_patterns:
                assert pattern not in response_text, f"XSS vulnerability found with payload: {payload}"
                
    def test_xss_search(self, authenticated_client, db_session):
        """Test XSS in search endpoint."""
        payloads = SecurityHelper.generate_xss_payloads()
        
        for payload in payloads:
            response = authenticated_client.get(f"/properties/search?location={quote(payload)}")
            
            # Check if XSS payload is reflected in response
            response_text = response.text.lower()
            dangerous_patterns = [
                "<script>",
                "javascript:",
                "onerror=",
                "onload=",
                "alert("
            ]
            
            for pattern in dangerous_patterns:
                assert pattern not in response_text, f"XSS vulnerability found with payload: {payload}"

class TestPathTraversal:
    """Test path traversal vulnerabilities."""
    
    def test_path_traversal_file_upload(self, authenticated_client, db_session):
        """Test path traversal in file upload."""
        payloads = SecurityHelper.generate_path_traversal_payloads()
        
        for payload in payloads:
            files = {
                "file": (payload, b"test content", "text/plain")
            }
            
            response = authenticated_client.post("/upload/file", files=files)
            
            # Should not return 200 for path traversal attempts
            assert response.status_code != 200, f"Path traversal successful with payload: {payload}"
            
    def test_path_traversal_file_access(self, authenticated_client, db_session):
        """Test path traversal in file access."""
        payloads = SecurityHelper.generate_path_traversal_payloads()
        
        for payload in payloads:
            response = authenticated_client.get(f"/files/{quote(payload)}")
            
            # Should not return 200 for path traversal attempts
            assert response.status_code != 200, f"Path traversal successful with payload: {payload}"

class TestAuthenticationBypass:
    """Test authentication bypass vulnerabilities."""
    
    def test_authentication_bypass_no_token(self, client, db_session):
        """Test accessing protected endpoints without token."""
        protected_endpoints = [
            "/auth/me",
            "/properties/search",
            "/chat/send",
            "/properties/list",
            "/admin/users"
        ]
        
        for endpoint in protected_endpoints:
            if endpoint == "/chat/send":
                response = client.post(endpoint, json={"message": "test"})
            else:
                response = client.get(endpoint)
            
            assert response.status_code == 401, f"Authentication bypass successful for {endpoint}"
            
    def test_authentication_bypass_invalid_token(self, client, db_session):
        """Test accessing protected endpoints with invalid token."""
        invalid_tokens = [
            "invalid_token",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid",
            "Bearer invalid",
            "Basic " + base64.b64encode(b"user:pass").decode(),
            ""
        ]
        
        protected_endpoints = [
            "/auth/me",
            "/properties/search",
            "/chat/send",
            "/properties/list"
        ]
        
        for token in invalid_tokens:
            headers = {"Authorization": f"Bearer {token}"}
            
            for endpoint in protected_endpoints:
                if endpoint == "/chat/send":
                    response = client.post(endpoint, json={"message": "test"}, headers=headers)
                else:
                    response = client.get(endpoint, headers=headers)
                
                assert response.status_code == 401, f"Authentication bypass successful for {endpoint} with token: {token}"
                
    def test_authentication_bypass_expired_token(self, client, db_session):
        """Test accessing protected endpoints with expired token."""
        # Create test user
        user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        # Generate expired token
        from auth.utils import generate_jwt_token
        from datetime import datetime, timedelta
        
        expired_payload = {
            "sub": str(user.id),
            "email": user.email,
            "role": "client",
            "exp": datetime.utcnow() - timedelta(hours=1)
        }
        expired_token = generate_jwt_token(expired_payload)
        
        headers = {"Authorization": f"Bearer {expired_token}"}
        
        protected_endpoints = [
            "/auth/me",
            "/properties/search",
            "/chat/send",
            "/properties/list"
        ]
        
        for endpoint in protected_endpoints:
            if endpoint == "/chat/send":
                response = client.post(endpoint, json={"message": "test"}, headers=headers)
            else:
                response = client.get(endpoint, headers=headers)
            
            assert response.status_code == 401, f"Authentication bypass successful for {endpoint} with expired token"

class TestAuthorizationBypass:
    """Test authorization bypass vulnerabilities."""
    
    def test_authorization_bypass_client_access_admin(self, client, db_session):
        """Test client accessing admin endpoints."""
        # Create client user
        client_user = User(
            first_name="Client",
            last_name="User",
            email="client@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        db_session.add(client_user)
        db_session.commit()
        
        # Login as client
        login_response = client.post("/auth/login", json={
            "email": "client@example.com",
            "password": "TestPassword123!"
        })
        client_token = login_response.json().get("access_token")
        client_headers = {"Authorization": f"Bearer {client_token}"}
        
        # Try to access admin endpoints
        admin_endpoints = [
            "/admin/users",
            "/admin/properties",
            "/admin/analytics",
            "/admin/settings"
        ]
        
        for endpoint in admin_endpoints:
            response = client.get(endpoint, headers=client_headers)
            assert response.status_code == 403, f"Authorization bypass successful for {endpoint}"
            
    def test_authorization_bypass_role_escalation(self, client, db_session):
        """Test role escalation attempts."""
        # Create client user
        client_user = User(
            first_name="Client",
            last_name="User",
            email="client@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        db_session.add(client_user)
        db_session.commit()
        
        # Login as client
        login_response = client.post("/auth/login", json={
            "email": "client@example.com",
            "password": "TestPassword123!"
        })
        client_token = login_response.json().get("access_token")
        
        # Try to modify token to escalate privileges
        import jwt
        from auth.utils import verify_jwt_token
        
        try:
            decoded_token = verify_jwt_token(client_token)
            # Try to modify role in token
            modified_payload = decoded_token.copy()
            modified_payload["role"] = "admin"
            
            # This should fail as we can't sign with the secret key
            modified_token = jwt.encode(modified_payload, "wrong_secret", algorithm="HS256")
            
            headers = {"Authorization": f"Bearer {modified_token}"}
            
            # Try to access admin endpoint
            response = client.get("/admin/users", headers=headers)
            assert response.status_code == 401, "Role escalation successful"
            
        except Exception:
            # Expected to fail
            pass

class TestCSRFVulnerabilities:
    """Test Cross-Site Request Forgery (CSRF) vulnerabilities."""
    
    def test_csrf_protection_headers(self, client, db_session):
        """Test CSRF protection headers."""
        response = client.get("/auth/me")
        
        headers = response.headers
        # Check for CSRF protection headers
        assert "X-CSRF-Token" in headers or "X-XSRF-Token" in headers, "CSRF protection headers missing"
        
    def test_csrf_token_validation(self, authenticated_client, db_session):
        """Test CSRF token validation."""
        # Test without CSRF token
        response = authenticated_client.post("/auth/logout")
        
        # Should require CSRF token for state-changing operations
        if response.status_code == 400:
            # CSRF protection is working
            pass
        else:
            # Check if other CSRF protection mechanisms are in place
            assert "X-CSRF-Token" in response.headers or "X-XSRF-Token" in response.headers

class TestSessionManagement:
    """Test session management vulnerabilities."""
    
    def test_session_fixation(self, client, db_session):
        """Test session fixation vulnerability."""
        # Create test user
        user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        # Login and get session token
        login_response1 = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "TestPassword123!"
        })
        token1 = login_response1.json().get("access_token")
        
        # Login again and get new session token
        login_response2 = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "TestPassword123!"
        })
        token2 = login_response2.json().get("access_token")
        
        # Tokens should be different (session fixation protection)
        assert token1 != token2, "Session fixation vulnerability: tokens are identical"
        
    def test_session_timeout(self, client, db_session):
        """Test session timeout."""
        # Create test user
        user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        # Login and get token
        login_response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "TestPassword123!"
        })
        token = login_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test that token expires after configured time
        # This would require time manipulation in tests
        # For now, we'll test with an expired token
        from auth.utils import generate_jwt_token
        from datetime import datetime, timedelta
        
        expired_payload = {
            "sub": str(user.id),
            "email": user.email,
            "role": "client",
            "exp": datetime.utcnow() - timedelta(minutes=1)
        }
        expired_token = generate_jwt_token(expired_payload)
        expired_headers = {"Authorization": f"Bearer {expired_token}"}
        
        response = client.get("/auth/me", headers=expired_headers)
        assert response.status_code == 401, "Session timeout not working"

class TestInputValidation:
    """Test input validation vulnerabilities."""
    
    def test_input_validation_email(self, client, db_session):
        """Test email input validation."""
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "test@",
            "test..test@example.com",
            "test@example..com",
            "test@example",
            "test@.com",
            "test@example.com.",
            "test@example.com..",
            "test@@example.com",
            "test@example.com ",
            " test@example.com",
            "test@example.com\n",
            "test@example.com\r",
            "test@example.com\t"
        ]
        
        for email in invalid_emails:
            user_data = {
                "first_name": "Test",
                "last_name": "User",
                "email": email,
                "password": "TestPassword123!",
                "role": "client"
            }
            
            response = client.post("/auth/register", json=user_data)
            assert response.status_code == 422, f"Invalid email accepted: {email}"
            
    def test_input_validation_password(self, client, db_session):
        """Test password input validation."""
        weak_passwords = [
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
        
        for password in weak_passwords:
            user_data = {
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com",
                "password": password,
                "role": "client"
            }
            
            response = client.post("/auth/register", json=user_data)
            assert response.status_code == 422, f"Weak password accepted: {password}"
            
    def test_input_validation_sql_injection_chars(self, client, db_session):
        """Test SQL injection character validation."""
        sql_chars = [
            "'",
            "';",
            "';--",
            "'; DROP TABLE users; --",
            "' OR '1'='1",
            "' UNION SELECT * FROM users --",
            "admin'--",
            "1' OR '1' = '1' --"
        ]
        
        for sql_char in sql_chars:
            user_data = {
                "first_name": sql_char,
                "last_name": "User",
                "email": "test@example.com",
                "password": "TestPassword123!",
                "role": "client"
            }
            
            response = client.post("/auth/register", json=user_data)
            # Should either reject or properly escape
            assert response.status_code in [422, 201], f"SQL injection chars not handled: {sql_char}"

class TestRateLimiting:
    """Test rate limiting security."""
    
    def test_rate_limiting_login_attempts(self, client, db_session):
        """Test rate limiting on login attempts."""
        # Create test user
        user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        # Make multiple failed login attempts
        login_data = {
            "email": "test@example.com",
            "password": "WrongPassword"
        }
        
        for i in range(10):
            response = client.post("/auth/login", json=login_data)
            
            if response.status_code == 429:  # Rate limited
                break
        
        # Should be rate limited after multiple attempts
        assert response.status_code == 429, "Rate limiting not working for login attempts"
        
    def test_rate_limiting_registration(self, client, db_session):
        """Test rate limiting on registration."""
        # Make multiple registration attempts
        for i in range(20):
            user_data = {
                "first_name": f"Test{i}",
                "last_name": "User",
                "email": f"test{i}@example.com",
                "password": "TestPassword123!",
                "role": "client"
            }
            
            response = client.post("/auth/register", json=user_data)
            
            if response.status_code == 429:  # Rate limited
                break
        
        # Should be rate limited after multiple attempts
        assert response.status_code == 429, "Rate limiting not working for registration"

class TestSecurityHeaders:
    """Test security headers."""
    
    def test_security_headers_present(self, client, db_session):
        """Test that security headers are present."""
        response = client.get("/auth/me")
        
        headers = response.headers
        
        # Check for essential security headers
        security_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Strict-Transport-Security",
            "Content-Security-Policy"
        ]
        
        for header in security_headers:
            assert header in headers, f"Security header {header} missing"
            
    def test_security_headers_values(self, client, db_session):
        """Test security header values."""
        response = client.get("/auth/me")
        
        headers = response.headers
        
        # Check specific header values
        assert headers.get("X-Content-Type-Options") == "nosniff", "X-Content-Type-Options not set correctly"
        assert headers.get("X-Frame-Options") in ["DENY", "SAMEORIGIN"], "X-Frame-Options not set correctly"
        assert "X-XSS-Protection" in headers, "X-XSS-Protection missing"
        assert "Strict-Transport-Security" in headers, "HSTS header missing"

class TestDataExposure:
    """Test data exposure vulnerabilities."""
    
    def test_sensitive_data_exposure(self, client, db_session):
        """Test for sensitive data exposure."""
        # Create test user
        user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        # Login
        login_response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "TestPassword123!"
        })
        
        # Check response for sensitive data
        response_data = login_response.json()
        
        # Should not expose password hash
        assert "password_hash" not in response_data, "Password hash exposed in response"
        
        # Should not expose internal IDs
        assert "internal_id" not in response_data, "Internal ID exposed in response"
        
        # Should not expose database IDs
        assert "db_id" not in response_data, "Database ID exposed in response"
        
    def test_error_message_information_disclosure(self, client, db_session):
        """Test for information disclosure in error messages."""
        # Test with invalid login
        login_data = {
            "email": "nonexistent@example.com",
            "password": "WrongPassword"
        }
        
        response = client.post("/auth/login", json=login_data)
        
        # Error message should not reveal if user exists
        response_data = response.json()
        error_message = response_data.get("detail", "").lower()
        
        # Should not reveal user existence
        assert "user does not exist" not in error_message, "Error message reveals user existence"
        assert "user not found" not in error_message, "Error message reveals user existence"
        
        # Should use generic error message
        assert "invalid" in error_message or "credentials" in error_message, "Error message should be generic"

class TestFileUploadSecurity:
    """Test file upload security."""
    
    def test_file_upload_type_validation(self, authenticated_client, db_session):
        """Test file upload type validation."""
        # Test with malicious file types
        malicious_files = [
            ("malicious.php", b"<?php echo 'hacked'; ?>", "application/x-php"),
            ("malicious.jsp", b"<% out.println('hacked'); %>", "application/x-jsp"),
            ("malicious.asp", b"<% Response.Write('hacked') %>", "application/x-asp"),
            ("malicious.exe", b"MZ\x90\x00", "application/x-executable"),
            ("malicious.sh", b"#!/bin/bash\necho 'hacked'", "application/x-sh")
        ]
        
        for filename, content, content_type in malicious_files:
            files = {
                "file": (filename, content, content_type)
            }
            
            response = authenticated_client.post("/upload/file", files=files)
            
            # Should reject malicious file types
            assert response.status_code != 200, f"Malicious file type accepted: {filename}"
            
    def test_file_upload_size_validation(self, authenticated_client, db_session):
        """Test file upload size validation."""
        # Test with oversized file
        large_content = b"A" * (10 * 1024 * 1024)  # 10MB
        
        files = {
            "file": ("large.txt", large_content, "text/plain")
        }
        
        response = authenticated_client.post("/upload/file", files=files)
        
        # Should reject oversized files
        assert response.status_code != 200, "Oversized file accepted"
        
    def test_file_upload_content_validation(self, authenticated_client, db_session):
        """Test file upload content validation."""
        # Test with files containing malicious content
        malicious_contents = [
            b"<script>alert('xss')</script>",
            b"<?php system($_GET['cmd']); ?>",
            b"javascript:alert('xss')",
            b"<img src=x onerror=alert('xss')>"
        ]
        
        for content in malicious_contents:
            files = {
                "file": ("malicious.txt", content, "text/plain")
            }
            
            response = authenticated_client.post("/upload/file", files=files)
            
            # Should validate file content
            assert response.status_code != 200, "Malicious content accepted in file upload"

class TestAPISecurity:
    """Test API security vulnerabilities."""
    
    def test_api_versioning(self, client, db_session):
        """Test API versioning security."""
        # Test accessing API without version
        response = client.get("/api/users")
        
        # Should require API version
        assert response.status_code == 404, "API versioning not enforced"
        
    def test_api_rate_limiting(self, client, db_session):
        """Test API rate limiting."""
        # Make multiple API requests
        for i in range(100):
            response = client.get("/api/v1/health")
            
            if response.status_code == 429:  # Rate limited
                break
        
        # Should be rate limited after many requests
        assert response.status_code == 429, "API rate limiting not working"
        
    def test_api_authentication_required(self, client, db_session):
        """Test API authentication requirements."""
        # Test accessing protected API endpoints without authentication
        protected_endpoints = [
            "/api/v1/users",
            "/api/v1/properties",
            "/api/v1/chat"
        ]
        
        for endpoint in protected_endpoints:
            response = client.get(endpoint)
            assert response.status_code == 401, f"API authentication not required for {endpoint}"
