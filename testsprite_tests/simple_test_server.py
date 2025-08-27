#!/usr/bin/env python3
"""
Simple test server for TestSprite testing
Mimics the main RAG web app API endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import json
import time
from datetime import datetime

# Create FastAPI app
app = FastAPI(title="RAG Web App Test Server", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    intent: str
    confidence: float
    context_used: List[Dict[str, Any]]
    suggestions: List[str]
    timestamp: str

class PropertyRequest(BaseModel):
    title: str
    description: str
    location: str
    property_type: str
    price: float
    bedrooms: int
    bathrooms: int
    area: float

# Mock data
mock_properties = [
    {
        "id": 1,
        "title": "Luxury Apartment in Dubai Marina",
        "description": "Beautiful 2-bedroom apartment with marina view",
        "location": "Dubai Marina",
        "property_type": "apartment",
        "price": 2500000,
        "bedrooms": 2,
        "bathrooms": 2,
        "area": 1200
    },
    {
        "id": 2,
        "title": "Villa in Palm Jumeirah",
        "description": "Exclusive villa with private beach access",
        "location": "Palm Jumeirah",
        "property_type": "villa",
        "price": 8500000,
        "bedrooms": 4,
        "bathrooms": 5,
        "area": 3500
    }
]

mock_clients = [
    {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+971501234567",
        "budget_min": 2000000,
        "budget_max": 5000000,
        "preferred_location": "Dubai Marina"
    }
]

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "services": {
            "database": "connected",
            "chromadb": "connected",
            "gemini": "connected"
        }
    }

# Status endpoint
@app.get("/status")
async def system_status():
    return {
        "uptime": "1 day, 2 hours, 30 minutes",
        "memory_usage": "45%",
        "cpu_usage": "23%",
        "active_connections": 15,
        "total_queries": 1250
    }

# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Mock AI response based on message content
    message_lower = request.message.lower()
    
    if "dubai marina" in message_lower:
        response = "Dubai Marina is one of the most prestigious areas in Dubai, known for its luxury apartments and waterfront lifestyle. Average property prices range from 2M to 8M AED depending on size and view."
        intent = "AREA_INFO"
        confidence = 0.95
    elif "investment" in message_lower:
        response = "Dubai real estate offers excellent investment opportunities with rental yields averaging 6-8%. Popular investment areas include Dubai Marina, Downtown Dubai, and Palm Jumeirah."
        intent = "INVESTMENT_ADVICE"
        confidence = 0.92
    elif "price" in message_lower:
        response = "Current market prices in Dubai vary by area. Dubai Marina apartments start from 2M AED, while villas in Palm Jumeirah can range from 8M to 20M AED."
        intent = "PRICE_INFO"
        confidence = 0.88
    else:
        response = "I can help you with information about Dubai real estate, property prices, investment opportunities, and market trends. What specific information are you looking for?"
        intent = "GENERAL_INQUIRY"
        confidence = 0.75
    
    return ChatResponse(
        response=response,
        intent=intent,
        confidence=confidence,
        context_used=[{"source": "market_data", "relevance": 0.9, "content": "Dubai real estate market analysis"}],
        suggestions=["View properties", "Get market report", "Contact agent"],
        timestamp=datetime.now().isoformat()
    )

# Properties endpoints
@app.get("/properties")
async def get_properties(
    page: int = 1,
    limit: int = 20,
    location: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    property_type: Optional[str] = None
):
    filtered_properties = mock_properties.copy()
    
    if location:
        filtered_properties = [p for p in filtered_properties if location.lower() in p["location"].lower()]
    if min_price:
        filtered_properties = [p for p in filtered_properties if p["price"] >= min_price]
    if max_price:
        filtered_properties = [p for p in filtered_properties if p["price"] <= max_price]
    if property_type:
        filtered_properties = [p for p in filtered_properties if p["property_type"] == property_type]
    
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_properties = filtered_properties[start_idx:end_idx]
    
    return {
        "properties": paginated_properties,
        "total": len(filtered_properties),
        "page": page,
        "limit": limit
    }

@app.get("/properties/{property_id}")
async def get_property(property_id: int):
    for prop in mock_properties:
        if prop["id"] == property_id:
            return prop
    raise HTTPException(status_code=404, detail="Property not found")

@app.post("/properties")
async def create_property(property_data: PropertyRequest):
    new_property = {
        "id": len(mock_properties) + 1,
        **property_data.dict()
    }
    mock_properties.append(new_property)
    return new_property

# Clients endpoints
@app.get("/clients")
async def get_clients(
    page: int = 1,
    limit: int = 20,
    search: Optional[str] = None,
    status: Optional[str] = None
):
    filtered_clients = mock_clients.copy()
    
    if search:
        filtered_clients = [c for c in filtered_clients if search.lower() in c["name"].lower() or search.lower() in c["email"].lower()]
    
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_clients = filtered_clients[start_idx:end_idx]
    
    return {
        "clients": paginated_clients,
        "total": len(filtered_clients),
        "page": page,
        "limit": limit
    }

# Market data endpoints
@app.get("/market/overview")
async def get_market_overview():
    return {
        "total_properties": 15000,
        "average_price": 2800000,
        "price_trend": 12.5,
        "rental_yield": 6.8,
        "top_areas": [
            {
                "area": "Dubai Marina",
                "properties": 2500,
                "avg_price": 3200000,
                "growth": 15.2
            }
        ],
        "market_sentiment": "bullish",
        "last_updated": datetime.now().isoformat()
    }

@app.get("/market/areas/{area_name}")
async def get_area_analysis(area_name: str):
    return {
        "area": area_name,
        "total_properties": 1200,
        "average_price": 3500000,
        "price_trend": 8.5,
        "rental_yield": 7.2,
        "popular_property_types": ["apartment", "penthouse"],
        "amenities": ["beach", "marina", "shopping", "restaurants"]
    }

# Analytics endpoints
@app.get("/analytics/usage")
async def get_usage_analytics(
    period: str = "month",
    user_id: Optional[str] = None
):
    return {
        "total_queries": 1250,
        "unique_users": 89,
        "avg_response_time": 1.8,
        "popular_intents": [
            {
                "intent": "MARKET_INFO",
                "count": 450,
                "percentage": 36
            }
        ],
        "top_queries": [
            "Dubai Marina investment opportunities",
            "Property prices in Palm Jumeirah"
        ],
        "period": "2024-08-01 to 2024-08-15"
    }

@app.get("/analytics/performance")
async def get_performance_metrics():
    return {
        "avg_response_time": 1.8,
        "p95_response_time": 3.2,
        "error_rate": 0.02,
        "uptime": 99.8,
        "active_connections": 15
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
