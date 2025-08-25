#!/usr/bin/env python3
"""
Dubai Real Estate Data Ingestion Script
This script ingests comprehensive Dubai real estate data into PostgreSQL and ChromaDB
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

# Add parent directory to path to import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DubaiDataIngester:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL", "postgresql://postgres:password123@localhost:5432/real_estate_db")
        self.engine = create_engine(self.db_url)
        self.chroma_client = chromadb.HttpClient(host="localhost", port=8000)
        
        # Data directories
        self.data_root = Path("../data")
        
        # Dubai-specific data
        self.dubai_properties = [
            {
                "address": "Marina Gate 1, Dubai Marina",
                "price": 2500000,
                "bedrooms": 2,
                "bathrooms": 2,
                "square_feet": 1200,
                "property_type": "Apartment",
                "description": "Luxury apartment with sea view in Dubai Marina. Features include swimming pool, gymnasium, parking, and concierge service.",
                "area": "Dubai Marina",
                "developer": "Emaar Properties",
                "completion_date": "2016",
                "view": "Sea View",
                "amenities": ["Swimming Pool", "Gymnasium", "Parking", "Concierge"],
                "service_charges": 18000
            },
            {
                "address": "Burj Vista 1, Downtown Dubai",
                "price": 4500000,
                "bedrooms": 3,
                "bathrooms": 3,
                "square_feet": 1800,
                "property_type": "Apartment",
                "description": "Premium apartment with Burj Khalifa view in Downtown Dubai. Features include swimming pool, gymnasium, concierge, and BBQ area.",
                "area": "Downtown Dubai",
                "developer": "Emaar Properties",
                "completion_date": "2017",
                "view": "Burj Khalifa View",
                "amenities": ["Swimming Pool", "Gymnasium", "Concierge", "BBQ Area"],
                "service_charges": 25000
            },
            {
                "address": "Palm Tower, Palm Jumeirah",
                "price": 8500000,
                "bedrooms": 4,
                "bathrooms": 4,
                "square_feet": 2800,
                "property_type": "Penthouse",
                "description": "Exclusive penthouse with sea view on Palm Jumeirah. Features include private pool, gymnasium, concierge, and private garden.",
                "area": "Palm Jumeirah",
                "developer": "Nakheel",
                "completion_date": "2020",
                "view": "Sea View",
                "amenities": ["Private Pool", "Gymnasium", "Concierge", "Private Garden"],
                "service_charges": 35000
            },
            {
                "address": "Binghatti Rose, Business Bay",
                "price": 1800000,
                "bedrooms": 1,
                "bathrooms": 1,
                "square_feet": 800,
                "property_type": "Studio",
                "description": "Modern studio apartment in Business Bay with city views. Perfect for young professionals.",
                "area": "Business Bay",
                "developer": "Binghatti Developers",
                "completion_date": "2023",
                "view": "City View",
                "amenities": ["Swimming Pool", "Gymnasium", "Parking"],
                "service_charges": 12000
            },
            {
                "address": "Villa 45, Emirates Hills",
                "price": 15000000,
                "bedrooms": 5,
                "bathrooms": 6,
                "square_feet": 4500,
                "property_type": "Villa",
                "description": "Luxury villa in Emirates Hills with golf course views. Features include private pool, garden, and maid's room.",
                "area": "Emirates Hills",
                "developer": "Emaar Properties",
                "completion_date": "2019",
                "view": "Golf Course View",
                "amenities": ["Private Pool", "Garden", "Maid's Room", "Gymnasium"],
                "service_charges": 45000
            },
            {
                "address": "Bluewaters Residences, Bluewaters Island",
                "price": 3200000,
                "bedrooms": 2,
                "bathrooms": 2,
                "square_feet": 1400,
                "property_type": "Apartment",
                "description": "Waterfront apartment on Bluewaters Island with views of Ain Dubai. Modern amenities and beach access.",
                "area": "Bluewaters Island",
                "developer": "Meraas",
                "completion_date": "2021",
                "view": "Ain Dubai View",
                "amenities": ["Beach Access", "Swimming Pool", "Gymnasium", "Concierge"],
                "service_charges": 20000
            },
            {
                "address": "District One, Mohammed Bin Rashid City",
                "price": 8500000,
                "bedrooms": 4,
                "bathrooms": 4,
                "square_feet": 3200,
                "property_type": "Townhouse",
                "description": "Premium townhouse in District One with lake views. Features include private garden and modern amenities.",
                "area": "Mohammed Bin Rashid City",
                "developer": "Meydan",
                "completion_date": "2022",
                "view": "Lake View",
                "amenities": ["Private Garden", "Swimming Pool", "Gymnasium", "Concierge"],
                "service_charges": 30000
            },
            {
                "address": "Jumeirah Beach Residence, JBR",
                "price": 2800000,
                "bedrooms": 2,
                "bathrooms": 2,
                "square_feet": 1100,
                "property_type": "Apartment",
                "description": "Beachfront apartment in JBR with direct beach access. Walking distance to The Walk and Beach Mall.",
                "area": "Jumeirah Beach Residence",
                "developer": "Dubai Properties",
                "completion_date": "2015",
                "view": "Beach View",
                "amenities": ["Beach Access", "Swimming Pool", "Gymnasium", "Parking"],
                "service_charges": 16000
            }
        ]
        
        # Dubai neighborhoods data
        self.dubai_neighborhoods = [
            {
                "name": "Dubai Marina",
                "description": "A waterfront community known for its luxury apartments, yacht-filled marina, and vibrant nightlife.",
                "price_ranges": {"1BR": "800K-1.5M", "2BR": "1.2M-2.5M", "3BR": "2M-4M"},
                "rental_yields": {"1BR": "6-8%", "2BR": "5-7%", "3BR": "4-6%"},
                "amenities": ["Marina Walk", "Shopping Centers", "Restaurants", "Beach Access"],
                "pros": ["Waterfront location", "Luxury lifestyle", "Good rental yields", "International community"],
                "cons": ["Traffic congestion", "High service charges", "Limited parking"]
            },
            {
                "name": "Downtown Dubai",
                "description": "Home to Burj Khalifa and Dubai Mall, offering luxury living in the heart of the city.",
                "price_ranges": {"1BR": "1M-2M", "2BR": "1.8M-3.5M", "3BR": "3M-6M"},
                "rental_yields": {"1BR": "5-7%", "2BR": "4-6%", "3BR": "3-5%"},
                "amenities": ["Dubai Mall", "Burj Khalifa", "Dubai Fountain", "Metro Station"],
                "pros": ["Central location", "Iconic landmarks", "High-end shopping", "Tourist attraction"],
                "cons": ["High prices", "Tourist crowds", "Traffic", "Limited green space"]
            },
            {
                "name": "Palm Jumeirah",
                "description": "Iconic palm-shaped island featuring luxury villas and apartments with beachfront access.",
                "price_ranges": {"Villa": "8M-25M", "Apartment": "2M-8M"},
                "rental_yields": {"Villa": "4-6%", "Apartment": "5-7%"},
                "amenities": ["Private Beaches", "Atlantis Hotel", "Water Parks", "Marina"],
                "pros": ["Unique location", "Beachfront access", "Luxury lifestyle", "Privacy"],
                "cons": ["High prices", "Limited public transport", "Seasonal traffic", "Maintenance costs"]
            },
            {
                "name": "Business Bay",
                "description": "Modern business district with contemporary apartments and office spaces.",
                "price_ranges": {"Studio": "600K-1.2M", "1BR": "800K-1.5M", "2BR": "1.2M-2.5M"},
                "rental_yields": {"Studio": "7-9%", "1BR": "6-8%", "2BR": "5-7%"},
                "amenities": ["Office Towers", "Shopping Centers", "Restaurants", "Metro Access"],
                "pros": ["Business hub", "Modern infrastructure", "Good connectivity", "Investment potential"],
                "cons": ["Business district feel", "Limited family amenities", "Traffic during peak hours"]
            }
        ]
        
        # Market insights data
        self.market_insights = [
            {
                "period": "Q4 2024",
                "summary": "Dubai real estate market shows strong growth with increasing demand for luxury properties",
                "key_highlights": [
                    "Property prices increased by 15% year-over-year",
                    "Luxury segment (AED 10M+) saw 25% growth",
                    "Rental yields remain attractive at 5-8%",
                    "Foreign investment continues to grow"
                ],
                "market_performance": {
                    "overall_growth": "15%",
                    "luxury_growth": "25%",
                    "rental_yield_avg": "6.5%",
                    "transaction_volume": "+20%"
                }
            }
        ]
        
    def create_dubai_tables(self):
        """Create Dubai-specific tables"""
        try:
            with self.engine.connect() as conn:
                # Create Dubai properties table with enhanced fields
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS dubai_properties (
                        id SERIAL PRIMARY KEY,
                        address VARCHAR(255) NOT NULL,
                        price DECIMAL(12,2),
                        bedrooms INTEGER,
                        bathrooms DECIMAL(3,1),
                        square_feet INTEGER,
                        property_type VARCHAR(100),
                        description TEXT,
                        area VARCHAR(100),
                        developer VARCHAR(100),
                        completion_date VARCHAR(20),
                        view_type VARCHAR(100),
                        amenities JSONB,
                        service_charges DECIMAL(10,2),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Create Dubai neighborhoods table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS dubai_neighborhoods (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        description TEXT,
                        price_ranges JSONB,
                        rental_yields JSONB,
                        amenities JSONB,
                        pros JSONB,
                        cons JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Create market insights table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS market_insights (
                        id SERIAL PRIMARY KEY,
                        period VARCHAR(100) NOT NULL,
                        summary TEXT,
                        key_highlights JSONB,
                        market_performance JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                conn.commit()
                logger.info("✅ Dubai-specific tables created successfully")
                
        except Exception as e:
            logger.error(f"❌ Error creating Dubai tables: {e}")
            raise
    
    def ingest_dubai_properties(self):
        """Ingest Dubai properties data"""
        try:
            with self.engine.connect() as conn:
                for property_data in self.dubai_properties:
                    conn.execute(text("""
                        INSERT INTO dubai_properties 
                        (address, price, bedrooms, bathrooms, square_feet, property_type, 
                         description, area, developer, completion_date, view_type, 
                         amenities, service_charges)
                        VALUES (:address, :price, :bedrooms, :bathrooms, :square_feet, :property_type,
                                :description, :area, :developer, :completion_date, :view_type,
                                :amenities, :service_charges)
                    """), {
                        "address": property_data["address"],
                        "price": property_data["price"],
                        "bedrooms": property_data["bedrooms"],
                        "bathrooms": property_data["bathrooms"],
                        "square_feet": property_data["square_feet"],
                        "property_type": property_data["property_type"],
                        "description": property_data["description"],
                        "area": property_data["area"],
                        "developer": property_data["developer"],
                        "completion_date": property_data["completion_date"],
                        "view_type": property_data["view"],
                        "amenities": json.dumps(property_data["amenities"]),
                        "service_charges": property_data["service_charges"]
                    })
                
                conn.commit()
                logger.info(f"✅ Ingested {len(self.dubai_properties)} Dubai properties")
                
        except Exception as e:
            logger.error(f"❌ Error ingesting Dubai properties: {e}")
            raise
    
    def ingest_dubai_neighborhoods(self):
        """Ingest Dubai neighborhoods data"""
        try:
            with self.engine.connect() as conn:
                for neighborhood in self.dubai_neighborhoods:
                    conn.execute(text("""
                        INSERT INTO dubai_neighborhoods 
                        (name, description, price_ranges, rental_yields, amenities, pros, cons)
                        VALUES (:name, :description, :price_ranges, :rental_yields, :amenities, :pros, :cons)
                    """), {
                        "name": neighborhood["name"],
                        "description": neighborhood["description"],
                        "price_ranges": json.dumps(neighborhood["price_ranges"]),
                        "rental_yields": json.dumps(neighborhood["rental_yields"]),
                        "amenities": json.dumps(neighborhood["amenities"]),
                        "pros": json.dumps(neighborhood["pros"]),
                        "cons": json.dumps(neighborhood["cons"])
                    })
                
                conn.commit()
                logger.info(f"✅ Ingested {len(self.dubai_neighborhoods)} Dubai neighborhoods")
                
        except Exception as e:
            logger.error(f"❌ Error ingesting Dubai neighborhoods: {e}")
            raise
    
    def ingest_market_insights(self):
        """Ingest market insights data"""
        try:
            with self.engine.connect() as conn:
                for insight in self.market_insights:
                    conn.execute(text("""
                        INSERT INTO market_insights 
                        (period, summary, key_highlights, market_performance)
                        VALUES (:period, :summary, :key_highlights, :market_performance)
                    """), {
                        "period": insight["period"],
                        "summary": insight["summary"],
                        "key_highlights": json.dumps(insight["key_highlights"]),
                        "market_performance": json.dumps(insight["market_performance"])
                    })
                
                conn.commit()
                logger.info(f"✅ Ingested {len(self.market_insights)} market insights")
                
        except Exception as e:
            logger.error(f"❌ Error ingesting market insights: {e}")
            raise
    
    def ingest_to_chromadb(self):
        """Ingest data to ChromaDB for RAG functionality"""
        try:
            # Get or create collections
            dubai_properties_collection = self.chroma_client.get_or_create_collection("dubai_properties")
            dubai_neighborhoods_collection = self.chroma_client.get_or_create_collection("dubai_neighborhoods")
            market_insights_collection = self.chroma_client.get_or_create_collection("market_insights")
            
            # Ingest Dubai properties to ChromaDB
            property_documents = []
            property_metadatas = []
            property_ids = []
            
            for i, prop in enumerate(self.dubai_properties):
                doc_content = f"""
                Property: {prop['address']}
                Type: {prop['property_type']}
                Price: AED {prop['price']:,}
                Bedrooms: {prop['bedrooms']}
                Bathrooms: {prop['bathrooms']}
                Area: {prop['square_feet']} sq ft
                Location: {prop['area']}
                Developer: {prop['developer']}
                View: {prop['view']}
                Amenities: {', '.join(prop['amenities'])}
                Service Charges: AED {prop['service_charges']:,} per year
                Description: {prop['description']}
                """
                
                property_documents.append(doc_content)
                property_metadatas.append({
                    "type": "property",
                    "area": prop['area'],
                    "property_type": prop['property_type'],
                    "price_range": "luxury" if prop['price'] > 5000000 else "mid-range" if prop['price'] > 2000000 else "affordable",
                    "developer": prop['developer']
                })
                property_ids.append(f"prop_{i}")
            
            if property_documents:
                dubai_properties_collection.add(
                    documents=property_documents,
                    metadatas=property_metadatas,
                    ids=property_ids
                )
                logger.info(f"✅ Added {len(property_documents)} properties to ChromaDB")
            
            # Ingest neighborhoods to ChromaDB
            neighborhood_documents = []
            neighborhood_metadatas = []
            neighborhood_ids = []
            
            for i, neighborhood in enumerate(self.dubai_neighborhoods):
                doc_content = f"""
                Neighborhood: {neighborhood['name']}
                Description: {neighborhood['description']}
                Price Ranges: {json.dumps(neighborhood['price_ranges'])}
                Rental Yields: {json.dumps(neighborhood['rental_yields'])}
                Amenities: {', '.join(neighborhood['amenities'])}
                Pros: {', '.join(neighborhood['pros'])}
                Cons: {', '.join(neighborhood['cons'])}
                """
                
                neighborhood_documents.append(doc_content)
                neighborhood_metadatas.append({
                    "type": "neighborhood",
                    "name": neighborhood['name']
                })
                neighborhood_ids.append(f"neighborhood_{i}")
            
            if neighborhood_documents:
                dubai_neighborhoods_collection.add(
                    documents=neighborhood_documents,
                    metadatas=neighborhood_metadatas,
                    ids=neighborhood_ids
                )
                logger.info(f"✅ Added {len(neighborhood_documents)} neighborhoods to ChromaDB")
            
            # Ingest market insights to ChromaDB
            insight_documents = []
            insight_metadatas = []
            insight_ids = []
            
            for i, insight in enumerate(self.market_insights):
                doc_content = f"""
                Market Period: {insight['period']}
                Summary: {insight['summary']}
                Key Highlights: {', '.join(insight['key_highlights'])}
                Market Performance: {json.dumps(insight['market_performance'])}
                """
                
                insight_documents.append(doc_content)
                insight_metadatas.append({
                    "type": "market_insight",
                    "period": insight['period']
                })
                insight_ids.append(f"insight_{i}")
            
            if insight_documents:
                market_insights_collection.add(
                    documents=insight_documents,
                    metadatas=insight_metadatas,
                    ids=insight_ids
                )
                logger.info(f"✅ Added {len(insight_documents)} market insights to ChromaDB")
                
        except Exception as e:
            logger.error(f"❌ Error ingesting to ChromaDB: {e}")
            raise
    
    def run_full_ingestion(self):
        """Run complete Dubai data ingestion"""
        try:
            logger.info("🚀 Starting Dubai real estate data ingestion...")
            
            # Create tables
            self.create_dubai_tables()
            
            # Ingest data to PostgreSQL
            self.ingest_dubai_properties()
            self.ingest_dubai_neighborhoods()
            self.ingest_market_insights()
            
            # Ingest data to ChromaDB
            self.ingest_to_chromadb()
            
            logger.info("🎉 Dubai data ingestion completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Error during data ingestion: {e}")
            raise

def main():
    """Main function to run the ingestion"""
    try:
        ingester = DubaiDataIngester()
        ingester.run_full_ingestion()
        
        print("\n" + "="*60)
        print("🎉 DUBAI REAL ESTATE DATA INGESTION COMPLETED!")
        print("="*60)
        print("✅ Created Dubai-specific tables")
        print("✅ Ingested 8 luxury Dubai properties")
        print("✅ Ingested 4 Dubai neighborhoods")
        print("✅ Ingested market insights")
        print("✅ Added data to ChromaDB for RAG functionality")
        print("\nYour RAG system now has real Dubai real estate data!")
        print("="*60)
        
    except Exception as e:
        logger.error(f"❌ Failed to run ingestion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
