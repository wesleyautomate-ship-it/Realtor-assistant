#!/usr/bin/env python3
"""
PDF Data Ingestion Script for Dubai Real Estate RAG System
This script processes PDF files and ingests the data into PostgreSQL and ChromaDB
"""

import os
import sys
import json
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import chromadb
from pathlib import Path
import logging
from datetime import datetime
import uuid
import PyPDF2
import fitz  # PyMuPDF
import re
from typing import List, Dict, Any

# Add parent directory to path to import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PDFDataIngester:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL", "postgresql://postgres:password123@localhost:5432/real_estate_db")
        self.engine = create_engine(self.db_url)
        self.chroma_client = chromadb.HttpClient(host="localhost", port=8000)
        
        # Data directories
        self.data_root = Path("../data")
        self.documents_dir = self.data_root / "documents"
        self.pdf_dir = self.data_root / "pdfs"
        
        # Create directories if they don't exist
        self.pdf_dir.mkdir(exist_ok=True)
        
        # PDF processing results
        self.extracted_data = {
            "neighborhoods": [],
            "transactions": [],
            "legal_requirements": [],
            "market_reports": [],
            "property_data": []
        }
        
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text from PDF using PyMuPDF"""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {e}")
            return ""
    
    def extract_text_from_pdf_pypdf2(self, pdf_path: Path) -> str:
        """Extract text from PDF using PyPDF2 as backup"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path} with PyPDF2: {e}")
            return ""
    
    def process_neighborhood_pdf(self, text: str, filename: str) -> List[Dict]:
        """Process neighborhood data from PDF text"""
        neighborhoods = []
        
        # Extract neighborhood information using regex patterns
        patterns = {
            'name': r'(?:Neighborhood|Area|Location):\s*([^\n]+)',
            'description': r'(?:Description|Overview):\s*([^\n]+)',
            'price_range': r'(?:Price Range|Prices):\s*([^\n]+)',
            'amenities': r'(?:Amenities|Facilities):\s*([^\n]+)',
            'pros': r'(?:Pros|Advantages):\s*([^\n]+)',
            'cons': r'(?:Cons|Disadvantages):\s*([^\n]+)'
        }
        
        # Split text into sections and extract data
        sections = text.split('\n\n')
        for section in sections:
            if any(keyword in section.lower() for keyword in ['neighborhood', 'area', 'location', 'community']):
                neighborhood = {'source_file': filename}
                
                for field, pattern in patterns.items():
                    match = re.search(pattern, section, re.IGNORECASE)
                    if match:
                        neighborhood[field] = match.group(1).strip()
                
                if 'name' in neighborhood:
                    neighborhoods.append(neighborhood)
        
        return neighborhoods
    
    def process_transaction_pdf(self, text: str, filename: str) -> List[Dict]:
        """Process transaction data from PDF text"""
        transactions = []
        
        # Extract transaction information
        patterns = {
            'property_address': r'(?:Address|Location):\s*([^\n]+)',
            'transaction_date': r'(?:Date|Transaction Date):\s*([^\n]+)',
            'price': r'(?:Price|Sale Price|Amount):\s*([^\n]+)',
            'property_type': r'(?:Type|Property Type):\s*([^\n]+)',
            'bedrooms': r'(?:Bedrooms|Beds):\s*(\d+)',
            'bathrooms': r'(?:Bathrooms|Baths):\s*(\d+)',
            'area': r'(?:Area|Size|Square Feet):\s*([^\n]+)',
            'developer': r'(?:Developer|Builder):\s*([^\n]+)'
        }
        
        # Split text into transaction sections
        sections = text.split('\n\n')
        for section in sections:
            if any(keyword in section.lower() for keyword in ['transaction', 'sale', 'purchase', 'deal']):
                transaction = {'source_file': filename}
                
                for field, pattern in patterns.items():
                    match = re.search(pattern, section, re.IGNORECASE)
                    if match:
                        transaction[field] = match.group(1).strip()
                
                if 'property_address' in transaction or 'price' in transaction:
                    transactions.append(transaction)
        
        return transactions
    
    def process_legal_pdf(self, text: str, filename: str) -> List[Dict]:
        """Process legal requirements from PDF text"""
        legal_requirements = []
        
        # Extract legal information
        patterns = {
            'requirement_type': r'(?:Type|Category):\s*([^\n]+)',
            'description': r'(?:Description|Requirement):\s*([^\n]+)',
            'applicable_to': r'(?:Applicable To|For):\s*([^\n]+)',
            'penalties': r'(?:Penalties|Fines):\s*([^\n]+)',
            'deadline': r'(?:Deadline|Due Date):\s*([^\n]+)'
        }
        
        # Split text into legal sections
        sections = text.split('\n\n')
        for section in sections:
            if any(keyword in section.lower() for keyword in ['legal', 'law', 'regulation', 'requirement', 'compliance']):
                legal_req = {'source_file': filename}
                
                for field, pattern in patterns.items():
                    match = re.search(pattern, section, re.IGNORECASE)
                    if match:
                        legal_req[field] = match.group(1).strip()
                
                if 'description' in legal_req:
                    legal_requirements.append(legal_req)
        
        return legal_requirements
    
    def process_market_report_pdf(self, text: str, filename: str) -> List[Dict]:
        """Process market report data from PDF text"""
        market_reports = []
        
        # Extract market information
        patterns = {
            'period': r'(?:Period|Quarter|Year):\s*([^\n]+)',
            'summary': r'(?:Summary|Overview):\s*([^\n]+)',
            'growth_rate': r'(?:Growth|Increase|Change):\s*([^\n]+)',
            'key_highlights': r'(?:Highlights|Key Points):\s*([^\n]+)',
            'market_performance': r'(?:Performance|Trends):\s*([^\n]+)'
        }
        
        # Split text into report sections
        sections = text.split('\n\n')
        for section in sections:
            if any(keyword in section.lower() for keyword in ['market', 'report', 'trend', 'analysis', 'quarter']):
                report = {'source_file': filename}
                
                for field, pattern in patterns.items():
                    match = re.search(pattern, section, re.IGNORECASE)
                    if match:
                        report[field] = match.group(1).strip()
                
                if 'summary' in report or 'period' in report:
                    market_reports.append(report)
        
        return market_reports
    
    def process_pdf_files(self):
        """Process all PDF files in the pdfs directory"""
        pdf_files = list(self.pdf_dir.glob("*.pdf"))
        
        if not pdf_files:
            logger.info("No PDF files found in pdfs directory")
            return
        
        logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        for pdf_file in pdf_files:
            logger.info(f"Processing {pdf_file.name}...")
            
            # Extract text from PDF
            text = self.extract_text_from_pdf(pdf_file)
            if not text:
                text = self.extract_text_from_pdf_pypdf2(pdf_file)
            
            if not text:
                logger.warning(f"Could not extract text from {pdf_file.name}")
                continue
            
            # Determine PDF type and process accordingly
            filename = pdf_file.name.lower()
            
            if any(keyword in filename for keyword in ['neighborhood', 'area', 'community']):
                neighborhoods = self.process_neighborhood_pdf(text, pdf_file.name)
                self.extracted_data['neighborhoods'].extend(neighborhoods)
                logger.info(f"Extracted {len(neighborhoods)} neighborhoods from {pdf_file.name}")
            
            elif any(keyword in filename for keyword in ['transaction', 'sale', 'deal']):
                transactions = self.process_transaction_pdf(text, pdf_file.name)
                self.extracted_data['transactions'].extend(transactions)
                logger.info(f"Extracted {len(transactions)} transactions from {pdf_file.name}")
            
            elif any(keyword in filename for keyword in ['legal', 'law', 'regulation']):
                legal_reqs = self.process_legal_pdf(text, pdf_file.name)
                self.extracted_data['legal_requirements'].extend(legal_reqs)
                logger.info(f"Extracted {len(legal_reqs)} legal requirements from {pdf_file.name}")
            
            elif any(keyword in filename for keyword in ['market', 'report', 'trend']):
                market_reports = self.process_market_report_pdf(text, pdf_file.name)
                self.extracted_data['market_reports'].extend(market_reports)
                logger.info(f"Extracted {len(market_reports)} market reports from {pdf_file.name}")
            
            else:
                # Generic property data processing
                property_data = self.process_neighborhood_pdf(text, pdf_file.name)
                self.extracted_data['property_data'].extend(property_data)
                logger.info(f"Extracted {len(property_data)} property data items from {pdf_file.name}")
    
    def create_pdf_tables(self):
        """Create tables for PDF-extracted data"""
        try:
            with self.engine.connect() as conn:
                # Create neighborhoods from PDF table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS pdf_neighborhoods (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255),
                        description TEXT,
                        price_range VARCHAR(255),
                        amenities TEXT,
                        pros TEXT,
                        cons TEXT,
                        source_file VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Create transactions from PDF table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS pdf_transactions (
                        id SERIAL PRIMARY KEY,
                        property_address VARCHAR(255),
                        transaction_date VARCHAR(100),
                        price VARCHAR(100),
                        property_type VARCHAR(100),
                        bedrooms INTEGER,
                        bathrooms INTEGER,
                        area VARCHAR(100),
                        developer VARCHAR(255),
                        source_file VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Create legal requirements table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS pdf_legal_requirements (
                        id SERIAL PRIMARY KEY,
                        requirement_type VARCHAR(255),
                        description TEXT,
                        applicable_to VARCHAR(255),
                        penalties TEXT,
                        deadline VARCHAR(100),
                        source_file VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Create market reports table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS pdf_market_reports (
                        id SERIAL PRIMARY KEY,
                        period VARCHAR(100),
                        summary TEXT,
                        growth_rate VARCHAR(100),
                        key_highlights TEXT,
                        market_performance TEXT,
                        source_file VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                conn.commit()
                logger.info("✅ PDF data tables created successfully")
                
        except Exception as e:
            logger.error(f"❌ Error creating PDF tables: {e}")
            raise
    
    def ingest_pdf_data_to_postgresql(self):
        """Ingest extracted PDF data to PostgreSQL"""
        try:
            with self.engine.connect() as conn:
                # Ingest neighborhoods
                for neighborhood in self.extracted_data['neighborhoods']:
                    conn.execute(text("""
                        INSERT INTO pdf_neighborhoods 
                        (name, description, price_range, amenities, pros, cons, source_file)
                        VALUES (:name, :description, :price_range, :amenities, :pros, :cons, :source_file)
                    """), neighborhood)
                
                # Ingest transactions
                for transaction in self.extracted_data['transactions']:
                    conn.execute(text("""
                        INSERT INTO pdf_transactions 
                        (property_address, transaction_date, price, property_type, bedrooms, 
                         bathrooms, area, developer, source_file)
                        VALUES (:property_address, :transaction_date, :price, :property_type, :bedrooms,
                                :bathrooms, :area, :developer, :source_file)
                    """), transaction)
                
                # Ingest legal requirements
                for legal_req in self.extracted_data['legal_requirements']:
                    conn.execute(text("""
                        INSERT INTO pdf_legal_requirements 
                        (requirement_type, description, applicable_to, penalties, deadline, source_file)
                        VALUES (:requirement_type, :description, :applicable_to, :penalties, :deadline, :source_file)
                    """), legal_req)
                
                # Ingest market reports
                for report in self.extracted_data['market_reports']:
                    conn.execute(text("""
                        INSERT INTO pdf_market_reports 
                        (period, summary, growth_rate, key_highlights, market_performance, source_file)
                        VALUES (:period, :summary, :growth_rate, :key_highlights, :market_performance, :source_file)
                    """), report)
                
                conn.commit()
                
                total_records = sum(len(data) for data in self.extracted_data.values())
                logger.info(f"✅ Ingested {total_records} records from PDF data to PostgreSQL")
                
        except Exception as e:
            logger.error(f"❌ Error ingesting PDF data to PostgreSQL: {e}")
            raise
    
    def ingest_pdf_data_to_chromadb(self):
        """Ingest PDF data to ChromaDB for RAG functionality"""
        try:
            # Create collections for different types of PDF data
            pdf_neighborhoods_collection = self.chroma_client.get_or_create_collection("pdf_neighborhoods")
            pdf_transactions_collection = self.chroma_client.get_or_create_collection("pdf_transactions")
            pdf_legal_collection = self.chroma_client.get_or_create_collection("pdf_legal_requirements")
            pdf_market_collection = self.chroma_client.get_or_create_collection("pdf_market_reports")
            
            # Process neighborhoods
            if self.extracted_data['neighborhoods']:
                neighborhood_docs = []
                neighborhood_metadatas = []
                neighborhood_ids = []
                
                for i, neighborhood in enumerate(self.extracted_data['neighborhoods']):
                    doc_content = f"""
                    Neighborhood: {neighborhood.get('name', 'N/A')}
                    Description: {neighborhood.get('description', 'N/A')}
                    Price Range: {neighborhood.get('price_range', 'N/A')}
                    Amenities: {neighborhood.get('amenities', 'N/A')}
                    Pros: {neighborhood.get('pros', 'N/A')}
                    Cons: {neighborhood.get('cons', 'N/A')}
                    Source: {neighborhood.get('source_file', 'N/A')}
                    """
                    
                    neighborhood_docs.append(doc_content)
                    neighborhood_metadatas.append({
                        "type": "pdf_neighborhood",
                        "source_file": neighborhood.get('source_file', 'N/A')
                    })
                    neighborhood_ids.append(f"pdf_neighborhood_{i}")
                
                pdf_neighborhoods_collection.add(
                    documents=neighborhood_docs,
                    metadatas=neighborhood_metadatas,
                    ids=neighborhood_ids
                )
                logger.info(f"✅ Added {len(neighborhood_docs)} PDF neighborhoods to ChromaDB")
            
            # Process transactions
            if self.extracted_data['transactions']:
                transaction_docs = []
                transaction_metadatas = []
                transaction_ids = []
                
                for i, transaction in enumerate(self.extracted_data['transactions']):
                    doc_content = f"""
                    Property Address: {transaction.get('property_address', 'N/A')}
                    Transaction Date: {transaction.get('transaction_date', 'N/A')}
                    Price: {transaction.get('price', 'N/A')}
                    Property Type: {transaction.get('property_type', 'N/A')}
                    Bedrooms: {transaction.get('bedrooms', 'N/A')}
                    Bathrooms: {transaction.get('bathrooms', 'N/A')}
                    Area: {transaction.get('area', 'N/A')}
                    Developer: {transaction.get('developer', 'N/A')}
                    Source: {transaction.get('source_file', 'N/A')}
                    """
                    
                    transaction_docs.append(doc_content)
                    transaction_metadatas.append({
                        "type": "pdf_transaction",
                        "source_file": transaction.get('source_file', 'N/A')
                    })
                    transaction_ids.append(f"pdf_transaction_{i}")
                
                pdf_transactions_collection.add(
                    documents=transaction_docs,
                    metadatas=transaction_metadatas,
                    ids=transaction_ids
                )
                logger.info(f"✅ Added {len(transaction_docs)} PDF transactions to ChromaDB")
            
            # Process legal requirements
            if self.extracted_data['legal_requirements']:
                legal_docs = []
                legal_metadatas = []
                legal_ids = []
                
                for i, legal_req in enumerate(self.extracted_data['legal_requirements']):
                    doc_content = f"""
                    Requirement Type: {legal_req.get('requirement_type', 'N/A')}
                    Description: {legal_req.get('description', 'N/A')}
                    Applicable To: {legal_req.get('applicable_to', 'N/A')}
                    Penalties: {legal_req.get('penalties', 'N/A')}
                    Deadline: {legal_req.get('deadline', 'N/A')}
                    Source: {legal_req.get('source_file', 'N/A')}
                    """
                    
                    legal_docs.append(doc_content)
                    legal_metadatas.append({
                        "type": "pdf_legal_requirement",
                        "source_file": legal_req.get('source_file', 'N/A')
                    })
                    legal_ids.append(f"pdf_legal_{i}")
                
                pdf_legal_collection.add(
                    documents=legal_docs,
                    metadatas=legal_metadatas,
                    ids=legal_ids
                )
                logger.info(f"✅ Added {len(legal_docs)} PDF legal requirements to ChromaDB")
            
            # Process market reports
            if self.extracted_data['market_reports']:
                market_docs = []
                market_metadatas = []
                market_ids = []
                
                for i, report in enumerate(self.extracted_data['market_reports']):
                    doc_content = f"""
                    Period: {report.get('period', 'N/A')}
                    Summary: {report.get('summary', 'N/A')}
                    Growth Rate: {report.get('growth_rate', 'N/A')}
                    Key Highlights: {report.get('key_highlights', 'N/A')}
                    Market Performance: {report.get('market_performance', 'N/A')}
                    Source: {report.get('source_file', 'N/A')}
                    """
                    
                    market_docs.append(doc_content)
                    market_metadatas.append({
                        "type": "pdf_market_report",
                        "source_file": report.get('source_file', 'N/A')
                    })
                    market_ids.append(f"pdf_market_{i}")
                
                pdf_market_collection.add(
                    documents=market_docs,
                    metadatas=market_metadatas,
                    ids=market_ids
                )
                logger.info(f"✅ Added {len(market_docs)} PDF market reports to ChromaDB")
                
        except Exception as e:
            logger.error(f"❌ Error ingesting PDF data to ChromaDB: {e}")
            raise
    
    def run_full_pdf_ingestion(self):
        """Run complete PDF data ingestion process"""
        try:
            logger.info("🚀 Starting PDF data ingestion...")
            
            # Process PDF files
            self.process_pdf_files()
            
            # Create tables
            self.create_pdf_tables()
            
            # Ingest to PostgreSQL
            self.ingest_pdf_data_to_postgresql()
            
            # Ingest to ChromaDB
            self.ingest_pdf_data_to_chromadb()
            
            logger.info("🎉 PDF data ingestion completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Error during PDF data ingestion: {e}")
            raise

def main():
    """Main function to run the PDF ingestion"""
    try:
        ingester = PDFDataIngester()
        ingester.run_full_pdf_ingestion()
        
        print("\n" + "="*60)
        print("🎉 PDF DATA INGESTION COMPLETED!")
        print("="*60)
        print("✅ Processed PDF files from data/pdfs/ directory")
        print("✅ Created PDF-specific tables in PostgreSQL")
        print("✅ Ingested data to ChromaDB for RAG functionality")
        print("\nTo add more data:")
        print("1. Place your PDF files in the 'data/pdfs/' directory")
        print("2. Run this script again: python pdf_data_ingestion.py")
        print("="*60)
        
    except Exception as e:
        logger.error(f"❌ Failed to run PDF ingestion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
