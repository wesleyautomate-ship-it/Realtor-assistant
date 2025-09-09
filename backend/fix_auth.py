#!/usr/bin/env python3
"""
Fix authentication issue by creating a proper admin user
"""

import psycopg2
import bcrypt
import sys

def fix_auth():
    try:
        # Connect to database
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="real_estate_db",
            user="admin",
            password="password123"
        )
        cur = conn.cursor()
        
        # Generate proper password hash
        password = "admin123"
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        
        print(f"Generated password hash: {password_hash}")
        
        # Delete existing admin user
        cur.execute("DELETE FROM users WHERE email = 'admin@realestate.com'")
        
        # Insert new admin user
        cur.execute("""
            INSERT INTO users (email, password_hash, first_name, last_name, role, is_active, email_verified)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            'admin@realestate.com',
            password_hash,
            'System',
            'Administrator',
            'admin',
            True,
            True
        ))
        
        conn.commit()
        
        # Verify the user was created
        cur.execute("SELECT id, email, first_name, last_name, role, is_active FROM users WHERE email = 'admin@realestate.com'")
        user = cur.fetchone()
        
        if user:
            print(f"✅ Admin user created successfully: {user}")
        else:
            print("❌ Failed to create admin user")
            
        # Test password verification
        cur.execute("SELECT password_hash FROM users WHERE email = 'admin@realestate.com'")
        stored_hash = cur.fetchone()[0]
        
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            print("✅ Password verification successful")
        else:
            print("❌ Password verification failed")
            
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fix_auth()
