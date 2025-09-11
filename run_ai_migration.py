#!/usr/bin/env python3
"""
AI Request System Migration Runner
==================================

This script runs the database migration for the new AI request system.
It creates all necessary tables, indexes, and initial data.
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pathlib import Path

def get_database_url():
    """Get database URL from environment or use default"""
    return os.getenv('DATABASE_URL', 'postgresql://admin:password123@localhost:5432/real_estate_db')

def run_migration():
    """Run the AI request system migration"""
    try:
        # Read the migration file
        migration_file = Path(__file__).parent / 'backend' / 'migrations' / 'ai_request_system_migration.sql'
        
        if not migration_file.exists():
            print(f"❌ Migration file not found: {migration_file}")
            return False
        
        with open(migration_file, 'r') as f:
            migration_sql = f.read()
        
        # Connect to database
        print("🔌 Connecting to database...")
        conn = psycopg2.connect(get_database_url())
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Execute migration
        print("🚀 Running AI request system migration...")
        cursor.execute(migration_sql)
        
        print("✅ Migration completed successfully!")
        
        # Verify tables were created
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('ai_requests_new', 'ai_request_steps', 'deliverables', 'templates', 'ai_brand_assets', 'ai_request_events')
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        print(f"📊 Created tables: {[table[0] for table in tables]}")
        
        # Check template count
        cursor.execute("SELECT COUNT(*) FROM templates;")
        template_count = cursor.fetchone()[0]
        print(f"📋 Loaded {template_count} templates")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def main():
    """Main function"""
    print("🎯 AI Request System Migration")
    print("=" * 40)
    
    if run_migration():
        print("\n🎉 Migration completed successfully!")
        print("You can now start the application with the new AI request system.")
    else:
        print("\n💥 Migration failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
