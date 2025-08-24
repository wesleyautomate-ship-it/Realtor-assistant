#!/usr/bin/env python3
"""
Data Collection Test Script
Tests the data collection pipeline end-to-end
"""

import sys
import os
import pandas as pd
import json
from datetime import datetime

# Add parent directory to path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from collectors.property_scraper import DubaiPropertyScraper
from processors.property_enricher import PropertyDataEnricher
from database.bulk_import import BulkDataImporter

class DataCollectionTester:
    def __init__(self):
        self.scraper = DubaiPropertyScraper()
        self.enricher = PropertyDataEnricher()
        self.importer = BulkDataImporter("postgresql://admin:password123@localhost:5432/real_estate_db")
    
    def test_scraper(self) -> bool:
        """Test the property scraper"""
        print("🧪 Testing Property Scraper...")
        
        try:
            # Test scraping Dubai Marina apartments (small sample)
            properties = self.scraper.scrape_dubizzle('dubai-marina', 'apartment', max_pages=1)
            
            if not properties:
                print("❌ No properties found")
                return False
            
            print(f"✅ Found {len(properties)} properties")
            
            # Test data structure
            required_fields = ['title', 'price', 'location', 'bedrooms', 'bathrooms', 'area_sqft']
            for field in required_fields:
                if field not in properties[0]:
                    print(f"❌ Missing required field: {field}")
                    return False
            
            print("✅ Data structure validation passed")
            
            # Save test data
            test_file = 'test_dubai_marina_properties.csv'
            self.scraper.save_to_csv(properties, test_file)
            print(f"✅ Test data saved to {test_file}")
            
            return True
            
        except Exception as e:
            print(f"❌ Scraper test failed: {e}")
            return False
    
    def test_enricher(self) -> bool:
        """Test the property enricher"""
        print("\n🧪 Testing Property Enricher...")
        
        try:
            # Load test data
            test_file = 'test_dubai_marina_properties.csv'
            if not os.path.exists(test_file):
                print(f"❌ Test file not found: {test_file}")
                return False
            
            df = pd.read_csv(test_file)
            print(f"✅ Loaded {len(df)} properties for enrichment")
            
            # Test enrichment
            enriched_df = self.enricher.enrich_properties(df)
            
            # Check for new columns
            new_columns = [
                'latitude', 'longitude', 'price_per_sqft', 'investment_score',
                'area_category', 'size_category', 'price_category'
            ]
            
            for col in new_columns:
                if col not in enriched_df.columns:
                    print(f"❌ Missing enriched column: {col}")
                    return False
            
            print("✅ Enrichment completed successfully")
            
            # Save enriched data
            enriched_file = 'test_enriched_properties.csv'
            self.enricher.save_enriched_data(enriched_df, enriched_file)
            print(f"✅ Enriched data saved to {enriched_file}")
            
            # Generate market report
            report = self.enricher.generate_market_report(enriched_df)
            print(f"✅ Market report generated with {len(report['by_area'])} areas")
            
            return True
            
        except Exception as e:
            print(f"❌ Enricher test failed: {e}")
            return False
    
    def test_database_import(self) -> bool:
        """Test the database import"""
        print("\n🧪 Testing Database Import...")
        
        try:
            # Create tables
            if not self.importer.create_tables():
                print("❌ Failed to create tables")
                return False
            
            print("✅ Database tables created")
            
            # Test import
            test_file = 'test_enriched_properties.csv'
            if not os.path.exists(test_file):
                print(f"❌ Test file not found: {test_file}")
                return False
            
            # Generate import report
            report = self.importer.generate_import_report(test_file)
            print(f"✅ Import report generated for {report['file_info']['total_records']} records")
            
            # Import data
            if not self.importer.import_properties(test_file):
                print("❌ Failed to import properties")
                return False
            
            print("✅ Properties imported successfully")
            
            # Verify import
            verification = self.importer.verify_import()
            print(f"✅ Import verified: {verification['record_count']} records in database")
            
            return True
            
        except Exception as e:
            print(f"❌ Database import test failed: {e}")
            return False
    
    def test_end_to_end(self) -> bool:
        """Test the complete pipeline end-to-end"""
        print("\n🚀 Testing Complete Pipeline...")
        
        try:
            # Step 1: Scrape data
            if not self.test_scraper():
                return False
            
            # Step 2: Enrich data
            if not self.test_enricher():
                return False
            
            # Step 3: Import to database
            if not self.test_database_import():
                return False
            
            print("\n🎉 All tests passed! Pipeline is working correctly.")
            return True
            
        except Exception as e:
            print(f"❌ End-to-end test failed: {e}")
            return False
    
    def generate_test_report(self) -> dict:
        """Generate a comprehensive test report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'tests': {
                'scraper': self.test_scraper(),
                'enricher': self.test_enricher(),
                'database_import': self.test_database_import()
            },
            'files_created': [],
            'data_quality': {}
        }
        
        # Check for created files
        test_files = [
            'test_dubai_marina_properties.csv',
            'test_enriched_properties.csv'
        ]
        
        for file in test_files:
            if os.path.exists(file):
                report['files_created'].append({
                    'filename': file,
                    'size_mb': os.path.getsize(file) / (1024 * 1024),
                    'created_at': datetime.fromtimestamp(os.path.getctime(file)).isoformat()
                })
        
        # Data quality metrics
        if os.path.exists('test_enriched_properties.csv'):
            df = pd.read_csv('test_enriched_properties.csv')
            report['data_quality'] = {
                'total_records': len(df),
                'valid_prices': (df['price'] > 0).sum(),
                'valid_areas': (df['area_sqft'] > 0).sum(),
                'valid_coordinates': (df['latitude'].notna() & df['longitude'].notna()).sum(),
                'avg_price': df['price'].mean(),
                'avg_area': df['area_sqft'].mean(),
                'unique_locations': df['location'].nunique()
            }
        
        return report
    
    def cleanup_test_files(self):
        """Clean up test files"""
        test_files = [
            'test_dubai_marina_properties.csv',
            'test_enriched_properties.csv'
        ]
        
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)
                print(f"🗑️ Removed test file: {file}")

def main():
    """Main function to run tests"""
    print("🧪 Dubai Real Estate Data Collection Pipeline Test")
    print("=" * 60)
    
    tester = DataCollectionTester()
    
    # Run end-to-end test
    success = tester.test_end_to_end()
    
    # Generate test report
    report = tester.generate_test_report()
    
    print("\n📊 Test Report:")
    print(json.dumps(report, indent=2))
    
    if success:
        print("\n✅ All tests passed! Your data collection pipeline is ready.")
        print("\nNext steps:")
        print("1. Run the scraper for more areas: python scripts/collectors/property_scraper.py")
        print("2. Enrich the data: python scripts/processors/property_enricher.py")
        print("3. Import to database: python scripts/database/bulk_import.py")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
    
    # Ask if user wants to clean up test files
    response = input("\nDo you want to clean up test files? (y/n): ")
    if response.lower() == 'y':
        tester.cleanup_test_files()

if __name__ == "__main__":
    main()

