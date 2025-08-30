#!/usr/bin/env python3
"""
Database setup script for Dubai Real Estate RAG System
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sqlalchemy import create_engine, text
from config.settings import DATABASE_URL

def setup_database():
    """Setup database tables and initial data"""
    
    print("🗄️  Setting up database...")
    
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful")
        
        # Create tables
        create_tables(engine)
        
        # Insert initial data
        insert_initial_data(engine)
        
        print("✅ Database setup completed successfully")
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False
    
    return True

def create_tables(engine):
    """Create database tables"""
    
    print("📋 Creating tables...")
    
    # Properties table
    properties_table = """
    CREATE TABLE IF NOT EXISTS properties (
        id SERIAL PRIMARY KEY,
        address VARCHAR(255) NOT NULL,
        price DECIMAL(12,2),
        bedrooms INTEGER,
        bathrooms DECIMAL(3,1),
        square_feet INTEGER,
        property_type VARCHAR(100),
        description TEXT,
        location VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # Clients table
    clients_table = """
    CREATE TABLE IF NOT EXISTS clients (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255),
        phone VARCHAR(50),
        budget_min DECIMAL(12,2),
        budget_max DECIMAL(12,2),
        preferred_location VARCHAR(255),
        requirements TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # Conversations table
    conversations_table = """
    CREATE TABLE IF NOT EXISTS conversations (
        id SERIAL PRIMARY KEY,
        session_id VARCHAR(255) UNIQUE NOT NULL,
        role VARCHAR(50) DEFAULT 'client',
        title VARCHAR(255),
        user_id INTEGER,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # Messages table
    messages_table = """
    CREATE TABLE IF NOT EXISTS messages (
        id SERIAL PRIMARY KEY,
        conversation_id INTEGER REFERENCES conversations(id),
        role VARCHAR(50) NOT NULL,
        content TEXT NOT NULL,
        message_type VARCHAR(50) DEFAULT 'text',
        metadata JSONB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    tables = [
        ("properties", properties_table),
        ("clients", clients_table),
        ("conversations", conversations_table),
        ("messages", messages_table)
    ]
    
    with engine.connect() as conn:
        for table_name, table_sql in tables:
            try:
                conn.execute(text(table_sql))
                conn.commit()
                print(f"✅ Created table: {table_name}")
            except Exception as e:
                print(f"⚠️  Table {table_name} may already exist: {e}")

def insert_initial_data(engine):
    """Insert initial sample data"""
    
    print("📊 Inserting initial data...")
    
    # Sample properties
    sample_properties = [
        {
            'address': 'Dubai Marina Tower 1, Unit 1501',
            'price': 2500000,
            'bedrooms': 2,
            'bathrooms': 2.5,
            'square_feet': 1200,
            'property_type': 'Apartment',
            'description': 'Luxury apartment with marina view',
            'location': 'Dubai Marina'
        },
        {
            'address': 'Downtown Dubai, Burj Vista 2, Unit 2503',
            'price': 4500000,
            'bedrooms': 3,
            'bathrooms': 3.5,
            'square_feet': 1800,
            'property_type': 'Apartment',
            'description': 'Premium apartment with Burj Khalifa view',
            'location': 'Downtown Dubai'
        },
        {
            'address': 'Palm Jumeirah, Shoreline Apartments, Unit 801',
            'price': 3200000,
            'bedrooms': 2,
            'bathrooms': 2.0,
            'square_feet': 1400,
            'property_type': 'Apartment',
            'description': 'Beachfront apartment with sea view',
            'location': 'Palm Jumeirah'
        }
    ]
    
    with engine.connect() as conn:
        # Insert sample properties
        for prop in sample_properties:
            try:
                conn.execute(text("""
                    INSERT INTO properties (address, price, bedrooms, bathrooms, square_feet, property_type, description, location)
                    VALUES (:address, :price, :bedrooms, :bathrooms, :square_feet, :property_type, :description, :location)
                    ON CONFLICT DO NOTHING
                """), prop)
                conn.commit()
            except Exception as e:
                print(f"⚠️  Could not insert property {prop['address']}: {e}")
        
        print(f"✅ Inserted {len(sample_properties)} sample properties")

if __name__ == "__main__":
    success = setup_database()
    if success:
        print("\n🎉 Database setup completed successfully!")
    else:
        print("\n❌ Database setup failed!")
        sys.exit(1)
