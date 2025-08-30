"""
Chat Sessions Router - FastAPI Router for Session and Conversation Management

This router handles all chat session and conversation management endpoints
migrated from main.py to maintain frontend compatibility while following
the secure architecture patterns of main_secure.py.
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Union
from sqlalchemy import text
from datetime import datetime
import uuid
import json
import time

# Import dependencies
from auth.middleware import get_current_user
from auth.models import User
from database_manager import get_db_connection
from config.settings import DATABASE_URL

# Initialize router
router = APIRouter(prefix="/sessions", tags=["Chat Sessions"])

# Root level chat endpoint (for frontend compatibility)
root_router = APIRouter(tags=["Chat"])

# Pydantic Models
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

class ChatRequest(BaseModel):
    """Chat request model"""
    message: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    role: str = "client"
    file_upload: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    session_id: str
    message_id: str
    timestamp: str
    sources: List[Dict[str, Any]] = []
    confidence: float
    intent: str
    metadata: Dict[str, Any] = {}

# Helper Functions
def get_ai_manager():
    """Get AI manager instance"""
    try:
        from ai_manager import AIEnhancementManager
        from config.settings import GOOGLE_API_KEY, AI_MODEL
        import google.generativeai as genai
        
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel(AI_MODEL)
        return AIEnhancementManager(DATABASE_URL, model)
    except Exception as e:
        print(f"Error initializing AI manager: {e}")
        return None

def get_rag_service():
    """Get RAG service instance"""
    try:
        from rag_service import ImprovedRAGService
        from config.settings import CHROMA_HOST, CHROMA_PORT
        return ImprovedRAGService(DATABASE_URL, CHROMA_HOST, CHROMA_PORT)
    except Exception as e:
        print(f"Error initializing RAG service: {e}")
        return None

# Router Endpoints

@router.post("", response_model=ChatSessionResponse)
async def create_new_chat_session(
    request: ChatSessionCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new ChatGPT-style chat session"""
    try:
        session_id = str(uuid.uuid4())
        
        with get_db_connection() as conn:
            # Create new conversation with user's actual role
            user_role = current_user.role
            session_title = f"Chat Session - {current_user.first_name} {current_user.last_name} ({user_role.title()})"
            
            result = conn.execute(text("""
                INSERT INTO conversations (session_id, user_id, role, title, is_active)
                VALUES (:session_id, :user_id, :role, :title, TRUE)
                RETURNING id, session_id, role, title, created_at, updated_at, is_active
            """), {
                "session_id": session_id,
                "user_id": current_user.id,
                "role": user_role,
                "title": session_title
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
            
            return ChatSessionResponse(
                session_id=session_id,
                title=session_title,
                role=user_role,
                created_at=str(row[4]),
                updated_at=str(row[5]),
                message_count=0,
                user_preferences=request.user_preferences or {},
                is_active=row[6]
            )
            
    except Exception as e:
        print(f"Error creating chat session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("")
async def list_chat_sessions(
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    days: Optional[int] = Query(None, description="Only sessions from last N days")
):
    """List chat sessions with user authentication and role-based filtering"""
    try:
        offset = (page - 1) * limit
        
        with get_db_connection() as conn:
            # Build query based on user role with date filter
            if current_user.role == "admin":
                # Admin can see all conversations
                if days:
                    query = """
                        SELECT id, session_id, title, created_at, updated_at, is_active,
                               (SELECT COUNT(*) FROM messages WHERE conversation_id = conversations.id) as message_count
                        FROM conversations 
                        WHERE created_at >= NOW() - INTERVAL ':days days'
                        ORDER BY created_at DESC 
                        LIMIT :limit OFFSET :offset
                    """
                    params = {"limit": limit, "offset": offset, "days": days}
                else:
                    query = """
                        SELECT id, session_id, title, created_at, updated_at, is_active,
                               (SELECT COUNT(*) FROM messages WHERE conversation_id = conversations.id) as message_count
                        FROM conversations 
                        ORDER BY created_at DESC 
                        LIMIT :limit OFFSET :offset
                    """
                    params = {"limit": limit, "offset": offset}
                    
            elif current_user.role == "agent":
                # Agent can see their own conversations
                if days:
                    query = """
                        SELECT id, session_id, title, created_at, updated_at, is_active,
                               (SELECT COUNT(*) FROM messages WHERE conversation_id = conversations.id) as message_count
                        FROM conversations 
                        WHERE user_id = :user_id 
                        AND created_at >= NOW() - INTERVAL ':days days'
                        ORDER BY created_at DESC 
                        LIMIT :limit OFFSET :offset
                    """
                    params = {"user_id": current_user.id, "limit": limit, "offset": offset, "days": days}
                else:
                    query = """
                        SELECT id, session_id, title, created_at, updated_at, is_active,
                               (SELECT COUNT(*) FROM messages WHERE conversation_id = conversations.id) as message_count
                        FROM conversations 
                        WHERE user_id = :user_id
                        ORDER BY created_at DESC 
                        LIMIT :limit OFFSET :offset
                    """
                    params = {"user_id": current_user.id, "limit": limit, "offset": offset}
                    
            else:
                # Employee can only see their own conversations
                if days:
                    query = """
                        SELECT id, session_id, title, created_at, updated_at, is_active,
                               (SELECT COUNT(*) FROM messages WHERE conversation_id = conversations.id) as message_count
                        FROM conversations 
                        WHERE user_id = :user_id 
                        AND created_at >= NOW() - INTERVAL ':days days'
                        ORDER BY created_at DESC 
                        LIMIT :limit OFFSET :offset
                    """
                    params = {"user_id": current_user.id, "limit": limit, "offset": offset, "days": days}
                else:
                    query = """
                        SELECT id, session_id, title, created_at, updated_at, is_active,
                               (SELECT COUNT(*) FROM messages WHERE conversation_id = conversations.id) as message_count
                        FROM conversations 
                        WHERE user_id = :user_id
                        ORDER BY created_at DESC 
                        LIMIT :limit OFFSET :offset
                    """
                    params = {"user_id": current_user.id, "limit": limit, "offset": offset}
            
            result = conn.execute(text(query), params)
            sessions = [dict(row) for row in result]
            
            # Get total count for pagination based on user role
            if current_user.role == "admin":
                if days:
                    count_query = """
                        SELECT COUNT(*) FROM conversations 
                        WHERE created_at >= NOW() - INTERVAL ':days days'
                    """
                    count_params = {"days": days}
                else:
                    count_query = "SELECT COUNT(*) FROM conversations"
                    count_params = {}
            elif current_user.role == "agent":
                if days:
                    count_query = """
                        SELECT COUNT(*) FROM conversations 
                        WHERE user_id = :user_id 
                        AND created_at >= NOW() - INTERVAL ':days days'
                    """
                    count_params = {"user_id": current_user.id, "days": days}
                else:
                    count_query = """
                        SELECT COUNT(*) FROM conversations 
                        WHERE user_id = :user_id
                    """
                    count_params = {"user_id": current_user.id}
            else:
                if days:
                    count_query = """
                        SELECT COUNT(*) FROM conversations 
                        WHERE user_id = :user_id 
                        AND created_at >= NOW() - INTERVAL ':days days'
                    """
                    count_params = {"user_id": current_user.id, "days": days}
                else:
                    count_query = "SELECT COUNT(*) FROM conversations WHERE user_id = :user_id"
                    count_params = {"user_id": current_user.id}
            
            count_result = conn.execute(text(count_query), count_params)
            total_count = count_result.fetchone()[0]
            
            return {
                "sessions": sessions,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total_count,
                    "pages": (total_count + limit - 1) // limit
                }
            }
            
    except Exception as e:
        print(f"Error listing chat sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{session_id}", response_model=ChatHistoryResponse)
async def get_chat_session(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get chat session with full history - with user access control"""
    try:
        with get_db_connection() as conn:
            # Check if user has access to this session
            if current_user.role == "admin":
                # Admin can access any session
                session_query = """
                    SELECT id, session_id, role, title, created_at, updated_at, is_active
                    FROM conversations 
                    WHERE session_id = :session_id AND is_active = TRUE
                """
                session_params = {"session_id": session_id}
            elif current_user.role == "agent":
                # Agent can access their own sessions
                session_query = """
                    SELECT id, session_id, role, title, created_at, updated_at, is_active
                    FROM conversations 
                    WHERE session_id = :session_id AND is_active = TRUE 
                    AND user_id = :user_id
                """
                session_params = {"session_id": session_id, "user_id": current_user.id}
            else:
                # Employee can only access their own sessions
                session_query = """
                    SELECT id, session_id, role, title, created_at, updated_at, is_active
                    FROM conversations 
                    WHERE session_id = :session_id AND is_active = TRUE AND user_id = :user_id
                """
                session_params = {"session_id": session_id, "user_id": current_user.id}
            
            session_result = conn.execute(text(session_query), session_params)
            session_row = session_result.fetchone()
            
            if not session_row:
                raise HTTPException(status_code=404, detail="Chat session not found or access denied")
            
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
                ai_manager = get_ai_manager()
                if ai_manager:
                    conversation_summary = ai_manager.get_conversation_summary(session_id)
                    summary_text = conversation_summary.get('summary', '') if conversation_summary else None
                else:
                    summary_text = None
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

@router.post("/{session_id}/chat", response_model=ChatResponse)
async def chat_with_session(
    session_id: str, 
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """Enhanced chat endpoint with session management"""
    start_time = time.time()
    
    try:
        # Get RAG service
        rag_service = get_rag_service()
        if not rag_service:
            raise HTTPException(status_code=500, detail="RAG service not available")
        
        # Verify session exists and user has access
        with get_db_connection() as conn:
            session_result = conn.execute(text("""
                SELECT id, session_id, role, title, user_id
                FROM conversations 
                WHERE session_id = :session_id AND is_active = TRUE
            """), {"session_id": session_id})
            
            session_row = session_result.fetchone()
            if not session_row:
                raise HTTPException(status_code=404, detail="Chat session not found")
            
            # Check if user has access to this session
            if current_user.role != "admin" and session_row[4] != current_user.id:
                raise HTTPException(status_code=403, detail="Access denied to this session")
        
        # Use RAG service as the single source of truth for conversational AI
        response_text = rag_service.get_response(
            message=request.message,
            role=request.role,
            session_id=session_id
        )
        
        # Save messages to database
        with get_db_connection() as conn:
            # Save user message
            conn.execute(text("""
                INSERT INTO messages (conversation_id, role, content, message_type, metadata)
                VALUES (:conversation_id, 'user', :content, 'text', :metadata)
            """), {
                "conversation_id": session_row[0],
                "content": request.message,
                "metadata": json.dumps({"file_upload": request.file_upload}) if request.file_upload else None
            })
            
            # Save assistant response
            conn.execute(text("""
                INSERT INTO messages (conversation_id, role, content, message_type, metadata)
                VALUES (:conversation_id, 'assistant', :content, 'text', :metadata)
            """), {
                "conversation_id": session_row[0],
                "content": response_text,
                "metadata": json.dumps({"sources": ["Dubai Real Estate Database", "Market Analysis Reports"]})
            })
        
        # Track performance
        end_time = time.time()
        response_time = end_time - start_time
        
        return ChatResponse(
            response=response_text,
            session_id=session_id,
            message_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow().isoformat() + 'Z',
            sources=[
                {"source": "Dubai Real Estate Database", "relevance": 0.9},
                {"source": "Market Analysis Reports", "relevance": 0.8},
                {"source": "Property Listings", "relevance": 0.7}
            ],
            confidence=0.8,
            intent="general",
            metadata={"response_time": response_time}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{session_id}")
async def delete_chat_session(session_id: str):
    """Delete a chat session (ChatGPT-style)"""
    try:
        with get_db_connection() as conn:
            # Soft delete - mark as inactive
            result = conn.execute(text("""
                UPDATE conversations 
                SET is_active = FALSE, updated_at = CURRENT_TIMESTAMP
                WHERE session_id = :session_id
                RETURNING id
            """), {"session_id": session_id})
            
            if not result.fetchone():
                raise HTTPException(status_code=404, detail="Chat session not found")
            
            return {"success": True, "message": "Chat session deleted"}
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting chat session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{session_id}/clear")
async def clear_chat_session(session_id: str):
    """Clear all messages in a chat session (keep session)"""
    try:
        with get_db_connection() as conn:
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
            
            # Clear AI manager memory cache if available
            try:
                ai_manager = get_ai_manager()
                if ai_manager and hasattr(ai_manager, 'memory_cache') and session_id in ai_manager.memory_cache:
                    del ai_manager.memory_cache[session_id]
            except:
                pass  # Ignore if AI manager is not available
            
            return {"success": True, "message": "Chat session cleared"}
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error clearing chat session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Conversation history endpoint (for frontend compatibility)
@root_router.get("/conversation/{session_id}", response_model=ChatHistoryResponse)
async def get_conversation_history(session_id: str):
    """Get conversation history for a specific session"""
    try:
        with get_db_connection() as conn:
            # Get conversation details
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
            for msg_row in messages_result.fetchall():
                try:
                    metadata = json.loads(msg_row[6]) if msg_row[6] else {}
                except (json.JSONDecodeError, TypeError):
                    print(f"Error parsing metadata for message {msg_row[0]}: {msg_row[6]}")
                    metadata = {}
                
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
            
            # Temporarily disable AI manager to fix conversation endpoint
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
        print(f"Error getting conversation history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Root level chat endpoint (for frontend compatibility)
@root_router.post("/chat", response_model=ChatResponse)
async def chat_with_rag(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """Enhanced chat endpoint with RAG and session management"""
    try:
        # Generate session ID if not provided
        if not request.session_id:
            request.session_id = str(uuid.uuid4())
        
        # Get RAG service
        rag_service = get_rag_service()
        if not rag_service:
            raise HTTPException(status_code=500, detail="RAG service not available")
        
        # Use RAG service as the single source of truth for conversational AI
        response_text = rag_service.get_response(
            message=request.message,
            role=request.role,
            session_id=request.session_id
        )
        
        # Save messages to database if session exists
        if request.session_id:
            try:
                with get_db_connection() as conn:
                    # Check if session exists
                    session_result = conn.execute(text("""
                        SELECT id FROM conversations 
                        WHERE session_id = :session_id AND is_active = TRUE
                    """), {"session_id": request.session_id})
                    
                    session_row = session_result.fetchone()
                    if session_row:
                        # Save user message
                        conn.execute(text("""
                            INSERT INTO messages (conversation_id, role, content, message_type, metadata)
                            VALUES (:conversation_id, 'user', :content, 'text', :metadata)
                        """), {
                            "conversation_id": session_row[0],
                            "content": request.message,
                            "metadata": json.dumps({"file_upload": request.file_upload}) if request.file_upload else None
                        })
                        
                        # Save assistant response
                        conn.execute(text("""
                            INSERT INTO messages (conversation_id, role, content, message_type, metadata)
                            VALUES (:conversation_id, 'assistant', :content, 'text', :metadata)
                        """), {
                            "conversation_id": session_row[0],
                            "content": response_text,
                            "metadata": json.dumps({"sources": ["Dubai Real Estate Database", "Market Analysis Reports"]})
                        })
            except Exception as db_error:
                print(f"Database error in chat endpoint: {db_error}")
                # Continue without saving to database
        
        return ChatResponse(
            response=response_text,
            session_id=request.session_id,
            message_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow().isoformat() + 'Z',
            sources=["Dubai Real Estate Database", "Market Analysis Reports", "Property Listings"],
            confidence=0.8,
            intent="general",
            metadata={}
        )
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
