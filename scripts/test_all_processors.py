#!/usr/bin/env python3
"""
Comprehensive Test Script for All Data Ingestion Processors
Demonstrates CSV, PDF, Excel, Web, and API processors with sample data
"""

import os
import sys
import tempfile
import pandas as pd
import json
from datetime import datetime
import logging

# Add the scripts directory to the path
sys.path.append(os.path.dirname(__file__))

from unified_data_ingestion import UnifiedDataIngestionPipeline

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AllProcessorsTester:
    """Test class for all data ingestion processors"""
    
    def __init__(self):
        self.pipeline = UnifiedDataIngestionPipeline()
        self.test_files = []
        
    def create_sample_csv_files(self):
        """Create sample CSV files for testing"""
        logger.info("Creating sample CSV files...")
        
        # Sample market data CSV
        market_data = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'neighborhood': ['Dubai Marina', 'Downtown Dubai', 'Palm Jumeirah'],
            'property_type': ['Apartment', 'Penthouse', 'Villa'],
            'avg_price_per_sqft': [1200.50, 1800.75, 2200.25],
            'transaction_volume': [45, 23, 12],
            'rental_yield': [6.5, 5.8, 7.2],
            'market_trend': ['Rising', 'Stable', 'Rising']
        })
        
        # Sample properties CSV
        properties_data = pd.DataFrame({
            'address': ['Marina Heights Tower 1', 'Burj Vista 2', 'Palm Tower A'],
            'price': [2500000, 4500000, 8500000],
            'bedrooms': [2, 3, 4],
            'bathrooms': [2, 3, 4],
            'neighborhood': ['Dubai Marina', 'Downtown Dubai', 'Palm Jumeirah'],
            'developer': ['Emaar Properties', 'Emaar Properties', 'Nakheel'],
            'completion_date': ['2023-12-01', '2024-06-01', '2024-03-01']
        })
        
        # Sample regulatory updates CSV
        regulatory_data = pd.DataFrame({
            'law_name': ['Golden Visa Extension', 'RERA Compliance Update'],
            'enactment_date': ['2024-01-15', '2024-02-01'],
            'description': [
                'Extended Golden Visa eligibility for property investors',
                'Updated RERA compliance requirements for developers'
            ],
            'status': ['Active', 'Active'],
            'impact_areas': ['Investment', 'Development']
        })
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            market_data.to_csv(f.name, index=False)
            self.test_files.append(('market_data.csv', f.name))
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            properties_data.to_csv(f.name, index=False)
            self.test_files.append(('properties.csv', f.name))
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            regulatory_data.to_csv(f.name, index=False)
            self.test_files.append(('regulatory_updates.csv', f.name))
        
        logger.info(f"Created {len(self.test_files)} CSV files")
    
    def create_sample_excel_files(self):
        """Create sample Excel files for testing"""
        logger.info("Creating sample Excel files...")
        
        # Create Excel file with multiple sheets
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            excel_file = f.name
        
        # Market data sheet
        market_data = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'neighborhood': ['Dubai Marina', 'Downtown Dubai', 'Palm Jumeirah'],
            'avg_price_per_sqft': [1200.50, 1800.75, 2200.25],
            'transaction_volume': [45, 23, 12]
        })
        
        # Financial analysis sheet
        financial_data = pd.DataFrame({
            'investment_type': ['Golden Visa', 'Rental Portfolio', 'Off-Plan'],
            'roi_projection': [8.5, 6.2, 12.5],
            'investment_amount_min': [2000000, 1500000, 1000000],
            'risk_level': ['Low', 'Medium', 'High']
        })
        
        # Write to Excel with multiple sheets
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            market_data.to_excel(writer, sheet_name='Market Data', index=False)
            financial_data.to_excel(writer, sheet_name='Financial Analysis', index=False)
        
        self.test_files.append(('financial_analysis.xlsx', excel_file))
        logger.info("Created Excel file with multiple sheets")
    
    def create_sample_pdf_files(self):
        """Create sample PDF files for testing"""
        logger.info("Creating sample PDF files...")
        
        # Create a simple text file that simulates PDF content
        pdf_content = """
        Dubai Real Estate Market Report 2024
        
        Market Analysis and Forecasts
        
        The Dubai real estate market has shown remarkable growth in 2024, with average prices in Dubai Marina increasing by 15% compared to 2023. The market analysis indicates strong demand for luxury properties, particularly in Downtown Dubai and Palm Jumeirah areas.
        
        Key Market Trends:
        - Average price per square foot in Dubai Marina: AED 1,200
        - Transaction volume increased by 25% in Q1 2024
        - Rental yields averaging 6.5% across prime locations
        
        Developer Performance:
        - Emaar Properties continues to lead with 25% market share
        - DAMAC Properties shows strong growth in mid-market segment
        - Nakheel's Palm Jumeirah projects maintain premium positioning
        
        Regulatory Updates:
        - Golden Visa requirements updated for property investors
        - RERA compliance standards enhanced for developers
        - New foreign investment regulations implemented
        
        Investment Opportunities:
        - Off-plan properties offer 12-15% ROI potential
        - Rental portfolios provide stable 6-8% annual returns
        - Golden Visa investments start from AED 2 million
        
        Market Forecast for 2025:
        - Expected 10-12% price appreciation in prime areas
        - Increased foreign investment due to regulatory reforms
        - Strong demand for luxury and mid-market properties
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(pdf_content)
            self.test_files.append(('market_report.txt', f.name))  # Simulating PDF
        
        logger.info("Created simulated PDF content file")
    
    def create_sample_json_files(self):
        """Create sample JSON files for testing"""
        logger.info("Creating sample JSON files...")
        
        # Developer profiles JSON
        developer_data = {
            "developers": [
                {
                    "name": "Emaar Properties",
                    "market_share": 25.5,
                    "reputation_score": 9.2,
                    "total_projects": 150,
                    "key_projects": ["Burj Khalifa", "Dubai Mall", "Downtown Dubai"],
                    "specialties": ["Luxury Development", "Mixed-Use Projects"]
                },
                {
                    "name": "DAMAC Properties",
                    "market_share": 8.3,
                    "reputation_score": 7.8,
                    "total_projects": 85,
                    "key_projects": ["DAMAC Hills", "DAMAC Towers"],
                    "specialties": ["Mid-Market Development", "Residential Projects"]
                }
            ],
            "api_version": "1.0",
            "last_updated": "2024-01-15"
        }
        
        # Neighborhood profiles JSON
        neighborhood_data = {
            "neighborhoods": [
                {
                    "name": "Dubai Marina",
                    "description": "Luxury waterfront community with high-rise towers",
                    "avg_price_per_sqft": 1200,
                    "rental_yield": 6.5,
                    "amenities": ["Marina Walk", "Shopping Centers", "Beach Access"],
                    "target_audience": "High Net Worth, Expats"
                },
                {
                    "name": "Downtown Dubai",
                    "description": "City center with iconic landmarks",
                    "avg_price_per_sqft": 1800,
                    "rental_yield": 5.8,
                    "amenities": ["Burj Khalifa", "Dubai Mall", "Fountain Views"],
                    "target_audience": "Luxury Buyers, Tourists"
                }
            ],
            "data_source": "Dubai Land Department",
            "extraction_date": "2024-01-15"
        }
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(developer_data, f, indent=2)
            self.test_files.append(('developer_profiles.json', f.name))
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(neighborhood_data, f, indent=2)
            self.test_files.append(('neighborhood_profiles.json', f.name))
        
        logger.info("Created JSON files for API testing")
    
    def create_sample_html_files(self):
        """Create sample HTML files for testing"""
        logger.info("Creating sample HTML files...")
        
        # Market forecast HTML
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dubai Real Estate Market Forecast 2024</title>
        </head>
        <body>
            <h1>Dubai Real Estate Market Forecast 2024</h1>
            <p>The Dubai real estate market is expected to show strong growth in 2024, with forecasts indicating a 10-15% increase in property prices across prime locations.</p>
            
            <h2>Market Predictions</h2>
            <ul>
                <li>Dubai Marina: Expected 12% price increase</li>
                <li>Downtown Dubai: Forecasted 15% growth</li>
                <li>Palm Jumeirah: Anticipated 18% appreciation</li>
            </ul>
            
            <h2>Investment Opportunities</h2>
            <p>Golden Visa investments starting from AED 2 million offer excellent ROI potential of 8-10% annually.</p>
            
            <h2>Developer Insights</h2>
            <p>Emaar Properties continues to dominate the market with 25% market share, followed by DAMAC Properties with 8.3%.</p>
            
            <p>For more information, contact: +971 4 123 4567</p>
            <p>Email: info@dubairealestate.ae</p>
        </body>
        </html>
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(html_content)
            self.test_files.append(('market_forecast.html', f.name))
        
        logger.info("Created HTML file for web scraping testing")
    
    def test_csv_processor(self):
        """Test CSV processor functionality"""
        logger.info("Testing CSV processor...")
        
        results = []
        for file_name, file_path in self.test_files:
            if file_name.endswith('.csv'):
                try:
                    result = self.pipeline.process_file(file_path)
                    results.append({
                        'file_name': file_name,
                        'result': result
                    })
                    
                    if result['status'] == 'success':
                        logger.info(f"✅ {file_name}: Successfully processed")
                        logger.info(f"   Schema: {result.get('schema_type', 'unknown')}")
                        logger.info(f"   Records: {result.get('row_count', 0)}")
                    else:
                        logger.error(f"❌ {file_name}: Failed - {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    logger.error(f"❌ {file_name}: Exception - {e}")
        
        return results
    
    def test_excel_processor(self):
        """Test Excel processor functionality"""
        logger.info("Testing Excel processor...")
        
        results = []
        for file_name, file_path in self.test_files:
            if file_name.endswith('.xlsx'):
                try:
                    result = self.pipeline.process_file(file_path)
                    results.append({
                        'file_name': file_name,
                        'result': result
                    })
                    
                    if result['status'] == 'success':
                        logger.info(f"✅ {file_name}: Successfully processed")
                        logger.info(f"   Sheets: {result.get('total_sheets', 0)}")
                        logger.info(f"   Total Rows: {result.get('total_rows', 0)}")
                    else:
                        logger.error(f"❌ {file_name}: Failed - {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    logger.error(f"❌ {file_name}: Exception - {e}")
        
        return results
    
    def test_pdf_processor(self):
        """Test PDF processor functionality"""
        logger.info("Testing PDF processor...")
        
        results = []
        for file_name, file_path in self.test_files:
            if file_name.endswith('.txt'):  # Simulating PDF
                try:
                    result = self.pipeline.process_file(file_path)
                    results.append({
                        'file_name': file_name,
                        'result': result
                    })
                    
                    if result['status'] == 'success':
                        logger.info(f"✅ {file_name}: Successfully processed")
                        logger.info(f"   Document Type: {result.get('document_type', 'unknown')}")
                        logger.info(f"   Text Length: {result.get('text_length', 0)}")
                    else:
                        logger.error(f"❌ {file_name}: Failed - {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    logger.error(f"❌ {file_name}: Exception - {e}")
        
        return results
    
    def test_api_processor(self):
        """Test API processor functionality"""
        logger.info("Testing API processor...")
        
        results = []
        for file_name, file_path in self.test_files:
            if file_name.endswith('.json'):
                try:
                    result = self.pipeline.process_file(file_path)
                    results.append({
                        'file_name': file_name,
                        'result': result
                    })
                    
                    if result['status'] == 'success':
                        logger.info(f"✅ {file_name}: Successfully processed")
                        logger.info(f"   API Type: {result.get('api_type_classified', 'unknown')}")
                        logger.info(f"   Data Size: {result.get('data_size', 0)}")
                    else:
                        logger.error(f"❌ {file_name}: Failed - {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    logger.error(f"❌ {file_name}: Exception - {e}")
        
        return results
    
    def test_web_processor(self):
        """Test Web processor functionality"""
        logger.info("Testing Web processor...")
        
        results = []
        for file_name, file_path in self.test_files:
            if file_name.endswith('.html'):
                try:
                    result = self.pipeline.process_file(file_path)
                    results.append({
                        'file_name': file_name,
                        'result': result
                    })
                    
                    if result['status'] == 'success':
                        logger.info(f"✅ {file_name}: Successfully processed")
                        logger.info(f"   Content Type: {result.get('content_type_classified', 'unknown')}")
                        logger.info(f"   Content Length: {result.get('content_length', 0)}")
                    else:
                        logger.error(f"❌ {file_name}: Failed - {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    logger.error(f"❌ {file_name}: Exception - {e}")
        
        return results
    
    def test_content_type_detection(self):
        """Test content type detection for all files"""
        logger.info("Testing content type detection...")
        
        results = []
        for file_name, file_path in self.test_files:
            try:
                detected_type = self.pipeline.detect_content_type(file_path)
                
                # Determine expected type based on file extension
                expected_type = None
                if file_name.endswith('.csv'):
                    expected_type = 'csv'
                elif file_name.endswith('.xlsx'):
                    expected_type = 'excel'
                elif file_name.endswith('.txt'):  # Simulating PDF
                    expected_type = 'pdf'
                elif file_name.endswith('.json'):
                    expected_type = 'api'
                elif file_name.endswith('.html'):
                    expected_type = 'web'
                
                correct = detected_type == expected_type
                results.append({
                    'file_name': file_name,
                    'expected_type': expected_type,
                    'detected_type': detected_type,
                    'correct': correct
                })
                
                status = "✅" if correct else "❌"
                logger.info(f"{status} {file_name}: Expected {expected_type}, Detected {detected_type}")
                
            except Exception as e:
                logger.error(f"❌ {file_name}: Exception - {e}")
        
        return results
    
    def generate_comprehensive_report(self, csv_results, excel_results, pdf_results, api_results, web_results, detection_results):
        """Generate comprehensive test report"""
        logger.info("Generating comprehensive test report...")
        
        print("\n" + "="*80)
        print("🧪 COMPREHENSIVE DATA INGESTION PROCESSORS TEST REPORT")
        print("="*80)
        
        # Content Type Detection Results
        print("\n🔍 Content Type Detection Results:")
        correct_detections = [r for r in detection_results if r['correct']]
        incorrect_detections = [r for r in detection_results if not r['correct']]
        
        print(f"   Total Tests: {len(detection_results)}")
        print(f"   Correct: {len(correct_detections)} ✅")
        print(f"   Incorrect: {len(incorrect_detections)} ❌")
        print(f"   Accuracy: {(len(correct_detections)/len(detection_results)*100):.1f}%")
        
        # CSV Processor Results
        print("\n📊 CSV Processor Results:")
        successful_csv = [r for r in csv_results if r['result']['status'] == 'success']
        failed_csv = [r for r in csv_results if r['result']['status'] == 'failed']
        
        print(f"   Total Files: {len(csv_results)}")
        print(f"   Successful: {len(successful_csv)} ✅")
        print(f"   Failed: {len(failed_csv)} ❌")
        print(f"   Success Rate: {(len(successful_csv)/len(csv_results)*100):.1f}%")
        
        # Excel Processor Results
        print("\n📈 Excel Processor Results:")
        successful_excel = [r for r in excel_results if r['result']['status'] == 'success']
        failed_excel = [r for r in excel_results if r['result']['status'] == 'failed']
        
        print(f"   Total Files: {len(excel_results)}")
        print(f"   Successful: {len(successful_excel)} ✅")
        print(f"   Failed: {len(failed_excel)} ❌")
        print(f"   Success Rate: {(len(successful_excel)/len(excel_results)*100):.1f}%")
        
        # PDF Processor Results
        print("\n📄 PDF Processor Results:")
        successful_pdf = [r for r in pdf_results if r['result']['status'] == 'success']
        failed_pdf = [r for r in pdf_results if r['result']['status'] == 'failed']
        
        print(f"   Total Files: {len(pdf_results)}")
        print(f"   Successful: {len(successful_pdf)} ✅")
        print(f"   Failed: {len(failed_pdf)} ❌")
        print(f"   Success Rate: {(len(successful_pdf)/len(pdf_results)*100):.1f}%")
        
        # API Processor Results
        print("\n🔌 API Processor Results:")
        successful_api = [r for r in api_results if r['result']['status'] == 'success']
        failed_api = [r for r in api_results if r['result']['status'] == 'failed']
        
        print(f"   Total Files: {len(api_results)}")
        print(f"   Successful: {len(successful_api)} ✅")
        print(f"   Failed: {len(failed_api)} ❌")
        print(f"   Success Rate: {(len(successful_api)/len(api_results)*100):.1f}%")
        
        # Web Processor Results
        print("\n🌐 Web Processor Results:")
        successful_web = [r for r in web_results if r['result']['status'] == 'success']
        failed_web = [r for r in web_results if r['result']['status'] == 'failed']
        
        print(f"   Total Files: {len(web_results)}")
        print(f"   Successful: {len(successful_web)} ✅")
        print(f"   Failed: {len(failed_web)} ❌")
        print(f"   Success Rate: {(len(successful_web)/len(web_results)*100):.1f}%")
        
        # Overall Assessment
        print("\n🎯 Overall Assessment:")
        total_tests = len(detection_results) + len(csv_results) + len(excel_results) + len(pdf_results) + len(api_results) + len(web_results)
        total_successful = len(correct_detections) + len(successful_csv) + len(successful_excel) + len(successful_pdf) + len(successful_api) + len(successful_web)
        overall_success_rate = (total_successful / total_tests * 100) if total_tests > 0 else 0
        
        print(f"   Total Tests: {total_tests}")
        print(f"   Total Successful: {total_successful}")
        print(f"   Overall Success Rate: {overall_success_rate:.1f}%")
        
        if overall_success_rate >= 90:
            print("   🎉 EXCELLENT: All processors are working perfectly!")
        elif overall_success_rate >= 80:
            print("   ✅ GOOD: Most processors are working well with minor issues.")
        elif overall_success_rate >= 70:
            print("   ⚠️ FAIR: Some processors need improvements.")
        else:
            print("   ❌ POOR: Multiple processors require significant fixes.")
        
        print("\n" + "="*80)
        
        return {
            'total_tests': total_tests,
            'total_successful': total_successful,
            'overall_success_rate': overall_success_rate,
            'detection_results': detection_results,
            'csv_results': csv_results,
            'excel_results': excel_results,
            'pdf_results': pdf_results,
            'api_results': api_results,
            'web_results': web_results
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
    logger.info("Starting Comprehensive Data Ingestion Processors Test")
    
    tester = AllProcessorsTester()
    
    try:
        # Create sample files
        tester.create_sample_csv_files()
        tester.create_sample_excel_files()
        tester.create_sample_pdf_files()
        tester.create_sample_json_files()
        tester.create_sample_html_files()
        
        # Run tests
        detection_results = tester.test_content_type_detection()
        csv_results = tester.test_csv_processor()
        excel_results = tester.test_excel_processor()
        pdf_results = tester.test_pdf_processor()
        api_results = tester.test_api_processor()
        web_results = tester.test_web_processor()
        
        # Generate report
        report = tester.generate_comprehensive_report(
            csv_results, excel_results, pdf_results, 
            api_results, web_results, detection_results
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
