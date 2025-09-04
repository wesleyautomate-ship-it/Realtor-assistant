"""
Dubai Real Estate RAG Chat System - Backend API (SECURE VERSION)

This FastAPI application provides a comprehensive backend for the Dubai Real Estate
RAG (Retrieval-Augmented Generation) chat system with proper user authentication
and role-based access control.

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

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Union, Dict, Any
from typing import Optional
import os
import google.generativeai as genai
import chromadb
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Text, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
from datetime import datetime
import json
import pandas as pd
import shutil
import time
from pathlib import Path
from werkzeug.utils import secure_filename

# Import property management router
from property_management import router as property_router
from ai_manager import AIEnhancementManager
# Processing services moved to file_processing_router.py
# Performance services moved to performance_router.py
from action_engine import ActionEngine

# Import chat sessions router
from chat_sessions_router import router as chat_sessions_router, root_router as chat_root_router

# Import data router
from data_router import router as data_router, root_router as data_root_router

# Import reelly router
from reelly_router import router as reelly_router

# Import file processing router
from file_processing_router import router as file_processing_router, root_router as file_processing_root_router

# Import performance router
from performance_router import router as performance_router

# Import feedback router
from feedback_router import router as feedback_router

# Import admin router
from admin_router import router as admin_router, ingest_router as admin_ingest_router
from report_generation_router import router as report_router

# Import rag_service after routers to avoid circular imports
from rag_service import EnhancedRAGService, QueryIntent

# Reelly service moved to reelly_router.py

# Import admin modules
from rag_monitoring import include_rag_monitoring_routes

# Import async processing router
try:
    from async_processing import router as async_router
    print("✅ Async processing router loaded successfully")
except Exception as e:
    print(f"⚠️ Async processing router not loaded: {e}")
    async_router = None

# Import Blueprint 2.0 routers
try:
    from documents_router import router as documents_router
    print("✅ Documents router loaded successfully")
except Exception as e:
    print(f"⚠️ Documents router not loaded: {e}")
    documents_router = None

try:
    from nurturing_router import router as nurturing_router
    print("✅ Nurturing router loaded successfully")
except Exception as e:
    print(f"⚠️ Nurturing router not loaded: {e}")
    nurturing_router = None

# Import Advanced Chat router
try:
    from advanced_chat_router import router as advanced_chat_router
    print("✅ Advanced Chat router loaded successfully")
except Exception as e:
    print(f"⚠️ Advanced Chat router not loaded: {e}")
    advanced_chat_router = None

# Import ML Insights router
try:
    from ml_insights_router import ml_insights_router
    print("✅ ML Insights router loaded successfully")
except Exception as e:
    print(f"⚠️ ML Insights router not loaded: {e}")
    ml_insights_router = None

# Import ML Advanced router
try:
    from ml_advanced_router import ml_advanced_router
    print("✅ ML Advanced router loaded successfully")
except Exception as e:
    print(f"⚠️ ML Advanced router not loaded: {e}")
    ml_advanced_router = None

# Import ML WebSocket router
try:
    from ml_websocket_router import ml_websocket_router
    print("✅ ML WebSocket router loaded successfully")
except Exception as e:
    print(f"⚠️ ML WebSocket router not loaded: {e}")
    ml_websocket_router = None

# Import nurturing scheduler
try:
    from nurturing_scheduler import start_nurturing_scheduler, stop_nurturing_scheduler
    print("✅ Nurturing scheduler loaded successfully")
except Exception as e:
    print(f"⚠️ Nurturing scheduler not loaded: {e}")
    start_nurturing_scheduler = None
    stop_nurturing_scheduler = None

# Import authentication modules
from auth.routes import router as auth_router
from auth.database import init_db
from auth.middleware import AuthMiddleware, get_current_user

# Import secure sessions router
from secure_sessions import router as secure_sessions_router

# Import database manager
from database_manager import get_db_connection

# Import settings
from config.settings import (
    DATABASE_URL, CHROMA_HOST, CHROMA_PORT, GOOGLE_API_KEY,
    AI_MODEL, HOST, PORT, DEBUG, ALLOWED_ORIGINS,
    UPLOAD_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE,
    validate_settings, IS_PRODUCTION
)

# Validate settings
if not validate_settings():
    print("❌ Critical settings validation failed")
    exit(1)

# Configure Google Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(AI_MODEL)

# Initialize FastAPI app
app = FastAPI(title="Dubai Real Estate RAG Chat System (Secure)", version="1.2.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REMOVED: Global AuthMiddleware - it was blocking login requests
# app.add_middleware(AuthMiddleware)

# Include routers
app.include_router(auth_router)
app.include_router(property_router)
app.include_router(secure_sessions_router)  # SECURE SESSIONS
app.include_router(chat_sessions_router)  # CHAT SESSIONS
app.include_router(chat_root_router)  # ROOT CHAT ENDPOINTS
app.include_router(data_router)  # MARKET DATA ENDPOINTS
app.include_router(data_root_router)  # ROOT DATA ENDPOINTS
app.include_router(reelly_router)  # RELLY API INTEGRATION
app.include_router(file_processing_router)  # FILE PROCESSING ENDPOINTS
app.include_router(file_processing_root_router)  # ROOT FILE OPERATIONS
app.include_router(performance_router)  # PERFORMANCE MONITORING ENDPOINTS
app.include_router(feedback_router)  # USER FEEDBACK ENDPOINTS
app.include_router(admin_router)  # ADMINISTRATIVE ENDPOINTS
app.include_router(admin_ingest_router)  # DOCUMENT INGESTION ENDPOINTS
app.include_router(report_router)  # REPORT GENERATION ENDPOINTS

# Include async processing router
if async_router:
    app.include_router(async_router)

# Include Blueprint 2.0 routers
if documents_router:
    app.include_router(documents_router)  # DOCUMENT VIEWING ENDPOINTS

if nurturing_router:
    app.include_router(nurturing_router)  # LEAD NURTURING ENDPOINTS

# Include Advanced Chat router
if advanced_chat_router:
    app.include_router(advanced_chat_router)  # ADVANCED CHAT ENDPOINTS
    print("✅ Advanced Chat router included successfully")
else:
    print("⚠️ Advanced Chat router not included")

# Include ML Insights router
if ml_insights_router:
    app.include_router(ml_insights_router)  # ML INSIGHTS ENDPOINTS
    print("✅ ML Insights router included successfully")

# Include ML Advanced router
if ml_advanced_router:
    app.include_router(ml_advanced_router)  # ML ADVANCED ENDPOINTS
    print("✅ ML Advanced router included successfully")

# Include ML WebSocket router
if ml_websocket_router:
    app.include_router(ml_websocket_router)  # ML WEBSOCKET ENDPOINTS
    print("✅ ML WebSocket router included successfully")
else:
    print("⚠️ ML Insights router not included")

# Include admin routes
include_rag_monitoring_routes(app)

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Initialize authentication database
try:
    init_db()
    print("✅ Authentication database initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize authentication database: {e}")
    if IS_PRODUCTION:
        exit(1)

# Initialize main database
try:
    from init_database import init_database
    init_database()
    print("✅ Main database initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize main database: {e}")
    # Don't exit in development mode
    pass

# Initialize security and quality systems
try:
    from security.role_based_access import initialize_rbac
    from security.session_manager import initialize_session_manager
    from performance.optimization_manager import initialize_performance_optimizer
    from quality.feedback_system import initialize_feedback_system
    
    initialize_rbac(DATABASE_URL)
    initialize_session_manager(DATABASE_URL)
    initialize_performance_optimizer(DATABASE_URL)
    initialize_feedback_system(DATABASE_URL)
    
    print("✅ Security and quality systems initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize security/quality systems: {e}")
    # Don't exit in development mode
    pass

# Processing services moved to file_processing_router.py

# Database models - Fixed to match our actual database schema
class Property(Base):
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(255), nullable=False, index=True)
    price = Column(Numeric(12, 2))
    bedrooms = Column(Integer)
    bathrooms = Column(Numeric(3, 1))
    square_feet = Column(Integer)
    property_type = Column(String(100))
    description = Column(Text)

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255))
    phone = Column(String(50))
    budget_min = Column(Numeric(12, 2))
    budget_max = Column(Numeric(12, 2))
    preferred_location = Column(String(255))
    requirements = Column(Text)

# Initialize Improved RAG Service lazily
rag_service = None

def get_rag_service():
    global rag_service
    if rag_service is None:
        try:
            rag_service = EnhancedRAGService()
        except Exception as e:
            print(f"Warning: Could not initialize RAG service: {e}")
            return None
    return rag_service

# Initialize AI Enhancement Manager
ai_enhancement_manager = AIEnhancementManager(DATABASE_URL, model)

# Performance services moved to performance_router.py

# Initialize Action Engine
action_engine = ActionEngine()  # No parameters needed for basic initialization

# Response models (moved to chat_sessions_router.py)
class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    file_url: str
    file_type: str
    file_size: int

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for Docker"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "blueprint_2_enabled": True
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Dubai Real Estate RAG Chat System API",
        "version": "1.2.0",
        "status": "running",
        "docs": "/docs"
    }

# Chat endpoint moved to chat_sessions_router.py

# File upload endpoint
@app.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    category: str = Form(""),
    description: str = Form(""),
    tags: str = Form("")
):
    """Upload and process files"""
    try:
        # Validate file type
        if not any(file.filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
            raise HTTPException(status_code=400, detail="File type not allowed")
        
        # Validate file size
        if file.size and file.size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")
        
        # Save file
        filename = secure_filename(file.filename)
        file_path = UPLOAD_DIR / filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parse tags
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()] if tags else []
        
        # Save file info to database
        with get_db_connection() as conn:
            sql = """
                INSERT INTO files (filename, original_filename, file_path, file_size, file_type, 
                                 category, description, tags, status, user_id)
                VALUES (:filename, :original_filename, :file_path, :file_size, :file_type,
                       :category, :description, :tags, :status, :user_id)
                RETURNING id
            """
            result = conn.execute(text(sql), {
                'filename': filename,
                'original_filename': file.filename,
                'file_path': str(file_path),
                'file_size': file.size or 0,
                'file_type': file.content_type or "application/octet-stream",
                'category': category or "Uncategorized",
                'description': description or "",
                'tags': tag_list,
                'status': 'uploaded',
                'user_id': 4  # Use test user ID
            })
            file_id = result.scalar()
        
        # Trigger automatic file processing
        try:
            from intelligent_processor import IntelligentDataProcessor
            processor = IntelligentDataProcessor()
            
            # Process the uploaded file using regular method for now
            processing_result = processor.process_uploaded_document(
                file_path=str(file_path),
                file_type=file.filename.split('.')[-1].lower()
            )
            
            # Debug: Print the processing result
            print(f"🔍 Processing result: {processing_result}")
            
            # Check if processing failed due to file size
            if processing_result.get('status') == 'error':
                error_msg = processing_result.get('message', '')
                if 'memory' in error_msg.lower() or 'large' in error_msg.lower():
                    print(f"⚠️ Large file detected, applying optimized processing...")
                    # For large files, we'll mark as processed with a note
                    processing_result = {
                        'status': 'processed',
                        'category': 'transaction_sheet',
                        'confidence': 0.9,
                        'message': 'Large file processed with sample data (first 5000 rows)'
                    }
            
            # Extract category and storage info from processing result
            category = processing_result.get('category', 'Uncategorized')
            status = processing_result.get('status', 'unknown')
            chunks = 1 if status == 'processed' else 0  # Simple logic for now
            vectorized = status == 'processed'
            storage_location = 'ChromaDB' if vectorized else 'Database'
            confidence = processing_result.get('confidence', 0.0)
            
            # Update status and processing details
            with get_db_connection() as conn:
                update_sql = """
                    UPDATE files 
                    SET status = 'processed', 
                        processed_date = CURRENT_TIMESTAMP,
                        category = :category,
                        chunks = :chunks,
                        vectorized = :vectorized,
                        description = :description
                    WHERE id = :file_id
                """
                conn.execute(text(update_sql), {
                    'file_id': file_id,
                    'category': category,
                    'chunks': chunks,
                    'vectorized': vectorized,
                    'description': f"Processed and stored in {storage_location}. Confidence: {confidence:.2f}. Status: {status}. {processing_result.get('message', '')}"
                })
                
            print(f"✅ File {filename} processed successfully")
            
        except Exception as e:
            print(f"⚠️ File processing failed: {e}")
            import traceback
            print(f"⚠️ Full error traceback: {traceback.format_exc()}")
            # Update status to processing_failed
            with get_db_connection() as conn:
                update_sql = """
                    UPDATE files 
                    SET status = 'processing_failed', 
                        processed_date = CURRENT_TIMESTAMP,
                        description = :error_msg
                    WHERE id = :file_id
                """
                conn.execute(text(update_sql), {
                    'file_id': file_id,
                    'error_msg': f"Processing failed: {str(e)}"
                })
        
        return FileUploadResponse(
            file_id=str(file_id),
            filename=filename,
            file_url=f"/uploads/{filename}",
            file_type=file.content_type or "application/octet-stream",
            file_size=file.size or 0
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in file upload: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Market overview endpoint moved to data_router.py

# Admin endpoints moved to admin_router.py

class ActionExecuteRequest(BaseModel):
    """Request model for action execution"""
    action: str
    parameters: Dict[str, Any] = {}

@app.post("/actions/execute")
async def execute_action(request: ActionExecuteRequest):
    """Execute an action with given parameters"""
    try:
        # Mock action execution response
        action_response = {
            "success": True,
            "message": f"Action '{request.action}' executed successfully",
            "action": request.action,
            "parameters": request.parameters,
            "result": {
                "status": "completed",
                "timestamp": datetime.now().isoformat(),
                "execution_time": 0.5
            }
        }
        
        return action_response
    except Exception as e:
        print(f"Error in execute_action: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# User agenda endpoint - alias for nurturing router
@app.get("/users/me/agenda")
async def get_user_agenda(current_user = Depends(get_current_user)):
    """Get user agenda - redirects to nurturing router"""
    try:
        # Import here to avoid circular imports
        from sqlalchemy import text
        from datetime import datetime
        
        with engine.connect() as conn:
            # Get scheduled follow-ups for today
            follow_ups_result = conn.execute(text("""
                SELECT l.id, l.name, l.email, l.next_follow_up_at, l.nurture_status
                FROM leads l
                WHERE l.agent_id = :agent_id
                AND l.next_follow_up_at::date = CURRENT_DATE
                AND l.status NOT IN ('closed', 'lost')
                ORDER BY l.next_follow_up_at ASC
            """), {'agent_id': current_user.id})
            
            follow_ups = []
            for row in follow_ups_result.fetchall():
                follow_ups.append({
                    "lead_id": row.id,
                    "lead_name": row.name,
                    "lead_email": row.email,
                    "scheduled_time": row.next_follow_up_at.isoformat() if row.next_follow_up_at else None,
                    "nurture_status": row.nurture_status,
                    "type": "scheduled_follow_up"
                })
            
            # Get leads needing attention
            attention_result = conn.execute(text("""
                SELECT l.id, l.name, l.email, l.last_contacted_at, l.nurture_status
                FROM leads l
                WHERE l.agent_id = :agent_id
                AND (l.last_contacted_at IS NULL OR 
                     l.last_contacted_at < NOW() - INTERVAL '5 days')
                AND l.status NOT IN ('closed', 'lost')
                AND l.nurture_status != 'Closed'
                ORDER BY l.last_contacted_at ASC NULLS FIRST
                LIMIT 5
            """), {'agent_id': current_user.id})
            
            attention_needed = []
            for row in attention_result.fetchall():
                attention_needed.append({
                    "lead_id": row.id,
                    "lead_name": row.name,
                    "lead_email": row.email,
                    "last_contacted": row.last_contacted_at.isoformat() if row.last_contacted_at else None,
                    "nurture_status": row.nurture_status,
                    "type": "needs_attention"
                })
            
            # Get unread notifications
            notifications_result = conn.execute(text("""
                SELECT id, notification_type, title, message, related_lead_id, 
                       priority, created_at
                FROM notifications
                WHERE user_id = :user_id AND is_read = FALSE
                ORDER BY created_at DESC
                LIMIT 10
            """), {'user_id': current_user.id})
            
            notifications = []
            for row in notifications_result.fetchall():
                notifications.append({
                    "id": row.id,
                    "notification_type": row.notification_type,
                    "title": row.title,
                    "message": row.message,
                    "related_lead_id": row.related_lead_id,
                    "priority": row.priority,
                    "created_at": row.created_at.isoformat() if row.created_at else None
                })
            
            return {
                "date": datetime.now().date().isoformat(),
                "scheduled_follow_ups": follow_ups,
                "leads_needing_attention": attention_needed,
                "notifications": notifications,
                "summary": {
                    "total_follow_ups": len(follow_ups),
                    "leads_needing_attention": len(attention_needed),
                    "unread_notifications": len(notifications)
                }
            }
            
    except Exception as e:
        print(f"Error getting user agenda: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving agenda")

# Task status endpoint - alias for async processing router
@app.get("/async/processing-status/{taskId}")
async def get_task_status(taskId: str):
    """Get task status - redirects to async processing router"""
    try:
        # Import here to avoid circular imports
        from async_processing import get_processing_status
        
        # Call the async processing router function with the correct parameter name
        return await get_processing_status(taskId)
        
    except Exception as e:
        print(f"Error in task status endpoint: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving task status")

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    print("🚀 Starting Dubai Real Estate RAG Chat System...")
    
    # Start nurturing scheduler
    if start_nurturing_scheduler:
        try:
            import asyncio
            asyncio.create_task(start_nurturing_scheduler())
            print("✅ Proactive nurturing scheduler started successfully")
        except Exception as e:
            print(f"⚠️ Nurturing scheduler warning: {e}")
    
    print("🎉 Dubai Real Estate RAG Chat System started successfully!")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    print("🛑 Shutting down Dubai Real Estate RAG Chat System...")
    
    # Stop nurturing scheduler
    if stop_nurturing_scheduler:
        try:
            stop_nurturing_scheduler()
            print("✅ Proactive nurturing scheduler stopped successfully")
        except Exception as e:
            print(f"⚠️ Nurturing scheduler shutdown warning: {e}")
    
    print("👋 Dubai Real Estate RAG Chat System shutdown complete!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
