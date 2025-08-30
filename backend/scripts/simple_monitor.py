#!/usr/bin/env python3
"""
Simple Performance Monitor for Dubai Real Estate RAG System
"""

import os
import asyncio
from datetime import datetime
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleMonitor:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL", "postgresql://postgres:password123@localhost:5432/real_estate_db")
        self.engine = create_engine(self.db_url)
    
    async def check_database_health(self):
        """Check database health and performance"""
        try:
            with self.engine.connect() as conn:
                # Get basic stats
                stats = {}
                
                # Conversations count
                result = conn.execute(text("SELECT COUNT(*) FROM conversations"))
                stats['conversations'] = result.fetchone()[0]
                
                # Messages count
                result = conn.execute(text("SELECT COUNT(*) FROM messages"))
                stats['messages'] = result.fetchone()[0]
                
                # Database size
                result = conn.execute(text("SELECT pg_size_pretty(pg_database_size('real_estate_db'))"))
                stats['database_size'] = result.fetchone()[0]
                
                # Active connections
                result = conn.execute(text("SELECT count(*) FROM pg_stat_activity WHERE state = 'active'"))
                stats['active_connections'] = result.fetchone()[0]
                
                # Check for potential issues
                alerts = []
                
                if stats['conversations'] > 1000:
                    alerts.append(f"⚠️ High conversation count: {stats['conversations']}")
                
                if stats['messages'] > 10000:
                    alerts.append(f"⚠️ High message count: {stats['messages']}")
                
                if stats['active_connections'] > 20:
                    alerts.append(f"⚠️ High active connections: {stats['active_connections']}")
                
                if 'GB' in stats['database_size']:
                    size_gb = float(stats['database_size'].split()[0])
                    if size_gb > 5:
                        alerts.append(f"⚠️ Large database size: {stats['database_size']}")
                
                return {
                    'timestamp': datetime.now().isoformat(),
                    'stats': stats,
                    'alerts': alerts,
                    'status': 'healthy' if not alerts else 'warning'
                }
                
        except Exception as e:
            logger.error(f"❌ Database health check failed: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'status': 'error'
            }
    
    async def run_health_check(self):
        """Run health check and log results"""
        result = await self.check_database_health()
        
        if result['status'] == 'healthy':
            logger.info("✅ Database is healthy")
        elif result['status'] == 'warning':
            logger.warning("⚠️ Database has warnings:")
            for alert in result['alerts']:
                logger.warning(f"  {alert}")
        else:
            logger.error(f"❌ Database error: {result.get('error', 'Unknown error')}")
        
        return result

async def main():
    monitor = SimpleMonitor()
    await monitor.run_health_check()

if __name__ == "__main__":
    asyncio.run(main())
