"""
Unit tests for authentication models
"""
import pytest
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from unittest.mock import patch, Mock

# Import the modules to test
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))
from auth.models import User, Role, Permission, UserSession, AuditLog
from auth.database import Base, engine, SessionLocal
from auth.utils import hash_password

class TestUserModel:
    """Test User model functionality."""
    
    def setup_method(self):
        """Set up test database."""
        Base.metadata.create_all(bind=engine)
        self.session = SessionLocal()
        
    def teardown_method(self):
        """Clean up test database."""
        self.session.close()
        Base.metadata.drop_all(bind=engine)
        
    def test_create_user(self):
        """Test creating a new user."""
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        
        self.session.add(user)
        self.session.commit()
        
        assert user.id is not None
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@example.com"
        assert user.is_active is True
        assert user.created_at is not None
        assert user.updated_at is not None
        
    def test_user_email_uniqueness(self):
        """Test that email addresses must be unique."""
        user1 = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        
        user2 = User(
            first_name="Jane",
            last_name="Doe",
            email="john.doe@example.com",  # Same email
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        
        self.session.add(user1)
        self.session.commit()
        
        with pytest.raises(IntegrityError):
            self.session.add(user2)
            self.session.commit()
            
    def test_user_required_fields(self):
        """Test that required fields are enforced."""
        user = User()  # Missing required fields
        
        with pytest.raises(IntegrityError):
            self.session.add(user)
            self.session.commit()
            
    def test_user_default_values(self):
        """Test user default values."""
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!")
        )
        
        self.session.add(user)
        self.session.commit()
        
        assert user.is_active is True
        assert user.failed_login_attempts == 0
        assert user.locked_until is None
        assert user.last_login is None
        
    def test_user_password_verification(self):
        """Test user password verification."""
        password = "TestPassword123!"
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password(password),
            is_active=True
        )
        
        self.session.add(user)
        self.session.commit()
        
        # Test password verification
        from auth.utils import verify_password
        assert verify_password(password, user.password_hash) is True
        assert verify_password("WrongPassword", user.password_hash) is False
        
    def test_user_full_name_property(self):
        """Test user full name property."""
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        
        assert user.full_name == "John Doe"
        
    def test_user_repr(self):
        """Test user string representation."""
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        
        self.session.add(user)
        self.session.commit()
        
        assert str(user) == f"<User(id={user.id}, email='john.doe@example.com')>"
        
    def test_user_update_timestamp(self):
        """Test that user updated_at timestamp is updated."""
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        
        self.session.add(user)
        self.session.commit()
        
        original_updated_at = user.updated_at
        
        # Update user
        user.first_name = "Jane"
        self.session.commit()
        
        assert user.updated_at > original_updated_at

class TestRoleModel:
    """Test Role model functionality."""
    
    def setup_method(self):
        """Set up test database."""
        Base.metadata.create_all(bind=engine)
        self.session = SessionLocal()
        
    def teardown_method(self):
        """Clean up test database."""
        self.session.close()
        Base.metadata.drop_all(bind=engine)
        
    def test_create_role(self):
        """Test creating a new role."""
        role = Role(
            name="admin",
            description="Administrator role with full access"
        )
        
        self.session.add(role)
        self.session.commit()
        
        assert role.id is not None
        assert role.name == "admin"
        assert role.description == "Administrator role with full access"
        assert role.created_at is not None
        assert role.updated_at is not None
        
    def test_role_name_uniqueness(self):
        """Test that role names must be unique."""
        role1 = Role(name="admin", description="Admin role")
        role2 = Role(name="admin", description="Another admin role")
        
        self.session.add(role1)
        self.session.commit()
        
        with pytest.raises(IntegrityError):
            self.session.add(role2)
            self.session.commit()
            
    def test_role_default_values(self):
        """Test role default values."""
        role = Role(name="user")
        
        self.session.add(role)
        self.session.commit()
        
        assert role.description is None
        
    def test_role_repr(self):
        """Test role string representation."""
        role = Role(name="admin", description="Admin role")
        
        self.session.add(role)
        self.session.commit()
        
        assert str(role) == f"<Role(id={role.id}, name='admin')>"

class TestPermissionModel:
    """Test Permission model functionality."""
    
    def setup_method(self):
        """Set up test database."""
        Base.metadata.create_all(bind=engine)
        self.session = SessionLocal()
        
    def teardown_method(self):
        """Clean up test database."""
        self.session.close()
        Base.metadata.drop_all(bind=engine)
        
    def test_create_permission(self):
        """Test creating a new permission."""
        permission = Permission(
            name="user_read",
            description="Read user data"
        )
        
        self.session.add(permission)
        self.session.commit()
        
        assert permission.id is not None
        assert permission.name == "user_read"
        assert permission.description == "Read user data"
        assert permission.created_at is not None
        assert permission.updated_at is not None
        
    def test_permission_name_uniqueness(self):
        """Test that permission names must be unique."""
        perm1 = Permission(name="user_read", description="Read user data")
        perm2 = Permission(name="user_read", description="Another read permission")
        
        self.session.add(perm1)
        self.session.commit()
        
        with pytest.raises(IntegrityError):
            self.session.add(perm2)
            self.session.commit()
            
    def test_permission_repr(self):
        """Test permission string representation."""
        permission = Permission(name="user_read", description="Read user data")
        
        self.session.add(permission)
        self.session.commit()
        
        assert str(permission) == f"<Permission(id={permission.id}, name='user_read')>"

class TestUserSessionModel:
    """Test UserSession model functionality."""
    
    def setup_method(self):
        """Set up test database."""
        Base.metadata.create_all(bind=engine)
        self.session = SessionLocal()
        
    def teardown_method(self):
        """Clean up test database."""
        self.session.close()
        Base.metadata.drop_all(bind=engine)
        
    def test_create_user_session(self):
        """Test creating a new user session."""
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        
        self.session.add(user)
        self.session.commit()
        
        session = UserSession(
            user_id=user.id,
            session_token="test_session_token",
            refresh_token="test_refresh_token",
            ip_address="127.0.0.1",
            user_agent="Mozilla/5.0 (Test Browser)",
            is_active=True
        )
        
        self.session.add(session)
        self.session.commit()
        
        assert session.id is not None
        assert session.user_id == user.id
        assert session.session_token == "test_session_token"
        assert session.refresh_token == "test_refresh_token"
        assert session.ip_address == "127.0.0.1"
        assert session.user_agent == "Mozilla/5.0 (Test Browser)"
        assert session.is_active is True
        assert session.created_at is not None
        assert session.updated_at is not None
        
    def test_user_session_default_values(self):
        """Test user session default values."""
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        
        self.session.add(user)
        self.session.commit()
        
        session = UserSession(
            user_id=user.id,
            session_token="test_session_token",
            refresh_token="test_refresh_token"
        )
        
        self.session.add(session)
        self.session.commit()
        
        assert session.is_active is True
        assert session.ip_address is None
        assert session.user_agent is None
        assert session.last_activity is None
        
    def test_user_session_foreign_key_constraint(self):
        """Test user session foreign key constraint."""
        session = UserSession(
            user_id=999,  # Non-existent user ID
            session_token="test_session_token",
            refresh_token="test_refresh_token"
        )
        
        with pytest.raises(IntegrityError):
            self.session.add(session)
            self.session.commit()
            
    def test_user_session_repr(self):
        """Test user session string representation."""
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        
        self.session.add(user)
        self.session.commit()
        
        session = UserSession(
            user_id=user.id,
            session_token="test_session_token",
            refresh_token="test_refresh_token"
        )
        
        self.session.add(session)
        self.session.commit()
        
        assert str(session) == f"<UserSession(id={session.id}, user_id={user.id})>"

class TestAuditLogModel:
    """Test AuditLog model functionality."""
    
    def setup_method(self):
        """Set up test database."""
        Base.metadata.create_all(bind=engine)
        self.session = SessionLocal()
        
    def teardown_method(self):
        """Clean up test database."""
        self.session.close()
        Base.metadata.drop_all(bind=engine)
        
    def test_create_audit_log(self):
        """Test creating a new audit log entry."""
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        
        self.session.add(user)
        self.session.commit()
        
        audit_log = AuditLog(
            user_id=user.id,
            action="login",
            resource_type="user",
            resource_id=str(user.id),
            ip_address="127.0.0.1",
            user_agent="Mozilla/5.0 (Test Browser)",
            details={"method": "password", "success": True}
        )
        
        self.session.add(audit_log)
        self.session.commit()
        
        assert audit_log.id is not None
        assert audit_log.user_id == user.id
        assert audit_log.action == "login"
        assert audit_log.resource_type == "user"
        assert audit_log.resource_id == str(user.id)
        assert audit_log.ip_address == "127.0.0.1"
        assert audit_log.user_agent == "Mozilla/5.0 (Test Browser)"
        assert audit_log.details == {"method": "password", "success": True}
        assert audit_log.created_at is not None
        
    def test_audit_log_default_values(self):
        """Test audit log default values."""
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        
        self.session.add(user)
        self.session.commit()
        
        audit_log = AuditLog(
            user_id=user.id,
            action="login",
            resource_type="user",
            resource_id=str(user.id)
        )
        
        self.session.add(audit_log)
        self.session.commit()
        
        assert audit_log.ip_address is None
        assert audit_log.user_agent is None
        assert audit_log.details is None
        
    def test_audit_log_foreign_key_constraint(self):
        """Test audit log foreign key constraint."""
        audit_log = AuditLog(
            user_id=999,  # Non-existent user ID
            action="login",
            resource_type="user",
            resource_id="999"
        )
        
        with pytest.raises(IntegrityError):
            self.session.add(audit_log)
            self.session.commit()
            
    def test_audit_log_repr(self):
        """Test audit log string representation."""
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        
        self.session.add(user)
        self.session.commit()
        
        audit_log = AuditLog(
            user_id=user.id,
            action="login",
            resource_type="user",
            resource_id=str(user.id)
        )
        
        self.session.add(audit_log)
        self.session.commit()
        
        assert str(audit_log) == f"<AuditLog(id={audit_log.id}, action='login', user_id={user.id})>"

class TestModelRelationships:
    """Test model relationships and associations."""
    
    def setup_method(self):
        """Set up test database."""
        Base.metadata.create_all(bind=engine)
        self.session = SessionLocal()
        
    def teardown_method(self):
        """Clean up test database."""
        self.session.close()
        Base.metadata.drop_all(bind=engine)
        
    def test_user_role_relationship(self):
        """Test user-role relationship."""
        # Create roles
        admin_role = Role(name="admin", description="Admin role")
        user_role = Role(name="user", description="User role")
        
        self.session.add_all([admin_role, user_role])
        self.session.commit()
        
        # Create user
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        
        # Add roles to user
        user.roles.append(admin_role)
        user.roles.append(user_role)
        
        self.session.add(user)
        self.session.commit()
        
        # Test relationship
        assert len(user.roles) == 2
        assert admin_role in user.roles
        assert user_role in user.roles
        
        # Test reverse relationship
        assert user in admin_role.users
        assert user in user_role.users
        
    def test_role_permission_relationship(self):
        """Test role-permission relationship."""
        # Create permissions
        read_perm = Permission(name="read", description="Read permission")
        write_perm = Permission(name="write", description="Write permission")
        
        self.session.add_all([read_perm, write_perm])
        self.session.commit()
        
        # Create role
        admin_role = Role(name="admin", description="Admin role")
        
        # Add permissions to role
        admin_role.permissions.append(read_perm)
        admin_role.permissions.append(write_perm)
        
        self.session.add(admin_role)
        self.session.commit()
        
        # Test relationship
        assert len(admin_role.permissions) == 2
        assert read_perm in admin_role.permissions
        assert write_perm in admin_role.permissions
        
        # Test reverse relationship
        assert admin_role in read_perm.roles
        assert admin_role in write_perm.roles
        
    def test_user_session_relationship(self):
        """Test user-session relationship."""
        # Create user
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        
        self.session.add(user)
        self.session.commit()
        
        # Create sessions
        session1 = UserSession(
            user_id=user.id,
            session_token="token1",
            refresh_token="refresh1"
        )
        
        session2 = UserSession(
            user_id=user.id,
            session_token="token2",
            refresh_token="refresh2"
        )
        
        self.session.add_all([session1, session2])
        self.session.commit()
        
        # Test relationship
        assert len(user.sessions) == 2
        assert session1 in user.sessions
        assert session2 in user.sessions
        
        # Test reverse relationship
        assert session1.user == user
        assert session2.user == user
        
    def test_user_audit_log_relationship(self):
        """Test user-audit log relationship."""
        # Create user
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        
        self.session.add(user)
        self.session.commit()
        
        # Create audit logs
        audit_log1 = AuditLog(
            user_id=user.id,
            action="login",
            resource_type="user",
            resource_id=str(user.id)
        )
        
        audit_log2 = AuditLog(
            user_id=user.id,
            action="logout",
            resource_type="user",
            resource_id=str(user.id)
        )
        
        self.session.add_all([audit_log1, audit_log2])
        self.session.commit()
        
        # Test relationship
        assert len(user.audit_logs) == 2
        assert audit_log1 in user.audit_logs
        assert audit_log2 in user.audit_logs
        
        # Test reverse relationship
        assert audit_log1.user == user
        assert audit_log2.user == user

class TestModelValidation:
    """Test model validation and constraints."""
    
    def setup_method(self):
        """Set up test database."""
        Base.metadata.create_all(bind=engine)
        self.session = SessionLocal()
        
    def teardown_method(self):
        """Clean up test database."""
        self.session.close()
        Base.metadata.drop_all(bind=engine)
        
    def test_user_email_format_validation(self):
        """Test user email format validation."""
        # This would typically be handled by SQLAlchemy validators
        # For now, we'll test the database constraint
        user = User(
            first_name="John",
            last_name="Doe",
            email="invalid-email",  # Invalid email format
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        
        # The database should accept this, but application-level validation should catch it
        self.session.add(user)
        self.session.commit()
        
    def test_user_password_hash_required(self):
        """Test that password hash is required."""
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            # Missing password_hash
            is_active=True
        )
        
        with pytest.raises(IntegrityError):
            self.session.add(user)
            self.session.commit()
            
    def test_session_token_uniqueness(self):
        """Test session token uniqueness."""
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        
        self.session.add(user)
        self.session.commit()
        
        session1 = UserSession(
            user_id=user.id,
            session_token="same_token",
            refresh_token="refresh1"
        )
        
        session2 = UserSession(
            user_id=user.id,
            session_token="same_token",  # Same token
            refresh_token="refresh2"
        )
        
        self.session.add(session1)
        self.session.commit()
        
        with pytest.raises(IntegrityError):
            self.session.add(session2)
            self.session.commit()
