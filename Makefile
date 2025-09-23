# Dubai Real Estate RAG Chat System - Development Makefile
# Convenient commands for local development and deployment

.PHONY: help build up down restart logs test lint clean install dev prod

# Default target
help: ## Show this help message
	@echo "Dubai Real Estate RAG Chat System - Development Commands"
	@echo "========================================================"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Examples:"
	@echo "  make dev          # Start development environment"
	@echo "  make test         # Run all tests"
	@echo "  make build        # Build Docker images"
	@echo "  make logs         # View application logs"

# =============================================================================
# ENVIRONMENT SETUP
# =============================================================================
install: ## Install dependencies and setup environment
	@echo "🔧 Setting up development environment..."
	@if [ ! -f .env ]; then \
		cp env.example .env; \
		echo "✅ Created .env file from env.example"; \
		echo "⚠️  Please update .env with your actual values"; \
	fi
	@python -m venv venv
	@echo "✅ Created virtual environment"
	@echo "📦 Installing Python dependencies..."
	@venv/Scripts/python.exe -m pip install --upgrade pip
	@venv/Scripts/python.exe -m pip install -r requirements.txt
	@echo "✅ Python dependencies installed"
	@echo "🎉 Environment setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Update .env file with your API keys and secrets"
	@echo "2. Run 'make dev' to start development environment"

# =============================================================================
# DOCKER COMMANDS
# =============================================================================
build: ## Build Docker images
	@echo "🔨 Building Docker images..."
	docker-compose build --no-cache
	@echo "✅ Docker images built successfully"

up: ## Start all services
	@echo "🚀 Starting all services..."
	docker-compose up -d
	@echo "✅ All services started"
	@echo ""
	@echo "Services available at:"
	@echo "  API:      http://localhost:8000"
	@echo "  Frontend: http://localhost:3000"
	@echo "  Database: localhost:5432"
	@echo "  Redis:    localhost:6379"
	@echo "  ChromaDB: http://localhost:8002"

down: ## Stop all services
	@echo "🛑 Stopping all services..."
	docker-compose down
	@echo "✅ All services stopped"

restart: ## Restart all services
	@echo "🔄 Restarting all services..."
	docker-compose restart
	@echo "✅ All services restarted"

logs: ## View application logs
	@echo "📋 Viewing application logs..."
	docker-compose logs -f

logs-api: ## View API logs only
	@echo "📋 Viewing API logs..."
	docker-compose logs -f api

logs-worker: ## View worker logs only
	@echo "📋 Viewing worker logs..."
	docker-compose logs -f worker

logs-db: ## View database logs only
	@echo "📋 Viewing database logs..."
	docker-compose logs -f db

# =============================================================================
# DEVELOPMENT COMMANDS
# =============================================================================
dev: ## Start development environment
	@echo "🚀 Starting development environment..."
	@if [ ! -f .env ]; then \
		echo "⚠️  .env file not found. Creating from env.example..."; \
		cp env.example .env; \
		echo "✅ Created .env file. Please update with your values."; \
	fi
	docker-compose up -d db redis chromadb
	@echo "⏳ Waiting for services to be ready..."
	@sleep 10
	@echo "✅ Development environment ready!"
	@echo ""
	@echo "To start the API server:"
	@echo "  make run-api"
	@echo ""
	@echo "To start the frontend:"
	@echo "  make run-frontend"

run-api: ## Run API server locally (requires venv)
	@echo "🚀 Starting API server..."
	@if [ ! -d "venv" ]; then \
		echo "❌ Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	venv/Scripts/python.exe -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

run-frontend: ## Run frontend locally
	@echo "🚀 Starting frontend..."
	cd frontend && npm install && npm start

# =============================================================================
# TESTING COMMANDS
# =============================================================================
test: ## Run all tests
	@echo "🧪 Running all tests..."
	@echo "Running backend tests..."
	@if [ -d "venv" ]; then \
		venv/Scripts/python.exe -m pytest backend/app/tests/ -v; \
	else \
		docker-compose exec api pytest app/tests/ -v; \
	fi
	@echo "Running frontend tests..."
	cd frontend && npm test -- --coverage --watchAll=false
	@echo "✅ All tests completed"

test-backend: ## Run backend tests only
	@echo "🧪 Running backend tests..."
	@if [ -d "venv" ]; then \
		venv/Scripts/python.exe -m pytest backend/app/tests/ -v; \
	else \
		docker-compose exec api pytest app/tests/ -v; \
	fi

test-frontend: ## Run frontend tests only
	@echo "🧪 Running frontend tests..."
	cd frontend && npm test -- --coverage --watchAll=false

test-integration: ## Run integration tests
	@echo "🧪 Running integration tests..."
	docker-compose exec api pytest app/tests/integration/ -v

# =============================================================================
# CODE QUALITY COMMANDS
# =============================================================================
lint: ## Run code linting and formatting
	@echo "🔍 Running code quality checks..."
	@echo "Running Black (code formatting)..."
	@if [ -d "venv" ]; then \
		venv/Scripts/python.exe -m black --check backend/; \
	else \
		docker-compose exec api black --check app/; \
	fi
	@echo "Running Flake8 (linting)..."
	@if [ -d "venv" ]; then \
		venv/Scripts/python.exe -m flake8 backend/; \
	else \
		docker-compose exec api flake8 app/; \
	fi
	@echo "Running ESLint (frontend)..."
	cd frontend && npm run lint
	@echo "✅ Code quality checks completed"

format: ## Format code with Black and isort
	@echo "🎨 Formatting code..."
	@if [ -d "venv" ]; then \
		venv/Scripts/python.exe -m black backend/; \
		venv/Scripts/python.exe -m isort backend/; \
	else \
		docker-compose exec api black app/; \
		docker-compose exec api isort app/; \
	fi
	@echo "✅ Code formatted"

# =============================================================================
# DATABASE COMMANDS
# =============================================================================
db-migrate: ## Run database migrations
	@echo "🗄️  Running database migrations..."
	docker-compose exec api python -c "from app.infrastructure.db.database_migrations import run_migrations; run_migrations()"
	@echo "✅ Database migrations completed"

db-reset: ## Reset database (WARNING: This will delete all data)
	@echo "⚠️  Resetting database (this will delete all data)..."
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ]
	docker-compose down
	docker volume rm real-estate-rag-chat-system_postgres_data || true
	docker-compose up -d db
	@sleep 10
	@make db-migrate
	@echo "✅ Database reset completed"

db-shell: ## Open database shell
	@echo "🗄️  Opening database shell..."
	docker-compose exec db psql -U admin -d real_estate_db

# =============================================================================
# PRODUCTION COMMANDS
# =============================================================================
prod: ## Start production environment
	@echo "🚀 Starting production environment..."
	docker-compose --profile production up -d
	@echo "✅ Production environment started"

prod-build: ## Build production images
	@echo "🔨 Building production images..."
	docker-compose --profile production build --no-cache
	@echo "✅ Production images built"

# =============================================================================
# UTILITY COMMANDS
# =============================================================================
clean: ## Clean up Docker resources
	@echo "🧹 Cleaning up Docker resources..."
	docker-compose down -v
	docker system prune -f
	docker volume prune -f
	@echo "✅ Cleanup completed"

clean-all: ## Clean up everything (including images)
	@echo "🧹 Cleaning up everything..."
	docker-compose down -v --rmi all
	docker system prune -af
	docker volume prune -f
	@echo "✅ Complete cleanup finished"

status: ## Show status of all services
	@echo "📊 Service Status:"
	@echo "=================="
	docker-compose ps

health: ## Check health of all services
	@echo "🏥 Health Check:"
	@echo "================"
	@echo "API Health:"
	@curl -s http://localhost:8000/health | python -m json.tool || echo "❌ API not responding"
	@echo ""
	@echo "Database Health:"
	@docker-compose exec db pg_isready -U admin -d real_estate_db || echo "❌ Database not responding"
	@echo ""
	@echo "Redis Health:"
	@docker-compose exec redis redis-cli ping || echo "❌ Redis not responding"

shell-api: ## Open shell in API container
	@echo "🐚 Opening API container shell..."
	docker-compose exec api /bin/bash

shell-db: ## Open shell in database container
	@echo "🐚 Opening database container shell..."
	docker-compose exec db /bin/bash

# =============================================================================
# BACKUP & RESTORE
# =============================================================================
backup: ## Backup database
	@echo "💾 Creating database backup..."
	@mkdir -p backups
	docker-compose exec db pg_dump -U admin real_estate_db > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Database backup created in backups/ directory"

restore: ## Restore database from backup (requires BACKUP_FILE variable)
	@echo "📥 Restoring database from backup..."
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "❌ Please specify BACKUP_FILE variable"; \
		echo "Usage: make restore BACKUP_FILE=backups/backup_20231201_120000.sql"; \
		exit 1; \
	fi
	docker-compose exec -T db psql -U admin -d real_estate_db < $(BACKUP_FILE)
	@echo "✅ Database restored from $(BACKUP_FILE)"

# =============================================================================
# MONITORING
# =============================================================================
monitor: ## Show real-time monitoring
	@echo "📊 Real-time monitoring (Press Ctrl+C to exit)..."
	docker-compose logs -f --tail=100

stats: ## Show container resource usage
	@echo "📊 Container Resource Usage:"
	@echo "============================"
	docker stats --no-stream

# =============================================================================
# DEVELOPMENT HELPERS
# =============================================================================
docs: ## Generate API documentation
	@echo "📚 Generating API documentation..."
	@if [ -d "venv" ]; then \
		venv/Scripts/python.exe -c "import webbrowser; webbrowser.open('http://localhost:8000/docs')"; \
	else \
		echo "📖 API documentation available at: http://localhost:8000/docs"; \
	fi

seed: ## Seed database with sample data
	@echo "🌱 Seeding database with sample data..."
	docker-compose exec api python -c "from app.infrastructure.integrations.populate_postgresql import seed_database; seed_database()"
	@echo "✅ Database seeded with sample data"

seed-properties: ## Seed demo properties (dev-only)
	@echo "🌱 Seeding demo properties (dev-only)..."
	docker-compose exec api python -m app.infrastructure.db.seed_properties
	@echo "✅ Demo properties seeded"

# =============================================================================
# QUICK COMMANDS
# =============================================================================
quick-start: install dev ## Quick start for new developers
	@echo "🎉 Quick start completed!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Update .env file with your API keys"
	@echo "2. Run 'make run-api' to start the API server"
	@echo "3. Visit http://localhost:8000/docs for API documentation"

quick-test: build up test down ## Quick test cycle
	@echo "✅ Quick test cycle completed"

# =============================================================================
# TROUBLESHOOTING
# =============================================================================
debug: ## Show debug information
	@echo "🐛 Debug Information:"
	@echo "===================="
	@echo "Docker version:"
	@docker --version
	@echo ""
	@echo "Docker Compose version:"
	@docker-compose --version
	@echo ""
	@echo "Python version:"
	@python --version
	@echo ""
	@echo "Node version:"
	@node --version
	@echo ""
	@echo "Environment file:"
	@if [ -f .env ]; then echo "✅ .env file exists"; else echo "❌ .env file missing"; fi
	@echo ""
	@echo "Virtual environment:"
	@if [ -d venv ]; then echo "✅ Virtual environment exists"; else echo "❌ Virtual environment missing"; fi
