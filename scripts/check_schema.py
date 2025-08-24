#!/usr/bin/env python3
"""Check database schema column names"""

import os
from sqlalchemy import create_engine, text

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/real_estate_db")
engine = create_engine(DATABASE_URL)

def check_table_schema(table_name):
    """Check column names for a specific table"""
    print(f"\n{table_name} columns:")
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{table_name}' 
                ORDER BY ordinal_position
            """))
            for row in result:
                print(f"  {row[0]} ({row[1]})")
    except Exception as e:
        print(f"  Error: {e}")

# Check all relevant tables
tables = [
    'market_data',
    'neighborhood_profiles', 
    'developers',
    'investment_insights',
    'regulatory_updates'
]

print("Database Schema Check")
print("=" * 50)

for table in tables:
    check_table_schema(table)
