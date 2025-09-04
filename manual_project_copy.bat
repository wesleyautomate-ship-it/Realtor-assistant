@echo off
echo ========================================
echo Dubai RAG System - Manual Project Copy
echo ========================================
echo.

REM Set source and destination paths
set "SOURCE_DIR=%~dp0"
set "DEST_DIR=%SOURCE_DIR%Dubai-RAG-System-New"

echo Source Directory: %SOURCE_DIR%
echo Destination Directory: %DEST_DIR%
echo.

REM Create destination directory
echo [1/10] Creating destination directory...
if exist "%DEST_DIR%" (
    echo Directory already exists. Removing old version...
    rmdir /s /q "%DEST_DIR%"
)
mkdir "%DEST_DIR%"
cd /d "%DEST_DIR%"

REM Create subdirectories
echo [2/10] Creating project structure...
mkdir backend
mkdir frontend
mkdir docs
mkdir scripts
mkdir config
mkdir data
mkdir uploads
mkdir logs
mkdir tests
mkdir monitoring
mkdir ssl
mkdir test_documents
mkdir test_reports
mkdir upload_data
mkdir testsprite_tests

echo [3/10] Copying backend directory...
xcopy "%SOURCE_DIR%backend" "backend\" /E /I /H /Y /Q

echo [4/10] Copying frontend directory...
xcopy "%SOURCE_DIR%frontend" "frontend\" /E /I /H /Y /Q

echo [5/10] Copying docs directory...
xcopy "%SOURCE_DIR%docs" "docs\" /E /I /H /Y /Q

echo [6/10] Copying scripts directory...
xcopy "%SOURCE_DIR%scripts" "scripts\" /E /I /H /Y /Q

echo [7/10] Copying config directory...
xcopy "%SOURCE_DIR%config" "config\" /E /I /H /Y /Q

echo [8/10] Copying essential data files...
xcopy "%SOURCE_DIR%data\*.csv" "data\" /Y /Q
xcopy "%SOURCE_DIR%data\*.json" "data\" /Y /Q
xcopy "%SOURCE_DIR%data\*.xlsx" "data\" /Y /Q
xcopy "%SOURCE_DIR%data\*.docx" "data\" /Y /Q
xcopy "%SOURCE_DIR%data\*.pdf" "data\" /Y /Q

echo [9/10] Copying configuration and setup files...
copy "%SOURCE_DIR%docker-compose.yml" "." /Y
copy "%SOURCE_DIR%docker-compose.*.yml" "." /Y
copy "%SOURCE_DIR%env.example" "." /Y
copy "%SOURCE_DIR%requirements.txt" "." /Y
copy "%SOURCE_DIR%package.json" "." /Y
copy "%SOURCE_DIR%package-lock.json" "." /Y
copy "%SOURCE_DIR%pytest.ini" "." /Y
copy "%SOURCE_DIR%ngrok.yml" "." /Y

echo [10/10] Copying documentation and setup files...
copy "%SOURCE_DIR%README.md" "." /Y
copy "%SOURCE_DIR%CHANGELOG.md" "." /Y
copy "%SOURCE_DIR%REPOSITORY_SETUP_GUIDE.md" "." /Y
copy "%SOURCE_DIR%setup_new_repository.bat" "." /Y
copy "%SOURCE_DIR%setup_new_repository.sh" "." /Y
copy "%SOURCE_DIR%docker-test-blueprint2.bat" "." /Y
copy "%SOURCE_DIR%docker-test-blueprint2.sh" "." /Y
copy "%SOURCE_DIR%run_tests.bat" "." /Y
copy "%SOURCE_DIR%run_tests.sh" "." /Y
copy "%SOURCE_DIR%verify_system.bat" "." /Y
copy "%SOURCE_DIR%verify_system.py" "." /Y
copy "%SOURCE_DIR%start_mobile.bat" "." /Y

REM Copy test files
copy "%SOURCE_DIR%test_*.py" "." /Y
copy "%SOURCE_DIR%*_SUMMARY.md" "." /Y
copy "%SOURCE_DIR%*_REPORT.md" "." /Y
copy "%SOURCE_DIR%*_PLAN.md" "." /Y
copy "%SOURCE_DIR%*_GUIDE.md" "." /Y

REM Copy monitoring files
xcopy "%SOURCE_DIR%monitoring" "monitoring\" /E /I /H /Y /Q

REM Copy test directories
xcopy "%SOURCE_DIR%test_documents" "test_documents\" /E /I /H /Y /Q
xcopy "%SOURCE_DIR%test_reports" "test_reports\" /E /I /H /Y /Q
xcopy "%SOURCE_DIR%upload_data" "upload_data\" /E /I /H /Y /Q
xcopy "%SOURCE_DIR%testsprite_tests" "testsprite_tests\" /E /I /H /Y /Q

REM Copy SSL directory if it exists
if exist "%SOURCE_DIR%ssl" (
    xcopy "%SOURCE_DIR%ssl" "ssl\" /E /I /H /Y /Q
)

echo.
echo ========================================
echo Copy Complete!
echo ========================================
echo.
echo Project copied to: %DEST_DIR%
echo.
echo Next steps:
echo 1. Navigate to the new directory: cd "%DEST_DIR%"
echo 2. Run setup script: setup_new_repository.bat
echo 3. Create new GitHub repository
echo 4. Update environment variables
echo 5. Install dependencies
echo.
echo Files copied:
echo - Backend: All Python files, ML services, routers
echo - Frontend: All React components, utilities, styles
echo - Documentation: All guides, API docs, troubleshooting
echo - Scripts: All automation and setup scripts
echo - Configuration: Docker, environment, package files
echo - Data: Sample data files (CSV, JSON, Excel, PDF)
echo - Tests: All test files and test data
echo - Monitoring: All monitoring configurations
echo.
echo Excluded (will be recreated):
echo - node_modules/ (run npm install)
echo - venv/ (create new virtual environment)
echo - .git/ (new repository will be created)
echo - logs/ (runtime logs)
echo - uploads/ (user uploads)
echo - chroma/ (vector database)
echo.
pause
