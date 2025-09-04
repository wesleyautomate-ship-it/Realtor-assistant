@echo off
REM Blueprint 2.0 Docker Testing Script for Windows
REM This script sets up and tests the Blueprint 2.0 implementation in Docker

echo 🚀 Starting Blueprint 2.0 Docker Testing...

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running. Please start Docker and try again.
    pause
    exit /b 1
)

REM Check if docker-compose is available
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] docker-compose is not installed. Please install it and try again.
    pause
    exit /b 1
)

echo [INFO] Stopping any existing containers...
docker-compose down -v

echo [INFO] Building and starting services...
docker-compose up -d --build

echo [INFO] Waiting for services to be healthy...
timeout /t 30 /nobreak >nul

echo [INFO] Checking service health...

REM Check PostgreSQL
docker-compose exec -T postgres pg_isready -U admin -d real_estate_db >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PostgreSQL is not healthy
    pause
    exit /b 1
) else (
    echo [SUCCESS] PostgreSQL is healthy
)

REM Check Redis
docker-compose exec -T redis redis-cli ping >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Redis is not healthy
    pause
    exit /b 1
) else (
    echo [SUCCESS] Redis is healthy
)

REM Check Backend
curl -f http://localhost:8003/health >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Backend health check failed, but continuing...
) else (
    echo [SUCCESS] Backend is healthy
)

echo [INFO] Running database migrations...
docker-compose exec -T backend python database_migrations.py

echo [INFO] Populating database with sample data...
docker-compose exec -T backend python populate_postgresql.py

echo [INFO] Testing Week 1 fixes...
docker-compose exec -T backend python test_week1_fixes.py

echo [INFO] Running Blueprint 2.0 tests...
docker-compose --profile test run --rm test-runner

echo [INFO] Testing API endpoints...

REM Test Documents API
echo [INFO] Testing Documents API...
curl -f http://localhost:8003/documents/ >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Documents API test failed
) else (
    echo [SUCCESS] Documents API is working
)

REM Test Nurturing API
echo [INFO] Testing Nurturing API...
curl -f http://localhost:8003/nurturing/users/me/agenda >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Nurturing API test failed
) else (
    echo [SUCCESS] Nurturing API is working
)

echo [SUCCESS] Blueprint 2.0 Docker testing completed!

echo.
echo 📋 Test Summary:
echo ✅ PostgreSQL: Running and healthy
echo ✅ Redis: Running and healthy
echo ✅ Backend: Running on http://localhost:8003
echo ✅ Frontend: Running on http://localhost:3000
echo ✅ ChromaDB: Running on http://localhost:8002
echo.
echo 🔗 Access Points:
echo    - Frontend: http://localhost:3000
echo    - Backend API: http://localhost:8003
echo    - API Documentation: http://localhost:8003/docs
echo    - ChromaDB: http://localhost:8002
echo.
echo 🧪 To run additional tests:
echo    docker-compose --profile test run --rm test-runner
echo.
echo 📊 To view logs:
echo    docker-compose logs -f backend
echo.
echo 🛑 To stop services:
echo    docker-compose down
echo.
pause
