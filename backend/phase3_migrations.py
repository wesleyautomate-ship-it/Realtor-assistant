#!/usr/bin/env python3
"""
Phase 3 Database Migrations for Advanced In-Chat Experience

This script creates the necessary database tables and schema updates
for Phase 3: Advanced In-Chat Experience implementation.
"""

import logging
from sqlalchemy import create_engine, text
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Phase3DatabaseMigration:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        
    def run_migrations(self):
        """Run all Phase 3 migrations"""
        logger.info("🚀 Starting Phase 3 database migrations...")
        
        try:
            with self.engine.connect() as conn:
                # Create new Phase 3 tables
                self._create_entity_detections_table(conn)
                self._create_context_cache_table(conn)
                self._create_rich_content_metadata_table(conn)
                
                # Update existing tables for Phase 3
                self._update_messages_table(conn)
                self._update_conversations_table(conn)
                
                # Create indexes for performance
                self._create_phase3_indexes(conn)
                
                conn.commit()
                logger.info("✅ All Phase 3 migrations completed successfully!")
                
        except Exception as e:
            logger.error(f"❌ Phase 3 migration failed: {e}")
            raise
    
    def _create_entity_detections_table(self, conn):
        """Create entity_detections table for storing detected entities"""
        logger.info("🔍 Creating entity_detections table...")
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS entity_detections (
                id SERIAL PRIMARY KEY,
                message_id INTEGER REFERENCES messages(id) ON DELETE CASCADE,
                entity_type VARCHAR(50) NOT NULL, -- 'property', 'client', 'location', 'market_data'
                entity_value TEXT NOT NULL,
                confidence_score DECIMAL(3,2) NOT NULL,
                context_source VARCHAR(100) NOT NULL, -- 'pattern_match', 'keyword_match'
                metadata JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        # Create indexes for entity detections
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_entity_detections_message_id 
            ON entity_detections(message_id)
        """))
        
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_entity_detections_entity_type 
            ON entity_detections(entity_type)
        """))
        
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_entity_detections_confidence 
            ON entity_detections(confidence_score DESC)
        """))
        
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_entity_detections_created_at 
            ON entity_detections(created_at)
        """))
        
        logger.info("✅ entity_detections table created successfully")
    
    def _create_context_cache_table(self, conn):
        """Create context_cache table for caching entity context data"""
        logger.info("💾 Creating context_cache table...")
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS context_cache (
                id SERIAL PRIMARY KEY,
                entity_type VARCHAR(50) NOT NULL,
                entity_id VARCHAR(255) NOT NULL,
                context_data JSONB,
                last_fetched TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(entity_type, entity_id)
            )
        """))
        
        # Create indexes for context cache
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_context_cache_entity_type_id 
            ON context_cache(entity_type, entity_id)
        """))
        
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_context_cache_expires_at 
            ON context_cache(expires_at)
        """))
        
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_context_cache_last_fetched 
            ON context_cache(last_fetched)
        """))
        
        logger.info("✅ context_cache table created successfully")
    
    def _create_rich_content_metadata_table(self, conn):
        """Create rich_content_metadata table for storing rich content information"""
        logger.info("🎨 Creating rich_content_metadata table...")
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS rich_content_metadata (
                id SERIAL PRIMARY KEY,
                message_id INTEGER REFERENCES messages(id) ON DELETE CASCADE,
                content_type VARCHAR(50) NOT NULL, -- 'property_card', 'content_preview', 'market_chart'
                content_data JSONB NOT NULL,
                interactive_elements JSONB,
                rendering_config JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        # Create indexes for rich content metadata
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_rich_content_message_id 
            ON rich_content_metadata(message_id)
        """))
        
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_rich_content_type 
            ON rich_content_metadata(content_type)
        """))
        
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_rich_content_created_at 
            ON rich_content_metadata(created_at)
        """))
        
        logger.info("✅ rich_content_metadata table created successfully")
    
    def _update_messages_table(self, conn):
        """Update messages table with Phase 3 columns"""
        logger.info("📝 Updating messages table for Phase 3...")
        
        # Check if columns already exist
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'messages' 
            AND column_name IN ('entities_detected', 'rich_content_metadata', 'context_summary')
        """))
        
        existing_columns = {row[0] for row in result}
        
        # Add entities_detected column if it doesn't exist
        if 'entities_detected' not in existing_columns:
            conn.execute(text("""
                ALTER TABLE messages 
                ADD COLUMN entities_detected JSONB
            """))
            logger.info("✅ Added entities_detected column to messages table")
        
        # Add rich_content_metadata column if it doesn't exist
        if 'rich_content_metadata' not in existing_columns:
            conn.execute(text("""
                ALTER TABLE messages 
                ADD COLUMN rich_content_metadata JSONB
            """))
            logger.info("✅ Added rich_content_metadata column to messages table")
        
        # Add context_summary column if it doesn't exist
        if 'context_summary' not in existing_columns:
            conn.execute(text("""
                ALTER TABLE messages 
                ADD COLUMN context_summary JSONB
            """))
            logger.info("✅ Added context_summary column to messages table")
        
        logger.info("✅ Messages table updated successfully")
    
    def _update_conversations_table(self, conn):
        """Update conversations table with Phase 3 columns"""
        logger.info("💬 Updating conversations table for Phase 3...")
        
        # Check if columns already exist
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'conversations' 
            AND column_name IN ('context_summary', 'active_entities', 'entity_history')
        """))
        
        existing_columns = {row[0] for row in result}
        
        # Add context_summary column if it doesn't exist
        if 'context_summary' not in existing_columns:
            conn.execute(text("""
                ALTER TABLE conversations 
                ADD COLUMN context_summary JSONB
            """))
            logger.info("✅ Added context_summary column to conversations table")
        
        # Add active_entities column if it doesn't exist
        if 'active_entities' not in existing_columns:
            conn.execute(text("""
                ALTER TABLE conversations 
                ADD COLUMN active_entities JSONB
            """))
            logger.info("✅ Added active_entities column to conversations table")
        
        # Add entity_history column if it doesn't exist
        if 'entity_history' not in existing_columns:
            conn.execute(text("""
                ALTER TABLE conversations 
                ADD COLUMN entity_history JSONB
            """))
            logger.info("✅ Added entity_history column to conversations table")
        
        logger.info("✅ Conversations table updated successfully")
    
    def _create_phase3_indexes(self, conn):
        """Create additional indexes for Phase 3 performance"""
        logger.info("⚡ Creating Phase 3 performance indexes...")
        
        # Index for messages with entities
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_messages_entities_detected 
            ON messages USING GIN (entities_detected)
        """))
        
        # Index for messages with rich content
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_messages_rich_content 
            ON messages USING GIN (rich_content_metadata)
        """))
        
        # Index for conversations with context
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_conversations_context 
            ON conversations USING GIN (context_summary)
        """))
        
        # Index for conversations with active entities
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_conversations_active_entities 
            ON conversations USING GIN (active_entities)
        """))
        
        # Index for context cache data
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_context_cache_data 
            ON context_cache USING GIN (context_data)
        """))
        
        logger.info("✅ Phase 3 performance indexes created successfully")
    
    def verify_migrations(self):
        """Verify that all Phase 3 migrations were applied successfully"""
        logger.info("🔍 Verifying Phase 3 migrations...")
        
        try:
            with self.engine.connect() as conn:
                # Check if all required tables exist
                required_tables = [
                    'entity_detections',
                    'context_cache', 
                    'rich_content_metadata'
                ]
                
                for table in required_tables:
                    result = conn.execute(text("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_name = :table_name
                        )
                    """), {'table_name': table})
                    
                    exists = result.scalar()
                    if exists:
                        logger.info(f"✅ Table {table} exists")
                    else:
                        logger.error(f"❌ Table {table} missing")
                        return False
                
                # Check if required columns exist in messages table
                required_columns = ['entities_detected', 'rich_content_metadata', 'context_summary']
                for column in required_columns:
                    result = conn.execute(text("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.columns 
                            WHERE table_name = 'messages' AND column_name = :column_name
                        )
                    """), {'column_name': column})
                    
                    exists = result.scalar()
                    if exists:
                        logger.info(f"✅ Column {column} exists in messages table")
                    else:
                        logger.error(f"❌ Column {column} missing from messages table")
                        return False
                
                # Check if required columns exist in conversations table
                required_columns = ['context_summary', 'active_entities', 'entity_history']
                for column in required_columns:
                    result = conn.execute(text("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.columns 
                            WHERE table_name = 'conversations' AND column_name = :column_name
                        )
                    """), {'column_name': column})
                    
                    exists = result.scalar()
                    if exists:
                        logger.info(f"✅ Column {column} exists in conversations table")
                    else:
                        logger.error(f"❌ Column {column} missing from conversations table")
                        return False
                
                logger.info("✅ All Phase 3 migrations verified successfully!")
                return True
                
        except Exception as e:
            logger.error(f"❌ Migration verification failed: {e}")
            return False

def main():
    """Run the Phase 3 migration script"""
    db_url = os.getenv('DATABASE_URL', 'postgresql://admin:password123@localhost:5432/real_estate_db')
    
    migration = Phase3DatabaseMigration(db_url)
    
    # Run migrations
    migration.run_migrations()
    
    # Verify migrations
    if migration.verify_migrations():
        print("🎉 Phase 3 database migrations completed and verified successfully!")
    else:
        print("❌ Phase 3 database migrations verification failed!")
        exit(1)

if __name__ == "__main__":
    main()
