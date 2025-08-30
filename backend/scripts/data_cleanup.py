#!/usr/bin/env python3
"""
Data Cleanup Script for Dubai Real Estate RAG System
Automatically removes old test data and prevents database bloat
"""

import os
import sys
import asyncio
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataCleanupManager:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL", "postgresql://postgres:password123@localhost:5432/real_estate_db")
        self.engine = create_engine(self.db_url)
        
    async def cleanup_old_conversations(self, days_old: int = 30):
        """Remove old conversations and their messages"""
        try:
            with self.engine.connect() as conn:
                # Get count before deletion
                count_result = conn.execute(text("""
                    SELECT COUNT(*) FROM conversations 
                    WHERE created_at < NOW() - INTERVAL ':days days'
                """), {"days": days_old})
                old_count = count_result.fetchone()[0]
                
                # Delete old conversations
                result = conn.execute(text("""
                    DELETE FROM conversations 
                    WHERE created_at < NOW() - INTERVAL ':days days'
                    AND is_active = FALSE
                """), {"days": days_old})
                
                # Delete orphaned messages
                conn.execute(text("""
                    DELETE FROM messages 
                    WHERE conversation_id NOT IN (SELECT id FROM conversations)
                """))
                
                conn.commit()
                logger.info(f"✅ Cleaned up {old_count} old conversations")
                
        except Exception as e:
            logger.error(f"❌ Error cleaning up conversations: {e}")
    
    async def cleanup_old_messages(self, days_old: int = 90):
        """Remove old messages while keeping recent ones"""
        try:
            with self.engine.connect() as conn:
                # Get count before deletion
                count_result = conn.execute(text("""
                    SELECT COUNT(*) FROM messages 
                    WHERE timestamp < NOW() - INTERVAL ':days days'
                """), {"days": days_old})
                old_count = count_result.fetchone()[0]
                
                # Delete old messages
                result = conn.execute(text("""
                    DELETE FROM messages 
                    WHERE timestamp < NOW() - INTERVAL ':days days'
                """), {"days": days_old})
                
                conn.commit()
                logger.info(f"✅ Cleaned up {old_count} old messages")
                
        except Exception as e:
            logger.error(f"❌ Error cleaning up messages: {e}")
    
    async def archive_important_conversations(self, days_old: int = 90):
        """Archive important conversations instead of deleting"""
        try:
            with self.engine.connect() as conn:
                # Create archive table if it doesn't exist
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS archived_conversations (
                        id SERIAL PRIMARY KEY,
                        original_id INTEGER,
                        session_id VARCHAR(255),
                        title VARCHAR(255),
                        created_at TIMESTAMP,
                        archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        message_count INTEGER
                    )
                """))
                
                # Archive conversations with many messages
                result = conn.execute(text("""
                    INSERT INTO archived_conversations (original_id, session_id, title, created_at, message_count)
                    SELECT 
                        c.id, c.session_id, c.title, c.created_at,
                        (SELECT COUNT(*) FROM messages WHERE conversation_id = c.id) as message_count
                    FROM conversations c
                    WHERE c.created_at < NOW() - INTERVAL ':days days'
                    AND c.is_active = TRUE
                    AND (SELECT COUNT(*) FROM messages WHERE conversation_id = c.id) > 5
                """), {"days": days_old})
                
                conn.commit()
                logger.info(f"✅ Archived important conversations")
                
        except Exception as e:
            logger.error(f"❌ Error archiving conversations: {e}")
    
    async def cleanup_test_data(self):
        """Remove test data and development artifacts"""
        try:
            with self.engine.connect() as conn:
                # Remove test conversations
                test_result = conn.execute(text("""
                    DELETE FROM conversations 
                    WHERE title ILIKE '%test%' 
                    OR title ILIKE '%demo%'
                    OR title ILIKE '%example%'
                """))
                
                # Remove conversations with very few messages (likely test data)
                sparse_result = conn.execute(text("""
                    DELETE FROM conversations 
                    WHERE id IN (
                        SELECT c.id FROM conversations c
                        LEFT JOIN messages m ON c.id = m.conversation_id
                        GROUP BY c.id
                        HAVING COUNT(m.id) <= 2
                    )
                    AND created_at < NOW() - INTERVAL '7 days'
                """))
                
                conn.commit()
                logger.info("✅ Cleaned up test data")
                
        except Exception as e:
            logger.error(f"❌ Error cleaning up test data: {e}")
    
    async def optimize_database(self):
        """Optimize database performance"""
        try:
            with self.engine.connect() as conn:
                # Analyze tables for better query planning
                conn.execute(text("ANALYZE conversations"))
                conn.execute(text("ANALYZE messages"))
                conn.execute(text("ANALYZE properties"))
                
                # Vacuum to reclaim space
                conn.execute(text("VACUUM ANALYZE"))
                
                conn.commit()
                logger.info("✅ Database optimized")
                
        except Exception as e:
            logger.error(f"❌ Error optimizing database: {e}")
    
    async def get_database_stats(self):
        """Get current database statistics"""
        try:
            with self.engine.connect() as conn:
                # Get table sizes
                stats = {}
                
                # Conversations count
                result = conn.execute(text("SELECT COUNT(*) FROM conversations"))
                stats['conversations'] = result.fetchone()[0]
                
                # Messages count
                result = conn.execute(text("SELECT COUNT(*) FROM messages"))
                stats['messages'] = result.fetchone()[0]
                
                # Properties count
                result = conn.execute(text("SELECT COUNT(*) FROM properties"))
                stats['properties'] = result.fetchone()[0]
                
                # Database size
                result = conn.execute(text("""
                    SELECT pg_size_pretty(pg_database_size('real_estate_db')) as db_size
                """))
                stats['database_size'] = result.fetchone()[0]
                
                # Old data counts
                result = conn.execute(text("""
                    SELECT COUNT(*) FROM conversations 
                    WHERE created_at < NOW() - INTERVAL '30 days'
                """))
                stats['old_conversations'] = result.fetchone()[0]
                
                result = conn.execute(text("""
                    SELECT COUNT(*) FROM messages 
                    WHERE timestamp < NOW() - INTERVAL '90 days'
                """))
                stats['old_messages'] = result.fetchone()[0]
                
                return stats
                
        except Exception as e:
            logger.error(f"❌ Error getting database stats: {e}")
            return {}
    
    async def run_full_cleanup(self):
        """Run complete cleanup process"""
        logger.info("🧹 Starting database cleanup...")
        
        # Get stats before cleanup
        before_stats = await self.get_database_stats()
        logger.info(f"📊 Before cleanup: {before_stats}")
        
        # Run cleanup tasks
        await self.cleanup_test_data()
        await self.cleanup_old_conversations(30)  # 30 days
        await self.cleanup_old_messages(90)       # 90 days
        await self.archive_important_conversations(90)
        await self.optimize_database()
        
        # Get stats after cleanup
        after_stats = await self.get_database_stats()
        logger.info(f"📊 After cleanup: {after_stats}")
        
        logger.info("✅ Database cleanup completed!")

async def main():
    """Main cleanup function"""
    cleanup_manager = DataCleanupManager()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "stats":
            stats = await cleanup_manager.get_database_stats()
            print("📊 Database Statistics:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
        
        elif command == "cleanup":
            await cleanup_manager.run_full_cleanup()
        
        elif command == "test":
            await cleanup_manager.cleanup_test_data()
        
        elif command == "conversations":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            await cleanup_manager.cleanup_old_conversations(days)
        
        elif command == "messages":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 90
            await cleanup_manager.cleanup_old_messages(days)
        
        else:
            print("Usage: python data_cleanup.py [stats|cleanup|test|conversations|messages] [days]")
    else:
        # Default: run full cleanup
        await cleanup_manager.run_full_cleanup()

if __name__ == "__main__":
    asyncio.run(main())
