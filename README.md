# Dubai Real Estate RAG System

A comprehensive AI-powered real estate assistant for Dubai property professionals.

## Quick Start

1. **Setup Database:**
   ```bash
   python scripts/setup_database.py
   ```

2. **Start Services:**
   ```bash
   python scripts/start_services.py
   ```

3. **Run Tests:**
   ```bash
   python scripts/test_system.py
   ```

4. **Deploy to Production:**
   ```bash
   python scripts/deploy.py
   ```

## Documentation

- [Project Overview](docs/PROJECT_OVERVIEW.md)
- [Production Deployment](docs/README_PROD.md)
- [TODO List](docs/TODO_CONSOLIDATED.md)

## Architecture

- **Backend:** FastAPI + PostgreSQL + ChromaDB + Google Gemini AI
- **Frontend:** React + Material-UI
- **AI:** Retrieval-Augmented Generation (RAG) with improved prompts
- **Performance:** Redis caching + batch processing

## Features

- 🤖 AI-powered property search and analysis
- 🏢 Dubai-specific real estate knowledge
- 👥 Role-based user experience (Client/Agent)
- 📊 Market trends and insights
- 🔍 Advanced property filtering
- 💾 Comprehensive data ingestion
- ⚡ High-performance caching
- 🐳 Production-ready Docker deployment

## Development

```bash
# Install dependencies
cd backend && pip install -r requirements.txt
cd frontend && npm install

# Start development servers
python scripts/start_services.py
```

## Production

```bash
# Deploy to production
python scripts/deploy.py

# Start production services
./start.sh
```

## Support

For issues and questions, please check the documentation in the `docs/` directory.
