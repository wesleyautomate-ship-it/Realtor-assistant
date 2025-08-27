#!/usr/bin/env python3
"""
Simple script to create default users for the Dubai Real Estate RAG System
"""

import bcrypt
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def create_default_users():
    """Create default admin and agent users"""
    
    # Database connection parameters
    db_params = {
        'host': 'postgres',  # Use service name when running in Docker
        'port': 5432,
        'database': 'real_estate_db',
        'user': 'admin',
        'password': 'password123'
    }
    
    try:
        # Connect to database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        # Create users table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                role VARCHAR(50) DEFAULT 'agent',
                is_active BOOLEAN DEFAULT TRUE,
                email_verified BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Default users data
        default_users = [
            # Admin users
            {
                "email": "admin1@dubai-estate.com",
                "password_hash": hash_password("Admin123!"),
                "first_name": "Ahmed",
                "last_name": "Al Mansouri",
                "role": "admin",
                "is_active": True,
                "email_verified": True
            },
            {
                "email": "admin2@dubai-estate.com",
                "password_hash": hash_password("Admin123!"),
                "first_name": "Fatima",
                "last_name": "Al Zahra",
                "role": "admin",
                "is_active": True,
                "email_verified": True
            },
            # Agent users
            {
                "email": "agent1@dubai-estate.com",
                "password_hash": hash_password("Agent123!"),
                "first_name": "Mohammed",
                "last_name": "Al Rashid",
                "role": "agent",
                "is_active": True,
                "email_verified": True
            },
            {
                "email": "agent2@dubai-estate.com",
                "password_hash": hash_password("Agent123!"),
                "first_name": "Aisha",
                "last_name": "Al Qasimi",
                "role": "agent",
                "is_active": True,
                "email_verified": True
            }
        ]
        
        # Insert default users
        for user in default_users:
            # Check if user already exists
            cursor.execute("SELECT id FROM users WHERE email = %s", (user["email"],))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO users (email, password_hash, first_name, last_name, role, is_active, email_verified)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    user["email"],
                    user["password_hash"],
                    user["first_name"],
                    user["last_name"],
                    user["role"],
                    user["is_active"],
                    user["email_verified"]
                ))
                logger.info(f"✅ Created user: {user['email']} ({user['role']})")
            else:
                logger.info(f"ℹ️ User already exists: {user['email']}")
        
        conn.commit()
        logger.info("✅ Default users created successfully")
        
        # Display user summary
        print("\n" + "="*60)
        print("👥 DEFAULT USERS CREATED!")
        print("="*60)
        print("📧 Email Addresses:")
        print("   - admin1@dubai-estate.com (Admin)")
        print("   - admin2@dubai-estate.com (Admin)")
        print("   - agent1@dubai-estate.com (Agent)")
        print("   - agent2@dubai-estate.com (Agent)")
        print("\n🔑 Default Passwords:")
        print("   - Admins: Admin123!")
        print("   - Agents: Agent123!")
        print("\n💡 Professional access only - login required!")
        print("="*60)
        
    except Exception as e:
        logger.error(f"❌ Error creating default users: {e}")
        raise
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_default_users()
