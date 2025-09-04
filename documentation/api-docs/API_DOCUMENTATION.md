# Dubai Real Estate RAG Chat System - API Documentation

## 📖 **Table of Contents**
1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Base URL](#base-url)
4. [Endpoints](#endpoints)
5. [Data Models](#data-models)
6. [Error Handling](#error-handling)
7. [Rate Limiting](#rate-limiting)
8. [Examples](#examples)
9. [OpenAPI Specification](#openapi-specification)

---

## 🌐 **Overview**

The Dubai Real Estate RAG Chat System API provides a comprehensive interface for real estate queries, property management, and AI-powered chat interactions. The API is built with FastAPI and supports both REST and WebSocket connections.

### **Key Features**
- **RAG-Powered Chat**: AI responses with context from Dubai real estate data
- **Property Management**: CRUD operations for properties and clients
- **Multi-Intent Support**: Handles complex queries with multiple intents
- **Real-time Processing**: WebSocket support for live chat
- **Comprehensive Search**: Hybrid search across structured and unstructured data

### **API Version**
- **Current Version**: 1.2.0
- **Base URL**: `https://your-domain.com/api`
- **Documentation**: Available at `/docs` (Swagger UI)

---

## 🔐 **Authentication**

### **API Key Authentication**
```http
Authorization: Bearer YOUR_API_KEY
```

### **Session Authentication**
```http
Cookie: session=YOUR_SESSION_TOKEN
```

### **Getting API Key**
1. Register at `/api/auth/register`
2. Login at `/api/auth/login`
3. Generate API key at `/api/auth/generate-key`

---

## 🌍 **Base URL**

### **Development**
```
http://localhost:8001/api
```

### **Production**
```
https://your-domain.com/api
```

### **WebSocket**
```
ws://localhost:8001/ws (Development)
wss://your-domain.com/ws (Production)
```

---

## 📡 **Endpoints**

### **1. Health & Status**

#### **Health Check**
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-08-15T10:30:00Z",
  "version": "1.2.0",
  "services": {
    "database": "connected",
    "chromadb": "connected",
    "gemini": "connected"
  }
}
```

#### **System Status**
```http
GET /status
```

**Response:**
```json
{
  "uptime": "5 days, 12 hours, 30 minutes",
  "memory_usage": "45%",
  "cpu_usage": "23%",
  "active_connections": 15,
  "total_queries": 1250
}
```

### **2. Chat Endpoints**

#### **Send Message**
```http
POST /chat
```

**Request Body:**
```json
{
  "message": "What are the best investment opportunities in Dubai Marina?",
  "user_id": "user123",
  "session_id": "session456",
  "context": {
    "budget": "2M-5M AED",
    "property_type": "apartment",
    "investment_horizon": "5-10 years"
  }
}
```

**Response:**
```json
{
  "response": "Based on current market analysis, Dubai Marina offers excellent investment opportunities...",
  "intent": "INVESTMENT_STRATEGY",
  "confidence": 0.92,
  "context_used": [
    {
      "source": "market_data",
      "relevance": 0.95,
      "content": "Dubai Marina market analysis..."
    }
  ],
  "suggestions": [
    "Compare with other areas",
    "View recent transactions",
    "Get detailed market report"
  ],
  "timestamp": "2024-08-15T10:30:00Z"
}
```

#### **Stream Chat (WebSocket)**
```javascript
// WebSocket connection
const ws = new WebSocket('wss://your-domain.com/ws');

ws.onopen = function() {
  ws.send(JSON.stringify({
    type: 'message',
    data: {
      message: "Tell me about Dubai Marina properties",
      user_id: "user123"
    }
  }));
};

ws.onmessage = function(event) {
  const response = JSON.parse(event.data);
  console.log(response);
};
```

### **3. Property Management**

#### **List Properties**
```http
GET /properties
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20)
- `location`: Filter by location
- `property_type`: Filter by property type
- `min_price`: Minimum price
- `max_price`: Maximum price
- `bedrooms`: Number of bedrooms
- `sort_by`: Sort field (price, date, location)
- `sort_order`: Sort order (asc, desc)

**Response:**
```json
{
  "properties": [
    {
      "id": 1,
      "title": "Luxury 3BR Apartment in Dubai Marina",
      "description": "Stunning waterfront apartment...",
      "location": "Dubai Marina",
      "property_type": "apartment",
      "price": 2500000,
      "bedrooms": 3,
      "bathrooms": 2,
      "area": 1800,
      "developer": "Emaar Properties",
      "completion_date": "2024-12-01",
      "amenities": ["pool", "gym", "parking"],
      "images": ["url1", "url2"],
      "created_at": "2024-08-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  }
}
```

#### **Get Property Details**
```http
GET /properties/{property_id}
```

**Response:**
```json
{
  "id": 1,
  "title": "Luxury 3BR Apartment in Dubai Marina",
  "description": "Stunning waterfront apartment...",
  "location": "Dubai Marina",
  "property_type": "apartment",
  "price": 2500000,
  "bedrooms": 3,
  "bathrooms": 2,
  "area": 1800,
  "developer": "Emaar Properties",
  "completion_date": "2024-12-01",
  "amenities": ["pool", "gym", "parking"],
  "images": ["url1", "url2"],
  "market_data": {
    "price_per_sqft": 1389,
    "rental_yield": 6.5,
    "price_change_1y": 12.5
  },
  "neighborhood_info": {
    "schools": 5,
    "hospitals": 2,
    "shopping_centers": 3,
    "metro_stations": 2
  },
  "created_at": "2024-08-15T10:30:00Z",
  "updated_at": "2024-08-15T10:30:00Z"
}
```

#### **Create Property**
```http
POST /properties
```

**Request Body:**
```json
{
  "title": "New Property Listing",
  "description": "Property description...",
  "location": "Dubai Marina",
  "property_type": "apartment",
  "price": 2500000,
  "bedrooms": 3,
  "bathrooms": 2,
  "area": 1800,
  "developer": "Emaar Properties",
  "completion_date": "2024-12-01",
  "amenities": ["pool", "gym", "parking"],
  "images": ["url1", "url2"]
}
```

#### **Update Property**
```http
PUT /properties/{property_id}
```

#### **Delete Property**
```http
DELETE /properties/{property_id}
```

### **4. Client Management**

#### **List Clients**
```http
GET /clients
```

**Query Parameters:**
- `page`: Page number
- `limit`: Items per page
- `search`: Search by name or email
- `status`: Filter by status (active, inactive)

#### **Get Client Details**
```http
GET /clients/{client_id}
```

#### **Create Client**
```http
POST /clients
```

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+971501234567",
  "preferences": {
    "budget_range": "2M-5M AED",
    "property_types": ["apartment", "villa"],
    "locations": ["Dubai Marina", "Palm Jumeirah"],
    "investment_horizon": "5-10 years"
  }
}
```

#### **Update Client**
```http
PUT /clients/{client_id}
```

#### **Delete Client**
```http
DELETE /clients/{client_id}
```

### **5. Market Data**

#### **Get Market Overview**
```http
GET /market/overview
```

**Response:**
```json
{
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
  "last_updated": "2024-08-15T10:30:00Z"
}
```

#### **Get Area Analysis**
```http
GET /market/areas/{area_name}
```

#### **Get Price Trends**
```http
GET /market/trends
```

**Query Parameters:**
- `area`: Specific area
- `property_type`: Property type
- `period`: Time period (1m, 3m, 6m, 1y)

### **6. Data Ingestion**

#### **Upload Document**
```http
POST /ingest/upload
```

**Request Body (multipart/form-data):**
- `file`: Document file (PDF, CSV, Excel)
- `category`: Document category
- `metadata`: Additional metadata (JSON)

**Response:**
```json
{
  "file_id": "file123",
  "filename": "market_report.pdf",
  "category": "market_data",
  "status": "processing",
  "pages": 25,
  "extracted_text": "Market analysis shows...",
  "processed_at": "2024-08-15T10:30:00Z"
}
```

#### **Get Ingestion Status**
```http
GET /ingest/status/{file_id}
```

#### **List Ingested Documents**
```http
GET /ingest/documents
```

### **7. Analytics**

#### **Get Usage Analytics**
```http
GET /analytics/usage
```

**Query Parameters:**
- `period`: Time period (day, week, month, year)
- `user_id`: Specific user

**Response:**
```json
{
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
```

#### **Get Performance Metrics**
```http
GET /analytics/performance
```

---

## 📊 **Data Models**

### **Property Model**
```json
{
  "id": "integer",
  "title": "string",
  "description": "string",
  "location": "string",
  "property_type": "string",
  "price": "number",
  "bedrooms": "integer",
  "bathrooms": "integer",
  "area": "number",
  "developer": "string",
  "completion_date": "date",
  "amenities": ["string"],
  "images": ["string"],
  "market_data": {
    "price_per_sqft": "number",
    "rental_yield": "number",
    "price_change_1y": "number"
  },
  "neighborhood_info": {
    "schools": "integer",
    "hospitals": "integer",
    "shopping_centers": "integer",
    "metro_stations": "integer"
  },
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### **Client Model**
```json
{
  "id": "integer",
  "name": "string",
  "email": "string",
  "phone": "string",
  "preferences": {
    "budget_range": "string",
    "property_types": ["string"],
    "locations": ["string"],
    "investment_horizon": "string"
  },
  "status": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### **Chat Message Model**
```json
{
  "id": "integer",
  "user_id": "string",
  "session_id": "string",
  "message": "string",
  "response": "string",
  "intent": "string",
  "confidence": "number",
  "context_used": [
    {
      "source": "string",
      "relevance": "number",
      "content": "string"
    }
  ],
  "timestamp": "datetime"
}
```

### **Market Data Model**
```json
{
  "id": "integer",
  "area": "string",
  "property_type": "string",
  "avg_price": "number",
  "price_change": "number",
  "rental_yield": "number",
  "transaction_volume": "number",
  "market_sentiment": "string",
  "date": "date"
}
```

---

## ⚠️ **Error Handling**

### **Standard Error Response**
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional error details",
    "timestamp": "2024-08-15T10:30:00Z"
  }
}
```

### **Common Error Codes**

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Request validation failed |
| `UNAUTHORIZED` | 401 | Authentication required |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Internal server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |

### **Validation Error Example**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": {
      "field": "price",
      "issue": "Price must be a positive number"
    },
    "timestamp": "2024-08-15T10:30:00Z"
  }
}
```

---

## 🚦 **Rate Limiting**

### **Rate Limits**
- **Standard Users**: 100 requests per hour
- **Premium Users**: 1000 requests per hour
- **API Keys**: 5000 requests per hour

### **Rate Limit Headers**
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

### **Rate Limit Exceeded Response**
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Try again in 3600 seconds.",
    "retry_after": 3600,
    "timestamp": "2024-08-15T10:30:00Z"
  }
}
```

---

## 💡 **Examples**

### **Complete Chat Flow**
```bash
# 1. Send initial message
curl -X POST "https://your-domain.com/api/chat" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the best investment opportunities in Dubai Marina?",
    "user_id": "user123",
    "session_id": "session456"
  }'

# 2. Follow-up with context
curl -X POST "https://your-domain.com/api/chat" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What about the rental yield?",
    "user_id": "user123",
    "session_id": "session456",
    "context": {
      "previous_query": "Dubai Marina investment",
      "budget": "2M-5M AED"
    }
  }'
```

### **Property Search**
```bash
# Search for properties in Dubai Marina
curl -X GET "https://your-domain.com/api/properties?location=Dubai%20Marina&min_price=2000000&max_price=5000000&property_type=apartment&sort_by=price&sort_order=asc" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### **Market Analysis**
```bash
# Get market overview
curl -X GET "https://your-domain.com/api/market/overview" \
  -H "Authorization: Bearer YOUR_API_KEY"

# Get area-specific analysis
curl -X GET "https://your-domain.com/api/market/areas/Dubai%20Marina" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### **Data Ingestion**
```bash
# Upload market report
curl -X POST "https://your-domain.com/api/ingest/upload" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@market_report.pdf" \
  -F "category=market_data" \
  -F "metadata={\"source\":\"RERA\",\"date\":\"2024-08-15\"}"
```

---

## 📋 **OpenAPI Specification**

### **Swagger UI**
Access the interactive API documentation at:
```
https://your-domain.com/docs
```

### **OpenAPI JSON**
```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Dubai Real Estate RAG Chat System API",
    "description": "Comprehensive API for Dubai real estate queries and property management",
    "version": "1.2.0",
    "contact": {
      "name": "API Support",
      "email": "api@dubairealestate.com"
    }
  },
  "servers": [
    {
      "url": "https://your-domain.com/api",
      "description": "Production server"
    },
    {
      "url": "http://localhost:8001/api",
      "description": "Development server"
    }
  ],
  "paths": {
    "/health": {
      "get": {
        "summary": "Health Check",
        "description": "Check API health status",
        "responses": {
          "200": {
            "description": "API is healthy",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HealthResponse"
                }
              }
            }
          }
        }
      }
    },
    "/chat": {
      "post": {
        "summary": "Send Chat Message",
        "description": "Send a message and get AI-powered response",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/ChatRequest"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Chat response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ChatResponse"
                }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "HealthResponse": {
        "type": "object",
        "properties": {
          "status": {
            "type": "string",
            "example": "healthy"
          },
          "timestamp": {
            "type": "string",
            "format": "date-time"
          },
          "version": {
            "type": "string",
            "example": "1.2.0"
          }
        }
      },
      "ChatRequest": {
        "type": "object",
        "required": ["message"],
        "properties": {
          "message": {
            "type": "string",
            "description": "User message"
          },
          "user_id": {
            "type": "string",
            "description": "User identifier"
          },
          "session_id": {
            "type": "string",
            "description": "Session identifier"
          }
        }
      },
      "ChatResponse": {
        "type": "object",
        "properties": {
          "response": {
            "type": "string",
            "description": "AI response"
          },
          "intent": {
            "type": "string",
            "description": "Detected intent"
          },
          "confidence": {
            "type": "number",
            "description": "Confidence score"
          }
        }
      }
    },
    "securitySchemes": {
      "ApiKeyAuth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "API key authentication"
      }
    }
  }
}
```

---

## 🔧 **SDK Examples**

### **Python SDK**
```python
import requests

class DubaiRealEstateAPI:
    def __init__(self, api_key, base_url="https://your-domain.com/api"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def send_message(self, message, user_id=None, session_id=None):
        data = {"message": message}
        if user_id:
            data["user_id"] = user_id
        if session_id:
            data["session_id"] = session_id
        
        response = requests.post(
            f"{self.base_url}/chat",
            headers=self.headers,
            json=data
        )
        return response.json()
    
    def get_properties(self, **filters):
        response = requests.get(
            f"{self.base_url}/properties",
            headers=self.headers,
            params=filters
        )
        return response.json()

# Usage
api = DubaiRealEstateAPI("YOUR_API_KEY")
response = api.send_message("Tell me about Dubai Marina properties")
properties = api.get_properties(location="Dubai Marina", min_price=2000000)
```

### **JavaScript SDK**
```javascript
class DubaiRealEstateAPI {
    constructor(apiKey, baseUrl = 'https://your-domain.com/api') {
        this.apiKey = apiKey;
        this.baseUrl = baseUrl;
        this.headers = {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
        };
    }
    
    async sendMessage(message, userId = null, sessionId = null) {
        const data = { message };
        if (userId) data.user_id = userId;
        if (sessionId) data.session_id = sessionId;
        
        const response = await fetch(`${this.baseUrl}/chat`, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(data)
        });
        return response.json();
    }
    
    async getProperties(filters = {}) {
        const params = new URLSearchParams(filters);
        const response = await fetch(`${this.baseUrl}/properties?${params}`, {
            headers: this.headers
        });
        return response.json();
    }
}

// Usage
const api = new DubaiRealEstateAPI('YOUR_API_KEY');
api.sendMessage('Tell me about Dubai Marina properties')
    .then(response => console.log(response));
```

---

## 📞 **Support**

### **Getting Help**
- **Documentation**: `/docs` (Swagger UI)
- **Email**: api@dubairealestate.com
- **Support Hours**: 24/7
- **Response Time**: < 4 hours

### **API Status**
- **Status Page**: https://status.dubairealestate.com
- **Uptime**: 99.9%
- **Average Response Time**: < 2 seconds

---

**Last Updated**: August 2024  
**Version**: 1.2.0  
**Maintainer**: API Team  
**Contact**: api@dubairealestate.com


