#!/usr/bin/env python3
"""
Data Ingestion Script for Real Estate RAG System
This script processes CSV files and documents, storing them in PostgreSQL and ChromaDB
"""

import os
import sys
import json
import uuid
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import chromadb
from pathlib import Path
import PyPDF2
from docx import Document
import logging

# Add parent directory to path to import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataIngester:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/real_estate_db")
        self.engine = create_engine(self.db_url)
        self.chroma_client = chromadb.HttpClient(host="localhost", port=8000)
        
        # Initialize collections for the new RAG system
        self.collections = {
            "real_estate_docs": "Company policies and general documents",
            "neighborhoods": "Dubai neighborhood information",
            "market_updates": "Market trends and updates",
            "agent_resources": "Sales techniques and agent resources",
            "employees": "Employee information and contacts"
        }
        
    def create_tables(self):
        """Create database tables if they don't exist"""
        try:
            with self.engine.connect() as conn:
                # Create properties table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS properties (
                        id SERIAL PRIMARY KEY,
                        address VARCHAR(255) NOT NULL,
                        price DECIMAL(12,2),
                        bedrooms INTEGER,
                        bathrooms DECIMAL(3,1),
                        square_feet INTEGER,
                        property_type VARCHAR(100),
                        description TEXT
                    )
                """))
                
                # Create clients table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS clients (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        email VARCHAR(255),
                        phone VARCHAR(50),
                        budget_min DECIMAL(12,2),
                        budget_max DECIMAL(12,2),
                        preferred_location VARCHAR(255),
                        requirements TEXT
                    )
                """))
                
                # Create conversations table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS conversations (
                        id SERIAL PRIMARY KEY,
                        session_id VARCHAR(255) UNIQUE NOT NULL,
                        role VARCHAR(50) NOT NULL DEFAULT 'client',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        title VARCHAR(255),
                        is_active BOOLEAN DEFAULT TRUE
                    )
                """))
                
                # Create messages table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS messages (
                        id SERIAL PRIMARY KEY,
                        conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
                        role VARCHAR(50) NOT NULL,
                        content TEXT NOT NULL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        message_type VARCHAR(50) DEFAULT 'text',
                        metadata JSONB
                    )
                """))
                
                conn.commit()
                logger.info("Database tables created successfully")
                
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            raise

    def ingest_csv_data(self):
        """Ingest CSV files into PostgreSQL"""
        try:
            data_dir = Path("data")
            
            # Ingest properties
            if (data_dir / "listings.csv").exists():
                df = pd.read_csv(data_dir / "listings.csv")
                df.to_sql('properties', self.engine, if_exists='replace', index=False)
                logger.info(f"Ingested {len(df)} properties")
            
            # Ingest clients
            if (data_dir / "clients.csv").exists():
                df = pd.read_csv(data_dir / "clients.csv")
                df.to_sql('clients', self.engine, if_exists='replace', index=False)
                logger.info(f"Ingested {len(df)} clients")
                
        except Exception as e:
            logger.error(f"Error ingesting CSV data: {e}")
            raise

    def ingest_documents(self):
        """Ingest documents into ChromaDB collections"""
        try:
            # Create all collections
            for collection_name, description in self.collections.items():
                try:
                    collection = self.chroma_client.get_or_create_collection(collection_name)
                    logger.info(f"Created/accessed collection: {collection_name} - {description}")
                except Exception as e:
                    logger.error(f"Error creating collection {collection_name}: {e}")
                    continue
            
            # Ingest general documents
            self._ingest_general_documents()
            
            # Ingest neighborhood data
            self._ingest_neighborhood_data()
            
            # Ingest market updates
            self._ingest_market_updates()
            
            # Ingest agent resources
            self._ingest_agent_resources()
            
            # Ingest employee data
            self._ingest_employee_data()
                
        except Exception as e:
            logger.error(f"Error ingesting documents: {e}")
            raise

    def _ingest_general_documents(self):
        """Ingest general company documents"""
        try:
            collection = self.chroma_client.get_collection("real_estate_docs")
            
            # Process documents from data/documents directory
            documents_dir = Path("data/documents")
            if not documents_dir.exists():
                logger.warning(f"Documents directory not found: {documents_dir}")
                return
            
            documents = []
            metadatas = []
            ids = []
            
            for file_path in documents_dir.glob("*"):
                if file_path.is_file():
                    try:
                        content = self.read_document(file_path)
                        if content:
                            documents.append(content)
                            metadatas.append({
                                "source": str(file_path),
                                "type": file_path.suffix,
                                "filename": file_path.name,
                                "collection": "real_estate_docs"
                            })
                            ids.append(str(uuid.uuid4()))
                    except Exception as e:
                        logger.error(f"Error processing {file_path}: {e}")
            
            if documents:
                collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                logger.info(f"Successfully ingested {len(documents)} general documents")
            else:
                logger.warning("No general documents found to ingest")
                
        except Exception as e:
            logger.error(f"Error ingesting general documents: {e}")

    def _ingest_neighborhood_data(self):
        """Ingest neighborhood information"""
        try:
            collection = self.chroma_client.get_collection("neighborhoods")
            
            # Process neighborhood data from data/dubai-market/neighborhoods
            neighborhoods_dir = Path("data/dubai-market/neighborhoods")
            if not neighborhoods_dir.exists():
                logger.warning(f"Neighborhoods directory not found: {neighborhoods_dir}")
                return
            
            documents = []
            metadatas = []
            ids = []
            
            for file_path in neighborhoods_dir.glob("*.json"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Convert JSON to text format
                    content = f"Neighborhood: {data.get('name', 'Unknown')}\n"
                    content += f"Description: {data.get('description', '')}\n"
                    content += f"Amenities: {', '.join(data.get('amenities', []))}\n"
                    content += f"Average Price: {data.get('average_price', 'N/A')}\n"
                    content += f"Transport: {', '.join(data.get('transport', []))}\n"
                    
                    documents.append(content)
                    metadatas.append({
                        "source": str(file_path),
                        "type": "neighborhood",
                        "filename": file_path.name,
                        "collection": "neighborhoods",
                        "neighborhood_name": data.get('name', 'Unknown')
                    })
                    ids.append(str(uuid.uuid4()))
                    
                except Exception as e:
                    logger.error(f"Error processing neighborhood file {file_path}: {e}")
            
            if documents:
                collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                logger.info(f"Successfully ingested {len(documents)} neighborhood documents")
            else:
                logger.warning("No neighborhood documents found to ingest")
                
        except Exception as e:
            logger.error(f"Error ingesting neighborhood data: {e}")

    def _ingest_market_updates(self):
        """Ingest market updates"""
        try:
            collection = self.chroma_client.get_collection("market_updates")
            
            # Process market updates from data/dubai-market/market-updates
            market_dir = Path("data/dubai-market/market-updates")
            if not market_dir.exists():
                logger.warning(f"Market updates directory not found: {market_dir}")
                return
            
            documents = []
            metadatas = []
            ids = []
            
            for file_path in market_dir.glob("*.json"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Convert JSON to text format
                    content = f"Market Update: {data.get('title', 'Unknown')}\n"
                    content += f"Date: {data.get('date', '')}\n"
                    content += f"Summary: {data.get('summary', '')}\n"
                    content += f"Key Points: {', '.join(data.get('key_points', []))}\n"
                    content += f"Trends: {data.get('trends', '')}\n"
                    
                    documents.append(content)
                    metadatas.append({
                        "source": str(file_path),
                        "type": "market_update",
                        "filename": file_path.name,
                        "collection": "market_updates",
                        "date": data.get('date', ''),
                        "title": data.get('title', 'Unknown')
                    })
                    ids.append(str(uuid.uuid4()))
                    
                except Exception as e:
                    logger.error(f"Error processing market update file {file_path}: {e}")
            
            if documents:
                collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                logger.info(f"Successfully ingested {len(documents)} market update documents")
            else:
                logger.warning("No market update documents found to ingest")
                
        except Exception as e:
            logger.error(f"Error ingesting market updates: {e}")

    def _ingest_agent_resources(self):
        """Ingest agent resources"""
        try:
            collection = self.chroma_client.get_collection("agent_resources")
            
            # Process agent resources from data/agent-resources
            resources_dir = Path("data/agent-resources")
            if not resources_dir.exists():
                logger.warning(f"Agent resources directory not found: {resources_dir}")
                return
            
            documents = []
            metadatas = []
            ids = []
            
            for file_path in resources_dir.rglob("*.json"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Convert JSON to text format based on resource type
                    content = f"Resource: {data.get('title', 'Unknown')}\n"
                    content += f"Category: {data.get('category', '')}\n"
                    content += f"Description: {data.get('description', '')}\n"
                    
                    if 'techniques' in data:
                        content += f"Techniques: {', '.join(data.get('techniques', []))}\n"
                    if 'strategies' in data:
                        content += f"Strategies: {', '.join(data.get('strategies', []))}\n"
                    if 'tips' in data:
                        content += f"Tips: {', '.join(data.get('tips', []))}\n"
                    
                    documents.append(content)
                    metadatas.append({
                        "source": str(file_path),
                        "type": "agent_resource",
                        "filename": file_path.name,
                        "collection": "agent_resources",
                        "category": data.get('category', ''),
                        "title": data.get('title', 'Unknown')
                    })
                    ids.append(str(uuid.uuid4()))
                    
                except Exception as e:
                    logger.error(f"Error processing agent resource file {file_path}: {e}")
            
            if documents:
                collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                logger.info(f"Successfully ingested {len(documents)} agent resource documents")
            else:
                logger.warning("No agent resource documents found to ingest")
                
        except Exception as e:
            logger.error(f"Error ingesting agent resources: {e}")

    def _ingest_employee_data(self):
        """Ingest employee information"""
        try:
            collection = self.chroma_client.get_collection("employees")
            
            # Process employee data from data/company-data/employees
            employees_dir = Path("data/company-data/employees")
            if not employees_dir.exists():
                logger.warning(f"Employees directory not found: {employees_dir}")
                return
            
            documents = []
            metadatas = []
            ids = []
            
            for file_path in employees_dir.glob("*.json"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Convert JSON to text format
                    content = f"Employee: {data.get('name', 'Unknown')}\n"
                    content += f"Role: {data.get('role', '')}\n"
                    content += f"Department: {data.get('department', '')}\n"
                    content += f"Specialization: {data.get('specialization', '')}\n"
                    content += f"Experience: {data.get('experience', '')}\n"
                    content += f"Contact: {data.get('contact', '')}\n"
                    
                    documents.append(content)
                    metadatas.append({
                        "source": str(file_path),
                        "type": "employee",
                        "filename": file_path.name,
                        "collection": "employees",
                        "name": data.get('name', 'Unknown'),
                        "role": data.get('role', ''),
                        "department": data.get('department', '')
                    })
                    ids.append(str(uuid.uuid4()))
                    
                except Exception as e:
                    logger.error(f"Error processing employee file {file_path}: {e}")
            
            if documents:
                collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                logger.info(f"Successfully ingested {len(documents)} employee documents")
            else:
                logger.warning("No employee documents found to ingest")
                
        except Exception as e:
            logger.error(f"Error ingesting employee data: {e}")

    def read_document(self, file_path):
        """Read different document formats"""
        try:
            if file_path.suffix.lower() == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            elif file_path.suffix.lower() == '.pdf':
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    return ' '.join([page.extract_text() for page in reader.pages])
            elif file_path.suffix.lower() == '.docx':
                doc = Document(file_path)
                return ' '.join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return None

def create_tables():
    """Standalone function to create database tables"""
    ingester = DataIngester()
    ingester.create_tables()

def main():
    """Main ingestion function"""
    try:
        ingester = DataIngester()
        
        logger.info("Starting data ingestion...")
        
        # Create tables
        ingester.create_tables()
        
        # Ingest CSV data
        ingester.ingest_csv_data()
        
        # Ingest documents
        ingester.ingest_documents()
        
        logger.info("Data ingestion completed successfully!")
        
    except Exception as e:
        logger.error(f"Data ingestion failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
