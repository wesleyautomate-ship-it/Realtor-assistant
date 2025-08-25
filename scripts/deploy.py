#!/usr/bin/env python3
"""
Production deployment script for Dubai Real Estate RAG System
"""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path

class ProductionDeployer:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root / "frontend"
        self.deploy_dir = self.project_root / "deploy"
        
    def run_command(self, cmd, cwd=None, check=True):
        """Run a command and handle errors"""
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or self.project_root,
                capture_output=True,
                text=True,
                check=check
            )
            return result
        except subprocess.CalledProcessError as e:
            print(f"❌ Command failed: {' '.join(cmd)}")
            print(f"Error: {e.stderr}")
            return None
    
    def check_prerequisites(self):
        """Check if all prerequisites are met"""
        print("🔍 Checking prerequisites...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version < (3, 9):
            print("❌ Python 3.9+ required")
            return False
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Check Node.js
        node_result = self.run_command(["node", "--version"])
        if not node_result:
            print("❌ Node.js not found")
            return False
        print(f"✅ Node.js {node_result.stdout.strip()}")
        
        # Check npm
        npm_result = self.run_command(["npm", "--version"])
        if not npm_result:
            print("❌ npm not found")
            return False
        print(f"✅ npm {npm_result.stdout.strip()}")
        
        # Check Docker
        docker_result = self.run_command(["docker", "--version"])
        if not docker_result:
            print("❌ Docker not found")
            return False
        print(f"✅ Docker {docker_result.stdout.strip()}")
        
        # Check environment file
        env_file = self.project_root / ".env"
        if not env_file.exists():
            print("❌ .env file not found")
            return False
        print("✅ .env file found")
        
        return True
    
    def setup_backend(self):
        """Setup backend for production"""
        print("\n⚙️  Setting up backend...")
        
        # Install Python dependencies
        print("📦 Installing Python dependencies...")
        result = self.run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                                cwd=self.backend_dir)
        if not result:
            return False
        
        # Create production config
        print("⚙️  Creating production configuration...")
        prod_env_content = f"""# Production Environment Variables
DATABASE_URL=postgresql://admin:password123@localhost:5432/real_estate_db
CHROMA_HOST=localhost
CHROMA_PORT=8000
GOOGLE_API_KEY={os.getenv('GOOGLE_API_KEY', 'your-api-key-here')}
AI_MODEL=gemini-1.5-flash
HOST=0.0.0.0
PORT=8001
DEBUG=false
IS_PRODUCTION=true
LOG_LEVEL=INFO
REDIS_URL=redis://localhost:6379
CACHE_TTL=3600
MAX_WORKERS=4
BATCH_SIZE=100
SECRET_KEY=your-secret-key-here
"""
        
        prod_env_file = self.backend_dir / ".env.production"
        with open(prod_env_file, "w") as f:
            f.write(prod_env_content)
        
        print("✅ Backend setup completed")
        return True
    
    def setup_frontend(self):
        """Setup frontend for production"""
        print("\n🌐 Setting up frontend...")
        
        # Install Node.js dependencies
        print("📦 Installing Node.js dependencies...")
        result = self.run_command(["npm", "install"], cwd=self.frontend_dir)
        if not result:
            return False
        
        # Build for production
        print("🏗️  Building for production...")
        result = self.run_command(["npm", "run", "build"], cwd=self.frontend_dir)
        if not result:
            return False
        
        print("✅ Frontend setup completed")
        return True
    
    def create_docker_compose(self):
        """Create production Docker Compose file"""
        print("\n🐳 Creating Docker Compose configuration...")
        
        docker_compose_content = """version: '3.8'

services:
  postgres:
    image: postgres:15
    container_name: real_estate_postgres
    environment:
      POSTGRES_DB: real_estate_db
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  chromadb:
    image: chromadb/chroma:latest
    container_name: real_estate_chromadb
    ports:
      - "8000:8000"
    volumes:
      - chromadb_data:/chroma/chroma
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: real_estate_redis
    ports:
      - "6379:6379"
    restart: unless-stopped

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: real_estate_backend
    environment:
      - DATABASE_URL=postgresql://admin:password123@postgres:5432/real_estate_db
      - CHROMA_HOST=chromadb
      - CHROMA_PORT=8000
      - REDIS_URL=redis://redis:6379
    ports:
      - "8001:8001"
    depends_on:
      - postgres
      - chromadb
      - redis
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: real_estate_frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: real_estate_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
  chromadb_data:
"""
        
        docker_compose_file = self.project_root / "docker-compose.prod.yml"
        with open(docker_compose_file, "w") as f:
            f.write(docker_compose_content)
        
        print("✅ Docker Compose configuration created")
        return True
    
    def create_backend_dockerfile(self):
        """Create backend Dockerfile"""
        print("🐳 Creating backend Dockerfile...")
        
        dockerfile_content = """FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8001/health || exit 1

# Start application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
"""
        
        dockerfile_path = self.backend_dir / "Dockerfile"
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile_content)
        
        print("✅ Backend Dockerfile created")
        return True
    
    def create_frontend_dockerfile(self):
        """Create frontend Dockerfile"""
        print("🐳 Creating frontend Dockerfile...")
        
        dockerfile_content = """FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Build application
RUN npm run build

# Install serve
RUN npm install -g serve

# Expose port
EXPOSE 3000

# Start application
CMD ["serve", "-s", "build", "-l", "3000"]
"""
        
        dockerfile_path = self.frontend_dir / "Dockerfile"
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile_content)
        
        print("✅ Frontend Dockerfile created")
        return True
    
    def create_nginx_config(self):
        """Create Nginx configuration"""
        print("🌐 Creating Nginx configuration...")
        
        nginx_config = """events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8001;
    }

    upstream frontend {
        server frontend:3000;
    }

    server {
        listen 80;
        server_name localhost;

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Backend API
        location /api/ {
            proxy_pass http://backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health check
        location /health {
            proxy_pass http://backend/health;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
"""
        
        nginx_file = self.project_root / "nginx.conf"
        with open(nginx_file, "w") as f:
            f.write(nginx_config)
        
        print("✅ Nginx configuration created")
        return True
    
    def create_deployment_scripts(self):
        """Create deployment scripts"""
        print("📜 Creating deployment scripts...")
        
        # Start script
        start_script = """#!/bin/bash
echo "🚀 Starting Dubai Real Estate RAG System..."

# Start all services
docker-compose -f docker-compose.prod.yml up -d

echo "✅ Services started successfully!"
echo "📋 Service URLs:"
echo "   Frontend: http://localhost"
echo "   Backend:  http://localhost/api"
echo "   Health:   http://localhost/health"
"""
        
        start_file = self.project_root / "start.sh"
        with open(start_file, "w") as f:
            f.write(start_script)
        
        # Make executable
        os.chmod(start_file, 0o755)
        
        # Stop script
        stop_script = """#!/bin/bash
echo "🛑 Stopping Dubai Real Estate RAG System..."

# Stop all services
docker-compose -f docker-compose.prod.yml down

echo "✅ Services stopped successfully!"
"""
        
        stop_file = self.project_root / "stop.sh"
        with open(stop_file, "w") as f:
            f.write(stop_script)
        
        # Make executable
        os.chmod(stop_file, 0o755)
        
        print("✅ Deployment scripts created")
        return True
    
    def create_readme(self):
        """Create production README"""
        print("📖 Creating production README...")
        
        readme_content = """# Dubai Real Estate RAG System - Production Deployment

## Quick Start

1. **Start all services:**
   ```bash
   ./start.sh
   ```

2. **Stop all services:**
   ```bash
   ./stop.sh
   ```

3. **View logs:**
   ```bash
   docker-compose -f docker-compose.prod.yml logs -f
   ```

## Service URLs

- **Frontend:** http://localhost
- **Backend API:** http://localhost/api
- **Health Check:** http://localhost/health

## Configuration

### Environment Variables

Update the environment variables in `docker-compose.prod.yml` or create a `.env` file:

```env
DATABASE_URL=postgresql://admin:password123@postgres:5432/real_estate_db
CHROMA_HOST=chromadb
CHROMA_PORT=8000
GOOGLE_API_KEY=your-api-key-here
REDIS_URL=redis://redis:6379
```

### SSL/HTTPS

To enable HTTPS:

1. Place SSL certificates in the `ssl/` directory
2. Update `nginx.conf` to include SSL configuration
3. Update `docker-compose.prod.yml` to mount SSL certificates

## Monitoring

### Health Checks

- Backend: http://localhost/health
- Database: Check logs with `docker-compose logs postgres`
- ChromaDB: Check logs with `docker-compose logs chromadb`

### Logs

View logs for specific services:

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
```

## Backup

### Database Backup

```bash
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U admin real_estate_db > backup.sql
```

### Restore Database

```bash
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U admin real_estate_db < backup.sql
```

## Troubleshooting

### Common Issues

1. **Port conflicts:** Ensure ports 80, 3000, 8000, 8001, 5432, 6379 are available
2. **Memory issues:** Increase Docker memory allocation
3. **API key issues:** Verify GOOGLE_API_KEY is set correctly

### Reset Everything

```bash
# Stop and remove all containers and volumes
docker-compose -f docker-compose.prod.yml down -v

# Remove all images
docker rmi $(docker images -q)

# Start fresh
./start.sh
```

## Security

- Change default passwords in production
- Use SSL certificates for HTTPS
- Configure firewall rules
- Regular security updates
- Monitor logs for suspicious activity
"""
        
        readme_file = self.project_root / "README_PROD.md"
        with open(readme_file, "w") as f:
            f.write(readme_content)
        
        print("✅ Production README created")
        return True
    
    def deploy(self):
        """Run complete deployment"""
        print("🚀 Starting production deployment...")
        print("=" * 50)
        
        # Check prerequisites
        if not self.check_prerequisites():
            print("❌ Prerequisites not met")
            return False
        
        # Setup backend
        if not self.setup_backend():
            print("❌ Backend setup failed")
            return False
        
        # Setup frontend
        if not self.setup_frontend():
            print("❌ Frontend setup failed")
            return False
        
        # Create Docker configurations
        if not self.create_docker_compose():
            print("❌ Docker Compose creation failed")
            return False
        
        if not self.create_backend_dockerfile():
            print("❌ Backend Dockerfile creation failed")
            return False
        
        if not self.create_frontend_dockerfile():
            print("❌ Frontend Dockerfile creation failed")
            return False
        
        # Create Nginx configuration
        if not self.create_nginx_config():
            print("❌ Nginx configuration creation failed")
            return False
        
        # Create deployment scripts
        if not self.create_deployment_scripts():
            print("❌ Deployment scripts creation failed")
            return False
        
        # Create README
        if not self.create_readme():
            print("❌ README creation failed")
            return False
        
        print("\n" + "=" * 50)
        print("🎉 Production deployment setup completed!")
        print("\n📋 Next steps:")
        print("1. Update environment variables in docker-compose.prod.yml")
        print("2. Run: ./start.sh")
        print("3. Access the application at: http://localhost")
        print("\n📚 See README_PROD.md for detailed instructions")
        
        return True

def main():
    """Main function"""
    deployer = ProductionDeployer()
    
    if deployer.deploy():
        print("\n✅ Deployment successful!")
    else:
        print("\n❌ Deployment failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
