"""
Data Storage Layer

Handles data storage to PostgreSQL and ChromaDB with role-based access control.
"""

import pandas as pd
import psycopg2
import chromadb
from typing import Dict, List, Any, Optional
import logging
import json
from datetime import datetime

class DataStorage:
    """Handles data storage to various databases"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.pg_conn = None
        self.chroma_client = None
        
    def connect_databases(self):
        """Connect to PostgreSQL and ChromaDB"""
        try:
            # PostgreSQL connection
            self.pg_conn = psycopg2.connect(
                host=self.config['postgres']['host'],
                database=self.config['postgres']['database'],
                user=self.config['postgres']['user'],
                password=self.config['postgres']['password'],
                port=self.config['postgres'].get('port', 5432)
            )
            
            # ChromaDB connection
            self.chroma_client = chromadb.HttpClient(
                host=self.config['chroma']['host'],
                port=self.config['chroma']['port']
            )
            
            self.logger.info("Successfully connected to databases")
            
        except Exception as e:
            self.logger.error(f"Error connecting to databases: {e}")
            raise
    
    def store_properties_postgres(self, properties: List[Dict[str, Any]]) -> bool:
        """Store property data in PostgreSQL"""
        try:
            cursor = self.pg_conn.cursor()
            
            for property_data in properties:
                # Insert or update property
                query = """
                INSERT INTO enhanced_properties (
                    address, price_aed, bedrooms, bathrooms, square_feet,
                    property_type, area, developer, completion_date, view,
                    amenities, service_charges, agent, agency, price_per_sqft,
                    market_context, investment_metrics, property_classification,
                    location_intelligence, validation_flags, cleaned_at, enriched_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                ) ON CONFLICT (address) DO UPDATE SET
                    price_aed = EXCLUDED.price_aed,
                    price_per_sqft = EXCLUDED.price_per_sqft,
                    market_context = EXCLUDED.market_context,
                    investment_metrics = EXCLUDED.investment_metrics,
                    property_classification = EXCLUDED.property_classification,
                    location_intelligence = EXCLUDED.location_intelligence,
                    validation_flags = EXCLUDED.validation_flags,
                    enriched_at = EXCLUDED.enriched_at
                """
                
                cursor.execute(query, (
                    property_data.get('address'),
                    property_data.get('price_aed'),
                    property_data.get('bedrooms'),
                    property_data.get('bathrooms'),
                    property_data.get('square_feet'),
                    property_data.get('property_type'),
                    property_data.get('area'),
                    property_data.get('developer'),
                    property_data.get('completion_date'),
                    property_data.get('view'),
                    json.dumps(property_data.get('amenities', [])),
                    property_data.get('service_charges'),
                    property_data.get('agent'),
                    property_data.get('agency'),
                    property_data.get('price_per_sqft'),
                    json.dumps(property_data.get('market_context', {})),
                    json.dumps(property_data.get('investment_metrics', {})),
                    json.dumps(property_data.get('property_classification', {})),
                    json.dumps(property_data.get('location_intelligence', {})),
                    json.dumps(property_data.get('validation_flags', {})),
                    property_data.get('cleaned_at'),
                    property_data.get('enriched_at')
                ))
            
            self.pg_conn.commit()
            self.logger.info(f"Successfully stored {len(properties)} properties in PostgreSQL")
            return True
            
        except Exception as e:
            self.logger.error(f"Error storing properties in PostgreSQL: {e}")
            if self.pg_conn:
                self.pg_conn.rollback()
            return False
    
    def store_properties_chroma(self, properties: List[Dict[str, Any]]) -> bool:
        """Store property data in ChromaDB for semantic search"""
        try:
            collection = self.chroma_client.get_or_create_collection("properties")
            
            documents = []
            metadatas = []
            ids = []
            
            for i, property_data in enumerate(properties):
                # Create document text for semantic search
                doc_text = f"""
                Property: {property_data.get('address', '')}
                Type: {property_data.get('property_type', '')}
                Area: {property_data.get('area', '')}
                Price: {property_data.get('price_aed', '')} AED
                Bedrooms: {property_data.get('bedrooms', '')}
                Bathrooms: {property_data.get('bathrooms', '')}
                Square Feet: {property_data.get('square_feet', '')}
                Developer: {property_data.get('developer', '')}
                Amenities: {', '.join(property_data.get('amenities', []))}
                Market Context: {json.dumps(property_data.get('market_context', {}))}
                Investment Metrics: {json.dumps(property_data.get('investment_metrics', {}))}
                Property Classification: {json.dumps(property_data.get('property_classification', {}))}
                Location Intelligence: {json.dumps(property_data.get('location_intelligence', {}))}
                """
                
                documents.append(doc_text)
                metadatas.append({
                    'source': 'property_listing',
                    'address': property_data.get('address', ''),
                    'area': property_data.get('area', ''),
                    'property_type': property_data.get('property_type', ''),
                    'price_range': self._get_price_range(property_data.get('price_aed', 0)),
                    'bedrooms': property_data.get('bedrooms', 0),
                    'price_class': property_data.get('property_classification', {}).get('price_class', 'Unknown'),
                    'investment_grade': property_data.get('investment_metrics', {}).get('investment_grade', 'Unknown')
                })
                ids.append(f"property_{i}")
            
            collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            self.logger.info(f"Successfully stored {len(properties)} properties in ChromaDB")
            return True
            
        except Exception as e:
            self.logger.error(f"Error storing properties in ChromaDB: {e}")
            return False
    
    def store_market_data_postgres(self, market_data: List[Dict[str, Any]]) -> bool:
        """Store market intelligence data in PostgreSQL"""
        try:
            cursor = self.pg_conn.cursor()
            
            for data in market_data:
                query = """
                INSERT INTO market_intelligence (
                    area, market_trend, average_price_per_sqft, rental_yield,
                    demand_level, market_volatility, investment_grade,
                    appreciation_rate, data_source, collected_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                ) ON CONFLICT (area) DO UPDATE SET
                    market_trend = EXCLUDED.market_trend,
                    average_price_per_sqft = EXCLUDED.average_price_per_sqft,
                    rental_yield = EXCLUDED.rental_yield,
                    demand_level = EXCLUDED.demand_level,
                    market_volatility = EXCLUDED.market_volatility,
                    investment_grade = EXCLUDED.investment_grade,
                    appreciation_rate = EXCLUDED.appreciation_rate,
                    collected_at = EXCLUDED.collected_at
                """
                
                cursor.execute(query, (
                    data.get('area'),
                    data.get('market_trend'),
                    data.get('average_price_per_sqft'),
                    data.get('rental_yield'),
                    data.get('demand_level'),
                    data.get('market_volatility'),
                    data.get('investment_grade'),
                    data.get('appreciation_rate'),
                    data.get('data_source', 'pipeline'),
                    datetime.now().isoformat()
                ))
            
            self.pg_conn.commit()
            self.logger.info(f"Successfully stored {len(market_data)} market data records in PostgreSQL")
            return True
            
        except Exception as e:
            self.logger.error(f"Error storing market data in PostgreSQL: {e}")
            if self.pg_conn:
                self.pg_conn.rollback()
            return False
    
    def store_market_data_chroma(self, market_data: List[Dict[str, Any]]) -> bool:
        """Store market intelligence data in ChromaDB"""
        try:
            collection = self.chroma_client.get_or_create_collection("market_intelligence")
            
            documents = []
            metadatas = []
            ids = []
            
            for i, data in enumerate(market_data):
                doc_text = f"""
                Market Intelligence for {data.get('area', '')}:
                Market Trend: {data.get('market_trend', '')}
                Average Price per Sqft: {data.get('average_price_per_sqft', '')} AED
                Rental Yield: {data.get('rental_yield', '')}%
                Demand Level: {data.get('demand_level', '')}
                Market Volatility: {data.get('market_volatility', '')}
                Investment Grade: {data.get('investment_grade', '')}
                Appreciation Rate: {data.get('appreciation_rate', '')}%
                """
                
                documents.append(doc_text)
                metadatas.append({
                    'source': 'market_intelligence',
                    'area': data.get('area', ''),
                    'data_type': 'market_data',
                    'investment_grade': data.get('investment_grade', ''),
                    'demand_level': data.get('demand_level', '')
                })
                ids.append(f"market_{i}")
            
            collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            self.logger.info(f"Successfully stored {len(market_data)} market data records in ChromaDB")
            return True
            
        except Exception as e:
            self.logger.error(f"Error storing market data in ChromaDB: {e}")
            return False
    
    def get_properties_by_role(self, role: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Get properties based on user role and access permissions"""
        try:
            cursor = self.pg_conn.cursor()
            
            # Base query
            query = "SELECT * FROM enhanced_properties WHERE 1=1"
            params = []
            
            # Apply role-based filtering
            if role == 'client':
                # Clients see limited information
                query = """
                SELECT 
                    property_type, area, bedrooms, bathrooms, square_feet,
                    price_per_sqft, market_context, property_classification,
                    location_intelligence
                FROM enhanced_properties WHERE 1=1
                """
            elif role == 'agent':
                # Agents see most information but not full addresses
                query = """
                SELECT 
                    SUBSTRING(address, 1, 50) as address_preview,
                    price_aed, bedrooms, bathrooms, square_feet,
                    property_type, area, developer, amenities,
                    price_per_sqft, market_context, investment_metrics,
                    property_classification, location_intelligence
                FROM enhanced_properties WHERE 1=1
                """
            elif role == 'listing_agent':
                # Listing agents see full information
                query = "SELECT * FROM enhanced_properties WHERE 1=1"
            elif role == 'manager':
                # Managers see everything
                query = "SELECT * FROM enhanced_properties WHERE 1=1"
            else:
                # Default to client view
                query = """
                SELECT 
                    property_type, area, bedrooms, bathrooms, square_feet,
                    price_per_sqft, market_context, property_classification
                FROM enhanced_properties WHERE 1=1
                """
            
            # Apply filters
            if filters:
                if filters.get('area'):
                    query += " AND area = %s"
                    params.append(filters['area'])
                
                if filters.get('property_type'):
                    query += " AND property_type = %s"
                    params.append(filters['property_type'])
                
                if filters.get('min_price'):
                    query += " AND price_aed >= %s"
                    params.append(filters['min_price'])
                
                if filters.get('max_price'):
                    query += " AND price_aed <= %s"
                    params.append(filters['max_price'])
                
                if filters.get('min_bedrooms'):
                    query += " AND bedrooms >= %s"
                    params.append(filters['min_bedrooms'])
                
                if filters.get('max_bedrooms'):
                    query += " AND bedrooms <= %s"
                    params.append(filters['max_bedrooms'])
            
            # Add ordering
            query += " ORDER BY enriched_at DESC"
            
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                result = dict(zip(columns, row))
                
                # Parse JSON fields
                for field in ['market_context', 'investment_metrics', 'property_classification', 
                             'location_intelligence', 'validation_flags', 'amenities']:
                    if field in result and result[field]:
                        try:
                            result[field] = json.loads(result[field])
                        except:
                            pass
                
                results.append(result)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error retrieving properties: {e}")
            return []
    
    def search_properties_semantic(self, query: str, role: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search properties using semantic search in ChromaDB"""
        try:
            collection = self.chroma_client.get_collection("properties")
            
            # Apply role-based filtering in metadata
            where_filter = {}
            if role == 'client':
                where_filter = {"price_class": {"$in": ["Affordable", "Mid-Market"]}}
            elif role == 'agent':
                where_filter = {"price_class": {"$in": ["Affordable", "Mid-Market", "Luxury"]}}
            
            results = collection.query(
                query_texts=[query],
                n_results=limit,
                where=where_filter if where_filter else None
            )
            
            # Convert results to property data
            properties = []
            if results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                    properties.append({
                        'document': doc,
                        'metadata': metadata,
                        'distance': results['distances'][0][i] if results['distances'] else 0
                    })
            
            return properties
            
        except Exception as e:
            self.logger.error(f"Error in semantic search: {e}")
            return []
    
    def _get_price_range(self, price: float) -> str:
        """Categorize price into range"""
        if price < 1000000:
            return 'Under 1M'
        elif price < 3000000:
            return '1M-3M'
        elif price < 10000000:
            return '3M-10M'
        else:
            return 'Over 10M'
    
    def create_tables_if_not_exist(self):
        """Create necessary tables if they don't exist"""
        try:
            cursor = self.pg_conn.cursor()
            
            # Enhanced Properties table (separate from original properties table)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS enhanced_properties (
                    id SERIAL PRIMARY KEY,
                    address VARCHAR(255) UNIQUE NOT NULL,
                    price_aed DECIMAL(15,2),
                    bedrooms INTEGER,
                    bathrooms INTEGER,
                    square_feet INTEGER,
                    property_type VARCHAR(100),
                    area VARCHAR(100),
                    developer VARCHAR(100),
                    completion_date DATE,
                    view VARCHAR(100),
                    amenities JSONB,
                    service_charges DECIMAL(10,2),
                    agent VARCHAR(100),
                    agency VARCHAR(100),
                    price_per_sqft DECIMAL(10,2),
                    market_context JSONB,
                    investment_metrics JSONB,
                    property_classification JSONB,
                    location_intelligence JSONB,
                    validation_flags JSONB,
                    cleaned_at TIMESTAMP,
                    enriched_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Market intelligence table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS market_intelligence (
                    id SERIAL PRIMARY KEY,
                    area VARCHAR(100) UNIQUE NOT NULL,
                    market_trend VARCHAR(50),
                    average_price_per_sqft DECIMAL(10,2),
                    rental_yield DECIMAL(5,2),
                    demand_level VARCHAR(50),
                    market_volatility VARCHAR(50),
                    investment_grade VARCHAR(10),
                    appreciation_rate DECIMAL(5,2),
                    data_source VARCHAR(100),
                    collected_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Processing logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS processing_logs (
                    id SERIAL PRIMARY KEY,
                    source_file VARCHAR(255),
                    records_processed INTEGER,
                    records_stored INTEGER,
                    processing_time DECIMAL(10,2),
                    status VARCHAR(50),
                    errors JSONB,
                    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            self.pg_conn.commit()
            self.logger.info("Database tables created successfully")
            
        except Exception as e:
            self.logger.error(f"Error creating tables: {e}")
            if self.pg_conn:
                self.pg_conn.rollback()
    
    def log_processing_result(self, source_file: str, records_processed: int, 
                            records_stored: int, processing_time: float, 
                            status: str, errors: List[str] = None):
        """Log processing results"""
        try:
            cursor = self.pg_conn.cursor()
            
            cursor.execute("""
                INSERT INTO processing_logs (
                    source_file, records_processed, records_stored,
                    processing_time, status, errors
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                source_file, records_processed, records_stored,
                processing_time, status, json.dumps(errors or [])
            ))
            
            self.pg_conn.commit()
            
        except Exception as e:
            self.logger.error(f"Error logging processing result: {e}")
            if self.pg_conn:
                self.pg_conn.rollback()
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics"""
        try:
            cursor = self.pg_conn.cursor()
            
            # Get total properties
            cursor.execute("SELECT COUNT(*) FROM enhanced_properties")
            total_properties = cursor.fetchone()[0]
            
            # Get recent processing stats
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_runs,
                    AVG(processing_time) as avg_processing_time,
                    SUM(records_processed) as total_processed,
                    SUM(records_stored) as total_stored
                FROM processing_logs 
                WHERE processed_at >= CURRENT_DATE - INTERVAL '7 days'
            """)
            
            stats = cursor.fetchone()
            
            return {
                'total_properties': total_properties,
                'recent_runs': stats[0] or 0,
                'avg_processing_time': float(stats[1] or 0),
                'total_processed_week': stats[2] or 0,
                'total_stored_week': stats[3] or 0
            }
            
        except Exception as e:
            self.logger.error(f"Error getting processing stats: {e}")
            return {}
    
    def close_connections(self):
        """Close database connections"""
        if self.pg_conn:
            self.pg_conn.close()
        self.logger.info("Database connections closed")
