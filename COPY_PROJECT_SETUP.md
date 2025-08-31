# Copy Project Setup - Different Ports Configuration

This document explains how to run the copy of the Real Estate Application using different ports and database names to avoid conflicts with the original project.

## Overview

This is a copy of the original Real Estate Application that uses different ports and database names to avoid conflicts when running both projects simultaneously.

## Port Configuration

### **Original Project Ports:**
- **Backend API**: `http://localhost:8001`
- **Frontend**: `http://localhost:3000`
- **PostgreSQL**: `localhost:5432`
- **Redis**: `localhost:6379`
- **ChromaDB**: `localhost:8002`

### **Copy Project Ports:**
- **Backend API**: `http://localhost:8002` ⭐
- **Frontend**: `http://localhost:3001` ⭐
- **PostgreSQL**: `localhost:5433` ⭐
- **Redis**: `localhost:6380` ⭐
- **ChromaDB**: `localhost:8004` ⭐

## Database Configuration

### **Original Project:**
- **Database Name**: `real_estate_db`
- **Database URL**: `postgresql://admin:password123@localhost:5432/real_estate_db`

### **Copy Project:**
- **Database Name**: `real_estate_db_copy` ⭐
- **Database URL**: `postgresql://admin:password123@localhost:5433/real_estate_db_copy` ⭐

## Quick Start

### **Option 1: Using Docker (Recommended)**

1. **Build and run the copy project:**
   ```bash
   docker-compose up --build
   ```

2. **Access the copy application:**
   - Backend API: http://localhost:8002
   - Frontend: http://localhost:3001
   - API Docs: http://localhost:8002/docs

### **Option 2: Manual Setup**

1. **Set environment variables:**
   ```bash
   export DATABASE_URL=postgresql://admin:password123@localhost:5433/real_estate_db_copy
   export REDIS_URL=redis://localhost:6380
   export CHROMA_HOST=localhost
   export CHROMA_PORT=8004
   ```

2. **Start the backend:**
   ```bash
   cd backend
   python -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload
   ```

3. **Start the frontend:**
   ```bash
   cd frontend
   npm start
   ```

## Configuration Files

### **Environment Variables (.env)**

Create a `.env` file based on `env.example`:

```bash
cp env.example .env
```

Key settings for the copy project:
```env
# Database Configuration (Different ports to avoid conflicts)
DATABASE_URL=postgresql://admin:password123@localhost:5433/real_estate_db_copy

# ChromaDB Configuration (Different port)
CHROMA_HOST=localhost
CHROMA_PORT=8004

# Redis Configuration (Different port)
REDIS_URL=redis://localhost:6380

# Server Configuration
HOST=0.0.0.0
PORT=8001
```

### **Docker Compose**

The `docker-compose.yml` file is configured with:
- Different host ports for all services
- Different database names
- Separate Docker volumes for data persistence

## Running Both Projects Simultaneously

You can run both the original and copy projects at the same time:

### **Original Project:**
```bash
# In original project directory
docker-compose up --build
# Access at: http://localhost:8001 (backend), http://localhost:3000 (frontend)
```

### **Copy Project:**
```bash
# In copy project directory
docker-compose up --build
# Access at: http://localhost:8002 (backend), http://localhost:3001 (frontend)
```

## Data Isolation

### **PostgreSQL:**
- **Original**: Database `real_estate_db` on port `5432`
- **Copy**: Database `real_estate_db_copy` on port `5433`
- **Data**: Completely separate, no conflicts

### **Redis:**
- **Original**: Port `6379`
- **Copy**: Port `6380`
- **Data**: Completely separate, no conflicts

### **ChromaDB:**
- **Original**: Port `8002`
- **Copy**: Port `8004`
- **Data**: Completely separate, no conflicts

### **Docker Volumes:**
- **Original**: `postgres_data`, `chroma_data`
- **Copy**: `postgres_data_copy`, `chroma_data_copy`
- **Data**: Completely separate, no conflicts

## API Endpoints

### **Copy Project API Endpoints:**
- **Base URL**: `http://localhost:8002`
- **Health Check**: `http://localhost:8002/health`
- **API Documentation**: `http://localhost:8002/docs`
- **ReDoc Documentation**: `http://localhost:8002/redoc`

### **Frontend Configuration:**
- **Base URL**: `http://localhost:3001`
- **API URL**: `http://localhost:8002` (configured in environment)

## Troubleshooting

### **Port Conflicts**

If you get port conflicts:

1. **Check if ports are in use:**
   ```bash
   # Windows
   netstat -ano | findstr :8002
   netstat -ano | findstr :3001
   netstat -ano | findstr :5433
   netstat -ano | findstr :6380
   netstat -ano | findstr :8004
   
   # Linux/Mac
   netstat -tulpn | grep :8002
   netstat -tulpn | grep :3001
   netstat -tulpn | grep :5433
   netstat -tulpn | grep :6380
   netstat -tulpn | grep :8004
   ```

2. **Kill processes using the ports:**
   ```bash
   # Windows
   taskkill /PID <PID> /F
   
   # Linux/Mac
   kill -9 <PID>
   ```

### **Database Connection Issues**

1. **Check if PostgreSQL is running:**
   ```bash
   docker ps | grep postgres
   ```

2. **Check database connection:**
   ```bash
   psql -h localhost -p 5433 -U admin -d real_estate_db_copy
   ```

### **Redis Connection Issues**

1. **Check if Redis is running:**
   ```bash
   docker ps | grep redis
   ```

2. **Test Redis connection:**
   ```bash
   redis-cli -h localhost -p 6380 ping
   ```

### **ChromaDB Connection Issues**

1. **Check if ChromaDB is running:**
   ```bash
   docker ps | grep chromadb
   ```

2. **Test ChromaDB connection:**
   ```bash
   curl http://localhost:8004/api/v1/heartbeat
   ```

## Development Workflow

### **Working with Both Projects:**

1. **Start original project:**
   ```bash
   cd /path/to/original/project
   docker-compose up -d
   ```

2. **Start copy project:**
   ```bash
   cd /path/to/copy/project
   docker-compose up -d
   ```

3. **Access applications:**
   - Original: http://localhost:3000 (frontend), http://localhost:8001 (backend)
   - Copy: http://localhost:3001 (frontend), http://localhost:8002 (backend)

4. **Stop projects:**
   ```bash
   # Stop original
   cd /path/to/original/project
   docker-compose down
   
   # Stop copy
   cd /path/to/copy/project
   docker-compose down
   ```

## Migration and Data Management

### **Copying Data Between Projects:**

1. **Export from original project:**
   ```bash
   # Export PostgreSQL data
   pg_dump -h localhost -p 5432 -U admin real_estate_db > original_backup.sql
   
   # Export Redis data (if needed)
   redis-cli -h localhost -p 6379 --rdb dump.rdb
   ```

2. **Import to copy project:**
   ```bash
   # Import PostgreSQL data
   psql -h localhost -p 5433 -U admin real_estate_db_copy < original_backup.sql
   
   # Import Redis data (if needed)
   redis-cli -h localhost -p 6380 --rdb dump.rdb
   ```

### **Backup and Restore:**

1. **Backup copy project data:**
   ```bash
   # PostgreSQL backup
   pg_dump -h localhost -p 5433 -U admin real_estate_db_copy > copy_backup.sql
   
   # Docker volumes backup
   docker run --rm -v copy_project_postgres_data_copy:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .
   ```

2. **Restore copy project data:**
   ```bash
   # PostgreSQL restore
   psql -h localhost -p 5433 -U admin real_estate_db_copy < copy_backup.sql
   
   # Docker volumes restore
   docker run --rm -v copy_project_postgres_data_copy:/data -v $(pwd):/backup alpine tar xzf /backup/postgres_backup.tar.gz -C /data
   ```

## Security Notes

- Each project has its own database with separate credentials
- API keys and secrets are isolated between projects
- Docker networks are separate for each project
- No data sharing between original and copy projects

## Support

For issues with the copy project setup:

1. Check the troubleshooting section above
2. Verify all ports are available
3. Ensure Docker is running
4. Check application logs for error messages
5. Verify environment variables are correctly set
