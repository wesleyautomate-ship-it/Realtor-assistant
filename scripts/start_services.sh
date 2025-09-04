#!/bin/bash
"""
Docker Services Startup Script
Ensures proper startup order and health checks for all services
"""

set -e

echo "🚀 Starting RAG System Services..."
echo "=================================="

# Function to wait for service health
wait_for_service() {
    local service_name=$1
    local health_url=$2
    local max_attempts=30
    local attempt=1
    
    echo "⏳ Waiting for $service_name to be healthy..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f "$health_url" >/dev/null 2>&1; then
            echo "✅ $service_name is healthy!"
            return 0
        fi
        
        echo "⏳ Attempt $attempt/$max_attempts - $service_name not ready yet..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "❌ $service_name failed to become healthy after $max_attempts attempts"
    return 1
}

# Start PostgreSQL
echo "📦 Starting PostgreSQL..."
docker-compose up -d postgres
wait_for_service "PostgreSQL" "http://localhost:5432"

# Start Redis
echo "📦 Starting Redis..."
docker-compose up -d redis
wait_for_service "Redis" "http://localhost:6379"

# Start ChromaDB
echo "📦 Starting ChromaDB..."
docker-compose up -d chromadb
wait_for_service "ChromaDB" "http://localhost:8002/api/v1/heartbeat"

# Start Backend
echo "📦 Starting Backend..."
docker-compose up -d backend
wait_for_service "Backend" "http://localhost:8003/health"

# Start Frontend
echo "📦 Starting Frontend..."
docker-compose up -d frontend
wait_for_service "Frontend" "http://localhost:3000"

echo ""
echo "🎉 All services started successfully!"
echo "=================================="
echo "📊 Service Status:"
echo "  PostgreSQL: http://localhost:5432"
echo "  Redis: http://localhost:6379"
echo "  ChromaDB: http://localhost:8002"
echo "  Backend API: http://localhost:8003"
echo "  Frontend: http://localhost:3000"
echo ""
echo "📚 API Documentation: http://localhost:8003/docs"
echo "🔍 Health Check: http://localhost:8003/health"
echo ""

# Run connection tests
echo "🧪 Running connection tests..."
python scripts/test_connections.py

echo ""
echo "✨ RAG System is ready to use!"
