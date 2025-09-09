#!/usr/bin/env python3
"""
AI Assistant Schema Migration Script
===================================

This script runs the AI assistant database migration for Phase 2.
It creates all the necessary tables for the AI-powered assistant system.
"""

import sys
import os
import logging
from pathlib import Path
from sqlalchemy import text

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from database_manager import get_db_connection
from config.settings import DATABASE_URL

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_ai_assistant_migration():
    """Run the AI assistant schema migration"""
    try:
        logger.info("=" * 60)
        logger.info("AI ASSISTANT SCHEMA MIGRATION")
        logger.info("=" * 60)
        logger.info("Starting AI assistant schema migration...")
        
        # Read migration SQL file
        migration_file = backend_dir / "migrations" / "ai_assistant_schema_migration.sql"
        
        if not migration_file.exists():
            logger.error(f"Migration file not found: {migration_file}")
            return False
        
        with open(migration_file, 'r', encoding='utf-8') as f:
            migration_sql = f.read()
        
        # Connect to database
        logger.info("Connecting to database...")
        
        with get_db_connection() as conn:
            try:
                # Execute migration
                logger.info("Executing migration SQL...")
                conn.execute(text(migration_sql))
                conn.commit()
                
                logger.info("✅ AI assistant schema migration completed successfully!")
                
                # Verify tables were created
                verify_tables(conn)
                
                return True
                
            except Exception as e:
                logger.error(f"Error executing migration: {e}")
                conn.rollback()
                return False
            
    except Exception as e:
        logger.error(f"Error running migration: {e}")
        return False

def verify_tables(conn):
    """Verify that all AI assistant tables were created successfully"""
    try:
        logger.info("Verifying table creation...")
        
        # List of tables that should be created
        required_tables = [
            'ai_requests',
            'human_experts',
            'content_deliverables',
            'voice_requests',
            'task_automation',
            'smart_nurturing_sequences',
            'dubai_property_data',
            'rera_compliance_data',
            'retention_analytics'
        ]
        
        for table in required_tables:
            result = conn.execute(text(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = '{table}'
                );
            """))
            
            exists = result.fetchone()[0]
            if exists:
                logger.info(f"✅ Table '{table}' created successfully")
            else:
                logger.error(f"❌ Table '{table}' was not created")
        
        # Check if default human expert was created
        result = conn.execute(text("SELECT COUNT(*) FROM human_experts WHERE expertise_area = 'general';"))
        count = result.fetchone()[0]
        
        if count > 0:
            logger.info("✅ Default human expert created successfully")
        else:
            logger.warning("⚠️ No default human expert found")
        
        # Check indexes
        logger.info("Verifying indexes...")
        index_tables = ['ai_requests', 'human_experts', 'content_deliverables', 'voice_requests']
        
        for table in index_tables:
            result = conn.execute(text(f"""
                SELECT COUNT(*) FROM pg_indexes 
                WHERE tablename = '{table}';
            """))
            
            index_count = result.fetchone()[0]
            if index_count > 0:
                logger.info(f"✅ Indexes created for '{table}' table")
            else:
                logger.warning(f"⚠️ No indexes found for '{table}' table")
        
        logger.info("✅ Table verification completed")
        
    except Exception as e:
        logger.error(f"Error verifying tables: {e}")

def check_database_connection():
    """Check if database connection is working"""
    try:
        logger.info("Testing database connection...")
        
        with get_db_connection() as conn:
            result = conn.execute(text("SELECT 1;"))
            if result.fetchone()[0] == 1:
                logger.info("✅ Database connection successful")
                return True
            else:
                logger.error("❌ Database connection failed")
                return False
                
    except Exception as e:
        logger.error(f"❌ Database connection error: {e}")
        return False

def main():
    """Main function"""
    try:
        logger.info("Starting AI Assistant Migration Process...")
        
        # Check database connection
        if not check_database_connection():
            logger.error("❌ Migration failed - Database connection failed!")
            return False
        
        # Run migration
        if run_ai_assistant_migration():
            logger.info("🎉 AI Assistant migration completed successfully!")
            logger.info("")
            logger.info("Next steps:")
            logger.info("1. Update main.py to include the AI assistant router")
            logger.info("2. Test the AI assistant endpoints")
            logger.info("3. Create frontend interfaces for AI assistant")
            logger.info("4. Set up human expert accounts")
            return True
        else:
            logger.error("❌ Migration failed!")
            return False
            
    except Exception as e:
        logger.error(f"❌ Migration process failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
