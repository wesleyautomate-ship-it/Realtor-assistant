# Dubai Real Estate RAG Chat System - Deployment Guide

## 📖 **Table of Contents**
1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Application Deployment](#application-deployment)
4. [Database Setup](#database-setup)
5. [SSL Configuration](#ssl-configuration)
6. [Monitoring & Maintenance](#monitoring--maintenance)
7. [Troubleshooting](#troubleshooting)
8. [Security Considerations](#security-considerations)

---

## ✅ **Prerequisites**

### **System Requirements**
- **Operating System**: Ubuntu 20.04 LTS or higher
- **CPU**: 4+ cores (8+ cores recommended for production)
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 100GB+ SSD storage
- **Network**: High-speed internet connection
- **Domain**: Registered domain name for SSL

### **Software Requirements**
- **Docker**: 20.10+ with Docker Compose
- **Nginx**: Web server and reverse proxy
- **Git**: Version control system
- **SSH Access**: Secure shell access to server

### **External Services**
- **Google Gemini API**: AI service provider
- **Domain Registrar**: For domain management
- **SSL Certificate**: Let's Encrypt or commercial certificate

---

## 🛠️ **Environment Setup**

### **1. Server Initialization**

#### **Update System**
```bash
# Update package list and upgrade existing packages
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y curl wget git unzip software-properties-common apt-transport-https ca-certificates gnupg lsb-release
```

#### **Create Deployment User**
```bash
# Create deployment user
sudo adduser deploy
sudo usermod -aG sudo deploy

# Switch to deployment user
su - deploy
```

### **2. Docker Installation**

#### **Install Docker**
```bash
# Download and run Docker installation script
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Start and enable Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Verify installation
docker --version
```

#### **Install Docker Compose**
```bash
# Download Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make executable
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version
```

### **3. Nginx Installation**

#### **Install Nginx**
```bash
# Install Nginx
sudo apt install -y nginx

# Start and enable Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Verify installation
sudo nginx -t
```

#### **Configure Firewall**
```bash
# Allow SSH, HTTP, and HTTPS
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable

# Verify firewall status
sudo ufw status
```

---

## 🚀 **Application Deployment**

### **1. Repository Setup**

#### **Clone Application**
```bash
# Navigate to deployment directory
cd /opt

# Clone repository
sudo git clone <repository-url> rag-web-app
sudo chown -R deploy:deploy rag-web-app
cd rag-web-app
```

#### **Configure Environment**
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

#### **Environment Configuration (.env)**
```env
# Application Configuration
DEBUG=False
HOST=0.0.0.0
PORT=8001
SECRET_KEY=your_very_secure_secret_key_here

# Database Configuration
DATABASE_URL=postgresql://admin:secure_password_here@postgres:5432/real_estate_db

# ChromaDB Configuration
CHROMA_HOST=chromadb
CHROMA_PORT=8000

# AI Service Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Frontend Configuration
REACT_APP_API_URL=https://your-domain.com/api
REACT_APP_VERSION=1.2.0

# Production Settings
LOG_LEVEL=INFO
CORS_ORIGINS=https://your-domain.com
```

### **2. Docker Compose Configuration**

#### **Production Docker Compose (docker-compose.prod.yml)**
```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:14
    container_name: rag_postgres
    environment:
      POSTGRES_DB: real_estate_db
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secure_password_here
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    ports:
      - "5432:5432"
    restart: unless-stopped
    networks:
      - rag_network

  # ChromaDB Vector Database
  chromadb:
    image: chromadb/chroma:latest
    container_name: rag_chromadb
    environment:
      - CHROMA_SERVER_HOST=0.0.0.0
      - CHROMA_SERVER_HTTP_PORT=8000
    volumes:
      - chromadb_data:/chroma/chroma
    ports:
      - "8000:8000"
    restart: unless-stopped
    networks:
      - rag_network

  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    container_name: rag_backend
    environment:
      - DATABASE_URL=postgresql://admin:secure_password_here@postgres:5432/real_estate_db
      - CHROMA_HOST=chromadb
      - CHROMA_PORT=8000
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - DEBUG=False
      - HOST=0.0.0.0
      - PORT=8001
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    ports:
      - "8001:8001"
    depends_on:
      - postgres
      - chromadb
    restart: unless-stopped
    networks:
      - rag_network

  # Frontend Application
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    container_name: rag_frontend
    environment:
      - REACT_APP_API_URL=https://your-domain.com/api
      - REACT_APP_VERSION=1.2.0
    ports:
      - "3000:80"
    depends_on:
      - backend
    restart: unless-stopped
    networks:
      - rag_network

  # Redis Cache (Optional)
  redis:
    image: redis:7-alpine
    container_name: rag_redis
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    restart: unless-stopped
    networks:
      - rag_network

volumes:
  postgres_data:
  chromadb_data:
  redis_data:

networks:
  rag_network:
    driver: bridge
```

### **3. Build and Deploy**

#### **Build Application**
```bash
# Build all services
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Check service status
docker-compose -f docker-compose.prod.yml ps
```

#### **Initialize Database**
```bash
# Run database migrations
docker-compose -f docker-compose.prod.yml exec backend python scripts/dubai_database_migration.py

# Load initial data
docker-compose -f docker-compose.prod.yml exec backend python scripts/dubai_research_ingestion.py

# Verify data loading
docker-compose -f docker-compose.prod.yml exec backend python scripts/verify_data.py
```

---

## 🗄️ **Database Setup**

### **1. PostgreSQL Configuration**

#### **Database Optimization**
```sql
-- Connect to PostgreSQL
docker-compose -f docker-compose.prod.yml exec postgres psql -U admin -d real_estate_db

-- Create indexes for better performance
CREATE INDEX idx_properties_location ON properties(location);
CREATE INDEX idx_properties_price ON properties(price);
CREATE INDEX idx_properties_neighborhood ON properties(neighborhood);
CREATE INDEX idx_market_data_area ON market_data(area);
CREATE INDEX idx_regulatory_updates_type ON regulatory_updates(regulation_type);

-- Optimize PostgreSQL settings
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;

-- Reload configuration
SELECT pg_reload_conf();
```

#### **Backup Configuration**
```bash
# Create backup script
cat > /opt/rag-web-app/backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/rag-web-app/backups"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup PostgreSQL
docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump -U admin real_estate_db > $BACKUP_DIR/postgres_backup_$DATE.sql

# Backup ChromaDB
docker-compose -f docker-compose.prod.yml exec chromadb tar -czf - /chroma/chroma > $BACKUP_DIR/chromadb_backup_$DATE.tar.gz

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
EOF

# Make executable
chmod +x /opt/rag-web-app/backup.sh

# Add to crontab for daily backups
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/rag-web-app/backup.sh") | crontab -
```

### **2. ChromaDB Configuration**

#### **Performance Optimization**
```python
# ChromaDB configuration for production
import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="/chroma/chroma",
    anonymized_telemetry=False
))
```

---

## 🔒 **SSL Configuration**

### **1. Domain Configuration**

#### **DNS Setup**
```bash
# Add A record pointing to your server IP
# your-domain.com -> YOUR_SERVER_IP
# www.your-domain.com -> YOUR_SERVER_IP
```

#### **Verify Domain Resolution**
```bash
# Test domain resolution
nslookup your-domain.com
ping your-domain.com
```

### **2. Let's Encrypt SSL**

#### **Install Certbot**
```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Stop Nginx temporarily
sudo systemctl stop nginx
```

#### **Obtain SSL Certificate**
```bash
# Get SSL certificate
sudo certbot certonly --standalone -d your-domain.com -d www.your-domain.com

# Verify certificate
sudo certbot certificates
```

#### **Auto-renewal Setup**
```bash
# Test auto-renewal
sudo certbot renew --dry-run

# Add to crontab for auto-renewal
(crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -
```

### **3. Nginx SSL Configuration**

#### **SSL Configuration File**
```nginx
# /etc/nginx/sites-available/rag-web-app
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeout settings
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Static files
    location /static {
        alias /opt/rag-web-app/frontend/build/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;
}
```

#### **Enable Site**
```bash
# Create symlink
sudo ln -s /etc/nginx/sites-available/rag-web-app /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

---

## 📊 **Monitoring & Maintenance**

### **1. Health Monitoring**

#### **Health Check Script**
```bash
# Create health check script
cat > /opt/rag-web-app/health_check.sh << 'EOF'
#!/bin/bash

# Check if services are running
check_service() {
    local service=$1
    if docker-compose -f docker-compose.prod.yml ps $service | grep -q "Up"; then
        echo "✅ $service is running"
        return 0
    else
        echo "❌ $service is not running"
        return 1
    fi
}

# Check API health
check_api() {
    local response=$(curl -s -o /dev/null -w "%{http_code}" https://your-domain.com/api/health)
    if [ $response -eq 200 ]; then
        echo "✅ API is healthy"
        return 0
    else
        echo "❌ API health check failed: $response"
        return 1
    fi
}

# Check database connectivity
check_database() {
    if docker-compose -f docker-compose.prod.yml exec -T postgres pg_isready -U admin; then
        echo "✅ Database is accessible"
        return 0
    else
        echo "❌ Database connectivity failed"
        return 1
    fi
}

# Run all checks
echo "=== Health Check $(date) ==="
check_service backend
check_service frontend
check_service postgres
check_service chromadb
check_api
check_database
echo "=========================="
EOF

# Make executable
chmod +x /opt/rag-web-app/health_check.sh

# Add to crontab for hourly checks
(crontab -l 2>/dev/null; echo "0 * * * * /opt/rag-web-app/health_check.sh >> /var/log/health_check.log 2>&1") | crontab -
```

#### **Log Monitoring**
```bash
# Create log monitoring script
cat > /opt/rag-web-app/monitor_logs.sh << 'EOF'
#!/bin/bash

# Monitor application logs
docker-compose -f docker-compose.prod.yml logs --tail=100 backend | grep -i error
docker-compose -f docker-compose.prod.yml logs --tail=100 frontend | grep -i error

# Check disk usage
df -h | grep -E "(/$|/opt)"

# Check memory usage
free -h

# Check CPU usage
top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1
EOF

chmod +x /opt/rag-web-app/monitor_logs.sh
```

### **2. Performance Monitoring**

#### **Resource Monitoring**
```bash
# Install monitoring tools
sudo apt install -y htop iotop nethogs

# Monitor system resources
htop
iotop
nethogs
```

#### **Application Metrics**
```bash
# Check container resource usage
docker stats

# Monitor API response times
curl -w "@curl-format.txt" -o /dev/null -s "https://your-domain.com/api/health"
```

### **3. Maintenance Tasks**

#### **Regular Maintenance Script**
```bash
# Create maintenance script
cat > /opt/rag-web-app/maintenance.sh << 'EOF'
#!/bin/bash

echo "=== Maintenance $(date) ==="

# Clean up old Docker images
docker image prune -f

# Clean up old containers
docker container prune -f

# Clean up old volumes
docker volume prune -f

# Restart services weekly
if [ $(date +%u) -eq 1 ]; then
    echo "Weekly restart of services..."
    docker-compose -f docker-compose.prod.yml restart
fi

# Update application (if needed)
# git pull origin main
# docker-compose -f docker-compose.prod.yml build
# docker-compose -f docker-compose.prod.yml up -d

echo "Maintenance completed"
EOF

chmod +x /opt/rag-web-app/maintenance.sh

# Add to crontab for daily maintenance
(crontab -l 2>/dev/null; echo "0 3 * * * /opt/rag-web-app/maintenance.sh >> /var/log/maintenance.log 2>&1") | crontab -
```

---

## 🔧 **Troubleshooting**

### **1. Common Issues**

#### **Service Not Starting**
```bash
# Check service logs
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml logs frontend

# Check service status
docker-compose -f docker-compose.prod.yml ps

# Restart specific service
docker-compose -f docker-compose.prod.yml restart backend
```

#### **Database Connection Issues**
```bash
# Check database connectivity
docker-compose -f docker-compose.prod.yml exec postgres pg_isready -U admin

# Check database logs
docker-compose -f docker-compose.prod.yml logs postgres

# Connect to database
docker-compose -f docker-compose.prod.yml exec postgres psql -U admin -d real_estate_db
```

#### **SSL Certificate Issues**
```bash
# Check certificate status
sudo certbot certificates

# Renew certificate manually
sudo certbot renew

# Check Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### **2. Performance Issues**

#### **High CPU Usage**
```bash
# Check CPU usage by container
docker stats

# Check system CPU usage
top

# Identify resource-intensive processes
ps aux --sort=-%cpu | head -10
```

#### **High Memory Usage**
```bash
# Check memory usage
free -h

# Check container memory usage
docker stats --no-stream

# Restart services if needed
docker-compose -f docker-compose.prod.yml restart
```

#### **Slow Response Times**
```bash
# Check API response times
curl -w "@curl-format.txt" -o /dev/null -s "https://your-domain.com/api/health"

# Check database query performance
docker-compose -f docker-compose.prod.yml exec postgres psql -U admin -d real_estate_db -c "SELECT * FROM pg_stat_activity;"

# Check Nginx access logs
sudo tail -f /var/log/nginx/access.log
```

### **3. Recovery Procedures**

#### **Service Recovery**
```bash
# Restart all services
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d

# Check service health
/opt/rag-web-app/health_check.sh
```

#### **Database Recovery**
```bash
# Restore from backup
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U admin -d real_estate_db < /opt/rag-web-app/backups/postgres_backup_YYYYMMDD_HHMMSS.sql

# Reinitialize data
docker-compose -f docker-compose.prod.yml exec backend python scripts/dubai_research_ingestion.py
```

#### **Full System Recovery**
```bash
# Stop all services
docker-compose -f docker-compose.prod.yml down

# Backup current state
/opt/rag-web-app/backup.sh

# Restart from scratch
docker-compose -f docker-compose.prod.yml up -d

# Reinitialize everything
docker-compose -f docker-compose.prod.yml exec backend python scripts/dubai_database_migration.py
docker-compose -f docker-compose.prod.yml exec backend python scripts/dubai_research_ingestion.py
```

---

## 🔐 **Security Considerations**

### **1. Network Security**

#### **Firewall Configuration**
```bash
# Configure UFW firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable

# Check firewall status
sudo ufw status verbose
```

#### **SSH Security**
```bash
# Edit SSH configuration
sudo nano /etc/ssh/sshd_config

# Recommended settings:
# Port 22 (or custom port)
# PermitRootLogin no
# PasswordAuthentication no
# PubkeyAuthentication yes
# MaxAuthTries 3
# ClientAliveInterval 300
# ClientAliveCountMax 2

# Restart SSH service
sudo systemctl restart ssh
```

### **2. Application Security**

#### **Environment Variables**
```bash
# Use strong passwords and keys
# Generate secure secret key
openssl rand -hex 32

# Use environment-specific configurations
# Never commit .env files to version control
```

#### **Container Security**
```bash
# Run containers as non-root user
# Use specific image tags (not 'latest')
# Regularly update base images
# Scan images for vulnerabilities
```

### **3. Data Security**

#### **Database Security**
```sql
-- Use strong passwords
-- Limit database access
-- Enable SSL connections
-- Regular security updates
```

#### **Backup Security**
```bash
# Encrypt backups
# Store backups securely
# Test backup restoration
# Monitor backup success
```

---

## 📋 **Deployment Checklist**

### **Pre-Deployment**
- [ ] Server requirements met
- [ ] Domain configured
- [ ] SSL certificate obtained
- [ ] Environment variables configured
- [ ] Database backup strategy in place

### **Deployment**
- [ ] Application built and deployed
- [ ] Database initialized
- [ ] SSL configured
- [ ] Nginx configured
- [ ] Services running

### **Post-Deployment**
- [ ] Health checks passing
- [ ] SSL certificate working
- [ ] Monitoring configured
- [ ] Backup system tested
- [ ] Security measures implemented

### **Ongoing Maintenance**
- [ ] Regular backups
- [ ] Security updates
- [ ] Performance monitoring
- [ ] Log monitoring
- [ ] SSL certificate renewal

---

**Last Updated**: August 2024  
**Version**: 1.2.0  
**Maintainer**: DevOps Team  
**Contact**: devops@dubairealestate.com


