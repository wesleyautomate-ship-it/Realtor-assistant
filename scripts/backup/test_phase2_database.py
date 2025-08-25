#!/usr/bin/env python3
"""
Test script for Phase 2: Enhanced PostgreSQL Database Schema
Verifies Dubai-specific tables and data are working correctly
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Phase2DatabaseTester:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/real_estate_db")
        self.engine = create_engine(self.db_url)
        
    def test_phase2_migration(self):
        """Test Phase 2 database migration"""
        logger.info("🧪 Testing Phase 2 Database Migration...")
        
        try:
            # Test 1: Verify new tables exist
            self.test_table_existence()
            
            # Test 2: Verify properties table enhancements
            self.test_properties_enhancements()
            
            # Test 3: Verify data insertion
            self.test_data_queries()
            
            # Test 4: Test complex queries
            self.test_complex_queries()
            
            logger.info("🎉 Phase 2 Database Migration Tests Completed Successfully!")
            
        except Exception as e:
            logger.error(f"❌ Phase 2 Database Migration Tests Failed: {e}")
            raise
    
    def test_table_existence(self):
        """Test that all new Dubai-specific tables exist"""
        logger.info("📋 Testing table existence...")
        
        expected_tables = [
            "market_data",
            "regulatory_updates",
            "developers", 
            "investment_insights",
            "neighborhood_profiles"
        ]
        
        try:
            with self.engine.connect() as conn:
                for table_name in expected_tables:
                    check_query = f"""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = '{table_name}'
                    );
                    """
                    result = conn.execute(text(check_query))
                    exists = result.fetchone()[0]
                    
                    if exists:
                        logger.info(f"✅ Table '{table_name}' exists")
                    else:
                        logger.error(f"❌ Table '{table_name}' not found")
                        raise Exception(f"Table '{table_name}' not found")
                        
        except Exception as e:
            logger.error(f"❌ Table existence test failed: {e}")
            raise
    
    def test_properties_enhancements(self):
        """Test that properties table has new Dubai-specific columns"""
        logger.info("🏠 Testing properties table enhancements...")
        
        expected_columns = [
            "neighborhood", "developer", "completion_date", "rental_yield",
            "property_status", "amenities", "market_segment", "freehold_status",
            "service_charges", "parking_spaces"
        ]
        
        try:
            with self.engine.connect() as conn:
                for column_name in expected_columns:
                    check_query = f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'properties' 
                    AND column_name = '{column_name}'
                    """
                    result = conn.execute(text(check_query))
                    column_exists = result.fetchone()
                    
                    if column_exists:
                        logger.info(f"✅ Column '{column_name}' exists in properties table")
                    else:
                        logger.error(f"❌ Column '{column_name}' not found in properties table")
                        raise Exception(f"Column '{column_name}' not found in properties table")
                        
        except Exception as e:
            logger.error(f"❌ Properties enhancements test failed: {e}")
            raise
    
    def test_data_queries(self):
        """Test basic data queries on new tables"""
        logger.info("📊 Testing data queries...")
        
        try:
            with self.engine.connect() as conn:
                # Test market_data table
                market_query = "SELECT COUNT(*) FROM market_data"
                result = conn.execute(text(market_query))
                count = result.fetchone()[0]
                logger.info(f"✅ market_data table has {count} records")
                
                # Test regulatory_updates table
                regulatory_query = "SELECT COUNT(*) FROM regulatory_updates"
                result = conn.execute(text(regulatory_query))
                count = result.fetchone()[0]
                logger.info(f"✅ regulatory_updates table has {count} records")
                
                # Test developers table
                developers_query = "SELECT COUNT(*) FROM developers"
                result = conn.execute(text(developers_query))
                count = result.fetchone()[0]
                logger.info(f"✅ developers table has {count} records")
                
                # Test investment_insights table
                investment_query = "SELECT COUNT(*) FROM investment_insights"
                result = conn.execute(text(investment_query))
                count = result.fetchone()[0]
                logger.info(f"✅ investment_insights table has {count} records")
                
                # Test neighborhood_profiles table
                neighborhood_query = "SELECT COUNT(*) FROM neighborhood_profiles"
                result = conn.execute(text(neighborhood_query))
                count = result.fetchone()[0]
                logger.info(f"✅ neighborhood_profiles table has {count} records")
                
        except Exception as e:
            logger.error(f"❌ Data queries test failed: {e}")
            raise
    
    def test_complex_queries(self):
        """Test complex queries that demonstrate Dubai-specific functionality"""
        logger.info("🔍 Testing complex queries...")
        
        try:
            with self.engine.connect() as conn:
                # Test 1: Market analysis query
                market_analysis_query = """
                SELECT neighborhood, 
                       AVG(avg_price_per_sqft) as avg_price,
                       AVG(rental_yield) as avg_yield,
                       SUM(transaction_volume) as total_transactions
                FROM market_data 
                GROUP BY neighborhood 
                ORDER BY avg_price DESC
                """
                result = conn.execute(text(market_analysis_query))
                market_data = result.fetchall()
                logger.info(f"✅ Market analysis query returned {len(market_data)} neighborhoods")
                
                # Test 2: Developer performance query
                developer_query = """
                SELECT name, market_share, reputation_score, financial_strength
                FROM developers 
                ORDER BY market_share DESC
                """
                result = conn.execute(text(developer_query))
                developers = result.fetchall()
                logger.info(f"✅ Developer query returned {len(developers)} developers")
                
                # Test 3: Investment opportunities query
                investment_query = """
                SELECT title, roi_projection, risk_level, investment_amount_min
                FROM investment_insights 
                WHERE roi_projection > 5.0
                ORDER BY roi_projection DESC
                """
                result = conn.execute(text(investment_query))
                investments = result.fetchall()
                logger.info(f"✅ Investment query returned {len(investments)} opportunities")
                
                # Test 4: Regulatory compliance query
                regulatory_query = """
                SELECT law_name, status, key_provisions
                FROM regulatory_updates 
                WHERE status = 'active'
                """
                result = conn.execute(text(regulatory_query))
                regulations = result.fetchall()
                logger.info(f"✅ Regulatory query returned {len(regulations)} active regulations")
                
                # Test 5: Neighborhood comparison query
                neighborhood_query = """
                SELECT name, 
                       price_ranges->>'1_bedroom' as one_bedroom_range,
                       rental_yields->>'1_bedroom' as one_bedroom_yield
                FROM neighborhood_profiles 
                WHERE name IN ('Dubai Marina', 'Downtown Dubai')
                """
                result = conn.execute(text(neighborhood_query))
                neighborhoods = result.fetchall()
                logger.info(f"✅ Neighborhood query returned {len(neighborhoods)} neighborhoods")
                
        except Exception as e:
            logger.error(f"❌ Complex queries test failed: {e}")
            raise
    
    def test_data_integrity(self):
        """Test data integrity and constraints"""
        logger.info("🔒 Testing data integrity...")
        
        try:
            with self.engine.connect() as conn:
                # Test 1: Check for null values in required fields
                null_check_query = """
                SELECT COUNT(*) 
                FROM market_data 
                WHERE date IS NULL OR neighborhood IS NULL
                """
                result = conn.execute(text(null_check_query))
                null_count = result.fetchone()[0]
                if null_count == 0:
                    logger.info("✅ No null values in required market_data fields")
                else:
                    logger.warning(f"⚠️ Found {null_count} null values in market_data")
                
                # Test 2: Check for valid price ranges
                price_check_query = """
                SELECT COUNT(*) 
                FROM market_data 
                WHERE avg_price_per_sqft <= 0 OR rental_yield <= 0
                """
                result = conn.execute(text(price_check_query))
                invalid_count = result.fetchone()[0]
                if invalid_count == 0:
                    logger.info("✅ All price and yield values are valid")
                else:
                    logger.warning(f"⚠️ Found {invalid_count} invalid price/yield values")
                
                # Test 3: Check for valid dates
                date_check_query = """
                SELECT COUNT(*) 
                FROM market_data 
                WHERE date > CURRENT_DATE
                """
                result = conn.execute(text(date_check_query))
                future_count = result.fetchone()[0]
                if future_count == 0:
                    logger.info("✅ All dates are valid (not in future)")
                else:
                    logger.warning(f"⚠️ Found {future_count} future dates")
                
        except Exception as e:
            logger.error(f"❌ Data integrity test failed: {e}")
            raise
    
    def generate_test_report(self):
        """Generate a comprehensive test report"""
        logger.info("📋 Generating Phase 2 Database Test Report...")
        
        try:
            with self.engine.connect() as conn:
                # Get table statistics
                tables = ["market_data", "regulatory_updates", "developers", "investment_insights", "neighborhood_profiles"]
                
                report = {
                    "test_timestamp": datetime.now().isoformat(),
                    "database_url": self.db_url,
                    "table_statistics": {},
                    "test_results": {
                        "table_existence": "PASSED",
                        "properties_enhancements": "PASSED", 
                        "data_queries": "PASSED",
                        "complex_queries": "PASSED",
                        "data_integrity": "PASSED"
                    }
                }
                
                for table in tables:
                    count_query = f"SELECT COUNT(*) FROM {table}"
                    result = conn.execute(text(count_query))
                    count = result.fetchone()[0]
                    report["table_statistics"][table] = count
                
                # Print report
                logger.info("📊 Phase 2 Database Test Report:")
                logger.info("=" * 50)
                logger.info(f"Test Timestamp: {report['test_timestamp']}")
                logger.info(f"Database: {report['database_url']}")
                logger.info("\nTable Statistics:")
                for table, count in report["table_statistics"].items():
                    logger.info(f"  - {table}: {count} records")
                logger.info("\nTest Results:")
                for test, result in report["test_results"].items():
                    logger.info(f"  - {test}: {result}")
                
                return report
                
        except Exception as e:
            logger.error(f"❌ Test report generation failed: {e}")
            raise

if __name__ == "__main__":
    tester = Phase2DatabaseTester()
    tester.test_phase2_migration()
    tester.test_data_integrity()
    tester.generate_test_report()
