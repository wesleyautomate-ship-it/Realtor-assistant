"""
Voice Processing Router for Laura AI Real Estate Assistant

This router handles voice processing endpoints and integrates with the existing
async processing system for batch operations.
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
import logging

# Import existing services
from services.voice_service import VoiceService
from services.content_management_service import ContentManagementService
from config.settings import get_settings

logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

# Initialize services
voice_service = VoiceService(settings.database_url, settings.google_api_key)
content_service = ContentManagementService(settings.database_url, settings.google_api_key)

# Create router
router = APIRouter(prefix="/voice", tags=["voice-processing"])

# =============================================
# REQUEST/RESPONSE MODELS
# =============================================

class VoiceProcessingRequest(BaseModel):
    """Request model for voice processing"""
    user_id: str
    session_id: Optional[str] = None
    transcript: Optional[str] = None  # For testing without audio

class VoiceProcessingResponse(BaseModel):
    """Response model for voice processing"""
    request_id: str
    transcript: str
    intent: str
    entities: Dict[str, Any]
    processing_type: str
    status: str
    response: Optional[Dict[str, Any]] = None
    eta: Optional[str] = None

class ContentGenerationRequest(BaseModel):
    """Request model for content generation"""
    template_type: str
    property_data: Dict[str, Any]
    user_preferences: Dict[str, Any]

class ContentGenerationResponse(BaseModel):
    """Response model for content generation"""
    content_id: str
    template_type: str
    status: str
    approval_status: str
    created_at: str

class VoiceRequestStatusResponse(BaseModel):
    """Response model for voice request status"""
    request_id: str
    status: str
    transcript: str
    intent: str
    processing_type: str
    ai_status: Optional[str] = None
    result_data: Optional[Dict[str, Any]] = None
    created_at: str
    completed_at: Optional[str] = None

# =============================================
# VOICE PROCESSING ENDPOINTS
# =============================================

@router.post("/process", response_model=VoiceProcessingResponse)
async def process_voice_request(
    audio_file: UploadFile = File(...),
    user_id: str = Form(...),
    session_id: Optional[str] = Form(None),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Process voice request and route to appropriate handler
    
    Args:
        audio_file: Audio file from voice input
        user_id: User ID for the request
        session_id: Optional session ID for tracking
        background_tasks: Background tasks for batch processing
        
    Returns:
        Voice processing response with transcript, intent, and processing type
    """
    try:
        # Read audio data
        audio_data = await audio_file.read()
        
        # Process voice request
        result = await voice_service.process_voice_request(
            audio_data=audio_data,
            user_id=user_id,
            session_id=session_id
        )
        
        # If batch processing, add to background tasks
        if result['processing_type'] == 'batch':
            background_tasks.add_task(process_batch_voice_request, result['request_id'])
        
        return VoiceProcessingResponse(
            request_id=result['request_id'],
            transcript=result['transcript'],
            intent=result['intent'],
            entities=result['entities'],
            processing_type=result['processing_type'],
            status=result['status'],
            response=result.get('response'),
            eta=result.get('eta')
        )
        
    except Exception as e:
        logger.error(f"Error processing voice request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process-text", response_model=VoiceProcessingResponse)
async def process_voice_text(
    request: VoiceProcessingRequest,
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Process voice request from text transcript (for testing)
    
    Args:
        request: Voice processing request with transcript
        background_tasks: Background tasks for batch processing
        
    Returns:
        Voice processing response
    """
    try:
        if not request.transcript:
            raise HTTPException(status_code=400, detail="Transcript is required")
        
        # Simulate audio data for text processing
        audio_data = request.transcript.encode('utf-8')
        
        # Process voice request
        result = await voice_service.process_voice_request(
            audio_data=audio_data,
            user_id=request.user_id,
            session_id=request.session_id
        )
        
        # If batch processing, add to background tasks
        if result['processing_type'] == 'batch':
            background_tasks.add_task(process_batch_voice_request, result['request_id'])
        
        return VoiceProcessingResponse(
            request_id=result['request_id'],
            transcript=result['transcript'],
            intent=result['intent'],
            entities=result['entities'],
            processing_type=result['processing_type'],
            status=result['status'],
            response=result.get('response'),
            eta=result.get('eta')
        )
        
    except Exception as e:
        logger.error(f"Error processing voice text: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{request_id}", response_model=VoiceRequestStatusResponse)
async def get_voice_request_status(request_id: str):
    """
    Get status of voice request
    
    Args:
        request_id: Voice request ID
        
    Returns:
        Voice request status information
    """
    try:
        status = await voice_service.get_voice_request_status(request_id)
        
        if status.get('error'):
            raise HTTPException(status_code=404, detail=status['error'])
        
        return VoiceRequestStatusResponse(
            request_id=status['request_id'],
            status=status['status'],
            transcript=status['transcript'],
            intent=status['intent'],
            processing_type=status['processing_type'],
            ai_status=status.get('ai_status'),
            result_data=status.get('result_data'),
            created_at=status['created_at'],
            completed_at=status.get('completed_at')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting voice request status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================
# CONTENT GENERATION ENDPOINTS
# =============================================

@router.post("/content/generate", response_model=ContentGenerationResponse)
async def generate_content(
    request: ContentGenerationRequest,
    user_id: str = Form(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Generate content using specified template
    
    Args:
        request: Content generation request
        user_id: User ID for the request
        background_tasks: Background tasks for content generation
        
    Returns:
        Content generation response
    """
    try:
        # Generate content
        result = await content_service.generate_content(
            template_type=request.template_type,
            property_data=request.property_data,
            user_preferences=request.user_preferences,
            user_id=user_id
        )
        
        # Add to background tasks for any post-processing
        background_tasks.add_task(process_content_generation, result['content_id'])
        
        return ContentGenerationResponse(
            content_id=result['content_id'],
            template_type=result['template_type'],
            status=result['status'],
            approval_status=result['approval_status'],
            created_at=result['created_at']
        )
        
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/content/approve/{content_id}")
async def approve_content(content_id: str, user_id: str = Form(...)):
    """
    Approve generated content for publishing
    
    Args:
        content_id: Content ID to approve
        user_id: User ID approving the content
        
    Returns:
        Approval confirmation
    """
    try:
        result = await content_service.approve_content(content_id, user_id)
        return result
        
    except Exception as e:
        logger.error(f"Error approving content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/content/pending/{user_id}")
async def get_pending_approvals(user_id: str):
    """
    Get pending content approvals for user
    
    Args:
        user_id: User ID
        
    Returns:
        List of pending content approvals
    """
    try:
        approvals = await content_service.get_pending_approvals(user_id)
        return {
            'user_id': user_id,
            'pending_approvals': approvals,
            'count': len(approvals)
        }
        
    except Exception as e:
        logger.error(f"Error getting pending approvals: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================
# BACKGROUND TASK FUNCTIONS
# =============================================

async def process_batch_voice_request(request_id: str):
    """
    Background task for processing batch voice requests
    """
    try:
        logger.info(f"Processing batch voice request: {request_id}")
        
        # Get voice request details
        status = await voice_service.get_voice_request_status(request_id)
        
        if status.get('error'):
            logger.error(f"Voice request not found: {request_id}")
            return
        
        # Process based on intent
        intent = status.get('intent')
        entities = status.get('result_data', {}).get('entities', {})
        
        if intent == 'content_generation':
            # Generate content
            template_type = entities.get('template_type', 'cma')
            property_data = {
                'address': entities.get('property_address', ''),
                'price': entities.get('price', ''),
                'beds': entities.get('bedrooms', ''),
                'baths': entities.get('bathrooms', ''),
                'sqft': entities.get('sqft', ''),
                'features': entities.get('features', [])
            }
            
            user_preferences = {
                'specialty': 'residential',  # Default
                'workflow': 'automated'
            }
            
            # Generate content
            content_result = await content_service.generate_content(
                template_type=template_type,
                property_data=property_data,
                user_preferences=user_preferences,
                user_id=status.get('user_id', '')
            )
            
            # Update voice request with result
            await update_voice_request_result(request_id, {
                'content_id': content_result['content_id'],
                'template_type': template_type,
                'status': 'completed'
            })
            
        else:
            # Handle other intents
            await update_voice_request_result(request_id, {
                'status': 'completed',
                'message': f'Batch processing for {intent} completed'
            })
        
        logger.info(f"Batch voice request processed: {request_id}")
        
    except Exception as e:
        logger.error(f"Error processing batch voice request {request_id}: {e}")
        await update_voice_request_result(request_id, {
            'status': 'failed',
            'error': str(e)
        })

async def process_content_generation(content_id: str):
    """
    Background task for post-processing content generation
    """
    try:
        logger.info(f"Post-processing content generation: {content_id}")
        
        # Add any post-processing logic here
        # For example: send notifications, update analytics, etc.
        
        logger.info(f"Content generation post-processing completed: {content_id}")
        
    except Exception as e:
        logger.error(f"Error in content generation post-processing {content_id}: {e}")

async def update_voice_request_result(request_id: str, result_data: Dict[str, Any]):
    """
    Update voice request with result data
    """
    try:
        # This would update the database with the result
        # Implementation depends on your database setup
        logger.info(f"Updated voice request {request_id} with result: {result_data}")
        
    except Exception as e:
        logger.error(f"Error updating voice request result {request_id}: {e}")

# =============================================
# HEALTH CHECK ENDPOINTS
# =============================================

@router.get("/health")
async def voice_health_check():
    """
    Health check for voice processing service
    """
    return {
        "status": "healthy",
        "service": "voice-processing",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@router.get("/templates")
async def get_available_templates():
    """
    Get available content templates
    """
    return {
        "templates": [
            {
                "type": "cma",
                "name": "Comparative Market Analysis",
                "description": "Generate comprehensive CMA reports with pricing strategies"
            },
            {
                "type": "just_listed",
                "name": "Just Listed Marketing",
                "description": "Create compelling just listed marketing content"
            },
            {
                "type": "just_sold",
                "name": "Just Sold Celebration",
                "description": "Generate just sold celebration content"
            },
            {
                "type": "open_house",
                "name": "Open House Invitation",
                "description": "Create open house invitations and promotional materials"
            },
            {
                "type": "newsletter",
                "name": "Market Newsletter",
                "description": "Generate market newsletters and client communications"
            },
            {
                "type": "investor_deck",
                "name": "Investment Presentation",
                "description": "Create investment presentations and property analysis"
            },
            {
                "type": "brochure",
                "name": "Property Brochure",
                "description": "Generate property brochures and marketing materials"
            },
            {
                "type": "social_banner",
                "name": "Social Media Banner",
                "description": "Create social media banners and graphics"
            },
            {
                "type": "story_content",
                "name": "Social Media Stories",
                "description": "Generate social media story content"
            }
        ]
    }
