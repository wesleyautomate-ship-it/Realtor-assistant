# 📁 Manual Project Copy Guide

## 🎯 **Overview**
This guide helps you manually copy your Dubai RAG System project to a different computer with a different GitHub account.

## 🚀 **Quick Start**

### **Option A: Automated Script (Recommended)**
```bash
# Windows
manual_project_copy.bat

# Linux/Mac
chmod +x manual_project_copy.sh
./manual_project_copy.sh
```

### **Option B: Manual Copy (Step by Step)**

## 📋 **Step-by-Step Manual Copy**

### **Step 1: Create New Project Directory**
```bash
# Create main project folder
mkdir Dubai-RAG-System-New
cd Dubai-RAG-System-New

# Create subdirectories
mkdir backend frontend docs scripts config data uploads logs tests monitoring ssl test_documents test_reports upload_data testsprite_tests
```

### **Step 2: Copy Backend Files**
```bash
# Copy entire backend directory
cp -r /path/to/source/backend/* backend/

# Or on Windows
xcopy "C:\path\to\source\backend" "backend\" /E /I /H /Y
```

### **Step 3: Copy Frontend Files**
```bash
# Copy entire frontend directory
cp -r /path/to/source/frontend/* frontend/

# Or on Windows
xcopy "C:\path\to\source\frontend" "frontend\" /E /I /H /Y
```

### **Step 4: Copy Documentation**
```bash
# Copy docs directory
cp -r /path/to/source/docs/* docs/

# Copy individual documentation files
cp /path/to/source/README.md .
cp /path/to/source/CHANGELOG.md .
cp /path/to/source/REPOSITORY_SETUP_GUIDE.md .
cp /path/to/source/*_SUMMARY.md .
cp /path/to/source/*_REPORT.md .
cp /path/to/source/*_PLAN.md .
cp /path/to/source/*_GUIDE.md .
```

### **Step 5: Copy Configuration Files**
```bash
# Copy Docker and environment files
cp /path/to/source/docker-compose.yml .
cp /path/to/source/docker-compose.*.yml .
cp /path/to/source/env.example .
cp /path/to/source/requirements.txt .
cp /path/to/source/package.json .
cp /path/to/source/package-lock.json .
cp /path/to/source/pytest.ini .
cp /path/to/source/ngrok.yml .
```

### **Step 6: Copy Scripts and Automation**
```bash
# Copy scripts directory
cp -r /path/to/source/scripts/* scripts/

# Copy setup and test scripts
cp /path/to/source/setup_new_repository.bat .
cp /path/to/source/setup_new_repository.sh .
cp /path/to/source/docker-test-blueprint2.bat .
cp /path/to/source/docker-test-blueprint2.sh .
cp /path/to/source/run_tests.bat .
cp /path/to/source/run_tests.sh .
cp /path/to/source/verify_system.bat .
cp /path/to/source/verify_system.py .
cp /path/to/source/start_mobile.bat .
```

### **Step 7: Copy Test Files**
```bash
# Copy test files
cp /path/to/source/test_*.py .

# Copy test directories
cp -r /path/to/source/test_documents/* test_documents/
cp -r /path/to/source/test_reports/* test_reports/
cp -r /path/to/source/upload_data/* upload_data/
cp -r /path/to/source/testsprite_tests/* testsprite_tests/
```

### **Step 8: Copy Data Files**
```bash
# Copy essential data files
cp /path/to/source/data/*.csv data/
cp /path/to/source/data/*.json data/
cp /path/to/source/data/*.xlsx data/
cp /path/to/source/data/*.docx data/
cp /path/to/source/data/*.pdf data/
```

### **Step 9: Copy Additional Directories**
```bash
# Copy monitoring
cp -r /path/to/source/monitoring/* monitoring/

# Copy config
cp -r /path/to/source/config/* config/

# Copy SSL if exists
if [ -d "/path/to/source/ssl" ]; then
    cp -r /path/to/source/ssl/* ssl/
fi
```

## ✅ **What Gets Copied**

### **📁 Directories:**
- `backend/` - All Python files, ML services, routers, models
- `frontend/` - All React components, utilities, styles, assets
- `docs/` - All documentation, guides, API docs
- `scripts/` - All automation and utility scripts
- `config/` - Configuration files and settings
- `data/` - Sample data files (CSV, JSON, Excel, PDF)
- `monitoring/` - Monitoring configurations and dashboards
- `test_documents/` - Test documents and files
- `test_reports/` - Test reports and outputs
- `upload_data/` - Sample upload data
- `testsprite_tests/` - TestSprite test files

### **📄 Files:**
- `docker-compose.yml` - Docker orchestration
- `env.example` - Environment template
- `requirements.txt` - Python dependencies
- `package.json` - Node.js dependencies
- `README.md` - Project documentation
- `CHANGELOG.md` - Version history
- All `*_SUMMARY.md`, `*_REPORT.md`, `*_PLAN.md`, `*_GUIDE.md` files
- All `test_*.py` files
- All setup and automation scripts

## ❌ **What Gets Excluded**

### **🚫 Runtime Files:**
- `node_modules/` - Node.js dependencies (reinstall with `npm install`)
- `venv/` - Python virtual environment (recreate with `python -m venv venv`)
- `.git/` - Git history (new repository will be created)
- `logs/` - Runtime logs (will be recreated)
- `uploads/` - User uploads (will be recreated)
- `chroma/` - Vector database (will be recreated)

### **🚫 Temporary Files:**
- `*.pyc` - Python bytecode
- `__pycache__/` - Python cache
- `.DS_Store` - macOS system files
- `Thumbs.db` - Windows thumbnail cache

## 🔧 **Setup on New Computer**

### **1. Run Setup Script**
```bash
# Windows
setup_new_repository.bat

# Linux/Mac
chmod +x setup_new_repository.sh
./setup_new_repository.sh
```

### **2. Install Dependencies**
```bash
# Backend dependencies
pip install -r requirements.txt

# Frontend dependencies
cd frontend
npm install
cd ..
```

### **3. Create Environment File**
```bash
# Copy and edit environment file
cp env.example .env
# Edit .env with your new API keys and settings
```

### **4. Create New GitHub Repository**
1. Go to GitHub and create a new repository
2. Add remote origin:
   ```bash
   git remote add origin https://github.com/NEW_USERNAME/NEW_REPO_NAME.git
   git push -u origin main
   ```

## 🚨 **Important Notes**

### **🔑 Environment Variables**
You'll need to update these in your new `.env` file:
- `GOOGLE_API_KEY` - Your Google API key
- `SECRET_KEY` - New JWT secret key
- `REELLY_API_KEY` - Your Reelly API key
- `DATABASE_URL` - Database connection string
- `REDIS_URL` - Redis connection string

### **🗄️ Database**
- You'll start with a fresh database
- Run migrations to set up the schema
- Import sample data if needed

### **🔐 Security**
- Generate new JWT secret key
- Update CORS settings if needed
- Review and update API keys

## 🧪 **Testing the Copy**

### **1. Run System Verification**
```bash
# Windows
verify_system.bat

# Linux/Mac
python verify_system.py
```

### **2. Run Tests**
```bash
# Run all tests
python -m pytest

# Or use the test script
run_tests.bat  # Windows
./run_tests.sh  # Linux/Mac
```

### **3. Test Docker Setup**
```bash
# Build and test Docker containers
docker-compose build
docker-compose up -d
```

## 📞 **Troubleshooting**

### **Common Issues:**

1. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   npm install
   ```

2. **Environment Variables**
   - Check `.env` file exists
   - Verify all required variables are set

3. **Database Connection**
   - Ensure PostgreSQL is running
   - Check database URL in `.env`

4. **Docker Issues**
   - Check Docker is running
   - Verify `docker-compose.yml` syntax

5. **Import Errors**
   - Check Python path
   - Verify all modules are installed

## 🎉 **Success Checklist**

- [ ] All directories copied successfully
- [ ] All configuration files present
- [ ] Dependencies installed
- [ ] Environment variables set
- [ ] New Git repository created
- [ ] System verification passes
- [ ] Tests run successfully
- [ ] Docker containers start
- [ ] Application runs without errors

## 📚 **Next Steps**

1. **Review Documentation**: Read through `README.md` and `REPOSITORY_SETUP_GUIDE.md`
2. **Configure Environment**: Set up your `.env` file with new API keys
3. **Test System**: Run verification and test scripts
4. **Deploy**: Set up your deployment environment
5. **Document**: Update any project-specific documentation

---

**Need Help?** Check the `TROUBLESHOOTING_GUIDE.md` for detailed solutions to common issues.
