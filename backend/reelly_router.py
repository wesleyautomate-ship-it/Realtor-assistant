"""
Reelly Router - FastAPI Router for Reelly API Integration

This router handles all Reelly API integration endpoints migrated from main.py
to maintain frontend compatibility while following the secure architecture
patterns of main_secure.py.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

# Import Reelly service
try:
    from reelly_service import ReellyService
    reelly_service = ReellyService()
    RELLY_AVAILABLE = True
    print("✅ Reelly service initialized successfully")
except ImportError:
    reelly_service = None
    RELLY_AVAILABLE = False
    print("⚠️ Reelly service not available - reelly_service module not found")

# Initialize router
router = APIRouter(prefix="/api/v1", tags=["Reelly Integration"])

# Pydantic Models
class Developer(BaseModel):
    """Developer data model"""
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    contact_info: Optional[Dict[str, Any]] = None

class Area(BaseModel):
    """Area data model"""
    id: Optional[int] = None
    name: Optional[str] = None
    country_id: Optional[int] = None
    description: Optional[str] = None
    coordinates: Optional[Dict[str, float]] = None

class ReellyProperty(BaseModel):
    """Reelly property data model"""
    id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    area_sqft: Optional[float] = None
    property_type: Optional[str] = None
    location: Optional[str] = None
    developer: Optional[str] = None
    images: Optional[List[str]] = None
    amenities: Optional[List[str]] = None
    status: Optional[str] = None

class ReellyStatus(BaseModel):
    """Reelly service status model"""
    enabled: bool
    status: str
    message: str
    last_check: Optional[str] = None
    api_version: Optional[str] = None

# Router Endpoints

@router.get("/reference/developers", tags=["Reference Data"])
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

@router.get("/reference/areas", tags=["Reference Data"])
async def get_all_areas(country_id: int = Query(1, description="Country ID")):
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

@router.get("/reelly/properties", tags=["Reelly Integration"])
async def search_reelly_properties(
    property_type: Optional[str] = Query(None, description="Property type filter"),
    budget_min: Optional[float] = Query(None, description="Minimum budget"),
    budget_max: Optional[float] = Query(None, description="Maximum budget"),
    bedrooms: Optional[int] = Query(None, description="Number of bedrooms"),
    area: Optional[str] = Query(None, description="Area/location filter"),
    developer: Optional[str] = Query(None, description="Developer filter"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page")
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

@router.get("/reelly/status", tags=["Reelly Integration"])
async def get_reelly_status():
    """
    Get the current status of the Reelly service.
    """
    if not RELLY_AVAILABLE or not reelly_service:
        return {
            "enabled": False,
            "status": "service_not_available",
            "message": "Reelly service not configured",
            "last_check": datetime.now().isoformat(),
            "api_version": None
        }
    
    try:
        status = reelly_service.get_service_status()
        return {
            **status,
            "last_check": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error checking Reelly status: {e}")
        return {
            "enabled": False,
            "status": "error",
            "message": f"Error checking service status: {str(e)}",
            "last_check": datetime.now().isoformat(),
            "api_version": None
        }
