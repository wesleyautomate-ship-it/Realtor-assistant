# Repository Setup Guide

This guide will help you set up a new repository for the Dubai RAG System project.

## 🚀 **Quick Setup (Windows)**

### Option 1: Automated Setup (Recommended)
1. **Run the setup script:**
   ```cmd
   setup_new_repository.bat
   ```
2. **Follow the prompts** - the script will automatically:
   - Remove the old Git repository
   - Initialize a new one
   - Add all files
   - Create an initial commit

### Option 2: Manual Setup
If you prefer to do it manually:

```cmd
# 1. Remove old Git repository
rmdir /s /q .git

# 2. Initialize new repository
git init

# 3. Add all files
git add .

# 4. Create initial commit
git commit -m "Initial commit: Dubai RAG System"
```

## 🐧 **Quick Setup (Linux/Mac)**

### Option 1: Automated Setup (Recommended)
1. **Make the script executable:**
   ```bash
   chmod +x setup_new_repository.sh
   ```
2. **Run the setup script:**
   ```bash
   ./setup_new_repository.sh
   ```

### Option 2: Manual Setup
```bash
# 1. Remove old Git repository
rm -rf .git

# 2. Initialize new repository
git init

# 3. Add all files
git add .

# 4. Create initial commit
git commit -m "Initial commit: Dubai RAG System"
```

## 📋 **Next Steps**

### 1. Create a New Repository
- **GitHub**: Go to [github.com](https://github.com) and create a new repository
- **GitLab**: Go to [gitlab.com](https://gitlab.com) and create a new repository
- **Bitbucket**: Go to [bitbucket.org](https://bitbucket.org) and create a new repository

### 2. Add Remote Origin
```bash
git remote add origin YOUR_NEW_REPO_URL
```

**Example:**
```bash
git remote add origin https://github.com/yourusername/dubai-rag-system.git
```

### 3. Push to New Repository
```bash
git push -u origin main
```

**Note:** If your default branch is `master` instead of `main`:
```bash
git push -u origin master
```

## 🔧 **Repository Configuration**

### Branch Naming Convention
- **Main branch**: `main` or `master`
- **Feature branches**: `feature/feature-name`
- **Bug fixes**: `fix/bug-description`
- **Hotfixes**: `hotfix/urgent-fix`

### Commit Message Format
```
Type: Brief description

- Detailed bullet points
- Additional context
- Related issues/tickets
```

**Examples:**
```
Feature: Add ML-powered market analysis

- Implemented automated reporting service
- Added market trend prediction
- Integrated with external data sources
- Resolves issue #123
```

```
Fix: Resolve backend startup issues

- Fixed ChromaDB connection problems
- Corrected import errors in ML services
- Improved error handling
- Closes issue #456
```

## 📁 **Project Structure Overview**

```
dubai-rag-system/
├── backend/                 # FastAPI backend
│   ├── ml/                 # Machine learning services
│   ├── auth/               # Authentication
│   ├── models/             # Database models
│   └── main.py             # Main application
├── frontend/               # React frontend
│   ├── src/                # Source code
│   └── package.json        # Dependencies
├── docker-compose.yml      # Docker configuration
├── env.example             # Environment template
├── README.md               # Project documentation
└── .gitignore              # Git ignore rules
```

## 🐳 **Docker Setup**

### Environment Configuration
1. **Copy environment template:**
   ```bash
   cp env.example .env
   ```

2. **Update environment variables:**
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/ragdb
   GOOGLE_API_KEY=your_google_api_key
   SECRET_KEY=your_secret_key
   ```

### Start Services
```bash
# Start all services
docker-compose up -d

# Check status
docker ps

# View logs
docker logs ragwebapp-backend-1
```

## 🧪 **Testing the Setup**

### Run Tests
```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

### Manual Testing
```bash
# Test script
python test_week1_fixes.py

# Docker test
./docker-test-blueprint2.bat
```

## 🔍 **Troubleshooting**

### Common Issues

#### Git Issues
```bash
# If you get "fatal: remote origin already exists"
git remote remove origin
git remote add origin YOUR_NEW_REPO_URL

# If you get "refusing to merge unrelated histories"
git pull origin main --allow-unrelated-histories
```

#### Docker Issues
```bash
# If containers won't start
docker-compose down
docker system prune -f
docker-compose up -d

# If backend is unhealthy
docker logs ragwebapp-backend-1
```

#### Python Issues
```bash
# If you get import errors
cd backend
python -m pip install -r requirements.txt

# If you get syntax errors
python -m py_compile main.py
```

## 📚 **Additional Resources**

- [Git Documentation](https://git-scm.com/doc)
- [Docker Documentation](https://docs.docker.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/docs/)

## 🆘 **Need Help?**

If you encounter any issues:

1. **Check the logs** for error messages
2. **Review this guide** for common solutions
3. **Check the main README.md** for project-specific information
4. **Create an issue** in your repository with detailed error information

---

**Happy coding! 🚀**
