# 🏠 Real Estate RAG Chat System

A comprehensive AI-powered chat system for real estate companies, built with FastAPI, React, and Google Gemini AI. This system provides intelligent property recommendations, policy information, and client assistance through a modern chat interface.

## 🚀 Features

- **AI-Powered Chat Interface**: Intelligent responses using Google Gemini AI
- **RAG (Retrieval-Augmented Generation)**: Combines property data with document knowledge
- **Property Database**: PostgreSQL database for property and client information
- **Document Processing**: ChromaDB for semantic search of company documents
- **Modern UI**: Beautiful React frontend with real-time chat
- **Docker Support**: Easy deployment with Docker Compose
- **Sample Data**: Pre-loaded with example properties and policies
- **Chat Persistence**: Chat history is automatically saved and restored across page refreshes
- **Role-Based Sessions**: Separate chat sessions for different user roles (client, agent, employee, admin)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  FastAPI Backend│    │   PostgreSQL    │
│   (Port 3000)   │◄──►│   (Port 8001)   │◄──►│   (Port 5432)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │    ChromaDB     │
                       │   (Port 8000)   │
                       └─────────────────┘
```

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **Docker Desktop** - [Download Docker](https://www.docker.com/products/docker-desktop/)
- **Git** - [Download Git](https://git-scm.com/)

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd real-estate-rag-app
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
# Copy the example environment file
cp env.example .env

# Edit the .env file with your Google API key
GOOGLE_API_KEY=your_google_api_key_here
DATABASE_URL=postgresql://admin:password123@localhost:5432/real_estate_db
CHROMA_HOST=localhost
CHROMA_PORT=8000
```

### 3. Get Your Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

### 4. Start the Application

#### Option A: Using Docker (Recommended)

```bash
# Start all services
docker-compose up --build

# The application will be available at:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8001
# API Documentation: http://localhost:8001/docs
```

#### Option B: Local Development

**Backend Setup:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL and ChromaDB (using Docker)
docker-compose up postgres chromadb -d

# Run data ingestion
cd scripts
python ingest_data.py

# Start backend
cd ../backend
python main.py
```

**Frontend Setup:**
```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm start
```

## 📊 Data Structure

### Properties Table
- `id`: Primary key
- `address`: Property address
- `price`: Listing price
- `bedrooms`: Number of bedrooms
- `bathrooms`: Number of bathrooms
- `square_feet`: Property size
- `property_type`: Type of property
- `description`: Property description

### Clients Table
- `id`: Primary key
- `name`: Client name
- `email`: Client email
- `phone`: Client phone
- `budget_min`: Minimum budget
- `budget_max`: Maximum budget
- `preferred_location`: Preferred area
- `requirements`: Client requirements

## 🤖 How the Enhanced RAG System Works

1. **Query Analysis**: System analyzes user intent, extracts entities, and identifies parameters
2. **Intent Classification**: Determines if query is about property search, market info, policies, or agent support
3. **Smart Context Retrieval**: Uses semantic search to find relevant documents and filtered property data
4. **Context Prioritization**: Ranks and prioritizes context items by relevance score
5. **Dynamic Prompt Generation**: Creates focused prompts based on query intent and user role
6. **AI Generation**: Google Gemini generates contextual, role-specific responses
7. **Response Delivery**: Returns intelligent responses with source attribution

### Key Improvements:
- **Query Understanding**: Extracts budget, location, property type, and other parameters
- **Intent-Based Routing**: Routes queries to appropriate data sources
- **Smart Filtering**: Only retrieves relevant properties instead of all properties
- **Context Scoring**: Prioritizes most relevant information
- **Role-Aware Responses**: Tailors responses to user role (client, agent, employee, admin)

## 🧪 Testing the System

Once the application is running, try these example queries:

### Chat Persistence Testing
- **Send a few messages** in the chat interface
- **Refresh the page** (F5 or Ctrl+R) - your chat history should be preserved
- **Switch between different roles** - each role maintains its own chat session
- **Test the clear chat button** - it should clear both current session and stored history

### Property Queries
- "Show me properties under $400,000"
- "I need a 3-bedroom house in the suburbs"
- "What luxury properties do you have?"
- "Show me condos in downtown"

### Policy Queries
- "What are your closing costs?"
- "How do I submit an offer?"
- "What's your virtual tour policy?"
- "Tell me about home staging services"

### Mixed Queries
- "I want to buy a house but need to know about financing requirements"
- "What's the process for buying a property over $500,000?"

## 🔧 API Endpoints

- `GET /` - Health check
- `GET /health` - System status
- `POST /api/chat` - Main chat endpoint
- `GET /api/properties` - List all properties
- `GET /api/clients` - List all clients

## 📁 Project Structure

```
real-estate-rag-app/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application
│   └── Dockerfile          # Backend container
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.js          # Main component
│   │   └── index.js        # Entry point
│   ├── public/             # Static files
│   └── Dockerfile          # Frontend container
├── scripts/                # Data processing
│   └── ingest_data.py      # Data ingestion script
├── data/                   # Sample data
│   ├── listings.csv        # Property data
│   ├── clients.csv         # Client data
│   └── documents/          # Company documents
├── docker-compose.yml      # Service orchestration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 Deployment

### Production Deployment

1. **Update Environment Variables**:
   - Use production database URLs
   - Set secure API keys
   - Configure CORS settings

2. **Build and Deploy**:
   ```bash
   docker-compose -f docker-compose.prod.yml up --build
   ```

3. **Set Up Monitoring**:
   - Configure logging
   - Set up health checks
   - Monitor API usage

## 🔒 Security Considerations

- Store API keys securely
- Use HTTPS in production
- Implement rate limiting
- Add authentication for production use
- Regular security updates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Port Already in Use**:
   ```bash
   # Check what's using the port
   netstat -ano | findstr :8001
   # Kill the process or change ports in docker-compose.yml
   ```

2. **Database Connection Issues**:
   - Ensure PostgreSQL is running
   - Check database credentials in `.env`
   - Verify network connectivity

3. **API Key Issues**:
   - Verify Google API key is correct
   - Check API key has proper permissions
   - Ensure billing is enabled on Google Cloud

4. **ChromaDB Issues**:
   - Check ChromaDB is running on port 8000
   - Verify collection exists
   - Check document ingestion completed

### Getting Help

- Check the logs: `docker-compose logs`
- Verify all services are running: `docker-compose ps`
- Test API endpoints: `curl http://localhost:8001/health`

## 🎯 Next Steps

- [ ] Add user authentication
- [ ] Implement file upload for documents
- [ ] Add property image support
- [ ] Create admin dashboard
- [ ] Add email notifications
- [ ] Implement chat history
- [ ] Add voice input support
- [ ] Create mobile app

---

**Built with ❤️ using FastAPI, React, and Google Gemini AI**
