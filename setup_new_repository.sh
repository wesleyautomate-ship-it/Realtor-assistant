#!/bin/bash

echo "========================================"
echo "  Dubai RAG System - Repository Setup"
echo "========================================"
echo

echo "[1/5] Cleaning up old Git configuration..."
if [ -d ".git" ]; then
    echo "Removing old Git repository..."
    rm -rf .git
    echo "Old Git repository removed."
else
    echo "No existing Git repository found."
fi

echo
echo "[2/5] Initializing new Git repository..."
git init
echo "New Git repository initialized."

echo
echo "[3/5] Adding all files to Git..."
git add .
echo "Files added to staging area."

echo
echo "[4/5] Creating initial commit..."
git commit -m "Initial commit: Dubai RAG System

- AI-powered real estate platform
- FastAPI backend with ML services
- React frontend
- Docker containerization
- PostgreSQL database
- ChromaDB vector database
- Redis caching
- Comprehensive testing suite"
echo "Initial commit created."

echo
echo "[5/5] Repository setup complete!"
echo
echo "Next steps:"
echo "1. Create a new repository on GitHub/GitLab/etc."
echo "2. Add the remote origin:"
echo "   git remote add origin YOUR_NEW_REPO_URL"
echo "3. Push to the new repository:"
echo "   git push -u origin main"
echo
echo "========================================"
