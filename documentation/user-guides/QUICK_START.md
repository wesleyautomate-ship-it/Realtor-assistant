# ⚡ Quick Start Guide

## 🚀 **Essential Commands**

### **1. Start Everything (Docker)**
```bash
# Start all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### **2. Start Everything (Local)**
```bash
# Terminal 1: Start PostgreSQL
# Windows: PostgreSQL service should be running
# macOS: brew services start postgresql
# Linux: sudo systemctl start postgresql

# Terminal 2: Start ChromaDB
docker run -p 8000:8000 chromadb/chroma:latest

# Terminal 3: Start Backend
cd backend
uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Terminal 4: Start Frontend
cd frontend
npm start
```

### **3. Environment Setup**
```bash
# Copy environment template
copy env.example .env

# Edit with your credentials
notepad .env
```

### **4. Database Setup**
```bash
# Create database
psql -U postgres
CREATE DATABASE real_estate_db;
CREATE USER admin WITH PASSWORD 'password123';
GRANT ALL PRIVILEGES ON DATABASE real_estate_db TO admin;
\q
```

## 🌐 **Access URLs**

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8001
- **API Docs:** http://localhost:8001/docs
- **pgAdmin:** http://localhost:5050

## 🔑 **Required API Keys**

1. **Google Cloud Console** → APIs & Services → Credentials → Create API Key
2. **Reelly** → Sign up → Get API key
3. **Add both to `.env` file**

## 🐳 **Docker Commands**

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

## 🧪 **Testing**

```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

## 🚨 **Troubleshooting**

```bash
# Check if ports are in use
netstat -ano | findstr :8001
netstat -ano | findstr :3000

# Kill process on port
taskkill /PID <process-id> /F

# Check Docker containers
docker ps
docker logs <container-id>
```

## 📋 **Checklist**

- [ ] `.env` file created with API keys
- [ ] PostgreSQL running
- [ ] ChromaDB running
- [ ] Backend server on port 8001
- [ ] Frontend server on port 3000
- [ ] Can access http://localhost:3000
- [ ] Can access http://localhost:8001/docs

**🎯 Ready to go!**
