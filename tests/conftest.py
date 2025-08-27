"""
Pytest configuration and fixtures for Dubai Real Estate RAG Chat System
"""
import os
import pytest
import asyncio
from typing import Generator, AsyncGenerator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import tempfile
import shutil
from unittest.mock import Mock, patch

# Import the FastAPI app
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
from main import app
from auth.database import get_db, Base
from auth.models import User, Role, Permission, UserSession, AuditLog
from auth.utils import hash_password
from config.settings import (
    DATABASE_URL, 
    CHROMA_PERSIST_DIRECTORY,
    GOOGLE_API_KEY,
    REDIS_URL
)

# Test configuration
TEST_DATABASE_URL = "sqlite:///./test.db"
TEST_CHROMA_DIR = "./test_chroma"
TEST_REDIS_URL = "redis://localhost:6379/1"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    yield engine
    engine.dispose()

@pytest.fixture(scope="session")
def test_db_session(test_engine):
    """Create test database session."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def db_session(test_db_session):
    """Provide a fresh database session for each test."""
    yield test_db_session
    test_db_session.rollback()

@pytest.fixture
def client(db_session) -> Generator:
    """Create test client with database dependency override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def test_chroma_dir():
    """Create temporary ChromaDB directory for testing."""
    temp_dir = tempfile.mkdtemp(prefix="test_chroma_")
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture
def mock_google_ai():
    """Mock Google AI service."""
    with patch('ai_manager.GoogleGenerativeAI') as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        mock_instance.generate_content.return_value.text = "Mock AI response"
        yield mock_instance

@pytest.fixture
def mock_redis():
    """Mock Redis service."""
    with patch('cache_manager.redis.Redis') as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "password": "TestPassword123!",
        "role": "client"
    }

@pytest.fixture
def admin_user_data():
    """Admin user data for testing."""
    return {
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@dubai-estate.com",
        "password": "Admin123!",
        "role": "admin"
    }

@pytest.fixture
def agent_user_data():
    """Agent user data for testing."""
    return {
        "first_name": "Agent",
        "last_name": "User",
        "email": "agent@dubai-estate.com",
        "password": "Agent123!",
        "role": "agent"
    }

@pytest.fixture
def sample_property_data():
    """Sample property data for testing."""
    return {
        "title": "Luxury Villa in Dubai Marina",
        "description": "Beautiful 4-bedroom villa with sea view",
        "price": 2500000,
        "location": "Dubai Marina",
        "property_type": "villa",
        "bedrooms": 4,
        "bathrooms": 3,
        "area_sqft": 3500,
        "amenities": ["pool", "gym", "parking"],
        "status": "available"
    }

@pytest.fixture
def sample_chat_data():
    """Sample chat data for testing."""
    return {
        "message": "I'm looking for properties in Dubai Marina under 3 million AED",
        "context": "property_search",
        "user_preferences": {
            "location": "Dubai Marina",
            "max_price": 3000000,
            "property_type": "apartment"
        }
    }

@pytest.fixture
def authenticated_client(client, db_session):
    """Create authenticated test client."""
    # Create test user
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "password_hash": hash_password("TestPassword123!"),
        "is_active": True
    }
    
    user = User(**user_data)
    db_session.add(user)
    db_session.commit()
    
    # Login to get token
    login_response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "TestPassword123!"
    })
    
    token = login_response.json().get("access_token")
    client.headers.update({"Authorization": f"Bearer {token}"})
    
    return client

@pytest.fixture
def admin_client(client, db_session):
    """Create authenticated admin test client."""
    # Create admin user
    admin_data = {
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@dubai-estate.com",
        "password_hash": hash_password("Admin123!"),
        "is_active": True
    }
    
    admin = User(**admin_data)
    db_session.add(admin)
    db_session.commit()
    
    # Login to get token
    login_response = client.post("/auth/login", json={
        "email": "admin@dubai-estate.com",
        "password": "Admin123!"
    })
    
    token = login_response.json().get("access_token")
    client.headers.update({"Authorization": f"Bearer {token}"})
    
    return client

@pytest.fixture
def agent_client(client, db_session):
    """Create authenticated agent test client."""
    # Create agent user
    agent_data = {
        "first_name": "Agent",
        "last_name": "User",
        "email": "agent@dubai-estate.com",
        "password_hash": hash_password("Agent123!"),
        "is_active": True
    }
    
    agent = User(**agent_data)
    db_session.add(agent)
    db_session.commit()
    
    # Login to get token
    login_response = client.post("/auth/login", json={
        "email": "agent@dubai-estate.com",
        "password": "Agent123!"
    })
    
    token = login_response.json().get("access_token")
    client.headers.update({"Authorization": f"Bearer {token}"})
    
    return client

@pytest.fixture
def sample_files():
    """Sample files for testing file uploads."""
    files = {
        "pdf": ("test_property.pdf", b"PDF content", "application/pdf"),
        "image": ("property_image.jpg", b"Image content", "image/jpeg"),
        "document": ("property_doc.docx", b"Document content", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    }
    return files

@pytest.fixture
def rate_limit_settings():
    """Rate limit settings for testing."""
    return {
        "requests_per_minute": 60,
        "login_attempts": 5,
        "lockout_duration": 15
    }

@pytest.fixture
def performance_test_data():
    """Data for performance testing."""
    return {
        "concurrent_users": 20,
        "test_duration": 60,
        "ramp_up_time": 10,
        "target_response_time": 2000
    }

# Environment variables for testing
os.environ["DATABASE_URL"] = TEST_DATABASE_URL
os.environ["CHROMA_PERSIST_DIRECTORY"] = TEST_CHROMA_DIR
os.environ["REDIS_URL"] = TEST_REDIS_URL
os.environ["GOOGLE_API_KEY"] = "test_api_key"
os.environ["JWT_SECRET_KEY"] = "test_secret_key"
os.environ["ENVIRONMENT"] = "test"
