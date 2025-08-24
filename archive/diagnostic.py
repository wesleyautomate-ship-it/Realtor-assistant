#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv
import chromadb
from sqlalchemy import create_engine, text
import google.generativeai as genai

def test_environment():
    print("🔍 Testing Environment Variables...")
    load_dotenv()
    
    # Check required environment variables
    required_vars = ['GOOGLE_API_KEY', 'DATABASE_URL', 'CHROMA_HOST', 'CHROMA_PORT']
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {'*' * len(value)} (length: {len(value)})")
        else:
            print(f"❌ {var}: Not set")
    
    print()

def test_database():
    print("🗄️ Testing Database Connection...")
    try:
        database_url = os.getenv('DATABASE_URL', 'postgresql://admin:password123@localhost:5432/real_estate_db')
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM properties"))
            count = result.fetchone()[0]
            print(f"✅ Database connected successfully. Properties count: {count}")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
    
    print()

def test_chromadb():
    print("🔍 Testing ChromaDB Connection...")
    try:
        chroma_host = os.getenv('CHROMA_HOST', 'localhost')
        chroma_port = int(os.getenv('CHROMA_PORT', '8000'))
        
        chroma_client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
        
        # Test getting collections
        collections = chroma_client.list_collections()
        print(f"✅ ChromaDB connected successfully. Collections: {len(collections)}")
        
        for collection in collections:
            print(f"   - {collection.name}")
            
    except Exception as e:
        print(f"❌ ChromaDB connection failed: {e}")
    
    print()

def test_google_api():
    print("🤖 Testing Google API...")
    try:
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("❌ GOOGLE_API_KEY not set")
            return
            
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content("Hello, test message")
        print(f"✅ Google API working. Response length: {len(response.text)}")
        
    except Exception as e:
        print(f"❌ Google API failed: {e}")
    
    print()

def main():
    print("🚀 Backend Diagnostic Tool")
    print("=" * 50)
    
    test_environment()
    test_database()
    test_chromadb()
    test_google_api()
    
    print("🏁 Diagnostic complete!")

if __name__ == "__main__":
    main()
