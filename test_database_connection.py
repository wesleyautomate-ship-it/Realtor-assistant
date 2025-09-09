#!/usr/bin/env python3
"""
Test Database Connection
=======================

Simple script to test database connection to the Docker PostgreSQL container.
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def test_connection():
    """Test connection to the database"""
    try:
        # Database connection parameters
        host = "localhost"
        port = "5432"
        user = "admin"
        password = "password123"
        database_name = "real_estate_db"
        
        print("=" * 50)
        print("TESTING DATABASE CONNECTION")
        print("=" * 50)
        print(f"Host: {host}")
        print(f"Port: {port}")
        print(f"User: {user}")
        print(f"Database: {database_name}")
        print("")
        
        # Connect to database
        print("Connecting to database...")
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database_name
        )
        
        cursor = conn.cursor()
        
        # Test query
        print("Testing query...")
        cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
        table_count = cursor.fetchone()[0]
        
        print(f"✅ Connection successful!")
        print(f"✅ Found {table_count} tables in the database")
        
        # List some tables
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name LIMIT 10;")
        tables = cursor.fetchall()
        
        print("\nFirst 10 tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Database connection test completed successfully!")
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
    success = test_connection()
    exit(0 if success else 1)
