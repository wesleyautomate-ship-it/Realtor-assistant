"""
Custom application metrics for RAG Real Estate System
"""
import time
import functools
from typing import Dict, Any, Optional
from prometheus_client import (
    Counter, Histogram, Gauge, Summary, 
    generate_latest, CONTENT_TYPE_LATEST,
    CollectorRegistry, multiprocess
)
from fastapi import Request, Response
import psutil
import asyncio
from contextlib import asynccontextmanager

# Initialize Prometheus registry
registry = CollectorRegistry()
multiprocess.MultiProcessCollector(registry)

# HTTP Metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status'],
    registry=registry
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    registry=registry
)

# RAG-specific Metrics
rag_queries_total = Counter(
    'rag_queries_total',
    'Total RAG queries processed',
    ['query_type', 'status'],
    registry=registry
)

rag_query_duration_seconds = Histogram(
    'rag_query_duration_seconds',
    'RAG query processing duration',
    ['query_type'],
    registry=registry
)

rag_vector_search_duration_seconds = Histogram(
    'rag_vector_search_duration_seconds',
    'Vector search duration',
    ['collection_name'],
    registry=registry
)

rag_llm_calls_total = Counter(
    'rag_llm_calls_total',
    'Total LLM API calls',
    ['model', 'status'],
    registry=registry
)

rag_llm_response_time_seconds = Histogram(
    'rag_llm_response_time_seconds',
    'LLM response time',
    ['model'],
    registry=registry
)

# Database Metrics
db_connections_active = Gauge(
    'db_connections_active',
    'Active database connections',
    ['database'],
    registry=registry
)

db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Database query duration',
    ['query_type'],
    registry=registry
)

# Cache Metrics
cache_hits_total = Counter(
    'cache_hits_total',
    'Total cache hits',
    ['cache_type'],
    registry=registry
)

cache_misses_total = Counter(
    'cache_misses_total',
    'Total cache misses',
    ['cache_type'],
    registry=registry
)

# User Activity Metrics
active_users = Gauge(
    'rag_active_users',
    'Number of active users',
    registry=registry
)

user_sessions_total = Counter(
    'user_sessions_total',
    'Total user sessions',
    ['user_type'],
    registry=registry
)

# File Processing Metrics
files_processed_total = Counter(
    'files_processed_total',
    'Total files processed',
    ['file_type', 'status'],
    registry=registry
)

file_processing_duration_seconds = Histogram(
    'file_processing_duration_seconds',
    'File processing duration',
    ['file_type'],
    registry=registry
)

# System Metrics
memory_usage_bytes = Gauge(
    'memory_usage_bytes',
    'Memory usage in bytes',
    registry=registry
)

cpu_usage_percent = Gauge(
    'cpu_usage_percent',
    'CPU usage percentage',
    registry=registry
)

# Business Metrics
property_queries_total = Counter(
    'property_queries_total',
    'Total property-related queries',
    ['query_category'],
    registry=registry
)

market_analysis_queries_total = Counter(
    'market_analysis_queries_total',
    'Total market analysis queries',
    ['analysis_type'],
    registry=registry
)

class MetricsMiddleware:
    """FastAPI middleware for collecting HTTP metrics"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        start_time = time.time()
        method = scope["method"]
        path = scope["path"]
        
        # Track request
        try:
            await self.app(scope, receive, send)
            status = 200  # Default success status
        except Exception as e:
            status = 500
            raise
        finally:
            duration = time.time() - start_time
            
            # Record metrics
            http_requests_total.labels(method=method, endpoint=path, status=status).inc()
            http_request_duration_seconds.labels(method=method, endpoint=path).observe(duration)

class MetricsCollector:
    """Collector for system and application metrics"""
    
    @staticmethod
    def collect_system_metrics():
        """Collect system-level metrics"""
        # Memory usage
        memory = psutil.virtual_memory()
        memory_usage_bytes.set(memory.used)
        
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_usage_percent.set(cpu_percent)
    
    @staticmethod
    def track_rag_query(query_type: str, duration: float, status: str = "success"):
        """Track RAG query metrics"""
        rag_queries_total.labels(query_type=query_type, status=status).inc()
        rag_query_duration_seconds.labels(query_type=query_type).observe(duration)
    
    @staticmethod
    def track_vector_search(collection_name: str, duration: float):
        """Track vector search metrics"""
        rag_vector_search_duration_seconds.labels(collection_name=collection_name).observe(duration)
    
    @staticmethod
    def track_llm_call(model: str, duration: float, status: str = "success"):
        """Track LLM API call metrics"""
        rag_llm_calls_total.labels(model=model, status=status).inc()
        rag_llm_response_time_seconds.labels(model=model).observe(duration)
    
    @staticmethod
    def track_db_query(query_type: str, duration: float):
        """Track database query metrics"""
        db_query_duration_seconds.labels(query_type=query_type).observe(duration)
    
    @staticmethod
    def track_cache_access(cache_type: str, hit: bool):
        """Track cache access metrics"""
        if hit:
            cache_hits_total.labels(cache_type=cache_type).inc()
        else:
            cache_misses_total.labels(cache_type=cache_type).inc()
    
    @staticmethod
    def track_file_processing(file_type: str, duration: float, status: str = "success"):
        """Track file processing metrics"""
        files_processed_total.labels(file_type=file_type, status=status).inc()
        file_processing_duration_seconds.labels(file_type=file_type).observe(duration)
    
    @staticmethod
    def set_active_users(count: int):
        """Set active users count"""
        active_users.set(count)

# Decorators for easy metric tracking
def track_rag_query(query_type: str):
    """Decorator to track RAG query metrics"""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                MetricsCollector.track_rag_query(query_type, duration, "success")
                return result
            except Exception as e:
                duration = time.time() - start_time
                MetricsCollector.track_rag_query(query_type, duration, "error")
                raise
        return wrapper
    return decorator

def track_llm_call(model: str):
    """Decorator to track LLM call metrics"""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                MetricsCollector.track_llm_call(model, duration, "success")
                return result
            except Exception as e:
                duration = time.time() - start_time
                MetricsCollector.track_llm_call(model, duration, "error")
                raise
        return wrapper
    return decorator

@asynccontextmanager
async def track_db_query_context(query_type: str):
    """Context manager to track database query metrics"""
    start_time = time.time()
    try:
        yield
    finally:
        duration = time.time() - start_time
        MetricsCollector.track_db_query(query_type, duration)

# Metrics endpoint for Prometheus
async def metrics_endpoint():
    """Return Prometheus metrics"""
    return Response(
        content=generate_latest(registry),
        media_type=CONTENT_TYPE_LATEST
    )

# Background task to collect system metrics
async def collect_metrics_background():
    """Background task to continuously collect system metrics"""
    while True:
        try:
            MetricsCollector.collect_system_metrics()
            await asyncio.sleep(15)  # Collect every 15 seconds
        except Exception as e:
            print(f"Error collecting metrics: {e}")
            await asyncio.sleep(30)  # Wait longer on error
