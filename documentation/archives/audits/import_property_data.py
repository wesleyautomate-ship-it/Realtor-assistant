#!/usr/bin/env python3
"""
Import Property Data Script
Imports property_listings.csv into the database
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

class PropertyDataImporter:
    def __init__(self):
        # Use Docker database URL
        self.db_url = "postgresql://postgres:password123@localhost:5432/real_estate_db"
        self.engine = create_engine(self.db_url)
        
    def import_property_listings(self):
        """Import property_listings.csv into the database"""
        try:
            csv_file = "upload_data/property_listings.csv"
            
            if not os.path.exists(csv_file):
                logger.error(f"CSV file not found: {csv_file}")
                return False
            
            logger.info(f"Reading CSV file: {csv_file}")
            df = pd.read_csv(csv_file)
            logger.info(f"Loaded {len(df)} properties from CSV")
            
            # Display first few rows for verification
            logger.info("First 3 rows of data:")
            print(df.head(3))
            logger.info(f"Columns: {list(df.columns)}")
            
            # Clean the data
            df = self._clean_data(df)
            
            # Import to database
            logger.info("Importing data to database...")
            
            # First, clear existing data from properties table
            with self.engine.connect() as conn:
                conn.execute(text("DELETE FROM properties"))
                conn.commit()
                logger.info("Cleared existing properties data")
            
            # Import new data
            df.to_sql('properties', self.engine, if_exists='append', index=False, method='multi')
            
            logger.info(f"✅ Successfully imported {len(df)} properties to database")
            
            # Verify import
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT COUNT(*) FROM properties"))
                count = result.fetchone()[0]
                logger.info(f"Verified {count} properties in database")
            
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
                'description': 'No description available'
            })
            
            # Convert numeric columns
            numeric_columns = ['bedrooms', 'bathrooms', 'area_sqft', 'price_aed', 'price_per_sqft']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            # Ensure bedrooms and bathrooms are integers
            if 'bedrooms' in df.columns:
                df['bedrooms'] = df['bedrooms'].astype(int)
            if 'bathrooms' in df.columns:
                df['bathrooms'] = df['bathrooms'].astype(int)
            
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
                result = conn.execute(text("SELECT * FROM properties LIMIT 5"))
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
    print("🚀 Starting Property Data Import")
    print("=" * 50)
    
    importer = PropertyDataImporter()
    
    # Import property listings
    if importer.import_property_listings():
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
    
    print("\n🎉 Import process completed!")

if __name__ == "__main__":
    main()
