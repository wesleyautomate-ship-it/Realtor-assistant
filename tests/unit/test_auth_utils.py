"""
Unit tests for authentication utilities
"""
import pytest
import jwt
from datetime import datetime, timedelta
from unittest.mock import patch, Mock
import bcrypt

# Import the modules to test
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))
from auth.utils import (
    hash_password,
    verify_password,
    generate_jwt_token,
    verify_jwt_token,
    generate_access_token,
    generate_refresh_token,
    generate_session_token,
    validate_email_address,
    validate_password_strength,
    generate_secure_token,
    sanitize_input,
    validate_username,
    get_password_requirements
)

class TestPasswordManagement:
    """Test password hashing and verification."""
    
    def test_hash_password(self):
        """Test password hashing."""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        assert hashed != password
        assert isinstance(hashed, str)
        assert len(hashed) > 0
        
    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
        
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "TestPassword123!"
        wrong_password = "WrongPassword123!"
        hashed = hash_password(password)
        
        assert verify_password(wrong_password, hashed) is False
        
    def test_verify_password_empty(self):
        """Test password verification with empty password."""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        assert verify_password("", hashed) is False
        
    def test_hash_password_empty(self):
        """Test hashing empty password."""
        with pytest.raises(ValueError):
            hash_password("")
            
    def test_hash_password_none(self):
        """Test hashing None password."""
        with pytest.raises(ValueError):
            hash_password(None)

class TestJWTTokenManagement:
    """Test JWT token generation and verification."""
    
    def test_generate_jwt_token(self):
        """Test JWT token generation."""
        payload = {"user_id": 123, "email": "test@example.com"}
        token = generate_jwt_token(payload)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
    def test_verify_jwt_token_valid(self):
        """Test JWT token verification with valid token."""
        payload = {"user_id": 123, "email": "test@example.com"}
        token = generate_jwt_token(payload)
        
        decoded = verify_jwt_token(token)
        assert decoded["user_id"] == 123
        assert decoded["email"] == "test@example.com"
        
    def test_verify_jwt_token_invalid(self):
        """Test JWT token verification with invalid token."""
        invalid_token = "invalid.token.here"
        
        with pytest.raises(jwt.InvalidTokenError):
            verify_jwt_token(invalid_token)
            
    def test_verify_jwt_token_expired(self):
        """Test JWT token verification with expired token."""
        payload = {
            "user_id": 123,
            "email": "test@example.com",
            "exp": datetime.utcnow() - timedelta(hours=1)
        }
        token = generate_jwt_token(payload)
        
        with pytest.raises(jwt.ExpiredSignatureError):
            verify_jwt_token(token)
            
    def test_generate_access_token(self):
        """Test access token generation."""
        user_id = 123
        email = "test@example.com"
        role = "client"
        
        token = generate_access_token(user_id, email, role)
        
        assert isinstance(token, str)
        decoded = verify_jwt_token(token)
        assert decoded["sub"] == str(user_id)
        assert decoded["email"] == email
        assert decoded["role"] == role
        
    def test_generate_refresh_token(self):
        """Test refresh token generation."""
        user_id = 123
        
        token = generate_refresh_token(user_id)
        
        assert isinstance(token, str)
        decoded = verify_jwt_token(token)
        assert decoded["sub"] == str(user_id)
        assert decoded["type"] == "refresh"
        
    def test_generate_session_token(self):
        """Test session token generation."""
        user_id = 123
        session_id = "session123"
        
        token = generate_session_token(user_id, session_id)
        
        assert isinstance(token, str)
        decoded = verify_jwt_token(token)
        assert decoded["sub"] == str(user_id)
        assert decoded["session_id"] == session_id

class TestInputValidation:
    """Test input validation functions."""
    
    @pytest.mark.parametrize("email,expected", [
        ("test@example.com", True),
        ("user.name@domain.co.uk", True),
        ("invalid-email", False),
        ("@example.com", False),
        ("test@", False),
        ("test..test@example.com", False),
        ("test@example..com", False),
        ("", False),
        (None, False),
    ])
    def test_validate_email_address(self, email, expected):
        """Test email address validation."""
        assert validate_email_address(email) == expected
        
    @pytest.mark.parametrize("password,expected", [
        ("StrongPassword123!", True),
        ("SecurePass456@", True),
        ("MyPassword789#", True),
        ("123456", False),  # Too short
        ("password", False),  # No uppercase, numbers, or special chars
        ("PASSWORD", False),  # No lowercase, numbers, or special chars
        ("Password", False),  # No numbers or special chars
        ("Password123", False),  # No special chars
        ("", False),
        (None, False),
    ])
    def test_validate_password_strength(self, password, expected):
        """Test password strength validation."""
        assert validate_password_strength(password) == expected
        
    @pytest.mark.parametrize("username,expected", [
        ("john_doe", True),
        ("user123", True),
        ("john.doe", True),
        ("a", False),  # Too short
        ("very_long_username_that_exceeds_maximum_length", False),  # Too long
        ("user@name", False),  # Invalid characters
        ("user name", False),  # Spaces not allowed
        ("", False),
        (None, False),
    ])
    def test_validate_username(self, username, expected):
        """Test username validation."""
        assert validate_username(username) == expected
        
    @pytest.mark.parametrize("input_text,expected", [
        ("<script>alert('xss')</script>", "&lt;script&gt;alert('xss')&lt;/script&gt;"),
        ("Hello World", "Hello World"),
        ("", ""),
        ("<img src=x onerror=alert('xss')>", "&lt;img src=x onerror=alert('xss')&gt;"),
        ("javascript:alert('xss')", "javascript:alert('xss')"),
    ])
    def test_sanitize_input(self, input_text, expected):
        """Test input sanitization."""
        assert sanitize_input(input_text) == expected

class TestTokenGeneration:
    """Test secure token generation."""
    
    def test_generate_secure_token(self):
        """Test secure token generation."""
        token = generate_secure_token()
        
        assert isinstance(token, str)
        assert len(token) > 0
        
    def test_generate_secure_token_length(self):
        """Test secure token generation with custom length."""
        token = generate_secure_token(length=32)
        
        assert isinstance(token, str)
        assert len(token) == 32
        
    def test_generate_secure_token_unique(self):
        """Test that generated tokens are unique."""
        tokens = set()
        for _ in range(100):
            token = generate_secure_token()
            assert token not in tokens
            tokens.add(token)

class TestPasswordRequirements:
    """Test password requirements function."""
    
    def test_get_password_requirements(self):
        """Test password requirements retrieval."""
        requirements = get_password_requirements()
        
        assert isinstance(requirements, dict)
        assert "min_length" in requirements
        assert "require_uppercase" in requirements
        assert "require_lowercase" in requirements
        assert "require_numbers" in requirements
        assert "require_special_chars" in requirements
        
    def test_password_requirements_values(self):
        """Test password requirements have correct values."""
        requirements = get_password_requirements()
        
        assert requirements["min_length"] >= 8
        assert isinstance(requirements["require_uppercase"], bool)
        assert isinstance(requirements["require_lowercase"], bool)
        assert isinstance(requirements["require_numbers"], bool)
        assert isinstance(requirements["require_special_chars"], bool)

class TestErrorHandling:
    """Test error handling in authentication utilities."""
    
    def test_hash_password_with_invalid_bcrypt_rounds(self):
        """Test password hashing with invalid bcrypt rounds."""
        with patch('auth.utils.bcrypt.gensalt') as mock_gensalt:
            mock_gensalt.side_effect = Exception("BCrypt error")
            
            with pytest.raises(Exception):
                hash_password("TestPassword123!")
                
    def test_verify_password_with_invalid_hash(self):
        """Test password verification with invalid hash."""
        with patch('auth.utils.bcrypt.checkpw') as mock_checkpw:
            mock_checkpw.side_effect = Exception("BCrypt error")
            
            with pytest.raises(Exception):
                verify_password("password", "invalid_hash")
                
    def test_generate_jwt_token_with_invalid_payload(self):
        """Test JWT token generation with invalid payload."""
        with patch('auth.utils.jwt.encode') as mock_encode:
            mock_encode.side_effect = Exception("JWT error")
            
            with pytest.raises(Exception):
                generate_jwt_token({"invalid": "payload"})
                
    def test_verify_jwt_token_with_malformed_token(self):
        """Test JWT token verification with malformed token."""
        with patch('auth.utils.jwt.decode') as mock_decode:
            mock_decode.side_effect = jwt.DecodeError("Malformed token")
            
            with pytest.raises(jwt.DecodeError):
                verify_jwt_token("malformed.token")

class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_hash_password_very_long_password(self):
        """Test hashing very long password."""
        long_password = "a" * 1000
        hashed = hash_password(long_password)
        
        assert hashed != long_password
        assert verify_password(long_password, hashed) is True
        
    def test_hash_password_special_characters(self):
        """Test hashing password with special characters."""
        special_password = "P@ssw0rd!@#$%^&*()_+-=[]{}|;':\",./<>?"
        hashed = hash_password(special_password)
        
        assert hashed != special_password
        assert verify_password(special_password, hashed) is True
        
    def test_validate_email_unicode(self):
        """Test email validation with unicode characters."""
        unicode_email = "test@exämple.com"
        assert validate_email_address(unicode_email) is True
        
    def test_sanitize_input_unicode(self):
        """Test input sanitization with unicode characters."""
        unicode_input = "Hello 世界 <script>alert('xss')</script>"
        sanitized = sanitize_input(unicode_input)
        
        assert "&lt;script&gt;" in sanitized
        assert "世界" in sanitized
        
    def test_generate_secure_token_zero_length(self):
        """Test secure token generation with zero length."""
        with pytest.raises(ValueError):
            generate_secure_token(length=0)
            
    def test_generate_secure_token_negative_length(self):
        """Test secure token generation with negative length."""
        with pytest.raises(ValueError):
            generate_secure_token(length=-1)

class TestPerformance:
    """Test performance characteristics."""
    
    def test_hash_password_performance(self):
        """Test password hashing performance."""
        import time
        
        password = "TestPassword123!"
        start_time = time.time()
        
        for _ in range(10):
            hash_password(password)
            
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete 10 hashes in reasonable time (less than 5 seconds)
        assert duration < 5.0
        
    def test_verify_password_performance(self):
        """Test password verification performance."""
        import time
        
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        start_time = time.time()
        
        for _ in range(100):
            verify_password(password, hashed)
            
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete 100 verifications in reasonable time (less than 1 second)
        assert duration < 1.0
        
    def test_jwt_token_generation_performance(self):
        """Test JWT token generation performance."""
        import time
        
        payload = {"user_id": 123, "email": "test@example.com"}
        
        start_time = time.time()
        
        for _ in range(1000):
            generate_jwt_token(payload)
            
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete 1000 token generations in reasonable time (less than 1 second)
        assert duration < 1.0
