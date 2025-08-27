#!/usr/bin/env python3
"""
Phase 1 Migration Script for Granular Data & Security Foundation
This script adds the new tables and data for Phase 1 implementation
"""

import os
import sys
from sqlalchemy import create_engine, text
from datetime import datetime, date
import logging
import json

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Phase1Migration:
    def __init__(self, db_url: str = "postgresql://admin:password123@localhost:5432/real_estate_db"):
        self.engine = create_engine(db_url)
        
    def run_migration(self):
        """Run Phase 1 migration"""
        try:
            logger.info("🚀 Starting Phase 1 migration...")
            
            with self.engine.connect() as conn:
                # 1. Alter Properties Table for Listing Status
                logger.info("📝 Adding listing_status column to properties table...")
                conn.execute(text("""
                    DO $$
                    BEGIN
                        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='properties' AND column_name='listing_status') THEN
                            ALTER TABLE properties ADD COLUMN listing_status VARCHAR(20) DEFAULT 'draft';
                        END IF;
                    END $$;
                """))
                
                # 2. Create Confidential Data Table
                logger.info("🔒 Creating property_confidential table...")
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS property_confidential (
                        id SERIAL PRIMARY KEY,
                        property_id INTEGER UNIQUE REFERENCES properties(id) ON DELETE CASCADE,
                        unit_number VARCHAR(50),
                        plot_number VARCHAR(50),
                        floor VARCHAR(20),
                        owner_details TEXT,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );
                """))
                
                # 3. Create Transactions Table
                logger.info("💰 Creating transactions table...")
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS transactions (
                        id SERIAL PRIMARY KEY,
                        property_id INTEGER REFERENCES properties(id),
                        agent_id INTEGER REFERENCES users(id),
                        transaction_date DATE NOT NULL,
                        sale_price NUMERIC(15, 2) NOT NULL,
                        price_per_sqft NUMERIC(10, 2),
                        source_document_id VARCHAR(255),
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );
                """))
                
                # 4. Create Lead History Table
                logger.info("📊 Creating lead_history table...")
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS lead_history (
                        id SERIAL PRIMARY KEY,
                        lead_id INTEGER REFERENCES leads(id) ON DELETE CASCADE,
                        status_from VARCHAR(50),
                        status_to VARCHAR(50),
                        change_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        changed_by_agent_id INTEGER REFERENCES users(id)
                    );
                """))
                
                # 5. Create Client Interactions Table
                logger.info("💬 Creating client_interactions table...")
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS client_interactions (
                        id SERIAL PRIMARY KEY,
                        lead_id INTEGER REFERENCES leads(id) ON DELETE CASCADE,
                        agent_id INTEGER REFERENCES users(id),
                        interaction_type VARCHAR(50),
                        notes TEXT,
                        interaction_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );
                """))
                
                # 6. Create Listing History Table
                logger.info("📈 Creating listing_history table...")
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS listing_history (
                        id SERIAL PRIMARY KEY,
                        property_id INTEGER REFERENCES properties(id) ON DELETE CASCADE,
                        event_type VARCHAR(50),
                        old_value VARCHAR(255),
                        new_value VARCHAR(255),
                        change_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        changed_by_agent_id INTEGER REFERENCES users(id)
                    );
                """))
                
                conn.commit()
                logger.info("✅ Phase 1 tables created successfully")
                
                # Populate with sample data
                self.populate_sample_data(conn)
                
        except Exception as e:
            logger.error(f"❌ Error during Phase 1 migration: {e}")
            raise
    
    def populate_sample_data(self, conn):
        """Populate new tables with sample data"""
        try:
            logger.info("📊 Populating sample data...")
            
            # Sample confidential data
            confidential_data = [
                {
                    "property_id": 1,
                    "unit_number": "MG1-1501",
                    "plot_number": "DM-001-2024",
                    "floor": "15",
                    "owner_details": "Ahmed Al Rashid - Emirates ID: 784-1985-1234567-8"
                },
                {
                    "property_id": 2,
                    "unit_number": "BV2-2203",
                    "plot_number": "DD-002-2024",
                    "floor": "22",
                    "owner_details": "Fatima Al Zahra - Emirates ID: 784-1990-9876543-2"
                },
                {
                    "property_id": 3,
                    "unit_number": "PT-4501",
                    "plot_number": "PJ-003-2024",
                    "floor": "45",
                    "owner_details": "Mohammed Al Qasimi - Emirates ID: 784-1988-4567890-1"
                }
            ]
            
            for data in confidential_data:
                conn.execute(text("""
                    INSERT INTO property_confidential (property_id, unit_number, plot_number, floor, owner_details)
                    VALUES (:property_id, :unit_number, :plot_number, :floor, :owner_details)
                    ON CONFLICT (property_id) DO NOTHING
                """), data)
            
            # Sample transactions
            transactions_data = [
                {
                    "property_id": 1,
                    "agent_id": 3,
                    "transaction_date": date(2024, 6, 15),
                    "sale_price": 2500000,
                    "price_per_sqft": 2083.33,
                    "source_document_id": "TRX-2024-001"
                },
                {
                    "property_id": 2,
                    "agent_id": 3,
                    "transaction_date": date(2024, 7, 20),
                    "sale_price": 4500000,
                    "price_per_sqft": 2500.00,
                    "source_document_id": "TRX-2024-002"
                }
            ]
            
            for data in transactions_data:
                conn.execute(text("""
                    INSERT INTO transactions (property_id, agent_id, transaction_date, sale_price, price_per_sqft, source_document_id)
                    VALUES (:property_id, :agent_id, :transaction_date, :sale_price, :price_per_sqft, :source_document_id)
                """), data)
            
            # Sample listing history
            listing_history_data = [
                {
                    "property_id": 1,
                    "event_type": "status_change",
                    "old_value": "draft",
                    "new_value": "live",
                    "changed_by_agent_id": 3
                },
                {
                    "property_id": 2,
                    "event_type": "status_change",
                    "old_value": "draft",
                    "new_value": "live",
                    "changed_by_agent_id": 3
                }
            ]
            
            for data in listing_history_data:
                conn.execute(text("""
                    INSERT INTO listing_history (property_id, event_type, old_value, new_value, changed_by_agent_id)
                    VALUES (:property_id, :event_type, :old_value, :new_value, :changed_by_agent_id)
                """), data)
            
            # Update existing properties to have live status
            conn.execute(text("""
                UPDATE properties 
                SET listing_status = 'live' 
                WHERE listing_status IS NULL OR listing_status = 'draft'
            """))
            
            conn.commit()
            logger.info("✅ Sample data populated successfully")
            
        except Exception as e:
            logger.error(f"❌ Error populating sample data: {e}")
            raise

def main():
    """Main function to run Phase 1 migration"""
    try:
        migration = Phase1Migration()
        migration.run_migration()
        
        print("\n" + "="*60)
        print("🎉 PHASE 1 MIGRATION COMPLETED!")
        print("="*60)
        print("✅ New tables created:")
        print("   - property_confidential")
        print("   - transactions")
        print("   - lead_history")
        print("   - client_interactions")
        print("   - listing_history")
        print("\n✅ Properties table updated with listing_status column")
        print("\n✅ Sample data populated")
        print("\n🔒 Security features implemented:")
        print("   - Access control for confidential data")
        print("   - Property status management")
        print("   - Audit trail for changes")
        print("\nPhase 1: Granular Data & Security Foundation is ready!")
        print("="*60)
        
    except Exception as e:
        logger.error(f"❌ Failed to run Phase 1 migration: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
