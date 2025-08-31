#!/usr/bin/env python3
"""
Import Data Inside Container Script
This script should be run inside the Docker container to import property data
"""

import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
import logging
from datetime import datetime
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ContainerDataImporter:
    def __init__(self):
        # Use the internal Docker network URL
        self.db_url = "postgresql://admin:password123@postgres:5432/real_estate_db"
        self.engine = create_engine(self.db_url)
        
    def create_properties_table(self):
        """Create the properties table with the correct schema"""
        try:
            with self.engine.connect() as conn:
                # Create properties table with schema matching property_listings.csv
                create_table_sql = """
                CREATE TABLE IF NOT EXISTS properties (
                    id SERIAL PRIMARY KEY,
                    listing_id VARCHAR(50),
                    title VARCHAR(500),
                    property_type VARCHAR(100),
                    bedrooms INTEGER,
                    bathrooms INTEGER,
                    area_sqft INTEGER,
                    price_aed DECIMAL(15,2),
                    price_per_sqft DECIMAL(10,2),
                    location VARCHAR(200),
                    building VARCHAR(200),
                    developer VARCHAR(200),
                    agent_id VARCHAR(100),
                    listing_status VARCHAR(50),
                    listing_date DATE,
                    last_updated DATE,
                    views_count INTEGER,
                    furnished BOOLEAN,
                    parking_spaces INTEGER,
                    balcony BOOLEAN,
                    gym_access BOOLEAN,
                    pool_access BOOLEAN,
                    security BOOLEAN,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
                
                conn.execute(text(create_table_sql))
                conn.commit()
                logger.info("✅ Properties table created successfully")
                return True
                    
        except Exception as e:
            logger.error(f"Error creating properties table: {e}")
            return False
    
    def import_property_data(self):
        """Import property_listings.csv into the database"""
        try:
            csv_file = "/app/upload_data/property_listings.csv"
            
            if not os.path.exists(csv_file):
                logger.error(f"CSV file not found: {csv_file}")
                return False
            
            logger.info(f"Reading CSV file: {csv_file}")
            df = pd.read_csv(csv_file)
            logger.info(f"Loaded {len(df)} properties from CSV")
            
            # Clean the data
            df = self._clean_data(df)
            
            # Import to database
            logger.info("Importing data to database...")
            
            # First, drop and recreate the properties table
            with self.engine.connect() as conn:
                conn.execute(text("DROP TABLE IF EXISTS properties"))
                conn.commit()
                logger.info("Dropped existing properties table")
            
            # Recreate the table
            self.create_properties_table()
            
            # Import new data in batches to avoid parameter limit
            batch_size = 100
            for i in range(0, len(df), batch_size):
                batch = df.iloc[i:i+batch_size]
                logger.info(f"Importing batch {i//batch_size + 1}/{(len(df) + batch_size - 1)//batch_size}")
                batch.to_sql('properties', self.engine, if_exists='append', index=False, method='multi')
            
            logger.info(f"✅ Successfully imported {len(df)} properties to database")
            return True
            
        except Exception as e:
            logger.error(f"Error importing properties: {e}")
            return False
    
    def _clean_data(self, df):
        """Clean and prepare the data for import"""
        try:
            # Remove any duplicate rows
            df = df.drop_duplicates()
            
            # Handle missing values
            df = df.fillna({
                'title': 'Untitled Property',
                'property_type': 'Unknown',
                'bedrooms': 0,
                'bathrooms': 0,
                'area_sqft': 0,
                'price_aed': 0,
                'price_per_sqft': 0,
                'location': 'Location not specified',
                'building': '',
                'developer': '',
                'agent_id': '',
                'listing_status': 'active',
                'description': 'No description available',
                'furnished': False,
                'parking_spaces': 0,
                'balcony': False,
                'gym_access': False,
                'pool_access': False,
                'security': False,
                'views_count': 0
            })
            
            # Convert numeric columns
            numeric_columns = ['bedrooms', 'bathrooms', 'area_sqft', 'price_aed', 'price_per_sqft', 'parking_spaces', 'views_count']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            # Ensure bedrooms and bathrooms are integers
            if 'bedrooms' in df.columns:
                df['bedrooms'] = df['bedrooms'].astype(int)
            if 'bathrooms' in df.columns:
                df['bathrooms'] = df['bathrooms'].astype(int)
            if 'parking_spaces' in df.columns:
                df['parking_spaces'] = df['parking_spaces'].astype(int)
            if 'views_count' in df.columns:
                df['views_count'] = df['views_count'].astype(int)
            
            # Convert boolean columns
            boolean_columns = ['furnished', 'balcony', 'gym_access', 'pool_access', 'security']
            for col in boolean_columns:
                if col in df.columns:
                    df[col] = df[col].astype(bool)
            
            # Convert date columns
            date_columns = ['listing_date', 'last_updated']
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
            
            logger.info(f"Cleaned data: {len(df)} properties")
            return df
            
        except Exception as e:
            logger.error(f"Error cleaning data: {e}")
            return df
    
    def verify_import(self):
        """Verify the imported data"""
        try:
            with self.engine.connect() as conn:
                # Get total count
                result = conn.execute(text("SELECT COUNT(*) FROM properties"))
                total_count = result.fetchone()[0]
                
                # Get sample data
                result = conn.execute(text("SELECT listing_id, title, location, price_aed, bedrooms, bathrooms FROM properties LIMIT 5"))
                sample_data = result.fetchall()
                
                logger.info(f"Total properties in database: {total_count}")
                logger.info("Sample data:")
                for row in sample_data:
                    print(f"  - {row}")
                
                return {
                    'total_count': total_count,
                    'sample_data': sample_data
                }
                
        except Exception as e:
            logger.error(f"Error verifying import: {e}")
            return None

def main():
    """Main function"""
    print("🚀 Starting Container Data Import")
    print("=" * 50)
    
    importer = ContainerDataImporter()
    
    # Create properties table
    print("\n🔨 Creating properties table...")
    if importer.create_properties_table():
        print("✅ Properties table created successfully!")
        
        # Import property data
        print("\n📥 Importing property data...")
        if importer.import_property_data():
            print("✅ Property data imported successfully!")
            
            # Verify import
            print("\n🔍 Verifying import...")
            verification = importer.verify_import()
            if verification:
                print(f"✅ Verified {verification['total_count']} properties in database")
            else:
                print("❌ Verification failed")
        else:
            print("❌ Property data import failed")
    else:
        print("❌ Failed to create properties table")
    
    print("\n🎉 Container data import completed!")

if __name__ == "__main__":
    main()
