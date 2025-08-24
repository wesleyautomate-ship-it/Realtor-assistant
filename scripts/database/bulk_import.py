#!/usr/bin/env python3
"""
Database Import Script
Imports collected property data into PostgreSQL database
"""

import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BulkDataImporter:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(database_url)
        
        # Define table schemas
        self.table_schemas = {
            'properties': {
                'columns': [
                    'id SERIAL PRIMARY KEY',
                    'title VARCHAR(500)',
                    'price DECIMAL(15,2)',
                    'price_currency VARCHAR(10)',
                    'location VARCHAR(200)',
                    'bedrooms INTEGER',
                    'bathrooms INTEGER',
                    'area_sqft DECIMAL(10,2)',
                    'property_type VARCHAR(100)',
                    'developer VARCHAR(200)',
                    'amenities JSONB',
                    'description TEXT',
                    'listing_url TEXT',
                    'source VARCHAR(100)',
                    'latitude DECIMAL(10,8)',
                    'longitude DECIMAL(11,8)',
                    'price_per_sqft DECIMAL(10,2)',
                    'price_per_bedroom DECIMAL(12,2)',
                    'investment_score DECIMAL(5,2)',
                    'area_category VARCHAR(50)',
                    'size_category VARCHAR(50)',
                    'price_category VARCHAR(50)',
                    'price_range VARCHAR(50)',
                    'market_position VARCHAR(50)',
                    'value_indicator VARCHAR(50)',
                    'scraped_at TIMESTAMP',
                    'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
                ]
            },
            'market_data': {
                'columns': [
                    'id SERIAL PRIMARY KEY',
                    'area_name VARCHAR(100)',
                    'property_type VARCHAR(50)',
                    'avg_price_per_sqft DECIMAL(10,2)',
                    'avg_rent_per_sqft DECIMAL(10,2)',
                    'price_change_3m DECIMAL(5,2)',
                    'price_change_6m DECIMAL(5,2)',
                    'price_change_1y DECIMAL(5,2)',
                    'rental_yield_avg DECIMAL(5,2)',
                    'days_on_market_avg INTEGER',
                    'inventory_count INTEGER',
                    'demand_score INTEGER',
                    'supply_score INTEGER',
                    'market_trend VARCHAR(20)',
                    'last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
                ]
            },
            'neighborhood_profiles': {
                'columns': [
                    'id SERIAL PRIMARY KEY',
                    'area_name VARCHAR(100)',
                    'description TEXT',
                    'amenities JSONB',
                    'transportation JSONB',
                    'safety_rating INTEGER',
                    'family_friendly_score INTEGER',
                    'investment_potential INTEGER',
                    'average_income DECIMAL(12,2)',
                    'population_density INTEGER',
                    'expat_percentage DECIMAL(5,2)',
                    'development_plans TEXT',
                    'photos JSONB',
                    'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
                ]
            }
        }
    
    def create_tables(self) -> bool:
        """
        Create database tables if they don't exist
        """
        try:
            with self.engine.connect() as conn:
                for table_name, schema in self.table_schemas.items():
                    # Check if table exists
                    result = conn.execute(text(f"""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_name = '{table_name}'
                        );
                    """))
                    
                    if not result.fetchone()[0]:
                        # Create table
                        columns_sql = ', '.join(schema['columns'])
                        create_sql = f"""
                        CREATE TABLE {table_name} (
                            {columns_sql}
                        );
                        """
                        
                        conn.execute(text(create_sql))
                        conn.commit()
                        logger.info(f"Created table: {table_name}")
                    else:
                        logger.info(f"Table {table_name} already exists")
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            return False
    
    def import_properties(self, csv_file: str, table_name: str = 'properties') -> bool:
        """
        Import properties from CSV file
        """
        try:
            logger.info(f"Importing properties from {csv_file}")
            
            # Read CSV file
            df = pd.read_csv(csv_file)
            logger.info(f"Loaded {len(df)} properties from CSV")
            
            # Clean and prepare data
            df = self._clean_property_data(df)
            
            # Import to database
            df.to_sql(table_name, self.engine, if_exists='append', index=False, method='multi')
            
            logger.info(f"Successfully imported {len(df)} properties to {table_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error importing properties: {e}")
            return False
    
    def _clean_property_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and prepare property data for import
        """
        # Create a copy to avoid modifying original
        cleaned_df = df.copy()
        
        # Handle missing values
        cleaned_df['bedrooms'] = cleaned_df['bedrooms'].fillna(0)
        cleaned_df['bathrooms'] = cleaned_df['bathrooms'].fillna(0)
        cleaned_df['area_sqft'] = cleaned_df['area_sqft'].fillna(0)
        cleaned_df['price'] = cleaned_df['price'].fillna(0)
        
        # Convert amenities to JSONB format
        if 'amenities' in cleaned_df.columns:
            cleaned_df['amenities'] = cleaned_df['amenities'].apply(
                lambda x: json.dumps(x) if isinstance(x, list) else json.dumps([])
            )
        
        # Ensure numeric columns are numeric
        numeric_columns = ['price', 'bedrooms', 'bathrooms', 'area_sqft', 'latitude', 'longitude']
        for col in numeric_columns:
            if col in cleaned_df.columns:
                cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce').fillna(0)
        
        # Handle timestamp columns
        if 'scraped_at' in cleaned_df.columns:
            cleaned_df['scraped_at'] = pd.to_datetime(cleaned_df['scraped_at'], errors='coerce')
        
        # Truncate text fields to avoid database errors
        text_columns = ['title', 'location', 'property_type', 'developer']
        for col in text_columns:
            if col in cleaned_df.columns:
                cleaned_df[col] = cleaned_df[col].astype(str).str[:200]
        
        return cleaned_df
    
    def import_market_data(self, csv_file: str) -> bool:
        """
        Import market data from CSV file
        """
        try:
            logger.info(f"Importing market data from {csv_file}")
            
            df = pd.read_csv(csv_file)
            df.to_sql('market_data', self.engine, if_exists='append', index=False)
            
            logger.info(f"Successfully imported {len(df)} market data records")
            return True
            
        except Exception as e:
            logger.error(f"Error importing market data: {e}")
            return False
    
    def import_neighborhood_profiles(self, json_file: str) -> bool:
        """
        Import neighborhood profiles from JSON file
        """
        try:
            logger.info(f"Importing neighborhood profiles from {json_file}")
            
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            df = pd.DataFrame(data)
            df.to_sql('neighborhood_profiles', self.engine, if_exists='append', index=False)
            
            logger.info(f"Successfully imported {len(df)} neighborhood profiles")
            return True
            
        except Exception as e:
            logger.error(f"Error importing neighborhood profiles: {e}")
            return False
    
    def verify_import(self, table_name: str = 'properties') -> Dict:
        """
        Verify the import by checking record counts and data quality
        """
        try:
            with self.engine.connect() as conn:
                # Get record count
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                record_count = result.fetchone()[0]
                
                # Get sample data
                result = conn.execute(text(f"SELECT * FROM {table_name} LIMIT 5"))
                sample_data = [dict(row) for row in result.fetchall()]
                
                # Get data quality metrics
                result = conn.execute(text(f"""
                    SELECT 
                        COUNT(*) as total_records,
                        COUNT(CASE WHEN price > 0 THEN 1 END) as valid_prices,
                        COUNT(CASE WHEN area_sqft > 0 THEN 1 END) as valid_areas,
                        COUNT(CASE WHEN bedrooms > 0 THEN 1 END) as valid_bedrooms,
                        AVG(price) as avg_price,
                        AVG(area_sqft) as avg_area
                    FROM {table_name}
                """))
                
                quality_metrics = dict(result.fetchone())
                
                return {
                    'table_name': table_name,
                    'record_count': record_count,
                    'sample_data': sample_data,
                    'quality_metrics': quality_metrics
                }
                
        except Exception as e:
            logger.error(f"Error verifying import: {e}")
            return {'error': str(e)}
    
    def generate_import_report(self, csv_file: str) -> Dict:
        """
        Generate a comprehensive import report
        """
        try:
            df = pd.read_csv(csv_file)
            
            report = {
                'file_info': {
                    'filename': csv_file,
                    'total_records': len(df),
                    'file_size_mb': os.path.getsize(csv_file) / (1024 * 1024)
                },
                'data_quality': {
                    'missing_prices': df['price'].isna().sum(),
                    'missing_areas': df['area_sqft'].isna().sum(),
                    'missing_bedrooms': df['bedrooms'].isna().sum(),
                    'zero_prices': (df['price'] == 0).sum(),
                    'zero_areas': (df['area_sqft'] == 0).sum()
                },
                'price_analysis': {
                    'min_price': df['price'].min(),
                    'max_price': df['price'].max(),
                    'avg_price': df['price'].mean(),
                    'median_price': df['price'].median()
                },
                'area_analysis': {
                    'min_area': df['area_sqft'].min(),
                    'max_area': df['area_sqft'].max(),
                    'avg_area': df['area_sqft'].mean(),
                    'median_area': df['area_sqft'].median()
                },
                'location_distribution': df['location'].value_counts().to_dict(),
                'property_type_distribution': df['property_type'].value_counts().to_dict()
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating import report: {e}")
            return {'error': str(e)}
    
    def backup_table(self, table_name: str, backup_suffix: str = None) -> bool:
        """
        Create a backup of the table before import
        """
        try:
            if not backup_suffix:
                backup_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            backup_table_name = f"{table_name}_backup_{backup_suffix}"
            
            with self.engine.connect() as conn:
                # Check if table exists
                result = conn.execute(text(f"""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = '{table_name}'
                    );
                """))
                
                if result.fetchone()[0]:
                    # Create backup
                    conn.execute(text(f"CREATE TABLE {backup_table_name} AS SELECT * FROM {table_name}"))
                    conn.commit()
                    logger.info(f"Created backup table: {backup_table_name}")
                    return True
                else:
                    logger.info(f"Table {table_name} doesn't exist, no backup needed")
                    return True
                    
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return False

def main():
    """
    Main function to test the importer
    """
    # Database connection
    database_url = "postgresql://admin:password123@localhost:5432/real_estate_db"
    
    # Initialize importer
    importer = BulkDataImporter(database_url)
    
    # Create tables
    print("Creating database tables...")
    if importer.create_tables():
        print("✅ Tables created successfully")
    else:
        print("❌ Error creating tables")
        return
    
    # Check for CSV files to import
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv') and 'dubai' in f.lower()]
    
    if not csv_files:
        print("No CSV files found. Please run the scraper first.")
        return
    
    # Import each CSV file
    for csv_file in csv_files:
        print(f"\nImporting {csv_file}...")
        
        # Generate import report
        report = importer.generate_import_report(csv_file)
        print(f"File contains {report['file_info']['total_records']} records")
        
        # Import data
        if importer.import_properties(csv_file):
            print(f"✅ Successfully imported {csv_file}")
            
            # Verify import
            verification = importer.verify_import()
            print(f"Verified {verification['record_count']} records in database")
        else:
            print(f"❌ Error importing {csv_file}")

if __name__ == "__main__":
    main()

