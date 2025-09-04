@echo off
REM Docker Services Startup Script for Windows
REM Ensures proper startup order and health checks for all services

echo 🚀 Starting RAG System Services...
echo ==================================

REM Function to wait for service health
:wait_for_service
set service_name=%1
set health_url=%2
set max_attempts=30
set attempt=1

echo ⏳ Waiting for %service_name% to be healthy...

:wait_loop
curl -f "%health_url%" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ %service_name% is healthy!
    goto :eof
)

echo ⏳ Attempt %attempt%/%max_attempts% - %service_name% not ready yet...
timeout /t 2 /nobreak >nul
set /a attempt+=1
if %attempt% leq %max_attempts% goto wait_loop

echo ❌ %service_name% failed to become healthy after %max_attempts% attempts
exit /b 1

REM Start PostgreSQL
echo 📦 Starting PostgreSQL...
docker-compose up -d postgres
call :wait_for_service "PostgreSQL" "http://localhost:5432"
if %errorlevel% neq 0 exit /b 1

REM Start Redis
echo 📦 Starting Redis...
docker-compose up -d redis
call :wait_for_service "Redis" "http://localhost:6379"
if %errorlevel% neq 0 exit /b 1

REM Start ChromaDB
echo 📦 Starting ChromaDB...
docker-compose up -d chromadb
call :wait_for_service "ChromaDB" "http://localhost:8002/api/v1/heartbeat"
if %errorlevel% neq 0 exit /b 1

REM Start Backend
echo 📦 Starting Backend...
docker-compose up -d backend
call :wait_for_service "Backend" "http://localhost:8003/health"
if %errorlevel% neq 0 exit /b 1

REM Start Frontend
echo 📦 Starting Frontend...
docker-compose up -d frontend
call :wait_for_service "Frontend" "http://localhost:3000"
if %errorlevel% neq 0 exit /b 1

echo.
echo 🎉 All services started successfully!
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

REM Run connection tests
echo 🧪 Running connection tests...
python scripts/test_connections.py

echo.
echo ✨ RAG System is ready to use!
pause
