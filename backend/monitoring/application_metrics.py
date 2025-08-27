#!/usr/bin/env python3
"""
Application metrics collection for the Dubai Real Estate RAG System
"""

import time
import logging
from typing import Dict, Any, Union
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class MetricsData:
    """Metrics data structure"""
    timestamp: float
    value: float
    tags: Dict[str, str]

class MetricsCollector:
    """Simple metrics collector for application monitoring"""
    
    def __init__(self):
        self.metrics: Dict[str, MetricsData] = {}
        self.start_time = time.time()
    
    def record_metric(self, name: str, value: float, tags: Union[Dict[str, str], None] = None):
        """Record a metric"""
        self.metrics[name] = MetricsData(
            timestamp=time.time(),
            value=value,
            tags=tags or {}
        )
        logger.debug(f"Recorded metric {name}: {value}")
    
    def get_metric(self, name: str) -> Union[MetricsData, None]:
        """Get a specific metric"""
        return self.metrics.get(name)
    
    def get_all_metrics(self) -> Dict[str, MetricsData]:
        """Get all recorded metrics"""
        return self.metrics.copy()
    
    def get_uptime(self) -> float:
        """Get application uptime in seconds"""
        return time.time() - self.start_time
    
    def record_api_request(self, endpoint: str, response_time: float, status_code: int):
        """Record API request metrics"""
        self.record_metric(
            f"api_request_{endpoint}",
            response_time,
            {"status_code": str(status_code)}
        )
    
    def record_database_query(self, query_type: str, execution_time: float):
        """Record database query metrics"""
        self.record_metric(
            f"db_query_{query_type}",
            execution_time,
            {"query_type": query_type}
        )
    
    def record_ai_request(self, model: str, response_time: float, tokens_used: int):
        """Record AI request metrics"""
        self.record_metric(
            f"ai_request_{model}",
            response_time,
            {"tokens_used": str(tokens_used)}
        )
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get system health metrics"""
        uptime = self.get_uptime()
        
        # Calculate average response times
        api_metrics = {k: v for k, v in self.metrics.items() if k.startswith("api_request_")}
        avg_api_response = sum(m.value for m in api_metrics.values()) / len(api_metrics) if api_metrics else 0
        
        db_metrics = {k: v for k, v in self.metrics.items() if k.startswith("db_query_")}
        avg_db_response = sum(m.value for m in db_metrics.values()) / len(db_metrics) if db_metrics else 0
        
        return {
            "uptime_seconds": uptime,
            "uptime_hours": uptime / 3600,
            "total_metrics_recorded": len(self.metrics),
            "avg_api_response_time": avg_api_response,
            "avg_db_response_time": avg_db_response,
            "active_connections": 0,  # Placeholder
            "memory_usage_mb": 0,     # Placeholder
            "cpu_usage_percent": 0    # Placeholder
        }
