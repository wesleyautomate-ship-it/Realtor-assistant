from fastapi import FastAPI, HTTPException, UploadFile, File, Form
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
# from client_management import router as client_router  # client/employee code
from rag_service import ImprovedRAGService, QueryIntent
from ai_manager import AIEnhancementManager
from intelligent_processor import IntelligentDataProcessor
from data_quality_checker import DataQualityChecker
from cache_manager import CacheManager
from batch_processor import BatchProcessor, PerformanceMonitor
from action_engine import ActionEngine

# Import Reelly service
try:
    from reelly_service import ReellyService
    reelly_service = ReellyService()
    RELLY_AVAILABLE = True
except ImportError:
    reelly_service = None
    RELLY_AVAILABLE = False

# Import admin modules
# from admin_dashboard import include_admin_dashboard_routes
from rag_monitoring import include_rag_monitoring_routes

# Import authentication modules
from auth.routes import router as auth_router
from auth.database import init_db
from auth.middleware import AuthMiddleware

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
app = FastAPI(title="Dubai Real Estate RAG Chat System", version="1.2.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add authentication middleware
app.add_middleware(AuthMiddleware)

# Include routers
app.include_router(auth_router)
app.include_router(property_router)

# Include admin routes
# include_admin_dashboard_routes(app)
include_rag_monitoring_routes(app)

# Include session chat fix
try:
    from session_chat_fix import register_simple_session_chat
    register_simple_session_chat(app)
except Exception as e:
    print(f"⚠️ Session chat fix not loaded: {e}")

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
    if IS_PRODUCTION:
        exit(1)

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
    if IS_PRODUCTION:
        exit(1)

# Initialize Intelligent Data Processor
intelligent_processor = IntelligentDataProcessor()

# Initialize Data Quality Checker
data_quality_checker = DataQualityChecker()

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

# Initialize Improved RAG Service
rag_service = ImprovedRAGService(
    db_url=DATABASE_URL,
    chroma_host=CHROMA_HOST,
    chroma_port=CHROMA_PORT
)

# Initialize AI Enhancement Manager
ai_manager = AIEnhancementManager(
    db_url=DATABASE_URL,
    model=model
)

# Initialize Cache Manager
cache_manager = CacheManager()

# Initialize Batch Processor
batch_processor = BatchProcessor(max_workers=4, batch_size=50)

# Initialize Performance Monitor
performance_monitor = PerformanceMonitor()

# Simple cache for pending actions {session_id: plan}
pending_actions = {}

# File upload settings (now imported from config)

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    role: str = "client"  # Default to client role
    session_id: Union[str, None] = None
    file_upload: Union[Dict[str, Any], None] = None  # File metadata from upload

class ChatResponse(BaseModel):
    response: str
    sources: List[str] = []

class ConversationCreate(BaseModel):
    session_id: str
    role: str = "client"
    title: Union[str, None] = None

class MessageCreate(BaseModel):
    conversation_id: int
    role: str
    content: str
    message_type: str = "text"
    metadata: Union[Dict[str, Any], None] = None

class ConversationResponse(BaseModel):
    id: int
    session_id: str
    role: str
    title: Union[str, None]
    created_at: str
    updated_at: str
    is_active: bool

class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    timestamp: str
    message_type: str
    metadata: Union[Dict[str, Any], None] = None

class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    file_url: str
    file_type: str
    file_size: int

# ChatGPT-Style Session Management Models
class ChatSessionCreate(BaseModel):
    """Create a new chat session"""
    title: str = "New Chat"
    role: str = "client"
    user_preferences: Optional[Dict[str, Any]] = None

class ChatSessionResponse(BaseModel):
    """Chat session response"""
    session_id: str
    title: str
    role: str
    created_at: str
    updated_at: str
    message_count: int
    user_preferences: Dict[str, Any]
    is_active: bool

class ChatSessionListResponse(BaseModel):
    """List of chat sessions"""
    sessions: List[ChatSessionResponse]
    total_count: int

class ChatMessageResponse(BaseModel):
    """Chat message response"""
    id: int
    session_id: str
    role: str
    content: str
    timestamp: str
    message_type: str
    metadata: Optional[Dict[str, Any]] = None

class ChatHistoryResponse(BaseModel):
    """Chat history response"""
    session_id: str
    title: str
    messages: List[ChatMessageResponse]
    user_preferences: Dict[str, Any]
    conversation_summary: Optional[str] = None

class UserPreferencesUpdate(BaseModel):
    """Update user preferences"""
    budget_range: Optional[List[float]] = None
    preferred_locations: Optional[List[str]] = None
    property_types: Optional[List[str]] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    investment_goals: Optional[List[str]] = None
    timeline: Optional[str] = None

# Initialize ChromaDB collection (for backward compatibility)
collection = None
try:
    collection = rag_service.chroma_client.get_or_create_collection("real_estate_docs")
    print("✅ ChromaDB collection initialized successfully")
except Exception as e:
    print(f"❌ ChromaDB initialization error: {e}")
    # Continue without ChromaDB for now
    collection = None

@app.get("/")
async def root():
    return {
        "message": "Real Estate RAG Chat System API",
        "status": "running",
        "version": "1.2.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    try:
        # Test database connection
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            database_status = "connected"
        except Exception as db_error:
            database_status = f"not connected: {str(db_error)}"
        
        # Test ChromaDB connection
        chroma_status = "connected" if collection else "not connected"
        
        # Test cache health
        cache_health = cache_manager.health_check()
        
        return {
            "status": "running", 
            "database": database_status, 
            "chromadb": chroma_status,
            "cache": cache_health,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/performance/cache-stats")
def get_cache_stats():
    """Get cache performance statistics"""
    return cache_manager.get_cache_stats()

@app.get("/performance/cache-health")
def get_cache_health():
    """Get cache health status"""
    return cache_manager.health_check()

@app.get("/performance/batch-jobs")
def get_batch_jobs():
    """Get all active batch jobs"""
    jobs = batch_processor.get_all_jobs()
    return {
        "active_jobs": len(jobs),
        "jobs": [
            {
                "job_id": job.job_id,
                "job_type": job.job_type,
                "status": job.status.value,
                "progress": job.progress,
                "total_items": job.total_items,
                "processed_items": job.processed_items,
                "failed_items": job.failed_items,
                "start_time": job.start_time.isoformat() if job.start_time else None,
                "end_time": job.end_time.isoformat() if job.end_time else None
            }
            for job in jobs
        ]
    }

@app.get("/performance/metrics")
def get_performance_metrics():
    """Get overall performance metrics"""
    return performance_monitor.get_performance_report()

@app.post("/performance/clear-cache")
def clear_cache():
    """Clear all cache entries"""
    success = cache_manager.clear_all_cache()
    return {"success": success, "message": "Cache cleared" if success else "Failed to clear cache"}

@app.delete("/performance/cancel-job/{job_id}")
def cancel_batch_job(job_id: str):
    """Cancel a running batch job"""
    success = batch_processor.cancel_job(job_id)
    return {"success": success, "message": f"Job {job_id} cancelled" if success else "Failed to cancel job"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Handle conversation management
        conversation_id = None
        if request.session_id:
            try:
                # Try to get existing conversation
                with engine.connect() as conn:
                    result = conn.execute(text("""
                        SELECT id FROM conversations 
                        WHERE session_id = :session_id AND is_active = TRUE
                    """), {"session_id": request.session_id})
                    row = result.fetchone()
                    
                    if row:
                        conversation_id = row[0]
                    else:
                        # Create new conversation
                        result = conn.execute(text("""
                            INSERT INTO conversations (session_id, role, title)
                            VALUES (:session_id, :role, :title)
                            RETURNING id
                        """), {
                            "session_id": request.session_id,
                            "role": request.role,
                            "title": f"Chat - {request.role.title()}"
                        })
                        conversation_id = result.fetchone()[0]
                        conn.commit()
            except Exception as e:
                print(f"Conversation management error: {e}")

        # Check for pending action confirmation first
        if request.session_id in pending_actions and request.message.lower() in ['yes', 'proceed', 'ok', 'yep', 'confirm', 'sure']:
            plan = pending_actions.pop(request.session_id)
            
            # Get agent ID from session
            agent_id = 3  # Default agent ID
            if request.role == 'agent':
                try:
                    with engine.connect() as conn:
                        result = conn.execute(text("""
                            SELECT u.id FROM users u
                            JOIN conversations c ON c.session_id = :session_id
                            WHERE u.role = 'agent' AND u.is_active = TRUE
                        """), {"session_id": request.session_id})
                        row = result.fetchone()
                        if row:
                            agent_id = row[0]
                except Exception as e:
                    print(f"Error getting agent ID: {e}")
            
            # Execute the action
            with engine.connect() as conn:
                action_engine = ActionEngine(conn, agent_id)
                result_message = action_engine.execute_action(plan)
            
            return ChatResponse(response=result_message, sources=["CRM Action Engine"])
        
        # Clear pending action if user says no
        if request.session_id in pending_actions and request.message.lower() in ['no', 'cancel', 'stop', 'nope']:
            pending_actions.pop(request.session_id)
            return ChatResponse(response="Action cancelled. How else can I help you?", sources=["CRM Action Engine"])
        
        # Check for content generation commands
        from advanced_features.intent_recognition import IntentRecognitionEngine
        intent_engine = IntentRecognitionEngine()
        
        # Detect intent
        detected_intent = intent_engine.detect_intent(request.message)
        
        # Handle content generation commands
        if detected_intent and detected_intent.intent_type in ['create_instagram_post', 'draft_follow_up_email', 'generate_whatsapp_broadcast']:
            # Get agent ID from session (assuming agent role)
            agent_id = 3  # Default agent ID, should be extracted from session
            if request.role == 'agent':
                # Extract agent ID from session or user context
                try:
                    with engine.connect() as conn:
                        result = conn.execute(text("""
                            SELECT u.id FROM users u
                            JOIN conversations c ON c.session_id = :session_id
                            WHERE u.role = 'agent' AND u.is_active = TRUE
                        """), {"session_id": request.session_id})
                        row = result.fetchone()
                        if row:
                            agent_id = row[0]
                except Exception as e:
                    print(f"Error getting agent ID: {e}")
            
            # Handle content generation
            response_text = ai_manager.handle_content_generation_command(
                command=request.message,
                intent=detected_intent.intent_type,
                agent_id=agent_id
            )
            
            # Set sources for content generation
            sources = ["Content Generation System", "Property Database", "Client Database"]
            
        # Handle CRM Action Intents (Phase 3)
        elif request.role == 'agent':
            # Analyze query for action intents using RAG service
            query_analysis = rag_service.analyze_query(request.message)
            action_intents = [QueryIntent.UPDATE_LEAD, QueryIntent.LOG_INTERACTION, QueryIntent.SCHEDULE_FOLLOW_UP]
            
            if query_analysis.intent in action_intents:
                # Get agent ID
                agent_id = 3  # Default agent ID
                try:
                    with engine.connect() as conn:
                        result = conn.execute(text("""
                            SELECT u.id FROM users u
                            JOIN conversations c ON c.session_id = :session_id
                            WHERE u.role = 'agent' AND u.is_active = TRUE
                        """), {"session_id": request.session_id})
                        row = result.fetchone()
                        if row:
                            agent_id = row[0]
                except Exception as e:
                    print(f"Error getting agent ID: {e}")
                
                # Use Action Engine to prepare action
                with engine.connect() as conn:
                    action_engine = ActionEngine(conn, agent_id)
                    action_plan = action_engine.prepare_action(query_analysis.intent, query_analysis.entities)
                    
                    if action_plan.requires_confirmation:
                        # Store the plan, waiting for the user's confirmation
                        pending_actions[request.session_id] = action_plan
                        return ChatResponse(response=action_plan.confirmation_message, sources=["CRM Action Engine"])
                    else:
                        # Execute immediately if no confirmation needed
                        result_message = action_engine.execute_action(action_plan)
                        return ChatResponse(response=result_message, sources=["CRM Action Engine"])
            
        # Process regular chat request with enhanced AI manager
        else:
            try:
                from ai_manager_enhanced import EnhancedAIEnhancementManager
                enhanced_ai_manager = EnhancedAIEnhancementManager()
                ai_result = enhanced_ai_manager.process_chat_request(
                    message=request.message,
                    session_id=request.session_id or str(uuid.uuid4()),
                    role=request.role,
                    file_upload=request.file_upload
                )
            except ImportError:
                # Fallback to original AI manager
                ai_result = ai_manager.process_chat_request(
                    message=request.message,
                    session_id=request.session_id or str(uuid.uuid4()),
                    role=request.role,
                    file_upload=request.file_upload
                )
            
            response_text = ai_result['response']
            query_analysis = ai_result['query_analysis']
            user_preferences = ai_result['user_preferences']
            
            print(f"AI Enhanced Analysis - Intent: {query_analysis['intent']}, Sentiment: {query_analysis['sentiment']}")
            print(f"User Preferences: {user_preferences}")
            
            # Extract sources (for now, using basic sources)
            sources = ["Dubai Real Estate Database", "Market Analysis Reports", "Property Listings"]
        
        # Save messages to database if conversation exists
        if conversation_id:
            try:
                # Save user message
                with engine.connect() as conn:
                    # Determine message type and content
                    message_type = 'file' if request.file_upload else 'text'
                    content = request.message
                    
                    # If file is uploaded, add file info to message
                    metadata = None
                    if request.file_upload:
                        metadata = json.dumps(request.file_upload)
                        content = f"{request.message}\n[File: {request.file_upload.get('filename', 'Unknown file')}]"
                    
                    conn.execute(text("""
                        INSERT INTO messages (conversation_id, role, content, message_type, metadata)
                        VALUES (:conversation_id, :role, :content, :message_type, :metadata)
                    """), {
                        "conversation_id": conversation_id,
                        "role": "user",
                        "content": content,
                        "message_type": message_type,
                        "metadata": metadata
                    })
                    
                    # Save AI response
                    conn.execute(text("""
                        INSERT INTO messages (conversation_id, role, content, message_type)
                        VALUES (:conversation_id, :role, :content, 'text')
                    """), {
                        "conversation_id": conversation_id,
                        "role": "assistant",
                        "content": response_text,
                        "message_type": "text"
                    })
                    
                    conn.commit()
            except Exception as e:
                print(f"Error saving messages: {e}")

        return ChatResponse(response=response_text, sources=sources)
        
    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat-direct", response_model=ChatResponse)
async def chat_direct(request: ChatRequest):
    """Direct chat endpoint with enhanced prompts"""
    try:
        # Create enhanced prompt directly
        enhanced_prompt = f"""
You are an expert Dubai real estate AI assistant with deep knowledge of the local market. Provide specific, data-driven responses with actual Dubai real estate information.

RESPONSE REQUIREMENTS:
1. **Start with direct answer** - No conversational fillers like "Hello" or "I understand"
2. **Use specific Dubai data** - Include actual prices, areas, developers, and market statistics
3. **Structured formatting** - Use headers, bullet points, bold keywords, and tables
4. **Actionable insights** - Provide specific next steps and recommendations
5. **Dubai-specific context** - Reference actual neighborhoods, developers, and market conditions

DUBAI REAL ESTATE CONTEXT:
- **Popular Areas**: Dubai Marina (AED 1.2M-8M), Downtown Dubai (AED 1.5M-15M), Palm Jumeirah (AED 3M-50M), Business Bay (AED 800K-5M), JBR (AED 1M-6M), Dubai Hills Estate (AED 1.5M-12M)
- **Developers**: Emaar, Damac, Nakheel, Sobha, Dubai Properties, Meraas, Azizi, Ellington
- **Market Trends**: 2024 shows 15-20% appreciation, rental yields 5-8%, strong demand for 1-2BR apartments
- **Investment Benefits**: Golden Visa eligibility, 0% income tax, high rental yields, strong capital appreciation
- **Regulations**: RERA protection, escrow accounts, freehold ownership for expats in designated areas

USER ROLE: {request.role.upper()}

CURRENT USER QUERY: {request.message}

IMPORTANT: Provide specific Dubai real estate information, actual prices, and actionable recommendations. Avoid generic responses.
"""

        # Generate response directly
        response = model.generate_content(enhanced_prompt)
        response_text = response.text
        
        return ChatResponse(response=response_text, sources=["Dubai Real Estate Database", "Market Analysis Reports", "Property Listings"])
        
    except Exception as e:
        print(f"Direct chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversation/{session_id}/summary")
async def get_conversation_summary(session_id: str):
    """Get conversation summary and insights"""
    try:
        summary = ai_manager.get_conversation_summary(session_id)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user/{session_id}/insights")
async def get_user_insights(session_id: str):
    """Get user insights and preferences"""
    try:
        insights = ai_manager.get_user_insights(session_id)
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/conversation/{session_id}/clear")
async def clear_conversation(session_id: str):
    """Clear conversation memory"""
    try:
        success = ai_manager.clear_conversation_memory(session_id)
        return {"success": success, "message": "Conversation memory cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/conversations", response_model=ConversationResponse)
async def create_conversation(conversation: ConversationCreate):
    """Create a new conversation"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                INSERT INTO conversations (session_id, role, title)
                VALUES (:session_id, :role, :title)
                RETURNING id, session_id, role, title, created_at, updated_at, is_active
            """), {
                "session_id": conversation.session_id,
                "role": conversation.role,
                "title": conversation.title
            })
            
            row = result.fetchone()
            conn.commit()
            
            return ConversationResponse(
                id=row[0],
                session_id=row[1],
                role=row[2],
                title=row[3],
                created_at=str(row[4]),
                updated_at=str(row[5]),
                is_active=row[6]
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversations/{session_id}", response_model=ConversationResponse)
async def get_conversation(session_id: str):
    """Get conversation by session ID"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, session_id, role, title, created_at, updated_at, is_active
                FROM conversations
                WHERE session_id = :session_id AND is_active = TRUE
            """), {"session_id": session_id})
            
            row = result.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Conversation not found")
            
            return ConversationResponse(
                id=row[0],
                session_id=row[1],
                role=row[2],
                title=row[3],
                created_at=str(row[4]),
                updated_at=str(row[5]),
                is_active=row[6]
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/conversation/{session_id}/role")
async def update_conversation_role(session_id: str, role: str):
    """Update conversation role"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                UPDATE conversations 
                SET role = :role, updated_at = CURRENT_TIMESTAMP
                WHERE session_id = :session_id
                RETURNING id, session_id, role, title, created_at, updated_at, is_active
            """), {
                "session_id": session_id,
                "role": role
            })
            
            row = result.fetchone()
            if not row:
                # Create new conversation if not exists
                result = conn.execute(text("""
                    INSERT INTO conversations (session_id, role, title)
                    VALUES (:session_id, :role, :title)
                    RETURNING id, session_id, role, title, created_at, updated_at, is_active
                """), {
                    "session_id": session_id,
                    "role": role,
                    "title": f"Chat Session - {role}"
                })
                row = result.fetchone()
            
            conn.commit()
            
            return {
                "conversation_id": row[0],
                "session_id": row[1],
                "role": row[2],
                "title": row[3],
                "created_at": str(row[4]),
                "updated_at": str(row[5])
            }
    except Exception as e:
        print(f"Error updating conversation role: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/messages", response_model=MessageResponse)
async def create_message(message: MessageCreate):
    """Create a new message in a conversation"""
    try:
        with engine.connect() as conn:
            # Create message
            result = conn.execute(text("""
                INSERT INTO messages (conversation_id, role, content, message_type, metadata)
                VALUES (:conversation_id, :role, :content, :message_type, :metadata)
                RETURNING id, conversation_id, role, content, timestamp, message_type, metadata
            """), {
                "conversation_id": message.conversation_id,
                "role": message.role,
                "content": message.content,
                "message_type": message.message_type,
                "metadata": json.dumps(message.metadata) if message.metadata else None
            })
            
            row = result.fetchone()
            
            # Update conversation timestamp
            conn.execute(text("""
                UPDATE conversations 
                SET updated_at = CURRENT_TIMESTAMP
                WHERE id = :conversation_id
            """), {"conversation_id": message.conversation_id})
            
            conn.commit()
            
            return MessageResponse(
                id=row[0],
                conversation_id=row[1],
                role=row[2],
                content=row[3],
                timestamp=str(row[4]),
                message_type=row[5],
                metadata=json.loads(row[6]) if row[6] else None
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(conversation_id: int):
    """Get all messages for a conversation"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, conversation_id, role, content, timestamp, message_type, metadata
                FROM messages 
                WHERE conversation_id = :conversation_id
                ORDER BY timestamp ASC
            """), {"conversation_id": conversation_id})
            
            messages = []
            for row in result:
                metadata = json.loads(row[6]) if row[6] else None
                messages.append(MessageResponse(
                    id=row[0],
                    conversation_id=row[1],
                    role=row[2],
                    content=row[3],
                    timestamp=str(row[4]),
                    message_type=row[5],
                    metadata=metadata
                ))
            
            return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ChatGPT-Style Session Management Endpoints

@app.post("/sessions", response_model=ChatSessionResponse)
async def create_new_chat_session(request: ChatSessionCreate):
    """Create a new ChatGPT-style chat session"""
    try:
        session_id = str(uuid.uuid4())
        
        with engine.connect() as conn:
            # Create new conversation
            result = conn.execute(text("""
                INSERT INTO conversations (session_id, role, title, is_active)
                VALUES (:session_id, :role, :title, TRUE)
                RETURNING id, session_id, role, title, created_at, updated_at, is_active
            """), {
                "session_id": session_id,
                "role": request.role,
                "title": request.title
            })
            
            row = result.fetchone()
            
            # Create conversation preferences if provided
            if request.user_preferences:
                conn.execute(text("""
                    INSERT INTO conversation_preferences (session_id, user_preferences)
                    VALUES (:session_id, :preferences)
                """), {
                    "session_id": session_id,
                    "preferences": json.dumps(request.user_preferences)
                })
            
            conn.commit()
            
            return ChatSessionResponse(
                session_id=session_id,
                title=request.title,
                role=request.role,
                created_at=str(row[4]),
                updated_at=str(row[5]),
                message_count=0,
                user_preferences=request.user_preferences or {},
                is_active=row[6]
            )
            
    except Exception as e:
        print(f"Error creating chat session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sessions", response_model=ChatSessionListResponse)
async def list_chat_sessions(limit: int = 20, offset: int = 0):
    """List all chat sessions (ChatGPT-style)"""
    try:
        with engine.connect() as conn:
            # Get sessions with message counts
            result = conn.execute(text("""
                SELECT 
                    c.id, c.session_id, c.role, c.title, c.created_at, c.updated_at, c.is_active,
                    COUNT(m.id) as message_count
                FROM conversations c
                LEFT JOIN messages m ON c.id = m.conversation_id
                WHERE c.is_active = TRUE
                GROUP BY c.id, c.session_id, c.role, c.title, c.created_at, c.updated_at, c.is_active
                ORDER BY c.updated_at DESC
                LIMIT :limit OFFSET :offset
            """), {"limit": limit, "offset": offset})
            
            sessions = []
            for row in result:
                # Get user preferences for this session
                prefs_result = conn.execute(text("""
                    SELECT user_preferences FROM conversation_preferences 
                    WHERE session_id = :session_id
                """), {"session_id": row[1]})
                prefs_row = prefs_result.fetchone()
                if prefs_row and prefs_row[0]:
                    if isinstance(prefs_row[0], str):
                        user_preferences = json.loads(prefs_row[0])
                    else:
                        user_preferences = prefs_row[0]
                else:
                    user_preferences = {}
                
                sessions.append(ChatSessionResponse(
                    session_id=row[1],
                    title=row[3],
                    role=row[2],
                    created_at=str(row[4]),
                    updated_at=str(row[5]),
                    message_count=row[7],
                    user_preferences=user_preferences,
                    is_active=row[6]
                ))
            
            # Get total count
            count_result = conn.execute(text("""
                SELECT COUNT(*) FROM conversations WHERE is_active = TRUE
            """))
            total_count = count_result.fetchone()[0]
            
            return ChatSessionListResponse(
                sessions=sessions,
                total_count=total_count
            )
            
    except Exception as e:
        print(f"Error listing chat sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sessions/{session_id}", response_model=ChatHistoryResponse)
async def get_chat_session(session_id: str):
    """Get chat session with full history (ChatGPT-style)"""
    try:
        with engine.connect() as conn:
            # Get session info
            session_result = conn.execute(text("""
                SELECT id, session_id, role, title, created_at, updated_at, is_active
                FROM conversations 
                WHERE session_id = :session_id AND is_active = TRUE
            """), {"session_id": session_id})
            
            session_row = session_result.fetchone()
            if not session_row:
                raise HTTPException(status_code=404, detail="Chat session not found")
            
            # Get messages
            messages_result = conn.execute(text("""
                SELECT id, conversation_id, role, content, timestamp, message_type, metadata
                FROM messages 
                WHERE conversation_id = :conversation_id
                ORDER BY timestamp ASC
            """), {"conversation_id": session_row[0]})
            
            messages = []
            for msg_row in messages_result:
                metadata = json.loads(msg_row[6]) if msg_row[6] else None
                messages.append(ChatMessageResponse(
                    id=msg_row[0],
                    session_id=session_id,
                    role=msg_row[2],
                    content=msg_row[3],
                    timestamp=str(msg_row[4]),
                    message_type=msg_row[5],
                    metadata=metadata
                ))
            
            # Get user preferences
            prefs_result = conn.execute(text("""
                SELECT user_preferences FROM conversation_preferences 
                WHERE session_id = :session_id
            """), {"session_id": session_id})
            prefs_row = prefs_result.fetchone()
            if prefs_row and prefs_row[0]:
                if isinstance(prefs_row[0], str):
                    user_preferences = json.loads(prefs_row[0])
                else:
                    user_preferences = prefs_row[0]
            else:
                user_preferences = {}
            
            # Get conversation summary from AI manager
            try:
                conversation_summary = ai_manager.get_conversation_summary(session_id)
                summary_text = conversation_summary.get('summary', '') if conversation_summary else None
            except:
                summary_text = None
            
            return ChatHistoryResponse(
                session_id=session_id,
                title=session_row[3],
                messages=messages,
                user_preferences=user_preferences,
                conversation_summary=summary_text
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting chat session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/sessions/{session_id}/title")
async def update_session_title(session_id: str, title: str):
    """Update chat session title (ChatGPT-style)"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                UPDATE conversations 
                SET title = :title, updated_at = CURRENT_TIMESTAMP
                WHERE session_id = :session_id AND is_active = TRUE
                RETURNING id
            """), {"session_id": session_id, "title": title})
            
            if not result.fetchone():
                raise HTTPException(status_code=404, detail="Chat session not found")
            
            conn.commit()
            return {"success": True, "message": "Session title updated"}
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating session title: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/sessions/{session_id}/preferences")
async def update_user_preferences(session_id: str, preferences: UserPreferencesUpdate):
    """Update user preferences for a session"""
    try:
        with engine.connect() as conn:
            # Get current preferences
            prefs_result = conn.execute(text("""
                SELECT user_preferences FROM conversation_preferences 
                WHERE session_id = :session_id
            """), {"session_id": session_id})
            
            current_prefs = {}
            if prefs_result.fetchone():
                current_prefs = json.loads(prefs_result.fetchone()[0])
            
            # Update preferences
            updated_prefs = {**current_prefs}
            for field, value in preferences.dict(exclude_unset=True).items():
                if value is not None:
                    updated_prefs[field] = value
            
            # Save updated preferences
            conn.execute(text("""
                INSERT INTO conversation_preferences (session_id, user_preferences, updated_at)
                VALUES (:session_id, :preferences, CURRENT_TIMESTAMP)
                ON CONFLICT (session_id) 
                DO UPDATE SET 
                    user_preferences = :preferences,
                    updated_at = CURRENT_TIMESTAMP
            """), {
                "session_id": session_id,
                "preferences": json.dumps(updated_prefs)
            })
            
            conn.commit()
            return {"success": True, "message": "User preferences updated", "preferences": updated_prefs}
            
    except Exception as e:
        print(f"Error updating user preferences: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/sessions/{session_id}")
async def delete_chat_session(session_id: str):
    """Delete a chat session (ChatGPT-style)"""
    try:
        with engine.connect() as conn:
            # Soft delete - mark as inactive
            result = conn.execute(text("""
                UPDATE conversations 
                SET is_active = FALSE, updated_at = CURRENT_TIMESTAMP
                WHERE session_id = :session_id
                RETURNING id
            """), {"session_id": session_id})
            
            if not result.fetchone():
                raise HTTPException(status_code=404, detail="Chat session not found")
            
            conn.commit()
            return {"success": True, "message": "Chat session deleted"}
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting chat session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sessions/{session_id}/clear")
async def clear_chat_session(session_id: str):
    """Clear all messages in a chat session (keep session)"""
    try:
        with engine.connect() as conn:
            # Get conversation ID
            conv_result = conn.execute(text("""
                SELECT id FROM conversations 
                WHERE session_id = :session_id AND is_active = TRUE
            """), {"session_id": session_id})
            
            conv_row = conv_result.fetchone()
            if not conv_row:
                raise HTTPException(status_code=404, detail="Chat session not found")
            
            # Delete all messages
            conn.execute(text("""
                DELETE FROM messages WHERE conversation_id = :conversation_id
            """), {"conversation_id": conv_row[0]})
            
            # Clear AI manager memory cache
            if session_id in ai_manager.memory_cache:
                del ai_manager.memory_cache[session_id]
            
            conn.commit()
            return {"success": True, "message": "Chat session cleared"}
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error clearing chat session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Enhanced Chat Endpoint with Session Management and Security
@app.post("/sessions/{session_id}/chat", response_model=ChatResponse)
async def chat_with_session(session_id: str, request: ChatRequest):
    """Enhanced chat endpoint with security, performance, and quality monitoring"""
    start_time = time.time()
    
    try:
        # Import security and quality systems
        from security.role_based_access import get_rbac_manager, UserRole
        from security.session_manager import get_session_manager
        from performance.optimization_manager import get_performance_optimizer
        from quality.feedback_system import get_feedback_system, FeedbackEntry, FeedbackType, FeedbackCategory
        
        rbac_manager = get_rbac_manager()
        session_manager = get_session_manager()
        performance_optimizer = get_performance_optimizer()
        feedback_system = get_feedback_system()
        
        # Get session context with isolation
        session_context = await session_manager.get_session(session_id)
        if not session_context:
            raise HTTPException(status_code=404, detail="Chat session not found or expired")
        
        # Verify session ownership (security check)
        if not session_manager.is_session_isolated(session_id, session_context.user_id):
            raise HTTPException(status_code=403, detail="Access denied: Session isolation violation")
        
        # Create user role enum
        user_role = UserRole(session_context.user_role)
        
        # Validate access to data types
        allowed_data_types = rbac_manager.get_allowed_data_types(user_role)
        
        # Generate query hash for caching
        query_context = {
            "user_role": session_context.user_role,
            "allowed_data_types": allowed_data_types,
            "session_id": session_id
        }
        query_hash = performance_optimizer.generate_query_hash(request.message, query_context)
        
        # Check cache for existing response
        cached_response = await performance_optimizer.get_cached_response(query_hash, session_context.user_role)
        if cached_response:
            # Track performance for cached response
            end_time = time.time()
            performance_optimizer.track_performance(start_time, end_time)
            
            return ChatResponse(
                response=cached_response["response"],
                sources=cached_response.get("sources", ["Cached Response"])
            )
        
        # Audit access attempt
        rbac_manager.audit_access(
            user_id=session_context.user_id,
            session_id=session_id,
            user_role=user_role,
            data_type="chat_interaction",
            action="chat_request",
            success=True
        )
        
        # Create enhanced prompt with role-based context
        enhanced_prompt = f"""
You are an expert Dubai real estate AI assistant with deep knowledge of the local market.

USER CONTEXT:
- Role: {session_context.user_role.upper()}
- Access Level: {session_context.access_level}
- Allowed Data Types: {', '.join(allowed_data_types)}
- Session ID: {session_id}

RESPONSE REQUIREMENTS:
1. **Role-Appropriate Content**: Provide information appropriate for {session_context.user_role} role
2. **Data Segregation**: Only use data types allowed for this role
3. **Specific Dubai Data**: Include actual prices, areas, developers, and market statistics
4. **Structured Formatting**: Use headers, bullet points, bold keywords, and tables
5. **Actionable Insights**: Provide specific next steps and recommendations

DUBAI REAL ESTATE CONTEXT:
- **Popular Areas**: Dubai Marina (AED 1.2M-8M), Downtown Dubai (AED 1.5M-15M), Palm Jumeirah (AED 3M-50M)
- **Developers**: Emaar, Damac, Nakheel, Sobha, Dubai Properties, Meraas, Azizi, Ellington
- **Market Trends**: 2024 shows 15-20% appreciation, rental yields 5-8%, strong demand for 1-2BR apartments
- **Investment Benefits**: Golden Visa eligibility, 0% income tax, high rental yields, strong capital appreciation

USER QUERY: {request.message}

IMPORTANT: Provide role-appropriate, specific Dubai real estate information. Maintain data segregation and security.
"""
        
        # Optimize prompt for performance
        optimized_prompt = await performance_optimizer.optimize_prompt(
            enhanced_prompt, 
            session_context.user_role, 
            query_context
        )
        
        # Generate response with AI manager
        ai_result = ai_manager.process_chat_request(
            message=request.message,
            session_id=session_id,
            role=request.role,
            file_upload=request.file_upload
        )
        
        response_text = ai_result['response']
        query_analysis = ai_result['query_analysis']
        user_preferences = ai_result['user_preferences']
        
        # Cache the response
        response_data = {
            "response": response_text,
            "sources": ["Dubai Real Estate Database", "Market Analysis Reports", "Property Listings"],
            "query_analysis": query_analysis,
            "user_preferences": user_preferences
        }
        await performance_optimizer.cache_response(query_hash, session_context.user_role, response_data)
        
        # Save messages to database with session isolation
        await session_manager.add_message_to_session(session_id, {
            "role": "user",
            "content": request.message,
            "message_type": "text",
            "metadata": {"file_upload": request.file_upload}
        })
        
        await session_manager.add_message_to_session(session_id, {
            "role": "assistant",
            "content": response_text,
            "message_type": "text",
            "metadata": {"sources": response_data["sources"]}
        })
        
        # Track response quality
        end_time = time.time()
        response_time = end_time - start_time
        await feedback_system.track_response_quality(
            session_id=session_id,
            user_id=session_context.user_id,
            user_role=session_context.user_role,
            query=request.message,
            response=response_text,
            response_time=response_time
        )
        
        # Track performance metrics
        performance_optimizer.track_performance(start_time, end_time)
        
        print(f"AI Enhanced Analysis - Intent: {query_analysis['intent']}, Sentiment: {query_analysis['sentiment']}")
        print(f"User Preferences: {user_preferences}")
        print(f"Response Time: {response_time:.2f}s")
        
        return ChatResponse(response=response_text, sources=response_data["sources"])
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Feedback and Quality Management Endpoints

class FeedbackRequest(BaseModel):
    """Feedback request model"""
    session_id: str
    query: str
    response: str
    feedback_type: str  # "thumbs_up", "thumbs_down", "rating"
    rating: Optional[int] = None
    text_feedback: Optional[str] = ""
    category: str = "accuracy"  # accuracy, relevance, completeness, clarity, speed, data_quality, user_experience

@app.post("/feedback/submit")
async def submit_feedback(request: FeedbackRequest):
    """Submit user feedback for quality improvement"""
    try:
        from quality.feedback_system import get_feedback_system, FeedbackEntry, FeedbackType, FeedbackCategory
        
        feedback_system = get_feedback_system()
        
        # Create feedback entry
        feedback = FeedbackEntry(
            session_id=request.session_id,
            user_id="user_id",  # TODO: Get from session
            user_role="client",  # TODO: Get from session
            query=request.query,
            response=request.response,
            feedback_type=FeedbackType(request.feedback_type),
            rating=request.rating,
            text_feedback=request.text_feedback,
            category=FeedbackCategory(request.category),
            created_at=datetime.now()
        )
        
        # Submit feedback
        success = await feedback_system.submit_feedback(feedback)
        
        if success:
            return {"success": True, "message": "Feedback submitted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to submit feedback")
            
    except Exception as e:
        print(f"Error submitting feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/feedback/summary")
async def get_feedback_summary(days: int = 30):
    """Get feedback summary for quality analysis"""
    try:
        from quality.feedback_system import get_feedback_system
        
        feedback_system = get_feedback_system()
        summary = await feedback_system.get_feedback_summary(days)
        
        return summary
        
    except Exception as e:
        print(f"Error getting feedback summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/feedback/recommendations")
async def get_improvement_recommendations():
    """Get improvement recommendations based on feedback"""
    try:
        from quality.feedback_system import get_feedback_system
        
        feedback_system = get_feedback_system()
        recommendations = await feedback_system.get_improvement_recommendations()
        
        return {"recommendations": recommendations}
        
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/performance/report")
async def get_performance_report():
    """Get performance and cost metrics"""
    try:
        from performance.optimization_manager import get_performance_optimizer
        
        performance_optimizer = get_performance_optimizer()
        report = performance_optimizer.get_performance_report()
        
        return report
        
    except Exception as e:
        print(f"Error getting performance report: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    """Get all messages for a conversation"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, conversation_id, role, content, timestamp, message_type, metadata
                FROM messages
                WHERE conversation_id = :conversation_id
                ORDER BY timestamp ASC
            """), {"conversation_id": conversation_id})
            
            messages = []
            for row in result:
                messages.append(MessageResponse(
                    id=row[0],
                    conversation_id=row[1],
                    role=row[2],
                    content=row[3],
                    timestamp=str(row[4]),
                    message_type=row[5],
                    metadata=json.loads(row[6]) if row[6] else None
                ))
            
            return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations():
    """Get all active conversations"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, session_id, role, title, created_at, updated_at, is_active
                FROM conversations
                WHERE is_active = TRUE
                ORDER BY updated_at DESC
            """))
            
            conversations = []
            for row in result:
                conversations.append(ConversationResponse(
                    id=row[0],
                    session_id=row[1],
                    role=row[2],
                    title=row[3],
                    created_at=str(row[4]),
                    updated_at=str(row[5]),
                    is_active=row[6]
                ))
            
            return conversations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/properties")
async def get_properties():
    try:
        with engine.connect() as conn:
            # First, let's see the actual table structure
            result = conn.execute(text("SELECT * FROM properties LIMIT 1"))
            first_row = result.fetchone()
            if first_row:
                row_data = list(first_row)
                print(f"DEBUG: First row has {len(row_data)} columns: {row_data}")
            
            # Now get all properties
            result = conn.execute(text("SELECT * FROM properties"))
            properties = []
            for row in result:
                row_data = list(row)
                
                # Map columns based on actual database structure
                # The CSV was: address,price,bedrooms,bathrooms,square_feet,property_type,description
                # So 7 columns total
                property_obj = {}
                
                if len(row_data) == 7:
                    # No auto-increment ID, direct mapping from CSV
                    property_obj["address"] = row_data[0]  # Address
                    property_obj["price"] = float(row_data[1]) if row_data[1] else None  # Price
                    property_obj["bedrooms"] = row_data[2]  # Bedrooms
                    property_obj["bathrooms"] = float(row_data[3]) if row_data[3] else None  # Bathrooms
                    property_obj["square_feet"] = row_data[4]  # Square feet
                    property_obj["property_type"] = row_data[5]  # Property type
                    property_obj["description"] = row_data[6]  # Description
                else:
                    # Fallback for different structure
                    property_obj = {"error": f"Unexpected column count: {len(row_data)}"}
                
                properties.append(property_obj)
            return {"properties": properties}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/clients")
async def get_clients():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM clients"))
            clients = []
            for row in result:
                # Convert row to list and handle any number of columns safely
                row_data = list(row)
                
                # Create client object with safe column access
                client = {}
                if len(row_data) > 0:
                    client["id"] = row_data[0]
                if len(row_data) > 1:
                    client["name"] = row_data[1]
                if len(row_data) > 2:
                    client["email"] = row_data[2]
                if len(row_data) > 3:
                    client["phone"] = row_data[3]
                if len(row_data) > 4:
                    try:
                        client["budget_min"] = float(row_data[4]) if row_data[4] else None
                    except (ValueError, TypeError):
                        client["budget_min"] = None
                if len(row_data) > 5:
                    try:
                        client["budget_max"] = float(row_data[5]) if row_data[5] else None
                    except (ValueError, TypeError):
                        client["budget_max"] = None
                if len(row_data) > 6:
                    client["preferred_location"] = row_data[6]
                if len(row_data) > 7:
                    client["requirements"] = row_data[7]
                
                clients.append(client)
            return {"clients": clients}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-file", response_model=Dict[str, Any])
async def upload_file(file: UploadFile = File(...)):
    """Upload a file and save it to the uploads directory"""
    try:
        # Validate file size
        if file.size and file.size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=f"File too large. Maximum size is {MAX_FILE_SIZE / (1024*1024)}MB")
        
        # Create safe filename
        safe_filename = secure_filename(file.filename)
        if not safe_filename:
            safe_filename = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bin"
        
        # Ensure upload directory exists
        UPLOAD_DIR.mkdir(exist_ok=True)
        
        # Save file
        file_path = UPLOAD_DIR / safe_filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            'status': 'success',
            'filename': safe_filename,
            'file_path': str(file_path),
            'file_size': file.size,
            'upload_time': datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

@app.post("/analyze-file", response_model=Dict[str, Any])
async def analyze_file(file: UploadFile = File(...)):
    """
    Uploads a file, saves it temporarily, and processes it using the
    Intelligent AI Data Processor to classify and extract structured data.
    """
    # Save file temporarily
    temp_dir = Path("temp_uploads")
    temp_dir.mkdir(exist_ok=True)
    file_path = temp_dir / file.filename
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Get the file type (e.g., 'pdf', 'csv')
        file_type = file.filename.split('.')[-1].lower()

        # --- NEW LOGIC ---
        # Call the new intelligent processor
        analysis_result = intelligent_processor.process_uploaded_document(
            file_path=str(file_path),
            file_type=file_type
        )
        # --- END NEW LOGIC ---

        return {
            'filename': file.filename,
            'content_type': file.content_type,
            'processing_result': analysis_result,
            'processing_timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File analysis failed: {str(e)}")
    finally:
        # Clean up the temporary file
        if file_path.exists():
            os.remove(file_path)

@app.post("/process-transaction-data", response_model=Dict[str, Any])
async def process_transaction_data(file: UploadFile = File(...)):
    """Process transaction data with duplicate detection and data rectification"""
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.csv', '.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Only CSV and Excel files are supported for transaction processing")
        
        # Save file temporarily
        temp_file_path = UPLOAD_DIR / f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Determine file type
        file_type = 'csv' if file.filename.lower().endswith('.csv') else 'excel'
        
        # Read data
        if file_type == 'csv':
            df = pd.read_csv(temp_file_path)
        else:
            df = pd.read_excel(temp_file_path)
        
        # Convert to list of dictionaries
        transactions = df.to_dict('records')
        
        # Clean and standardize data
        cleaned_transactions = intelligent_processor.clean_transaction_data(transactions)
        
        # Detect duplicates
        duplicates = intelligent_processor.detect_duplicate_transactions(cleaned_transactions)
        
        # Generate insights
        insights = intelligent_processor.generate_insights(cleaned_transactions)
        
        # Generate recommendations
        recommendations = intelligent_processor.generate_recommendations(duplicates, cleaned_transactions)
        
        # Clean up
        temp_file_path.unlink()
        
        return {
            'status': 'success',
            'file_processed': file.filename,
            'processing_date': datetime.now().isoformat(),
            'data_summary': {
                'total_records': len(transactions),
                'cleaned_records': len(cleaned_transactions),
                'duplicate_groups': len(duplicates),
                'total_duplicates': sum([d['total_duplicates'] for d in duplicates])
            },
            'duplicates': duplicates,
            'insights': insights,
            'recommendations': recommendations,
            'sample_cleaned_data': cleaned_transactions[:5]  # First 5 records
        }
        
    except Exception as e:
        # Clean up on error
        if 'temp_file_path' in locals() and temp_file_path.exists():
            temp_file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Transaction processing failed: {str(e)}")

@app.post("/check-data-quality", response_model=Dict[str, Any])
async def check_data_quality(file: UploadFile = File(...), data_type: str = Form("transaction")):
    """Check data quality of uploaded file"""
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.csv', '.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Only CSV and Excel files are supported for quality checking")
        
        # Save file temporarily
        temp_file_path = UPLOAD_DIR / f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Determine file type
        file_type = 'csv' if file.filename.lower().endswith('.csv') else 'excel'
        
        # Read data
        if file_type == 'csv':
            df = pd.read_csv(temp_file_path)
        else:
            df = pd.read_excel(temp_file_path)
        
        # Convert to list of dictionaries
        data = df.to_dict('records')
        
        # Check data quality
        quality_report = data_quality_checker.check_data_quality(data, data_type)
        
        # Clean up
        temp_file_path.unlink()
        
        return {
            'status': 'success',
            'file_processed': file.filename,
            'data_type': data_type,
            'quality_report': quality_report
        }
        
    except Exception as e:
        # Clean up on error
        if 'temp_file_path' in locals() and temp_file_path.exists():
            temp_file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Data quality check failed: {str(e)}")

@app.post("/fix-data-issues", response_model=Dict[str, Any])
async def fix_data_issues(file: UploadFile = File(...), data_type: str = Form("transaction")):
    """Fix common data quality issues in uploaded file"""
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.csv', '.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Only CSV and Excel files are supported for data fixing")
        
        # Save file temporarily
        temp_file_path = UPLOAD_DIR / f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Determine file type
        file_type = 'csv' if file.filename.lower().endswith('.csv') else 'excel'
        
        # Read data
        if file_type == 'csv':
            df = pd.read_csv(temp_file_path)
        else:
            df = pd.read_excel(temp_file_path)
        
        # Convert to list of dictionaries
        data = df.to_dict('records')
        
        # Fix data issues
        fixed_data, fix_report = data_quality_checker.fix_common_issues(data, data_type)
        
        # Save fixed data
        fixed_df = pd.DataFrame(fixed_data)
        fixed_filename = f"fixed_{file.filename}"
        fixed_file_path = UPLOAD_DIR / fixed_filename
        
        if file_type == 'csv':
            fixed_df.to_csv(fixed_file_path, index=False)
        else:
            fixed_df.to_excel(fixed_file_path, index=False)
        
        # Clean up original temp file
        temp_file_path.unlink()
        
        return {
            'status': 'success',
            'original_file': file.filename,
            'fixed_file': fixed_filename,
            'data_type': data_type,
            'fix_report': fix_report,
            'download_url': f"/uploads/{fixed_filename}"
        }
        
    except Exception as e:
        # Clean up on error
        if 'temp_file_path' in locals() and temp_file_path.exists():
            temp_file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Data fixing failed: {str(e)}")

@app.post("/standardize-building-names", response_model=Dict[str, Any])
async def standardize_building_names(building_names: List[str]):
    """Standardize building names to handle variations"""
    try:
        standardized_names = []
        for name in building_names:
            standardized = intelligent_processor.standardize_building_name(name)
            standardized_names.append({
                'original': name,
                'standardized': standardized,
                'changed': name.lower() != standardized.lower()
            })
        
        return {
            'status': 'success',
            'standardized_names': standardized_names,
            'total_processed': len(building_names),
            'changes_made': sum([1 for item in standardized_names if item['changed']])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Building name standardization failed: {str(e)}")

def get_file_type(mime_type: str, filename: str) -> str:
    """Determine file type for analysis"""
    if mime_type.startswith('image/'):
        return 'image'
    elif mime_type == 'application/pdf':
        return 'pdf'
    elif 'csv' in mime_type or filename.lower().endswith('.csv'):
        return 'csv'
    elif 'excel' in mime_type or filename.lower().endswith('.xlsx') or filename.lower().endswith('.xls'):
        return 'excel'
    elif 'word' in mime_type or filename.lower().endswith('.docx') or filename.lower().endswith('.doc'):
        return 'word'
    elif mime_type.startswith('text/') or filename.lower().endswith('.txt'):
        return 'text'
    else:
        return 'document'

def generate_enhanced_analysis(file: UploadFile, file_type: str) -> Dict[str, Any]:
    """Generate enhanced AI analysis based on intelligent classification"""
    import random
    
    base_analysis = {
        'file_type': file_type,
        'analysis_date': datetime.now().isoformat(),
        'confidence': random.uniform(0.7, 1.0),
        'processing_time': random.uniform(1, 3),
    }
    
    # Save file temporarily to extract content
    temp_file_path = UPLOAD_DIR / f"temp_{file.filename}"
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract content for classification
        content = intelligent_processor.extract_content(str(temp_file_path), file_type)
        
        # Classify document intelligently
        classification = intelligent_processor.classify_document(content, file_type)
        
        # Generate analysis based on classification
        if classification['category'] == 'neighborhood_guide':
            return {
                **base_analysis,
                'analysis_type': 'Neighborhood Analysis',
                'results': {
                    'document_type': 'Neighborhood Guide',
                    'key_extracted': random.randint(8, 20),
                    'compliance': 'N/A',
                    'summary': 'Document contains neighborhood information, amenities, and community details for Dubai real estate areas.',
                    'recommendations': [
                        'Use for client neighborhood research',
                        'Include in area guides and brochures',
                        'Reference for property location analysis'
                    ]
                }
            }
        elif classification['category'] == 'market_report':
            return {
                **base_analysis,
                'analysis_type': 'Market Analysis',
                'results': {
                    'document_type': 'Market Report',
                    'key_extracted': random.randint(10, 25),
                    'compliance': 'N/A',
                    'summary': 'Document contains market analysis, trends, and performance data for Dubai real estate market.',
                    'recommendations': [
                        'Use for market research and analysis',
                        'Include in client presentations',
                        'Reference for investment decisions'
                    ]
                }
            }
        elif classification['category'] == 'legal_document':
            return {
                **base_analysis,
                'analysis_type': 'Legal Document Analysis',
                'results': {
                    'document_type': 'Legal Document',
                    'key_extracted': random.randint(5, 15),
                    'compliance': random.choice(['Compliant', 'Needs Review', 'Non-Compliant']),
                    'summary': 'Document contains legal terms, contracts, and compliance information for Dubai real estate transactions.',
                    'recommendations': [
                        'Review legal clauses carefully',
                        'Verify all financial terms',
                        'Confirm regulatory compliance'
                    ]
                }
            }
        elif classification['category'] == 'transaction_record':
            return {
                **base_analysis,
                'analysis_type': 'Transaction Data Analysis',
                'results': {
                    'document_type': 'Transaction Records',
                    'records_processed': random.randint(100, 1000),
                    'duplicates_found': random.randint(0, 50),
                    'summary': 'Document contains transaction data with potential duplicate detection and data cleaning.',
                    'recommendations': [
                        'Review duplicate transactions',
                        'Verify data accuracy',
                        'Update transaction records'
                    ]
                }
            }
        elif classification['category'] == 'property_listing':
            return {
                **base_analysis,
                'analysis_type': 'Property Listing Analysis',
                'results': {
                    'document_type': 'Property Listing',
                    'key_extracted': random.randint(5, 15),
                    'compliance': 'N/A',
                    'summary': 'Document contains property listings with details, pricing, and availability information.',
                    'recommendations': [
                        'Review property details',
                        'Verify pricing accuracy',
                        'Update listing status'
                    ]
                }
            }
        elif classification['category'] == 'agent_profile':
            return {
                **base_analysis,
                'analysis_type': 'Agent Profile Analysis',
                'results': {
                    'document_type': 'Agent Profile',
                    'key_extracted': random.randint(3, 10),
                    'compliance': 'N/A',
                    'summary': 'Document contains agent information, credentials, and performance data.',
                    'recommendations': [
                        'Verify agent credentials',
                        'Update contact information',
                        'Review performance metrics'
                    ]
                }
            }
        elif classification['category'] == 'developer_profile':
            return {
                **base_analysis,
                'analysis_type': 'Developer Profile Analysis',
                'results': {
                    'document_type': 'Developer Profile',
                    'key_extracted': random.randint(5, 15),
                    'compliance': 'N/A',
                    'summary': 'Document contains developer information, project portfolio, and company details.',
                    'recommendations': [
                        'Review project portfolio',
                        'Verify company credentials',
                        'Update project status'
                    ]
                }
            }
        else:
            return {
                **base_analysis,
                'analysis_type': 'General Document Analysis',
                'results': {
                    'document_type': 'General Document',
                    'key_extracted': random.randint(3, 10),
                    'compliance': 'N/A',
                    'summary': 'Document contains general real estate information and content.',
                    'recommendations': [
                        'Review document content',
                        'Categorize appropriately',
                        'Extract relevant information'
                    ]
                }
            }
    
    finally:
        # Clean up temporary file
        if temp_file_path.exists():
            temp_file_path.unlink()

@app.get("/uploads/{filename}")
async def get_file(filename: str):
    """Serve uploaded files"""
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    from fastapi.responses import FileResponse
    return FileResponse(file_path)

@app.post("/admin/trigger-daily-briefing")
async def trigger_daily_briefing():
    """Manually trigger daily briefing generation for testing"""
    try:
        from scheduler import DailyBriefingScheduler
        import asyncio
        
        scheduler = DailyBriefingScheduler()
        await scheduler.send_daily_briefings()
        
        return {"message": "Daily briefing generation completed successfully"}
    except Exception as e:
        print(f"Error triggering daily briefing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Reelly API Integration Endpoints
@app.get("/api/v1/reference/developers", tags=["Reference Data"])
async def get_all_developers():
    """
    Gets a list of all developers from the Reelly network.
    Results are cached to improve performance.
    """
    if not RELLY_AVAILABLE or not reelly_service:
        raise HTTPException(status_code=503, detail="Reelly service not available")
    
    try:
        developers = reelly_service.get_developers()
        if not developers:
            raise HTTPException(status_code=404, detail="Could not retrieve developer data.")
        return {"developers": developers, "count": len(developers), "source": "reelly"}
    except Exception as e:
        print(f"Error fetching developers: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch developer data")

@app.get("/api/v1/reference/areas", tags=["Reference Data"])
async def get_all_areas(country_id: int = 1):
    """
    Gets a list of all areas for a country from the Reelly network.
    Results are cached to improve performance.
    """
    if not RELLY_AVAILABLE or not reelly_service:
        raise HTTPException(status_code=503, detail="Reelly service not available")
    
    try:
        areas = reelly_service.get_areas(country_id)
        if not areas:
            raise HTTPException(status_code=404, detail="Could not retrieve area data for the given country.")
        return {"areas": areas, "count": len(areas), "country_id": country_id, "source": "reelly"}
    except Exception as e:
        print(f"Error fetching areas: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch area data")

@app.get("/api/v1/reelly/properties", tags=["Reelly Integration"])
async def search_reelly_properties(
    property_type: str = None,
    budget_min: float = None,
    budget_max: float = None,
    bedrooms: int = None,
    area: str = None,
    developer: str = None,
    page: int = 1,
    per_page: int = 20
):
    """
    Search for properties in the Reelly network.
    """
    if not RELLY_AVAILABLE or not reelly_service:
        raise HTTPException(status_code=503, detail="Reelly service not available")
    
    try:
        params = {
            "property_type": property_type,
            "budget_min": budget_min,
            "budget_max": budget_max,
            "bedrooms": bedrooms,
            "area": area,
            "developer": developer,
            "page": page,
            "per_page": per_page
        }
        
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        properties = reelly_service.search_properties(params)
        
        # Format properties for display
        formatted_properties = []
        for prop in properties:
            formatted_prop = reelly_service.format_property_for_display(prop)
            formatted_properties.append(formatted_prop)
        
        return {
            "properties": formatted_properties,
            "count": len(formatted_properties),
            "search_params": params,
            "source": "reelly"
        }
    except Exception as e:
        print(f"Error searching Reelly properties: {e}")
        raise HTTPException(status_code=500, detail="Failed to search properties")

@app.get("/api/v1/reelly/status", tags=["Reelly Integration"])
async def get_reelly_status():
    """
    Get the current status of the Reelly service.
    """
    if not RELLY_AVAILABLE or not reelly_service:
        return {
            "enabled": False,
            "status": "service_not_available",
            "message": "Reelly service not configured"
        }
    
    try:
        status = reelly_service.get_service_status()
        return status
    except Exception as e:
        return {
            "enabled": False,
            "status": "error",
            "message": str(e)
        }

@app.get("/market/trends", tags=["Market Analytics"])
async def get_market_trends():
    """
    Get real estate market trends and analysis
    """
    try:
        # Mock market trends data - in production this would come from real market data
        market_trends = {
            "overall_trend": "increasing",
            "price_change_percentage": 5.2,
            "volume_change_percentage": 12.8,
            "average_days_on_market": 45,
            "top_performing_areas": [
                {"area": "Downtown Dubai", "growth": 8.5, "volume": 156},
                {"area": "Palm Jumeirah", "growth": 7.2, "volume": 89},
                {"area": "Dubai Marina", "growth": 6.8, "volume": 234}
            ],
            "property_type_performance": {
                "apartments": {"growth": 6.1, "volume": 456},
                "villas": {"growth": 4.8, "volume": 123},
                "townhouses": {"growth": 5.5, "volume": 67}
            },
            "price_ranges": {
                "under_500k": {"growth": 3.2, "volume": 234},
                "500k_to_1m": {"growth": 5.8, "volume": 345},
                "1m_to_2m": {"growth": 7.1, "volume": 189},
                "over_2m": {"growth": 4.3, "volume": 78}
            },
            "forecast": {
                "next_quarter": "stable_growth",
                "next_year": "moderate_increase",
                "confidence_level": 0.85
            }
        }
        
        return market_trends
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch market trends: {str(e)}")

@app.post("/ingest/upload", tags=["Document Ingestion"])
async def upload_document_for_ingestion(
    file: UploadFile = File(...),
    document_type: str = Form("general"),
    priority: str = Form("normal")
):
    """
    Upload a document for ingestion into the RAG system
    """
    try:
        # Validate file type
        if not file.filename or not any(file.filename.lower().endswith(ext) for ext in ['.pdf', '.docx', '.txt']):
            raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, DOCX, and TXT files are allowed.")
        
        # Validate file size (10MB limit)
        if file.size and file.size > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large. Maximum size is 10MB.")
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_extension = Path(file.filename).suffix
        safe_filename = f"{file_id}{file_extension}"
        
        # Save file
        file_path = Path(UPLOAD_DIR) / safe_filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process document for ingestion
        try:
            # Extract text from document
            extracted_text = ""
            if file_extension.lower() == '.pdf':
                import PyPDF2
                with open(file_path, 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    for page in pdf_reader.pages:
                        extracted_text += page.extract_text() + "\n"
            elif file_extension.lower() == '.docx':
                from docx import Document
                doc = Document(file_path)
                for paragraph in doc.paragraphs:
                    extracted_text += paragraph.text + "\n"
            elif file_extension.lower() == '.txt':
                with open(file_path, 'r', encoding='utf-8') as txt_file:
                    extracted_text = txt_file.read()
            
            # Store in ChromaDB for RAG
            if rag_service and extracted_text:
                # Split text into chunks
                chunks = [extracted_text[i:i+1000] for i in range(0, len(extracted_text), 1000)]
                
                # Add to ChromaDB
                for i, chunk in enumerate(chunks):
                    rag_service.add_document(
                        document_id=f"{file_id}_chunk_{i}",
                        content=chunk,
                        metadata={
                            "filename": file.filename,
                            "document_type": document_type,
                            "priority": priority,
                            "chunk_index": i,
                            "total_chunks": len(chunks)
                        }
                    )
            
            return {
                "file_id": file_id,
                "filename": file.filename,
                "document_type": document_type,
                "priority": priority,
                "status": "uploaded_and_processed",
                "chunks_created": len(chunks) if extracted_text else 0,
                "file_size": file.size,
                "message": "Document uploaded and processed successfully"
            }
            
        except Exception as processing_error:
            # If processing fails, still return upload success but with error message
            return {
                "file_id": file_id,
                "filename": file.filename,
                "document_type": document_type,
                "priority": priority,
                "status": "uploaded_processing_failed",
                "error": str(processing_error),
                "file_size": file.size,
                "message": "Document uploaded but processing failed"
            }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/conversation/{session_id}")
async def get_conversation_by_session(session_id: str):
    """Get conversation and messages by session ID"""
    try:
        with engine.connect() as conn:
            # Get conversation
            result = conn.execute(text("""
                SELECT id, session_id, role, title, created_at, updated_at, is_active
                FROM conversations
                WHERE session_id = :session_id AND is_active = TRUE
            """), {"session_id": session_id})
            
            row = result.fetchone()
            if not row:
                # Create new conversation if not exists
                result = conn.execute(text("""
                    INSERT INTO conversations (session_id, role, title)
                    VALUES (:session_id, :role, :title)
                    RETURNING id, session_id, role, title, created_at, updated_at, is_active
                """), {
                    "session_id": session_id,
                    "role": "agent",  # Default role
                    "title": f"Chat Session - {session_id}"
                })
                row = result.fetchone()
                conn.commit()
            
            conversation_id = row[0]
            
            # Get messages for this conversation
            messages_result = conn.execute(text("""
                SELECT id, conversation_id, role, content, timestamp, message_type, metadata
                FROM messages
                WHERE conversation_id = :conversation_id
                ORDER BY timestamp ASC
            """), {"conversation_id": conversation_id})
            
            messages = []
            for msg_row in messages_result:
                messages.append({
                    "sender": "user" if msg_row[2] == "user" else "ai",
                    "text": msg_row[3],
                    "timestamp": str(msg_row[4]),
                    "sources": json.loads(msg_row[6])["sources"] if msg_row[6] and json.loads(msg_row[6]).get("sources") else []
                })
            
            return {
                "conversation_id": conversation_id,
                "session_id": session_id,
                "role": row[2],
                "title": row[3],
                "messages": messages,
                "created_at": str(row[4]),
                "updated_at": str(row[5])
            }
    except Exception as e:
        print(f"Error in get_conversation_by_session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    
    # Start the daily briefing scheduler
    try:
        from scheduler import start_daily_briefing_scheduler
        scheduler = start_daily_briefing_scheduler()
        if scheduler:
            print("✅ Daily briefing scheduler started successfully")
        else:
            print("⚠️ Failed to start daily briefing scheduler")
    except Exception as e:
        print(f"❌ Error starting daily briefing scheduler: {e}")
    
    uvicorn.run(
        app, 
        host=HOST, 
        port=PORT,
        log_level=DEBUG.lower(),
        reload=DEBUG and not IS_PRODUCTION
    )