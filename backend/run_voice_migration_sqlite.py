#!/usr/bin/env python3
"""
Run Voice AI Schema Migration (SQLite Version)
Executes the voice AI schema migration using SQLite for testing
"""

import os
import sys
from sqlalchemy import create_engine, text
from datetime import datetime

def run_voice_migration_sqlite():
    """Run the voice AI schema migration using SQLite"""
    
    # Use SQLite for testing
    database_url = 'sqlite:///voice_ai_test.db'
    
    print(f"🔗 Connecting to SQLite database: voice_ai_test.db")
    
    try:
        engine = create_engine(database_url)
        
        print("🚀 Running Voice AI schema migration (SQLite)...")
        
        with engine.connect() as conn:
            # Create voice_sessions table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS voice_sessions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    session_id TEXT NOT NULL UNIQUE,
                    transcript TEXT,
                    intent TEXT,
                    entities TEXT DEFAULT '{}',
                    processing_type TEXT DEFAULT 'realtime',
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ended_at TIMESTAMP,
                    metadata TEXT DEFAULT '{}'
                )
            """))
            
            # Create voice_requests table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS voice_requests (
                    id TEXT PRIMARY KEY,
                    session_id TEXT,
                    user_id TEXT NOT NULL,
                    audio_file_path TEXT,
                    transcript TEXT,
                    intent TEXT,
                    entities TEXT DEFAULT '{}',
                    processing_type TEXT NOT NULL,
                    status TEXT DEFAULT 'queued',
                    response_data TEXT,
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    processed_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES voice_sessions(id)
                )
            """))
            
            # Create content_templates table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS content_templates (
                    id TEXT PRIMARY KEY,
                    template_type TEXT NOT NULL,
                    template_name TEXT NOT NULL,
                    template_description TEXT,
                    template_prompt TEXT NOT NULL,
                    template_config TEXT DEFAULT '{}',
                    is_active INTEGER DEFAULT 1,
                    created_by TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Create generated_content table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS generated_content (
                    id TEXT PRIMARY KEY,
                    voice_request_id TEXT,
                    template_id TEXT,
                    user_id TEXT NOT NULL,
                    template_type TEXT NOT NULL,
                    content_data TEXT NOT NULL,
                    property_data TEXT DEFAULT '{}',
                    user_preferences TEXT DEFAULT '{}',
                    approval_status TEXT DEFAULT 'pending',
                    approved_by TEXT,
                    approved_at TIMESTAMP,
                    published_at TIMESTAMP,
                    published_to TEXT DEFAULT '[]',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (voice_request_id) REFERENCES voice_requests(id),
                    FOREIGN KEY (template_id) REFERENCES content_templates(id)
                )
            """))
            
            # Create content_versions table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS content_versions (
                    id TEXT PRIMARY KEY,
                    content_id TEXT,
                    version_number INTEGER NOT NULL,
                    content_data TEXT NOT NULL,
                    change_description TEXT,
                    created_by TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (content_id) REFERENCES generated_content(id)
                )
            """))
            
            # Create content_publishing_log table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS content_publishing_log (
                    id TEXT PRIMARY KEY,
                    content_id TEXT,
                    channel TEXT NOT NULL,
                    channel_details TEXT DEFAULT '{}',
                    status TEXT DEFAULT 'pending',
                    published_at TIMESTAMP,
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (content_id) REFERENCES generated_content(id)
                )
            """))
            
            # Create user_preferences table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL UNIQUE,
                    specialty TEXT NOT NULL,
                    workflow TEXT NOT NULL,
                    preferred_templates TEXT DEFAULT '[]',
                    notification_settings TEXT DEFAULT '{}',
                    voice_settings TEXT DEFAULT '{}',
                    content_preferences TEXT DEFAULT '{}',
                    onboarding_completed INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Create ai_requests table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS ai_requests (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    request_type TEXT NOT NULL,
                    input_data TEXT NOT NULL,
                    status TEXT DEFAULT 'queued',
                    result_data TEXT,
                    processing_type TEXT DEFAULT 'batch',
                    voice_request_id TEXT,
                    content_id TEXT,
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    processing_time_ms INTEGER,
                    FOREIGN KEY (voice_request_id) REFERENCES voice_requests(id),
                    FOREIGN KEY (content_id) REFERENCES generated_content(id)
                )
            """))
            
            # Create migration_log table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS migration_log (
                    id TEXT PRIMARY KEY,
                    migration_name TEXT UNIQUE NOT NULL,
                    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'completed'
                )
            """))
            
            # Insert default content templates
            templates = [
                ('cma', 'Comparative Market Analysis', 'Generate comprehensive CMA reports with pricing strategies'),
                ('just_listed', 'Just Listed Marketing', 'Create compelling just listed marketing content'),
                ('just_sold', 'Just Sold Celebration', 'Generate just sold celebration content'),
                ('open_house', 'Open House Invitation', 'Create open house invitations and promotional materials'),
                ('newsletter', 'Market Newsletter', 'Generate market newsletters and client communications'),
                ('investor_deck', 'Investment Presentation', 'Create investment presentations and property analysis'),
                ('brochure', 'Property Brochure', 'Generate property brochures and marketing materials'),
                ('social_banner', 'Social Media Banner', 'Create social media banners and graphics'),
                ('story_content', 'Social Media Stories', 'Generate social media story content')
            ]
            
            for template_type, name, description in templates:
                conn.execute(text("""
                    INSERT OR IGNORE INTO content_templates (id, template_type, template_name, template_description, template_prompt)
                    VALUES (:id, :template_type, :template_name, :template_description, :prompt)
                """), {
                    'id': f'template_{template_type}',
                    'template_type': template_type,
                    'template_name': name,
                    'template_description': description,
                    'prompt': f'Generate {template_type} content for the given property'
                })
            
            # Log migration completion
            conn.execute(text("""
                INSERT OR REPLACE INTO migration_log (id, migration_name, executed_at, status)
                VALUES (:id, :name, :executed_at, :status)
            """), {
                'id': 'voice_ai_migration',
                'name': 'voice_ai_schema_migration',
                'executed_at': datetime.now().isoformat(),
                'status': 'completed'
            })
            
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
        print("   - ai_requests")
        print("   - migration_log")
        print(f"📁 Database file: voice_ai_test.db")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    print("🎤 Voice AI Schema Migration (SQLite)")
    print("=" * 50)
    
    success = run_voice_migration_sqlite()
    
    if success:
        print("\n🎉 Migration completed successfully!")
        print("You can now test the voice command functionality with SQLite.")
        print("Note: This is a test database. For production, use PostgreSQL.")
    else:
        print("\n💥 Migration failed!")
        sys.exit(1)
