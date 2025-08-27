"""
Health check endpoints and system status monitoring for RAG Real Estate System
"""
import asyncio
import time
import psutil
import aiohttp
import redis
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import json
from fastapi import HTTPException
import asyncpg
from chromadb import Client as ChromaClient

logger = logging.getLogger(__name__)

class HealthStatus(Enum):
    """Health status enumeration"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

@dataclass
class HealthCheck:
    """Health check result"""
    name: str
    status: HealthStatus
    response_time: float
    details: Dict[str, Any]
    timestamp: datetime
    error_message: Optional[str] = None

@dataclass
class SystemHealth:
    """System health summary"""
    overall_status: HealthStatus
    checks: List[HealthCheck]
    timestamp: datetime
    uptime: float
    version: str

class HealthChecker:
    """Comprehensive health checking system"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.redis_client = None
        self.db_pool = None
        self.chroma_client = None
        self.health_history = []
        
        # Initialize connections
        self._initialize_connections()
    
    def _initialize_connections(self):
        """Initialize database and service connections"""
        try:
            # Redis connection
            redis_url = self.config.get("redis_url", "redis://localhost:6379")
            self.redis_client = redis.from_url(redis_url)
            
            # Database connection pool
            db_config = self.config.get("database", {})
            if db_config:
                self.db_pool = asyncpg.create_pool(
                    host=db_config.get("host", "localhost"),
                    port=db_config.get("port", 5432),
                    user=db_config.get("user", "postgres"),
                    password=db_config.get("password", ""),
                    database=db_config.get("database", "rag_real_estate"),
                    min_size=1,
                    max_size=10
                )
            
            # ChromaDB client
            chroma_config = self.config.get("chromadb", {})
            if chroma_config:
                self.chroma_client = ChromaClient(
                    host=chroma_config.get("host", "localhost"),
                    port=chroma_config.get("port", 8000)
                )
                
        except Exception as e:
            logger.error(f"Error initializing connections: {e}")
    
    async def check_system_health(self) -> SystemHealth:
        """Perform comprehensive system health check"""
        start_time = time.time()
        checks = []
        
        # System-level checks
        checks.append(await self._check_system_resources())
        checks.append(await self._check_disk_space())
        checks.append(await self._check_memory_usage())
        checks.append(await self._check_cpu_usage())
        
        # Service-level checks
        checks.append(await self._check_redis_health())
        checks.append(await self._check_database_health())
        checks.append(await self._check_chromadb_health())
        checks.append(await self._check_external_apis())
        
        # Application-level checks
        checks.append(await self._check_application_health())
        checks.append(await self._check_background_tasks())
        
        # Determine overall status
        overall_status = self._determine_overall_status(checks)
        
        # Create system health summary
        system_health = SystemHealth(
            overall_status=overall_status,
            checks=checks,
            timestamp=datetime.now(),
            uptime=time.time() - start_time,
            version=self.config.get("version", "1.0.0")
        )
        
        # Store health history
        self.health_history.append(system_health)
        if len(self.health_history) > 100:  # Keep last 100 health checks
            self.health_history.pop(0)
        
        return system_health
    
    async def _check_system_resources(self) -> HealthCheck:
        """Check system resource availability"""
        start_time = time.time()
        
        try:
            # Check CPU cores
            cpu_count = psutil.cpu_count()
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Check memory
            memory = psutil.virtual_memory()
            
            # Check disk
            disk = psutil.disk_usage('/')
            
            details = {
                "cpu_count": cpu_count,
                "cpu_percent": cpu_percent,
                "memory_total": memory.total,
                "memory_available": memory.available,
                "memory_percent": memory.percent,
                "disk_total": disk.total,
                "disk_free": disk.free,
                "disk_percent": (disk.used / disk.total) * 100
            }
            
            # Determine status
            status = HealthStatus.HEALTHY
            if cpu_percent > 90 or memory.percent > 90 or details["disk_percent"] > 90:
                status = HealthStatus.DEGRADED
            elif cpu_percent > 95 or memory.percent > 95 or details["disk_percent"] > 95:
                status = HealthStatus.UNHEALTHY
            
            return HealthCheck(
                name="system_resources",
                status=status,
                response_time=time.time() - start_time,
                details=details,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return HealthCheck(
                name="system_resources",
                status=HealthStatus.UNHEALTHY,
                response_time=time.time() - start_time,
                details={},
                timestamp=datetime.now(),
                error_message=str(e)
            )
    
    async def _check_disk_space(self) -> HealthCheck:
        """Check disk space availability"""
        start_time = time.time()
        
        try:
            disk = psutil.disk_usage('/')
            free_percent = (disk.free / disk.total) * 100
            
            details = {
                "total_bytes": disk.total,
                "free_bytes": disk.free,
                "used_bytes": disk.used,
                "free_percent": free_percent
            }
            
            status = HealthStatus.HEALTHY
            if free_percent < 10:
                status = HealthStatus.DEGRADED
            elif free_percent < 5:
                status = HealthStatus.UNHEALTHY
            
            return HealthCheck(
                name="disk_space",
                status=status,
                response_time=time.time() - start_time,
                details=details,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return HealthCheck(
                name="disk_space",
                status=HealthStatus.UNHEALTHY,
                response_time=time.time() - start_time,
                details={},
                timestamp=datetime.now(),
                error_message=str(e)
            )
    
    async def _check_memory_usage(self) -> HealthCheck:
        """Check memory usage"""
        start_time = time.time()
        
        try:
            memory = psutil.virtual_memory()
            
            details = {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "percent": memory.percent,
                "swap_total": psutil.swap_memory().total,
                "swap_used": psutil.swap_memory().used
            }
            
            status = HealthStatus.HEALTHY
            if memory.percent > 85:
                status = HealthStatus.DEGRADED
            elif memory.percent > 95:
                status = HealthStatus.UNHEALTHY
            
            return HealthCheck(
                name="memory_usage",
                status=status,
                response_time=time.time() - start_time,
                details=details,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return HealthCheck(
                name="memory_usage",
                status=HealthStatus.UNHEALTHY,
                response_time=time.time() - start_time,
                details={},
                timestamp=datetime.now(),
                error_message=str(e)
            )
    
    async def _check_cpu_usage(self) -> HealthCheck:
        """Check CPU usage"""
        start_time = time.time()
        
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            load_avg = psutil.getloadavg()
            
            details = {
                "cpu_percent": cpu_percent,
                "cpu_count": cpu_count,
                "load_average_1min": load_avg[0],
                "load_average_5min": load_avg[1],
                "load_average_15min": load_avg[2]
            }
            
            status = HealthStatus.HEALTHY
            if cpu_percent > 80:
                status = HealthStatus.DEGRADED
            elif cpu_percent > 95:
                status = HealthStatus.UNHEALTHY
            
            return HealthCheck(
                name="cpu_usage",
                status=status,
                response_time=time.time() - start_time,
                details=details,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return HealthCheck(
                name="cpu_usage",
                status=HealthStatus.UNHEALTHY,
                response_time=time.time() - start_time,
                details={},
                timestamp=datetime.now(),
                error_message=str(e)
            )
    
    async def _check_redis_health(self) -> HealthCheck:
        """Check Redis health"""
        start_time = time.time()
        
        try:
            if not self.redis_client:
                return HealthCheck(
                    name="redis",
                    status=HealthStatus.UNKNOWN,
                    response_time=time.time() - start_time,
                    details={},
                    timestamp=datetime.now(),
                    error_message="Redis client not configured"
                )
            
            # Test Redis connection
            self.redis_client.ping()
            
            # Get Redis info
            info = self.redis_client.info()
            
            details = {
                "version": info.get("redis_version"),
                "connected_clients": info.get("connected_clients"),
                "used_memory": info.get("used_memory"),
                "used_memory_peak": info.get("used_memory_peak"),
                "total_commands_processed": info.get("total_commands_processed"),
                "keyspace_hits": info.get("keyspace_hits"),
                "keyspace_misses": info.get("keyspace_misses")
            }
            
            return HealthCheck(
                name="redis",
                status=HealthStatus.HEALTHY,
                response_time=time.time() - start_time,
                details=details,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return HealthCheck(
                name="redis",
                status=HealthStatus.UNHEALTHY,
                response_time=time.time() - start_time,
                details={},
                timestamp=datetime.now(),
                error_message=str(e)
            )
    
    async def _check_database_health(self) -> HealthCheck:
        """Check database health"""
        start_time = time.time()
        
        try:
            if not self.db_pool:
                return HealthCheck(
                    name="database",
                    status=HealthStatus.UNKNOWN,
                    response_time=time.time() - start_time,
                    details={},
                    timestamp=datetime.now(),
                    error_message="Database pool not configured"
                )
            
            # Test database connection
            async with self.db_pool.acquire() as conn:
                # Check connection
                await conn.execute("SELECT 1")
                
                # Get database statistics
                stats = await conn.fetchrow("""
                    SELECT 
                        count(*) as table_count,
                        pg_size_pretty(pg_database_size(current_database())) as db_size
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
                
                # Get active connections
                connections = await conn.fetchrow("""
                    SELECT count(*) as active_connections
                    FROM pg_stat_activity 
                    WHERE state = 'active'
                """)
                
                details = {
                    "table_count": stats['table_count'],
                    "database_size": stats['db_size'],
                    "active_connections": connections['active_connections']
                }
            
            return HealthCheck(
                name="database",
                status=HealthStatus.HEALTHY,
                response_time=time.time() - start_time,
                details=details,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return HealthCheck(
                name="database",
                status=HealthStatus.UNHEALTHY,
                response_time=time.time() - start_time,
                details={},
                timestamp=datetime.now(),
                error_message=str(e)
            )
    
    async def _check_chromadb_health(self) -> HealthCheck:
        """Check ChromaDB health"""
        start_time = time.time()
        
        try:
            if not self.chroma_client:
                return HealthCheck(
                    name="chromadb",
                    status=HealthStatus.UNKNOWN,
                    response_time=time.time() - start_time,
                    details={},
                    timestamp=datetime.now(),
                    error_message="ChromaDB client not configured"
                )
            
            # Test ChromaDB connection
            collections = self.chroma_client.list_collections()
            
            details = {
                "collections_count": len(collections),
                "collections": [col.name for col in collections]
            }
            
            return HealthCheck(
                name="chromadb",
                status=HealthStatus.HEALTHY,
                response_time=time.time() - start_time,
                details=details,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return HealthCheck(
                name="chromadb",
                status=HealthStatus.UNHEALTHY,
                response_time=time.time() - start_time,
                details={},
                timestamp=datetime.now(),
                error_message=str(e)
            )
    
    async def _check_external_apis(self) -> HealthCheck:
        """Check external API health"""
        start_time = time.time()
        
        try:
            # Check Google Gemini API
            gemini_status = await self._check_gemini_api()
            
            # Check other external APIs
            external_apis = {
                "gemini": gemini_status
            }
            
            # Determine overall status
            all_healthy = all(status == HealthStatus.HEALTHY for status in external_apis.values())
            any_unhealthy = any(status == HealthStatus.UNHEALTHY for status in external_apis.values())
            
            if any_unhealthy:
                status = HealthStatus.UNHEALTHY
            elif not all_healthy:
                status = HealthStatus.DEGRADED
            else:
                status = HealthStatus.HEALTHY
            
            return HealthCheck(
                name="external_apis",
                status=status,
                response_time=time.time() - start_time,
                details={"apis": external_apis},
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return HealthCheck(
                name="external_apis",
                status=HealthStatus.UNHEALTHY,
                response_time=time.time() - start_time,
                details={},
                timestamp=datetime.now(),
                error_message=str(e)
            )
    
    async def _check_gemini_api(self) -> HealthStatus:
        """Check Google Gemini API health"""
        try:
            # This would be implemented based on your Gemini API configuration
            # For now, return healthy as placeholder
            return HealthStatus.HEALTHY
        except Exception:
            return HealthStatus.UNHEALTHY
    
    async def _check_application_health(self) -> HealthCheck:
        """Check application-specific health"""
        start_time = time.time()
        
        try:
            # Check application-specific metrics
            details = {
                "uptime": time.time() - self.config.get("start_time", time.time()),
                "version": self.config.get("version", "1.0.0"),
                "environment": self.config.get("environment", "development")
            }
            
            return HealthCheck(
                name="application",
                status=HealthStatus.HEALTHY,
                response_time=time.time() - start_time,
                details=details,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return HealthCheck(
                name="application",
                status=HealthStatus.UNHEALTHY,
                response_time=time.time() - start_time,
                details={},
                timestamp=datetime.now(),
                error_message=str(e)
            )
    
    async def _check_background_tasks(self) -> HealthCheck:
        """Check background task health"""
        start_time = time.time()
        
        try:
            # Check if background tasks are running
            details = {
                "background_tasks_running": True,  # Placeholder
                "task_queue_size": 0  # Placeholder
            }
            
            return HealthCheck(
                name="background_tasks",
                status=HealthStatus.HEALTHY,
                response_time=time.time() - start_time,
                details=details,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return HealthCheck(
                name="background_tasks",
                status=HealthStatus.UNHEALTHY,
                response_time=time.time() - start_time,
                details={},
                timestamp=datetime.now(),
                error_message=str(e)
            )
    
    def _determine_overall_status(self, checks: List[HealthCheck]) -> HealthStatus:
        """Determine overall system health status"""
        if not checks:
            return HealthStatus.UNKNOWN
        
        # Count statuses
        status_counts = {}
        for check in checks:
            status_counts[check.status] = status_counts.get(check.status, 0) + 1
        
        # Determine overall status
        if HealthStatus.UNHEALTHY in status_counts:
            return HealthStatus.UNHEALTHY
        elif HealthStatus.DEGRADED in status_counts:
            return HealthStatus.DEGRADED
        elif HealthStatus.HEALTHY in status_counts:
            return HealthStatus.HEALTHY
        else:
            return HealthStatus.UNKNOWN
    
    async def get_health_summary(self) -> Dict[str, Any]:
        """Get health summary for API response"""
        health = await self.check_system_health()
        
        return {
            "status": health.overall_status.value,
            "timestamp": health.timestamp.isoformat(),
            "uptime": health.uptime,
            "version": health.version,
            "checks": [
                {
                    "name": check.name,
                    "status": check.status.value,
                    "response_time": check.response_time,
                    "details": check.details,
                    "error_message": check.error_message
                }
                for check in health.checks
            ]
        }
    
    async def get_health_history(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get health check history"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        history = []
        for health in self.health_history:
            if health.timestamp >= cutoff_time:
                history.append({
                    "timestamp": health.timestamp.isoformat(),
                    "status": health.overall_status.value,
                    "uptime": health.uptime
                })
        
        return history

# Health check endpoints for FastAPI
async def health_check_endpoint(health_checker: HealthChecker):
    """Health check endpoint"""
    try:
        health_summary = await health_checker.get_health_summary()
        
        # Return appropriate HTTP status based on health
        status_code = 200
        if health_summary["status"] == "unhealthy":
            status_code = 503
        elif health_summary["status"] == "degraded":
            status_code = 200  # Still operational but degraded
        
        return {
            "status": health_summary["status"],
            "timestamp": health_summary["timestamp"],
            "checks": health_summary["checks"]
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Health check failed")

async def health_detailed_endpoint(health_checker: HealthChecker):
    """Detailed health check endpoint"""
    try:
        return await health_checker.get_health_summary()
    except Exception as e:
        logger.error(f"Detailed health check failed: {e}")
        raise HTTPException(status_code=503, detail="Detailed health check failed")

async def health_history_endpoint(health_checker: HealthChecker, hours: int = 24):
    """Health history endpoint"""
    try:
        return await health_checker.get_health_history(hours)
    except Exception as e:
        logger.error(f"Health history failed: {e}")
        raise HTTPException(status_code=500, detail="Health history failed")
