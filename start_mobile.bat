@echo off
echo ========================================
echo    RAG Web App - Mobile Setup Script
echo ========================================
echo.

REM Check if Docker is running
echo Checking Docker status...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

REM Check if ngrok exists
if not exist "ngrok.exe" (
    echo ERROR: ngrok.exe not found in current directory!
    echo Please download ngrok from https://ngrok.com/download
    pause
    exit /b 1
)

echo Starting Docker services...
docker-compose up -d --build

echo.
echo Waiting for services to start...
timeout /t 10 /nobreak >nul

echo.
echo Checking service status...
docker-compose ps

echo.
echo ========================================
echo    Starting ngrok tunnels...
echo ========================================
echo.

REM Start ngrok tunnels in separate windows
start "Frontend Tunnel (Port 3000)" ngrok http 3000
timeout /t 3 /nobreak >nul
start "Backend Tunnel (Port 8003)" ngrok http 8003

echo.
echo ========================================
echo    Setup Complete!
echo ========================================
echo.
echo Look for ngrok URLs in the new windows:
echo.
echo 1. Frontend Tunnel window - Copy the HTTPS URL
echo 2. Backend Tunnel window - Copy the HTTPS URL
echo.
echo Next steps:
echo 1. Open the frontend ngrok URL on your phone
echo 2. If you get API errors, update the frontend config
echo 3. See NGROK_SETUP_GUIDE.md for detailed instructions
echo.
echo Press any key to continue...
pause >nul
