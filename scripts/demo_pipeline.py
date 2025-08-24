#!/usr/bin/env python3
"""
Demo Script for Data Ingestion Pipeline
Shows how to use the unified data ingestion pipeline with real examples
"""

import os
import sys
import tempfile
import pandas as pd
import json
from datetime import datetime

# Add the scripts directory to the path
sys.path.append(os.path.dirname(__file__))

from unified_data_ingestion import UnifiedDataIngestionPipeline

def create_demo_files():
    """Create demo files for testing"""
    demo_files = []
    
    print("📁 Creating demo files...")
    
    # Demo CSV file
    csv_data = pd.DataFrame({
        'address': ['Marina Heights Tower 1', 'Burj Vista 2', 'Palm Tower A'],
        'price': [2500000, 4500000, 8500000],
        'bedrooms': [2, 3, 4],
        'bathrooms': [2, 3, 4],
        'neighborhood': ['Dubai Marina', 'Downtown Dubai', 'Palm Jumeirah'],
        'developer': ['Emaar Properties', 'Emaar Properties', 'Nakheel']
    })
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        csv_data.to_csv(f.name, index=False)
        demo_files.append(('properties.csv', f.name))
    
    # Demo JSON file (simulating API data)
    json_data = {
        "developers": [
            {
                "name": "Emaar Properties",
                "market_share": 25.5,
                "reputation_score": 9.2,
                "total_projects": 150
            },
            {
                "name": "DAMAC Properties", 
                "market_share": 8.3,
                "reputation_score": 7.8,
                "total_projects": 85
            }
        ]
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(json_data, f, indent=2)
        demo_files.append(('developer_profiles.json', f.name))
    
    # Demo HTML file (simulating web content)
    html_content = """
    <!DOCTYPE html>
    <html>
    <head><title>Dubai Market Forecast 2024</title></head>
    <body>
        <h1>Dubai Real Estate Market Forecast 2024</h1>
        <p>The Dubai real estate market is expected to show strong growth in 2024, with forecasts indicating a 10-15% increase in property prices across prime locations.</p>
        <h2>Market Predictions</h2>
        <ul>
            <li>Dubai Marina: Expected 12% price increase</li>
            <li>Downtown Dubai: Forecasted 15% growth</li>
        </ul>
    </body>
    </html>
    """
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(html_content)
        demo_files.append(('market_forecast.html', f.name))
    
    print(f"✅ Created {len(demo_files)} demo files")
    return demo_files

def demo_single_file_processing(pipeline, demo_files):
    """Demo single file processing"""
    print("\n🎯 Demo 1: Single File Processing")
    print("="*50)
    
    for file_name, file_path in demo_files:
        print(f"\n📄 Processing: {file_name}")
        
        try:
            result = pipeline.process_file(file_path)
            
            if result['status'] == 'success':
                print(f"✅ Successfully processed {file_name}")
                print(f"   Content Type: {result.get('content_type', 'unknown')}")
                
                if result.get('content_type') == 'csv':
                    print(f"   Schema: {result.get('schema_type', 'unknown')}")
                    print(f"   Records: {result.get('row_count', 0)}")
                elif result.get('content_type') == 'api':
                    print(f"   API Type: {result.get('api_type_classified', 'unknown')}")
                elif result.get('content_type') == 'web':
                    print(f"   Content Type: {result.get('content_type_classified', 'unknown')}")
                
            else:
                print(f"❌ Failed to process {file_name}: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Exception processing {file_name}: {e}")

def demo_content_type_detection(pipeline, demo_files):
    """Demo content type detection"""
    print("\n🔍 Demo 2: Content Type Detection")
    print("="*50)
    
    for file_name, file_path in demo_files:
        try:
            detected_type = pipeline.detect_content_type(file_path)
            print(f"📄 {file_name} → Detected as: {detected_type}")
        except Exception as e:
            print(f"❌ Error detecting type for {file_name}: {e}")

def demo_storage_strategy(pipeline, demo_files):
    """Demo storage strategy determination"""
    print("\n💾 Demo 3: Storage Strategy Determination")
    print("="*50)
    
    for file_name, file_path in demo_files:
        try:
            # Get content type
            content_type = pipeline.detect_content_type(file_path)
            
            # Determine storage strategy
            strategy = pipeline._determine_storage_strategy(content_type, {})
            
            print(f"\n📄 {file_name} ({content_type})")
            if 'postgres' in strategy:
                tables = strategy['postgres'].get('tables', [])
                print(f"   PostgreSQL Tables: {', '.join(tables)}")
            if 'chromadb' in strategy:
                collections = strategy['chromadb'].get('collections', [])
                print(f"   ChromaDB Collections: {', '.join(collections)}")
                
        except Exception as e:
            print(f"❌ Error determining strategy for {file_name}: {e}")

def demo_directory_processing(pipeline, demo_files):
    """Demo directory processing"""
    print("\n📁 Demo 4: Directory Processing")
    print("="*50)
    
    # Create a temporary directory with demo files
    import shutil
    
    temp_dir = tempfile.mkdtemp()
    print(f"📁 Created temporary directory: {temp_dir}")
    
    try:
        # Copy demo files to directory
        for file_name, file_path in demo_files:
            shutil.copy2(file_path, os.path.join(temp_dir, file_name))
        
        print(f"📄 Copied {len(demo_files)} files to directory")
        
        # Process directory
        results = pipeline.process_directory(temp_dir)
        
        print(f"\n📊 Directory Processing Results:")
        print(f"   Total Files: {results['ingestion_stats']['total_files']}")
        print(f"   Successfully Processed: {results['ingestion_stats']['processed_files']}")
        print(f"   Failed: {results['ingestion_stats']['failed_files']}")
        
        success_rate = (results['ingestion_stats']['processed_files'] / results['ingestion_stats']['total_files'] * 100) if results['ingestion_stats']['total_files'] > 0 else 0
        print(f"   Success Rate: {success_rate:.1f}%")
        
    except Exception as e:
        print(f"❌ Error processing directory: {e}")
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)
        print(f"🧹 Cleaned up temporary directory")

def demo_ingestion_report(pipeline):
    """Demo ingestion report generation"""
    print("\n📊 Demo 5: Ingestion Report Generation")
    print("="*50)
    
    try:
        report = pipeline.generate_ingestion_report()
        print("📋 Generated ingestion report:")
        print(report)
    except Exception as e:
        print(f"❌ Error generating report: {e}")

def cleanup_demo_files(demo_files):
    """Clean up demo files"""
    print("\n🧹 Cleaning up demo files...")
    
    for file_name, file_path in demo_files:
        try:
            os.unlink(file_path)
            print(f"✅ Deleted: {file_name}")
        except Exception as e:
            print(f"⚠️ Could not delete {file_name}: {e}")

def main():
    """Main demo function"""
    print("🚀 Dubai Real Estate Data Ingestion Pipeline Demo")
    print("="*60)
    
    # Initialize pipeline
    print("\n🔧 Initializing data ingestion pipeline...")
    pipeline = UnifiedDataIngestionPipeline()
    print("✅ Pipeline initialized successfully")
    
    # Create demo files
    demo_files = create_demo_files()
    
    try:
        # Run demos
        demo_content_type_detection(pipeline, demo_files)
        demo_single_file_processing(pipeline, demo_files)
        demo_storage_strategy(pipeline, demo_files)
        demo_directory_processing(pipeline, demo_files)
        demo_ingestion_report(pipeline)
        
        print("\n🎉 Demo completed successfully!")
        print("\n💡 Next Steps:")
        print("   1. Try processing your own CSV, PDF, Excel, or JSON files")
        print("   2. Test with real web URLs or API endpoints")
        print("   3. Process entire directories of mixed content")
        print("   4. Integrate with your existing data workflows")
        
    except Exception as e:
        print(f"\n❌ Demo failed with exception: {e}")
    
    finally:
        # Cleanup
        cleanup_demo_files(demo_files)

if __name__ == "__main__":
    main()
