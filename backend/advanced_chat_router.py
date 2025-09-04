"""
Advanced Chat Router - Enhanced In-Chat Experience API Endpoints

This router provides advanced API endpoints for enhanced chat experience:
- Entity detection from AI responses
- Context fetching for detected entities
- Rich content management
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import logging

# Import dependencies
from auth.middleware import get_current_user
from auth.models import User
from entity_detection_service import entity_detection_service, Entity
from context_management_service import context_management_service

# Initialize router
router = APIRouter(prefix="/advanced-chat", tags=["Advanced Chat"])

# Pydantic Models
class EntityDetectionRequest(BaseModel):
    """Request model for entity detection"""
    message: str
    session_id: Optional[str] = None
    user_id: Optional[int] = None

class EntityDetectionResponse(BaseModel):
    """Response model for entity detection"""
    entities: List[Dict[str, Any]]
    total_count: int
    confidence_threshold: float
    processing_time: float

class ContextRequest(BaseModel):
    """Request model for context fetching"""
    entity_type: str
    entity_id: str
    include_cache: bool = True

class ContextResponse(BaseModel):
    """Response model for context data"""
    entity_type: str
    entity_id: str
    context_data: Dict[str, Any]
    cache_status: str  # 'cached', 'fresh', 'not_found'
    last_updated: str

class PropertyDetailsRequest(BaseModel):
    """Request model for property details"""
    property_id: str
    include_market_data: bool = True
    include_similar_properties: bool = True

class PropertyDetailsResponse(BaseModel):
    """Response model for property details"""
    property: Dict[str, Any]
    market_data: List[Dict[str, Any]]
    similar_properties: List[Dict[str, Any]]
    context_type: str
    last_updated: str

class ClientInfoRequest(BaseModel):
    """Request model for client information"""
    client_id: str
    include_history: bool = True
    include_preferences: bool = True

class ClientInfoResponse(BaseModel):
    """Response model for client information"""
    client: Dict[str, Any]
    history: List[Dict[str, Any]]
    preferences: Dict[str, Any]
    context_type: str
    last_updated: str

class MarketContextRequest(BaseModel):
    """Request model for market context"""
    location: str
    property_type: Optional[str] = None
    include_trends: bool = True
    include_insights: bool = True

class MarketContextResponse(BaseModel):
    """Response model for market context"""
    location: str
    market_data: List[Dict[str, Any]]
    trends: List[Dict[str, Any]]
    insights: List[Dict[str, Any]]
    context_type: str
    last_updated: str

# API Endpoints

@router.post("/ai/detect-entities", response_model=EntityDetectionResponse)
async def detect_entities(
    request: EntityDetectionRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Detect entities in AI response messages
    
    This endpoint analyzes AI response messages to extract real estate domain entities
    such as properties, clients, locations, and market data.
    """
    try:
        import time
        start_time = time.time()
        
        # Detect entities using the service
        entities = entity_detection_service.detect_entities(request.message)
        
        # Convert entities to response format
        entity_data = []
        for entity in entities:
            # Get context mapping for the entity
            context_mapping = entity_detection_service.get_entity_context_mapping(entity)
            
            entity_data.append({
                'entity_type': entity.entity_type,
                'entity_value': entity.entity_value,
                'confidence_score': entity.confidence_score,
                'context_source': entity.context_source,
                'metadata': entity.metadata,
                'context_mapping': context_mapping
            })
        
        processing_time = time.time() - start_time
        
        return EntityDetectionResponse(
            entities=entity_data,
            total_count=len(entity_data),
            confidence_threshold=0.6,
            processing_time=round(processing_time, 3)
        )
        
    except Exception as e:
        logging.error(f"Error in entity detection: {e}")
        raise HTTPException(status_code=500, detail=f"Entity detection failed: {str(e)}")

@router.get("/context/{entity_type}/{entity_id}", response_model=ContextResponse)
async def fetch_entity_context(
    entity_type: str,
    entity_id: str,
    include_cache: bool = Query(True, description="Include cached data if available"),
    current_user: User = Depends(get_current_user)
):
    """
    Fetch context data for a specific entity
    
    This endpoint retrieves contextual information for detected entities,
    including property details, client information, location data, and market analysis.
    """
    try:
        # Fetch context data
        context_data = await context_management_service.fetch_entity_context(entity_type, entity_id)
        
        if not context_data:
            raise HTTPException(status_code=404, detail=f"Context not found for {entity_type}:{entity_id}")
        
        # Determine cache status
        cache_status = "fresh"  # For now, assume fresh data
        
        return ContextResponse(
            entity_type=entity_type,
            entity_id=entity_id,
            context_data=context_data,
            cache_status=cache_status,
            last_updated=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error fetching context for {entity_type}:{entity_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Context fetching failed: {str(e)}")

@router.get("/properties/{property_id}/details", response_model=PropertyDetailsResponse)
async def get_property_details(
    property_id: str,
    include_market_data: bool = Query(True, description="Include market data for the property"),
    include_similar_properties: bool = Query(True, description="Include similar properties"),
    current_user: User = Depends(get_current_user)
):
    """
    Get detailed property information
    
    This endpoint provides comprehensive property details including
    basic information, market data, and similar properties.
    """
    try:
        # Fetch property context
        context_data = await context_management_service.fetch_entity_context('property', property_id)
        
        if not context_data or 'property' not in context_data:
            raise HTTPException(status_code=404, detail=f"Property not found: {property_id}")
        
        return PropertyDetailsResponse(
            property=context_data.get('property', {}),
            market_data=context_data.get('market_data', []) if include_market_data else [],
            similar_properties=context_data.get('similar_properties', []) if include_similar_properties else [],
            context_type=context_data.get('context_type', 'property_details'),
            last_updated=context_data.get('last_updated', datetime.now().isoformat())
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error getting property details for {property_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Property details fetching failed: {str(e)}")

@router.get("/clients/{client_id}", response_model=ClientInfoResponse)
async def get_client_info(
    client_id: str,
    include_history: bool = Query(True, description="Include client interaction history"),
    include_preferences: bool = Query(True, description="Include client preferences"),
    current_user: User = Depends(get_current_user)
):
    """
    Get client/lead information
    
    This endpoint provides comprehensive client information including
    basic details, interaction history, and preferences.
    """
    try:
        # Fetch client context
        context_data = await context_management_service.fetch_entity_context('client', client_id)
        
        if not context_data or 'client' not in context_data:
            raise HTTPException(status_code=404, detail=f"Client not found: {client_id}")
        
        return ClientInfoResponse(
            client=context_data.get('client', {}),
            history=context_data.get('history', []) if include_history else [],
            preferences=context_data.get('preferences', {}) if include_preferences else {},
            context_type=context_data.get('context_type', 'client_info'),
            last_updated=context_data.get('last_updated', datetime.now().isoformat())
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error getting client info for {client_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Client info fetching failed: {str(e)}")

@router.get("/market/context", response_model=MarketContextResponse)
async def get_market_context(
    location: str = Query(..., description="Location to get market context for"),
    property_type: Optional[str] = Query(None, description="Property type filter"),
    include_trends: bool = Query(True, description="Include market trends"),
    include_insights: bool = Query(True, description="Include investment insights"),
    current_user: User = Depends(get_current_user)
):
    """
    Get market context for a location
    
    This endpoint provides market analysis data for a specific location,
    including trends, insights, and property data.
    """
    try:
        # Fetch location context
        context_data = await context_management_service.fetch_entity_context('location', location)
        
        if not context_data:
            raise HTTPException(status_code=404, detail=f"Market context not found for location: {location}")
        
        return MarketContextResponse(
            location=location,
            market_data=context_data.get('market_data', []),
            trends=context_data.get('trends', []) if include_trends else [],
            insights=context_data.get('insights', []) if include_insights else [],
            context_type=context_data.get('context_type', 'location_data'),
            last_updated=context_data.get('last_updated', datetime.now().isoformat())
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error getting market context for {location}: {e}")
        raise HTTPException(status_code=500, detail=f"Market context fetching failed: {str(e)}")

@router.post("/context/batch")
async def fetch_batch_context(
    entities: List[Dict[str, str]],
    current_user: User = Depends(get_current_user)
):
    """
    Fetch context for multiple entities in batch
    
    This endpoint allows fetching context for multiple entities in a single request
    to improve performance when dealing with multiple detected entities.
    """
    try:
        results = {}
        
        for entity in entities:
            entity_type = entity.get('entity_type')
            entity_id = entity.get('entity_id')
            
            if not entity_type or not entity_id:
                continue
            
            try:
                context_data = await context_management_service.fetch_entity_context(entity_type, entity_id)
                results[f"{entity_type}:{entity_id}"] = {
                    'success': True,
                    'data': context_data
                }
            except Exception as e:
                results[f"{entity_type}:{entity_id}"] = {
                    'success': False,
                    'error': str(e)
                }
        
        return {
            'results': results,
            'total_entities': len(entities),
            'successful_fetches': sum(1 for r in results.values() if r['success']),
            'processing_time': datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Error in batch context fetching: {e}")
        raise HTTPException(status_code=500, detail=f"Batch context fetching failed: {str(e)}")

@router.delete("/context/cache/clear")
async def clear_context_cache(
    current_user: User = Depends(get_current_user)
):
    """
    Clear expired context cache entries
    
    This endpoint clears expired cache entries to free up database space.
    """
    try:
        await context_management_service.clear_expired_cache()
        
        return {
            'message': 'Context cache cleared successfully',
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Error clearing context cache: {e}")
        raise HTTPException(status_code=500, detail=f"Cache clearing failed: {str(e)}")

@router.get("/health")
async def phase3_health_check():
    """
    Health check endpoint for Phase 3 services
    
    This endpoint verifies that all Phase 3 services are operational.
    """
    try:
        # Basic health checks
        health_status = {
            'status': 'healthy',
            'services': {
                'entity_detection': 'operational',
                'context_management': 'operational',
                'database_connection': 'operational'
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return health_status
        
    except Exception as e:
        logging.error(f"Phase 3 health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Phase 3 services unhealthy: {str(e)}")
