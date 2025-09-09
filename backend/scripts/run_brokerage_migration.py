#!/usr/bin/env python3
"""
Brokerage Schema Migration Script
=================================

This script runs the brokerage-centric schema migration for Phase 1.
It creates all necessary tables and relationships for the new architecture.
"""

import os
import sys
import logging
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from database_manager import get_db_connection
from config.settings import DATABASE_URL
from sqlalchemy import text

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_migration():
    """Run the brokerage schema migration"""
    try:
        logger.info("Starting brokerage schema migration...")
        
        # Read the migration SQL file
        migration_file = backend_dir / "migrations" / "brokerage_schema_migration.sql"
        
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
                
                logger.info("✅ Brokerage schema migration completed successfully!")
                
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
    """Verify that all required tables were created"""
    try:
        logger.info("Verifying table creation...")
        
        required_tables = [
            'brokerages',
            'team_performance',
            'knowledge_base',
            'brand_assets',
            'workflow_automation',
            'client_nurturing',
            'compliance_rules',
            'agent_consistency_metrics',
            'lead_retention_analytics',
            'workflow_efficiency_metrics'
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
        
        # Check if brokerage_id was added to existing tables
        existing_tables = ['users', 'properties', 'conversations']
        
        for table in existing_tables:
            result = conn.execute(text(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.columns 
                    WHERE table_name = '{table}' AND column_name = 'brokerage_id'
                );
            """))
            
            exists = result.fetchone()[0]
            if exists:
                logger.info(f"✅ Column 'brokerage_id' added to '{table}' table")
            else:
                logger.warning(f"⚠️ Column 'brokerage_id' not found in '{table}' table")
        
        # Check default brokerage creation
        result = conn.execute(text("SELECT COUNT(*) FROM brokerages WHERE license_number = 'DEFAULT-001';"))
        count = result.fetchone()[0]
        
        if count > 0:
            logger.info("✅ Default brokerage created successfully")
        else:
            logger.warning("⚠️ Default brokerage was not created")
        
        logger.info("Table verification completed")
        
    except Exception as e:
        logger.error(f"Error verifying tables: {e}")

def main():
    """Main function"""
    logger.info("=" * 60)
    logger.info("BROKERAGE SCHEMA MIGRATION")
    logger.info("=" * 60)
    
    success = run_migration()
    
    if success:
        logger.info("🎉 Migration completed successfully!")
        logger.info("You can now start using the brokerage-centric features.")
    else:
        logger.error("❌ Migration failed!")
        logger.error("Please check the logs and fix any issues before retrying.")
        sys.exit(1)

if __name__ == "__main__":
    main()
