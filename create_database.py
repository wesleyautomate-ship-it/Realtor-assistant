#!/usr/bin/env python3
"""
Simple Database Creation Script
==============================

This script creates the PostgreSQL database for the real estate system.
Run this before running any migrations.
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    """Create the real_estate_db database"""
    try:
        # Database connection parameters
        host = "localhost"
        port = "5432"
        user = "admin"
        password = "password123"
        database_name = "real_estate_db"
        
        print("=" * 50)
        print("CREATING DATABASE")
        print("=" * 50)
        print(f"Host: {host}")
        print(f"Port: {port}")
        print(f"User: {user}")
        print(f"Database: {database_name}")
        print("")
        
        # Connect to PostgreSQL server (not to specific database)
        print("Connecting to PostgreSQL server...")
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database='postgres'  # Connect to default postgres database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        print("Checking if database exists...")
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{database_name}'")
        exists = cursor.fetchone()
        
        if exists:
            print(f"✅ Database '{database_name}' already exists")
        else:
            # Create database
            print(f"Creating database '{database_name}'...")
            cursor.execute(f"CREATE DATABASE {database_name}")
            print(f"✅ Database '{database_name}' created successfully")
        
        cursor.close()
        conn.close()
        
        print("")
        print("🎉 Database setup completed!")
        print("")
        print("Next steps:")
        print("1. Run: python backend/scripts/setup_database.py")
        print("2. Or run individual migrations:")
        print("   - python backend/scripts/run_brokerage_migration.py")
        print("   - python backend/scripts/run_ai_assistant_migration.py") 
        print("   - python backend/scripts/run_phase3_migration.py")
        
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Connection error: {e}")
        print("")
        print("Make sure PostgreSQL is running and accessible.")
        print("If using Docker, run: docker-compose up postgres")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = create_database()
    exit(0 if success else 1)
