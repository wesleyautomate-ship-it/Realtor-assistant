# Dubai Real Estate RAG Chat System - Developer Guide

## 📖 **Table of Contents**
1. [System Architecture](#system-architecture)
2. [Development Setup](#development-setup)
3. [Code Structure](#code-structure)
4. [API Documentation](#api-documentation)
5. [Database Schema](#database-schema)
6. [Testing Guidelines](#testing-guidelines)
7. [Deployment Guide](#deployment-guide)
8. [Contributing Guidelines](#contributing-guidelines)

---

## 🏗️ **System Architecture**

### **High-Level Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Databases     │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   PostgreSQL    │
│                 │    │                 │    │   ChromaDB      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   AI Service    │
                       │   (Gemini)      │
                       └─────────────────┘
```

### **Component Overview**

#### **Frontend (React)**
- **Technology**: React 18 with functional components and hooks
- **Styling**: CSS with responsive design
- **State Management**: React useState and useEffect
- **Key Features**: Role-based UI, file upload, chat interface

#### **Backend (FastAPI)**
- **Technology**: FastAPI with Python 3.11+
- **Architecture**: RESTful API with async support
- **Key Services**: RAG Service, Chat Service, File Processing
- **Performance**: Optimized for concurrent requests

#### **Databases**
- **PostgreSQL**: Structured data (properties, users, conversations)
- **ChromaDB**: Vector database for semantic search
- **Hybrid Approach**: Combined structured and unstructured data

#### **AI Service**
- **Provider**: Google Gemini (gemini-1.5-flash)
- **Integration**: RESTful API calls with streaming support
- **Context Management**: Intelligent prompt engineering

### **Data Flow Architecture**

```
User Query → Intent Classification → Context Retrieval → Response Generation
     │              │                      │                    │
     ▼              ▼                      ▼                    ▼
Frontend → FastAPI → RAG Service → ChromaDB/PostgreSQL → Gemini AI → Response
```

---

## 🛠️ **Development Setup**

### **Prerequisites**
- **Python**: 3.11 or higher
- **Node.js**: 18 or higher
- **Docker**: For containerized development
- **PostgreSQL**: 14 or higher
- **Git**: For version control

### **Environment Setup**

#### **1. Clone the Repository**
```bash
git clone <repository-url>
cd rag-web-app
```

#### **2. Backend Setup**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

#### **3. Frontend Setup**
```bash
cd frontend
npm install
npm start
```

#### **4. Database Setup**
```bash
# Start PostgreSQL and ChromaDB with Docker
docker-compose up -d

# Run database migrations
python scripts/dubai_database_migration.py

# Ingest sample data
python scripts/dubai_research_ingestion.py
```

### **Environment Variables**

#### **Backend (.env)**
```env
# Database Configuration
DATABASE_URL=postgresql://admin:password123@localhost:5432/real_estate_db

# ChromaDB Configuration
CHROMA_HOST=localhost
CHROMA_PORT=8000

# AI Service Configuration
GEMINI_API_KEY=your_gemini_api_key

# Application Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8001

# Security
SECRET_KEY=your_secret_key
```

#### **Frontend (.env)**
```env
REACT_APP_API_URL=http://localhost:8001
REACT_APP_VERSION=1.2.0
```

### **Development Tools**

#### **Recommended IDE Setup**
- **VS Code** with extensions:
  - Python
  - React Developer Tools
  - Docker
  - GitLens
  - Prettier
  - ESLint

#### **Debugging Tools**
- **Backend**: FastAPI debug mode with auto-reload
- **Frontend**: React Developer Tools
- **Database**: pgAdmin for PostgreSQL
- **API Testing**: Postman or Insomnia

---

## 📁 **Code Structure**

### **Project Organization**
```
rag-web-app/
├── backend/                    # FastAPI backend
│   ├── main.py                # FastAPI application entry point
│   ├── enhanced_rag_service.py # Core RAG service
│   ├── property_management.py  # Property management endpoints
│   └── requirements.txt       # Python dependencies
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── App.js             # Main React component
│   │   ├── App.css            # Main stylesheet
│   │   └── components/        # React components
│   ├── package.json           # Node.js dependencies
│   └── public/                # Static assets
├── scripts/                    # Utility scripts
│   ├── dubai_research_ingestion.py
│   ├── dubai_database_migration.py
│   ├── test_*.py              # Test scripts
│   └── processors/            # Data processing modules
├── docs/                       # Documentation
├── docker-compose.yml         # Docker configuration
└── README.md                  # Project overview
```

### **Backend Architecture**

#### **Core Services**
- **EnhancedRAGService**: Main RAG implementation with Dubai-specific features
- **PropertyManagement**: Property search and management endpoints
- **FileProcessing**: Document upload and processing
- **ChatService**: Chat functionality and conversation management

#### **Key Classes and Functions**

##### **EnhancedRAGService**
```python
class EnhancedRAGService:
    def __init__(self, db_url: str, chroma_host: str, chroma_port: int)
    def analyze_query(self, query: str) -> QueryAnalysis
    def get_relevant_context(self, query: str, analysis: QueryAnalysis) -> List[ContextItem]
    def generate_response(self, query: str, context: List[ContextItem], role: str) -> str
```

##### **QueryAnalysis**
```python
@dataclass
class QueryAnalysis:
    intent: QueryIntent
    entities: Dict[str, Any]
    dubai_specific: bool
    confidence: float
```

##### **ContextItem**
```python
@dataclass
class ContextItem:
    content: str
    source: str
    relevance_score: float
    data_type: str
    metadata: Dict[str, Any]
```

### **Frontend Architecture**

#### **Component Structure**
- **App.js**: Main application component with routing
- **ChatInterface**: Chat functionality and message handling
- **RoleSelector**: Role-based UI switching
- **FileUpload**: Document upload and processing
- **PropertySearch**: Property search interface

#### **State Management**
```javascript
// Main application state
const [messages, setMessages] = useState([]);
const [selectedRole, setSelectedRole] = useState('client');
const [isLoading, setIsLoading] = useState(false);
const [uploadedFiles, setUploadedFiles] = useState([]);
```

---

## 🔌 **API Documentation**

### **Core Endpoints**

#### **Chat Endpoint**
```http
POST /chat
Content-Type: application/json

{
  "message": "string",
  "role": "client|agent|employee|admin",
  "session_id": "string"
}

Response:
{
  "response": "string",
  "context_used": ["string"],
  "intent": "string",
  "confidence": 0.95
}
```

#### **Property Search**
```http
GET /properties
Query Parameters:
- location: string
- min_price: number
- max_price: number
- bedrooms: number
- property_type: string

Response:
{
  "properties": [
    {
      "id": 1,
      "title": "string",
      "location": "string",
      "price": 1000000,
      "bedrooms": 2,
      "property_type": "apartment"
    }
  ],
  "total": 10
}
```

#### **File Upload**
```http
POST /upload
Content-Type: multipart/form-data

Form Data:
- file: File
- role: string

Response:
{
  "filename": "string",
  "status": "processed",
  "message": "string"
}
```

### **Error Handling**

#### **Standard Error Response**
```json
{
  "error": "string",
  "detail": "string",
  "status_code": 400
}
```

#### **Common Error Codes**
- **400**: Bad Request - Invalid input data
- **401**: Unauthorized - Authentication required
- **422**: Validation Error - Invalid request format
- **500**: Internal Server Error - Server-side error

---

## 🗄️ **Database Schema**

### **PostgreSQL Tables**

#### **Properties Table**
```sql
CREATE TABLE properties (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    location VARCHAR(255),
    price DECIMAL(12,2),
    bedrooms INTEGER,
    bathrooms INTEGER,
    property_type VARCHAR(50),
    neighborhood VARCHAR(100),
    developer VARCHAR(100),
    completion_date DATE,
    rental_yield DECIMAL(5,2),
    property_status VARCHAR(50),
    amenities JSONB,
    market_segment VARCHAR(50),
    freehold_status BOOLEAN,
    service_charges DECIMAL(10,2),
    parking_spaces INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **Dubai-Specific Tables**
```sql
-- Market Data
CREATE TABLE market_data (
    id SERIAL PRIMARY KEY,
    area VARCHAR(100),
    property_type VARCHAR(50),
    avg_price DECIMAL(12,2),
    price_change_percentage DECIMAL(5,2),
    transaction_volume INTEGER,
    rental_yield DECIMAL(5,2),
    market_trend VARCHAR(50),
    data_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Regulatory Updates
CREATE TABLE regulatory_updates (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    regulation_type VARCHAR(100),
    effective_date DATE,
    requirements JSONB,
    impact_analysis TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Developers
CREATE TABLE developers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    market_share DECIMAL(5,2),
    reputation_score DECIMAL(3,1),
    key_projects JSONB,
    track_record TEXT,
    contact_info JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **ChromaDB Collections**

#### **Collection Structure**
```python
# Collection metadata
{
    "name": "collection_name",
    "metadata": {
        "description": "Collection description",
        "data_type": "market_analysis|regulatory|neighborhoods",
        "last_updated": "2024-08-23"
    }
}

# Document structure
{
    "id": "unique_id",
    "content": "document_content",
    "metadata": {
        "source": "source_name",
        "date": "2024-08-23",
        "category": "category_name",
        "relevance_score": 0.95
    }
}
```

#### **Collection Types**
- **market_analysis**: Market trends and analysis
- **regulatory_framework**: Laws and regulations
- **neighborhood_profiles**: Area information
- **investment_insights**: Investment guidance
- **developer_profiles**: Developer information
- **transaction_guidance**: Transaction processes
- **market_forecasts**: Future predictions
- **agent_resources**: Agent tools and resources
- **urban_planning**: Dubai 2040 and planning
- **financial_insights**: Financial information

---

## 🧪 **Testing Guidelines**

### **Testing Strategy**

#### **Test Types**
1. **Unit Tests**: Individual component testing
2. **Integration Tests**: End-to-end workflow testing
3. **Performance Tests**: Load and stress testing
4. **User Acceptance Tests**: Real-world scenario testing

#### **Test Coverage Requirements**
- **Backend**: >90% code coverage
- **Frontend**: >80% component coverage
- **API**: 100% endpoint coverage
- **Database**: All CRUD operations tested

### **Running Tests**

#### **Backend Tests**
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_rag_service.py

# Run with coverage
python -m pytest --cov=backend tests/
```

#### **Frontend Tests**
```bash
cd frontend
npm test
npm run test:coverage
```

#### **Integration Tests**
```bash
# Run integration test suite
python scripts/test_integration_suite.py

# Run performance tests
python scripts/performance_testing.py

# Run user acceptance tests
python scripts/user_acceptance_testing.py
```

### **Test Data Management**

#### **Test Databases**
- **Development**: Local PostgreSQL instance
- **Testing**: Separate test database
- **Staging**: Production-like environment

#### **Sample Data**
```bash
# Load test data
python scripts/dubai_research_ingestion.py

# Reset test data
python scripts/reset_test_data.py
```

---

## 🚀 **Deployment Guide**

### **Production Environment**

#### **System Requirements**
- **CPU**: 4+ cores
- **RAM**: 8GB+ (16GB recommended)
- **Storage**: 100GB+ SSD
- **Network**: High-speed internet connection

#### **Software Stack**
- **OS**: Ubuntu 20.04 LTS or higher
- **Web Server**: Nginx
- **Application Server**: Gunicorn
- **Database**: PostgreSQL 14+
- **Vector Database**: ChromaDB
- **Container**: Docker & Docker Compose

### **Deployment Steps**

#### **1. Server Setup**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### **2. Application Deployment**
```bash
# Clone repository
git clone <repository-url>
cd rag-web-app

# Configure environment
cp .env.example .env
# Edit .env with production values

# Build and start services
docker-compose -f docker-compose.prod.yml up -d

# Run database migrations
docker-compose exec backend python scripts/dubai_database_migration.py

# Load initial data
docker-compose exec backend python scripts/dubai_research_ingestion.py
```

#### **3. Nginx Configuration**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### **4. SSL Configuration**
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com
```

### **Monitoring and Maintenance**

#### **Enterprise Monitoring Setup**
```bash
# Start monitoring infrastructure
docker-compose -f docker-compose.monitoring.yml up -d

# Access monitoring dashboards
# Grafana: http://localhost:3001 (admin/admin)
# Prometheus: http://localhost:9090
# AlertManager: http://localhost:9093

# Check monitoring services
docker-compose -f docker-compose.monitoring.yml ps
docker-compose -f docker-compose.monitoring.yml logs prometheus
```

#### **Application Monitoring Integration**
```python
# The monitoring system is automatically integrated through monitoring_manager.py
# Key monitoring features available:

# 1. Performance Monitoring
from monitoring.application_metrics import MetricsCollector
metrics = MetricsCollector()
metrics.track_rag_query("property_search", response_time=1.2)

# 2. Error Tracking
from monitoring.error_tracker import ErrorTracker
error_tracker = ErrorTracker()
error_tracker.track_error("database_connection", "Connection timeout", severity="high")

# 3. Health Checks
from monitoring.health_checks import HealthChecker
health_checker = HealthChecker()
status = health_checker.check_system_health()

# 4. Custom Metrics
from monitoring.application_metrics import rag_queries_total, response_time_histogram
rag_queries_total.inc()
response_time_histogram.observe(1.5)
```

#### **Health Checks**
```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Monitor resources
docker stats

# Health check endpoints
curl http://localhost:8001/health
curl http://localhost:8001/health/detailed
curl http://localhost:8001/metrics
```

#### **Backup Procedures**
```bash
# Database backup
docker-compose exec postgres pg_dump -U admin real_estate_db > backup.sql

# ChromaDB backup
docker-compose exec chromadb tar -czf chromadb_backup.tar.gz /chroma/chroma

# Application backup
tar -czf app_backup.tar.gz /path/to/application
```

#### **Performance Monitoring**
- **Application Metrics**: Response times, error rates
- **Database Metrics**: Query performance, connection usage
- **System Metrics**: CPU, memory, disk usage
- **User Metrics**: Active users, session duration

---

## 🤝 **Contributing Guidelines**

### **Development Workflow**

#### **1. Feature Development**
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "feat: add new feature"

# Push and create pull request
git push origin feature/new-feature
```

#### **2. Code Review Process**
1. **Create Pull Request**: Detailed description of changes
2. **Code Review**: At least one reviewer approval required
3. **Testing**: All tests must pass
4. **Documentation**: Update relevant documentation
5. **Merge**: Squash and merge to main branch

### **Coding Standards**

#### **Python (Backend)**
```python
# Follow PEP 8 style guide
def calculate_roi(property_price: float, rental_income: float) -> float:
    """
    Calculate ROI for a property investment.
    
    Args:
        property_price: Total property price
        rental_income: Annual rental income
        
    Returns:
        ROI percentage
    """
    return (rental_income / property_price) * 100
```

#### **JavaScript (Frontend)**
```javascript
// Use ES6+ features and consistent formatting
const calculateROI = (propertyPrice, rentalIncome) => {
  /**
   * Calculate ROI for a property investment
   * @param {number} propertyPrice - Total property price
   * @param {number} rentalIncome - Annual rental income
   * @returns {number} ROI percentage
   */
  return (rentalIncome / propertyPrice) * 100;
};
```

#### **Documentation Standards**
- **Code Comments**: Explain complex logic
- **API Documentation**: Use OpenAPI/Swagger
- **README Updates**: Keep documentation current
- **Change Log**: Document all changes

### **Quality Assurance**

#### **Pre-commit Checks**
```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run checks
pre-commit run --all-files
```

#### **Code Quality Tools**
- **Python**: Black, Flake8, MyPy
- **JavaScript**: ESLint, Prettier
- **Git**: Conventional Commits

---

## 📚 **Additional Resources**

### **Documentation**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [ChromaDB Documentation](https://docs.trychroma.com/)

### **Development Tools**
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Git Documentation](https://git-scm.com/doc)

### **Testing Resources**
- [Pytest Documentation](https://docs.pytest.org/)
- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [Postman Documentation](https://learning.postman.com/)

---

**Last Updated**: August 2024  
**Version**: 1.2.0  
**Maintainer**: Development Team  
**Contact**: dev@dubairealestate.com


