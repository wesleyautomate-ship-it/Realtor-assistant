
# Dubai Real Estate RAG System

A comprehensive AI-powered real estate platform that combines Retrieval-Augmented Generation (RAG) with advanced machine learning capabilities for Dubai's real estate market.

## 🏗️ **Project Overview**

This system provides an intelligent platform for real estate professionals to:
- **Analyze market trends** using AI-powered insights
- **Generate property reports** with automated data processing
- **Manage client interactions** through intelligent chatbots
- **Predict market movements** using advanced ML models
- **Streamline workflows** with automated task management

## 🚀 **Quick Start**

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- Git

### 1. Clone the Repository
```bash
git clone <your-new-repository-url>
cd "RAG web app"
```

### 2. Environment Setup
```bash
# Copy environment template
cp env.example .env

# Update with your configuration
# Required: DATABASE_URL, GOOGLE_API_KEY, SECRET_KEY
```

### 3. Start the System
```bash
# Start all services
docker-compose up -d

# Check status
docker ps

# View logs
docker logs ragwebapp-backend-1
```

### 4. Access the System
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8003
- **API Documentation**: http://localhost:8003/docs
- **Database**: localhost:5432

## 🏗️ **Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Database      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (PostgreSQL)  │
│   Port: 3000    │    │   Port: 8003    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   ML Services   │
                       │   (Advanced)    │
                       │   (Reporting)   │
                       │   (Analytics)   │
                       └─────────────────┘
```

## 📁 **Project Structure**

```
├── backend/                 # FastAPI backend services
│   ├── ml/                 # Machine learning services
│   ├── auth/               # Authentication & authorization
│   ├── models/             # Database models
│   └── main.py             # Main application entry point
├── frontend/               # React frontend application
│   ├── src/                # Source code
│   ├── public/             # Static assets
│   └── package.json        # Dependencies
├── docker-compose.yml      # Docker services configuration
├── env.example             # Environment variables template
└── README.md               # This file
```

## 🔧 **Development**

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8003
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 🐳 **Docker Commands**

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Rebuild and start
docker-compose up -d --build

# View logs
docker-compose logs -f

# Check service status
docker-compose ps
```

## 📊 **System Status**

| Component | Status | Description |
|-----------|--------|-------------|
| **Backend API** | ✅ Operational | FastAPI server with ML services |
| **Database** | ✅ Connected | PostgreSQL with optimized schema |
| **ChromaDB** | ✅ Connected | Vector database for embeddings |
| **ML Services** | ✅ Active | Advanced analytics and reporting |
| **Frontend** | ✅ Running | React application |
| **Redis** | ✅ Connected | Session and cache management |

## 🔐 **Environment Variables**

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ragdb

# API Keys
GOOGLE_API_KEY=your_google_api_key
SECRET_KEY=your_secret_key

# Services
REDIS_URL=redis://localhost:6379
CHROMA_HOST=localhost
CHROMA_PORT=8000
```

## 🧪 **Testing**

### Automated Testing
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest test_ml_infrastructure.py

# Run with coverage
python -m pytest --cov=backend
```

### Manual Testing
```bash
# Test script
python test_week1_fixes.py

# Docker test
./docker-test-blueprint2.bat
```

## 📚 **Documentation**

- [API Documentation](http://localhost:8003/docs) - Interactive API docs
- [System Architecture](docs/ARCHITECTURE.md) - Detailed system design
- [Development Guide](docs/DEVELOPMENT.md) - Development setup and guidelines
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment instructions

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 **Support**

For support and questions:
- Create an issue in the repository
- Check the [documentation](docs/)
- Review the [troubleshooting guide](docs/TROUBLESHOOTING.md)

## 🗺️ **Roadmap**

- [ ] Enhanced ML model training
- [ ] Real-time market data integration
- [ ] Mobile application
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] API rate limiting and security
- [ ] Performance optimization
- [ ] Comprehensive testing suite

---

**Built with ❤️ for the Dubai Real Estate Community**
