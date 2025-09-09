#!/usr/bin/env python3
"""
Phase 3 Advanced Schema Migration Script
=======================================

This script runs the Phase 3 advanced database migration.
It creates all the necessary tables for advanced analytics, Dubai data integration, and developer panel.
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

def run_phase3_migration():
    """Run the Phase 3 advanced schema migration"""
    try:
        logger.info("=" * 60)
        logger.info("PHASE 3 ADVANCED SCHEMA MIGRATION")
        logger.info("=" * 60)
        logger.info("Starting Phase 3 advanced schema migration...")
        
        # Read migration SQL file
        migration_file = backend_dir / "migrations" / "phase3_advanced_schema_migration.sql"
        
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
                
                logger.info("✅ Phase 3 advanced schema migration completed successfully!")
                
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
    """Verify that all Phase 3 tables were created successfully"""
    try:
        logger.info("Verifying table creation...")
        
        # List of tables that should be created
        required_tables = [
            'predictive_performance_models',
            'benchmarking_data',
            'dubai_market_data',
            'rera_integration_data',
            'system_performance_metrics',
            'user_activity_analytics',
            'ai_processing_analytics',
            'multi_brokerage_analytics',
            'developer_panel_settings',
            'system_alerts'
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
        
        # Check if sample data was inserted
        result = conn.execute(text("SELECT COUNT(*) FROM dubai_market_data;"))
        market_data_count = result.fetchone()[0]
        
        if market_data_count > 0:
            logger.info(f"✅ Sample Dubai market data inserted ({market_data_count} records)")
        else:
            logger.warning("⚠️ No sample Dubai market data found")
        
        result = conn.execute(text("SELECT COUNT(*) FROM system_performance_metrics;"))
        performance_metrics_count = result.fetchone()[0]
        
        if performance_metrics_count > 0:
            logger.info(f"✅ Sample system performance metrics inserted ({performance_metrics_count} records)")
        else:
            logger.warning("⚠️ No sample system performance metrics found")
        
        result = conn.execute(text("SELECT COUNT(*) FROM multi_brokerage_analytics;"))
        analytics_count = result.fetchone()[0]
        
        if analytics_count > 0:
            logger.info(f"✅ Sample multi-brokerage analytics inserted ({analytics_count} records)")
        else:
            logger.warning("⚠️ No sample multi-brokerage analytics found")
        
        # Check indexes
        logger.info("Verifying indexes...")
        index_tables = ['predictive_performance_models', 'benchmarking_data', 'dubai_market_data', 'system_alerts']
        
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

def check_phase2_dependencies():
    """Check if Phase 2 tables exist (dependencies)"""
    try:
        logger.info("Checking Phase 2 dependencies...")
        
        with get_db_connection() as conn:
            # Check for Phase 2 tables
            phase2_tables = [
                'ai_requests',
                'human_experts',
                'content_deliverables',
                'voice_requests',
                'brokerages'
            ]
            
            missing_tables = []
            for table in phase2_tables:
                result = conn.execute(text(f"""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = '{table}'
                    );
                """))
                
                exists = result.fetchone()[0]
                if not exists:
                    missing_tables.append(table)
            
            if missing_tables:
                logger.error(f"❌ Missing Phase 2 dependencies: {', '.join(missing_tables)}")
                logger.error("Please run Phase 2 migration first!")
                return False
            else:
                logger.info("✅ All Phase 2 dependencies found")
                return True
                
    except Exception as e:
        logger.error(f"Error checking Phase 2 dependencies: {e}")
        return False

def main():
    """Main function"""
    try:
        logger.info("Starting Phase 3 Advanced Migration Process...")
        
        # Check database connection
        if not check_database_connection():
            logger.error("❌ Migration failed - Database connection failed!")
            return False
        
        # Check Phase 2 dependencies
        if not check_phase2_dependencies():
            logger.error("❌ Migration failed - Phase 2 dependencies missing!")
            return False
        
        # Run migration
        if run_phase3_migration():
            logger.info("🎉 Phase 3 Advanced migration completed successfully!")
            logger.info("")
            logger.info("Next steps:")
            logger.info("1. Update main.py to include the Phase 3 advanced router")
            logger.info("2. Test the Phase 3 advanced endpoints")
            logger.info("3. Create frontend interfaces for developer panel")
            logger.info("4. Set up Dubai data integration")
            logger.info("5. Configure system monitoring and alerts")
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
