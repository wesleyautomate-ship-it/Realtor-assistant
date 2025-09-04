#!/bin/bash

echo "========================================"
echo "Dubai RAG System - Manual Project Copy"
echo "========================================"
echo

# Set source and destination paths
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST_DIR="${SOURCE_DIR}/Dubai-RAG-System-New"

echo "Source Directory: $SOURCE_DIR"
echo "Destination Directory: $DEST_DIR"
echo

# Create destination directory
echo "[1/10] Creating destination directory..."
if [ -d "$DEST_DIR" ]; then
    echo "Directory already exists. Removing old version..."
    rm -rf "$DEST_DIR"
fi
mkdir -p "$DEST_DIR"
cd "$DEST_DIR"

# Create subdirectories
echo "[2/10] Creating project structure..."
mkdir -p backend frontend docs scripts config data uploads logs tests monitoring ssl test_documents test_reports upload_data testsprite_tests

echo "[3/10] Copying backend directory..."
cp -r "$SOURCE_DIR/backend"/* backend/ 2>/dev/null || true

echo "[4/10] Copying frontend directory..."
cp -r "$SOURCE_DIR/frontend"/* frontend/ 2>/dev/null || true

echo "[5/10] Copying docs directory..."
cp -r "$SOURCE_DIR/docs"/* docs/ 2>/dev/null || true

echo "[6/10] Copying scripts directory..."
cp -r "$SOURCE_DIR/scripts"/* scripts/ 2>/dev/null || true

echo "[7/10] Copying config directory..."
cp -r "$SOURCE_DIR/config"/* config/ 2>/dev/null || true

echo "[8/10] Copying essential data files..."
cp "$SOURCE_DIR/data"/*.csv data/ 2>/dev/null || true
cp "$SOURCE_DIR/data"/*.json data/ 2>/dev/null || true
cp "$SOURCE_DIR/data"/*.xlsx data/ 2>/dev/null || true
cp "$SOURCE_DIR/data"/*.docx data/ 2>/dev/null || true
cp "$SOURCE_DIR/data"/*.pdf data/ 2>/dev/null || true

echo "[9/10] Copying configuration and setup files..."
cp "$SOURCE_DIR/docker-compose.yml" . 2>/dev/null || true
cp "$SOURCE_DIR/docker-compose."*.yml . 2>/dev/null || true
cp "$SOURCE_DIR/env.example" . 2>/dev/null || true
cp "$SOURCE_DIR/requirements.txt" . 2>/dev/null || true
cp "$SOURCE_DIR/package.json" . 2>/dev/null || true
cp "$SOURCE_DIR/package-lock.json" . 2>/dev/null || true
cp "$SOURCE_DIR/pytest.ini" . 2>/dev/null || true
cp "$SOURCE_DIR/ngrok.yml" . 2>/dev/null || true

echo "[10/10] Copying documentation and setup files..."
cp "$SOURCE_DIR/README.md" . 2>/dev/null || true
cp "$SOURCE_DIR/CHANGELOG.md" . 2>/dev/null || true
cp "$SOURCE_DIR/REPOSITORY_SETUP_GUIDE.md" . 2>/dev/null || true
cp "$SOURCE_DIR/setup_new_repository.bat" . 2>/dev/null || true
cp "$SOURCE_DIR/setup_new_repository.sh" . 2>/dev/null || true
cp "$SOURCE_DIR/docker-test-blueprint2.bat" . 2>/dev/null || true
cp "$SOURCE_DIR/docker-test-blueprint2.sh" . 2>/dev/null || true
cp "$SOURCE_DIR/run_tests.bat" . 2>/dev/null || true
cp "$SOURCE_DIR/run_tests.sh" . 2>/dev/null || true
cp "$SOURCE_DIR/verify_system.bat" . 2>/dev/null || true
cp "$SOURCE_DIR/verify_system.py" . 2>/dev/null || true
cp "$SOURCE_DIR/start_mobile.bat" . 2>/dev/null || true

# Copy test files
cp "$SOURCE_DIR/test_"*.py . 2>/dev/null || true
cp "$SOURCE_DIR/"*_SUMMARY.md . 2>/dev/null || true
cp "$SOURCE_DIR/"*_REPORT.md . 2>/dev/null || true
cp "$SOURCE_DIR/"*_PLAN.md . 2>/dev/null || true
cp "$SOURCE_DIR/"*_GUIDE.md . 2>/dev/null || true

# Copy monitoring files
cp -r "$SOURCE_DIR/monitoring"/* monitoring/ 2>/dev/null || true

# Copy test directories
cp -r "$SOURCE_DIR/test_documents"/* test_documents/ 2>/dev/null || true
cp -r "$SOURCE_DIR/test_reports"/* test_reports/ 2>/dev/null || true
cp -r "$SOURCE_DIR/upload_data"/* upload_data/ 2>/dev/null || true
cp -r "$SOURCE_DIR/testsprite_tests"/* testsprite_tests/ 2>/dev/null || true

# Copy SSL directory if it exists
if [ -d "$SOURCE_DIR/ssl" ]; then
    cp -r "$SOURCE_DIR/ssl"/* ssl/ 2>/dev/null || true
fi

echo
echo "========================================"
echo "Copy Complete!"
echo "========================================"
echo
echo "Project copied to: $DEST_DIR"
echo
echo "Next steps:"
echo "1. Navigate to the new directory: cd \"$DEST_DIR\""
echo "2. Run setup script: ./setup_new_repository.sh"
echo "3. Create new GitHub repository"
echo "4. Update environment variables"
echo "5. Install dependencies"
echo
echo "Files copied:"
echo "- Backend: All Python files, ML services, routers"
echo "- Frontend: All React components, utilities, styles"
echo "- Documentation: All guides, API docs, troubleshooting"
echo "- Scripts: All automation and setup scripts"
echo "- Configuration: Docker, environment, package files"
echo "- Data: Sample data files (CSV, JSON, Excel, PDF)"
echo "- Tests: All test files and test data"
echo "- Monitoring: All monitoring configurations"
echo
echo "Excluded (will be recreated):"
echo "- node_modules/ (run npm install)"
echo "- venv/ (create new virtual environment)"
echo "- .git/ (new repository will be created)"
echo "- logs/ (runtime logs)"
echo "- uploads/ (user uploads)"
echo "- chroma/ (vector database)"
echo
