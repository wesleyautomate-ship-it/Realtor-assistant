from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import create_engine, text
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/properties", tags=["properties"])

# Database connection
database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/real_estate')
engine = create_engine(database_url)

class PropertySearchRequest(BaseModel):
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    property_type: Optional[str] = None
    location: Optional[str] = None
    min_square_feet: Optional[float] = None
    max_square_feet: Optional[float] = None

class PropertyResponse(BaseModel):
    address: str
    price: float
    bedrooms: int
    bathrooms: float
    square_feet: Optional[float]
    property_type: str
    description: str
    id: Optional[int] = None

class PropertyDetailsResponse(BaseModel):
    property: PropertyResponse
    similar_properties: List[PropertyResponse]
    market_analysis: Dict[str, Any]
    neighborhood_info: Dict[str, Any]

@router.get("/search", response_model=List[PropertyResponse])
async def search_properties(
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    bedrooms: Optional[int] = Query(None, description="Number of bedrooms"),
    bathrooms: Optional[float] = Query(None, description="Number of bathrooms"),
    property_type: Optional[str] = Query(None, description="Property type"),
    location: Optional[str] = Query(None, description="Location/area"),
    min_square_feet: Optional[float] = Query(None, description="Minimum square feet"),
    max_square_feet: Optional[float] = Query(None, description="Maximum square feet"),
    limit: int = Query(20, description="Number of results to return")
):
    """Advanced property search with multiple filters"""
    
    # Build dynamic SQL query
    query = "SELECT * FROM properties WHERE 1=1"
    params = {}
    
    if min_price is not None:
        query += " AND price >= :min_price"
        params["min_price"] = min_price
    
    if max_price is not None:
        query += " AND price <= :max_price"
        params["max_price"] = max_price
    
    if bedrooms is not None:
        query += " AND bedrooms = :bedrooms"
        params["bedrooms"] = bedrooms
    
    if bathrooms is not None:
        query += " AND bathrooms = :bathrooms"
        params["bathrooms"] = bathrooms
    
    if property_type:
        query += " AND property_type ILIKE :property_type"
        params["property_type"] = f"%{property_type}%"
    
    if location:
        query += " AND address ILIKE :location"
        params["location"] = f"%{location}%"
    
    if min_square_feet is not None:
        query += " AND square_feet >= :min_square_feet"
        params["min_square_feet"] = min_square_feet
    
    if max_square_feet is not None:
        query += " AND square_feet <= :max_square_feet"
        params["max_square_feet"] = max_square_feet
    
    query += f" LIMIT {limit}"
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), params)
            properties = []
            
            for row in result:
                row_data = list(row)
                if len(row_data) >= 7:
                    properties.append(PropertyResponse(
                        address=row_data[0],
                        price=float(row_data[1]) if row_data[1] else 0,
                        bedrooms=row_data[2],
                        bathrooms=float(row_data[3]) if row_data[3] else 0,
                        square_feet=float(row_data[4]) if row_data[4] else None,
                        property_type=row_data[5],
                        description=row_data[6]
                    ))
            
            return properties
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/{property_id}", response_model=PropertyDetailsResponse)
async def get_property_details(property_id: int):
    """Get detailed property information with similar properties and market analysis"""
    
    try:
        with engine.connect() as conn:
            # Get property details
            result = conn.execute(text("SELECT * FROM properties LIMIT 1 OFFSET :offset"), {"offset": property_id - 1})
            property_data = result.fetchone()
            
            if not property_data:
                raise HTTPException(status_code=404, detail="Property not found")
            
            row_data = list(property_data)
            property_obj = PropertyResponse(
                address=row_data[0],
                price=float(row_data[1]) if row_data[1] else 0,
                bedrooms=row_data[2],
                bathrooms=float(row_data[3]) if row_data[3] else 0,
                square_feet=float(row_data[4]) if row_data[4] else None,
                property_type=row_data[5],
                description=row_data[6],
                id=property_id
            )
            
            # Get similar properties (same type, similar price range)
            similar_query = """
                SELECT * FROM properties 
                WHERE property_type = :property_type 
                AND price BETWEEN :min_price AND :max_price
                AND address != :current_address
                LIMIT 5
            """
            
            price_range = property_obj.price * 0.2  # 20% range
            similar_result = conn.execute(text(similar_query), {
                "property_type": property_obj.property_type,
                "min_price": property_obj.price - price_range,
                "max_price": property_obj.price + price_range,
                "current_address": property_obj.address
            })
            
            similar_properties = []
            for row in similar_result:
                row_data = list(row)
                if len(row_data) >= 7:
                    similar_properties.append(PropertyResponse(
                        address=row_data[0],
                        price=float(row_data[1]) if row_data[1] else 0,
                        bedrooms=row_data[2],
                        bathrooms=float(row_data[3]) if row_data[3] else 0,
                        square_feet=float(row_data[4]) if row_data[4] else None,
                        property_type=row_data[5],
                        description=row_data[6]
                    ))
            
            # Mock market analysis (in real app, this would come from market data)
            market_analysis = {
                "price_per_sqft": property_obj.price / (property_obj.square_feet or 1000),
                "market_trend": "Stable",
                "days_on_market": 45,
                "price_comparison": "Above average for area",
                "investment_potential": "High"
            }
            
            # Mock neighborhood info (in real app, this would come from neighborhood data)
            neighborhood_info = {
                "name": "Downtown",
                "average_price": property_obj.price * 0.9,
                "schools": ["Downtown Elementary", "Central High"],
                "amenities": ["Shopping Mall", "Restaurants", "Public Transport"],
                "crime_rate": "Low",
                "walkability_score": 85
            }
            
            return PropertyDetailsResponse(
                property=property_obj,
                similar_properties=similar_properties,
                market_analysis=market_analysis,
                neighborhood_info=neighborhood_info
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/types/list")
async def get_property_types():
    """Get list of available property types"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT DISTINCT property_type FROM properties"))
            types = [row[0] for row in result if row[0]]
            return {"property_types": types}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/locations/list")
async def get_locations():
    """Get list of available locations/areas"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT DISTINCT address FROM properties"))
            locations = [row[0] for row in result if row[0]]
            return {"locations": locations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
