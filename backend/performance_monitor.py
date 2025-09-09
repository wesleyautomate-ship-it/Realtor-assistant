#!/usr/bin/env python3
"""
Performance Monitoring System for Dubai Real Estate RAG System
Tracks and analyzes system performance metrics for optimization
"""

import os
import time
import logging
import psutil
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
import json
from cache_manager import cache_manager
from hybrid_search_engine import get_hybrid_search_engine

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetric:
    timestamp: datetime
    metric_name: str
    value: float
    unit: str
    metadata: Dict[str, Any]

@dataclass
class SystemHealth:
    timestamp: datetime
    overall_status: str
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    database_status: str
    chromadb_status: str
    redis_status: str
    response_time_avg: float
    error_rate: float

class PerformanceMonitor:
    """Comprehensive performance monitoring system"""
    
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.metrics_history: List[PerformanceMetric] = []
        self.health_history: List[SystemHealth] = []
        self.start_time = datetime.now()
        
        # Performance thresholds
        self.thresholds = {
            "cpu_usage": 80.0,
            "memory_usage": 85.0,
            "disk_usage": 90.0,
            "response_time": 2.0,
            "error_rate": 5.0
        }
        
        # Monitoring intervals
        self.monitoring_intervals = {
            "system_metrics": 30,  # seconds
            "database_metrics": 60,  # seconds
            "health_check": 120  # seconds
        }
    
    async def start_monitoring(self):
        """Start continuous performance monitoring"""
        logger.info("🚀 Starting performance monitoring system")
        
        # Start monitoring tasks
        tasks = [
            asyncio.create_task(self._monitor_system_metrics()),
            asyncio.create_task(self._monitor_database_metrics()),
            asyncio.create_task(self._monitor_health_status())
        ]
        
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            logger.error(f"Error in monitoring tasks: {e}")
    
    async def _monitor_system_metrics(self):
        """Monitor system-level metrics"""
        while True:
            try:
                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                self._record_metric("cpu_usage", cpu_percent, "percent")
                
                # Memory usage
                memory = psutil.virtual_memory()
                self._record_metric("memory_usage", memory.percent, "percent")
                self._record_metric("memory_available", memory.available / (1024**3), "GB")
                
                # Disk usage
                disk = psutil.disk_usage('/')
                disk_percent = (disk.used / disk.total) * 100
                self._record_metric("disk_usage", disk_percent, "percent")
                self._record_metric("disk_free", disk.free / (1024**3), "GB")
                
                # Network I/O
                network = psutil.net_io_counters()
                self._record_metric("network_bytes_sent", network.bytes_sent / (1024**2), "MB")
                self._record_metric("network_bytes_recv", network.bytes_recv / (1024**2), "MB")
                
                await asyncio.sleep(self.monitoring_intervals["system_metrics"])
                
            except Exception as e:
                logger.error(f"Error monitoring system metrics: {e}")
                await asyncio.sleep(30)
    
    async def _monitor_database_metrics(self):
        """Monitor database performance metrics"""
        while True:
            try:
                # PostgreSQL metrics
                await self._monitor_postgres_metrics()
                
                # ChromaDB metrics
                await self._monitor_chromadb_metrics()
                
                # Redis metrics
                await self._monitor_redis_metrics()
                
                await asyncio.sleep(self.monitoring_intervals["database_metrics"])
                
            except Exception as e:
                logger.error(f"Error monitoring database metrics: {e}")
                await asyncio.sleep(60)
    
    async def _monitor_postgres_metrics(self):
        """Monitor PostgreSQL performance"""
        try:
            with self.engine.connect() as conn:
                # Active connections
                result = conn.execute(text("""
                    SELECT count(*) as active_connections 
                    FROM pg_stat_activity 
                    WHERE state = 'active'
                """))
                active_connections = result.fetchone()[0]
                self._record_metric("postgres_active_connections", active_connections, "count")
                
                # Database size
                result = conn.execute(text("""
                    SELECT pg_size_pretty(pg_database_size(current_database())) as db_size
                """))
                db_size = result.fetchone()[0]
                self._record_metric("postgres_db_size", db_size, "size")
                
                # Slow queries (if pg_stat_statements is available)
                try:
                    result = conn.execute(text("""
                        SELECT count(*) as slow_queries
                        FROM pg_stat_statements 
                        WHERE mean_time > 1000
                    """))
                    slow_queries = result.fetchone()[0]
                    self._record_metric("postgres_slow_queries", slow_queries, "count")
                except:
                    pass  # pg_stat_statements might not be enabled
                
        except Exception as e:
            logger.error(f"Error monitoring PostgreSQL: {e}")
    
    async def _monitor_chromadb_metrics(self):
        """Monitor ChromaDB performance"""
        try:
            search_engine = get_hybrid_search_engine()
            chroma_health = search_engine.health_check()
            
            if chroma_health["chromadb"] == "healthy":
                self._record_metric("chromadb_status", 1, "status")
            else:
                self._record_metric("chromadb_status", 0, "status")
                
        except Exception as e:
            logger.error(f"Error monitoring ChromaDB: {e}")
            self._record_metric("chromadb_status", 0, "status")
    
    async def _monitor_redis_metrics(self):
        """Monitor Redis performance"""
        try:
            redis_health = cache_manager.health_check()
            
            if redis_health["status"] == "healthy":
                self._record_metric("redis_status", 1, "status")
                self._record_metric("redis_memory_usage", redis_health.get("memory_usage", "0"), "memory")
                self._record_metric("redis_connected_clients", redis_health.get("connected_clients", 0), "count")
            else:
                self._record_metric("redis_status", 0, "status")
                
        except Exception as e:
            logger.error(f"Error monitoring Redis: {e}")
            self._record_metric("redis_status", 0, "status")
    
    async def _monitor_health_status(self):
        """Monitor overall system health"""
        while True:
            try:
                health = await self._check_system_health()
                self.health_history.append(health)
                
                # Keep only last 100 health records
                if len(self.health_history) > 100:
                    self.health_history = self.health_history[-100:]
                
                # Log health status
                if health.overall_status != "healthy":
                    logger.warning(f"⚠️ System health issue: {health.overall_status}")
                
                await asyncio.sleep(self.monitoring_intervals["health_check"])
                
            except Exception as e:
                logger.error(f"Error monitoring health status: {e}")
                await asyncio.sleep(120)
    
    async def _check_system_health(self) -> SystemHealth:
        """Check overall system health"""
        # Get current metrics
        current_metrics = self._get_current_metrics()
        
        # Check system resources
        cpu_usage = current_metrics.get("cpu_usage", 0)
        memory_usage = current_metrics.get("memory_usage", 0)
        disk_usage = current_metrics.get("disk_usage", 0)
        
        # Check database status
        postgres_status = "healthy" if current_metrics.get("postgres_active_connections", 0) >= 0 else "unhealthy"
        chromadb_status = "healthy" if current_metrics.get("chromadb_status", 0) == 1 else "unhealthy"
        redis_status = "healthy" if current_metrics.get("redis_status", 0) == 1 else "unhealthy"
        
        # Calculate overall status
        overall_status = "healthy"
        if (cpu_usage > self.thresholds["cpu_usage"] or 
            memory_usage > self.thresholds["memory_usage"] or 
            disk_usage > self.thresholds["disk_usage"] or
            postgres_status != "healthy" or
            chromadb_status != "healthy" or
            redis_status != "healthy"):
            overall_status = "degraded"
        
        return SystemHealth(
            timestamp=datetime.now(),
            overall_status=overall_status,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            disk_usage=disk_usage,
            database_status=postgres_status,
            chromadb_status=chromadb_status,
            redis_status=redis_status,
            response_time_avg=current_metrics.get("response_time_avg", 0),
            error_rate=current_metrics.get("error_rate", 0)
        )
    
    def _record_metric(self, name: str, value: float, unit: str, metadata: Dict[str, Any] = None):
        """Record a performance metric"""
        metric = PerformanceMetric(
            timestamp=datetime.now(),
            metric_name=name,
            value=value,
            unit=unit,
            metadata=metadata or {}
        )
        
        self.metrics_history.append(metric)
        
        # Keep only last 1000 metrics
        if len(self.metrics_history) > 1000:
            self.metrics_history = self.metrics_history[-1000:]
    
    def _get_current_metrics(self) -> Dict[str, float]:
        """Get current metric values"""
        current_metrics = {}
        
        # Get latest metrics for each type
        metric_names = set(metric.metric_name for metric in self.metrics_history)
        
        for metric_name in metric_names:
            latest_metric = next(
                (m for m in reversed(self.metrics_history) if m.metric_name == metric_name),
                None
            )
            if latest_metric:
                current_metrics[metric_name] = latest_metric.value
        
        return current_metrics
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        current_metrics = self._get_current_metrics()
        latest_health = self.health_history[-1] if self.health_history else None
        
        # Calculate averages for key metrics
        uptime = datetime.now() - self.start_time
        
        return {
            "system_info": {
                "uptime_seconds": uptime.total_seconds(),
                "uptime_human": str(uptime),
                "start_time": self.start_time.isoformat(),
                "total_metrics_collected": len(self.metrics_history)
            },
            "current_metrics": current_metrics,
            "health_status": asdict(latest_health) if latest_health else None,
            "thresholds": self.thresholds,
            "performance_trends": self._calculate_trends(),
            "alerts": self._check_alerts(current_metrics)
        }
    
    def _calculate_trends(self) -> Dict[str, Any]:
        """Calculate performance trends"""
        if len(self.metrics_history) < 10:
            return {"status": "insufficient_data"}
        
        # Get metrics from last hour
        one_hour_ago = datetime.now() - timedelta(hours=1)
        recent_metrics = [m for m in self.metrics_history if m.timestamp > one_hour_ago]
        
        trends = {}
        metric_groups = {}
        
        # Group metrics by name
        for metric in recent_metrics:
            if metric.metric_name not in metric_groups:
                metric_groups[metric.metric_name] = []
            metric_groups[metric.metric_name].append(metric.value)
        
        # Calculate trends for each metric
        for metric_name, values in metric_groups.items():
            if len(values) >= 2:
                # Simple linear trend calculation
                first_half = values[:len(values)//2]
                second_half = values[len(values)//2:]
                
                first_avg = sum(first_half) / len(first_half)
                second_avg = sum(second_half) / len(second_half)
                
                trend_direction = "increasing" if second_avg > first_avg else "decreasing"
                trend_magnitude = abs(second_avg - first_avg) / first_avg * 100 if first_avg > 0 else 0
                
                trends[metric_name] = {
                    "direction": trend_direction,
                    "magnitude_percent": round(trend_magnitude, 2),
                    "current_avg": round(second_avg, 2),
                    "previous_avg": round(first_avg, 2)
                }
        
        return trends
    
    def _check_alerts(self, current_metrics: Dict[str, float]) -> List[Dict[str, Any]]:
        """Check for performance alerts"""
        alerts = []
        
        # Check CPU usage
        cpu_usage = current_metrics.get("cpu_usage", 0)
        if cpu_usage > self.thresholds["cpu_usage"]:
            alerts.append({
                "type": "cpu_high",
                "severity": "warning",
                "message": f"CPU usage is {cpu_usage:.1f}% (threshold: {self.thresholds['cpu_usage']}%)",
                "value": cpu_usage,
                "threshold": self.thresholds["cpu_usage"]
            })
        
        # Check memory usage
        memory_usage = current_metrics.get("memory_usage", 0)
        if memory_usage > self.thresholds["memory_usage"]:
            alerts.append({
                "type": "memory_high",
                "severity": "warning",
                "message": f"Memory usage is {memory_usage:.1f}% (threshold: {self.thresholds['memory_usage']}%)",
                "value": memory_usage,
                "threshold": self.thresholds["memory_usage"]
            })
        
        # Check disk usage
        disk_usage = current_metrics.get("disk_usage", 0)
        if disk_usage > self.thresholds["disk_usage"]:
            alerts.append({
                "type": "disk_high",
                "severity": "critical",
                "message": f"Disk usage is {disk_usage:.1f}% (threshold: {self.thresholds['disk_usage']}%)",
                "value": disk_usage,
                "threshold": self.thresholds["disk_usage"]
            })
        
        # Check database status
        if current_metrics.get("postgres_active_connections", 0) < 0:
            alerts.append({
                "type": "database_unavailable",
                "severity": "critical",
                "message": "PostgreSQL database is not responding",
                "value": 0,
                "threshold": 1
            })
        
        if current_metrics.get("chromadb_status", 0) == 0:
            alerts.append({
                "type": "chromadb_unavailable",
                "severity": "critical",
                "message": "ChromaDB is not responding",
                "value": 0,
                "threshold": 1
            })
        
        if current_metrics.get("redis_status", 0) == 0:
            alerts.append({
                "type": "redis_unavailable",
                "severity": "warning",
                "message": "Redis cache is not responding",
                "value": 0,
                "threshold": 1
            })
        
        return alerts
    
    def get_metrics_history(self, metric_name: str, hours: int = 24) -> List[Dict[str, Any]]:
        """Get historical metrics for a specific metric"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        filtered_metrics = [
            asdict(metric) for metric in self.metrics_history
            if metric.metric_name == metric_name and metric.timestamp > cutoff_time
        ]
        
        return filtered_metrics
    
    def export_metrics(self, filepath: str):
        """Export metrics to JSON file"""
        try:
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "metrics": [asdict(metric) for metric in self.metrics_history],
                "health_history": [asdict(health) for health in self.health_history],
                "summary": self.get_performance_summary()
            }
            
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            logger.info(f"✅ Metrics exported to {filepath}")
            
        except Exception as e:
            logger.error(f"Error exporting metrics: {e}")

# Global performance monitor instance
performance_monitor = None

def get_performance_monitor() -> PerformanceMonitor:
    """Get or create global performance monitor instance"""
    global performance_monitor
    if performance_monitor is None:
        performance_monitor = PerformanceMonitor(database_url=os.getenv("DATABASE_URL"))
    return performance_monitor
