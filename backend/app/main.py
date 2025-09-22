"""
Dubai Real Estate RAG Chat System - Backend API (CLEAN ARCHITECTURE VERSION)

This FastAPI application provides a comprehensive backend for the Dubai Real Estate
RAG (Retrieval-Augmented Generation) chat system with clean architecture principles.

📚 API Documentation:
- Interactive API docs: http://localhost:8001/docs
- ReDoc documentation: http://localhost:8001/redoc
- OpenAPI schema: http://localhost:8001/openapi.json

🔐 Security Features:
- User authentication with JWT tokens
- Role-based access control (RBAC)
- User data isolation
- Secure session management
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Union, Dict, Any, Optional
import os
import json
import google.generativeai as genai
import chromadb
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Text, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
from datetime import datetime
import pandas as pd
import shutil
import time
import asyncio
from pathlib import Path
from werkzeug.utils import secure_filename

# Import from clean architecture structure
from app.core.settings import get_settings
from app.core.database import get_db
from app.core.middleware import get_current_user, require_roles

# Import routers from clean architecture
try:
    from app.api.v1.property_management import router as property_router
    print("✅ Property management router loaded")
except ImportError as e:
    print(f"⚠️ Property management router not loaded: {e}")
    property_router = None

try:
    from app.api.v1.chat_sessions_router import router as chat_sessions_router, root_router as chat_root_router
    print("✅ Chat sessions router loaded")
except ImportError as e:
    print(f"⚠️ Chat sessions router not loaded: {e}")
    chat_sessions_router = None
    chat_root_router = None

try:
    from app.api.v1.data_router import router as data_router, root_router as data_root_router
    print("✅ Data router loaded")
except ImportError as e:
    print(f"⚠️ Data router not loaded: {e}")
    data_router = None
    data_root_router = None

try:
    from app.api.v1.file_processing_router import router as file_processing_router, root_router as file_processing_root_router
    print("✅ File processing router loaded")
except ImportError as e:
    print(f"⚠️ File processing router not loaded: {e}")
    file_processing_router = None
    file_processing_root_router = None

try:
    from app.api.v1.performance_router import router as performance_router
    print("✅ Performance router loaded")
except ImportError as e:
    print(f"⚠️ Performance router not loaded: {e}")
    performance_router = None

try:
    from app.api.v1.feedback_router import router as feedback_router
    print("✅ Feedback router loaded")
except ImportError as e:
    print(f"⚠️ Feedback router not loaded: {e}")
    feedback_router = None

try:
    from app.api.v1.admin_router import router as admin_router, ingest_router as admin_ingest_router
    print("✅ Admin router loaded")
except ImportError as e:
    print(f"⚠️ Admin router not loaded: {e}")
    admin_router = None
    admin_ingest_router = None

try:
    from app.api.v1.report_generation_router import router as report_router
    print("✅ Report generation router loaded")
except ImportError as e:
    print(f"⚠️ Report generation router not loaded: {e}")
    report_router = None

# Import AI services from clean architecture
try:
    from app.domain.ai.rag_service import EnhancedRAGService, QueryIntent
    print("✅ RAG service loaded")
except ImportError as e:
    print(f"⚠️ RAG service not loaded: {e}")
    EnhancedRAGService = None
    QueryIntent = None

try:
    from app.domain.ai.ai_manager import AIEnhancementManager
    print("✅ AI manager loaded")
except ImportError as e:
    print(f"⚠️ AI manager not loaded: {e}")
    AIEnhancementManager = None

try:
    from app.domain.ai.action_engine import ActionEngine
    print("✅ Action engine loaded")
except ImportError as e:
    print(f"⚠️ Action engine not loaded: {e}")
    ActionEngine = None

# Import monitoring from clean architecture
try:
    from app.infrastructure.integrations.rag_monitoring import include_rag_monitoring_routes
    print("✅ RAG monitoring loaded")
except ImportError as e:
    print(f"⚠️ RAG monitoring not loaded: {e}")
    include_rag_monitoring_routes = None

# Import async processing from clean architecture
try:
    from app.infrastructure.queue.async_processing import router as async_router
    print("✅ Async processing router loaded")
except ImportError as e:
    print(f"⚠️ Async processing router not loaded: {e}")
    async_router = None

# Import Blueprint 2.0 routers from clean architecture
try:
    from app.api.v1.documents_router import router as documents_router
    print("✅ Documents router loaded")
except ImportError as e:
    print(f"⚠️ Documents router not loaded: {e}")
    documents_router = None

try:
    from app.api.v1.nurturing_router import router as nurturing_router
    print("✅ Nurturing router loaded")
except ImportError as e:
    print(f"⚠️ Nurturing router not loaded: {e}")
    nurturing_router = None

try:
    from app.api.v1.ml_advanced_router import router as ml_advanced_router
    print("✅ ML advanced router loaded")
except ImportError as e:
    print(f"⚠️ ML advanced router not loaded: {e}")
    ml_advanced_router = None

try:
    from app.api.v1.ml_insights_router import router as ml_insights_router
    print("✅ ML insights router loaded")
except ImportError as e:
    print(f"⚠️ ML insights router not loaded: {e}")
    ml_insights_router = None

try:
    from app.api.v1.ml_websocket_router import router as ml_websocket_router
    print("✅ ML websocket router loaded")
except ImportError as e:
    print(f"⚠️ ML websocket router not loaded: {e}")
    ml_websocket_router = None

try:
    from app.api.v1.search_optimization_router import router as search_optimization_router
    print("✅ Search optimization router loaded")
except ImportError as e:
    print(f"⚠️ Search optimization router not loaded: {e}")
    search_optimization_router = None

try:
    from app.api.v1.database_enhancement_router import router as database_enhancement_router
    print("✅ Database enhancement router loaded")
except ImportError as e:
    print(f"⚠️ Database enhancement router not loaded: {e}")
    database_enhancement_router = None

# Import Phase 3 routers from clean architecture
try:
    from app.api.v1.phase3_advanced_router import router as phase3_advanced_router
    print("✅ Phase 3 advanced router loaded")
except ImportError as e:
    print(f"⚠️ Phase 3 advanced router not loaded: {e}")
    phase3_advanced_router = None

try:
    from app.api.v1.ai_assistant_router import router as ai_assistant_router
    print("✅ AI assistant router loaded")
except ImportError as e:
    print(f"⚠️ AI assistant router not loaded: {e}")
    ai_assistant_router = None

try:
    from app.api.v1.ai_request_router import router as ai_request_router
    print("✅ AI request router loaded")
except ImportError as e:
    print(f"⚠️ AI request router not loaded: {e}")
    ai_request_router = None

try:
    from app.api.v1.team_management_router import router as team_management_router
    print("✅ Team management router loaded")
except ImportError as e:
    print(f"⚠️ Team management router not loaded: {e}")
    team_management_router = None

try:
    from app.api.v1.property_detection_router import router as property_detection_router
    print("✅ Property detection router loaded")
except ImportError as e:
    print(f"⚠️ Property detection router not loaded: {e}")
    property_detection_router = None

try:
    from app.api.v1.admin_knowledge_router import router as admin_knowledge_router
    print("✅ Admin knowledge router loaded")
except ImportError as e:
    print(f"⚠️ Admin knowledge router not loaded: {e}")
    admin_knowledge_router = None

# Import models from clean architecture
try:
    from app.domain.listings.brokerage_models import *
    from app.domain.listings.phase3_advanced_models import *
    from app.domain.listings.ai_assistant_models import *
    from app.core.models import *
    print("✅ Models loaded")
except ImportError as e:
    print(f"⚠️ Some models could not be imported: {e}")

# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="Dubai Real Estate RAG Chat System",
    description="AI-powered real estate assistant with clean architecture",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
print("\n🚀 Including routers...")

if property_router:
    app.include_router(property_router, prefix="/api/properties", tags=["Properties"])
    print("✅ Property router included")

if chat_sessions_router:
    app.include_router(chat_sessions_router, prefix="/api/chat", tags=["Chat"])
    print("✅ Chat sessions router included")

if chat_root_router:
    app.include_router(chat_root_router, prefix="/api", tags=["Chat Root"])
    print("✅ Chat root router included")

if data_router:
    app.include_router(data_router, prefix="/api/data", tags=["Data"])
    print("✅ Data router included")

if data_root_router:
    app.include_router(data_root_router, prefix="/api", tags=["Data Root"])
    print("✅ Data root router included")

if file_processing_router:
    app.include_router(file_processing_router, prefix="/api/files", tags=["File Processing"])
    print("✅ File processing router included")

if file_processing_root_router:
    app.include_router(file_processing_root_router, prefix="/api", tags=["File Processing Root"])
    print("✅ File processing root router included")

if performance_router:
    app.include_router(performance_router, prefix="/api/performance", tags=["Performance"])
    print("✅ Performance router included")

if feedback_router:
    app.include_router(feedback_router, prefix="/api/feedback", tags=["Feedback"])
    print("✅ Feedback router included")

if admin_router:
    app.include_router(admin_router, prefix="/api/admin", tags=["Admin"])
    print("✅ Admin router included")

if admin_ingest_router:
    app.include_router(admin_ingest_router, prefix="/api/admin/ingest", tags=["Admin Ingest"])
    print("✅ Admin ingest router included")

if report_router:
    app.include_router(report_router, prefix="/api/reports", tags=["Reports"])
    print("✅ Report router included")

if async_router:
    app.include_router(async_router, prefix="/api/async", tags=["Async Processing"])
    print("✅ Async router included")

if documents_router:
    app.include_router(documents_router, prefix="/api/documents", tags=["Documents"])
    print("✅ Documents router included")

if nurturing_router:
    app.include_router(nurturing_router, prefix="/api/nurturing", tags=["Nurturing"])
    print("✅ Nurturing router included")

if ml_advanced_router:
    app.include_router(ml_advanced_router, prefix="/api/ml/advanced", tags=["ML Advanced"])
    print("✅ ML advanced router included")

if ml_insights_router:
    app.include_router(ml_insights_router, prefix="/api/ml/insights", tags=["ML Insights"])
    print("✅ ML insights router included")

if ml_websocket_router:
    app.include_router(ml_websocket_router, prefix="/api/ml/websocket", tags=["ML WebSocket"])
    print("✅ ML websocket router included")

if search_optimization_router:
    app.include_router(search_optimization_router, prefix="/api/search", tags=["Search Optimization"])
    print("✅ Search optimization router included")

if database_enhancement_router:
    app.include_router(database_enhancement_router, prefix="/api/database", tags=["Database Enhancement"])
    print("✅ Database enhancement router included")

if phase3_advanced_router:
    app.include_router(phase3_advanced_router, prefix="/api/phase3", tags=["Phase 3 Advanced"])
    print("✅ Phase 3 advanced router included")

if ai_assistant_router:
    app.include_router(ai_assistant_router, prefix="/api/ai/assistant", tags=["AI Assistant"])
    print("✅ AI assistant router included")

if ai_request_router:
    app.include_router(ai_request_router, prefix="/api/ai/requests", tags=["AI Requests"])
    print("✅ AI request router included")

if team_management_router:
    app.include_router(team_management_router, prefix="/api/teams", tags=["Team Management"])
    print("✅ Team management router included")

if property_detection_router:
    app.include_router(property_detection_router, prefix="/api/property-detection", tags=["Property Detection"])
    print("✅ Property detection router included")

if admin_knowledge_router:
    app.include_router(admin_knowledge_router, prefix="/api/admin/knowledge", tags=["Admin Knowledge"])
    print("✅ Admin knowledge router included")

# Include RAG monitoring routes
if include_rag_monitoring_routes:
    include_rag_monitoring_routes(app)
    print("✅ RAG monitoring routes included")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "architecture": "clean"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Dubai Real Estate RAG Chat System - Clean Architecture",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
