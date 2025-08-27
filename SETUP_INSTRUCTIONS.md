# 🚀 Complete Setup Instructions for RAG Web App

## 📋 **Prerequisites**

### **Required Software**
- **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **Docker Desktop** - [Download Docker](https://www.docker.com/products/docker-desktop/)
- **Git** - [Download Git](https://git-scm.com/)
- **PostgreSQL** - [Download PostgreSQL](https://www.postgresql.org/download/)
- **pgAdmin** - [Download pgAdmin](https://www.pgadmin.org/download/)

### **Required Accounts**
- **Google Cloud Console** - [Sign Up](https://console.cloud.google.com/)
- **GitHub** - [Sign Up](https://github.com/) (for deployment)
- **Vercel** - [Sign Up](https://vercel.com/) (frontend deployment)
- **Railway/Render** - [Sign Up](https://railway.app/) (backend deployment)

---

## 🛠️ **Local Development Setup**

### **1. Clone and Setup Project**

```bash
# Clone the repository
git clone <your-repo-url>
cd "RAG web app"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### **2. Environment Configuration**

```bash
# Copy environment template
copy env.example .env

# Edit .env file with your credentials
notepad .env
```

**Required Environment Variables:**
```env
# Database Configuration
DATABASE_URL=postgresql://admin:password123@localhost:5432/real_estate_db

# ChromaDB Configuration
CHROMA_HOST=localhost
CHROMA_PORT=8000

# Google AI Configuration
GOOGLE_API_KEY=your-google-api-key-here

# Reelly API Configuration
REELLY_API_KEY=your-reelly-api-key-here

# AI Model Configuration
AI_MODEL=gemini-1.5-flash

# Server Configuration
HOST=0.0.0.0
PORT=8001
DEBUG=True

# Authentication Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
BCRYPT_ROUNDS=12
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_LOGIN_ATTEMPTS=5

# Security Configuration
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Production Configuration
ENVIRONMENT=development
```

### **3. Database Setup**

#### **Option A: Local PostgreSQL**
```bash
# Install PostgreSQL locally
# Windows: Download from https://www.postgresql.org/download/windows/
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql postgresql-contrib

# Start PostgreSQL service
# Windows: PostgreSQL service should start automatically
# macOS: brew services start postgresql
# Ubuntu: sudo systemctl start postgresql

# Create database
psql -U postgres
CREATE DATABASE real_estate_db;
CREATE USER admin WITH PASSWORD 'password123';
GRANT ALL PRIVILEGES ON DATABASE real_estate_db TO admin;
\q
```

#### **Option B: Docker PostgreSQL**
```bash
# Run PostgreSQL in Docker
docker run --name postgres-db -e POSTGRES_PASSWORD=password123 -e POSTGRES_USER=admin -e POSTGRES_DB=real_estate_db -p 5432:5432 -d postgres:15
```

### **4. ChromaDB Setup**

#### **Option A: Local ChromaDB**
```bash
# Install ChromaDB
pip install chromadb

# Start ChromaDB server
chroma run --host localhost --port 8000
```

#### **Option B: Docker ChromaDB**
```bash
# Run ChromaDB in Docker
docker run -p 8000:8000 chromadb/chroma:latest
```

### **5. Google Cloud Setup**

1. **Go to [Google Cloud Console](https://console.cloud.google.com/)**
2. **Create a new project or select existing**
3. **Enable APIs:**
   - Go to "APIs & Services" > "Library"
   - Search and enable:
     - "Generative AI API"
     - "Vertex AI API"
4. **Create API Key:**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy the API key to your `.env` file

### **6. Reelly API Setup**

1. **Go to [Reelly](https://reelly.com/)**
2. **Sign up for an account**
3. **Navigate to API section**
4. **Generate API key**
5. **Add to your `.env` file**

---

## 🐳 **Docker Setup**

### **1. Build and Run with Docker Compose**

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### **2. Individual Docker Commands**

```bash
# Build backend image
docker build -t rag-backend ./backend

# Build frontend image
docker build -t rag-frontend ./frontend

# Run backend container
docker run -p 8001:8001 --env-file .env rag-backend

# Run frontend container
docker run -p 3000:3000 rag-frontend
```

---

## 🚀 **Running the Application**

### **1. Start Backend Server**

```bash
# Navigate to backend directory
cd backend

# Start FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Or using Python
python main.py
```

### **2. Start Frontend Development Server**

```bash
# Navigate to frontend directory
cd frontend

# Start React development server
npm start

# Or using yarn
yarn start
```

### **3. Access the Application**

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8001
- **API Documentation:** http://localhost:8001/docs
- **pgAdmin:** http://localhost:5050 (if using Docker)

---

## 🧪 **Testing**

### **1. Backend Tests**

```bash
# Navigate to backend directory
cd backend

# Run all tests
python -m pytest

# Run specific test file
python -m pytest test_rag.py

# Run with coverage
python -m pytest --cov=.
```

### **2. Frontend Tests**

```bash
# Navigate to frontend directory
cd frontend

# Run tests
npm test

# Run tests with coverage
npm test -- --coverage
```

### **3. Integration Tests**

```bash
# Run integration tests
python -m pytest tests/test_integration.py

# Run load tests
python -m pytest tests/test_load_testing.py
```

---

## 📊 **Monitoring and Logs**

### **1. Application Logs**

```bash
# View backend logs
tail -f logs/app.log

# View Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### **2. Database Monitoring**

```bash
# Connect to PostgreSQL
psql -U admin -d real_estate_db -h localhost

# View database logs
tail -f /var/log/postgresql/postgresql-*.log
```

### **3. ChromaDB Monitoring**

```bash
# Check ChromaDB status
curl http://localhost:8000/api/v1/heartbeat

# View ChromaDB logs
docker logs <chromadb-container-id>
```

---

## 🌐 **Deployment Setup**

### **1. Frontend Deployment (Vercel)**

1. **Go to [Vercel](https://vercel.com/)**
2. **Sign up/Login with GitHub**
3. **Import your repository**
4. **Configure build settings:**
   - **Framework Preset:** Create React App
   - **Build Command:** `npm run build`
   - **Output Directory:** `build`
   - **Install Command:** `npm install`
5. **Add Environment Variables:**
   - `REACT_APP_API_URL` = Your backend URL
6. **Deploy**

### **2. Backend Deployment (Railway/Render)**

#### **Option A: Railway**
1. **Go to [Railway](https://railway.app/)**
2. **Sign up/Login with GitHub**
3. **Create new project**
4. **Connect your repository**
5. **Add environment variables from your `.env` file**
6. **Deploy**

#### **Option B: Render**
1. **Go to [Render](https://render.com/)**
2. **Sign up/Login with GitHub**
3. **Create new Web Service**
4. **Connect your repository**
5. **Configure:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. **Add environment variables**
7. **Deploy**

### **3. Database Deployment**

#### **Option A: Railway PostgreSQL**
1. **In Railway dashboard, add PostgreSQL service**
2. **Copy connection string to environment variables**

#### **Option B: Supabase**
1. **Go to [Supabase](https://supabase.com/)**
2. **Create new project**
3. **Get connection string from Settings > Database**
4. **Update environment variables**

### **4. ChromaDB Deployment**

#### **Option A: Railway**
1. **Add ChromaDB service in Railway**
2. **Update environment variables**

#### **Option B: Self-hosted**
```bash
# Deploy ChromaDB to your server
docker run -d -p 8000:8000 --name chromadb chromadb/chroma:latest
```

### **5. Environment Variables for Production**

```env
# Production Environment Variables
DATABASE_URL=postgresql://user:password@host:port/database
CHROMA_HOST=your-chromadb-host
CHROMA_PORT=8000
GOOGLE_API_KEY=your-production-google-api-key
REELLY_API_KEY=your-production-reelly-api-key
JWT_SECRET_KEY=your-production-jwt-secret
SECRET_KEY=your-production-secret-key
ENVIRONMENT=production
DEBUG=False
```

---

## 🔧 **IDE Setup**

### **VS Code Configuration**

1. **Install Extensions:**
   - Python
   - JavaScript and TypeScript
   - Docker
   - PostgreSQL
   - GitLens
   - REST Client

2. **Workspace Settings** (`.vscode/settings.json`):
```json
{
    "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/node_modules": true
    }
}
```

3. **Launch Configuration** (`.vscode/launch.json`):
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": ["main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"],
            "cwd": "${workspaceFolder}/backend"
        },
        {
            "name": "React: Start",
            "type": "node",
            "request": "launch",
            "program": "${workspaceFolder}/frontend/node_modules/.bin/react-scripts",
            "args": ["start"],
            "cwd": "${workspaceFolder}/frontend"
        }
    ]
}
```

---

## 🚨 **Troubleshooting**

### **Common Issues**

1. **Port Already in Use:**
```bash
# Find process using port
netstat -ano | findstr :8001
# Kill process
taskkill /PID <process-id> /F
```

2. **Database Connection Issues:**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql
# Restart PostgreSQL
sudo systemctl restart postgresql
```

3. **ChromaDB Connection Issues:**
```bash
# Check ChromaDB status
curl http://localhost:8000/api/v1/heartbeat
# Restart ChromaDB
docker restart <chromadb-container-id>
```

4. **Environment Variables Not Loading:**
```bash
# Check if .env file exists
ls -la .env
# Verify environment variables
python -c "import os; print(os.getenv('DATABASE_URL'))"
```

### **Performance Optimization**

1. **Database Indexing:**
```sql
-- Add indexes for better performance
CREATE INDEX idx_properties_location ON properties(location);
CREATE INDEX idx_properties_price ON properties(price);
```

2. **ChromaDB Optimization:**
```python
# Configure ChromaDB for better performance
import chromadb
client = chromadb.Client(chromadb.config.Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_db"
))
```

---

## 📚 **Additional Resources**

- **FastAPI Documentation:** https://fastapi.tiangolo.com/
- **React Documentation:** https://reactjs.org/docs/
- **ChromaDB Documentation:** https://docs.trychroma.com/
- **Google AI Documentation:** https://ai.google.dev/
- **Docker Documentation:** https://docs.docker.com/
- **PostgreSQL Documentation:** https://www.postgresql.org/docs/

---

## ✅ **Verification Checklist**

- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed
- [ ] Docker Desktop installed
- [ ] PostgreSQL installed and running
- [ ] ChromaDB running
- [ ] Google Cloud API key configured
- [ ] Reelly API key configured
- [ ] Environment variables set
- [ ] Backend server running on port 8001
- [ ] Frontend server running on port 3000
- [ ] Database connection working
- [ ] ChromaDB connection working
- [ ] API endpoints responding
- [ ] Frontend loading correctly
- [ ] File upload working
- [ ] Chat functionality working
- [ ] Property management working

---

**🎉 Your RAG Web App is now ready to run!**
