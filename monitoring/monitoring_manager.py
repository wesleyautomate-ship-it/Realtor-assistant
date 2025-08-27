"""
Comprehensive monitoring manager for RAG Real Estate System
"""
import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import redis
from fastapi import FastAPI

from .application_metrics import MetricsCollector, MetricsMiddleware, collect_metrics_background
from .error_tracker import ErrorTracker, ErrorMiddleware
from .performance_monitor import PerformanceMonitor, PerformanceAnalyzer
from .health_checks import HealthChecker
from .logging_config import setup_logging, get_request_logger, get_error_logger, get_performance_logger
from .sentry_config import initialize_sentry, get_sentry_config
from .alert_manager import AlertManager, AlertType, AlertSeverity

logger = logging.getLogger(__name__)

class MonitoringManager:
    """Comprehensive monitoring manager that orchestrates all monitoring components"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.redis_client = None
        self.metrics_collector = None
        self.error_tracker = None
        self.performance_monitor = None
        self.health_checker = None
        self.alert_manager = None
        self.request_logger = None
        self.error_logger = None
        self.performance_logger = None
        
        # Initialize components
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all monitoring components"""
        try:
            # Initialize Redis connection
            redis_url = self.config.get("redis_url", "redis://localhost:6379")
            self.redis_client = redis.from_url(redis_url)
            
            # Initialize logging
            setup_logging()
            self.request_logger = get_request_logger()
            self.error_logger = get_error_logger()
            self.performance_logger = get_performance_logger()
            
            # Initialize Sentry
            if self.config.get("sentry_dsn"):
                initialize_sentry()
            
            # Initialize metrics collector
            self.metrics_collector = MetricsCollector()
            
            # Initialize error tracker
            self.error_tracker = ErrorTracker(
                redis_client=self.redis_client,
                sentry_dsn=self.config.get("sentry_dsn")
            )
            
            # Initialize performance monitor
            self.performance_monitor = PerformanceMonitor(redis_client=self.redis_client)
            
            # Initialize health checker
            self.health_checker = HealthChecker(self.config)
            
            # Initialize alert manager
            self.alert_manager = AlertManager(redis_client=self.redis_client)
            
            logger.info("Monitoring manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing monitoring manager: {e}")
            raise
    
    async def start_monitoring(self):
        """Start all monitoring services"""
        try:
            # Start performance monitoring
            await self.performance_monitor.start_monitoring()
            
            # Start metrics collection background task
            asyncio.create_task(collect_metrics_background())
            
            logger.info("All monitoring services started")
            
        except Exception as e:
            logger.error(f"Error starting monitoring services: {e}")
            raise
    
    async def stop_monitoring(self):
        """Stop all monitoring services"""
        try:
            # Stop performance monitoring
            await self.performance_monitor.stop_monitoring()
            
            logger.info("All monitoring services stopped")
            
        except Exception as e:
            logger.error(f"Error stopping monitoring services: {e}")
    
    def setup_fastapi_middleware(self, app: FastAPI):
        """Setup FastAPI middleware for monitoring"""
        try:
            # Add metrics middleware
            app.add_middleware(MetricsMiddleware)
            
            # Add error tracking middleware
            app.add_middleware(ErrorMiddleware, error_tracker=self.error_tracker)
            
            # Add monitoring endpoints
            self._add_monitoring_endpoints(app)
            
            logger.info("FastAPI monitoring middleware setup completed")
            
        except Exception as e:
            logger.error(f"Error setting up FastAPI middleware: {e}")
            raise
    
    def _add_monitoring_endpoints(self, app: FastAPI):
        """Add monitoring endpoints to FastAPI app"""
        from fastapi import APIRouter
        
        monitoring_router = APIRouter(prefix="/monitoring", tags=["monitoring"])
        
        @monitoring_router.get("/health")
        async def health_check():
            """Basic health check endpoint"""
            return await self.health_checker.get_health_summary()
        
        @monitoring_router.get("/health/detailed")
        async def detailed_health_check():
            """Detailed health check endpoint"""
            return await self.health_checker.get_health_summary()
        
        @monitoring_router.get("/metrics")
        async def metrics_endpoint():
            """Prometheus metrics endpoint"""
            from .application_metrics import metrics_endpoint
            return await metrics_endpoint()
        
        @monitoring_router.get("/alerts")
        async def get_alerts():
            """Get active alerts"""
            return await self.alert_manager.get_active_alerts()
        
        @monitoring_router.get("/alerts/summary")
        async def get_alert_summary():
            """Get alert summary"""
            return await self.alert_manager.get_alert_summary()
        
        @monitoring_router.get("/errors")
        async def get_errors():
            """Get recent errors"""
            return await self.error_tracker.get_error_summary()
        
        @monitoring_router.get("/performance")
        async def get_performance_report():
            """Get performance report"""
            return self.performance_monitor.get_performance_report()
        
        @monitoring_router.get("/performance/bottlenecks")
        async def get_bottlenecks():
            """Get performance bottlenecks"""
            analyzer = PerformanceAnalyzer(self.performance_monitor)
            return analyzer.identify_bottlenecks()
        
        @monitoring_router.get("/performance/recommendations")
        async def get_optimization_recommendations():
            """Get optimization recommendations"""
            analyzer = PerformanceAnalyzer(self.performance_monitor)
            return analyzer.generate_optimization_recommendations()
        
        app.include_router(monitoring_router)
    
    async def track_request(self, request_id: str, method: str, path: str, 
                          user_id: Optional[str] = None, session_id: Optional[str] = None, **kwargs):
        """Track incoming request"""
        try:
            self.request_logger.log_request(
                request_id=request_id,
                method=method,
                path=path,
                user_id=user_id,
                session_id=session_id,
                **kwargs
            )
        except Exception as e:
            logger.error(f"Error tracking request: {e}")
    
    async def track_response(self, request_id: str, status_code: int, response_time: float, **kwargs):
        """Track response"""
        try:
            self.request_logger.log_response(
                request_id=request_id,
                status_code=status_code,
                response_time=response_time,
                **kwargs
            )
        except Exception as e:
            logger.error(f"Error tracking response: {e}")
    
    async def track_error(self, error: Exception, request_id: Optional[str] = None, 
                         user_id: Optional[str] = None, context: Optional[Dict[str, Any]] = None):
        """Track error"""
        try:
            # Track in error tracker
            await self.error_tracker.track_error(error, user_id=user_id, context=context)
            
            # Log error
            self.error_logger.log_error(error, context=context, request_id=request_id, user_id=user_id)
            
        except Exception as e:
            logger.error(f"Error tracking error: {e}")
    
    async def track_performance(self, operation: str, duration: float, success: bool = True,
                              metadata: Optional[Dict[str, Any]] = None, request_id: Optional[str] = None):
        """Track performance metrics"""
        try:
            # Track in performance logger
            self.performance_logger.log_performance(
                operation=operation,
                duration=duration,
                success=success,
                metadata=metadata,
                request_id=request_id
            )
            
            # Track in metrics collector
            if operation.startswith("rag_query"):
                self.metrics_collector.track_rag_query(operation, duration, "success" if success else "error")
            elif operation.startswith("db_query"):
                self.metrics_collector.track_db_query(operation, duration)
            elif operation.startswith("llm_call"):
                self.metrics_collector.track_llm_call("gemini", duration, "success" if success else "error")
            
        except Exception as e:
            logger.error(f"Error tracking performance: {e}")
    
    async def create_alert(self, alert_type: AlertType, severity: AlertSeverity, 
                          title: str, message: str, source: str, metadata: Optional[Dict[str, Any]] = None):
        """Create an alert"""
        try:
            return await self.alert_manager.create_alert(
                alert_type=alert_type,
                severity=severity,
                title=title,
                message=message,
                source=source,
                metadata=metadata
            )
        except Exception as e:
            logger.error(f"Error creating alert: {e}")
            return None
    
    def get_metrics_collector(self) -> MetricsCollector:
        """Get metrics collector"""
        return self.metrics_collector
    
    def get_error_tracker(self) -> ErrorTracker:
        """Get error tracker"""
        return self.error_tracker
    
    def get_performance_monitor(self) -> PerformanceMonitor:
        """Get performance monitor"""
        return self.performance_monitor
    
    def get_health_checker(self) -> HealthChecker:
        """Get health checker"""
        return self.health_checker
    
    def get_alert_manager(self) -> AlertManager:
        """Get alert manager"""
        return self.alert_manager
    
    async def get_monitoring_summary(self) -> Dict[str, Any]:
        """Get comprehensive monitoring summary"""
        try:
            summary = {
                "timestamp": datetime.now().isoformat(),
                "health": await self.health_checker.get_health_summary(),
                "alerts": await self.alert_manager.get_alert_summary(),
                "errors": await self.error_tracker.get_error_summary(),
                "performance": self.performance_monitor.get_performance_report()
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting monitoring summary: {e}")
            return {"error": str(e)}

# Global monitoring manager instance
monitoring_manager = None

def initialize_monitoring(config: Dict[str, Any]) -> MonitoringManager:
    """Initialize global monitoring manager"""
    global monitoring_manager
    monitoring_manager = MonitoringManager(config)
    return monitoring_manager

def get_monitoring_manager() -> Optional[MonitoringManager]:
    """Get global monitoring manager"""
    return monitoring_manager

# Convenience functions for common monitoring operations
async def track_request(request_id: str, method: str, path: str, 
                       user_id: Optional[str] = None, session_id: Optional[str] = None, **kwargs):
    """Track incoming request"""
    if monitoring_manager:
        await monitoring_manager.track_request(request_id, method, path, user_id, session_id, **kwargs)

async def track_response(request_id: str, status_code: int, response_time: float, **kwargs):
    """Track response"""
    if monitoring_manager:
        await monitoring_manager.track_response(request_id, status_code, response_time, **kwargs)

async def track_error(error: Exception, request_id: Optional[str] = None, 
                     user_id: Optional[str] = None, context: Optional[Dict[str, Any]] = None):
    """Track error"""
    if monitoring_manager:
        await monitoring_manager.track_error(error, request_id, user_id, context)

async def track_performance(operation: str, duration: float, success: bool = True,
                          metadata: Optional[Dict[str, Any]] = None, request_id: Optional[str] = None):
    """Track performance metrics"""
    if monitoring_manager:
        await monitoring_manager.track_performance(operation, duration, success, metadata, request_id)

async def create_alert(alert_type: AlertType, severity: AlertSeverity, 
                      title: str, message: str, source: str, metadata: Optional[Dict[str, Any]] = None):
    """Create an alert"""
    if monitoring_manager:
        return await monitoring_manager.create_alert(alert_type, severity, title, message, source, metadata)
    return None
