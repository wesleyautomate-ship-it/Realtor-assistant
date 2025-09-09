#!/usr/bin/env python3
"""
Database Setup Script
====================

This script creates the database and runs all migrations in the correct order.
"""

import sys
import os
import logging
import psycopg2
from pathlib import Path
from sqlalchemy import create_engine, text

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from config.settings import DATABASE_URL

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Parse the database URL to get connection details
        # Format: postgresql://user:password@host:port/database
        url_parts = DATABASE_URL.replace('postgresql://', '').split('/')
        connection_part = url_parts[0]
        database_name = url_parts[1]
        
        # Split connection part
        auth_host = connection_part.split('@')
        auth = auth_host[0].split(':')
        host_port = auth_host[1].split(':')
        
        user = auth[0]
        password = auth[1]
        host = host_port[0]
        port = host_port[1] if len(host_port) > 1 else '5432'
        
        logger.info(f"Creating database: {database_name}")
        logger.info(f"Host: {host}, Port: {port}, User: {user}")
        
        # Connect to PostgreSQL server (not to specific database)
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database='postgres'  # Connect to default postgres database
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{database_name}'")
        exists = cursor.fetchone()
        
        if exists:
            logger.info(f"✅ Database '{database_name}' already exists")
        else:
            # Create database
            cursor.execute(f"CREATE DATABASE {database_name}")
            logger.info(f"✅ Database '{database_name}' created successfully")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating database: {e}")
        return False

def test_database_connection():
    """Test connection to the database"""
    try:
        logger.info("Testing database connection...")
        
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            if result.fetchone()[0] == 1:
                logger.info("✅ Database connection successful")
                return True
            else:
                logger.error("❌ Database connection failed")
                return False
                
    except Exception as e:
        logger.error(f"❌ Database connection error: {e}")
        return False

def run_migrations():
    """Run all migrations in order"""
    try:
        logger.info("Running database migrations...")
        
        # List of migration files in order
        migration_files = [
            "brokerage_schema_migration.sql",
            "ai_assistant_schema_migration.sql", 
            "phase3_advanced_schema_migration.sql"
        ]
        
        engine = create_engine(DATABASE_URL)
        
        for migration_file in migration_files:
            migration_path = backend_dir / "migrations" / migration_file
            
            if not migration_path.exists():
                logger.warning(f"⚠️ Migration file not found: {migration_file}")
                continue
            
            logger.info(f"Running migration: {migration_file}")
            
            with open(migration_path, 'r', encoding='utf-8') as f:
                migration_sql = f.read()
            
            with engine.connect() as conn:
                conn.execute(text(migration_sql))
                conn.commit()
            
            logger.info(f"✅ Migration {migration_file} completed")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error running migrations: {e}")
        return False

def main():
    """Main function"""
    try:
        logger.info("=" * 60)
        logger.info("DATABASE SETUP SCRIPT")
        logger.info("=" * 60)
        
        # Step 1: Create database
        if not create_database():
            logger.error("❌ Database creation failed!")
            return False
        
        # Step 2: Test connection
        if not test_database_connection():
            logger.error("❌ Database connection test failed!")
            return False
        
        # Step 3: Run migrations
        if not run_migrations():
            logger.error("❌ Migration failed!")
            return False
        
        logger.info("🎉 Database setup completed successfully!")
        logger.info("")
        logger.info("Next steps:")
        logger.info("1. Start the backend server: python backend/main.py")
        logger.info("2. Test the API endpoints")
        logger.info("3. Start the frontend: cd frontend && npm start")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Database setup failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
