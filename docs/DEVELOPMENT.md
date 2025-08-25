# Development Guide

## Setup Development Environment

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 15+
- Docker
- Google AI API Key

### Initial Setup

1. **Clone and setup:**
   ```bash
   git clone <repository-url>
   cd rag-web-app
   python scripts/setup_database.py
   ```

2. **Install dependencies:**
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   
   # Frontend
   cd ../frontend
   npm install
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and settings
   ```

### Development Workflow

1. **Start services:**
   ```bash
   python scripts/start_services.py
   ```

2. **Run tests:**
   ```bash
   python scripts/test_system.py
   ```

3. **Development URLs:**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8001
   - ChromaDB: http://localhost:8000

### Code Structure

```
rag-web-app/
├── backend/                 # FastAPI backend
│   ├── config/             # Configuration
│   ├── rag_service_improved.py  # Main RAG service
│   ├── ai_manager.py       # AI enhancement
│   ├── cache_manager.py    # Redis caching
│   ├── batch_processor.py  # Batch processing
│   └── main.py            # FastAPI app
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API services
│   │   └── App.js         # Main app
│   └── package.json
├── scripts/                # Utility scripts
│   ├── setup_database.py   # Database setup
│   ├── test_system.py      # System testing
│   ├── start_services.py   # Service management
│   └── deploy.py          # Production deployment
├── data/                   # Data files
│   ├── uploads/           # File uploads
│   └── exports/           # Data exports
└── docs/                   # Documentation
```

### Key Components

#### RAG Service (`rag_service_improved.py`)
- Query analysis and intent classification
- Context retrieval from ChromaDB and PostgreSQL
- Improved prompt generation
- Response enhancement

#### AI Manager (`ai_manager.py`)
- Conversation memory
- User preferences
- Role-based responses
- Enhanced prompts

#### Cache Manager (`cache_manager.py`)
- Redis caching for queries
- Context caching
- Session management
- Performance optimization

#### Batch Processor (`batch_processor.py`)
- Asynchronous data processing
- Background jobs
- Performance monitoring
- Error handling

### Testing

```bash
# Run system tests
python scripts/test_system.py

# Run specific tests
python -m pytest backend/tests/

# Test RAG service
python scripts/test_improved_rag.py
```

### Debugging

1. **Check logs:**
   ```bash
   # Backend logs
   tail -f logs/backend.log
   
   # Frontend logs
   tail -f logs/frontend.log
   ```

2. **Database debugging:**
   ```bash
   # Connect to PostgreSQL
   psql -U admin -d real_estate_db
   
   # Check ChromaDB
   curl http://localhost:8000/api/v1/heartbeat
   ```

3. **API debugging:**
   ```bash
   # Test health endpoint
   curl http://localhost:8001/health
   
   # Test chat endpoint
   curl -X POST http://localhost:8001/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "test", "session_id": "test"}'
   ```

### Performance Optimization

1. **Caching:**
   - Redis is used for query caching
   - Context items are cached
   - User sessions are cached

2. **Batch Processing:**
   - Large data ingestion is batched
   - Background processing for heavy tasks
   - Async operations for better performance

3. **Database Optimization:**
   - Indexed queries
   - Connection pooling
   - Query optimization

### Deployment

```bash
# Development deployment
python scripts/deploy.py

# Production deployment
./start.sh
```

### Contributing

1. Follow the existing code structure
2. Add tests for new features
3. Update documentation
4. Run the full test suite
5. Follow the coding standards

### Troubleshooting

Common issues and solutions:

1. **Database connection issues:**
   - Check PostgreSQL service is running
   - Verify connection string in .env
   - Check firewall settings

2. **ChromaDB issues:**
   - Ensure Docker is running
   - Check ChromaDB container status
   - Verify port 8000 is available

3. **API key issues:**
   - Verify GOOGLE_API_KEY in .env
   - Check API key permissions
   - Monitor API usage limits

4. **Performance issues:**
   - Check Redis connection
   - Monitor database performance
   - Review caching strategy
