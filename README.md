
# Dubai Real Estate AI Intelligence Platform

A comprehensive AI-powered platform that revolutionizes Dubai's real estate industry through intelligent conversational AI, automated content generation, and advanced document processing. This platform serves real estate agents, investors, and clients by providing instant access to market insights, property information, and personalized recommendations through natural language conversations.

## High-Level Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        A[React Frontend<br/>Material-UI Components]
    end
    
    subgraph "Backend Layer"
        B[FastAPI Backend<br/>RESTful APIs]
        C[AI Enhancement Manager<br/>Conversation Memory]
        D[Intelligent Data Processor<br/>Document Classification]
    end
    
    subgraph "Data Layer"
        E[PostgreSQL DB<br/>User Data & Properties]
        F[ChromaDB<br/>Vector Embeddings]
        G[Redis Cache<br/>Session Management]
    end
    
    subgraph "AI Services"
        H[Google Gemini AI<br/>Natural Language Processing]
    end
    
    A --> B
    B --> C
    B --> D
    B --> E
    B --> F
    B --> G
    C --> H
    D --> H
    B --> H
```

## Key Features

### 🤖 **AI-Powered Conversational RAG**
Advanced chat functionality that understands natural language queries about Dubai real estate. The system maintains conversation context, learns user preferences, and provides personalized responses with market insights, property recommendations, and investment advice.

### 🚀 **Automated Content Generation Engine**
Powered by `ai_manager.py`, this engine generates personalized content including:
- Daily market briefings for agents
- Social media posts and marketing materials
- Client follow-up emails
- Market reports and property brochures
- Investment analysis and recommendations

### 📄 **Intelligent Document Processing**
The `intelligent_processor.py` system automatically:
- Classifies documents by content (legal, listings, market reports, etc.)
- Detects and merges duplicate properties
- Extracts key information from PDFs, CSVs, and other formats
- Validates data quality and completeness
- Standardizes property names and addresses

## Technology Stack

| Category | Technology | Version | Purpose |
|----------|------------|---------|---------|
| **Frontend** | React | 18.2.0 | User interface |
| | Material-UI | 5.18.0 | UI components |
| | React Router | 6.30.1 | Navigation |
| | Axios | 1.11.0 | HTTP client |
| **Backend** | FastAPI | 0.104.1 | API framework |
| | SQLAlchemy | 2.0.23 | ORM |
| | Pydantic | 2.5.0+ | Data validation |
| | Uvicorn | 0.24.0 | ASGI server |
| **Databases** | PostgreSQL | 15 | Primary database |
| | ChromaDB | 0.5.0+ | Vector database |
| | Redis | 7-alpine | Caching |
| **AI Services** | Google Gemini | 1.5-flash | Natural language processing |
| | Google Generative AI | 0.3.2 | AI integration |
| **Security** | JWT | 2.8.0 | Authentication |
| | bcrypt | 4.0.1 | Password hashing |
| | PyJWT | 2.8.0 | Token management |

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- Docker Desktop
- PostgreSQL 15+
- Google Cloud API Key

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "RAG web app"
```

### 2. Set Up Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Copy environment template
copy env.example .env
```

### 3. Configure Environment Variables
Edit `.env` file with your credentials:
```env
# Database Configuration
DATABASE_URL=postgresql://admin:password123@localhost:5432/real_estate_db

# Google AI Configuration
GOOGLE_API_KEY=your-google-api-key-here

# AI Model Configuration
AI_MODEL=gemini-1.5-flash

# Server Configuration
HOST=0.0.0.0
PORT=8001
DEBUG=True

# Authentication Configuration
SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Install Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### 5. Initialize Database
```bash
# Start PostgreSQL and create database
# The application will auto-initialize tables on first run
```

## Running the Application

### Start All Services with Docker
```bash
# Start all services (recommended)
docker-compose up -d
```

### Manual Startup (Alternative)
```bash
# Terminal 1: Start PostgreSQL and Redis
docker-compose up postgres redis chromadb -d

# Terminal 2: Start Backend
cd backend
uvicorn main_secure:app --host 0.0.0.0 --port 8001 --reload

# Terminal 3: Start Frontend
cd frontend
npm start
```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs
- **ReDoc Documentation**: http://localhost:8001/redoc

## API Documentation

The backend uses FastAPI with automatic OpenAPI documentation generation. When the server is running, you can access:

- **Interactive API Docs**: http://localhost:8001/docs - Swagger UI for testing endpoints
- **ReDoc Documentation**: http://localhost:8001/redoc - Alternative documentation view
- **OpenAPI Schema**: http://localhost:8001/openapi.json - Raw OpenAPI specification

The API includes endpoints for:
- User authentication and session management
- Chat conversations with AI
- Property management and search
- File upload and processing
- Market data and analytics
- Admin functions and monitoring

## Development

### Project Structure
```
├── backend/                 # FastAPI backend
│   ├── main_secure.py      # Main application entry point
│   ├── ai_manager.py       # AI enhancement manager
│   ├── intelligent_processor.py  # Document processing
│   ├── rag_service.py      # RAG implementation
│   └── auth/               # Authentication modules
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   └── context/        # React context
│   └── public/             # Static assets
├── data/                   # Sample data and documents
├── scripts/                # Utility scripts
├── tests/                  # Test files
└── docker-compose.yml      # Docker configuration
```

### Testing
```bash
# Run backend tests
pytest

# Run frontend tests
cd frontend
npm test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please refer to the project documentation or create an issue in the repository.
