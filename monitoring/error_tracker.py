"""
Error tracking service for RAG Real Estate System
"""
import traceback
import logging
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import redis
from fastapi import Request, HTTPException
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

logger = logging.getLogger(__name__)

class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    """Error categories"""
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    VALIDATION = "validation"
    DATABASE = "database"
    EXTERNAL_API = "external_api"
    RAG_PROCESSING = "rag_processing"
    VECTOR_SEARCH = "vector_search"
    LLM_ERROR = "llm_error"
    FILE_PROCESSING = "file_processing"
    SYSTEM = "system"
    NETWORK = "network"
    UNKNOWN = "unknown"

@dataclass
class ErrorEvent:
    """Error event data structure"""
    id: str
    timestamp: datetime
    error_type: str
    error_message: str
    error_traceback: str
    severity: ErrorSeverity
    category: ErrorCategory
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    endpoint: Optional[str] = None
    method: Optional[str] = None
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    request_data: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None
    tags: Optional[Dict[str, str]] = None
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None

class ErrorTracker:
    """Comprehensive error tracking service"""
    
    def __init__(self, redis_client: Optional[redis.Redis] = None, sentry_dsn: Optional[str] = None):
        self.redis_client = redis_client
        self.error_patterns = self._initialize_error_patterns()
        self.error_counts = {}
        self.alert_thresholds = {
            ErrorSeverity.CRITICAL: 1,
            ErrorSeverity.HIGH: 5,
            ErrorSeverity.MEDIUM: 10,
            ErrorSeverity.LOW: 20
        }
        
        # Initialize Sentry if DSN provided
        if sentry_dsn:
            sentry_sdk.init(
                dsn=sentry_dsn,
                integrations=[
                    FastApiIntegration(),
                    RedisIntegration(),
                    SqlalchemyIntegration(),
                ],
                traces_sample_rate=0.1,
                profiles_sample_rate=0.1,
            )
            logger.info("Sentry initialized for error tracking")
    
    def _initialize_error_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize error pattern matching rules"""
        return {
            "authentication": {
                "patterns": ["jwt", "token", "unauthorized", "forbidden", "401", "403"],
                "category": ErrorCategory.AUTHENTICATION,
                "severity": ErrorSeverity.MEDIUM
            },
            "database": {
                "patterns": ["database", "connection", "sql", "postgres", "chromadb", "redis"],
                "category": ErrorCategory.DATABASE,
                "severity": ErrorSeverity.HIGH
            },
            "rag_processing": {
                "patterns": ["rag", "retrieval", "embedding", "vector"],
                "category": ErrorCategory.RAG_PROCESSING,
                "severity": ErrorSeverity.HIGH
            },
            "llm_error": {
                "patterns": ["gemini", "openai", "llm", "model", "generation"],
                "category": ErrorCategory.LLM_ERROR,
                "severity": ErrorSeverity.HIGH
            },
            "file_processing": {
                "patterns": ["file", "upload", "pdf", "document", "processing"],
                "category": ErrorCategory.FILE_PROCESSING,
                "severity": ErrorSeverity.MEDIUM
            },
            "external_api": {
                "patterns": ["api", "http", "request", "timeout", "external"],
                "category": ErrorCategory.EXTERNAL_API,
                "severity": ErrorSeverity.MEDIUM
            },
            "validation": {
                "patterns": ["validation", "invalid", "required", "format"],
                "category": ErrorCategory.VALIDATION,
                "severity": ErrorSeverity.LOW
            }
        }
    
    def _categorize_error(self, error_message: str, error_type: str) -> tuple[ErrorCategory, ErrorSeverity]:
        """Categorize error based on message and type"""
        error_text = f"{error_message} {error_type}".lower()
        
        for pattern_name, pattern_info in self.error_patterns.items():
            for pattern in pattern_info["patterns"]:
                if pattern.lower() in error_text:
                    return pattern_info["category"], pattern_info["severity"]
        
        # Default categorization
        if "critical" in error_text or "fatal" in error_text:
            return ErrorCategory.SYSTEM, ErrorSeverity.CRITICAL
        elif "error" in error_text:
            return ErrorCategory.SYSTEM, ErrorSeverity.HIGH
        else:
            return ErrorCategory.UNKNOWN, ErrorSeverity.MEDIUM
    
    def _generate_error_id(self, error_message: str, error_type: str) -> str:
        """Generate unique error ID"""
        error_hash = hashlib.md5(f"{error_type}:{error_message}".encode()).hexdigest()
        return f"error_{error_hash[:8]}"
    
    async def track_error(
        self,
        error: Exception,
        request: Optional[Request] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Track an error event"""
        try:
            error_message = str(error)
            error_type = type(error).__name__
            error_traceback = traceback.format_exc()
            
            # Categorize error
            category, severity = self._categorize_error(error_message, error_type)
            
            # Generate error ID
            error_id = self._generate_error_id(error_message, error_type)
            
            # Extract request information
            endpoint = None
            method = None
            user_agent = None
            ip_address = None
            request_data = None
            
            if request:
                endpoint = request.url.path
                method = request.method
                user_agent = request.headers.get("user-agent")
                ip_address = request.client.host if request.client else None
                
                # Extract request data (be careful with sensitive data)
                try:
                    if request.method in ["POST", "PUT", "PATCH"]:
                        body = await request.body()
                        if body:
                            request_data = {"body_size": len(body)}
                except Exception:
                    pass
            
            # Create error event
            error_event = ErrorEvent(
                id=error_id,
                timestamp=datetime.now(),
                error_type=error_type,
                error_message=error_message,
                error_traceback=error_traceback,
                severity=severity,
                category=category,
                user_id=user_id,
                session_id=session_id,
                request_id=getattr(request, 'state', {}).get('request_id') if request else None,
                endpoint=endpoint,
                method=method,
                user_agent=user_agent,
                ip_address=ip_address,
                request_data=request_data,
                context=context or {},
                tags={
                    "environment": "production",
                    "service": "rag-real-estate"
                }
            )
            
            # Store error event
            await self._store_error_event(error_event)
            
            # Update error counts
            await self._update_error_counts(error_event)
            
            # Check for alerts
            await self._check_error_alerts(error_event)
            
            # Send to Sentry
            if sentry_sdk.Hub.current:
                with sentry_sdk.push_scope() as scope:
                    scope.set_tag("error_id", error_id)
                    scope.set_tag("category", category.value)
                    scope.set_tag("severity", severity.value)
                    if user_id:
                        scope.set_user({"id": user_id})
                    if context:
                        scope.set_context("custom", context)
                    sentry_sdk.capture_exception(error)
            
            logger.error(f"Error tracked: {error_id} - {error_message}")
            return error_id
            
        except Exception as e:
            logger.error(f"Error tracking failed: {e}")
            return "tracking_failed"
    
    async def _store_error_event(self, error_event: ErrorEvent):
        """Store error event in Redis"""
        if not self.redis_client:
            return
        
        try:
            # Store error event
            error_data = asdict(error_event)
            error_data['timestamp'] = error_event.timestamp.isoformat()
            error_data['severity'] = error_event.severity.value
            error_data['category'] = error_event.category.value
            
            # Store in Redis
            self.redis_client.lpush(f"errors:{error_event.id}", json.dumps(error_data))
            self.redis_client.expire(f"errors:{error_event.id}", 86400 * 7)  # 7 days
            
            # Store in recent errors list
            self.redis_client.lpush("errors:recent", json.dumps(error_data))
            self.redis_client.ltrim("errors:recent", 0, 999)  # Keep last 1000 errors
            
            # Store by category
            self.redis_client.lpush(f"errors:category:{error_event.category.value}", json.dumps(error_data))
            self.redis_client.ltrim(f"errors:category:{error_event.category.value}", 0, 999)
            
            # Store by severity
            self.redis_client.lpush(f"errors:severity:{error_event.severity.value}", json.dumps(error_data))
            self.redis_client.ltrim(f"errors:severity:{error_event.severity.value}", 0, 999)
            
        except Exception as e:
            logger.error(f"Error storing error event: {e}")
    
    async def _update_error_counts(self, error_event: ErrorEvent):
        """Update error count statistics"""
        try:
            # Update global error count
            error_key = f"error_count:{error_event.error_type}"
            self.redis_client.incr(error_key)
            self.redis_client.expire(error_key, 86400)  # 1 day
            
            # Update category count
            category_key = f"error_count:category:{error_event.category.value}"
            self.redis_client.incr(category_key)
            self.redis_client.expire(category_key, 86400)
            
            # Update severity count
            severity_key = f"error_count:severity:{error_event.severity.value}"
            self.redis_client.incr(severity_key)
            self.redis_client.expire(severity_key, 86400)
            
        except Exception as e:
            logger.error(f"Error updating error counts: {e}")
    
    async def _check_error_alerts(self, error_event: ErrorEvent):
        """Check if error should trigger alerts"""
        try:
            threshold = self.alert_thresholds.get(error_event.severity, 10)
            
            # Get error count for this type in the last hour
            error_key = f"error_count:{error_event.error_type}"
            count = int(self.redis_client.get(error_key) or 0)
            
            if count >= threshold:
                alert = {
                    'type': 'error_threshold_exceeded',
                    'severity': error_event.severity.value,
                    'error_type': error_event.error_type,
                    'error_message': error_event.error_message,
                    'count': count,
                    'threshold': threshold,
                    'timestamp': datetime.now().isoformat(),
                    'message': f'Error threshold exceeded: {error_event.error_type} ({count} errors)'
                }
                
                # Store alert
                self.redis_client.lpush("alerts:errors", json.dumps(alert))
                self.redis_client.ltrim("alerts:errors", 0, 99)
                
                logger.warning(f"Error alert triggered: {alert['message']}")
                
        except Exception as e:
            logger.error(f"Error checking alerts: {e}")
    
    async def get_error_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get error summary for the specified time period"""
        try:
            if not self.redis_client:
                return {}
            
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            # Get recent errors
            recent_errors = self.redis_client.lrange("errors:recent", 0, 999)
            errors = []
            
            for error_json in recent_errors:
                error_data = json.loads(error_json)
                error_time = datetime.fromisoformat(error_data['timestamp'])
                if error_time >= cutoff_time:
                    errors.append(error_data)
            
            # Calculate statistics
            total_errors = len(errors)
            errors_by_category = {}
            errors_by_severity = {}
            
            for error in errors:
                category = error['category']
                severity = error['severity']
                
                errors_by_category[category] = errors_by_category.get(category, 0) + 1
                errors_by_severity[severity] = errors_by_severity.get(severity, 0) + 1
            
            return {
                'total_errors': total_errors,
                'errors_by_category': errors_by_category,
                'errors_by_severity': errors_by_severity,
                'time_period_hours': hours,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting error summary: {e}")
            return {}
    
    async def get_error_details(self, error_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific error"""
        try:
            if not self.redis_client:
                return None
            
            error_data = self.redis_client.lrange(f"errors:{error_id}", 0, 0)
            if error_data:
                return json.loads(error_data[0])
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting error details: {e}")
            return None
    
    async def resolve_error(self, error_id: str, resolved_by: str) -> bool:
        """Mark an error as resolved"""
        try:
            if not self.redis_client:
                return False
            
            error_data = self.redis_client.lrange(f"errors:{error_id}", 0, 0)
            if not error_data:
                return False
            
            error = json.loads(error_data[0])
            error['resolved'] = True
            error['resolved_at'] = datetime.now().isoformat()
            error['resolved_by'] = resolved_by
            
            # Update stored error
            self.redis_client.lset(f"errors:{error_id}", 0, json.dumps(error))
            
            logger.info(f"Error {error_id} marked as resolved by {resolved_by}")
            return True
            
        except Exception as e:
            logger.error(f"Error resolving error: {e}")
            return False
    
    async def get_active_errors(self) -> List[Dict[str, Any]]:
        """Get list of active (unresolved) errors"""
        try:
            if not self.redis_client:
                return []
            
            recent_errors = self.redis_client.lrange("errors:recent", 0, 999)
            active_errors = []
            
            for error_json in recent_errors:
                error_data = json.loads(error_json)
                if not error_data.get('resolved', False):
                    active_errors.append(error_data)
            
            return active_errors
            
        except Exception as e:
            logger.error(f"Error getting active errors: {e}")
            return []
    
    def set_alert_threshold(self, severity: ErrorSeverity, threshold: int):
        """Set alert threshold for error severity"""
        self.alert_thresholds[severity] = threshold
        logger.info(f"Set alert threshold for {severity.value}: {threshold}")

class ErrorMiddleware:
    """FastAPI middleware for automatic error tracking"""
    
    def __init__(self, error_tracker: ErrorTracker):
        self.error_tracker = error_tracker
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        try:
            await self.app(scope, receive, send)
        except Exception as e:
            # Create a mock request object for error tracking
            request = type('Request', (), {
                'url': type('URL', (), {'path': scope.get('path', '')}),
                'method': scope.get('method', ''),
                'headers': dict(scope.get('headers', [])),
                'client': type('Client', (), {'host': scope.get('client', [''])[0] if scope.get('client') else None}),
                'state': {'request_id': scope.get('request_id', '')}
            })()
            
            await self.error_tracker.track_error(e, request)
            raise
