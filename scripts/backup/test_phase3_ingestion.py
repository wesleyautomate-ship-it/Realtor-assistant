#!/usr/bin/env python3
"""
Test script for Phase 3: Unified Data Ingestion Pipeline
Tests the complete data ingestion workflow with sample files
"""

import os
import sys
import tempfile
import pandas as pd
from datetime import datetime, date
import logging

# Add the scripts directory to the path
sys.path.append(os.path.dirname(__file__))

from unified_data_ingestion import UnifiedDataIngestionPipeline

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Phase3IngestionTester:
    """Test class for Phase 3 data ingestion pipeline"""
    
    def __init__(self):
        self.pipeline = UnifiedDataIngestionPipeline()
        self.test_files = []
        
    def create_sample_csv_files(self):
        """Create sample CSV files for testing"""
        logger.info("Creating sample CSV files for testing...")
        
        # Sample market data CSV
        market_data = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'neighborhood': ['Dubai Marina', 'Downtown Dubai', 'Palm Jumeirah'],
            'property_type': ['Apartment', 'Penthouse', 'Villa'],
            'avg_price_per_sqft': [1200.50, 1800.75, 2200.25],
            'transaction_volume': [45, 23, 12],
            'rental_yield': [6.5, 5.8, 7.2],
            'market_trend': ['Rising', 'Stable', 'Rising'],
            'price_change_percent': [2.5, 0.8, 3.2]
        })
        
        # Sample properties CSV
        properties_data = pd.DataFrame({
            'address': ['Marina Heights Tower 1', 'Burj Vista 2', 'Palm Tower A'],
            'price': [2500000, 4500000, 8500000],
            'bedrooms': [2, 3, 4],
            'bathrooms': [2, 3, 4],
            'neighborhood': ['Dubai Marina', 'Downtown Dubai', 'Palm Jumeirah'],
            'developer': ['Emaar Properties', 'Emaar Properties', 'Nakheel'],
            'completion_date': ['2023-12-01', '2024-06-01', '2024-03-01'],
            'rental_yield': [6.2, 5.5, 6.8],
            'property_status': ['ready', 'off-plan', 'ready'],
            'market_segment': ['mid-market', 'luxury', 'ultra-luxury']
        })
        
        # Sample regulatory updates CSV
        regulatory_data = pd.DataFrame({
            'law_name': ['Golden Visa Extension', 'RERA Compliance Update', 'Foreign Investment Law'],
            'enactment_date': ['2024-01-15', '2024-02-01', '2024-03-01'],
            'description': [
                'Extended Golden Visa eligibility for property investors',
                'Updated RERA compliance requirements for developers',
                'New foreign investment regulations for real estate'
            ],
            'status': ['Active', 'Active', 'Active'],
            'impact_areas': ['Investment', 'Development', 'Foreign Investment'],
            'key_provisions': [
                'Minimum investment reduced to AED 2M',
                'Enhanced transparency requirements',
                'Streamlined foreign investment process'
            ]
        })
        
        # Sample developers CSV
        developers_data = pd.DataFrame({
            'name': ['Emaar Properties', 'DAMAC Properties', 'Nakheel'],
            'market_share': [25.5, 8.3, 12.1],
            'reputation_score': [9.2, 7.8, 8.5],
            'financial_strength': ['Excellent', 'Good', 'Good'],
            'total_projects': [150, 85, 120],
            'avg_project_value': [5000000, 3500000, 4200000],
            'specialties': ['Luxury Development', 'Mid-Market', 'Mixed-Use'],
            'key_projects': ['Burj Khalifa', 'DAMAC Hills', 'Palm Jumeirah']
        })
        
        # Sample investment insights CSV
        investment_data = pd.DataFrame({
            'title': ['Golden Visa Investment', 'Rental Portfolio', 'Off-Plan Investment'],
            'category': ['Golden Visa', 'Rental Income', 'Capital Appreciation'],
            'roi_projection': [8.5, 6.2, 12.5],
            'investment_amount_min': [2000000, 1500000, 1000000],
            'investment_amount_max': [5000000, 3000000, 2500000],
            'risk_level': ['Low', 'Medium', 'High'],
            'target_audience': ['High Net Worth', 'Investors', 'Risk Takers'],
            'requirements': ['Minimum AED 2M', 'Property Management', 'Long-term Hold'],
            'key_benefits': ['Visa Benefits', 'Stable Income', 'High Returns']
        })
        
        # Create temporary files
        test_files = []
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            market_data.to_csv(f.name, index=False)
            test_files.append(('market_data.csv', f.name))
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            properties_data.to_csv(f.name, index=False)
            test_files.append(('properties.csv', f.name))
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            regulatory_data.to_csv(f.name, index=False)
            test_files.append(('regulatory_updates.csv', f.name))
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            developers_data.to_csv(f.name, index=False)
            test_files.append(('developers.csv', f.name))
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            investment_data.to_csv(f.name, index=False)
            test_files.append(('investment_insights.csv', f.name))
        
        self.test_files = test_files
        logger.info(f"Created {len(test_files)} sample CSV files")
        
        return test_files
    
    def test_single_file_processing(self):
        """Test processing of individual files"""
        logger.info("Testing single file processing...")
        
        results = []
        
        for file_name, file_path in self.test_files:
            logger.info(f"Testing file: {file_name}")
            
            try:
                result = self.pipeline.process_file(file_path)
                results.append({
                    'file_name': file_name,
                    'result': result
                })
                
                if result['status'] == 'success':
                    logger.info(f"✅ {file_name}: Successfully processed")
                    logger.info(f"   Schema detected: {result.get('schema_type', 'unknown')}")
                    logger.info(f"   Records: {result.get('row_count', 0)}")
                else:
                    logger.error(f"❌ {file_name}: Failed - {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                logger.error(f"❌ {file_name}: Exception - {e}")
                results.append({
                    'file_name': file_name,
                    'result': {'status': 'failed', 'error': str(e)}
                })
        
        return results
    
    def test_content_type_detection(self):
        """Test content type detection"""
        logger.info("Testing content type detection...")
        
        test_cases = [
            ('market_data.csv', 'csv'),
            ('properties.csv', 'csv'),
            ('regulatory_updates.csv', 'csv'),
            ('developers.csv', 'csv'),
            ('investment_insights.csv', 'csv')
        ]
        
        results = []
        
        for file_name, expected_type in test_cases:
            file_path = next((path for name, path in self.test_files if name == file_name), None)
            
            if file_path:
                detected_type = self.pipeline.detect_content_type(file_path)
                correct = detected_type == expected_type
                
                results.append({
                    'file_name': file_name,
                    'expected_type': expected_type,
                    'detected_type': detected_type,
                    'correct': correct
                })
                
                status = "✅" if correct else "❌"
                logger.info(f"{status} {file_name}: Expected {expected_type}, Detected {detected_type}")
        
        return results
    
    def test_csv_processor_schema_detection(self):
        """Test CSV processor schema detection"""
        logger.info("Testing CSV processor schema detection...")
        
        from processors.csv_processor import CSVProcessor
        processor = CSVProcessor()
        
        results = []
        
        for file_name, file_path in self.test_files:
            try:
                # Read the CSV file
                df = pd.read_csv(file_path)
                
                # Test schema detection
                detected_schema = processor._detect_schema_type(df)
                
                # Determine expected schema based on file name
                expected_schema = file_name.replace('.csv', '')
                
                correct = detected_schema == expected_schema
                
                results.append({
                    'file_name': file_name,
                    'expected_schema': expected_schema,
                    'detected_schema': detected_schema,
                    'correct': correct
                })
                
                status = "✅" if correct else "❌"
                logger.info(f"{status} {file_name}: Expected {expected_schema}, Detected {detected_schema}")
                
            except Exception as e:
                logger.error(f"❌ {file_name}: Exception - {e}")
                results.append({
                    'file_name': file_name,
                    'error': str(e)
                })
        
        return results
    
    def test_storage_strategy_determination(self):
        """Test storage strategy determination"""
        logger.info("Testing storage strategy determination...")
        
        test_cases = [
            ('csv', ['market_data', 'properties']),
            ('pdf', ['regulatory_framework', 'transaction_guidance']),
            ('excel', ['market_data', 'investment_insights']),
            ('web', ['market_forecasts', 'agent_resources']),
            ('api', ['developers', 'neighborhood_profiles'])
        ]
        
        results = []
        
        for content_type, expected_tables in test_cases:
            strategy = self.pipeline._determine_storage_strategy(content_type, {})
            
            if 'postgres' in strategy:
                actual_tables = strategy['postgres'].get('tables', [])
                correct = set(actual_tables) == set(expected_tables)
                
                results.append({
                    'content_type': content_type,
                    'expected_tables': expected_tables,
                    'actual_tables': actual_tables,
                    'correct': correct
                })
                
                status = "✅" if correct else "❌"
                logger.info(f"{status} {content_type}: Expected {expected_tables}, Got {actual_tables}")
            else:
                logger.warning(f"⚠️ {content_type}: No PostgreSQL strategy found")
        
        return results
    
    def generate_test_report(self, single_file_results, content_type_results, schema_results, strategy_results):
        """Generate comprehensive test report"""
        logger.info("Generating test report...")
        
        print("\n" + "="*80)
        print("🧪 PHASE 3: UNIFIED DATA INGESTION PIPELINE TEST REPORT")
        print("="*80)
        
        # Single file processing results
        print("\n📁 Single File Processing Results:")
        successful_files = [r for r in single_file_results if r['result']['status'] == 'success']
        failed_files = [r for r in single_file_results if r['result']['status'] == 'failed']
        
        print(f"   Total Files: {len(single_file_results)}")
        print(f"   Successful: {len(successful_files)} ✅")
        print(f"   Failed: {len(failed_files)} ❌")
        print(f"   Success Rate: {(len(successful_files)/len(single_file_results)*100):.1f}%")
        
        # Content type detection results
        print("\n🔍 Content Type Detection Results:")
        correct_detections = [r for r in content_type_results if r['correct']]
        incorrect_detections = [r for r in content_type_results if not r['correct']]
        
        print(f"   Total Tests: {len(content_type_results)}")
        print(f"   Correct: {len(correct_detections)} ✅")
        print(f"   Incorrect: {len(incorrect_detections)} ❌")
        print(f"   Accuracy: {(len(correct_detections)/len(content_type_results)*100):.1f}%")
        
        # Schema detection results
        print("\n🏗️ Schema Detection Results:")
        correct_schemas = [r for r in schema_results if r.get('correct', False)]
        incorrect_schemas = [r for r in schema_results if not r.get('correct', False)]
        
        print(f"   Total Tests: {len(schema_results)}")
        print(f"   Correct: {len(correct_schemas)} ✅")
        print(f"   Incorrect: {len(incorrect_schemas)} ❌")
        print(f"   Accuracy: {(len(correct_schemas)/len(schema_results)*100):.1f}%")
        
        # Storage strategy results
        print("\n💾 Storage Strategy Results:")
        correct_strategies = [r for r in strategy_results if r.get('correct', False)]
        incorrect_strategies = [r for r in strategy_results if not r.get('correct', False)]
        
        print(f"   Total Tests: {len(strategy_results)}")
        print(f"   Correct: {len(correct_strategies)} ✅")
        print(f"   Incorrect: {len(incorrect_strategies)} ❌")
        print(f"   Accuracy: {(len(correct_strategies)/len(strategy_results)*100):.1f}%")
        
        # Overall assessment
        print("\n🎯 Overall Assessment:")
        total_tests = len(single_file_results) + len(content_type_results) + len(schema_results) + len(strategy_results)
        total_successful = len(successful_files) + len(correct_detections) + len(correct_schemas) + len(correct_strategies)
        overall_success_rate = (total_successful / total_tests * 100) if total_tests > 0 else 0
        
        print(f"   Total Tests: {total_tests}")
        print(f"   Total Successful: {total_successful}")
        print(f"   Overall Success Rate: {overall_success_rate:.1f}%")
        
        if overall_success_rate >= 90:
            print("   🎉 EXCELLENT: Phase 3 implementation is working very well!")
        elif overall_success_rate >= 80:
            print("   ✅ GOOD: Phase 3 implementation is working well with minor issues.")
        elif overall_success_rate >= 70:
            print("   ⚠️ FAIR: Phase 3 implementation needs some improvements.")
        else:
            print("   ❌ POOR: Phase 3 implementation requires significant fixes.")
        
        print("\n" + "="*80)
        
        return {
            'total_tests': total_tests,
            'total_successful': total_successful,
            'overall_success_rate': overall_success_rate,
            'single_file_results': single_file_results,
            'content_type_results': content_type_results,
            'schema_results': schema_results,
            'strategy_results': strategy_results
        }
    
    def cleanup_test_files(self):
        """Clean up temporary test files"""
        logger.info("Cleaning up test files...")
        
        for file_name, file_path in self.test_files:
            try:
                os.unlink(file_path)
                logger.info(f"Deleted: {file_path}")
            except Exception as e:
                logger.warning(f"Could not delete {file_path}: {e}")
        
        self.test_files = []


def main():
    """Main test function"""
    logger.info("Starting Phase 3: Unified Data Ingestion Pipeline Tests")
    
    tester = Phase3IngestionTester()
    
    try:
        # Create sample files
        tester.create_sample_csv_files()
        
        # Run tests
        single_file_results = tester.test_single_file_processing()
        content_type_results = tester.test_content_type_detection()
        schema_results = tester.test_csv_processor_schema_detection()
        strategy_results = tester.test_storage_strategy_determination()
        
        # Generate report
        report = tester.generate_test_report(
            single_file_results, 
            content_type_results, 
            schema_results, 
            strategy_results
        )
        
        # Cleanup
        tester.cleanup_test_files()
        
        return report
        
    except Exception as e:
        logger.error(f"Test failed with exception: {e}")
        tester.cleanup_test_files()
        return None


if __name__ == "__main__":
    main()
