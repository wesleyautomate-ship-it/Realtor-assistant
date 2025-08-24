# Real Estate RAG Chat Application - Debugging & Troubleshooting Guide

## 🚨 **Project Development Challenges & Solutions**

This document chronicles all the major challenges, debugging issues, dependency problems, and sequencing issues we encountered during the development of the Real Estate RAG Chat Application.

---

## 🔧 **PHASE 1: ENVIRONMENT & SETUP CHALLENGES**

### **1.1 PowerShell Command Issues**

#### **Problem:**
```bash
# This doesn't work in PowerShell
npm install && npm start
```

#### **Root Cause:**
PowerShell doesn't support the `&&` operator like bash does.

#### **Solution:**
```powershell
# Use semicolon instead
npm install; npm start

# Or use separate commands
npm install
npm start

# Or use PowerShell's logical AND
npm install -and npm start
```

#### **Best Practice:**
Always test commands in your specific shell environment before assuming they'll work.

---

### **1.2 Docker Compose Networking Issues**

#### **Problem:**
```bash
# Services couldn't communicate with each other
Connection refused: localhost:5432
```

#### **Root Cause:**
Docker services trying to connect to `localhost` instead of service names.

#### **Solution:**
```yaml
# In docker-compose.yml, use service names
DATABASE_URL=postgresql://admin:password123@postgres:5432/real_estate_db
CHROMA_HOST=chromadb
```

#### **Debugging Steps:**
1. Check if containers are running: `docker-compose ps`
2. Check container logs: `docker-compose logs [service-name]`
3. Test network connectivity: `docker exec -it [container] ping [service]`

---

### **1.3 Python Virtual Environment Issues**

#### **Problem:**
```bash
# ModuleNotFoundError: No module named 'fastapi'
ModuleNotFoundError: No module named 'chromadb'
```

#### **Root Cause:**
Not activating virtual environment or installing dependencies.

#### **Solution:**
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

#### **Common Mistake:**
Forgetting to activate venv before running Python scripts.

---

## 🔄 **PHASE 2: DEPENDENCY & VERSION CONFLICTS**

### **2.1 ChromaDB Version Compatibility**

#### **Problem:**
```python
# ChromaDB client initialization errors
TypeError: __init__() got an unexpected keyword argument 'host'
```

#### **Root Cause:**
ChromaDB API changes between versions.

#### **Solution:**
```python
# Old way (deprecated)
chroma_client = chromadb.HttpClient(host="localhost", port=8000)

# New way
chroma_client = chromadb.HttpClient("http://localhost:8000")
```

#### **Version Management:**
```txt
# requirements.txt - Pin specific versions
chromadb==0.4.22
fastapi==0.104.1
uvicorn==0.24.0
```

---

### **2.2 FastAPI CORS Issues**

#### **Problem:**
```javascript
// Frontend CORS errors
Access to fetch at 'http://localhost:8001/chat' from origin 'http://localhost:3000' has been blocked by CORS policy
```

#### **Root Cause:**
CORS middleware not properly configured.

#### **Solution:**
```python
# In backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### **Debugging:**
1. Check browser console for CORS errors
2. Verify backend is running on correct port
3. Ensure CORS middleware is added before routes

---

### **2.3 React Dependencies Conflicts**

#### **Problem:**
```bash
# npm install conflicts
npm ERR! ERESOLVE overriding peer dependency
```

#### **Root Cause:**
Conflicting peer dependencies between packages.

#### **Solution:**
```bash
# Force install
npm install --force

# Or use legacy peer deps
npm install --legacy-peer-deps

# Or update package.json with compatible versions
```

---

## 🗄️ **PHASE 3: DATABASE & DATA ISSUES**

### **3.1 PostgreSQL Connection Issues**

#### **Problem:**
```python
# Database connection errors
psycopg2.OperationalError: connection to server at "localhost" (127.0.0.1), port 5432 failed
```

#### **Root Cause:**
Database not started or wrong credentials.

#### **Solution:**
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Restart database
docker-compose restart postgres

# Check logs
docker-compose logs postgres
```

#### **Credentials Debugging:**
```python
# Verify connection string
DATABASE_URL = "postgresql://admin:password123@localhost:5432/real_estate_db"
```

---

### **3.2 ChromaDB Collection Issues**

#### **Problem:**
```python
# Collection not found errors
ValueError: Collection 'neighborhoods' not found
```

#### **Root Cause:**
Collections not created or data not ingested.

#### **Solution:**
```python
# Create collection if it doesn't exist
try:
    collection = chroma_client.get_collection("neighborhoods")
except:
    collection = chroma_client.create_collection("neighborhoods")
```

#### **Data Ingestion Debugging:**
```python
# Check if collections exist
collections = chroma_client.list_collections()
print([col.name for col in collections])
```

---

### **3.3 SQL Schema Mismatches**

#### **Problem:**
```python
# Column count mismatch
IndexError: list index out of range
```

#### **Root Cause:**
Database schema doesn't match expected column count.

#### **Solution:**
```python
# Safe column access
row_data = list(row)
if len(row_data) > 0:
    client["id"] = row_data[0]
if len(row_data) > 1:
    client["name"] = row_data[1]
# ... continue for all columns
```

---

## 🎨 **PHASE 4: FRONTEND DEVELOPMENT ISSUES**

### **4.1 React Component Import Errors**

#### **Problem:**
```javascript
// Import errors
Module not found: Can't resolve './components/FileUpload'
```

#### **Root Cause:**
File path issues or missing files.

#### **Solution:**
```javascript
// Check file structure
// Ensure file exists at: frontend/src/components/FileUpload.jsx

// Use correct import path
import FileUpload from './components/FileUpload';
```

#### **Debugging Steps:**
1. Verify file exists
2. Check file extension (.jsx vs .js)
3. Ensure correct relative path
4. Restart development server

---

### **4.2 CSS Styling Issues**

#### **Problem:**
```css
/* Styles not applying */
.upload-area {
    /* Styles not working */
}
```

#### **Root Cause:**
CSS file not imported or specificity issues.

#### **Solution:**
```javascript
// Ensure CSS is imported
import './FileUpload.css';

// Check CSS specificity
.upload-area.drag-over {
    /* More specific selector */
}
```

#### **Debugging:**
1. Check browser dev tools
2. Verify CSS is loaded in Network tab
3. Check for CSS conflicts

---

### **4.3 State Management Issues**

#### **Problem:**
```javascript
// State not updating
const [uploadedFiles, setUploadedFiles] = useState([]);
// setUploadedFiles not working
```

#### **Root Cause:**
State updates not triggering re-renders.

#### **Solution:**
```javascript
// Use functional updates
setUploadedFiles(prev => [...prev, newFile]);

// Ensure dependencies in useEffect
useEffect(() => {
    // Effect logic
}, [dependency]);
```

---

## 🔄 **PHASE 5: API & INTEGRATION ISSUES**

### **5.1 File Upload Response Handling**

#### **Problem:**
```javascript
// Upload always failing
if (response.data.success) {
    // This never executes
}
```

#### **Root Cause:**
Backend returns different response format than expected.

#### **Solution:**
```javascript
// Backend returns FileUploadResponse directly
// Remove success field check
setSuccess(`File "${file.name}" uploaded successfully!`);
```

#### **Debugging:**
```javascript
// Log response to understand structure
console.log('Upload response:', response.data);
```

---

### **5.2 Axios Request Issues**

#### **Problem:**
```javascript
// Network errors
Network Error
```

#### **Root Cause:**
Backend not running or wrong URL.

#### **Solution:**
```javascript
// Check backend URL
const API_BASE_URL = 'http://localhost:8001';

// Add error handling
try {
    const response = await axios.post(`${API_BASE_URL}/upload-file`, formData);
} catch (err) {
    console.error('Upload error:', err);
    setError(err.message);
}
```

---

### **5.3 FormData Issues**

#### **Problem:**
```javascript
// File not being sent
FormData is empty
```

#### **Root Cause:**
File not properly appended to FormData.

#### **Solution:**
```javascript
const formData = new FormData();
formData.append('file', file);
formData.append('role', role);

// Verify FormData contents
for (let [key, value] of formData.entries()) {
    console.log(key, value);
}
```

---

## 🤖 **PHASE 6: AI & RAG SYSTEM ISSUES**

### **6.1 Google Gemini API Issues**

#### **Problem:**
```python
# API key errors
google.generativeai.types.BlockedPromptException
```

#### **Root Cause:**
Invalid API key or content policy violations.

#### **Solution:**
```python
# Check API key
import os
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not set")

# Configure Gemini
genai.configure(api_key=api_key)
```

#### **Debugging:**
1. Verify API key in .env file
2. Check Google Cloud Console for API usage
3. Ensure content doesn't violate policies

---

### **6.2 ChromaDB Query Issues**

#### **Problem:**
```python
# Query returning no results
results = collection.query(query_texts=[message], n_results=5)
# results['documents'] is empty
```

#### **Root Cause:**
No documents in collection or embedding issues.

#### **Solution:**
```python
# Check collection count
print(f"Collection count: {collection.count()}")

# Check if documents exist
if collection.count() == 0:
    print("No documents in collection")
    return []
```

---

### **6.3 RAG Context Issues**

#### **Problem:**
```python
# Context too long for Gemini
Token limit exceeded
```

#### **Root Cause:**
Too much context being sent to AI model.

#### **Solution:**
```python
# Limit context length
enhanced_context = enhanced_context[:6]  # Limit to top 6 results

# Truncate long documents
def truncate_text(text, max_length=1000):
    return text[:max_length] + "..." if len(text) > max_length else text
```

---

## 📊 **PHASE 7: DATA PROCESSING PIPELINE ISSUES**

### **7.1 File Path Issues**

#### **Problem:**
```python
# File not found errors
FileNotFoundError: [Errno 2] No such file or directory
```

#### **Root Cause:**
Relative vs absolute path issues.

#### **Solution:**
```python
from pathlib import Path

# Use Path for cross-platform compatibility
file_path = Path("data/sample.csv")
if not file_path.exists():
    print(f"File not found: {file_path.absolute()}")
```

---

### **7.2 Data Validation Issues**

#### **Problem:**
```python
# Data type errors
ValueError: could not convert string to float
```

#### **Root Cause:**
Inconsistent data formats.

#### **Solution:**
```python
def safe_float(value):
    try:
        return float(value) if value else 0.0
    except (ValueError, TypeError):
        return 0.0

# Use safe conversion
price = safe_float(row_data[1])
```

---

### **7.3 Pipeline Configuration Issues**

#### **Problem:**
```python
# Configuration not loading
KeyError: 'postgres'
```

#### **Root Cause:**
YAML configuration file not found or malformed.

#### **Solution:**
```python
import yaml
from pathlib import Path

def load_config(config_path):
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)
```

---

## 🚀 **PHASE 8: DEPLOYMENT & SCALABILITY ISSUES**

### **8.1 Docker Build Issues**

#### **Problem:**
```bash
# Build failures
ERROR: failed to solve: process "/bin/sh -c pip install -r requirements.txt" did not complete
```

#### **Root Cause:**
Dependency conflicts or network issues.

#### **Solution:**
```dockerfile
# Use multi-stage build
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.9-slim
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
```

---

### **8.2 Port Conflicts**

#### **Problem:**
```bash
# Port already in use
Error: listen EADDRINUSE: address already in use :::8001
```

#### **Root Cause:**
Another service using the same port.

#### **Solution:**
```bash
# Find process using port
netstat -ano | findstr :8001

# Kill process
taskkill /PID <process_id> /F

# Or use different port
uvicorn main:app --host 0.0.0.0 --port 8002
```

---

## 🔍 **DEBUGGING METHODOLOGY**

### **1. Systematic Approach**
1. **Identify the Problem**: What exactly is failing?
2. **Check Logs**: Look at console, browser, and server logs
3. **Isolate the Issue**: Test components individually
4. **Research**: Check documentation and Stack Overflow
5. **Implement Fix**: Apply solution and test
6. **Document**: Record the issue and solution

### **2. Common Debugging Tools**
```bash
# Backend debugging
docker-compose logs -f [service]
python -m pdb script.py

# Frontend debugging
console.log('Debug info:', data)
React Developer Tools
Network tab in browser

# Database debugging
psql -h localhost -U admin -d real_estate_db
\dt  # List tables
SELECT * FROM table_name LIMIT 5;
```

### **3. Environment Verification Checklist**
- [ ] All services running (`docker-compose ps`)
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip list`, `npm list`)
- [ ] Environment variables set (`.env` file)
- [ ] Ports available (no conflicts)
- [ ] File permissions correct
- [ ] Network connectivity (ping, curl)

---

## 📋 **COMMON COMMANDS REFERENCE**

### **Docker Commands**
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f [service]

# Rebuild containers
docker-compose build --no-cache

# Access container shell
docker exec -it [container_name] bash
```

### **Python Commands**
```bash
# Activate virtual environment (PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run backend
python main.py

# Run with debug
python -m pdb main.py
```

### **Node.js Commands**
```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Clear cache
npm cache clean --force
```

---

## 🎯 **LESSONS LEARNED**

### **1. Environment Consistency**
- Always use the same development environment across team
- Document exact versions of dependencies
- Use Docker for consistent deployment

### **2. Error Handling**
- Implement comprehensive error handling from the start
- Log errors with context for easier debugging
- Provide user-friendly error messages

### **3. Testing Strategy**
- Test components individually before integration
- Use manual testing for UI components
- Implement automated tests for critical functionality

### **4. Documentation**
- Document all configuration steps
- Keep troubleshooting guides updated
- Record solutions for future reference

### **5. Version Control**
- Commit frequently with descriptive messages
- Use feature branches for major changes
- Tag releases for easy rollback

---

## 🚨 **CRITICAL ISSUES & SOLUTIONS**

### **1. File Upload Response Mismatch**
**Issue**: Frontend expected `success` field, backend returned direct response
**Solution**: Removed success field check, handled response directly

### **2. ChromaDB API Changes**
**Issue**: HttpClient constructor signature changed
**Solution**: Updated to new API format with URL string

### **3. PowerShell Command Compatibility**
**Issue**: `&&` operator not supported
**Solution**: Used semicolon or separate commands

### **4. CORS Configuration**
**Issue**: Frontend couldn't connect to backend
**Solution**: Properly configured CORS middleware with correct origins

### **5. Database Schema Mismatches**
**Issue**: Column count assumptions caused index errors
**Solution**: Implemented safe column access with length checks

---

## 📚 **RESOURCES & REFERENCES**

### **Documentation**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/docs/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Docker Documentation](https://docs.docker.com/)

### **Troubleshooting Guides**
- [PowerShell vs Bash Commands](https://docs.microsoft.com/en-us/powershell/)
- [Docker Compose Networking](https://docs.docker.com/compose/networking/)
- [React Development Tools](https://chrome.google.com/webstore/detail/react-developer-tools/)

### **Community Resources**
- [Stack Overflow](https://stackoverflow.com/)
- [GitHub Issues](https://github.com/)
- [Reddit r/reactjs](https://www.reddit.com/r/reactjs/)

---

This debugging guide serves as a comprehensive reference for future development and helps avoid repeating the same issues. Always refer to this document when encountering similar problems in the future.
