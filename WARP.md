# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

# Dubai Real Estate RAG System - Developer Guide

## Project Overview

This is an **Enterprise-Grade AI-Powered Real Estate Intelligence Platform** for Dubai property professionals. The system combines **Retrieval-Augmented Generation (RAG)**, **Model Context Protocol (MCP)**, and **AI Agentic features** to create an intelligent real estate assistant with conversational CRM, workflow automation, and enterprise monitoring capabilities.

The platform serves multiple user roles (clients, agents, admin, employees) with role-based access control and data segregation. It processes Dubai real estate data through a sophisticated AI pipeline and provides market insights, property recommendations, and workflow automation.

## Essential Development Commands

### Quick Start (Local Development)
```powershell
# 1. Environment Setup
Copy-Item env.example .env
# Edit .env with your API keys (GOOGLE_API_KEY, REELLY_API_KEY)

# 2. Start Services (Local)
# Terminal 1 - Backend
cd backend
uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Terminal 2 - Frontend  
cd frontend
npm start

# Terminal 3 - ChromaDB (Docker)
docker run -p 8002:8000 chromadb/chroma:latest

# Terminal 4 - PostgreSQL (ensure service is running)
# Windows: Services → PostgreSQL should be started
```

### Docker Deployment
```powershell
# Start all services
docker-compose up -d --build

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

### Database Management
```sql
-- Create PostgreSQL database (run once)
psql -U postgres
CREATE DATABASE real_estate_db;
CREATE USER admin WITH PASSWORD 'password123';
GRANT ALL PRIVILEGES ON DATABASE real_estate_db TO admin;
\q
```

```powershell
# Initialize database tables
cd backend
python init_database.py

# Populate with sample data
python populate_postgresql.py
python populate_chromadb.py
```

### Testing Commands
```powershell
# Run all tests (Windows)
.\run_tests.bat all

# Run specific test types
.\run_tests.bat unit                    # Unit tests only
.\run_tests.bat integration            # Integration tests only
.\run_tests.bat performance --load     # Performance tests
.\run_tests.bat quick                  # Unit + integration

# Alternative: Python test runner
python scripts\run_tests.py --test-types unit integration
python scripts\test_system.py
```

### Service Management Scripts
```powershell
# Setup database and services
python scripts\setup_database.py
python scripts\start_services.py

# Deploy to production
python scripts\deploy.py
```

## High-Level Architecture

The system implements a sophisticated RAG pipeline with multi-intent recognition and context-aware response generation:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │◄──►│  FastAPI Backend│◄──►│ Google Gemini   │
│   Material-UI    │    │  + Auth + RBAC  │    │   AI Model      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
        ┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼─────┐
        │ PostgreSQL   │ │  ChromaDB   │ │   Redis   │
        │ (Relational) │ │ (Vectors)   │ │  (Cache)  │
        └──────────────┘ └─────────────┘ └───────────┘
```

### RAG Pipeline Flow
1. **Intent Classification** → Extract user intent (property_search, market_info, investment_question, etc.)
2. **Entity Extraction** → Parse entities (budget, location, property_type, bedrooms)
3. **Context Retrieval** → Query ChromaDB collections based on intent
4. **Prompt Engineering** → Create enhanced prompts with context and user preferences
5. **AI Generation** → Generate response using Google Gemini
6. **Response Enhancement** → Add property recommendations, market insights, next steps
7. **Caching & Monitoring** → Cache responses and track performance metrics

### Core AI Components
- **ImprovedRAGService**: Main RAG orchestration with 10 specialized ChromaDB collections
- **AIEnhancementManager**: Response enhancement and personalization
- **IntelligentDataProcessor**: Document processing and data extraction
- **ConversationMemory**: Context persistence across chat sessions
- **ActionEngine**: Conversational CRM workflow automation

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | React 18 + Material-UI + TypeScript | User interface and interactions |
| **Backend** | FastAPI + Python + SQLAlchemy | API services and business logic |
| **AI/ML** | Google Gemini + Custom RAG + ChromaDB | Natural language processing and generation |
| **Database** | PostgreSQL + Redis | Relational data and caching |
| **Vector DB** | ChromaDB | Document embeddings and similarity search |
| **Auth** | JWT + bcrypt + RBAC | Authentication and authorization |
| **Deployment** | Docker + Docker Compose | Containerization and orchestration |
| **Monitoring** | Prometheus + Grafana | Application performance monitoring |
| **Testing** | Pytest + Jest + Coverage | Comprehensive test suites |

## Repository Structure

```
├── backend/                    # FastAPI application
│   ├── auth/                   # Authentication system
│   ├── security/              # RBAC and session management
│   ├── performance/           # Optimization and caching
│   ├── quality/               # Feedback system
│   ├── monitoring/            # Application metrics
│   ├── advanced_features/     # AI enhancements
│   ├── main.py               # FastAPI app entry point
│   ├── rag_service.py        # RAG implementation
│   ├── ai_manager.py         # AI orchestration
│   ├── property_management.py # Property APIs
│   └── requirements.txt      # Python dependencies
├── frontend/                  # React application
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── auth/            # Authentication UI
│   │   └── utils/           # Utilities and API calls
│   ├── package.json         # Node.js dependencies
│   └── Dockerfile           # Frontend container config
├── scripts/                  # Automation scripts
│   ├── setup_database.py    # Database initialization
│   ├── start_services.py    # Service orchestration
│   ├── run_tests.py         # Test runner
│   └── deploy.py            # Deployment automation
├── tests/                    # Test suites
├── docs/                     # Additional documentation
├── monitoring/              # Grafana/Prometheus configs
├── docker-compose.yml       # Container orchestration
├── pytest.ini             # Test configuration
└── run_tests.bat           # Windows test runner
```

## Database Schema & Setup

### Core PostgreSQL Tables
```sql
-- Properties table
CREATE TABLE properties (
    id SERIAL PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    price_aed DECIMAL(15,2),
    bedrooms INTEGER,
    bathrooms DECIMAL(3,1),
    size_sqft INTEGER,
    property_type VARCHAR(100),
    area VARCHAR(100),
    developer VARCHAR(100),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users and authentication
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'client',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Conversations and messages
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Market data for insights
CREATE TABLE market_data (
    id SERIAL PRIMARY KEY,
    area VARCHAR(100),
    property_type VARCHAR(100),
    avg_price DECIMAL(15,2),
    price_change_percentage DECIMAL(5,2),
    rental_yield DECIMAL(5,2),
    data_date DATE
);
```

### ChromaDB Collections
The system uses 10 specialized vector collections:
- `market_analysis` - Price dynamics and trends
- `regulatory_framework` - Dubai real estate laws
- `neighborhood_profiles` - Area information and amenities
- `investment_insights` - ROI analysis and strategies
- `developer_profiles` - Major developers and projects
- `transaction_guidance` - Buying/selling processes
- `market_forecasts` - Future predictions
- `agent_resources` - Sales techniques
- `urban_planning` - Dubai 2040 development plans
- `financial_insights` - Financing options

## Environment Configuration

### Required Environment Variables (.env)
```bash
# Database
DATABASE_URL=postgresql://admin:password123@localhost:5432/real_estate_db

# AI Services
GOOGLE_API_KEY=AIzaSyAocEBBwmq_eZ1Dy5RT9S7Kkfyw8nNibmM
REELLY_API_KEY=reelly-ca193726-B8UWmLERvIIp-S_PuqiJ5vkXKFcBM3Fv  # Optional

# ChromaDB
CHROMA_HOST=localhost
CHROMA_PORT=8002

# Redis Cache
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# JWT Authentication
JWT_SECRET_KEY=e093b4726d3097764be917a8ac782c53
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Security
BCRYPT_ROUNDS=12
SECRET_KEY=your_secret_key_for_sessions

# Application
AI_MODEL=gemini-1.5-flash-latest
HOST=0.0.0.0
PORT=8001
DEBUG=true
ENVIRONMENT=development

# File Upload
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_DIR=backend/uploads
ALLOWED_EXTENSIONS=pdf,docx,xlsx,txt
```

## Docker Deployment

### Services Overview
- **postgres**: PostgreSQL database (port 5432)
- **redis**: Redis cache (port 6379)  
- **chromadb**: Vector database (port 8002)
- **backend**: FastAPI application (port 8001)
- **frontend**: React application (port 3000)

### Docker Commands
```powershell
# Development with live reload
docker-compose up -d
docker-compose logs -f backend

# Production build
docker-compose -f docker-compose.prod.yml up -d

# View service status
docker-compose ps

# Access individual services
docker-compose exec backend python init_database.py
docker-compose exec postgres psql -U admin -d real_estate_db
```

### Monitoring Infrastructure
```powershell
# Start monitoring stack
docker-compose -f docker-compose.monitoring.yml up -d

# Access dashboards
# Grafana: http://localhost:3001 (admin/admin)
# Prometheus: http://localhost:9090
# AlertManager: http://localhost:9093
```

## Testing Framework

### Pytest Configuration
The system uses comprehensive pytest setup with multiple test categories:

```powershell
# Test markers available
pytest -m unit                    # Unit tests
pytest -m integration            # Integration tests  
pytest -m performance           # Performance tests
pytest -m security              # Security tests
pytest -m api                   # API endpoint tests
pytest -m rag                   # RAG functionality tests

# Coverage reporting
pytest --cov=backend --cov-report=html
```

### Test Categories
- **Unit Tests**: Individual component testing
- **Integration Tests**: Service integration testing
- **Performance Tests**: Load and stress testing scenarios
- **Security Tests**: Authentication and authorization testing
- **End-to-End Tests**: Complete workflow testing
- **AI Tests**: RAG pipeline and response quality testing

### Performance Test Scenarios
```powershell
# Load testing options
.\run_tests.bat performance --load     # 20 users, 5 minutes
.\run_tests.bat performance --stress   # 50 users, 10 minutes  
.\run_tests.bat performance --smoke    # 5 users, 1 minute
.\run_tests.bat performance --spike    # 100 users, 5 minutes
```

## Key Integration Points

### Google Gemini AI Integration
```python
# Configuration in backend/main.py
import google.generativeai as genai
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Health check endpoint
GET /api/health/gemini
```

### ChromaDB Vector Database
```python
# Connection setup
chroma_client = chromadb.HttpClient(
    host=CHROMA_HOST, 
    port=CHROMA_PORT
)

# Health check
GET /api/health/chroma
```

### PostgreSQL Database
```python
# SQLAlchemy connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Health check
GET /api/health/database
```

### Redis Cache
```python
# Redis connection
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

# Health check
GET /api/health/redis
```

## Security & Authentication

### JWT Authentication Flow
1. User login with email/password
2. Backend validates credentials with bcrypt
3. JWT access token generated (30min expiry)
4. JWT refresh token generated (7 day expiry)
5. Subsequent requests include Authorization header
6. Middleware validates JWT and extracts user context

### Role-Based Access Control (RBAC)
```python
# Available roles and permissions
role_permissions = {
    'admin': ['read', 'write', 'delete', 'admin'],
    'agent': ['read', 'write', 'limited_delete'],
    'client': ['read', 'limited_write'],
    'employee': ['read', 'write']
}
```

### Authentication Endpoints
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `POST /auth/refresh` - Token refresh
- `POST /auth/logout` - User logout
- `GET /auth/me` - Current user profile

## Performance, Caching & Monitoring

### Cache Strategy
```python
# Redis caching with TTL
cache_manager = CacheManager()
cache_manager.cache_response(query_hash, response, ttl=1800)  # 30 minutes
cache_manager.cache_property_data(area, property_type, data)
```

### Performance Monitoring
- **Response Time Tracking**: API endpoint performance
- **Cache Hit Rates**: Redis cache efficiency
- **Database Query Performance**: Query execution times
- **Memory Usage**: Application resource monitoring
- **User Session Analytics**: Active session tracking

### Monitoring Dashboards
```bash
# Access monitoring interfaces
http://localhost:3001  # Grafana (admin/admin)
http://localhost:9090  # Prometheus metrics
http://localhost:8001/docs  # FastAPI OpenAPI docs
```

## File Upload & Document Processing

### Supported File Types
- **PDF**: Property brochures, legal documents
- **DOCX**: Company policies, contracts
- **XLSX**: Market data, property listings
- **TXT**: Simple text documents

### Upload Configuration
```python
MAX_FILE_SIZE = 10485760  # 10MB
ALLOWED_EXTENSIONS = ['pdf', 'docx', 'xlsx', 'txt']
UPLOAD_DIR = 'backend/uploads'
```

### IntelligentDataProcessor Pipeline
1. **File Validation**: Type and size checking
2. **Content Extraction**: Text extraction from documents
3. **Data Classification**: AI-powered document categorization
4. **Structured Extraction**: Property data extraction
5. **Database Integration**: Automatic data insertion
6. **ChromaDB Indexing**: Vector embedding generation

### File Upload Endpoints
- `POST /api/upload` - Single file upload
- `POST /api/upload/batch` - Multiple file upload
- `GET /api/upload/status/{task_id}` - Upload status
- `GET /api/files` - List uploaded files

## Troubleshooting & FAQ

### Common Development Issues

**Port Conflicts**
```powershell
# Check port usage
netstat -ano | findstr :8001
netstat -ano | findstr :3000

# Kill process on port
taskkill /PID <process-id> /F
```

**Database Connection Issues**
```powershell
# Test PostgreSQL connection
psql -U admin -h localhost -p 5432 -d real_estate_db

# Check Docker containers
docker ps
docker logs <container-id>
```

**ChromaDB Issues**
```powershell
# Restart ChromaDB container
docker restart <chromadb-container-id>

# Check ChromaDB logs
docker logs <chromadb-container-id>
```

**Environment Variables Not Loading**
```powershell
# Verify .env file exists
Get-Content .env

# Check environment in application
GET /api/health/config
```

### Performance Issues
- **Slow API Responses**: Check Redis cache hit rates
- **High Memory Usage**: Monitor ChromaDB vector storage
- **Database Timeouts**: Review query performance and indexes
- **AI Response Delays**: Monitor Google Gemini API limits

### Testing Issues
```powershell
# Clear test database
python -c "from backend.init_database import clear_test_db; clear_test_db()"

# Reset ChromaDB test collections
docker volume rm <chroma-test-volume>

# Run tests with verbose output
pytest -v -s tests/
```

### Security Considerations
- Always use HTTPS in production
- Rotate JWT secret keys regularly
- Monitor failed authentication attempts
- Validate all user inputs
- Keep API keys secure and never commit to repository
- Use environment-specific configurations

### Quick Health Checks
```bash
# Backend health
GET http://localhost:8001/health

# Frontend health  
GET http://localhost:3000

# Database connectivity
GET http://localhost:8001/api/health/database

# AI service connectivity
GET http://localhost:8001/api/health/gemini
```
