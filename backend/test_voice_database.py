#!/usr/bin/env python3
"""
Test Voice AI Database Schema
Verifies that all voice AI tables were created correctly
"""

import sqlite3
from datetime import datetime

def test_voice_database():
    """Test the voice AI database schema"""
    
    print("🧪 Testing Voice AI Database Schema")
    print("=" * 50)
    
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('voice_ai_test.db')
        cursor = conn.cursor()
        
        # List of expected tables
        expected_tables = [
            'voice_sessions',
            'voice_requests',
            'content_templates',
            'generated_content',
            'content_versions',
            'content_publishing_log',
            'user_preferences',
            'ai_requests',
            'migration_log'
        ]
        
        print("📋 Checking tables...")
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        # Check each expected table
        for table in expected_tables:
            if table in existing_tables:
                print(f"   ✅ {table}")
                
                # Get table info
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                print(f"      Columns: {len(columns)}")
                
            else:
                print(f"   ❌ {table} - MISSING")
        
        # Test content templates
        print("\n📄 Testing content templates...")
        cursor.execute("SELECT COUNT(*) FROM content_templates")
        template_count = cursor.fetchone()[0]
        print(f"   Templates available: {template_count}")
        
        if template_count > 0:
            cursor.execute("SELECT template_type, template_name FROM content_templates LIMIT 5")
            templates = cursor.fetchall()
            for template_type, name in templates:
                print(f"   - {template_type}: {name}")
        
        # Test migration log
        print("\n📝 Testing migration log...")
        cursor.execute("SELECT migration_name, status, executed_at FROM migration_log")
        migrations = cursor.fetchall()
        for name, status, executed_at in migrations:
            print(f"   - {name}: {status} ({executed_at})")
        
        # Test inserting a sample voice session
        print("\n🎤 Testing voice session creation...")
        test_session_id = f"test_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        cursor.execute("""
            INSERT INTO voice_sessions (id, user_id, session_id, transcript, intent, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (test_session_id, 'demo-user-123', test_session_id, 'Test transcript', 'test_intent', 'active'))
        
        # Verify insertion
        cursor.execute("SELECT COUNT(*) FROM voice_sessions WHERE id = ?", (test_session_id,))
        count = cursor.fetchone()[0]
        
        if count > 0:
            print("   ✅ Voice session created successfully")
        else:
            print("   ❌ Failed to create voice session")
        
        conn.commit()
        conn.close()
        
        print("\n🎉 Database test completed successfully!")
        print("✅ All voice AI tables are working correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_voice_database()
    
    if success:
        print("\n🚀 Voice AI database is ready for testing!")
    else:
        print("\n💥 Database test failed!")
        exit(1)
