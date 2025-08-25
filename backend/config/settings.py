#!/usr/bin/env python3
"""
Centralized settings configuration for the Dubai Real Estate RAG System
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="../../.env")

# Base directory
BASE_DIR = Path(__file__).parent.parent.parent

# Database Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:password123@localhost:5432/real_estate_db"
)

# ChromaDB Configuration
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))

# Google AI Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    GOOGLE_API_KEY = "AIzaSyAocEBBwmq_eZ1Dy5RT9S7Kkfyw8nNibmM"
    print("⚠️  Using fallback API key - set GOOGLE_API_KEY in .env for production")

# AI Model Configuration
AI_MODEL = os.getenv("AI_MODEL", "gemini-1.5-flash")

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8001"))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# CORS Configuration
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001", 
    "http://192.168.1.241:3001"
]

# File Upload Configuration
UPLOAD_DIR = BASE_DIR / "backend" / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx', '.txt'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Cache Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = BASE_DIR / "logs" / "app.log"
LOG_FILE.parent.mkdir(exist_ok=True)

# Performance Configuration
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "50"))

# Security Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Production Configuration
IS_PRODUCTION = os.getenv("ENVIRONMENT", "development") == "production"

# Validation
def validate_settings():
    """Validate critical settings"""
    required_vars = ["DATABASE_URL"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"⚠️  Missing environment variables: {missing_vars}")
        return False
    
    return True

# Export settings
__all__ = [
    'DATABASE_URL', 'CHROMA_HOST', 'CHROMA_PORT', 'GOOGLE_API_KEY',
    'AI_MODEL', 'HOST', 'PORT', 'DEBUG', 'ALLOWED_ORIGINS',
    'UPLOAD_DIR', 'ALLOWED_EXTENSIONS', 'MAX_FILE_SIZE',
    'REDIS_URL', 'CACHE_TTL', 'LOG_LEVEL', 'LOG_FILE',
    'MAX_WORKERS', 'BATCH_SIZE', 'SECRET_KEY', 'IS_PRODUCTION',
    'validate_settings'
]
