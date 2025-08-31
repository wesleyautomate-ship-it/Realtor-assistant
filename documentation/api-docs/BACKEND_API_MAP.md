# Backend API Map

This document provides a complete map of all API endpoints in the Dubai Real Estate RAG Chat System backend, organized by router and functionality.

## API Endpoints Overview

| HTTP Method | URL Path | Router File | Description |
|-------------|----------|-------------|-------------|
| **Core Application Endpoints** |
| GET | `/` | main.py | Root endpoint with application information |
| GET | `/health` | main.py | Health check for all services (database, ChromaDB, cache) |
| POST | `/upload` | main.py | File upload endpoint with metadata |
| GET | `/admin/files` | main.py | Get list of uploaded files for admin management |
| DELETE | `/admin/files/{file_id}` | main.py | Delete a specific file by ID |
| POST | `/actions/execute` | main.py | Execute AI-powered actions |
| **Authentication Endpoints** |
| POST | `/auth/login` | auth/routes.py | User login with email and password |
| GET | `/auth/me` | auth/routes.py | Get current user information |
| **Chat Session Management** |
| POST | `/sessions` | chat_sessions_router.py | Create a new chat session |
| GET | `/sessions` | chat_sessions_router.py | List all chat sessions with pagination |
| GET | `/sessions/{session_id}` | chat_sessions_router.py | Get chat history for a specific session |
| POST | `/sessions/{session_id}/chat` | chat_sessions_router.py | Send a message in a chat session |
| DELETE | `/sessions/{session_id}` | chat_sessions_router.py | Delete a chat session |
| POST | `/sessions/{session_id}/clear` | chat_sessions_router.py | Clear all messages in a session |
| **Root Level Chat Endpoints** |
| POST | `/chat` | chat_sessions_router.py | Direct chat endpoint for RAG queries |
| **Property Management** |
| POST | `/properties` | property_management.py | Create a new property |
| GET | `/properties/search` | property_management.py | Search properties with filters |
| GET | `/properties/{property_id}` | property_management.py | Get detailed property information |
| PUT | `/properties/{property_id}` | property_management.py | Update property information |
| DELETE | `/properties/{property_id}` | property_management.py | Delete a property |
| GET | `/properties/types/list` | property_management.py | Get list of property types |
| GET | `/properties/locations/list` | property_management.py | Get list of property locations |
| PUT | `/properties/{property_id}/status` | property_management.py | Update property status |
| GET | `/properties/{property_id}/confidential` | property_management.py | Get confidential property details |
| **Market Data Endpoints** |
| GET | `/market/overview` | data_router.py | Get market overview and statistics |
| GET | `/market/trends` | data_router.py | Get market trends and analytics |
| GET | `/properties` | data_router.py | Get all properties (root level) |
| GET | `/clients` | data_router.py | Get all clients (root level) |
| **Reelly API Integration** |
| GET | `/api/v1/reference/developers` | reelly_router.py | Get all developers from Reelly network |
| GET | `/api/v1/reference/areas` | reelly_router.py | Get areas for a specific country |
| GET | `/api/v1/reelly/properties` | reelly_router.py | Search properties in Reelly network |
| GET | `/api/v1/reelly/status` | reelly_router.py | Get Reelly service status |
| **File Processing Endpoints** |
| POST | `/upload-file` | file_processing_router.py | Upload a file to uploads directory |
| POST | `/analyze-file` | file_processing_router.py | Analyze uploaded file using AI processor |
| POST | `/process-transaction-data` | file_processing_router.py | Process transaction data with duplicate detection |
| POST | `/check-data-quality` | file_processing_router.py | Check data quality of uploaded file |
| POST | `/fix-data-issues` | file_processing_router.py | Fix common data quality issues |
| POST | `/standardize-building-names` | file_processing_router.py | Standardize building names |
| GET | `/uploads/{filename}` | file_processing_router.py | Serve uploaded files |
| **Performance Monitoring** |
| GET | `/performance/cache-stats` | performance_router.py | Get cache performance statistics |
| GET | `/performance/cache-health` | performance_router.py | Get cache health status |
| GET | `/performance/batch-jobs` | performance_router.py | Get all active batch jobs |
| GET | `/performance/metrics` | performance_router.py | Get overall performance metrics |
| POST | `/performance/clear-cache` | performance_router.py | Clear all cache entries |
| DELETE | `/performance/cancel-job/{job_id}` | performance_router.py | Cancel a running batch job |
| GET | `/performance/analytics` | performance_router.py | Get performance analytics for the system |
| GET | `/performance/report` | performance_router.py | Get performance and cost metrics |
| **User Feedback System** |
| POST | `/feedback/submit` | feedback_router.py | Submit user feedback for quality improvement |
| GET | `/feedback/summary` | feedback_router.py | Get feedback summary for quality analysis |
| GET | `/feedback/recommendations` | feedback_router.py | Get improvement recommendations based on feedback |
| **Administrative Functions** |
| POST | `/admin/trigger-daily-briefing` | admin_router.py | Manually trigger daily briefing generation |
| **Document Ingestion** |
| POST | `/ingest/upload` | admin_router.py | Upload document for RAG system ingestion |
| **RAG Monitoring** |
| GET | `/rag-metrics` | rag_monitoring.py | Get RAG system metrics |
| GET | `/rag-performance-trends` | rag_monitoring.py | Get RAG performance trends |
| GET | `/knowledge-gaps-analysis` | rag_monitoring.py | Analyze knowledge gaps in RAG system |
| **Async Processing** |
| POST | `/async/analyze-file` | async_processing.py | Asynchronously analyze uploaded file |
| GET | `/async/processing-status/{task_id}` | async_processing.py | Get status of async processing task |
| **Admin Dashboard** |
| GET | `/dashboard-metrics` | admin_dashboard.py | Get dashboard metrics for admin panel |
| **Secure Sessions** |
| GET | `/sessions` | secure_sessions.py | Get secure chat sessions |
| GET | `/sessions/{session_id}` | secure_sessions.py | Get secure session details |
| POST | `/sessions` | secure_sessions.py | Create secure session |

## Router Organization

### Core Application (main.py)
- **6 endpoints**: Root, health check, file upload, admin files, actions
- **Purpose**: Core application functionality and health monitoring

### Authentication (auth/routes.py)
- **2 endpoints**: Login, user info
- **Purpose**: User authentication and session management

### Chat Sessions (chat_sessions_router.py)
- **8 endpoints**: Session management, chat, history
- **Purpose**: Complete chat functionality with RAG integration

### Property Management (property_management.py)
- **9 endpoints**: CRUD operations, search, types, locations
- **Purpose**: Comprehensive property management system

### Market Data (data_router.py)
- **4 endpoints**: Market overview, trends, properties, clients
- **Purpose**: Real estate market data and analytics

### Reelly Integration (reelly_router.py)
- **4 endpoints**: Developers, areas, properties, status
- **Purpose**: External Reelly API integration

### File Processing (file_processing_router.py)
- **7 endpoints**: Upload, analysis, processing, quality
- **Purpose**: File handling and data processing

### Performance Monitoring (performance_router.py)
- **8 endpoints**: Cache, metrics, analytics, reports
- **Purpose**: System performance monitoring and optimization

### User Feedback (feedback_router.py)
- **3 endpoints**: Submit, summary, recommendations
- **Purpose**: User feedback collection and analysis

### Administrative (admin_router.py)
- **2 endpoints**: Daily briefing, document ingestion
- **Purpose**: Administrative functions and system management

### RAG Monitoring (rag_monitoring.py)
- **3 endpoints**: Metrics, trends, knowledge gaps
- **Purpose**: RAG system monitoring and analysis

### Async Processing (async_processing.py)
- **2 endpoints**: File analysis, status checking
- **Purpose**: Asynchronous file processing

### Admin Dashboard (admin_dashboard.py)
- **1 endpoint**: Dashboard metrics
- **Purpose**: Admin panel data

### Secure Sessions (secure_sessions.py)
- **3 endpoints**: Secure session management
- **Purpose**: Enhanced session security

## API Statistics

- **Total Endpoints**: 65+ endpoints
- **HTTP Methods Used**: GET, POST, PUT, DELETE
- **Router Files**: 12 router files
- **Authentication Required**: Most endpoints require authentication
- **Response Formats**: JSON responses with Pydantic models
- **Error Handling**: Comprehensive error handling across all endpoints

## Endpoint Categories

### Public Endpoints
- Health check
- Root endpoint

### Authenticated Endpoints
- All other endpoints require valid authentication

### Admin-Only Endpoints
- Admin files management
- Daily briefing trigger
- Dashboard metrics
- Performance monitoring

### User Endpoints
- Chat sessions
- Property search
- File uploads
- Feedback submission

## Response Models

All endpoints use Pydantic models for:
- **Request Validation**: Input data validation
- **Response Serialization**: Consistent response formats
- **API Documentation**: Automatic OpenAPI schema generation
- **Type Safety**: Enhanced type checking

## Error Handling

- **HTTP Status Codes**: Proper status codes for different scenarios
- **Error Messages**: Descriptive error messages
- **Validation Errors**: Input validation with detailed feedback
- **Database Errors**: Graceful handling of database issues
- **External API Errors**: Proper error handling for external services
