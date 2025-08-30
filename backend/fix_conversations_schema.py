#!/usr/bin/env python3
"""
Fix Conversations Table Schema

This script adds the missing user_id column to the conversations table
to fix the new chat registration issue.
"""

import os
import sys
from sqlalchemy import create_engine, text
from config.settings import DATABASE_URL

def fix_conversations_schema():
    """Add missing user_id column to conversations table"""
    try:
        # Create database connection
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            # Check if user_id column exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'conversations' 
                AND column_name = 'user_id'
            """))
            
            if not result.fetchone():
                print("🔧 Adding missing user_id column to conversations table...")
                
                # Add user_id column
                conn.execute(text("""
                    ALTER TABLE conversations 
                    ADD COLUMN user_id INTEGER REFERENCES users(id)
                """))
                
                # Update existing conversations to assign them to a default user (admin)
                # First, get the first admin user
                admin_result = conn.execute(text("""
                    SELECT id FROM users WHERE role = 'admin' LIMIT 1
                """))
                admin_user = admin_result.fetchone()
                
                if admin_user:
                    conn.execute(text("""
                        UPDATE conversations 
                        SET user_id = :admin_id 
                        WHERE user_id IS NULL
                    """), {"admin_id": admin_user[0]})
                    print(f"✅ Updated existing conversations to user ID: {admin_user[0]}")
                else:
                    print("⚠️ No admin user found. Please create an admin user first.")
                
                conn.commit()
                print("✅ user_id column added successfully")
            else:
                print("✅ user_id column already exists")
            
            # Verify the schema
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'conversations'
                ORDER BY ordinal_position
            """))
            
            print("\n📋 Current conversations table schema:")
            for row in result:
                print(f"  - {row[0]}: {row[1]} ({'NULL' if row[2] == 'YES' else 'NOT NULL'})")
                
    except Exception as e:
        print(f"❌ Error fixing conversations schema: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🔧 Fixing Conversations Table Schema...")
    fix_conversations_schema()
    print("✅ Schema fix completed!")
