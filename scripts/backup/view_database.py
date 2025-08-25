#!/usr/bin/env python3
"""
Database Viewer Script
Shows contents of PostgreSQL and ChromaDB databases
"""

import os
import sys
from dotenv import load_dotenv
import psycopg2
import chromadb
from sqlalchemy import create_engine, text
import pandas as pd

# Load environment variables
load_dotenv()

def view_postgresql_database():
    """View PostgreSQL database contents"""
    print("=" * 60)
    print("📊 POSTGRESQL DATABASE CONTENTS")
    print("=" * 60)
    
    try:
        # Connect to PostgreSQL
        DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/real_estate_db")
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            # Get list of tables
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            tables = [row[0] for row in result]
            
            print(f"📋 Found {len(tables)} tables: {', '.join(tables)}")
            print()
            
            # Show contents of each table
            for table in tables:
                print(f"📄 Table: {table}")
                print("-" * 40)
                
                # Get row count
                count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = count_result.fetchone()[0]
                print(f"Total rows: {count}")
                
                if count > 0:
                    # Get sample data
                    sample_result = conn.execute(text(f"SELECT * FROM {table} LIMIT 5"))
                    rows = sample_result.fetchall()
                    columns = sample_result.keys()
                    
                    # Create DataFrame for better display
                    df = pd.DataFrame(rows, columns=columns)
                    print(df.to_string(index=False))
                else:
                    print("(No data)")
                
                print()
                
    except Exception as e:
        print(f"❌ Error connecting to PostgreSQL: {e}")
        print("Make sure PostgreSQL is running and the connection string is correct.")

def view_chromadb_database():
    """View ChromaDB database contents"""
    print("=" * 60)
    print("🧠 CHROMADB VECTOR DATABASE CONTENTS")
    print("=" * 60)
    
    try:
        # Connect to ChromaDB
        chroma_host = os.getenv("CHROMA_HOST", "localhost")
        chroma_port = int(os.getenv("CHROMA_PORT", "8000"))
        
        client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
        
        # Get all collections
        collections = client.list_collections()
        print(f"📋 Found {len(collections)} collections:")
        
        for collection in collections:
            print(f"\n📄 Collection: {collection.name}")
            print("-" * 40)
            
            try:
                # Get collection info
                coll = client.get_collection(collection.name)
                count = coll.count()
                print(f"Total documents: {count}")
                
                if count > 0:
                    # Get sample data
                    results = coll.peek(limit=3)
                    
                    print("\nSample documents:")
                    for i in range(min(3, len(results['documents']))):
                        print(f"\nDocument {i+1}:")
                        print(f"  ID: {results['ids'][i]}")
                        print(f"  Content: {results['documents'][i][:200]}...")
                        if results['metadatas'] and results['metadatas'][i]:
                            print(f"  Metadata: {results['metadatas'][i]}")
                
            except Exception as e:
                print(f"  Error accessing collection: {e}")
                
    except Exception as e:
        print(f"❌ Error connecting to ChromaDB: {e}")
        print("Make sure ChromaDB is running and the connection details are correct.")

def view_uploaded_files():
    """View uploaded files in the uploads directory"""
    print("=" * 60)
    print("📁 UPLOADED FILES")
    print("=" * 60)
    
    uploads_dir = "backend/uploads"
    
    if os.path.exists(uploads_dir):
        files = os.listdir(uploads_dir)
        print(f"📋 Found {len(files)} uploaded files:")
        
        for file in files:
            file_path = os.path.join(uploads_dir, file)
            size = os.path.getsize(file_path)
            print(f"  📄 {file} ({size} bytes)")
    else:
        print("❌ Uploads directory not found")
        print("Directory should be: backend/uploads")

def main():
    """Main function to view all databases"""
    print("🔍 DATABASE VIEWER")
    print("=" * 60)
    print("This script shows the contents of your databases")
    print()
    
    # View PostgreSQL database
    view_postgresql_database()
    
    print()
    
    # View ChromaDB database
    view_chromadb_database()
    
    print()
    
    # View uploaded files
    view_uploaded_files()
    
    print()
    print("=" * 60)
    print("✅ Database viewing complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
