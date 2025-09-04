@echo off
REM Simple Docker Services Startup Script for Windows
REM Starts services in order with basic checks

echo 🚀 Starting RAG System Services...
echo ==================================

REM Start PostgreSQL
echo 📦 Starting PostgreSQL...
docker-compose up -d postgres
timeout /t 10 /nobreak >nul
echo ✅ PostgreSQL started

REM Start Redis
echo 📦 Starting Redis...
docker-compose up -d redis
timeout /t 5 /nobreak >nul
echo ✅ Redis started

REM Start ChromaDB
echo 📦 Starting ChromaDB...
docker-compose up -d chromadb
timeout /t 15 /nobreak >nul
echo ✅ ChromaDB started

REM Start Backend
echo 📦 Starting Backend...
docker-compose up -d backend
timeout /t 10 /nobreak >nul
echo ✅ Backend started

REM Start Frontend
echo 📦 Starting Frontend...
docker-compose up -d frontend
timeout /t 5 /nobreak >nul
echo ✅ Frontend started

echo.
echo 🎉 All services started!
echo ==================================
echo 📊 Service Status:
echo   PostgreSQL: http://localhost:5432
echo   Redis: http://localhost:6379
echo   ChromaDB: http://localhost:8002
echo   Backend API: http://localhost:8003
echo   Frontend: http://localhost:3000
echo.
echo 📚 API Documentation: http://localhost:8003/docs
echo 🔍 Health Check: http://localhost:8003/health
echo.

REM Check if services are running
echo 🔍 Checking service status...
docker-compose ps

echo.
echo ✨ RAG System is ready to use!
echo.
echo 💡 If services aren't healthy, wait a few minutes and check:
echo    docker-compose logs backend
echo    docker-compose logs chromadb
pause
