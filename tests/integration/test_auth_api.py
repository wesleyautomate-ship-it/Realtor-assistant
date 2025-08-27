"""
Integration tests for authentication API endpoints
"""
import pytest
import json
from datetime import datetime, timedelta
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient

# Import the modules to test
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))
from main import app
from auth.models import User, Role, Permission
from auth.utils import hash_password, generate_jwt_token

class TestAuthRegistration:
    """Test user registration endpoint."""
    
    def test_register_user_success(self, client, db_session):
        """Test successful user registration."""
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "TestPassword123!",
            "role": "client"
        }
        
        response = client.post("/auth/register", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "User registered successfully"
        assert data["user"]["email"] == user_data["email"]
        assert data["user"]["first_name"] == user_data["first_name"]
        assert data["user"]["last_name"] == user_data["last_name"]
        assert "password" not in data["user"]
        
    def test_register_user_duplicate_email(self, client, db_session):
        """Test registration with duplicate email."""
        # Create existing user
        existing_user = User(
            first_name="Jane",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        db_session.add(existing_user)
        db_session.commit()
        
        # Try to register with same email
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "TestPassword123!",
            "role": "client"
        }
        
        response = client.post("/auth/register", json=user_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "already exists" in data["detail"].lower()
        
    def test_register_user_invalid_email(self, client, db_session):
        """Test registration with invalid email."""
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email",
            "password": "TestPassword123!",
            "role": "client"
        }
        
        response = client.post("/auth/register", json=user_data)
        
        assert response.status_code == 422
        
    def test_register_user_weak_password(self, client, db_session):
        """Test registration with weak password."""
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "123",  # Weak password
            "role": "client"
        }
        
        response = client.post("/auth/register", json=user_data)
        
        assert response.status_code == 422
        
    def test_register_user_missing_fields(self, client, db_session):
        """Test registration with missing required fields."""
        user_data = {
            "first_name": "John",
            "email": "john.doe@example.com"
            # Missing last_name and password
        }
        
        response = client.post("/auth/register", json=user_data)
        
        assert response.status_code == 422
        
    def test_register_user_invalid_role(self, client, db_session):
        """Test registration with invalid role."""
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "TestPassword123!",
            "role": "invalid_role"
        }
        
        response = client.post("/auth/register", json=user_data)
        
        assert response.status_code == 422

class TestAuthLogin:
    """Test user login endpoint."""
    
    def test_login_success(self, client, db_session):
        """Test successful login."""
        # Create user
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        login_data = {
            "email": "john.doe@example.com",
            "password": "TestPassword123!"
        }
        
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == login_data["email"]
        
    def test_login_invalid_credentials(self, client, db_session):
        """Test login with invalid credentials."""
        # Create user
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        login_data = {
            "email": "john.doe@example.com",
            "password": "WrongPassword"
        }
        
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == 401
        data = response.json()
        assert "invalid" in data["detail"].lower()
        
    def test_login_nonexistent_user(self, client, db_session):
        """Test login with non-existent user."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "TestPassword123!"
        }
        
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == 401
        data = response.json()
        assert "invalid" in data["detail"].lower()
        
    def test_login_inactive_user(self, client, db_session):
        """Test login with inactive user."""
        # Create inactive user
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=False
        )
        db_session.add(user)
        db_session.commit()
        
        login_data = {
            "email": "john.doe@example.com",
            "password": "TestPassword123!"
        }
        
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == 401
        data = response.json()
        assert "inactive" in data["detail"].lower()
        
    def test_login_locked_user(self, client, db_session):
        """Test login with locked user."""
        # Create locked user
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True,
            locked_until=datetime.utcnow() + timedelta(minutes=30)
        )
        db_session.add(user)
        db_session.commit()
        
        login_data = {
            "email": "john.doe@example.com",
            "password": "TestPassword123!"
        }
        
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == 423  # Locked
        data = response.json()
        assert "locked" in data["detail"].lower()
        
    def test_login_missing_fields(self, client, db_session):
        """Test login with missing fields."""
        login_data = {
            "email": "john.doe@example.com"
            # Missing password
        }
        
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == 422

class TestAuthLogout:
    """Test user logout endpoint."""
    
    def test_logout_success(self, authenticated_client, db_session):
        """Test successful logout."""
        response = authenticated_client.post("/auth/logout")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Logged out successfully"
        
    def test_logout_without_token(self, client, db_session):
        """Test logout without authentication token."""
        response = client.post("/auth/logout")
        
        assert response.status_code == 401
        
    def test_logout_invalid_token(self, client, db_session):
        """Test logout with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.post("/auth/logout", headers=headers)
        
        assert response.status_code == 401

class TestAuthRefresh:
    """Test token refresh endpoint."""
    
    def test_refresh_token_success(self, client, db_session):
        """Test successful token refresh."""
        # Create user
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        # Generate refresh token
        from auth.utils import generate_refresh_token
        refresh_token = generate_refresh_token(user.id)
        
        refresh_data = {"refresh_token": refresh_token}
        
        response = client.post("/auth/refresh", json=refresh_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        
    def test_refresh_token_invalid(self, client, db_session):
        """Test refresh with invalid token."""
        refresh_data = {"refresh_token": "invalid_token"}
        
        response = client.post("/auth/refresh", json=refresh_data)
        
        assert response.status_code == 401
        
    def test_refresh_token_expired(self, client, db_session):
        """Test refresh with expired token."""
        # Create user
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        # Generate expired refresh token
        payload = {
            "sub": str(user.id),
            "type": "refresh",
            "exp": datetime.utcnow() - timedelta(hours=1)
        }
        expired_token = generate_jwt_token(payload)
        
        refresh_data = {"refresh_token": expired_token}
        
        response = client.post("/auth/refresh", json=refresh_data)
        
        assert response.status_code == 401
        
    def test_refresh_token_missing(self, client, db_session):
        """Test refresh without token."""
        response = client.post("/auth/refresh", json={})
        
        assert response.status_code == 422

class TestAuthMe:
    """Test current user endpoint."""
    
    def test_get_current_user_success(self, authenticated_client, db_session):
        """Test successful current user retrieval."""
        response = authenticated_client.get("/auth/me")
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "email" in data
        assert "first_name" in data
        assert "last_name" in data
        assert "password" not in data
        
    def test_get_current_user_unauthorized(self, client, db_session):
        """Test current user without authentication."""
        response = client.get("/auth/me")
        
        assert response.status_code == 401
        
    def test_get_current_user_invalid_token(self, client, db_session):
        """Test current user with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/auth/me", headers=headers)
        
        assert response.status_code == 401

class TestAuthForgotPassword:
    """Test forgot password endpoint."""
    
    def test_forgot_password_success(self, client, db_session):
        """Test successful forgot password request."""
        # Create user
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        forgot_data = {"email": "john.doe@example.com"}
        
        with patch('auth.routes.send_reset_email') as mock_send_email:
            mock_send_email.return_value = True
            
            response = client.post("/auth/forgot-password", json=forgot_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "reset email sent" in data["message"].lower()
            
    def test_forgot_password_nonexistent_user(self, client, db_session):
        """Test forgot password with non-existent user."""
        forgot_data = {"email": "nonexistent@example.com"}
        
        response = client.post("/auth/forgot-password", json=forgot_data)
        
        # Should return success to prevent email enumeration
        assert response.status_code == 200
        
    def test_forgot_password_inactive_user(self, client, db_session):
        """Test forgot password with inactive user."""
        # Create inactive user
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=False
        )
        db_session.add(user)
        db_session.commit()
        
        forgot_data = {"email": "john.doe@example.com"}
        
        response = client.post("/auth/forgot-password", json=forgot_data)
        
        # Should return success to prevent email enumeration
        assert response.status_code == 200
        
    def test_forgot_password_invalid_email(self, client, db_session):
        """Test forgot password with invalid email."""
        forgot_data = {"email": "invalid-email"}
        
        response = client.post("/auth/forgot-password", json=forgot_data)
        
        assert response.status_code == 422

class TestAuthResetPassword:
    """Test reset password endpoint."""
    
    def test_reset_password_success(self, client, db_session):
        """Test successful password reset."""
        # Create user
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        # Generate reset token
        from auth.utils import generate_secure_token
        reset_token = generate_secure_token()
        
        reset_data = {
            "token": reset_token,
            "new_password": "NewPassword123!"
        }
        
        with patch('auth.routes.verify_reset_token') as mock_verify:
            mock_verify.return_value = user.email
            
            response = client.post("/auth/reset-password", json=reset_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "password reset" in data["message"].lower()
            
    def test_reset_password_invalid_token(self, client, db_session):
        """Test password reset with invalid token."""
        reset_data = {
            "token": "invalid_token",
            "new_password": "NewPassword123!"
        }
        
        with patch('auth.routes.verify_reset_token') as mock_verify:
            mock_verify.return_value = None
            
            response = client.post("/auth/reset-password", json=reset_data)
            
            assert response.status_code == 400
            data = response.json()
            assert "invalid" in data["detail"].lower()
            
    def test_reset_password_weak_password(self, client, db_session):
        """Test password reset with weak password."""
        reset_data = {
            "token": "valid_token",
            "new_password": "123"  # Weak password
        }
        
        response = client.post("/auth/reset-password", json=reset_data)
        
        assert response.status_code == 422
        
    def test_reset_password_missing_fields(self, client, db_session):
        """Test password reset with missing fields."""
        reset_data = {"token": "valid_token"}
        # Missing new_password
        
        response = client.post("/auth/reset-password", json=reset_data)
        
        assert response.status_code == 422

class TestAuthRateLimiting:
    """Test rate limiting on authentication endpoints."""
    
    def test_login_rate_limiting(self, client, db_session):
        """Test rate limiting on login endpoint."""
        # Create user
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        login_data = {
            "email": "john.doe@example.com",
            "password": "WrongPassword"
        }
        
        # Make multiple failed login attempts
        for _ in range(6):  # More than the limit
            response = client.post("/auth/login", json=login_data)
            
        # Should be rate limited
        assert response.status_code == 429
        
    def test_register_rate_limiting(self, client, db_session):
        """Test rate limiting on register endpoint."""
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@example.com",
            "password": "TestPassword123!",
            "role": "client"
        }
        
        # Make multiple registration attempts
        for i in range(10):
            user_data["email"] = f"test{i}@example.com"
            response = client.post("/auth/register", json=user_data)
            
        # Should be rate limited
        assert response.status_code == 429

class TestAuthSecurityHeaders:
    """Test security headers on authentication endpoints."""
    
    def test_security_headers_present(self, client, db_session):
        """Test that security headers are present."""
        response = client.get("/auth/me")
        
        headers = response.headers
        assert "X-Content-Type-Options" in headers
        assert "X-Frame-Options" in headers
        assert "X-XSS-Protection" in headers
        assert "Strict-Transport-Security" in headers
        
    def test_cors_headers(self, client, db_session):
        """Test CORS headers."""
        response = client.options("/auth/login")
        
        headers = response.headers
        assert "Access-Control-Allow-Origin" in headers
        assert "Access-Control-Allow-Methods" in headers
        assert "Access-Control-Allow-Headers" in headers

class TestAuthAuditLogging:
    """Test audit logging for authentication events."""
    
    def test_login_audit_log(self, client, db_session):
        """Test that login events are logged."""
        # Create user
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        login_data = {
            "email": "john.doe@example.com",
            "password": "TestPassword123!"
        }
        
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == 200
        
        # Check that audit log was created
        from auth.models import AuditLog
        audit_logs = db_session.query(AuditLog).filter_by(
            user_id=user.id,
            action="login"
        ).all()
        
        assert len(audit_logs) > 0
        
    def test_failed_login_audit_log(self, client, db_session):
        """Test that failed login events are logged."""
        # Create user
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        login_data = {
            "email": "john.doe@example.com",
            "password": "WrongPassword"
        }
        
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == 401
        
        # Check that audit log was created
        from auth.models import AuditLog
        audit_logs = db_session.query(AuditLog).filter_by(
            user_id=user.id,
            action="login_failed"
        ).all()
        
        assert len(audit_logs) > 0

class TestAuthErrorHandling:
    """Test error handling in authentication endpoints."""
    
    def test_database_error_handling(self, client, db_session):
        """Test handling of database errors."""
        with patch('auth.routes.get_db') as mock_get_db:
            mock_get_db.side_effect = Exception("Database error")
            
            user_data = {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "password": "TestPassword123!",
                "role": "client"
            }
            
            response = client.post("/auth/register", json=user_data)
            
            assert response.status_code == 500
            
    def test_validation_error_handling(self, client, db_session):
        """Test handling of validation errors."""
        user_data = {
            "first_name": "",  # Invalid
            "last_name": "Doe",
            "email": "invalid-email",
            "password": "123",  # Too short
            "role": "invalid_role"
        }
        
        response = client.post("/auth/register", json=user_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        
    def test_authentication_error_handling(self, client, db_session):
        """Test handling of authentication errors."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/auth/me", headers=headers)
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
