# Blueprint 2.0 Docker Testing Guide

This guide provides comprehensive instructions for testing the Blueprint 2.0 implementation using Docker.

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- Docker Compose installed
- At least 4GB of available RAM
- Ports 3000, 5432, 6379, 8002, 8003 available

### Automated Testing (Recommended)

#### Windows
```bash
docker-test-blueprint2.bat
```

#### Linux/Mac
```bash
chmod +x docker-test-blueprint2.sh
./docker-test-blueprint2.sh
```

### Manual Testing

1. **Start Services**
   ```bash
   docker-compose up -d --build
   ```

2. **Wait for Services to be Healthy**
   ```bash
   # Check service status
   docker-compose ps
   
   # View logs
   docker-compose logs -f backend
   ```

3. **Run Database Setup**
   ```bash
   # Run migrations
   docker-compose exec backend python database_migrations.py
   
   # Populate with sample data
   docker-compose exec backend python populate_postgresql.py
   ```

4. **Run Blueprint 2.0 Tests**
   ```bash
   docker-compose --profile test run --rm test-runner
   ```

## 📋 Service Architecture

### Services Overview
- **PostgreSQL** (Port 5432): Main database
- **Redis** (Port 6379): Caching and session storage
- **ChromaDB** (Port 8002): Vector database for embeddings
- **Backend** (Port 8003): FastAPI application with Blueprint 2.0
- **Frontend** (Port 3000): React application
- **Test Runner**: Dedicated service for running tests

### Blueprint 2.0 Features Tested
- ✅ Web-based content delivery (HTML documents)
- ✅ Proactive lead nurturing system
- ✅ Document generation with AI
- ✅ Lead interaction tracking
- ✅ Automated notifications
- ✅ Background scheduling

## 🧪 Testing Blueprint 2.0 Features

### 1. Document Generation Testing

#### Test CMA Generation
```bash
curl -X POST http://localhost:8003/async/process-file \
  -H "Content-Type: application/json" \
  -d '{
    "file_type": "cma_request",
    "instructions": "Generate CMA for Villa 12, Emirates Hills",
    "metadata": {
      "subject_property": {
        "address": "Villa 12, Emirates Hills",
        "property_type": "villa",
        "bedrooms": 5,
        "bathrooms": 6,
        "size_sqft": 4500,
        "current_price": 12000000
      }
    }
  }'
```

#### Test Document Viewing
```bash
# List documents
curl http://localhost:8003/documents/

# View specific document (replace {id} with actual document ID)
curl http://localhost:8003/documents/view/{id}
```

### 2. Lead Nurturing Testing

#### Test Agenda Endpoint
```bash
curl http://localhost:8003/nurturing/users/me/agenda
```

#### Test Lead History
```bash
# Get lead history (replace {lead_id} with actual lead ID)
curl http://localhost:8003/nurturing/leads/{lead_id}/history
```

#### Test Notifications
```bash
# Get notifications
curl http://localhost:8003/nurturing/notifications

# Mark notification as read
curl -X PUT http://localhost:8003/nurturing/notifications/{id}/read \
  -H "Content-Type: application/json" \
  -d '{"is_read": true}'
```

### 3. API Documentation
Visit the interactive API documentation:
- **Swagger UI**: http://localhost:8003/docs
- **ReDoc**: http://localhost:8003/redoc

## 🔍 Monitoring and Debugging

### View Service Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f postgres
docker-compose logs -f redis
```

### Check Service Health
```bash
# Backend health
curl http://localhost:8003/health

# Database health
docker-compose exec postgres pg_isready -U admin -d real_estate_db

# Redis health
docker-compose exec redis redis-cli ping
```

### Database Inspection
```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U admin -d real_estate_db

# Check Blueprint 2.0 tables
\dt generated_documents
\dt notifications
\dt lead_history
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Conflicts
```bash
# Check what's using the ports
netstat -an | grep :8003
netstat -an | grep :3000

# Stop conflicting services or change ports in docker-compose.yml
```

#### 2. Memory Issues
```bash
# Increase Docker memory limit in Docker Desktop settings
# Recommended: 4GB minimum, 8GB preferred
```

#### 3. Database Connection Issues
```bash
# Reset database
docker-compose down -v
docker-compose up -d postgres
# Wait for postgres to be ready, then run migrations
```

#### 4. AI Model Issues
```bash
# Check API key is set correctly
docker-compose exec backend env | grep GOOGLE_API_KEY

# Test AI connection
docker-compose exec backend python -c "
import google.generativeai as genai
genai.configure(api_key='AIzaSyAocEBBwmq_eZ1Dy5RT9S7Kkfyw8nNibmM')
model = genai.GenerativeModel('gemini-pro')
print('AI connection successful')
"
```

### Performance Optimization

#### 1. Resource Limits
Add to `docker-compose.yml`:
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
```

#### 2. Caching
```bash
# Clear Redis cache if needed
docker-compose exec redis redis-cli FLUSHALL
```

## 📊 Test Results Interpretation

### Successful Test Indicators
- ✅ All services show "healthy" status
- ✅ Database migrations complete without errors
- ✅ Blueprint 2.0 tests pass (5/5)
- ✅ API endpoints respond correctly
- ✅ Document generation works
- ✅ Lead nurturing features functional

### Test Output Analysis
```bash
# View detailed test results
docker-compose --profile test run --rm test-runner

# Expected output:
# ✅ Database Schema: All tables created successfully
# ✅ Document Generator: HTML generation working
# ✅ Action Engine: Lead context and nurturing working
# ✅ Nurturing Scheduler: Background jobs working
# ✅ API Endpoints: All endpoints accessible
```

## 🔄 Development Workflow

### Making Changes
1. Edit code in your local directory
2. Changes are automatically reflected due to volume mounting
3. Restart specific service if needed:
   ```bash
   docker-compose restart backend
   ```

### Adding New Tests
1. Add test functions to `backend/test_blueprint_2.py`
2. Run tests:
   ```bash
   docker-compose --profile test run --rm test-runner
   ```

### Database Schema Changes
1. Update `backend/database_migrations.py`
2. Run migrations:
   ```bash
   docker-compose exec backend python database_migrations.py
   ```

## 🚀 Production Deployment

### Environment Variables
Create `.env` file with production values:
```bash
GOOGLE_API_KEY=your_production_key
REELLY_API_KEY=your_production_key
SECRET_KEY=your_production_secret
ENVIRONMENT=production
```

### Security Considerations
- Change default passwords
- Use production API keys
- Enable SSL/TLS
- Set up proper logging
- Configure backup strategies

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review service logs: `docker-compose logs -f`
3. Verify environment variables are set correctly
4. Ensure all prerequisites are met

## 🎯 Next Steps

After successful testing:
1. **Frontend Integration**: Connect frontend to Blueprint 2.0 APIs
2. **User Testing**: Test with real estate agents
3. **Performance Testing**: Load testing with multiple users
4. **Security Audit**: Review security measures
5. **Production Deployment**: Deploy to production environment

---

**Happy Testing! 🎉**
