"""
Data Router - FastAPI Router for Core Real Estate Data Endpoints

This router handles all core real estate data endpoints migrated from main.py
to maintain frontend compatibility while following the secure architecture
patterns of main_secure.py.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy import text
from datetime import datetime

# Import dependencies
from database_manager import get_db_connection

# Initialize router
router = APIRouter(prefix="/market", tags=["Market Data"])

# Root level data endpoints
root_router = APIRouter(tags=["Data"])

# Pydantic Models
class MarketOverview(BaseModel):
    """Market overview data model"""
    total_properties: int
    average_price: float
    price_change_24h: float
    volume_change_24h: float
    hot_areas: List[Dict[str, Any]]
    property_types: Dict[str, Dict[str, Any]]
    market_trends: Dict[str, Any]

class MarketTrends(BaseModel):
    """Market trends data model"""
    overall_trend: str
    price_change_percentage: float
    volume_change_percentage: float
    average_days_on_market: int
    top_performing_areas: List[Dict[str, Any]]
    property_type_performance: Dict[str, Dict[str, Any]]
    price_ranges: Dict[str, Dict[str, Any]]
    forecast: Dict[str, Any]

class Property(BaseModel):
    """Property data model"""
    address: Optional[str] = None
    price: Optional[float] = None
    bedrooms: Optional[str] = None
    bathrooms: Optional[float] = None
    square_feet: Optional[str] = None
    property_type: Optional[str] = None
    description: Optional[str] = None

class Client(BaseModel):
    """Client data model"""
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    preferred_location: Optional[str] = None
    requirements: Optional[str] = None

# Router Endpoints

@router.get("/overview")
async def get_market_overview():
    """Get market overview data"""
    try:
        # Mock market overview data
        market_data = {
            "total_properties": 1250,
            "average_price": 2850000,
            "price_change_24h": 2.5,
            "volume_change_24h": 8.3,
            "hot_areas": [
                {"name": "Dubai Marina", "price_change": 5.2, "volume": 45},
                {"name": "Palm Jumeirah", "price_change": 3.8, "volume": 32},
                {"name": "Downtown Dubai", "price_change": 4.1, "volume": 38},
                {"name": "Business Bay", "price_change": 2.9, "volume": 28}
            ],
            "property_types": {
                "apartments": {"count": 850, "avg_price": 2200000},
                "villas": {"count": 320, "avg_price": 5800000},
                "townhouses": {"count": 80, "avg_price": 3200000}
            },
            "market_trends": {
                "trend": "bullish",
                "confidence": 85,
                "prediction": "Continued growth expected"
            }
        }
        
        return market_data
    except Exception as e:
        print(f"Error in get_market_overview: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trends")
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

@root_router.get("/properties")
async def get_properties():
    """Get all properties from the database"""
    try:
        with get_db_connection() as conn:
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

@root_router.get("/clients")
async def get_clients():
    """Get all clients from the database"""
    try:
        with get_db_connection() as conn:
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
