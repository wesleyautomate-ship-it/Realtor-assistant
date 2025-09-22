#!/usr/bin/env python3
"""
Run Voice AI Schema Migration
Executes the voice_ai_schema_migration.sql file
"""

import os
import sys
from sqlalchemy import create_engine, text
from datetime import datetime

def run_voice_migration():
    """Run the voice AI schema migration"""
    
    # Database connection
    database_url = os.getenv('DATABASE_URL', 'postgresql://admin:password123@localhost:5432/real_estate_db')
    
    print(f"🔗 Connecting to database: {database_url.split('@')[1] if '@' in database_url else 'localhost'}")
    
    try:
        engine = create_engine(database_url)
        
        # Read the migration file
        migration_file = os.path.join(os.path.dirname(__file__), 'migrations', 'voice_ai_schema_migration.sql')
        
        if not os.path.exists(migration_file):
            print(f"❌ Migration file not found: {migration_file}")
            return False
            
        print(f"📄 Reading migration file: {migration_file}")
        
        with open(migration_file, 'r', encoding='utf-8') as f:
            migration_sql = f.read()
        
        print("🚀 Running Voice AI schema migration...")
        
        with engine.connect() as conn:
            # Execute the migration
            conn.execute(text(migration_sql))
            conn.commit()
            
        print("✅ Voice AI schema migration completed successfully!")
        print("📋 Created tables:")
        print("   - voice_sessions")
        print("   - voice_requests") 
        print("   - content_templates")
        print("   - generated_content")
        print("   - content_versions")
        print("   - content_publishing_log")
        print("   - user_preferences")
        print("   - ai_requests (enhanced)")
        print("   - migration_log")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    print("🎤 Voice AI Schema Migration")
    print("=" * 50)
    
    success = run_voice_migration()
    
    if success:
        print("\n🎉 Migration completed successfully!")
        print("You can now use the voice command functionality.")
    else:
        print("\n💥 Migration failed!")
        sys.exit(1)
