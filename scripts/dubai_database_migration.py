#!/usr/bin/env python3
"""
Dubai Real Estate Database Migration Script
Phase 2: Enhanced PostgreSQL Database Schema with Dubai-specific tables and fields
"""

import os
import sys
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, Numeric, Text, Date, Boolean, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv
import logging
from datetime import datetime
from typing import List, Dict, Any
import json

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DubaiDatabaseMigration:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/real_estate_db")
        self.engine = create_engine(self.db_url)
        
    def run_migration(self):
        """Run the complete Dubai database migration"""
        logger.info("🚀 Starting Dubai Real Estate Database Migration...")
        
        try:
            # Step 1: Enhance existing properties table
            self.enhance_properties_table()
            
            # Step 2: Create new Dubai-specific tables
            self.create_market_data_table()
            self.create_regulatory_updates_table()
            self.create_developers_table()
            self.create_investment_insights_table()
            self.create_neighborhood_profiles_table()
            
            # Step 3: Insert sample data
            self.insert_sample_data()
            
            logger.info("🎉 Dubai database migration completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Migration failed: {e}")
            raise
    
    def enhance_properties_table(self):
        """Add Dubai-specific fields to the existing properties table"""
        logger.info("📝 Enhancing properties table with Dubai-specific fields...")
        
        # List of new columns to add
        new_columns = [
            ("neighborhood", "VARCHAR(100)", "Dubai Marina, Downtown, etc."),
            ("developer", "VARCHAR(100)", "Emaar, DAMAC, Nakheel, etc."),
            ("completion_date", "DATE", "Property completion date"),
            ("rental_yield", "DECIMAL(5,2)", "Annual rental yield percentage"),
            ("property_status", "VARCHAR(50)", "ready, off-plan, under-construction"),
            ("amenities", "JSONB", "Pool, gym, parking, etc."),
            ("market_segment", "VARCHAR(50)", "luxury, mid-market, affordable"),
            ("freehold_status", "BOOLEAN", "True for freehold areas"),
            ("service_charges", "DECIMAL(10,2)", "Annual service charges"),
            ("parking_spaces", "INTEGER", "Number of parking spaces")
        ]
        
        for column_name, column_type, description in new_columns:
            try:
                # Check if column already exists
                check_query = f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'properties' 
                AND column_name = '{column_name}'
                """
                
                with self.engine.connect() as conn:
                    result = conn.execute(text(check_query))
                    if not result.fetchone():
                        # Add the column
                        alter_query = f"ALTER TABLE properties ADD COLUMN {column_name} {column_type}"
                        conn.execute(text(alter_query))
                        conn.commit()
                        logger.info(f"✅ Added column '{column_name}' to properties table")
                    else:
                        logger.info(f"ℹ️ Column '{column_name}' already exists in properties table")
                        
            except Exception as e:
                logger.warning(f"⚠️ Could not add column '{column_name}': {e}")
    
    def create_market_data_table(self):
        """Create market_data table for historical analysis"""
        logger.info("📊 Creating market_data table...")
        
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS market_data (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            neighborhood VARCHAR(100),
            property_type VARCHAR(50),
            avg_price_per_sqft DECIMAL(10,2),
            transaction_volume INTEGER,
            price_change_percent DECIMAL(5,2),
            rental_yield DECIMAL(5,2),
            market_trend VARCHAR(50),
            off_plan_percentage DECIMAL(5,2),
            foreign_investment_percentage DECIMAL(5,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        try:
            with self.engine.connect() as conn:
                conn.execute(text(create_table_sql))
                conn.commit()
                logger.info("✅ Created market_data table")
        except Exception as e:
            logger.warning(f"⚠️ Could not create market_data table: {e}")
    
    def create_regulatory_updates_table(self):
        """Create regulatory_updates table"""
        logger.info("📋 Creating regulatory_updates table...")
        
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS regulatory_updates (
            id SERIAL PRIMARY KEY,
            law_name VARCHAR(200),
            enactment_date DATE,
            description TEXT,
            impact_areas TEXT[],
            relevant_stakeholders TEXT[],
            status VARCHAR(50),
            key_provisions TEXT[],
            compliance_requirements TEXT[],
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        try:
            with self.engine.connect() as conn:
                conn.execute(text(create_table_sql))
                conn.commit()
                logger.info("✅ Created regulatory_updates table")
        except Exception as e:
            logger.warning(f"⚠️ Could not create regulatory_updates table: {e}")
    
    def create_developers_table(self):
        """Create developers table"""
        logger.info("🏢 Creating developers table...")
        
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS developers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            type VARCHAR(50),
            market_share DECIMAL(5,2),
            total_projects INTEGER,
            avg_project_value DECIMAL(15,2),
            reputation_score DECIMAL(3,1),
            specialties TEXT[],
            key_projects TEXT[],
            financial_strength VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        try:
            with self.engine.connect() as conn:
                conn.execute(text(create_table_sql))
                conn.commit()
                logger.info("✅ Created developers table")
        except Exception as e:
            logger.warning(f"⚠️ Could not create developers table: {e}")
    
    def create_investment_insights_table(self):
        """Create investment_insights table"""
        logger.info("💰 Creating investment_insights table...")
        
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS investment_insights (
            id SERIAL PRIMARY KEY,
            category VARCHAR(100),
            title VARCHAR(200),
            description TEXT,
            key_benefits TEXT[],
            requirements TEXT[],
            investment_amount_min DECIMAL(15,2),
            investment_amount_max DECIMAL(15,2),
            roi_projection DECIMAL(5,2),
            risk_level VARCHAR(50),
            target_audience TEXT[],
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        try:
            with self.engine.connect() as conn:
                conn.execute(text(create_table_sql))
                conn.commit()
                logger.info("✅ Created investment_insights table")
        except Exception as e:
            logger.warning(f"⚠️ Could not create investment_insights table: {e}")
    
    def create_neighborhood_profiles_table(self):
        """Create neighborhood_profiles table"""
        logger.info("🏘️ Creating neighborhood_profiles table...")
        
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS neighborhood_profiles (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            description TEXT,
            location_data JSONB,
            amenities JSONB,
            price_ranges JSONB,
            rental_yields JSONB,
            market_trends JSONB,
            target_audience TEXT[],
            pros TEXT[],
            cons TEXT[],
            investment_advice TEXT,
            transportation_links TEXT[],
            schools_hospitals JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        try:
            with self.engine.connect() as conn:
                conn.execute(text(create_table_sql))
                conn.commit()
                logger.info("✅ Created neighborhood_profiles table")
        except Exception as e:
            logger.warning(f"⚠️ Could not create neighborhood_profiles table: {e}")
    
    def insert_sample_data(self):
        """Insert sample Dubai real estate data"""
        logger.info("📊 Inserting sample Dubai real estate data...")
        
        # Sample market data
        market_data = [
            {
                "date": "2025-01-01",
                "neighborhood": "Dubai Marina",
                "property_type": "apartment",
                "avg_price_per_sqft": 1800.00,
                "transaction_volume": 245,
                "price_change_percent": 8.5,
                "rental_yield": 6.2,
                "market_trend": "rising",
                "off_plan_percentage": 35.0,
                "foreign_investment_percentage": 65.0
            },
            {
                "date": "2025-01-01",
                "neighborhood": "Downtown Dubai",
                "property_type": "apartment",
                "avg_price_per_sqft": 2500.00,
                "transaction_volume": 189,
                "price_change_percent": 12.3,
                "rental_yield": 4.8,
                "market_trend": "rising",
                "off_plan_percentage": 28.0,
                "foreign_investment_percentage": 72.0
            },
            {
                "date": "2025-01-01",
                "neighborhood": "Palm Jumeirah",
                "property_type": "villa",
                "avg_price_per_sqft": 3200.00,
                "transaction_volume": 67,
                "price_change_percent": 15.7,
                "rental_yield": 5.1,
                "market_trend": "rising",
                "off_plan_percentage": 15.0,
                "foreign_investment_percentage": 85.0
            }
        ]
        
        # Sample regulatory updates
        regulatory_data = [
            {
                "law_name": "Golden Visa Property Investment",
                "enactment_date": "2019-05-20",
                "description": "Property investment of AED 2 million grants 10-year residency visa",
                "impact_areas": ["foreign_investment", "residency", "property_market"],
                "relevant_stakeholders": ["foreign_investors", "developers", "real_estate_agents"],
                "status": "active",
                "key_provisions": ["AED 2M investment", "10-year visa", "renewable"],
                "compliance_requirements": ["property_registration", "minimum_investment", "annual_renewal"]
            },
            {
                "law_name": "RERA Off-Plan Regulations",
                "enactment_date": "2007-07-16",
                "description": "Regulations for off-plan property sales and developer compliance",
                "impact_areas": ["developer_regulation", "consumer_protection", "off_plan_sales"],
                "relevant_stakeholders": ["developers", "buyers", "real_estate_agents"],
                "status": "active",
                "key_provisions": ["escrow_accounts", "project_registration", "delivery_guarantees"],
                "compliance_requirements": ["project_approval", "escrow_setup", "progress_reporting"]
            }
        ]
        
        # Sample developers data
        developers_data = [
            {
                "name": "Emaar Properties",
                "type": "government",
                "market_share": 25.5,
                "total_projects": 150,
                "avg_project_value": 2500000000.00,
                "reputation_score": 9.2,
                "specialties": ["master_planned_communities", "luxury_developments", "mixed_use"],
                "key_projects": ["Burj Khalifa", "Dubai Mall", "Dubai Marina", "Dubai Hills Estate"],
                "financial_strength": "excellent"
            },
            {
                "name": "DAMAC Properties",
                "type": "private",
                "market_share": 8.3,
                "total_projects": 85,
                "avg_project_value": 1800000000.00,
                "reputation_score": 8.7,
                "specialties": ["luxury_residences", "branded_properties", "high_end"],
                "key_projects": ["DAMAC Hills", "AKOYA Oxygen", "DAMAC Towers"],
                "financial_strength": "strong"
            },
            {
                "name": "Nakheel",
                "type": "government",
                "market_share": 12.1,
                "total_projects": 95,
                "avg_project_value": 2200000000.00,
                "reputation_score": 8.9,
                "specialties": ["waterfront_developments", "island_projects", "tourism"],
                "key_projects": ["Palm Jumeirah", "Palm Jebel Ali", "Deira Islands"],
                "financial_strength": "excellent"
            }
        ]
        
        # Sample investment insights
        investment_data = [
            {
                "category": "golden_visa",
                "title": "Golden Visa Property Investment",
                "description": "Property investment pathway to UAE residency",
                "key_benefits": ["10_year_residency", "tax_advantages", "family_inclusion"],
                "requirements": ["AED 2M investment", "freehold_property", "valid_passport"],
                "investment_amount_min": 2000000.00,
                "investment_amount_max": 50000000.00,
                "roi_projection": 8.5,
                "risk_level": "low",
                "target_audience": ["foreign_investors", "expats", "high_net_worth"]
            },
            {
                "category": "rental_investment",
                "title": "Dubai Marina Rental Investment",
                "description": "High-yield rental investment in prime location",
                "key_benefits": ["high_rental_yield", "capital_appreciation", "liquidity"],
                "requirements": ["AED 1.5M minimum", "good_credit", "down_payment"],
                "investment_amount_min": 1500000.00,
                "investment_amount_max": 8000000.00,
                "roi_projection": 6.2,
                "risk_level": "medium",
                "target_audience": ["investors", "expats", "professionals"]
            }
        ]
        
        # Sample neighborhood profiles
        neighborhood_data = [
            {
                "name": "Dubai Marina",
                "description": "Master-planned waterfront community with luxury high-rise apartments",
                "location_data": {"latitude": 25.0922, "longitude": 55.1381, "district": "Dubai Marina"},
                "amenities": {
                    "shopping": ["Marina Walk", "Dubai Marina Mall"],
                    "dining": ["Pier 7", "Marina Promenade"],
                    "recreation": ["Dubai Marina Yacht Club", "JBR Beach"],
                    "transport": ["Dubai Marina Metro Station", "Water Taxi"]
                },
                "price_ranges": {
                    "studio": {"min": 800000, "max": 1200000},
                    "1_bedroom": {"min": 1200000, "max": 2000000},
                    "2_bedroom": {"min": 2000000, "max": 3500000},
                    "3_bedroom": {"min": 3500000, "max": 6000000}
                },
                "rental_yields": {
                    "studio": 6.8,
                    "1_bedroom": 6.5,
                    "2_bedroom": 6.2,
                    "3_bedroom": 5.9
                },
                "market_trends": {
                    "price_growth": 8.5,
                    "rental_growth": 5.2,
                    "demand": "high",
                    "supply": "moderate"
                },
                "target_audience": ["young_professionals", "expats", "investors"],
                "pros": ["waterfront_location", "luxury_amenities", "metro_connected", "high_rental_yield"],
                "cons": ["traffic_congestion", "high_service_charges", "limited_parking"],
                "investment_advice": "Excellent for rental investment with strong capital appreciation potential",
                "transportation_links": ["Dubai Metro Red Line", "Water Taxi", "Bus Routes"],
                "schools_hospitals": {
                    "schools": ["Dubai British School", "Emirates International School"],
                    "hospitals": ["Medcare Hospital", "Emirates Hospital"]
                }
            },
            {
                "name": "Downtown Dubai",
                "description": "Iconic district featuring Burj Khalifa and Dubai Mall",
                "location_data": {"latitude": 25.1972, "longitude": 55.2744, "district": "Downtown Dubai"},
                "amenities": {
                    "shopping": ["Dubai Mall", "Souk Al Bahar"],
                    "dining": ["At.mosphere", "Armani Hotel Restaurants"],
                    "recreation": ["Dubai Fountain", "Burj Khalifa Observation Deck"],
                    "transport": ["Burj Khalifa/Dubai Mall Metro Station"]
                },
                "price_ranges": {
                    "studio": {"min": 1200000, "max": 1800000},
                    "1_bedroom": {"min": 1800000, "max": 3000000},
                    "2_bedroom": {"min": 3000000, "max": 5000000},
                    "3_bedroom": {"min": 5000000, "max": 10000000}
                },
                "rental_yields": {
                    "studio": 4.5,
                    "1_bedroom": 4.8,
                    "2_bedroom": 5.1,
                    "3_bedroom": 5.3
                },
                "market_trends": {
                    "price_growth": 12.3,
                    "rental_growth": 6.8,
                    "demand": "very_high",
                    "supply": "limited"
                },
                "target_audience": ["luxury_buyers", "high_net_worth", "tourists"],
                "pros": ["iconic_location", "luxury_amenities", "high_capital_appreciation", "prestige"],
                "cons": ["high_prices", "lower_rental_yield", "tourist_traffic"],
                "investment_advice": "Premium location for capital appreciation, lower rental yields but high prestige value",
                "transportation_links": ["Dubai Metro Red Line", "Dubai Tram"],
                "schools_hospitals": {
                    "schools": ["Dubai International Academy", "GEMS World Academy"],
                    "hospitals": ["Mediclinic City Hospital", "Emirates Hospital"]
                }
            }
        ]
        
        # Insert market data
        try:
            with self.engine.connect() as conn:
                for data in market_data:
                    insert_query = """
                    INSERT INTO market_data (date, neighborhood, property_type, avg_price_per_sqft, 
                                           transaction_volume, price_change_percent, rental_yield, 
                                           market_trend, off_plan_percentage, foreign_investment_percentage)
                    VALUES (:date, :neighborhood, :property_type, :avg_price_per_sqft, 
                           :transaction_volume, :price_change_percent, :rental_yield, 
                           :market_trend, :off_plan_percentage, :foreign_investment_percentage)
                    """
                    conn.execute(text(insert_query), data)
                conn.commit()
                logger.info(f"✅ Inserted {len(market_data)} market data records")
        except Exception as e:
            logger.warning(f"⚠️ Could not insert market data: {e}")
        
        # Insert regulatory data
        try:
            with self.engine.connect() as conn:
                for data in regulatory_data:
                    insert_query = """
                    INSERT INTO regulatory_updates (law_name, enactment_date, description, impact_areas,
                                                  relevant_stakeholders, status, key_provisions, compliance_requirements)
                    VALUES (:law_name, :enactment_date, :description, :impact_areas,
                           :relevant_stakeholders, :status, :key_provisions, :compliance_requirements)
                    """
                    conn.execute(text(insert_query), data)
                conn.commit()
                logger.info(f"✅ Inserted {len(regulatory_data)} regulatory records")
        except Exception as e:
            logger.warning(f"⚠️ Could not insert regulatory data: {e}")
        
        # Insert developers data
        try:
            with self.engine.connect() as conn:
                for data in developers_data:
                    insert_query = """
                    INSERT INTO developers (name, type, market_share, total_projects, avg_project_value,
                                          reputation_score, specialties, key_projects, financial_strength)
                    VALUES (:name, :type, :market_share, :total_projects, :avg_project_value,
                           :reputation_score, :specialties, :key_projects, :financial_strength)
                    """
                    conn.execute(text(insert_query), data)
                conn.commit()
                logger.info(f"✅ Inserted {len(developers_data)} developer records")
        except Exception as e:
            logger.warning(f"⚠️ Could not insert developers data: {e}")
        
        # Insert investment insights
        try:
            with self.engine.connect() as conn:
                for data in investment_data:
                    insert_query = """
                    INSERT INTO investment_insights (category, title, description, key_benefits,
                                                   requirements, investment_amount_min, investment_amount_max,
                                                   roi_projection, risk_level, target_audience)
                    VALUES (:category, :title, :description, :key_benefits,
                           :requirements, :investment_amount_min, :investment_amount_max,
                           :roi_projection, :risk_level, :target_audience)
                    """
                    conn.execute(text(insert_query), data)
                conn.commit()
                logger.info(f"✅ Inserted {len(investment_data)} investment insight records")
        except Exception as e:
            logger.warning(f"⚠️ Could not insert investment data: {e}")
        
        # Insert neighborhood profiles
        try:
            with self.engine.connect() as conn:
                for data in neighborhood_data:
                    # Convert Python dictionaries to JSON strings for JSONB columns
                    data_for_insert = {
                        "name": data["name"],
                        "description": data["description"],
                        "location_data": json.dumps(data["location_data"]),
                        "amenities": json.dumps(data["amenities"]),
                        "price_ranges": json.dumps(data["price_ranges"]),
                        "rental_yields": json.dumps(data["rental_yields"]),
                        "market_trends": json.dumps(data["market_trends"]),
                        "target_audience": data["target_audience"],
                        "pros": data["pros"],
                        "cons": data["cons"],
                        "investment_advice": data["investment_advice"],
                        "transportation_links": data["transportation_links"],
                        "schools_hospitals": json.dumps(data["schools_hospitals"])
                    }
                    
                    insert_query = """
                    INSERT INTO neighborhood_profiles (name, description, location_data, amenities,
                                                     price_ranges, rental_yields, market_trends,
                                                     target_audience, pros, cons, investment_advice,
                                                     transportation_links, schools_hospitals)
                    VALUES (:name, :description, :location_data, :amenities,
                           :price_ranges, :rental_yields, :market_trends,
                           :target_audience, :pros, :cons, :investment_advice,
                           :transportation_links, :schools_hospitals)
                    """
                    conn.execute(text(insert_query), data_for_insert)
                conn.commit()
                logger.info(f"✅ Inserted {len(neighborhood_data)} neighborhood profile records")
        except Exception as e:
            logger.warning(f"⚠️ Could not insert neighborhood data: {e}")
    
    def verify_migration(self):
        """Verify that all tables and columns were created successfully"""
        logger.info("🔍 Verifying database migration...")
        
        # List of expected tables
        expected_tables = [
            "market_data",
            "regulatory_updates", 
            "developers",
            "investment_insights",
            "neighborhood_profiles"
        ]
        
        # List of expected columns in properties table
        expected_properties_columns = [
            "neighborhood", "developer", "completion_date", "rental_yield",
            "property_status", "amenities", "market_segment", "freehold_status",
            "service_charges", "parking_spaces"
        ]
        
        try:
            with self.engine.connect() as conn:
                # Check tables
                for table_name in expected_tables:
                    check_table_query = f"""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = '{table_name}'
                    );
                    """
                    result = conn.execute(text(check_table_query))
                    if result.fetchone()[0]:
                        logger.info(f"✅ Table '{table_name}' exists")
                    else:
                        logger.warning(f"⚠️ Table '{table_name}' not found")
                
                # Check properties table columns
                for column_name in expected_properties_columns:
                    check_column_query = f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'properties' 
                    AND column_name = '{column_name}'
                    """
                    result = conn.execute(text(check_column_query))
                    if result.fetchone():
                        logger.info(f"✅ Column '{column_name}' exists in properties table")
                    else:
                        logger.warning(f"⚠️ Column '{column_name}' not found in properties table")
                
                # Count records in new tables
                for table_name in expected_tables:
                    count_query = f"SELECT COUNT(*) FROM {table_name}"
                    result = conn.execute(text(count_query))
                    count = result.fetchone()[0]
                    logger.info(f"📊 Table '{table_name}' has {count} records")
                
        except Exception as e:
            logger.error(f"❌ Verification failed: {e}")

if __name__ == "__main__":
    migration = DubaiDatabaseMigration()
    migration.run_migration()
    migration.verify_migration()
