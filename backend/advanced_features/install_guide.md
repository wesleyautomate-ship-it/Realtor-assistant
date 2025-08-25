# 🛠️ Advanced Features Installation Guide

## 🚨 Common Installation Errors & Solutions

### **Error 1: Version Conflicts**
```
ERROR: Cannot install package because these package versions conflict
```

**Solution:**
```bash
# 1. Create a clean virtual environment
python -m venv advanced_features_env
source advanced_features_env/bin/activate  # On Windows: advanced_features_env\Scripts\activate

# 2. Install main requirements first
pip install -r ../requirements.txt

# 3. Install advanced features requirements
pip install -r requirements_simple.txt
```

### **Error 2: spaCy Model Not Found**
```
OSError: Can't find model 'en_core_web_sm'
```

**Solution:**
```bash
# Install spaCy model
python -m spacy download en_core_web_sm

# If that fails, try:
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.0/en_core_web_sm-3.7.0-py3-none-any.whl
```

### **Error 3: Compilation Errors (Windows)**
```
error: Microsoft Visual C++ 14.0 or greater is required
```

**Solution:**
```bash
# Install pre-compiled wheels
pip install --only-binary=all scikit-learn numpy scipy

# Or install Visual Studio Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

### **Error 4: Memory Issues**
```
MemoryError: Unable to allocate array
```

**Solution:**
```bash
# Install lighter versions
pip install scikit-learn-intelex  # Intel optimized version
pip install --no-cache-dir -r requirements_simple.txt
```

## 📋 Step-by-Step Installation

### **Step 1: Check Current Environment**
```bash
# Check Python version (should be 3.8+)
python --version

# Check pip version
pip --version

# List current packages
pip list
```

### **Step 2: Install Dependencies**
```bash
# Navigate to backend directory
cd backend

# Install main requirements (if not already done)
pip install -r requirements.txt

# Install advanced features
cd advanced_features
pip install -r requirements_simple.txt
```

### **Step 3: Install spaCy Model**
```bash
# Install English language model
python -m spacy download en_core_web_sm

# Verify installation
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('✅ spaCy model loaded successfully')"
```

### **Step 4: Test Installation**
```bash
# Test basic imports
python -c "
try:
    from advanced_features.integration_manager import AdvancedFeaturesIntegrationManager
    print('✅ Advanced features imported successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
"

# Run example (optional)
python example_usage.py
```

## 🔧 Alternative Installation Methods

### **Method 1: Conda Installation**
```bash
# Create conda environment
conda create -n advanced_features python=3.9
conda activate advanced_features

# Install packages
conda install scikit-learn numpy pandas scipy
conda install -c conda-forge spacy
python -m spacy download en_core_web_sm

# Install remaining packages
pip install -r requirements_simple.txt
```

### **Method 2: Docker Installation**
```dockerfile
# Dockerfile for advanced features
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements_simple.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements_simple.txt

# Install spaCy model
RUN python -m spacy download en_core_web_sm

# Copy advanced features
COPY . .

CMD ["python", "example_usage.py"]
```

### **Method 3: Minimal Installation**
```bash
# Install only essential packages
pip install scikit-learn textblob requests

# Skip spaCy for now (will use fallback)
# The system will work without spaCy, just with reduced NLP capabilities
```

## 🐛 Troubleshooting Specific Errors

### **Error: "No module named 'sklearn'"
```bash
# Install scikit-learn
pip install scikit-learn

# If that fails, try:
pip install --upgrade pip
pip install scikit-learn --no-cache-dir
```

### **Error: "No module named 'textblob'"
```bash
# Install textblob
pip install textblob

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
```

### **Error: "No module named 'spacy'"
```bash
# Install spaCy
pip install spacy

# If that fails, try:
pip install spacy --no-cache-dir
```

### **Error: "spaCy model not found"**
```bash
# Install model
python -m spacy download en_core_web_sm

# If that fails, try manual download:
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.0/en_core_web_sm-3.7.0-py3-none-any.whl
```

## 🔍 Verification Commands

### **Check All Imports**
```python
# Create test_imports.py
import sys
print(f"Python version: {sys.version}")

try:
    import sklearn
    print("✅ scikit-learn imported")
except ImportError as e:
    print(f"❌ scikit-learn error: {e}")

try:
    import spacy
    print("✅ spaCy imported")
    nlp = spacy.load('en_core_web_sm')
    print("✅ spaCy model loaded")
except ImportError as e:
    print(f"❌ spaCy error: {e}")

try:
    import textblob
    print("✅ textblob imported")
except ImportError as e:
    print(f"❌ textblob error: {e}")

try:
    import numpy
    print("✅ numpy imported")
except ImportError as e:
    print(f"❌ numpy error: {e}")

try:
    import pandas
    print("✅ pandas imported")
except ImportError as e:
    print(f"❌ pandas error: {e}")
```

### **Test Advanced Features**
```python
# Create test_advanced_features.py
try:
    from advanced_features.integration_manager import AdvancedFeaturesIntegrationManager
    print("✅ AdvancedFeaturesIntegrationManager imported")
    
    manager = AdvancedFeaturesIntegrationManager()
    print("✅ Manager initialized")
    
    result = manager.process_message("Calculate ROI for 2M AED property")
    print("✅ Message processed successfully")
    
except Exception as e:
    print(f"❌ Error: {e}")
```

## 📞 Getting Help

If you're still experiencing issues:

1. **Check your Python version** (should be 3.8+)
2. **Check your pip version** (should be latest)
3. **Try creating a fresh virtual environment**
4. **Install packages one by one** to identify the problematic package
5. **Check system requirements** (especially on Windows)

### **Common System Requirements:**
- **Windows**: Visual Studio Build Tools
- **macOS**: Xcode Command Line Tools
- **Linux**: build-essential package

### **Useful Commands:**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Clear pip cache
pip cache purge

# Install with verbose output
pip install -v package_name

# Check package conflicts
pip check
```

## ✅ Success Indicators

You'll know the installation is successful when:

1. ✅ All imports work without errors
2. ✅ spaCy model loads successfully
3. ✅ AdvancedFeaturesIntegrationManager initializes
4. ✅ Example usage runs without errors
5. ✅ No version conflicts in pip list

---

**Need more help?** Create an issue with your specific error message and system details!
