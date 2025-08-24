# 🎯 Demo Use Cases - Light to Heavy

## Overview

This document provides comprehensive demo scenarios that showcase the data ingestion pipeline's capabilities, from simple single-file processing to complex multi-source enterprise scenarios.

## 🟢 Light Use Cases (Beginner Level)

### **Use Case 1: Single CSV File Processing**
**Scenario**: A real estate agent has a simple CSV file with property listings.

**Input**: `simple_properties.csv`
```csv
address,price,bedrooms,bathrooms,neighborhood
Marina Heights Tower 1,2500000,2,2,Dubai Marina
Burj Vista 2,4500000,3,3,Downtown Dubai
Palm Tower A,8500000,4,4,Palm Jumeirah
```

**Processing Steps**:
1. **Content Detection**: `.csv` → `"csv"`
2. **Schema Detection**: Columns `address`, `price`, `bedrooms` → `"properties"`
3. **Storage Strategy**: 
   - PostgreSQL: `properties` table
   - ChromaDB: `market_analysis` collection
4. **Result**: Data searchable via chat interface

**Usage**:
```python
from scripts.unified_data_ingestion import UnifiedDataIngestionPipeline

pipeline = UnifiedDataIngestionPipeline()
result = pipeline.process_file("simple_properties.csv")
print(f"Processed {result['structured_data']['row_count']} properties")
```

### **Use Case 2: Single PDF Document**
**Scenario**: Upload a market report PDF for analysis.

**Input**: `dubai_market_report_2024.pdf`
```
Dubai Real Estate Market Report 2024
Market Analysis and Forecasts
Average prices in Dubai Marina increased by 15% in 2024...
```

**Processing Steps**:
1. **Content Detection**: `.pdf` → `"pdf"`
2. **Document Classification**: Keywords "market", "analysis", "forecast" → `"market_report"`
3. **Storage Strategy**: ChromaDB: `market_analysis`, `market_forecasts` collections
4. **Result**: Text searchable via semantic search

**Usage**:
```python
result = pipeline.process_file("dubai_market_report_2024.pdf")
print(f"Document classified as: {result['structured_data']['document_type']}")
```

### **Use Case 3: Single Excel File**
**Scenario**: Process a financial analysis Excel file.

**Input**: `investment_analysis.xlsx` (with sheets: "ROI Analysis", "Market Trends")

**Processing Steps**:
1. **Content Detection**: `.xlsx` → `"excel"`
2. **Sheet Classification**: 
   - "ROI Analysis" → `"financial_analysis"`
   - "Market Trends" → `"market_data"`
3. **Storage Strategy**: 
   - PostgreSQL: `market_data`, `investment_insights` tables
   - ChromaDB: `financial_insights` collection
4. **Result**: Multi-sheet data organized and searchable

**Usage**:
```python
result = pipeline.process_file("investment_analysis.xlsx")
print(f"Processed {result['total_sheets']} sheets with {result['total_rows']} total rows")
```

## 🟡 Medium Use Cases (Intermediate Level)

### **Use Case 4: Web Content Scraping**
**Scenario**: Extract market forecasts from real estate websites.

**Input**: `https://www.propertyfinder.ae/market-insights/dubai-2024-forecast`

**Processing Steps**:
1. **Content Detection**: URL → `"web"`
2. **Content Classification**: Keywords "forecast", "2024" → `"market_forecast"`
3. **Entity Extraction**: "Dubai Marina", "Emaar Properties"
4. **Storage Strategy**: ChromaDB: `market_forecasts`, `market_analysis` collections
5. **Result**: Live web data integrated into knowledge base

**Usage**:
```python
result = pipeline.process_file("https://www.propertyfinder.ae/market-insights/dubai-2024-forecast")
print(f"Extracted {len(result['structured_data']['key_entities'])} entities")
```

### **Use Case 5: API Data Integration**
**Scenario**: Fetch developer profiles from real estate API.

**Input**: `https://api.dubai.gov.ae/developers/profiles`

**Processing Steps**:
1. **Content Detection**: API URL → `"api"`
2. **API Classification**: Keywords "developer", "profiles" → `"developer_profiles"`
3. **Data Extraction**: Developer information, project counts
4. **Storage Strategy**: 
   - PostgreSQL: `developers` table
   - ChromaDB: `developer_profiles` collection
5. **Result**: Real-time API data integrated

**Usage**:
```python
result = pipeline.process_file("https://api.dubai.gov.ae/developers/profiles")
print(f"API data type: {result['api_type_classified']}")
```

### **Use Case 6: Mixed Content Directory**
**Scenario**: Process a folder containing various file types.

**Input Directory**: `real_estate_data/`
```
real_estate_data/
├── market_data.csv
├── regulations.pdf
├── developer_profiles.json
├── market_forecast.html
└── financial_analysis.xlsx
```

**Processing Steps**:
1. **Directory Scan**: Identify all supported file types
2. **Parallel Processing**: Each file processed by appropriate processor
3. **Unified Storage**: All data organized into appropriate databases
4. **Result**: Complete knowledge base from multiple sources

**Usage**:
```python
results = pipeline.process_directory("real_estate_data/")
print(f"Processed {results['ingestion_stats']['processed_files']} files successfully")
```

## 🔴 Heavy Use Cases (Advanced Level)

### **Use Case 7: Enterprise Data Integration**
**Scenario**: Large-scale data ingestion for a real estate company.

**Input Sources**:
- **CSV Files**: 50+ property listing files (10,000+ properties)
- **PDF Reports**: 20+ market reports and regulations
- **Excel Files**: 15+ financial analysis workbooks
- **Web APIs**: 5+ real-time data feeds
- **Web Scraping**: 10+ market forecast websites

**Processing Steps**:
1. **Batch Processing**: Process files in parallel batches
2. **Data Validation**: Comprehensive quality checks
3. **Deduplication**: Remove duplicate entries across sources
4. **Cross-Reference**: Link related data across sources
5. **Performance Optimization**: Efficient storage and indexing
6. **Result**: Enterprise-grade knowledge base

**Usage**:
```python
# Process large directory with custom patterns
results = pipeline.process_directory(
    "enterprise_data/",
    file_patterns=["*.csv", "*.pdf", "*.xlsx", "*.json", "*.html"]
)

# Generate comprehensive report
report = pipeline.generate_ingestion_report()
print(f"Enterprise ingestion completed: {report}")
```

### **Use Case 8: Real-Time Data Pipeline**
**Scenario**: Continuous data ingestion from multiple live sources.

**Input Sources**:
- **Real-time APIs**: Property listings, market data
- **Web Scraping**: Live market forecasts, news
- **File Monitoring**: New CSV/PDF uploads
- **Database Feeds**: External system integrations

**Processing Steps**:
1. **Continuous Monitoring**: Watch for new data sources
2. **Real-time Processing**: Process data as it arrives
3. **Incremental Updates**: Update existing data without duplicates
4. **Quality Assurance**: Validate data in real-time
5. **Performance Monitoring**: Track processing metrics
6. **Result**: Live, up-to-date knowledge base

**Usage**:
```python
# Set up continuous monitoring
pipeline.monitor_directory("live_data/", interval=60)  # Check every minute

# Process real-time API feeds
pipeline.process_api_feed("https://api.propertyfinder.ae/live-listings", interval=300)

# Monitor processing performance
pipeline.get_performance_metrics()
```

### **Use Case 9: Multi-Tenant Data Management**
**Scenario**: Handle data for multiple real estate agencies.

**Input Structure**:
```
multi_tenant_data/
├── agency_1/
│   ├── properties.csv
│   ├── market_reports.pdf
│   └── financial_data.xlsx
├── agency_2/
│   ├── listings.csv
│   ├── regulations.pdf
│   └── investment_analysis.xlsx
└── shared/
    ├── market_forecasts.json
    └── developer_profiles.json
```

**Processing Steps**:
1. **Tenant Isolation**: Separate data by agency
2. **Shared Resources**: Common market data accessible to all
3. **Access Control**: Agency-specific data access
4. **Data Aggregation**: Combined insights across agencies
5. **Result**: Multi-tenant knowledge base with proper isolation

**Usage**:
```python
# Process tenant-specific data
for agency in ["agency_1", "agency_2"]:
    results = pipeline.process_directory(
        f"multi_tenant_data/{agency}/",
        tenant_id=agency
    )

# Process shared data
shared_results = pipeline.process_directory(
    "multi_tenant_data/shared/",
    tenant_id="shared"
)
```

## 🎯 Demo Scenarios by Complexity

### **Beginner Demo (5 minutes)**
1. Upload `simple_properties.csv`
2. Show automatic schema detection
3. Demonstrate chat query: "Show me properties in Dubai Marina"
4. Display storage locations

### **Intermediate Demo (15 minutes)**
1. Process mixed content directory
2. Show different processors in action
3. Demonstrate web scraping
4. Show API integration
5. Generate ingestion report

### **Advanced Demo (30 minutes)**
1. Enterprise-scale data processing
2. Real-time data pipeline setup
3. Multi-tenant data management
4. Performance monitoring
5. Comprehensive reporting

## 📊 Expected Results by Use Case

| Use Case | Files Processed | Data Volume | Processing Time | Storage Used |
|----------|----------------|-------------|-----------------|--------------|
| Light 1 | 1 CSV | 3 records | < 5 seconds | 1 table + 1 collection |
| Light 2 | 1 PDF | 1 document | < 10 seconds | 2 collections |
| Light 3 | 1 Excel | 2 sheets | < 15 seconds | 2 tables + 1 collection |
| Medium 4 | 1 URL | Live content | < 30 seconds | 2 collections |
| Medium 5 | 1 API | JSON data | < 20 seconds | 1 table + 1 collection |
| Medium 6 | 5 files | Mixed content | < 2 minutes | 4 tables + 5 collections |
| Heavy 7 | 100+ files | 10,000+ records | < 30 minutes | All tables + collections |
| Heavy 8 | Continuous | Real-time | Ongoing | Live updates |
| Heavy 9 | Multi-tenant | 50,000+ records | < 1 hour | Isolated + shared |

## 🚀 Getting Started

### **Prerequisites**
```bash
# Install required libraries
pip install pandas openpyxl PyPDF2 requests beautifulsoup4

# Activate virtual environment
.\venv\Scripts\activate
```

### **Quick Start**
```python
from scripts.unified_data_ingestion import UnifiedDataIngestionPipeline

# Initialize pipeline
pipeline = UnifiedDataIngestionPipeline()

# Start with light use case
result = pipeline.process_file("demo_data/simple_properties.csv")
print("Demo completed successfully!")
```

### **Next Steps**
1. **Try Light Use Cases**: Start with single file processing
2. **Experiment with Medium Use Cases**: Test mixed content processing
3. **Scale to Heavy Use Cases**: Implement enterprise scenarios
4. **Customize**: Adapt processors for your specific needs

The pipeline is designed to handle any scale of data ingestion, from simple single files to complex enterprise scenarios!
