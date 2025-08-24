#!/usr/bin/env python3
"""
Example script demonstrating how to use the Data Processing Pipeline

This script shows how to:
1. Initialize the pipeline
2. Process property data from CSV files
3. Process web data
4. Get processing statistics
5. Run batch processing
"""

import sys
import os
from pathlib import Path

# Add the data_pipeline directory to the Python path
sys.path.append(str(Path(__file__).parent / "data_pipeline"))

from data_pipeline import DataPipeline

def main():
    """Main function demonstrating pipeline usage"""
    
    print("🏗️ Initializing Data Processing Pipeline...")
    
    # Initialize the pipeline
    pipeline = DataPipeline()
    
    # Validate pipeline configuration
    print("\n🔍 Validating Pipeline Configuration...")
    validation = pipeline.validate_pipeline()
    
    if not validation['config_valid']:
        print("❌ Pipeline configuration is invalid:")
        for error in validation['errors']:
            print(f"   - {error}")
        return
    
    if not validation['database_connections']:
        print("❌ Database connections failed:")
        for error in validation['errors']:
            print(f"   - {error}")
        return
    
    print("✅ Pipeline validation successful!")
    
    # Example 1: Process a single CSV file
    print("\n📊 Example 1: Processing Single CSV File")
    csv_file = "../data/listings.csv"  # Use existing sample data
    
    if os.path.exists(csv_file):
        print(f"Processing: {csv_file}")
        result = pipeline.process_property_data(csv_file)
        
        if result['success']:
            print(f"✅ Successfully processed {result['records_stored']} properties")
            print(f"⏱️ Processing time: {result['processing_time']:.2f} seconds")
            
            if result['quality_metrics']:
                quality = result['quality_metrics'].get('quality_metrics', {})
                print(f"📈 Data quality score: {quality.get('data_quality_score', 0):.2f}")
        else:
            print("❌ Processing failed:")
            for error in result['errors']:
                print(f"   - {error}")
    else:
        print(f"⚠️ File not found: {csv_file}")
    
    # Example 2: Process market data
    print("\n📈 Example 2: Processing Market Data")
    market_data = [
        {
            'area': 'Dubai Marina',
            'market_trend': 'Stable',
            'average_price_per_sqft': 1200,
            'rental_yield': 6.5,
            'demand_level': 'High',
            'market_volatility': 'Low',
            'investment_grade': 'A',
            'appreciation_rate': 3.5
        },
        {
            'area': 'Downtown Dubai',
            'market_trend': 'Growing',
            'average_price_per_sqft': 1500,
            'rental_yield': 5.8,
            'demand_level': 'Very High',
            'market_volatility': 'Medium',
            'investment_grade': 'A+',
            'appreciation_rate': 4.2
        }
    ]
    
    market_result = pipeline.process_market_data(market_data)
    
    if market_result['success']:
        print(f"✅ Successfully processed {market_result['records_stored']} market records")
    else:
        print("❌ Market data processing failed:")
        for error in market_result['errors']:
            print(f"   - {error}")
    
    # Example 3: Get processing statistics
    print("\n📊 Example 3: Processing Statistics")
    stats = pipeline.get_processing_stats()
    
    if stats:
        print(f"📈 Total properties in database: {stats.get('total_properties', 0)}")
        print(f"🔄 Recent processing runs: {stats.get('recent_runs', 0)}")
        print(f"⏱️ Average processing time: {stats.get('avg_processing_time', 0):.2f} seconds")
        print(f"📝 Total records processed this week: {stats.get('total_processed_week', 0)}")
        print(f"💾 Total records stored this week: {stats.get('total_stored_week', 0)}")
    else:
        print("❌ Could not retrieve processing statistics")
    
    # Example 4: Batch processing (if you have a data directory)
    print("\n🔄 Example 4: Batch Processing")
    data_directory = "../data"
    
    if os.path.exists(data_directory):
        print(f"Running batch processing on: {data_directory}")
        batch_result = pipeline.run_batch_processing(data_directory, ['csv', 'json'])
        
        print(f"📁 Total files found: {batch_result['total_files']}")
        print(f"✅ Successful files: {batch_result['successful_files']}")
        print(f"❌ Failed files: {batch_result['failed_files']}")
        print(f"📊 Total records processed: {batch_result['total_records_processed']}")
        print(f"💾 Total records stored: {batch_result['total_records_stored']}")
        print(f"⏱️ Total processing time: {batch_result['processing_time']:.2f} seconds")
        
        if batch_result['file_results']:
            print("\n📋 File Results:")
            for file_result in batch_result['file_results']:
                status = "✅" if file_result['success'] else "❌"
                print(f"   {status} {file_result['file']}")
                if not file_result['success'] and file_result['errors']:
                    for error in file_result['errors']:
                        print(f"      - {error}")
    else:
        print(f"⚠️ Data directory not found: {data_directory}")
    
    # Example 5: Create sample real Dubai property data
    print("\n🏠 Example 5: Creating Sample Dubai Property Data")
    sample_properties = [
        {
            'address': 'Marina Gate 1, Dubai Marina',
            'price_aed': 2500000,
            'bedrooms': 2,
            'bathrooms': 2,
            'square_feet': 1200,
            'property_type': 'Apartment',
            'area': 'Dubai Marina',
            'developer': 'Emaar Properties',
            'completion_date': '2016',
            'view': 'Sea View',
            'amenities': ['Swimming Pool', 'Gymnasium', 'Parking', 'Concierge'],
            'service_charges': 18000,
            'agent': 'Ahmed Ali',
            'agency': 'Emaar Properties'
        },
        {
            'address': 'Burj Vista 1, Downtown Dubai',
            'price_aed': 4500000,
            'bedrooms': 3,
            'bathrooms': 3,
            'square_feet': 1800,
            'property_type': 'Apartment',
            'area': 'Downtown Dubai',
            'developer': 'Emaar Properties',
            'completion_date': '2017',
            'view': 'Burj Khalifa View',
            'amenities': ['Swimming Pool', 'Gymnasium', 'Concierge', 'BBQ Area'],
            'service_charges': 25000,
            'agent': 'Sarah Johnson',
            'agency': 'Emaar Properties'
        },
        {
            'address': 'Palm Tower, Palm Jumeirah',
            'price_aed': 8500000,
            'bedrooms': 4,
            'bathrooms': 4,
            'square_feet': 2800,
            'property_type': 'Penthouse',
            'area': 'Palm Jumeirah',
            'developer': 'Nakheel',
            'completion_date': '2020',
            'view': 'Sea View',
            'amenities': ['Private Pool', 'Gymnasium', 'Concierge', 'Private Garden'],
            'service_charges': 35000,
            'agent': 'Michael Brown',
            'agency': 'Nakheel'
        }
    ]
    
    # Save sample data to CSV for processing
    import pandas as pd
    sample_csv = "../data/sample_dubai_properties.csv"
    df = pd.DataFrame(sample_properties)
    df.to_csv(sample_csv, index=False)
    
    print(f"📝 Created sample data file: {sample_csv}")
    
    # Process the sample data
    sample_result = pipeline.process_property_data(sample_csv)
    
    if sample_result['success']:
        print(f"✅ Successfully processed {sample_result['records_stored']} sample properties")
        print(f"⏱️ Processing time: {sample_result['processing_time']:.2f} seconds")
        
        # Show quality metrics
        if sample_result['quality_metrics']:
            quality = sample_result['quality_metrics'].get('quality_metrics', {})
            print(f"📈 Data quality score: {quality.get('data_quality_score', 0):.2f}")
            print(f"📊 Completeness score: {quality.get('completeness_score', 0):.2f}")
    else:
        print("❌ Sample data processing failed:")
        for error in sample_result['errors']:
            print(f"   - {error}")
    
    print("\n🎉 Pipeline demonstration completed!")
    print("\n📚 Next Steps:")
    print("1. Add your real Dubai property data to the data/ directory")
    print("2. Configure the pipeline_config.yaml with your database credentials")
    print("3. Run the pipeline on your data files")
    print("4. Monitor processing logs in data_pipeline.log")
    print("5. Query the processed data from PostgreSQL and ChromaDB")

if __name__ == "__main__":
    main()
