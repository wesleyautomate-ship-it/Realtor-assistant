# Monitoring and Observability System

## Overview

This comprehensive monitoring and observability system provides enterprise-grade monitoring, error tracking, and analytics for the Dubai Real Estate RAG Chat System. It includes application performance monitoring, error tracking, log aggregation, health checks, and automated alerting.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Application   │    │   Prometheus    │    │     Grafana     │
│   (FastAPI)     │───▶│   (Metrics)     │───▶│  (Dashboards)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Error Tracker │    │ AlertManager    │    │   Log Aggregator│
│   (Sentry)      │    │ (Notifications) │    │   (ELK Stack)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Components

### 1. Application Performance Monitoring (APM)

**Files:**
- `application_metrics.py` - Custom Prometheus metrics
- `performance_monitor.py` - Performance monitoring service

**Features:**
- Real-time performance metrics collection
- Response time tracking
- Memory and CPU usage monitoring
- Database query performance
- External API call monitoring
- Custom business metrics

**Usage:**
```python
from monitoring.application_metrics import track_rag_query, track_llm_call

@track_rag_query("property_search")
async def search_properties(query: str):
    # Your RAG query logic
    pass

@track_llm_call("gemini")
async def generate_response(prompt: str):
    # Your LLM call logic
    pass
```

### 2. Error Tracking & Alerting

**Files:**
- `error_tracker.py` - Error tracking service
- `sentry_config.py` - Sentry integration
- `alert_manager.py` - Alert management system

**Features:**
- Real-time error detection and categorization
- Automatic alerting via email/Slack
- Error trend analysis
- Root cause analysis
- Incident response automation

**Usage:**
```python
from monitoring.error_tracker import track_error

try:
    # Your code
    pass
except Exception as e:
    await track_error(e, user_id=user_id, context={"operation": "rag_query"})
```

### 3. Log Aggregation

**Files:**
- `logging_config.py` - Structured logging configuration

**Features:**
- Structured JSON logging
- Log level filtering
- Log search and analysis
- Log retention policies
- Performance log analysis

**Usage:**
```python
from monitoring.logging_config import log_info, log_error

log_info("User query processed", user_id=user_id, query_type="property_search")
log_error("Database connection failed", error_code="DB_001")
```

### 4. Health Check Dashboards

**Files:**
- `health_checks.py` - Health check endpoints

**Features:**
- System health status monitoring
- Service availability checks
- Database connectivity monitoring
- External service status
- Performance metrics
- Public status page

**Endpoints:**
- `GET /monitoring/health` - Basic health check
- `GET /monitoring/health/detailed` - Detailed health check

### 5. Monitoring Infrastructure

**Files:**
- `docker-compose.monitoring.yml` - Monitoring services
- `prometheus.yml` - Prometheus configuration
- `grafana/dashboards/` - Grafana dashboard configurations
- `alertmanager/config.yml` - AlertManager configuration

## Quick Start

### 1. Environment Setup

Add these environment variables to your `.env` file:

```bash
# Monitoring Configuration
LOG_LEVEL=INFO
LOG_FORMAT=json
ENABLE_CONSOLE_LOGGING=true
ENABLE_FILE_LOGGING=true

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Sentry Configuration (Optional)
SENTRY_DSN=your_sentry_dsn_here
ENVIRONMENT=production

# SMTP Configuration (for email alerts)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Slack Configuration (for Slack alerts)
SLACK_WEBHOOK_URL=your_slack_webhook_url

# Alert Webhook (Optional)
ALERT_WEBHOOK_URL=your_webhook_url
```

### 2. Initialize Monitoring

In your FastAPI application:

```python
from fastapi import FastAPI
from monitoring.monitoring_manager import initialize_monitoring

app = FastAPI()

# Initialize monitoring
monitoring_config = {
    "redis_url": "redis://localhost:6379",
    "sentry_dsn": "your_sentry_dsn",
    "version": "1.0.0",
    "environment": "production"
}

monitoring_manager = initialize_monitoring(monitoring_config)
monitoring_manager.setup_fastapi_middleware(app)

@app.on_event("startup")
async def startup_event():
    await monitoring_manager.start_monitoring()

@app.on_event("shutdown")
async def shutdown_event():
    await monitoring_manager.stop_monitoring()
```

### 3. Start Monitoring Services

```bash
# Start monitoring infrastructure
docker-compose -f docker-compose.monitoring.yml up -d

# Access monitoring dashboards
# Grafana: http://localhost:3000 (admin/admin123)
# Prometheus: http://localhost:9090
# AlertManager: http://localhost:9093
```

## Monitoring Endpoints

### Application Metrics
- `GET /monitoring/metrics` - Prometheus metrics endpoint

### Health Checks
- `GET /monitoring/health` - Basic health check
- `GET /monitoring/health/detailed` - Detailed health check

### Alerts
- `GET /monitoring/alerts` - Get active alerts
- `GET /monitoring/alerts/summary` - Get alert summary

### Errors
- `GET /monitoring/errors` - Get recent errors

### Performance
- `GET /monitoring/performance` - Get performance report
- `GET /monitoring/performance/bottlenecks` - Get performance bottlenecks
- `GET /monitoring/performance/recommendations` - Get optimization recommendations

## Dashboards

### Grafana Dashboards

1. **RAG Application Overview** (`rag-overview.json`)
   - Request rate and response time
   - Error rates and active users
   - RAG queries and database connections
   - Memory and CPU usage

2. **System Health Dashboard**
   - System resource utilization
   - Service health status
   - Database and Redis metrics
   - External API health

3. **Error Analysis Dashboard**
   - Error trends and categories
   - Error distribution by severity
   - Error resolution tracking

## Alert Rules

The system includes comprehensive alert rules for:

- **Performance Alerts**
  - High CPU usage (>80%)
  - High memory usage (>85%)
  - High response time (>2s)
  - RAG query timeouts (>30s)

- **Error Alerts**
  - High error rate (>5%)
  - LLM API errors
  - Database connection issues
  - Service downtime

- **System Alerts**
  - Disk space low (<10%)
  - High cache miss rate (>20%)
  - Vector search performance issues

## Integration with Existing Code

### RAG Service Integration

```python
from monitoring.monitoring_manager import track_performance, track_error

class RAGService:
    async def query(self, question: str, user_id: str):
        start_time = time.time()
        try:
            # Your RAG query logic
            result = await self._process_query(question)
            
            # Track performance
            duration = time.time() - start_time
            await track_performance(
                operation="rag_query_property_search",
                duration=duration,
                success=True,
                metadata={"query_length": len(question), "result_count": len(result)},
                request_id=request_id
            )
            
            return result
            
        except Exception as e:
            # Track error
            await track_error(e, user_id=user_id, context={"operation": "rag_query"})
            raise
```

### Database Integration

```python
from monitoring.monitoring_manager import track_performance

async def get_properties(filters: dict):
    start_time = time.time()
    try:
        # Your database query
        result = await db.execute("SELECT * FROM properties WHERE ...")
        
        # Track performance
        duration = time.time() - start_time
        await track_performance(
            operation="db_query_properties",
            duration=duration,
            success=True,
            metadata={"filter_count": len(filters), "result_count": len(result)}
        )
        
        return result
        
    except Exception as e:
        await track_error(e, context={"operation": "db_query"})
        raise
```

## Best Practices

### 1. Error Handling
- Always wrap critical operations in try-catch blocks
- Use structured error tracking with context
- Categorize errors appropriately

### 2. Performance Monitoring
- Track all external API calls
- Monitor database query performance
- Track RAG-specific operations

### 3. Logging
- Use structured logging with relevant context
- Include user IDs and request IDs in logs
- Log at appropriate levels (INFO, WARNING, ERROR)

### 4. Alerting
- Set appropriate thresholds for alerts
- Use different severity levels
- Configure multiple notification channels

## Troubleshooting

### Common Issues

1. **Prometheus not scraping metrics**
   - Check if the application is exposing metrics on `/monitoring/metrics`
   - Verify Prometheus configuration in `prometheus.yml`

2. **Grafana dashboards not loading**
   - Check if Prometheus datasource is configured correctly
   - Verify dashboard JSON files are in the correct location

3. **Alerts not firing**
   - Check AlertManager configuration
   - Verify alert rules in `prometheus/rules/alerts.yml`
   - Check notification channel configurations

4. **High memory usage**
   - Monitor application memory usage
   - Check for memory leaks in long-running operations
   - Review database connection pooling

### Debug Commands

```bash
# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# Check AlertManager status
curl http://localhost:9093/api/v1/status

# Check application health
curl http://localhost:8000/monitoring/health

# Check application metrics
curl http://localhost:8000/monitoring/metrics
```

## Scaling Considerations

### Horizontal Scaling
- Use Redis for shared state across instances
- Configure Prometheus to scrape multiple application instances
- Use load balancer health checks

### Performance Optimization
- Use connection pooling for databases
- Implement caching strategies
- Monitor and optimize slow queries

### High Availability
- Deploy monitoring services in multiple availability zones
- Use persistent storage for Prometheus and Grafana
- Implement backup and recovery procedures

## Security Considerations

1. **Access Control**
   - Secure Grafana with authentication
   - Use HTTPS for all monitoring endpoints
   - Implement role-based access control

2. **Data Protection**
   - Sanitize sensitive data in logs
   - Use environment variables for secrets
   - Implement data retention policies

3. **Network Security**
   - Use internal networks for monitoring communication
   - Implement firewall rules
   - Use VPN for remote access

## Support and Maintenance

### Regular Maintenance Tasks
- Monitor disk space usage
- Review and update alert thresholds
- Clean up old logs and metrics
- Update monitoring dependencies

### Performance Tuning
- Adjust Prometheus retention settings
- Optimize Grafana dashboard queries
- Tune alert rule evaluation intervals

### Backup and Recovery
- Backup Prometheus data
- Export Grafana dashboards
- Document recovery procedures

## Contributing

When adding new monitoring features:

1. Follow the existing code structure
2. Add appropriate tests
3. Update documentation
4. Consider backward compatibility
5. Add relevant alert rules
6. Create Grafana dashboards if needed

## License

This monitoring system is part of the Dubai Real Estate RAG Chat System and follows the same licensing terms.
