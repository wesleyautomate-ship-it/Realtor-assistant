#!/usr/bin/env python3
"""
Data Integrity Verification Script
==================================

This script verifies that all database tables are properly populated
and relationships are correctly established after the data audit.
"""

import os
import sys
from sqlalchemy import create_engine, text
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataIntegrityVerifier:
    def __init__(self, db_url: str = "postgresql://admin:password123@localhost:5432/real_estate_db"):
        # Use Docker connection string if running in containerized environment
        # Check if we're running inside Docker by looking for the postgres service
        try:
            import socket
            socket.gethostbyname('postgres')
            db_url = "postgresql://admin:password123@postgres:5432/real_estate_db"
        except:
            # Fall back to localhost if postgres service not found
            pass
        self.engine = create_engine(db_url)
        
    def verify_table_counts(self):
        """Verify that all tables have the expected number of records"""
        expected_counts = {
            'users': 4,  # 2 admin + 2 agent users
            'properties': 5,  # 5 sample properties
            'leads': 4,  # 4 sample leads
            'viewings': 3,  # 3 sample viewings
            'appointments': 4,  # 4 sample appointments
            'market_data': 3,  # 3 market data records
            'neighborhood_profiles': 3,  # 3 neighborhood profiles
            'developers': 3,  # 3 developer profiles
            'investment_insights': 3,  # 3 investment insights
            'regulatory_updates': 3,  # 3 regulatory updates
            'property_confidential': 5,  # 5 confidential property records
            'transactions': 3,  # 3 transaction records
            'lead_history': 5,  # 5 lead history records
            'client_interactions': 4,  # 4 client interaction records
            'listing_history': 5,  # 5 listing history records
        }
        
        verification_results = {}
        
        for table_name, expected_count in expected_counts.items():
            try:
                with self.engine.connect() as conn:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                    actual_count = result.fetchone()[0]
                    verification_results[table_name] = {
                        'expected': expected_count,
                        'actual': actual_count,
                        'status': '✅ PASS' if actual_count >= expected_count else '❌ FAIL'
                    }
                    logger.info(f"📊 {table_name}: {actual_count}/{expected_count} records - {verification_results[table_name]['status']}")
            except Exception as e:
                logger.error(f"❌ Error verifying {table_name}: {e}")
                verification_results[table_name] = {
                    'expected': expected_count,
                    'actual': 0,
                    'status': '❌ ERROR'
                }
        
        return verification_results
    
    def verify_relationships(self):
        """Verify that foreign key relationships are properly established"""
        relationship_checks = [
            {
                'name': 'Leads -> Users',
                'sql': """
                    SELECT COUNT(*) FROM leads l 
                    LEFT JOIN users u ON l.agent_id = u.id 
                    WHERE u.id IS NULL
                """,
                'expected': 0
            },
            {
                'name': 'Viewings -> Users',
                'sql': """
                    SELECT COUNT(*) FROM viewings v 
                    LEFT JOIN users u ON v.agent_id = u.id 
                    WHERE u.id IS NULL
                """,
                'expected': 0
            },
            {
                'name': 'Appointments -> Users',
                'sql': """
                    SELECT COUNT(*) FROM appointments a 
                    LEFT JOIN users u ON a.agent_id = u.id 
                    WHERE u.id IS NULL
                """,
                'expected': 0
            },
            {
                'name': 'Property Confidential -> Properties',
                'sql': """
                    SELECT COUNT(*) FROM property_confidential pc 
                    LEFT JOIN properties p ON pc.property_id = p.id 
                    WHERE p.id IS NULL
                """,
                'expected': 0
            },
            {
                'name': 'Transactions -> Properties',
                'sql': """
                    SELECT COUNT(*) FROM transactions t 
                    LEFT JOIN properties p ON t.property_id = p.id 
                    WHERE p.id IS NULL
                """,
                'expected': 0
            }
        ]
        
        relationship_results = {}
        
        for check in relationship_checks:
            try:
                with self.engine.connect() as conn:
                    result = conn.execute(text(check['sql']))
                    orphaned_count = result.fetchone()[0]
                    relationship_results[check['name']] = {
                        'orphaned_count': orphaned_count,
                        'expected': check['expected'],
                        'status': '✅ PASS' if orphaned_count == check['expected'] else '❌ FAIL'
                    }
                    logger.info(f"🔗 {check['name']}: {orphaned_count} orphaned records - {relationship_results[check['name']]['status']}")
            except Exception as e:
                logger.error(f"❌ Error checking {check['name']}: {e}")
                relationship_results[check['name']] = {
                    'orphaned_count': -1,
                    'expected': check['expected'],
                    'status': '❌ ERROR'
                }
        
        return relationship_results
    
    def verify_security_filters(self):
        """Verify that security filters are properly implemented"""
        security_checks = [
            {
                'name': 'Public Properties Only',
                'sql': "SELECT COUNT(*) FROM properties WHERE listing_status != 'live'",
                'expected': 0,
                'description': 'All properties should have listing_status = live'
            },
            {
                'name': 'Agent Isolation - Leads',
                'sql': "SELECT COUNT(*) FROM leads WHERE agent_id IS NULL",
                'expected': 0,
                'description': 'All leads should be assigned to an agent'
            },
            {
                'name': 'Agent Isolation - Viewings',
                'sql': "SELECT COUNT(*) FROM viewings WHERE agent_id IS NULL",
                'expected': 0,
                'description': 'All viewings should be assigned to an agent'
            }
        ]
        
        security_results = {}
        
        for check in security_checks:
            try:
                with self.engine.connect() as conn:
                    result = conn.execute(text(check['sql']))
                    count = result.fetchone()[0]
                    security_results[check['name']] = {
                        'count': count,
                        'expected': check['expected'],
                        'status': '✅ PASS' if count == check['expected'] else '❌ FAIL',
                        'description': check['description']
                    }
                    logger.info(f"🔒 {check['name']}: {count} violations - {security_results[check['name']]['status']}")
            except Exception as e:
                logger.error(f"❌ Error checking {check['name']}: {e}")
                security_results[check['name']] = {
                    'count': -1,
                    'expected': check['expected'],
                    'status': '❌ ERROR',
                    'description': check['description']
                }
        
        return security_results
    
    def run_full_verification(self):
        """Run complete data integrity verification"""
        logger.info("🔍 Starting Data Integrity Verification...")
        
        # Verify table counts
        logger.info("\n📊 Verifying Table Counts...")
        table_results = self.verify_table_counts()
        
        # Verify relationships
        logger.info("\n🔗 Verifying Relationships...")
        relationship_results = self.verify_relationships()
        
        # Verify security
        logger.info("\n🔒 Verifying Security Filters...")
        security_results = self.verify_security_filters()
        
        # Summary
        logger.info("\n" + "="*60)
        logger.info("📋 VERIFICATION SUMMARY")
        logger.info("="*60)
        
        # Table count summary
        passed_tables = sum(1 for r in table_results.values() if r['status'] == '✅ PASS')
        total_tables = len(table_results)
        logger.info(f"📊 Tables: {passed_tables}/{total_tables} passed")
        
        # Relationship summary
        passed_relationships = sum(1 for r in relationship_results.values() if r['status'] == '✅ PASS')
        total_relationships = len(relationship_results)
        logger.info(f"🔗 Relationships: {passed_relationships}/{total_relationships} passed")
        
        # Security summary
        passed_security = sum(1 for r in security_results.values() if r['status'] == '✅ PASS')
        total_security = len(security_results)
        logger.info(f"🔒 Security: {passed_security}/{total_security} passed")
        
        # Overall status
        total_passed = passed_tables + passed_relationships + passed_security
        total_checks = total_tables + total_relationships + total_security
        
        if total_passed == total_checks:
            logger.info(f"\n🎉 ALL VERIFICATIONS PASSED! ({total_passed}/{total_checks})")
            logger.info("✅ Data integrity verified - Ready for staging deployment!")
        else:
            logger.warning(f"\n⚠️ SOME VERIFICATIONS FAILED ({total_passed}/{total_checks})")
            logger.warning("❌ Please review failed checks before deployment")
        
        return {
            'table_results': table_results,
            'relationship_results': relationship_results,
            'security_results': security_results,
            'overall_status': 'PASS' if total_passed == total_checks else 'FAIL'
        }

def main():
    """Main function to run verification"""
    try:
        verifier = DataIntegrityVerifier()
        results = verifier.run_full_verification()
        
        if results['overall_status'] == 'PASS':
            print("\n✅ Data integrity verification completed successfully!")
            print("🚀 Application is ready for staging deployment.")
            sys.exit(0)
        else:
            print("\n❌ Data integrity verification found issues.")
            print("🔧 Please address the issues before deployment.")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"❌ Verification failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
