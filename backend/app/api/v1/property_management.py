from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy import create_engine, text
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import os
from sqlalchemy.orm import Session
from app.core.middleware import get_current_user
from app.core.database import get_db
from app.core.settings import DATABASE_URL as SETTINGS_DATABASE_URL

router = APIRouter(prefix="", tags=["properties"])

# Database connection
database_url = SETTINGS_DATABASE_URL
engine = create_engine(database_url)

class PropertySearchRequest(BaseModel):
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    property_type: Optional[str] = None
    location: Optional[str] = None
    min_area_sqft: Optional[float] = None
    max_area_sqft: Optional[float] = None

class PropertyCreate(BaseModel):
    title: str
    description: str
    price: float
    location: str
    property_type: str
    bedrooms: int
    bathrooms: int
    area_sqft: Optional[float] = None

class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    location: Optional[str] = None
    property_type: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area_sqft: Optional[float] = None

class PropertyResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    location: str
    property_type: str
    bedrooms: int
    bathrooms: int
    area_sqft: Optional[float] = None

class PropertyDetailsResponse(BaseModel):
    property: PropertyResponse
    similar_properties: List[PropertyResponse]
    market_analysis: Dict[str, Any]
    neighborhood_info: Dict[str, Any]

@router.get("/", response_model=List[PropertyResponse])
async def get_all_properties():
    """Get all properties from the database"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, title, description, price, location, property_type, bedrooms, bathrooms, area_sqft FROM properties"))
            properties = []
            for row in result:
                properties.append(PropertyResponse(
                    id=row[0],
                    title=row[1],
                    description=row[2],
                    price=float(row[3]),
                    location=row[4],
                    property_type=row[5],
                    bedrooms=row[6],
                    bathrooms=row[7],
                    area_sqft=float(row[8]) if row[8] else None
                ))
            return properties
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/", response_model=PropertyResponse)
async def create_property(property_data: PropertyCreate):
    """Create a new property"""
    try:
        query = """
        INSERT INTO properties (title, description, price, location, property_type, bedrooms, bathrooms, area_sqft)
        VALUES (:title, :description, :price, :location, :property_type, :bedrooms, :bathrooms, :area_sqft)
        RETURNING id, title, description, price, location, property_type, bedrooms, bathrooms, area_sqft
        """
        
        with engine.connect() as conn:
            result = conn.execute(text(query), {
                "title": property_data.title,
                "description": property_data.description,
                "price": property_data.price,
                "location": property_data.location,
                "property_type": property_data.property_type,
                "bedrooms": property_data.bedrooms,
                "bathrooms": property_data.bathrooms,
                "area_sqft": property_data.area_sqft
            })
            conn.commit()
            
            row = result.fetchone()
            if row:
                return PropertyResponse(
                    id=row[0],
                    title=row[1],
                    description=row[2],
                    price=float(row[3]),
                    location=row[4],
                    property_type=row[5],
                    bedrooms=row[6],
                    bathrooms=row[7],
                    area_sqft=float(row[8]) if row[8] else None
                )
            else:
                raise HTTPException(status_code=500, detail="Failed to create property")
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/search", response_model=List[PropertyResponse])
async def search_properties(
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    bedrooms: Optional[int] = Query(None, description="Number of bedrooms"),
    bathrooms: Optional[int] = Query(None, description="Number of bathrooms"),
    property_type: Optional[str] = Query(None, description="Property type"),
    location: Optional[str] = Query(None, description="Location/area"),
    min_area_sqft: Optional[float] = Query(None, description="Minimum area in sqft"),
    max_area_sqft: Optional[float] = Query(None, description="Maximum area in sqft"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Number of results to return")
):
    """Advanced property search with multiple filters and pagination"""
    
    try:
        with engine.connect() as conn:
            # Calculate offset for pagination
            offset = (page - 1) * limit
            
            # Build dynamic SQL query with pagination
            query = """
                SELECT id, title, description, price, location, property_type, 
                       bedrooms, bathrooms, area_sqft
                FROM properties WHERE 1=1
            """
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
                query += " AND location ILIKE :location"
                params["location"] = f"%{location}%"
            
            if min_area_sqft is not None:
                query += " AND area_sqft >= :min_area_sqft"
                params["min_area_sqft"] = min_area_sqft
            
            if max_area_sqft is not None:
                query += " AND area_sqft <= :max_area_sqft"
                params["max_area_sqft"] = max_area_sqft
            
            # Add pagination
            query += " ORDER BY id DESC LIMIT :limit OFFSET :offset"
            params["limit"] = limit
            params["offset"] = offset
            
            result = conn.execute(text(query), params)
            properties = []
            
            for row in result:
                properties.append(PropertyResponse(
                    id=row[0],
                    title=row[1],
                    description=row[2],
                    price=float(row[3]) if row[3] else 0.0,
                    location=row[4] if row[4] else "",
                    property_type=row[5] if row[5] else "Unknown",
                    bedrooms=row[6] if row[6] else 0,
                    bathrooms=row[7] if row[7] else 0,
                    area_sqft=float(row[8]) if row[8] else None
                ))
            
            # Get total count for pagination
            count_query = "SELECT COUNT(*) FROM properties WHERE 1=1"
            count_params = {}
            
            # Add same filters to count query
            if min_price is not None:
                count_query += " AND price >= :min_price"
                count_params["min_price"] = min_price
            if max_price is not None:
                count_query += " AND price <= :max_price"
                count_params["max_price"] = max_price
            if bedrooms is not None:
                count_query += " AND bedrooms = :bedrooms"
                count_params["bedrooms"] = bedrooms
            if bathrooms is not None:
                count_query += " AND bathrooms = :bathrooms"
                count_params["bathrooms"] = bathrooms
            if property_type:
                count_query += " AND property_type ILIKE :property_type"
                count_params["property_type"] = f"%{property_type}%"
            if location:
                count_query += " AND location ILIKE :location"
                count_params["location"] = f"%{location}%"
            if min_area_sqft is not None:
                count_query += " AND area_sqft >= :min_area_sqft"
                count_params["min_area_sqft"] = min_area_sqft
            if max_area_sqft is not None:
                count_query += " AND area_sqft <= :max_area_sqft"
                count_params["max_area_sqft"] = max_area_sqft
            
            count_result = conn.execute(text(count_query), count_params)
            total_count = count_result.fetchone()[0]
            
            return {
                "properties": properties,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total_count,
                    "pages": (total_count + limit - 1) // limit
                }
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/{property_id}", response_model=PropertyDetailsResponse)
async def get_property_details(property_id: int):
    """Get detailed information about a specific property"""
    try:
        # Get property details
        property_query = "SELECT * FROM properties WHERE id = :property_id"
        
        with engine.connect() as conn:
            result = conn.execute(text(property_query), {"property_id": property_id})
            property_row = result.fetchone()
            
            if not property_row:
                raise HTTPException(status_code=404, detail="Property not found")
            
            property_data = PropertyResponse(
                id=property_row[0],
                title=property_row[1],
                description=property_row[2],
                price=float(property_row[3]) if property_row[3] else 0.0,
                location=property_row[4] if property_row[4] else "",
                property_type=property_row[5] if property_row[5] else "Unknown",
                bedrooms=property_row[6] if property_row[6] else 0,
                bathrooms=property_row[7] if property_row[7] else 0,
                area_sqft=float(property_row[8]) if property_row[8] else None
            )
            
            # Get similar properties (same type, similar price range)
            similar_query = """
            SELECT * FROM properties 
            WHERE property_type = :property_type 
            AND id != :property_id
            AND price BETWEEN :min_price AND :max_price
            LIMIT 5
            """
            
            price_range = property_data.price * 0.2  # 20% range
            similar_result = conn.execute(text(similar_query), {
                "property_type": property_data.property_type,
                "property_id": property_id,
                "min_price": property_data.price - price_range,
                "max_price": property_data.price + price_range
            })
            
            similar_properties = []
            for row in similar_result:
                similar_properties.append(PropertyResponse(
                    id=row[0],
                    title=row[1],
                    description=row[2],
                    price=float(row[3]) if row[3] else 0.0,
                    location=row[4] if row[4] else "",
                    property_type=row[5] if row[5] else "Unknown",
                    bedrooms=row[6] if row[6] else 0,
                    bathrooms=row[7] if row[7] else 0,
                    area_sqft=float(row[8]) if row[8] else None
                ))
            
            # Mock market analysis and neighborhood info
            market_analysis = {
                "average_price": property_data.price * 1.1,
                "price_trend": "increasing",
                "days_on_market": 15,
                "price_per_sqft": property_data.price / (property_data.area_sqft or 1000)
            }
            
            neighborhood_info = {
                "schools": ["Dubai International School", "American School of Dubai"],
                "amenities": ["Shopping Mall", "Park", "Hospital"],
                "transportation": ["Metro Station", "Bus Stop"],
                "crime_rate": "Low"
            }
            
            return PropertyDetailsResponse(
                property=property_data,
                similar_properties=similar_properties,
                market_analysis=market_analysis,
                neighborhood_info=neighborhood_info
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/{property_id}", response_model=PropertyResponse)
async def update_property(property_id: int, property_data: PropertyUpdate):
    """Update an existing property"""
    try:
        # Check if property exists
        check_query = "SELECT id FROM properties WHERE id = :property_id"
        
        with engine.connect() as conn:
            result = conn.execute(text(check_query), {"property_id": property_id})
            if not result.fetchone():
                raise HTTPException(status_code=404, detail="Property not found")
            
            # Build dynamic update query
            update_fields = []
            params = {"property_id": property_id}
            
            if property_data.title is not None:
                update_fields.append("title = :title")
                params["title"] = property_data.title
            
            if property_data.description is not None:
                update_fields.append("description = :description")
                params["description"] = property_data.description
            
            if property_data.price is not None:
                update_fields.append("price = :price")
                params["price"] = property_data.price
            
            if property_data.location is not None:
                update_fields.append("location = :location")
                params["location"] = property_data.location
            
            if property_data.property_type is not None:
                update_fields.append("property_type = :property_type")
                params["property_type"] = property_data.property_type
            
            if property_data.bedrooms is not None:
                update_fields.append("bedrooms = :bedrooms")
                params["bedrooms"] = property_data.bedrooms
            
            if property_data.bathrooms is not None:
                update_fields.append("bathrooms = :bathrooms")
                params["bathrooms"] = property_data.bathrooms
            
            if property_data.area_sqft is not None:
                update_fields.append("area_sqft = :area_sqft")
                params["area_sqft"] = property_data.area_sqft
            
            if not update_fields:
                raise HTTPException(status_code=400, detail="No fields to update")
            
            update_query = f"""
            UPDATE properties 
            SET {', '.join(update_fields)}
            WHERE id = :property_id
            RETURNING id, title, description, price, location, property_type, bedrooms, bathrooms, area_sqft
            """
            
            result = conn.execute(text(update_query), params)
            conn.commit()
            
            row = result.fetchone()
            if row:
                return PropertyResponse(
                    id=row[0],
                    title=row[1],
                    description=row[2],
                    price=float(row[3]),
                    location=row[4],
                    property_type=row[5],
                    bedrooms=row[6],
                    bathrooms=row[7],
                    area_sqft=float(row[8]) if row[8] else None
                )
            else:
                raise HTTPException(status_code=500, detail="Failed to update property")
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.delete("/{property_id}")
async def delete_property(property_id: int):
    """Delete a property"""
    try:
        with engine.connect() as conn:
            # Check if property exists
            check_query = "SELECT id FROM properties WHERE id = :property_id"
            result = conn.execute(text(check_query), {"property_id": property_id})
            
            if not result.fetchone():
                raise HTTPException(status_code=404, detail="Property not found")
            
            # Delete property
            delete_query = "DELETE FROM properties WHERE id = :property_id"
            conn.execute(text(delete_query), {"property_id": property_id})
            conn.commit()
            
            return {"message": "Property deleted successfully"}
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/types/list")
async def get_property_types():
    """Get list of available property types"""
    try:
        query = "SELECT DISTINCT property_type FROM properties WHERE property_type IS NOT NULL"
        
        with engine.connect() as conn:
            result = conn.execute(text(query))
            types = [row[0] for row in result if row[0]]
            
            return {"property_types": types}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/locations/list")
async def get_property_locations():
    """Get list of available property locations"""
    try:
        query = "SELECT DISTINCT location FROM properties WHERE location IS NOT NULL"
        
        with engine.connect() as conn:
            result = conn.execute(text(query))
            locations = [row[0] for row in result if row[0]]
            
            return {"locations": locations}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# --- Phase 1: Granular Data & Security Foundation ---

@router.put("/{property_id}/status", tags=["Properties"])
async def update_property_status(
    property_id: int,
    new_status: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update property listing status with access control"""
    # Check for valid status
    valid_statuses = ['draft', 'live', 'pocket', 'sold', 'archived']
    if new_status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status provided.")

    try:
        with engine.connect() as conn:
            # Find the property and verify ownership
            property_query = """
                SELECT id, listing_status, agent_id 
                FROM properties 
                WHERE id = :property_id
            """
            result = conn.execute(text(property_query), {"property_id": property_id})
            property_to_update = result.fetchone()
            
            if not property_to_update:
                raise HTTPException(status_code=404, detail="Property not found.")

            # Ensure the current user is the agent assigned to this property or an admin
            if property_to_update.agent_id != current_user.id and current_user.role != 'admin':
                raise HTTPException(status_code=403, detail="Not authorized to update this property.")

            # Log the change in listing_history
            history_query = """
                INSERT INTO listing_history (
                    property_id, event_type, old_value, new_value, changed_by_agent_id
                ) VALUES (
                    :property_id, 'status_change', :old_value, :new_value, :changed_by_agent_id
                )
            """
            conn.execute(text(history_query), {
                "property_id": property_id,
                "old_value": property_to_update.listing_status,
                "new_value": new_status,
                "changed_by_agent_id": current_user.id
            })

            # Update the status
            update_query = """
                UPDATE properties 
                SET listing_status = :new_status 
                WHERE id = :property_id
            """
            conn.execute(text(update_query), {
                "property_id": property_id,
                "new_status": new_status
            })
            
            conn.commit()

            return {"message": f"Property {property_id} status updated to {new_status}."}
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/{property_id}/confidential", tags=["Properties"])
async def get_confidential_property_data(
    property_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get confidential property data with access control"""
    try:
        with engine.connect() as conn:
            # Get the property to check ownership
            property_query = """
                SELECT id, agent_id 
                FROM properties 
                WHERE id = :property_id
            """
            result = conn.execute(text(property_query), {"property_id": property_id})
            property_record = result.fetchone()
            
            if not property_record:
                raise HTTPException(status_code=404, detail="Property not found.")

            # Access Control Algorithm: User must be an admin/manager or the assigned agent
            is_authorized = (
                current_user.role in ['admin', 'manager'] or
                property_record.agent_id == current_user.id
            )

            if not is_authorized:
                raise HTTPException(status_code=403, detail="You do not have permission to view these details.")

            # Fetch the confidential data
            confidential_query = """
                SELECT unit_number, plot_number, floor, owner_details, created_at
                FROM property_confidential 
                WHERE property_id = :property_id
            """
            result = conn.execute(text(confidential_query), {"property_id": property_id})
            confidential_data = result.fetchone()
            
            if not confidential_data:
                raise HTTPException(status_code=404, detail="Confidential data not found for this property.")

            return {
                "unit_number": confidential_data.unit_number,
                "plot_number": confidential_data.plot_number,
                "floor": confidential_data.floor,
                "owner_details": confidential_data.owner_details,
                "created_at": confidential_data.created_at
            }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
