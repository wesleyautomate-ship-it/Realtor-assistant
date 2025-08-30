#!/usr/bin/env python3
"""
Performance Monitor for Dubai Real Estate RAG System
Monitors database performance and prevents overload
"""

import os
import sys
import asyncio
import time
import psutil
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import logging
import json

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceMonitor:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL", "postgresql://postgres:password123@localhost:5432/real_estate_db")
        self.engine = create_engine(self.db_url)
        self.performance_data = []
        
    async def monitor_database_performance(self):
        """Monitor database performance metrics"""
        try:
            with self.engine.connect() as conn:
                # Get database size
                size_result = conn.execute(text("""
                    SELECT pg_size_pretty(pg_database_size('real_estate_db')) as db_size
                """))
                db_size = size_result.fetchone()[0]
                
                # Get table sizes
                table_sizes = {}
                tables = ['conversations', 'messages', 'properties']
                for table in tables:
                    result = conn.execute(text(f"""
                        SELECT COUNT(*) as count, 
                               pg_size_pretty(pg_total_relation_size('{table}')) as size
                        FROM {table}
                    """))
                    row = result.fetchone()
                    table_sizes[table] = {
                        'count': row[0],
                        'size': row[1]
                    }
                
                # Get slow queries
                slow_queries = conn.execute(text("""
                    SELECT query, mean_time, calls
                    FROM pg_stat_statements 
                    WHERE mean_time > 1000  -- Queries taking more than 1 second
                    ORDER BY mean_time DESC 
                    LIMIT 5
                """))
                
                # Get connection count
                connections = conn.execute(text("""
                    SELECT count(*) as active_connections 
                    FROM pg_stat_activity 
                    WHERE state = 'active'
                """))
                active_connections = connections.fetchone()[0]
                
                # Get cache hit ratio
                cache_stats = conn.execute(text("""
                    SELECT 
                        sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as cache_hit_ratio
                    FROM pg_statio_user_tables
                """))
                cache_hit_ratio = cache_stats.fetchone()[0] or 0
                
                return {
                    'timestamp': datetime.now().isoformat(),
                    'database_size': db_size,
                    'table_sizes': table_sizes,
                    'active_connections': active_connections,
                    'cache_hit_ratio': round(cache_hit_ratio * 100, 2),
                    'slow_queries': [dict(row) for row in slow_queries]
                }
                
        except Exception as e:
            logger.error(f"❌ Error monitoring database: {e}")
            return None
    
    async def monitor_system_performance(self):
        """Monitor system performance metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            
            # Disk usage
            disk = psutil.disk_usage('/')
            
            # Network I/O
            network = psutil.net_io_counters()
            
            return {
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available': memory.available,
                'disk_percent': disk.percent,
                'disk_free': disk.free,
                'network_bytes_sent': network.bytes_sent,
                'network_bytes_recv': network.bytes_recv
            }
            
        except Exception as e:
            logger.error(f"❌ Error monitoring system: {e}")
            return None
    
    async def check_performance_thresholds(self, db_metrics, system_metrics):
        """Check if performance metrics exceed thresholds"""
        alerts = []
        
        if db_metrics:
            # Database size alert
            if 'GB' in db_metrics['database_size']:
                size_gb = float(db_metrics['database_size'].split()[0])
                if size_gb > 10:  # 10GB threshold
                    alerts.append(f"⚠️ Database size ({db_metrics['database_size']}) exceeds 10GB threshold")
            
            # Connection count alert
            if db_metrics['active_connections'] > 50:  # 50 connections threshold
                alerts.append(f"⚠️ High active connections: {db_metrics['active_connections']}")
            
            # Cache hit ratio alert
            if db_metrics['cache_hit_ratio'] < 80:  # 80% threshold
                alerts.append(f"⚠️ Low cache hit ratio: {db_metrics['cache_hit_ratio']}%")
            
            # Table size alerts
            for table, data in db_metrics['table_sizes'].items():
                if data['count'] > 100000:  # 100k records threshold
                    alerts.append(f"⚠️ Large {table} table: {data['count']} records")
        
        if system_metrics:
            # CPU usage alert
            if system_metrics['cpu_percent'] > 80:  # 80% threshold
                alerts.append(f"⚠️ High CPU usage: {system_metrics['cpu_percent']}%")
            
            # Memory usage alert
            if system_metrics['memory_percent'] > 85:  # 85% threshold
                alerts.append(f"⚠️ High memory usage: {system_metrics['memory_percent']}%")
            
            # Disk usage alert
            if system_metrics['disk_percent'] > 90:  # 90% threshold
                alerts.append(f"⚠️ High disk usage: {system_metrics['disk_percent']}%")
        
        return alerts
    
    async def generate_performance_report(self):
        """Generate comprehensive performance report"""
        logger.info("📊 Generating performance report...")
        
        # Collect metrics
        db_metrics = await self.monitor_database_performance()
        system_metrics = await self.monitor_system_performance()
        
        # Check thresholds
        alerts = await self.check_performance_thresholds(db_metrics, system_metrics)
        
        # Create report
        report = {
            'timestamp': datetime.now().isoformat(),
            'database_metrics': db_metrics,
            'system_metrics': system_metrics,
            'alerts': alerts,
            'recommendations': []
        }
        
        # Generate recommendations
        if db_metrics:
            if db_metrics['cache_hit_ratio'] < 80:
                report['recommendations'].append("Increase database cache size")
            
            if db_metrics['active_connections'] > 30:
                report['recommendations'].append("Optimize connection pooling")
            
            if any(data['count'] > 50000 for data in db_metrics['table_sizes'].values()):
                report['recommendations'].append("Implement data archiving strategy")
        
        if system_metrics:
            if system_metrics['cpu_percent'] > 70:
                report['recommendations'].append("Consider scaling up CPU resources")
            
            if system_metrics['memory_percent'] > 80:
                report['recommendations'].append("Increase memory allocation")
        
        # Save report
        self.performance_data.append(report)
        
        # Keep only last 100 reports
        if len(self.performance_data) > 100:
            self.performance_data = self.performance_data[-100:]
        
        return report
    
    async def save_performance_data(self, filename=None):
        """Save performance data to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_report_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.performance_data, f, indent=2)
            logger.info(f"✅ Performance data saved to {filename}")
        except Exception as e:
            logger.error(f"❌ Error saving performance data: {e}")
    
    async def continuous_monitoring(self, interval=300):  # 5 minutes
        """Run continuous performance monitoring"""
        logger.info(f"🔄 Starting continuous monitoring (interval: {interval}s)")
        
        try:
            while True:
                report = await self.generate_performance_report()
                
                # Log alerts
                if report['alerts']:
                    logger.warning("🚨 Performance Alerts:")
                    for alert in report['alerts']:
                        logger.warning(f"  {alert}")
                
                # Log summary
                if report['database_metrics']:
                    db = report['database_metrics']
                    logger.info(f"📊 DB: {db['database_size']}, Connections: {db['active_connections']}, Cache: {db['cache_hit_ratio']}%")
                
                if report['system_metrics']:
                    sys_metrics = report['system_metrics']
                    logger.info(f"💻 CPU: {sys_metrics['cpu_percent']}%, Memory: {sys_metrics['memory_percent']}%, Disk: {sys_metrics['disk_percent']}%")
                
                # Wait for next interval
                await asyncio.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("🛑 Monitoring stopped by user")
        except Exception as e:
            logger.error(f"❌ Monitoring error: {e}")

async def main():
    """Main monitoring function"""
    monitor = PerformanceMonitor()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "report":
            report = await monitor.generate_performance_report()
            print(json.dumps(report, indent=2))
        
        elif command == "monitor":
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300
            await monitor.continuous_monitoring(interval)
        
        elif command == "save":
            filename = sys.argv[2] if len(sys.argv) > 2 else None
            await monitor.save_performance_data(filename)
        
        else:
            print("Usage: python performance_monitor.py [report|monitor|save] [interval|filename]")
    else:
        # Default: generate single report
        report = await monitor.generate_performance_report()
        print(json.dumps(report, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
