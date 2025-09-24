# PropertyPro AI Setup & Deployment Guide
## Complete AURA Integration - Development to Production

**Version**: 1.0  
**Last Updated**: September 24, 2025  
**Status**: ✅ Production Ready

---

## 🎯 **Overview**

This comprehensive guide covers the complete setup and deployment process for PropertyPro AI with full AURA integration. From local development to production deployment, this guide ensures a smooth setup experience for both backend and frontend components.

### **What You'll Set Up**
- ✅ **AURA Backend**: 95+ API endpoints with enterprise-grade workflow automation
- ✅ **React Native Frontend**: Mobile-first app with complete AURA integration
- ✅ **Database**: PostgreSQL with comprehensive AURA schema
- ✅ **AI Services**: OpenAI integration with advanced orchestration
- ✅ **Monitoring**: Health checks, logging, and performance tracking

---

## 📋 **Prerequisites**

### **System Requirements**
```bash
# Required Software
- Node.js 18+ (LTS recommended)
- Python 3.11+
- PostgreSQL 15+
- Redis 6+ (optional, for caching)
- Docker & Docker Compose (recommended)
- Git

# Development Tools
- VS Code (recommended)
- Expo CLI (for React Native)
- Postman (for API testing)
```

### **API Keys & Services**
```bash
# Required API Keys
OPENAI_API_KEY=your_openai_api_key_here
JWT_SECRET=your_secure_jwt_secret_here
SECRET_KEY=your_secure_secret_key_here

# Optional Services
REDIS_URL=redis://localhost:6379/0
SENTRY_DSN=your_sentry_dsn_here (for error tracking)
```

### **Hardware Requirements**
```bash
# Minimum Requirements
- RAM: 8GB (16GB recommended)
- Storage: 20GB free space
- CPU: 4 cores (8 cores recommended)
- Internet: Stable connection for AI API calls

# Production Requirements
- RAM: 16GB minimum
- Storage: 100GB+ SSD
- CPU: 8+ cores
- Network: High-speed, low-latency connection
```

---

## 🚀 **Quick Start (Development)**

### **Option 1: Docker Setup (Recommended)**

```bash
# 1. Clone Repository
git clone <repository-url>
cd PropertyPro AI/Realtor-assistant

# 2. Environment Setup
cp env.example .env
# Edit .env with your configuration (see Environment Configuration section)

# 3. Start All Services
docker-compose up -d

# 4. Initialize Database
make db-migrate
make db-seed

# 5. Verify Installation
make health-check

# 6. Access Applications
# Backend API: http://localhost:8000
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

### **Option 2: Manual Setup**

```bash
# 1. Clone Repository
git clone <repository-url>
cd PropertyPro AI/Realtor-assistant

# 2. Backend Setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Database Setup
# Start PostgreSQL service
createdb propertypro_ai
export DATABASE_URL="postgresql://username:password@localhost/propertypro_ai"

# 4. Run Migrations
alembic upgrade head

# 5. Start Backend
uvicorn app.main:app --reload --port 8000

# 6. Frontend Setup (New Terminal)
cd ../frontend
npm install
npm start

# 7. Start React Native App (New Terminal)
cd ../frontend
npx expo start
```

---

## ⚙️ **Environment Configuration**

### **Backend Environment (.env)**
```bash
# ============================================================================
# Core Application Settings
# ============================================================================
APP_NAME=PropertyPro AI
APP_VERSION=1.0.0
DEBUG=true
ENVIRONMENT=development

# ============================================================================
# Database Configuration
# ============================================================================
DATABASE_URL=postgresql://username:password@localhost:5432/propertypro_ai
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=30
DB_ECHO=false

# ============================================================================
# Security & Authentication
# ============================================================================
SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_SECRET=your-jwt-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# ============================================================================
# AURA Configuration
# ============================================================================
AURA_ENABLED=true
AURA_LOG_LEVEL=INFO
AURA_MAX_CONCURRENT_WORKFLOWS=25
AURA_TASK_QUEUE_SIZE=1000

# ============================================================================
# AI Services Configuration
# ============================================================================
OPENAI_API_KEY=your-openai-api-key-here
AI_MODEL_PRIMARY=gpt-4
AI_MODEL_FALLBACK=gpt-3.5-turbo
AI_REQUEST_TIMEOUT=30
AI_MAX_RETRIES=3
AI_REQUEST_RATE_LIMIT=60

# ============================================================================
# Redis Configuration (Optional)
# ============================================================================
REDIS_URL=redis://localhost:6379/0
REDIS_TASK_QUEUE_KEY=AURA:tasks
REDIS_CACHE_TTL=3600

# ============================================================================
# File Storage Configuration
# ============================================================================
FILE_STORAGE_PROVIDER=local
FILE_STORAGE_PATH=/var/uploads/AURA
FILE_STORAGE_MAX_SIZE=100MB
FILE_STORAGE_ALLOWED_TYPES=pdf,jpg,jpeg,png,doc,docx

# ============================================================================
# Monitoring & Logging
# ============================================================================
MONITORING_ENABLED=true
LOG_LEVEL=INFO
METRICS_EXPORT_INTERVAL=60
HEALTH_CHECK_INTERVAL=30
SENTRY_DSN=your-sentry-dsn-here

# ============================================================================
# CORS Configuration
# ============================================================================
CORS_ORIGINS=http://localhost:3000,http://localhost:19006,http://localhost:8081
CORS_ALLOW_CREDENTIALS=true
CORS_METHODS=GET,POST,PUT,DELETE,OPTIONS
CORS_HEADERS=*

# ============================================================================
# Email Configuration (Optional)
# ============================================================================
EMAIL_ENABLED=false
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### **Frontend Environment (.env)**
```bash
# ============================================================================
# API Configuration
# ============================================================================
EXPO_PUBLIC_API_URL=http://localhost:8000
EXPO_PUBLIC_WS_URL=ws://localhost:8000
API_TIMEOUT=30000

# ============================================================================
# AURA Configuration
# ============================================================================
EXPO_PUBLIC_AURA_ENABLED=true
EXPO_PUBLIC_AURA_POLLING_INTERVAL=5000
EXPO_PUBLIC_AURA_MAX_RETRIES=3

# ============================================================================
# App Configuration
# ============================================================================
EXPO_PUBLIC_APP_NAME=PropertyPro AI
EXPO_PUBLIC_APP_VERSION=1.0.0
EXPO_PUBLIC_ENVIRONMENT=development

# ============================================================================
# Feature Flags
# ============================================================================
EXPO_PUBLIC_ENABLE_ANALYTICS=true
EXPO_PUBLIC_ENABLE_CRASH_REPORTING=true
EXPO_PUBLIC_ENABLE_OFFLINE_MODE=false

# ============================================================================
# Debugging
# ============================================================================
EXPO_PUBLIC_DEBUG=true
EXPO_PUBLIC_LOG_LEVEL=info
```

---

## 🗄️ **Database Setup**

### **PostgreSQL Installation**

#### **macOS (Homebrew)**
```bash
# Install PostgreSQL
brew install postgresql@15
brew services start postgresql@15

# Create database and user
createdb propertypro_ai
psql -d postgres -c "CREATE USER propertypro WITH PASSWORD 'your_password';"
psql -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE propertypro_ai TO propertypro;"
```

#### **Ubuntu/Debian**
```bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql-15 postgresql-contrib

# Start service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres createdb propertypro_ai
sudo -u postgres psql -c "CREATE USER propertypro WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE propertypro_ai TO propertypro;"
```

#### **Windows**
```powershell
# Download and install PostgreSQL from official website
# https://www.postgresql.org/download/windows/

# Using pgAdmin or psql, create database:
CREATE DATABASE propertypro_ai;
CREATE USER propertypro WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE propertypro_ai TO propertypro;
```

### **Database Migration & Seeding**

```bash
# Navigate to backend directory
cd backend

# Run database migrations (creates all AURA tables)
alembic upgrade head

# Seed with sample data (optional for development)
python scripts/seed_sample_data.py

# Verify migration success
psql -d propertypro_ai -c "\dt"  # List all tables

# Should show 25+ tables including:
# - marketing_campaigns
# - marketing_templates  
# - workflow_packages
# - package_executions
# - cma_reports
# - social_media_posts
# - And many more...
```

### **Database Schema Verification**

```sql
-- Connect to database
psql -d propertypro_ai

-- Verify AURA tables exist
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' AND table_name LIKE '%marketing%';

-- Check workflow packages are seeded
SELECT package_name, display_name, estimated_duration 
FROM workflow_packages;

-- Verify marketing templates
SELECT template_name, category, market, compliance_status 
FROM marketing_templates;

-- Check system is ready
SELECT 'Database Ready' as status;
```

---

## 🔧 **Backend Setup (Detailed)**

### **Python Environment Setup**

```bash
# 1. Create virtual environment
cd backend
python3.11 -m venv venv

# 2. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Verify installation
python -c "import fastapi, sqlalchemy, alembic; print('All dependencies installed successfully')"
```

### **AURA Backend Configuration**

```bash
# 1. Verify AURA routers are registered
cd backend
python -c "
from app.main import app
print('Registered routes:')
for route in app.routes:
    if hasattr(route, 'path'):
        print(f'  {route.methods} {route.path}')
"

# 2. Test database connection
python -c "
from app.core.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text('SELECT 1'))
    print('Database connection successful')
"

# 3. Verify AI service configuration
python -c "
import openai
from app.core.settings import settings
print(f'OpenAI API configured: {bool(settings.OPENAI_API_KEY)}')
"
```

### **Start Backend Services**

```bash
# Method 1: Development server (recommended for development)
cd backend
uvicorn app.main:app --reload --port 8000 --host 0.0.0.0

# Method 2: Production server
cd backend
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Method 3: Using make commands
make run-api

# Verify backend is running
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/analytics/health/system
```

---

## 📱 **Frontend Setup (Detailed)**

### **React Native Environment Setup**

```bash
# 1. Install Node.js dependencies
cd frontend
npm install

# 2. Install Expo CLI globally
npm install -g @expo/cli

# 3. Install iOS Simulator (macOS only)
xcode-select --install

# 4. Install Android Studio (for Android development)
# Download from: https://developer.android.com/studio

# 5. Verify Expo setup
expo doctor
```

### **AURA Frontend Configuration**

```bash
# 1. Verify AURA API service is configured
cd frontend/src/services
cat AURA.ts | head -20

# 2. Test API connectivity
node -e "
const { AURAAPI } = require('./src/services/AURA.ts');
AURAAPI.config.baseURL = 'http://localhost:8000';
console.log('AURA API service configured successfully');
"

# 3. Verify TypeScript compilation
npm run type-check
```

### **Start Frontend Services**

```bash
# Method 1: Start Expo development server
cd frontend
npm start
# or
expo start

# Method 2: Start specific platform
npm run ios     # iOS Simulator
npm run android # Android Emulator
npm run web     # Web browser

# Method 3: Using make commands
make run-frontend

# Access the application
# Expo DevTools: http://localhost:19002
# Web version: http://localhost:19006
# Mobile: Scan QR code with Expo Go app
```

---

## 🐳 **Docker Deployment**

### **Development with Docker**

```bash
# 1. Build and start all services
docker-compose up -d

# 2. Check service status
docker-compose ps

# 3. View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# 4. Run database migrations
docker-compose exec backend alembic upgrade head

# 5. Access services
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# Database: localhost:5432
```

### **Production Docker Setup**

```yaml
# docker-compose.production.yml
version: '3.8'

services:
  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile.production
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - DEBUG=false
      - DATABASE_URL=postgresql://user:pass@db:5432/propertypro_ai
    depends_on:
      - db
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=propertypro_ai
      - POSTGRES_USER=propertypro
      - POSTGRES_PASSWORD=secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backend/database/init.sql:/docker-entrypoint-initdb.d/init.sql

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl/certs
    depends_on:
      - backend

volumes:
  postgres_data:
  redis_data:
```

```bash
# Deploy to production
docker-compose -f docker-compose.production.yml up -d

# Monitor production services
docker-compose -f docker-compose.production.yml logs -f

# Scale backend for load balancing
docker-compose -f docker-compose.production.yml up -d --scale backend=3
```

---

## 🌐 **Production Deployment**

### **Server Setup (Ubuntu 22.04)**

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install required packages
sudo apt install -y python3.11 python3.11-venv postgresql-15 redis-server nginx certbot

# 3. Create application user
sudo useradd -m -s /bin/bash propertypro
sudo usermod -aG sudo propertypro

# 4. Setup application directory
sudo mkdir -p /opt/propertypro
sudo chown propertypro:propertypro /opt/propertypro
```

### **Backend Production Setup**

```bash
# 1. Deploy code
cd /opt/propertypro
git clone <repository-url> .
cd backend

# 2. Setup Python environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Setup environment
cp ../env.production .env
# Edit .env with production values

# 4. Run database migrations
alembic upgrade head

# 5. Setup systemd service
sudo tee /etc/systemd/system/propertypro-backend.service > /dev/null <<EOF
[Unit]
Description=PropertyPro AI Backend
After=network.target postgresql.service

[Service]
Type=exec
User=propertypro
WorkingDirectory=/opt/propertypro/backend
Environment=PATH=/opt/propertypro/backend/venv/bin
ExecStart=/opt/propertypro/backend/venv/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# 6. Start backend service
sudo systemctl daemon-reload
sudo systemctl enable propertypro-backend
sudo systemctl start propertypro-backend

# 7. Verify backend is running
sudo systemctl status propertypro-backend
curl http://localhost:8000/health
```

### **Frontend Production Build**

```bash
# 1. Build React Native Web
cd frontend
npm run build

# 2. Setup Nginx configuration
sudo tee /etc/nginx/sites-available/propertypro > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;
    
    # Frontend static files
    location / {
        root /opt/propertypro/frontend/dist;
        try_files \$uri \$uri/ /index.html;
        
        # Enable gzip compression
        gzip on;
        gzip_types text/css application/javascript application/json;
    }
    
    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
    
    # WebSocket support
    location /ws/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# 3. Enable site and restart Nginx
sudo ln -s /etc/nginx/sites-available/propertypro /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 4. Setup SSL certificate
sudo certbot --nginx -d your-domain.com
```

### **Mobile App Deployment**

```bash
# 1. Build for iOS (macOS required)
cd frontend
eas build --platform ios --profile production

# 2. Build for Android
eas build --platform android --profile production

# 3. Submit to App Stores
eas submit --platform ios
eas submit --platform android

# 4. Over-the-Air Updates
eas update --branch production --message "AURA integration update"
```

---

## 📊 **Monitoring & Health Checks**

### **System Health Monitoring**

```bash
# 1. Setup health check endpoints
curl -s http://localhost:8000/health | jq
curl -s http://localhost:8000/api/v1/analytics/health/system | jq

# 2. Database health check
psql -d propertypro_ai -c "
SELECT 
    'Database' as component,
    CASE WHEN COUNT(*) > 20 THEN 'Healthy' ELSE 'Unhealthy' END as status
FROM information_schema.tables 
WHERE table_schema = 'public';
"

# 3. Redis health check (if using)
redis-cli ping

# 4. Check AURA workflow system
curl -s http://localhost:8000/api/v1/workflows/packages/templates | jq '.workflow_packages | length'
```

### **Performance Monitoring**

```bash
# 1. Setup Prometheus metrics (optional)
# Add to requirements.txt: prometheus-fastapi-instrumentator
pip install prometheus-fastapi-instrumentator

# 2. Monitor API response times
curl -w "%{time_total}" -s -o /dev/null http://localhost:8000/api/v1/analytics/dashboard/overview

# 3. Check workflow execution performance
curl -s http://localhost:8000/api/v1/workflows/packages/history | jq '.summary'

# 4. Monitor database connections
psql -d propertypro_ai -c "
SELECT count(*) as active_connections 
FROM pg_stat_activity 
WHERE state = 'active';
"
```

### **Log Monitoring**

```bash
# 1. Check application logs
sudo journalctl -u propertypro-backend -f

# 2. Monitor AURA workflow logs
tail -f /var/log/AURA/application.log

# 3. Check error logs
sudo journalctl -u propertypro-backend --since "1 hour ago" | grep ERROR

# 4. Monitor database logs
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

---

## 🧪 **Testing the Setup**

### **Backend API Testing**

```bash
# 1. Health checks
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/analytics/health/system

# 2. Authentication test
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpassword"}'

# 3. AURA workflow templates
curl http://localhost:8000/api/v1/workflows/packages/templates

# 4. Marketing templates
curl http://localhost:8000/api/v1/marketing/templates?market=dubai

# 5. Analytics dashboard
curl http://localhost:8000/api/v1/analytics/dashboard/overview
```

### **Frontend Testing**

```bash
# 1. Start frontend and test navigation
npm start

# 2. Test AURA API integration
# Open browser developer tools and check network requests

# 3. Test workflow execution
# Navigate to Workflows tab and execute a test workflow

# 4. Test dashboard analytics
# Navigate to Dashboard and verify data loads from AURA APIs
```

### **End-to-End Testing**

```bash
# 1. Create test property
curl -X POST http://localhost:8000/api/properties \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Dubai Marina Property",
    "location": "Dubai Marina",
    "bedrooms": 2,
    "bathrooms": 2,
    "price": 2500000
  }'

# 2. Execute workflow package
curl -X POST http://localhost:8000/api/v1/workflows/packages/execute \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "package_name": "new_listing_package",
    "parameters": {
      "property_id": "test_prop_123",
      "listing_price": 2500000,
      "marketing_budget": 5000
    }
  }'

# 3. Track workflow progress
curl http://localhost:8000/api/v1/workflows/packages/status/EXECUTION_ID

# 4. Generate CMA report
curl -X POST http://localhost:8000/api/v1/cma/reports \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "subject_property": {
      "address": "Dubai Marina, Marina Heights Tower",
      "bedrooms": 2,
      "bathrooms": 2,
      "area_sqft": 1200,
      "property_type": "apartment"
    },
    "analysis_options": {
      "comparable_count": 6,
      "radius_km": 2.0,
      "time_frame_months": 12,
      "include_market_trends": true
    }
  }'
```

---

## 🔧 **Troubleshooting**

### **Common Issues & Solutions**

#### **Backend Issues**

```bash
# Issue: Database connection failed
# Solution: Check PostgreSQL service and credentials
sudo systemctl status postgresql
psql -d propertypro_ai -c "SELECT 1;"

# Issue: Migration failed
# Solution: Reset and re-run migrations
alembic downgrade base
alembic upgrade head

# Issue: OpenAI API errors
# Solution: Verify API key and test connection
python -c "
import openai
openai.api_key = 'your-key'
try:
    response = openai.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': 'test'}],
        max_tokens=10
    )
    print('OpenAI API working')
except Exception as e:
    print(f'OpenAI API error: {e}')
"

# Issue: AURA endpoints not found
# Solution: Verify router registration
python -c "
from app.main import app
AURA_routes = [route.path for route in app.routes if '/api/v1/' in str(route.path)]
print(f'AURA routes: {len(AURA_routes)}')
print('\\n'.join(AURA_routes[:10]))
"
```

#### **Frontend Issues**

```bash
# Issue: Expo app won't start
# Solution: Clear cache and restart
npx expo start --clear

# Issue: API connection failed
# Solution: Check API URL and network connectivity
curl http://localhost:8000/health

# Issue: React Native build errors
# Solution: Clear node_modules and reinstall
rm -rf node_modules
npm install

# Issue: iOS Simulator not opening
# Solution: Reset iOS Simulator
xcrun simctl erase all
```

#### **Database Issues**

```bash
# Issue: Too many database connections
# Solution: Check and adjust connection pool settings
psql -d propertypro_ai -c "
SELECT count(*) as total_connections, 
       count(*) FILTER (WHERE state = 'active') as active_connections
FROM pg_stat_activity;
"

# Issue: AURA tables missing
# Solution: Re-run specific migrations
alembic upgrade 004_aura_core_entities
alembic upgrade 005_seed_aura_data

# Issue: Slow query performance
# Solution: Check indexes and analyze queries
psql -d propertypro_ai -c "
SELECT schemaname, tablename, indexname 
FROM pg_indexes 
WHERE schemaname = 'public' 
ORDER BY tablename;
"
```

#### **Production Issues**

```bash
# Issue: High CPU usage
# Solution: Monitor and adjust worker processes
htop
# Adjust gunicorn workers: -w 2 (reduce if high CPU)

# Issue: Memory leaks
# Solution: Monitor memory usage and restart services
free -h
sudo systemctl restart propertypro-backend

# Issue: SSL certificate expired
# Solution: Renew Let's Encrypt certificate
sudo certbot renew

# Issue: Nginx serving 502 errors
# Solution: Check backend service and proxy settings
sudo systemctl status propertypro-backend
sudo nginx -t
```

---

## 📈 **Performance Optimization**

### **Backend Optimization**

```python
# 1. Database Query Optimization
# Use SQLAlchemy query optimization techniques
from sqlalchemy.orm import selectinload, joinedload

# Example optimized query
def get_marketing_campaigns_optimized():
    return db.query(MarketingCampaign)\
        .options(
            selectinload(MarketingCampaign.assets),
            joinedload(MarketingCampaign.property)
        )\
        .limit(50)\
        .all()

# 2. Redis Caching Implementation
import redis
import json

class AURACache:
    def __init__(self):
        self.redis = redis.Redis.from_url(settings.REDIS_URL)
    
    async def get_cma_report(self, property_key: str):
        cached = await self.redis.get(f"cma:{property_key}")
        return json.loads(cached) if cached else None
    
    async def set_cma_report(self, property_key: str, data: dict):
        await self.redis.setex(
            f"cma:{property_key}", 
            3600,  # 1 hour TTL
            json.dumps(data)
        )

# 3. Async Processing for Heavy Tasks
from celery import Celery

celery_app = Celery('AURA_tasks')

@celery_app.task
def generate_marketing_package(property_id: str):
    # Heavy workflow processing in background
    pass
```

### **Frontend Optimization**

```typescript
// 1. React Native Performance Optimizations
import { useMemo, useCallback, memo } from 'react';

// Memoized component
const WorkflowCard = memo(({ workflow, onExecute }) => {
  const handleExecute = useCallback(() => {
    onExecute(workflow.package_name);
  }, [workflow.package_name, onExecute]);

  return (
    <Card>
      <Text>{workflow.display_name}</Text>
      <Button onPress={handleExecute} />
    </Card>
  );
});

// 2. API Response Caching
import AsyncStorage from '@react-native-async-storage/async-storage';

class CacheManager {
  async getCachedData(key: string) {
    try {
      const cached = await AsyncStorage.getItem(key);
      if (cached) {
        const { data, timestamp } = JSON.parse(cached);
        if (Date.now() - timestamp < 300000) { // 5 min TTL
          return data;
        }
      }
    } catch (error) {
      console.error('Cache read error:', error);
    }
    return null;
  }

  async setCachedData(key: string, data: any) {
    try {
      await AsyncStorage.setItem(key, JSON.stringify({
        data,
        timestamp: Date.now()
      }));
    } catch (error) {
      console.error('Cache write error:', error);
    }
  }
}

// 3. Optimized API Polling
const useOptimizedPolling = (executionIds: string[]) => {
  const [statuses, setStatuses] = useState({});
  
  useEffect(() => {
    if (executionIds.length === 0) return;
    
    const poll = async () => {
      // Batch API calls for efficiency
      const promises = executionIds.map(id => 
        AURAAPI.getWorkflowStatus(id).catch(err => ({ error: err }))
      );
      
      const results = await Promise.all(promises);
      const newStatuses = {};
      
      results.forEach((result, index) => {
        if (!result.error) {
          newStatuses[executionIds[index]] = result;
        }
      });
      
      setStatuses(prev => ({ ...prev, ...newStatuses }));
    };
    
    const interval = setInterval(poll, 5000);
    poll(); // Initial call
    
    return () => clearInterval(interval);
  }, [executionIds]);
  
  return statuses;
};
```

---

## 🔒 **Security Configuration**

### **Backend Security**

```python
# 1. Enhanced CORS Configuration
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count"]
)

# 2. Rate Limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/v1/marketing/templates")
@limiter.limit("100/minute")
async def get_templates(request: Request):
    pass

# 3. Input Validation & Sanitization
from pydantic import BaseModel, validator
import bleach

class WorkflowRequest(BaseModel):
    package_name: str
    parameters: dict
    
    @validator('package_name')
    def sanitize_package_name(cls, v):
        return bleach.clean(v.strip())
    
    @validator('parameters')
    def validate_parameters(cls, v):
        # Validate parameter types and ranges
        if 'listing_price' in v:
            price = float(v['listing_price'])
            if not 100000 <= price <= 100000000:  # AED range
                raise ValueError("Invalid listing price range")
        return v

# 4. Security Headers
from fastapi.security import HTTPBearer
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Add security headers
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*.yourdomain.com"])

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

### **Frontend Security**

```typescript
// 1. Secure Token Storage
import * as SecureStore from 'expo-secure-store';

class SecureTokenManager {
  private static TOKEN_KEY = 'auth_token';
  
  static async saveToken(token: string): Promise<void> {
    await SecureStore.setItemAsync(this.TOKEN_KEY, token);
  }
  
  static async getToken(): Promise<string | null> {
    return await SecureStore.getItemAsync(this.TOKEN_KEY);
  }
  
  static async deleteToken(): Promise<void> {
    await SecureStore.deleteItemAsync(this.TOKEN_KEY);
  }
}

// 2. API Request Interceptors
import axios, { AxiosError } from 'axios';

const apiClient = axios.create({
  baseURL: process.env.EXPO_PUBLIC_API_URL,
  timeout: 30000,
});

// Request interceptor for auth token
apiClient.interceptors.request.use(async (config) => {
  const token = await SecureTokenManager.getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    if (error.response?.status === 401) {
      await SecureTokenManager.deleteToken();
      // Redirect to login
    }
    return Promise.reject(error);
  }
);

// 3. Input Sanitization
import DOMPurify from 'isomorphic-dompurify';

const sanitizeInput = (input: string): string => {
  return DOMPurify.sanitize(input.trim());
};

// 4. Certificate Pinning (Production)
const trustKit = {
  'your-api-domain.com': {
    certificateChainValidation: true,
    caPinSet: [
      'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=', // Your certificate pin
    ],
  },
};
```

---

## 📋 **Maintenance Tasks**

### **Daily Maintenance**

```bash
#!/bin/bash
# daily_maintenance.sh

# 1. Check system health
curl -s http://localhost:8000/api/v1/analytics/health/system | jq '.system_status'

# 2. Monitor disk space
df -h

# 3. Check database connections
psql -d propertypro_ai -c "SELECT count(*) FROM pg_stat_activity;"

# 4. Check error logs
sudo journalctl -u propertypro-backend --since "24 hours ago" | grep ERROR | wc -l

# 5. Backup database
pg_dump propertypro_ai > /backups/$(date +%Y%m%d)_propertypro_ai.sql

# 6. Clean up old workflow executions (older than 30 days)
psql -d propertypro_ai -c "
DELETE FROM workflow_steps 
WHERE execution_id IN (
  SELECT execution_id FROM package_executions 
  WHERE completed_at < NOW() - INTERVAL '30 days' 
  AND status = 'completed'
);
"
```

### **Weekly Maintenance**

```bash
#!/bin/bash
# weekly_maintenance.sh

# 1. Update database statistics
psql -d propertypro_ai -c "ANALYZE;"

# 2. Vacuum database
psql -d propertypro_ai -c "VACUUM ANALYZE;"

# 3. Check for database index usage
psql -d propertypro_ai -c "
SELECT schemaname, tablename, attname, n_distinct, correlation 
FROM pg_stats 
WHERE schemaname = 'public' 
ORDER BY n_distinct DESC LIMIT 20;
"

# 4. Archive old marketing campaigns
psql -d propertypro_ai -c "
UPDATE marketing_campaigns 
SET status = 'archived' 
WHERE created_at < NOW() - INTERVAL '90 days' 
AND status = 'completed';
"

# 5. Clean Redis cache (if using)
redis-cli FLUSHDB

# 6. Update system packages
sudo apt update && sudo apt upgrade -y
```

### **Monthly Maintenance**

```bash
#!/bin/bash
# monthly_maintenance.sh

# 1. Full database backup
pg_dump -Fc propertypro_ai > /backups/monthly/$(date +%Y%m)_propertypro_ai.backup

# 2. Check SSL certificate expiration
openssl x509 -in /etc/ssl/certs/your-domain.crt -text -noout | grep "Not After"

# 3. Audit user access and permissions
psql -d propertypro_ai -c "
SELECT u.email, r.name as role, u.last_login 
FROM users u 
JOIN roles r ON u.role_id = r.id 
ORDER BY u.last_login DESC;
"

# 4. Performance analysis
psql -d propertypro_ai -c "
SELECT query, calls, total_time, mean_time 
FROM pg_stat_statements 
ORDER BY total_time DESC LIMIT 10;
"

# 5. Security audit log review
grep "FAILED LOGIN" /var/log/auth.log | tail -50

# 6. Clean up old log files
find /var/log -name "*.log" -mtime +30 -delete
```

---

## 🎉 **Conclusion**

You now have a comprehensive setup guide for PropertyPro AI with complete AURA integration. This guide covers everything from initial development setup to production deployment, monitoring, and maintenance.

### **What You've Accomplished**

✅ **Complete Development Environment**: Backend and frontend with full AURA integration  
✅ **Production-Ready Deployment**: Docker, systemd services, and Nginx configuration  
✅ **Security Implementation**: Authentication, HTTPS, input validation, and secure storage  
✅ **Monitoring & Logging**: Health checks, performance monitoring, and error tracking  
✅ **Maintenance Procedures**: Daily, weekly, and monthly maintenance scripts  

### **Next Steps**

1. **User Acceptance Testing**: Test all AURA workflows with real users
2. **Performance Optimization**: Monitor and optimize based on production usage
3. **Scaling**: Plan for horizontal scaling as user base grows
4. **Feature Enhancement**: Add new AURA workflow packages based on user feedback

### **Support Resources**

- **API Documentation**: http://localhost:8000/docs
- **Health Monitoring**: http://localhost:8000/api/v1/analytics/health/system
- **Log Files**: `/var/log/AURA/` and `journalctl -u propertypro-backend`

**PropertyPro AI with AURA integration is now ready for production deployment and will provide Dubai real estate professionals with enterprise-grade AI workflow automation.**

---

**PropertyPro AI Setup Guide** - From Development to Production with Complete AURA Integration
