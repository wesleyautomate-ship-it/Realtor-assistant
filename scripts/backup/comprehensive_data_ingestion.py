#!/usr/bin/env python3
"""
Comprehensive Data Ingestion Script for Dubai Real Estate RAG System
This script processes ALL file types and ingests data into PostgreSQL and ChromaDB
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
import openpyxl
from docx import Document

# Add parent directory to path to import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComprehensiveDataIngester:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL", "postgresql://postgres:password123@localhost:5432/real_estate_db")
        self.engine = create_engine(self.db_url)
        self.chroma_client = chromadb.HttpClient(host="localhost", port=8000)
        
        # Data directories
        self.data_root = Path("../data")
        
        # Processing results
        self.extracted_data = {
            "properties": [],
            "clients": [],
            "transactions": [],
            "neighborhoods": [],
            "market_data": [],
            "legal_requirements": [],
            "company_policies": [],
            "analytics": [],
            "employees": [],
            "agents": []
        }
        
    def process_all_files(self):
        """Process all file types in the data directory"""
        logger.info("🚀 Starting comprehensive file processing...")
        
        # Process CSV files
        self.process_csv_files()
        
        # Process JSON files
        self.process_json_files()
        
        # Process Excel files
        self.process_excel_files()
        
        # Process PDF files
        self.process_pdf_files()
        
        # Process Word files
        self.process_word_files()
        
        logger.info("✅ File processing completed!")
    
    def process_csv_files(self):
        """Process all CSV files"""
        csv_files = list(self.data_root.glob("*.csv"))
        logger.info(f"Found {len(csv_files)} CSV files to process")
        
        for csv_file in csv_files:
            logger.info(f"Processing CSV: {csv_file.name}")
            try:
                df = pd.read_csv(csv_file)
                
                if "properties" in csv_file.name.lower() or "listings" in csv_file.name.lower():
                    self.process_properties_csv(df, csv_file.name)
                elif "clients" in csv_file.name.lower():
                    self.process_clients_csv(df, csv_file.name)
                elif "transactions" in csv_file.name.lower():
                    self.process_transactions_csv(df, csv_file.name)
                elif "market" in csv_file.name.lower():
                    self.process_market_csv(df, csv_file.name)
                elif "employees" in csv_file.name.lower():
                    self.process_employees_csv(df, csv_file.name)
                elif "agents" in csv_file.name.lower():
                    self.process_agents_csv(df, csv_file.name)
                else:
                    self.process_generic_csv(df, csv_file.name)
                    
            except Exception as e:
                logger.error(f"Error processing {csv_file.name}: {e}")
    
    def process_json_files(self):
        """Process all JSON files"""
        json_files = list(self.data_root.glob("*.json"))
        logger.info(f"Found {len(json_files)} JSON files to process")
        
        for json_file in json_files:
            logger.info(f"Processing JSON: {json_file.name}")
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "neighborhoods" in json_file.name.lower():
                    self.process_neighborhoods_json(data, json_file.name)
                elif "analytics" in json_file.name.lower():
                    self.process_analytics_json(data, json_file.name)
                elif "market_trends" in json_file.name.lower():
                    self.process_market_trends_json(data, json_file.name)
                else:
                    self.process_generic_json(data, json_file.name)
                    
            except Exception as e:
                logger.error(f"Error processing {json_file.name}: {e}")
    
    def process_excel_files(self):
        """Process all Excel files"""
        excel_files = list(self.data_root.glob("*.xlsx"))
        logger.info(f"Found {len(excel_files)} Excel files to process")
        
        for excel_file in excel_files:
            logger.info(f"Processing Excel: {excel_file.name}")
            try:
                excel_data = pd.read_excel(excel_file, sheet_name=None)
                
                for sheet_name, df in excel_data.items():
                    if "properties" in sheet_name.lower() or "listings" in sheet_name.lower():
                        self.process_properties_excel(df, excel_file.name, sheet_name)
                    elif "market" in sheet_name.lower():
                        self.process_market_excel(df, excel_file.name, sheet_name)
                    else:
                        self.process_generic_excel(df, excel_file.name, sheet_name)
                        
            except Exception as e:
                logger.error(f"Error processing {excel_file.name}: {e}")
    
    def process_pdf_files(self):
        """Process all PDF files"""
        pdf_files = list(self.data_root.glob("*.pdf"))
        logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        for pdf_file in pdf_files:
            logger.info(f"Processing PDF: {pdf_file.name}")
            try:
                text = self.extract_text_from_pdf(pdf_file)
                if not text:
                    text = self.extract_text_from_pdf_pypdf2(pdf_file)
                
                if text:
                    if "legal" in pdf_file.name.lower():
                        self.process_legal_pdf(text, pdf_file.name)
                    elif "brochure" in pdf_file.name.lower():
                        self.process_brochure_pdf(text, pdf_file.name)
                    else:
                        self.process_generic_pdf(text, pdf_file.name)
                        
            except Exception as e:
                logger.error(f"Error processing {pdf_file.name}: {e}")
    
    def process_word_files(self):
        """Process all Word files"""
        word_files = list(self.data_root.glob("*.docx"))
        logger.info(f"Found {len(word_files)} Word files to process")
        
        for word_file in word_files:
            logger.info(f"Processing Word: {word_file.name}")
            try:
                doc = Document(word_file)
                text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                
                if "market_report" in word_file.name.lower():
                    self.process_market_report_word(text, word_file.name)
                elif "company_policies" in word_file.name.lower():
                    self.process_company_policies_word(text, word_file.name)
                else:
                    self.process_generic_word(text, word_file.name)
                    
            except Exception as e:
                logger.error(f"Error processing {word_file.name}: {e}")
    
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
    
    # CSV Processing Methods
    def process_properties_csv(self, df: pd.DataFrame, filename: str):
        """Process properties CSV data"""
        for _, row in df.iterrows():
            property_data = {
                'source_file': filename,
                'title': row.get('title', ''),
                'description': row.get('description', ''),
                'price': row.get('price', 0),
                'location': row.get('location', ''),
                'property_type': row.get('property_type', ''),
                'bedrooms': row.get('bedrooms', 0),
                'bathrooms': row.get('bathrooms', 0),
                'area_sqft': row.get('area_sqft', 0),
                'developer': row.get('developer', ''),
                'completion_date': row.get('completion_date', ''),
                'amenities': row.get('amenities', ''),
                'view_type': row.get('view_type', ''),
                'service_charges': row.get('service_charges', 0)
            }
            self.extracted_data['properties'].append(property_data)
        
        logger.info(f"Processed {len(df)} properties from {filename}")
    
    def process_clients_csv(self, df: pd.DataFrame, filename: str):
        """Process clients CSV data"""
        for _, row in df.iterrows():
            client_data = {
                'source_file': filename,
                'name': row.get('name', ''),
                'email': row.get('email', ''),
                'phone': row.get('phone', ''),
                'preferences': row.get('preferences', ''),
                'budget_range': row.get('budget_range', ''),
                'preferred_areas': row.get('preferred_areas', ''),
                'property_type': row.get('property_type', ''),
                'status': row.get('status', '')
            }
            self.extracted_data['clients'].append(client_data)
        
        logger.info(f"Processed {len(df)} clients from {filename}")
    
    def process_transactions_csv(self, df: pd.DataFrame, filename: str):
        """Process transactions CSV data"""
        for _, row in df.iterrows():
            transaction_data = {
                'source_file': filename,
                'property_address': row.get('property_address', ''),
                'transaction_date': row.get('transaction_date', ''),
                'price': row.get('price', 0),
                'property_type': row.get('property_type', ''),
                'bedrooms': row.get('bedrooms', 0),
                'bathrooms': row.get('bathrooms', 0),
                'area': row.get('area', 0),
                'developer': row.get('developer', ''),
                'buyer_name': row.get('buyer_name', ''),
                'seller_name': row.get('seller_name', ''),
                'agent_name': row.get('agent_name', '')
            }
            self.extracted_data['transactions'].append(transaction_data)
        
        logger.info(f"Processed {len(df)} transactions from {filename}")
    
    def process_market_csv(self, df: pd.DataFrame, filename: str):
        """Process market CSV data"""
        for _, row in df.iterrows():
            market_data = {
                'source_file': filename,
                'content': f"Period: {row.get('period', '')} | Summary: {row.get('summary', '')} | Growth: {row.get('growth_rate', '')} | Highlights: {row.get('key_highlights', '')} | Performance: {row.get('market_performance', '')}",
                'type': 'market_csv',
                'extracted_at': datetime.now().isoformat()
            }
            self.extracted_data['market_data'].append(market_data)
        
        logger.info(f"Processed {len(df)} market records from {filename}")
    
    def process_employees_csv(self, df: pd.DataFrame, filename: str):
        """Process employees CSV data"""
        for _, row in df.iterrows():
            employee_data = {
                'source_file': filename,
                'name': row.get('name', ''),
                'email': row.get('email', ''),
                'position': row.get('position', ''),
                'department': row.get('department', ''),
                'hire_date': row.get('hire_date', ''),
                'salary': row.get('salary', 0)
            }
            self.extracted_data['employees'].append(employee_data)
        
        logger.info(f"Processed {len(df)} employees from {filename}")
    
    def process_agents_csv(self, df: pd.DataFrame, filename: str):
        """Process agents CSV data"""
        for _, row in df.iterrows():
            agent_data = {
                'source_file': filename,
                'name': row.get('name', ''),
                'email': row.get('email', ''),
                'phone': row.get('phone', ''),
                'specialization': row.get('specialization', ''),
                'experience_years': row.get('experience_years', 0),
                'commission_rate': row.get('commission_rate', 0)
            }
            self.extracted_data['agents'].append(agent_data)
        
        logger.info(f"Processed {len(df)} agents from {filename}")
    
    # JSON Processing Methods
    def process_neighborhoods_json(self, data: List[Dict], filename: str):
        """Process neighborhoods JSON data"""
        for item in data:
            neighborhood_data = {
                'source_file': filename,
                'name': item.get('name', ''),
                'description': item.get('description', ''),
                'price_ranges': json.dumps(item.get('price_ranges', {})),
                'rental_yields': json.dumps(item.get('rental_yields', {})),
                'amenities': json.dumps(item.get('amenities', [])),
                'pros': json.dumps(item.get('pros', [])),
                'cons': json.dumps(item.get('cons', []))
            }
            self.extracted_data['neighborhoods'].append(neighborhood_data)
        
        logger.info(f"Processed {len(data)} neighborhoods from {filename}")
    
    def process_analytics_json(self, data: List[Dict], filename: str):
        """Process analytics JSON data"""
        for item in data:
            analytics_data = {
                'source_file': filename,
                'period': item.get('period', ''),
                'summary': item.get('summary', ''),
                'key_highlights': json.dumps(item.get('key_highlights', [])),
                'market_performance': json.dumps(item.get('market_performance', {}))
            }
            self.extracted_data['analytics'].append(analytics_data)
        
        logger.info(f"Processed {len(data)} analytics records from {filename}")
    
    def process_market_trends_json(self, data: List[Dict], filename: str):
        """Process market trends JSON data"""
        for item in data:
            trend_data = {
                'source_file': filename,
                'content': f"Period: {item.get('period', '')} | Trend: {item.get('trend', '')} | Growth Rate: {item.get('growth_rate', '')} | Analysis: {item.get('analysis', '')}",
                'type': 'market_trends_json',
                'extracted_at': datetime.now().isoformat()
            }
            self.extracted_data['market_data'].append(trend_data)
        
        logger.info(f"Processed {len(data)} market trends from {filename}")
    
    # Excel Processing Methods
    def process_properties_excel(self, df: pd.DataFrame, filename: str, sheet_name: str):
        """Process properties Excel data"""
        for _, row in df.iterrows():
            property_data = {
                'source_file': f"{filename}_{sheet_name}",
                'title': row.get('title', ''),
                'description': row.get('description', ''),
                'price': row.get('price', 0),
                'location': row.get('location', ''),
                'property_type': row.get('property_type', ''),
                'bedrooms': row.get('bedrooms', 0),
                'bathrooms': row.get('bathrooms', 0),
                'area_sqft': row.get('area_sqft', 0),
                'developer': row.get('developer', ''),
                'completion_date': row.get('completion_date', ''),
                'amenities': row.get('amenities', ''),
                'view_type': row.get('view_type', ''),
                'service_charges': row.get('service_charges', 0)
            }
            self.extracted_data['properties'].append(property_data)
        
        logger.info(f"Processed {len(df)} properties from {filename} sheet {sheet_name}")
    
    def process_market_excel(self, df: pd.DataFrame, filename: str, sheet_name: str):
        """Process market Excel data"""
        for _, row in df.iterrows():
            market_data = {
                'source_file': f"{filename}_{sheet_name}",
                'content': f"Period: {row.get('period', '')} | Summary: {row.get('summary', '')} | Growth Rate: {row.get('growth_rate', '')} | Highlights: {row.get('key_highlights', '')} | Performance: {row.get('market_performance', '')}",
                'type': 'market_excel',
                'extracted_at': datetime.now().isoformat()
            }
            self.extracted_data['market_data'].append(market_data)
        
        logger.info(f"Processed {len(df)} market records from {filename} sheet {sheet_name}")
    
    # PDF Processing Methods
    def process_legal_pdf(self, text: str, filename: str):
        """Process legal requirements from PDF"""
        legal_requirements = []
        
        patterns = {
            'requirement_type': r'(?:Type|Category):\s*([^\n]+)',
            'description': r'(?:Description|Requirement):\s*([^\n]+)',
            'applicable_to': r'(?:Applicable To|For):\s*([^\n]+)',
            'penalties': r'(?:Penalties|Fines):\s*([^\n]+)',
            'deadline': r'(?:Deadline|Due Date):\s*([^\n]+)'
        }
        
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
        
        self.extracted_data['legal_requirements'].extend(legal_requirements)
        logger.info(f"Processed {len(legal_requirements)} legal requirements from {filename}")
    
    def process_brochure_pdf(self, text: str, filename: str):
        """Process property brochure from PDF"""
        brochure_data = {
            'source_file': filename,
            'content': text,
            'type': 'property_brochure',
            'extracted_at': datetime.now().isoformat()
        }
        self.extracted_data['analytics'].append(brochure_data)
        logger.info(f"Processed property brochure from {filename}")
    
    # Word Processing Methods
    def process_market_report_word(self, text: str, filename: str):
        """Process market report from Word document"""
        market_data = {
            'source_file': filename,
            'content': text,
            'type': 'market_report',
            'extracted_at': datetime.now().isoformat()
        }
        self.extracted_data['market_data'].append(market_data)
        logger.info(f"Processed market report from {filename}")
    
    def process_company_policies_word(self, text: str, filename: str):
        """Process company policies from Word document"""
        policy_data = {
            'source_file': filename,
            'content': text,
            'type': 'company_policy',
            'extracted_at': datetime.now().isoformat()
        }
        self.extracted_data['company_policies'].append(policy_data)
        logger.info(f"Processed company policies from {filename}")
    
    # Generic Processing Methods
    def process_generic_csv(self, df: pd.DataFrame, filename: str):
        """Process generic CSV data"""
        for _, row in df.iterrows():
            generic_data = {
                'source_file': filename,
                'data': row.to_dict(),
                'type': 'generic_csv',
                'extracted_at': datetime.now().isoformat()
            }
            self.extracted_data['analytics'].append(generic_data)
        
        logger.info(f"Processed {len(df)} generic records from {filename}")
    
    def process_generic_json(self, data: Any, filename: str):
        """Process generic JSON data"""
        generic_data = {
            'source_file': filename,
            'data': data,
            'type': 'generic_json',
            'extracted_at': datetime.now().isoformat()
        }
        self.extracted_data['analytics'].append(generic_data)
        logger.info(f"Processed generic JSON data from {filename}")
    
    def process_generic_excel(self, df: pd.DataFrame, filename: str, sheet_name: str):
        """Process generic Excel data"""
        for _, row in df.iterrows():
            generic_data = {
                'source_file': f"{filename}_{sheet_name}",
                'data': row.to_dict(),
                'type': 'generic_excel',
                'extracted_at': datetime.now().isoformat()
            }
            self.extracted_data['analytics'].append(generic_data)
        
        logger.info(f"Processed {len(df)} generic records from {filename} sheet {sheet_name}")
    
    def process_generic_pdf(self, text: str, filename: str):
        """Process generic PDF data"""
        generic_data = {
            'source_file': filename,
            'content': text,
            'type': 'generic_pdf',
            'extracted_at': datetime.now().isoformat()
        }
        self.extracted_data['analytics'].append(generic_data)
        logger.info(f"Processed generic PDF data from {filename}")
    
    def process_generic_word(self, text: str, filename: str):
        """Process generic Word data"""
        generic_data = {
            'source_file': filename,
            'content': text,
            'type': 'generic_word',
            'extracted_at': datetime.now().isoformat()
        }
        self.extracted_data['analytics'].append(generic_data)
        logger.info(f"Processed generic Word data from {filename}")
    
    def create_comprehensive_tables(self):
        """Create comprehensive tables for all data types"""
        try:
            with self.engine.connect() as conn:
                # Create comprehensive properties table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS comprehensive_properties (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(255),
                        description TEXT,
                        price DECIMAL(12,2),
                        location VARCHAR(255),
                        property_type VARCHAR(100),
                        bedrooms INTEGER,
                        bathrooms INTEGER,
                        area_sqft DECIMAL(10,2),
                        developer VARCHAR(255),
                        completion_date VARCHAR(50),
                        amenities TEXT,
                        view_type VARCHAR(100),
                        service_charges DECIMAL(10,2),
                        source_file VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Create comprehensive clients table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS comprehensive_clients (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255),
                        email VARCHAR(255),
                        phone VARCHAR(100),
                        preferences TEXT,
                        budget_range VARCHAR(100),
                        preferred_areas TEXT,
                        property_type VARCHAR(100),
                        status VARCHAR(50),
                        source_file VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Create comprehensive transactions table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS comprehensive_transactions (
                        id SERIAL PRIMARY KEY,
                        property_address VARCHAR(255),
                        transaction_date VARCHAR(100),
                        price DECIMAL(12,2),
                        property_type VARCHAR(100),
                        bedrooms INTEGER,
                        bathrooms INTEGER,
                        area DECIMAL(10,2),
                        developer VARCHAR(255),
                        buyer_name VARCHAR(255),
                        seller_name VARCHAR(255),
                        agent_name VARCHAR(255),
                        source_file VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Create comprehensive neighborhoods table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS comprehensive_neighborhoods (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255),
                        description TEXT,
                        price_ranges JSONB,
                        rental_yields JSONB,
                        amenities JSONB,
                        pros JSONB,
                        cons JSONB,
                        source_file VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Create comprehensive analytics table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS comprehensive_analytics (
                        id SERIAL PRIMARY KEY,
                        period VARCHAR(100),
                        summary TEXT,
                        key_highlights JSONB,
                        market_performance JSONB,
                        source_file VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Create comprehensive legal requirements table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS comprehensive_legal_requirements (
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
                
                # Create comprehensive market data table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS comprehensive_market_data (
                        id SERIAL PRIMARY KEY,
                        content TEXT,
                        type VARCHAR(100),
                        source_file VARCHAR(255),
                        extracted_at TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Create comprehensive company policies table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS comprehensive_company_policies (
                        id SERIAL PRIMARY KEY,
                        content TEXT,
                        type VARCHAR(100),
                        source_file VARCHAR(255),
                        extracted_at TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                conn.commit()
                logger.info("✅ Comprehensive tables created successfully")
                
        except Exception as e:
            logger.error(f"❌ Error creating comprehensive tables: {e}")
            raise
    
    def ingest_comprehensive_data_to_postgresql(self):
        """Ingest all extracted data to PostgreSQL"""
        try:
            with self.engine.connect() as conn:
                # Ingest properties
                for prop in self.extracted_data['properties']:
                    conn.execute(text("""
                        INSERT INTO comprehensive_properties 
                        (title, description, price, location, property_type, bedrooms, 
                         bathrooms, area_sqft, developer, completion_date, amenities, 
                         view_type, service_charges, source_file)
                        VALUES (:title, :description, :price, :location, :property_type, :bedrooms,
                                :bathrooms, :area_sqft, :developer, :completion_date, :amenities,
                                :view_type, :service_charges, :source_file)
                    """), prop)
                
                # Ingest clients
                for client in self.extracted_data['clients']:
                    conn.execute(text("""
                        INSERT INTO comprehensive_clients 
                        (name, email, phone, preferences, budget_range, preferred_areas, 
                         property_type, status, source_file)
                        VALUES (:name, :email, :phone, :preferences, :budget_range, :preferred_areas,
                                :property_type, :status, :source_file)
                    """), client)
                
                # Ingest transactions
                for transaction in self.extracted_data['transactions']:
                    conn.execute(text("""
                        INSERT INTO comprehensive_transactions 
                        (property_address, transaction_date, price, property_type, bedrooms,
                         bathrooms, area, developer, buyer_name, seller_name, agent_name, source_file)
                        VALUES (:property_address, :transaction_date, :price, :property_type, :bedrooms,
                                :bathrooms, :area, :developer, :buyer_name, :seller_name, :agent_name, :source_file)
                    """), transaction)
                
                # Ingest neighborhoods
                for neighborhood in self.extracted_data['neighborhoods']:
                    conn.execute(text("""
                        INSERT INTO comprehensive_neighborhoods 
                        (name, description, price_ranges, rental_yields, amenities, pros, cons, source_file)
                        VALUES (:name, :description, :price_ranges, :rental_yields, :amenities, :pros, :cons, :source_file)
                    """), neighborhood)
                
                # Ingest analytics
                for analytics in self.extracted_data['analytics']:
                    if isinstance(analytics, dict) and 'period' in analytics:
                        conn.execute(text("""
                            INSERT INTO comprehensive_analytics 
                            (period, summary, key_highlights, market_performance, source_file)
                            VALUES (:period, :summary, :key_highlights, :market_performance, :source_file)
                        """), analytics)
                
                # Ingest legal requirements
                for legal_req in self.extracted_data['legal_requirements']:
                    conn.execute(text("""
                        INSERT INTO comprehensive_legal_requirements 
                        (requirement_type, description, applicable_to, penalties, deadline, source_file)
                        VALUES (:requirement_type, :description, :applicable_to, :penalties, :deadline, :source_file)
                    """), legal_req)
                
                # Ingest market data
                for market_data in self.extracted_data['market_data']:
                    conn.execute(text("""
                        INSERT INTO comprehensive_market_data 
                        (content, type, source_file, extracted_at)
                        VALUES (:content, :type, :source_file, :extracted_at)
                    """), market_data)
                
                # Ingest company policies
                for policy in self.extracted_data['company_policies']:
                    conn.execute(text("""
                        INSERT INTO comprehensive_company_policies 
                        (content, type, source_file, extracted_at)
                        VALUES (:content, :type, :source_file, :extracted_at)
                    """), policy)
                
                conn.commit()
                
                total_records = sum(len(data) for data in self.extracted_data.values())
                logger.info(f"✅ Ingested {total_records} records to PostgreSQL")
                
        except Exception as e:
            logger.error(f"❌ Error ingesting data to PostgreSQL: {e}")
            raise
    
    def ingest_comprehensive_data_to_chromadb(self):
        """Ingest all data to ChromaDB for RAG functionality"""
        try:
            # Create comprehensive collections
            comprehensive_collection = self.chroma_client.get_or_create_collection("comprehensive_data")
            
            all_documents = []
            all_metadatas = []
            all_ids = []
            
            # Process all data types
            for data_type, data_list in self.extracted_data.items():
                for i, item in enumerate(data_list):
                    if isinstance(item, dict):
                        # Create document content based on data type
                        if data_type == 'properties':
                            doc_content = f"""
                            Property: {item.get('title', 'N/A')}
                            Description: {item.get('description', 'N/A')}
                            Price: AED {item.get('price', 'N/A')}
                            Location: {item.get('location', 'N/A')}
                            Type: {item.get('property_type', 'N/A')}
                            Bedrooms: {item.get('bedrooms', 'N/A')}
                            Bathrooms: {item.get('bathrooms', 'N/A')}
                            Area: {item.get('area_sqft', 'N/A')} sq ft
                            Developer: {item.get('developer', 'N/A')}
                            Source: {item.get('source_file', 'N/A')}
                            """
                        elif data_type == 'clients':
                            doc_content = f"""
                            Client: {item.get('name', 'N/A')}
                            Email: {item.get('email', 'N/A')}
                            Phone: {item.get('phone', 'N/A')}
                            Preferences: {item.get('preferences', 'N/A')}
                            Budget: {item.get('budget_range', 'N/A')}
                            Preferred Areas: {item.get('preferred_areas', 'N/A')}
                            Source: {item.get('source_file', 'N/A')}
                            """
                        elif data_type == 'transactions':
                            doc_content = f"""
                            Transaction: {item.get('property_address', 'N/A')}
                            Date: {item.get('transaction_date', 'N/A')}
                            Price: AED {item.get('price', 'N/A')}
                            Type: {item.get('property_type', 'N/A')}
                            Buyer: {item.get('buyer_name', 'N/A')}
                            Seller: {item.get('seller_name', 'N/A')}
                            Agent: {item.get('agent_name', 'N/A')}
                            Source: {item.get('source_file', 'N/A')}
                            """
                        elif data_type == 'neighborhoods':
                            doc_content = f"""
                            Neighborhood: {item.get('name', 'N/A')}
                            Description: {item.get('description', 'N/A')}
                            Price Ranges: {item.get('price_ranges', 'N/A')}
                            Rental Yields: {item.get('rental_yields', 'N/A')}
                            Amenities: {item.get('amenities', 'N/A')}
                            Source: {item.get('source_file', 'N/A')}
                            """
                        elif data_type == 'legal_requirements':
                            doc_content = f"""
                            Legal Requirement: {item.get('requirement_type', 'N/A')}
                            Description: {item.get('description', 'N/A')}
                            Applicable To: {item.get('applicable_to', 'N/A')}
                            Penalties: {item.get('penalties', 'N/A')}
                            Deadline: {item.get('deadline', 'N/A')}
                            Source: {item.get('source_file', 'N/A')}
                            """
                        elif data_type == 'market_data':
                            doc_content = f"""
                            Market Data: {item.get('type', 'N/A')}
                            Content: {item.get('content', 'N/A')[:500]}...
                            Source: {item.get('source_file', 'N/A')}
                            """
                        elif data_type == 'company_policies':
                            doc_content = f"""
                            Company Policy: {item.get('type', 'N/A')}
                            Content: {item.get('content', 'N/A')[:500]}...
                            Source: {item.get('source_file', 'N/A')}
                            """
                        else:
                            # Generic content for other data types
                            doc_content = f"""
                            Data Type: {data_type}
                            Content: {str(item)[:500]}...
                            Source: {item.get('source_file', 'N/A')}
                            """
                        
                        all_documents.append(doc_content)
                        all_metadatas.append({
                            "type": data_type,
                            "source_file": item.get('source_file', 'N/A')
                        })
                        all_ids.append(f"{data_type}_{i}")
            
            if all_documents:
                comprehensive_collection.add(
                    documents=all_documents,
                    metadatas=all_metadatas,
                    ids=all_ids
                )
                logger.info(f"✅ Added {len(all_documents)} documents to ChromaDB")
                
        except Exception as e:
            logger.error(f"❌ Error ingesting data to ChromaDB: {e}")
            raise
    
    def run_comprehensive_ingestion(self):
        """Run complete comprehensive data ingestion process"""
        try:
            logger.info("🚀 Starting comprehensive data ingestion...")
            
            # Process all file types
            self.process_all_files()
            
            # Create tables
            self.create_comprehensive_tables()
            
            # Ingest to PostgreSQL
            self.ingest_comprehensive_data_to_postgresql()
            
            # Ingest to ChromaDB
            self.ingest_comprehensive_data_to_chromadb()
            
            logger.info("🎉 Comprehensive data ingestion completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Error during comprehensive data ingestion: {e}")
            raise

def main():
    """Main function to run the comprehensive ingestion"""
    try:
        ingester = ComprehensiveDataIngester()
        ingester.run_comprehensive_ingestion()
        
        print("\n" + "="*60)
        print("🎉 COMPREHENSIVE DATA INGESTION COMPLETED!")
        print("="*60)
        print("✅ Processed ALL file types from data directory:")
        print("   - CSV files (properties, clients, transactions, etc.)")
        print("   - JSON files (analytics, neighborhoods, trends)")
        print("   - Excel files (comprehensive data, market data)")
        print("   - PDF files (legal guidelines, brochures)")
        print("   - Word documents (market reports, company policies)")
        print("✅ Created comprehensive tables in PostgreSQL")
        print("✅ Added all data to ChromaDB for RAG functionality")
        print("\nYour RAG system now has comprehensive Dubai real estate data!")
        print("="*60)
        
    except Exception as e:
        logger.error(f"❌ Failed to run comprehensive ingestion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
