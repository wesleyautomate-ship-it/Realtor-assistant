@echo off
echo 🧪 Running Dubai Real Estate RAG Frontend Tests
echo ================================================

echo.
echo 📋 Available Test Commands:
echo   npm run test          - Run all tests once
echo   npm run test:watch    - Run tests in watch mode
echo   npm run test:coverage - Run tests with coverage report
echo   npm run test:ci       - Run tests for CI/CD
echo   npm run test:debug    - Run tests with debug info
echo   npm run test:update   - Update test snapshots
echo   npm run test:clear    - Clear Jest cache
echo.

echo 🚀 Starting tests...
npm run test

echo.
echo ✅ Tests completed!
pause
