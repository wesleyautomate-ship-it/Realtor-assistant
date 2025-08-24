#!/usr/bin/env python3
"""
Test script for Database Queries with Dubai-specific data
Tests the new database tables and queries
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

class DatabaseQueryTester:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/real_estate_db")
        self.engine = create_engine(self.db_url)
        
    def test_dubai_database_queries(self):
        """Test Dubai-specific database queries"""
        logger.info("🧪 Testing Dubai Database Queries...")
        
        try:
            # Test 1: Market Analysis Queries
            self.test_market_analysis_queries()
            
            # Test 2: Investment Insights Queries
            self.test_investment_insights_queries()
            
            # Test 3: Developer Information Queries
            self.test_developer_queries()
            
            # Test 4: Regulatory Information Queries
            self.test_regulatory_queries()
            
            # Test 5: Neighborhood Profile Queries
            self.test_neighborhood_queries()
            
            # Test 6: Complex Cross-Table Queries
            self.test_complex_queries()
            
            logger.info("🎉 Dubai Database Query Tests Completed Successfully!")
            
        except Exception as e:
            logger.error(f"❌ Database Query Tests Failed: {e}")
            raise
    
    def test_market_analysis_queries(self):
        """Test market analysis queries"""
        logger.info("📊 Testing Market Analysis Queries...")
        
        try:
            with self.engine.connect() as conn:
                # Query 1: Get average prices by neighborhood
                query1 = """
                SELECT neighborhood, 
                       AVG(avg_price_per_sqft) as avg_price,
                       AVG(rental_yield) as avg_yield,
                       SUM(transaction_volume) as total_transactions
                FROM market_data 
                GROUP BY neighborhood 
                ORDER BY avg_price DESC
                """
                result1 = conn.execute(text(query1))
                market_data = result1.fetchall()
                logger.info(f"✅ Market analysis query returned {len(market_data)} neighborhoods")
                
                # Query 2: Get market trends
                query2 = """
                SELECT neighborhood, property_type, market_trend, 
                       price_change_percent, rental_yield
                FROM market_data 
                WHERE market_trend = 'rising'
                ORDER BY price_change_percent DESC
                """
                result2 = conn.execute(text(query2))
                trends_data = result2.fetchall()
                logger.info(f"✅ Market trends query returned {len(trends_data)} records")
                
                # Query 3: Get foreign investment data
                query3 = """
                SELECT neighborhood, foreign_investment_percentage, 
                       off_plan_percentage, transaction_volume
                FROM market_data 
                ORDER BY foreign_investment_percentage DESC
                """
                result3 = conn.execute(text(query3))
                investment_data = result3.fetchall()
                logger.info(f"✅ Foreign investment query returned {len(investment_data)} records")
                
        except Exception as e:
            logger.error(f"❌ Market analysis queries failed: {e}")
            raise
    
    def test_investment_insights_queries(self):
        """Test investment insights queries"""
        logger.info("💰 Testing Investment Insights Queries...")
        
        try:
            with self.engine.connect() as conn:
                # Query 1: Get Golden Visa opportunities
                query1 = """
                SELECT title, roi_projection, investment_amount_min, 
                       investment_amount_max, risk_level
                FROM investment_insights 
                WHERE category = 'golden_visa'
                ORDER BY roi_projection DESC
                """
                result1 = conn.execute(text(query1))
                golden_visa_data = result1.fetchall()
                logger.info(f"✅ Golden Visa query returned {len(golden_visa_data)} opportunities")
                
                # Query 2: Get high ROI opportunities
                query2 = """
                SELECT title, category, roi_projection, risk_level, 
                       target_audience
                FROM investment_insights 
                WHERE roi_projection > 6.0
                ORDER BY roi_projection DESC
                """
                result2 = conn.execute(text(query2))
                high_roi_data = result2.fetchall()
                logger.info(f"✅ High ROI query returned {len(high_roi_data)} opportunities")
                
                # Query 3: Get investment requirements
                query3 = """
                SELECT title, requirements, key_benefits, 
                       investment_amount_min, investment_amount_max
                FROM investment_insights 
                ORDER BY investment_amount_min ASC
                """
                result3 = conn.execute(text(query3))
                requirements_data = result3.fetchall()
                logger.info(f"✅ Investment requirements query returned {len(requirements_data)} records")
                
        except Exception as e:
            logger.error(f"❌ Investment insights queries failed: {e}")
            raise
    
    def test_developer_queries(self):
        """Test developer information queries"""
        logger.info("🏢 Testing Developer Queries...")
        
        try:
            with self.engine.connect() as conn:
                # Query 1: Get top developers by market share
                query1 = """
                SELECT name, market_share, reputation_score, 
                       financial_strength, total_projects
                FROM developers 
                ORDER BY market_share DESC
                """
                result1 = conn.execute(text(query1))
                top_developers = result1.fetchall()
                logger.info(f"✅ Top developers query returned {len(top_developers)} developers")
                
                # Query 2: Get developer specialties
                query2 = """
                SELECT name, specialties, key_projects, type
                FROM developers 
                WHERE market_share > 5.0
                ORDER BY reputation_score DESC
                """
                result2 = conn.execute(text(query2))
                specialties_data = result2.fetchall()
                logger.info(f"✅ Developer specialties query returned {len(specialties_data)} records")
                
                # Query 3: Get high-reputation developers
                query3 = """
                SELECT name, reputation_score, financial_strength, 
                       avg_project_value, total_projects
                FROM developers 
                WHERE reputation_score > 8.5
                ORDER BY reputation_score DESC
                """
                result3 = conn.execute(text(query3))
                high_reputation = result3.fetchall()
                logger.info(f"✅ High reputation developers query returned {len(high_reputation)} records")
                
        except Exception as e:
            logger.error(f"❌ Developer queries failed: {e}")
            raise
    
    def test_regulatory_queries(self):
        """Test regulatory information queries"""
        logger.info("📋 Testing Regulatory Queries...")
        
        try:
            with self.engine.connect() as conn:
                # Query 1: Get active regulations
                query1 = """
                SELECT law_name, enactment_date, status, 
                       impact_areas, relevant_stakeholders
                FROM regulatory_updates 
                WHERE status = 'active'
                ORDER BY enactment_date DESC
                """
                result1 = conn.execute(text(query1))
                active_regulations = result1.fetchall()
                logger.info(f"✅ Active regulations query returned {len(active_regulations)} records")
                
                # Query 2: Get Golden Visa regulations
                query2 = """
                SELECT law_name, description, key_provisions, 
                       compliance_requirements
                FROM regulatory_updates 
                WHERE law_name ILIKE '%golden visa%'
                """
                result2 = conn.execute(text(query2))
                golden_visa_regs = result2.fetchall()
                logger.info(f"✅ Golden Visa regulations query returned {len(golden_visa_regs)} records")
                
                # Query 3: Get RERA regulations
                query3 = """
                SELECT law_name, description, impact_areas, 
                       key_provisions
                FROM regulatory_updates 
                WHERE law_name ILIKE '%rera%'
                """
                result3 = conn.execute(text(query3))
                rera_regs = result3.fetchall()
                logger.info(f"✅ RERA regulations query returned {len(rera_regs)} records")
                
        except Exception as e:
            logger.error(f"❌ Regulatory queries failed: {e}")
            raise
    
    def test_neighborhood_queries(self):
        """Test neighborhood profile queries"""
        logger.info("🏘️ Testing Neighborhood Queries...")
        
        try:
            with self.engine.connect() as conn:
                # Query 1: Get neighborhood basic info
                query1 = """
                SELECT name, description, target_audience, 
                       pros, cons
                FROM neighborhood_profiles 
                ORDER BY name
                """
                result1 = conn.execute(text(query1))
                neighborhood_info = result1.fetchall()
                logger.info(f"✅ Neighborhood info query returned {len(neighborhood_info)} records")
                
                # Query 2: Get price ranges
                query2 = """
                SELECT name, price_ranges, rental_yields, 
                       market_trends
                FROM neighborhood_profiles 
                WHERE name IN ('Dubai Marina', 'Downtown Dubai')
                """
                result2 = conn.execute(text(query2))
                price_data = result2.fetchall()
                logger.info(f"✅ Price ranges query returned {len(price_data)} records")
                
                # Query 3: Get amenities and transportation
                query3 = """
                SELECT name, amenities, transportation_links, 
                       schools_hospitals
                FROM neighborhood_profiles 
                ORDER BY name
                """
                result3 = conn.execute(text(query3))
                amenities_data = result3.fetchall()
                logger.info(f"✅ Amenities query returned {len(amenities_data)} records")
                
        except Exception as e:
            logger.error(f"❌ Neighborhood queries failed: {e}")
            raise
    
    def test_complex_queries(self):
        """Test complex cross-table queries"""
        logger.info("🔍 Testing Complex Cross-Table Queries...")
        
        try:
            with self.engine.connect() as conn:
                # Query 1: Market data with developer info
                query1 = """
                SELECT md.neighborhood, md.avg_price_per_sqft, 
                       md.rental_yield, d.name as developer_name,
                       d.reputation_score
                FROM market_data md
                LEFT JOIN developers d ON md.neighborhood ILIKE '%' || d.name || '%'
                WHERE md.market_trend = 'rising'
                ORDER BY md.avg_price_per_sqft DESC
                """
                result1 = conn.execute(text(query1))
                market_dev_data = result1.fetchall()
                logger.info(f"✅ Market-Developer cross query returned {len(market_dev_data)} records")
                
                # Query 2: Investment opportunities with market data
                query2 = """
                SELECT ii.title, ii.roi_projection, ii.risk_level,
                       md.neighborhood, md.avg_price_per_sqft,
                       md.rental_yield
                FROM investment_insights ii
                CROSS JOIN market_data md
                WHERE ii.roi_projection > 6.0
                ORDER BY ii.roi_projection DESC
                LIMIT 10
                """
                result2 = conn.execute(text(query2))
                investment_market_data = result2.fetchall()
                logger.info(f"✅ Investment-Market cross query returned {len(investment_market_data)} records")
                
                # Query 3: Neighborhood profiles with market trends
                query3 = """
                SELECT np.name, np.description, np.investment_advice,
                       md.avg_price_per_sqft, md.market_trend,
                       md.price_change_percent
                FROM neighborhood_profiles np
                LEFT JOIN market_data md ON np.name = md.neighborhood
                ORDER BY md.avg_price_per_sqft DESC
                """
                result3 = conn.execute(text(query3))
                neighborhood_market_data = result3.fetchall()
                logger.info(f"✅ Neighborhood-Market cross query returned {len(neighborhood_market_data)} records")
                
        except Exception as e:
            logger.error(f"❌ Complex queries failed: {e}")
            raise
    
    def generate_query_report(self):
        """Generate a comprehensive query test report"""
        logger.info("📋 Generating Database Query Test Report...")
        
        try:
            with self.engine.connect() as conn:
                # Get table statistics
                tables = ["market_data", "regulatory_updates", "developers", "investment_insights", "neighborhood_profiles"]
                
                report = {
                    "test_timestamp": datetime.now().isoformat(),
                    "database_url": self.db_url,
                    "table_statistics": {},
                    "query_performance": {
                        "market_analysis": "PASSED",
                        "investment_insights": "PASSED",
                        "developer_queries": "PASSED",
                        "regulatory_queries": "PASSED",
                        "neighborhood_queries": "PASSED",
                        "complex_queries": "PASSED"
                    }
                }
                
                for table in tables:
                    count_query = f"SELECT COUNT(*) FROM {table}"
                    result = conn.execute(text(count_query))
                    count = result.fetchone()[0]
                    report["table_statistics"][table] = count
                
                # Print report
                logger.info("📊 Database Query Test Report:")
                logger.info("=" * 50)
                logger.info(f"Test Timestamp: {report['test_timestamp']}")
                logger.info(f"Database: {report['database_url']}")
                logger.info("\nTable Statistics:")
                for table, count in report["table_statistics"].items():
                    logger.info(f"  - {table}: {count} records")
                logger.info("\nQuery Performance:")
                for query_type, result in report["query_performance"].items():
                    logger.info(f"  - {query_type}: {result}")
                
                return report
                
        except Exception as e:
            logger.error(f"❌ Query report generation failed: {e}")
            raise

if __name__ == "__main__":
    tester = DatabaseQueryTester()
    tester.test_dubai_database_queries()
    tester.generate_query_report()
