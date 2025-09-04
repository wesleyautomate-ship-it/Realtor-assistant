@echo off
echo ========================================
echo Dubai Real Estate RAG System Verification
echo ========================================
echo.

:: Check if Docker is running
echo [1/5] Checking Docker status...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed or not running
    echo Please install Docker Desktop and start it
    pause
    exit /b 1
) else (
    echo ✅ Docker is available
)

:: Check Docker Compose
echo.
echo [2/5] Checking Docker Compose...
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not available
    pause
    exit /b 1
) else (
    echo ✅ Docker Compose is available
)

:: Check if services are running
echo.
echo [3/5] Checking Docker services...
docker-compose ps
if %errorlevel% neq 0 (
    echo ❌ Docker services are not running
    echo Starting services...
    docker-compose up -d
    timeout /t 30 /nobreak >nul
) else (
    echo ✅ Docker services are running
)

:: Check if Python is available
echo.
echo [4/5] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not available
    echo Please install Python 3.8+ and add it to PATH
    pause
    exit /b 1
) else (
    echo ✅ Python is available
)

:: Run system verification
echo.
echo [5/5] Running system verification...
python verify_system.py
if %errorlevel% neq 0 (
    echo.
    echo ❌ System verification failed
    echo.
    echo Troubleshooting steps:
    echo 1. Ensure Docker Desktop is running
    echo 2. Run: docker-compose up -d
    echo 3. Wait for services to start (30-60 seconds)
    echo 4. Run: python verify_system.py
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo ✅ System verification completed successfully!
    echo.
    echo 🚀 System is ready for testing!
    echo.
    echo Access the application at:
    echo - Frontend: http://localhost:3000
    echo - Backend API: http://localhost:8003
    echo - API Docs: http://localhost:8003/docs
    echo.
)

pause
