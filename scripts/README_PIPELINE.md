# 🏗️ Real Estate Data Processing Pipeline

A comprehensive data processing system designed specifically for Dubai real estate data. This pipeline handles ingestion, cleaning, enrichment, and storage of property data with role-based access control and market intelligence.

## 🎯 Features

### ✅ **Data Ingestion**
- **Multiple Formats**: CSV, Excel, JSON, PDF, Web scraping
- **Batch Processing**: Process entire directories of files
- **Validation**: Automatic data quality checks
- **Error Handling**: Robust error recovery and logging

### ✅ **Data Cleaning & Validation**
- **Standardization**: Dubai area names, property types, developers
- **Data Validation**: Price ranges, bedroom counts, square footage
- **Duplicate Removal**: Intelligent duplicate detection
- **Quality Scoring**: Automated data quality assessment

### ✅ **Data Enrichment**
- **Market Intelligence**: Area-specific market data and trends
- **Investment Metrics**: ROI calculations, rental yields, appreciation rates
- **Property Classification**: Price classes, target markets, investment grades
- **Location Intelligence**: Amenity proximity, transportation scores, safety ratings

### ✅ **Data Storage**
- **PostgreSQL**: Structured property and market data
- **ChromaDB**: Semantic search capabilities
- **Role-Based Access**: Different data visibility per user role
- **Audit Trail**: Complete processing logs and statistics

### ✅ **Role-Based Access Control**
- **Manager**: Full access to all data
- **Listing Agent**: Full property details
- **Regular Agent**: Limited address information
- **Client**: Public information only

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA PROCESSING PIPELINE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   INPUT     │    │  PROCESSING │    │   OUTPUT    │         │
│  │   LAYER     │───▶│   LAYER     │───▶│   LAYER     │         │
│  │             │    │             │    │             │         │
│  │ • CSV Files │    │ • Cleaning  │    │ • PostgreSQL│         │
│  │ • Excel     │    │ • Validation│    │ • ChromaDB  │         │
│  │ • JSON      │    │ • Enrichment│    │ • Analytics │         │
│  │ • PDF       │    │ • Deduplication│  │ • Reports  │         │
│  │ • Web Data  │    │ • Standardization│ │ • Dashboards│        │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
scripts/
├── data_pipeline/
│   ├── __init__.py              # Package initialization
│   ├── ingestion.py             # Data ingestion layer
│   ├── cleaning.py              # Data cleaning & validation
│   ├── enrichment.py            # Data enrichment & intelligence
│   ├── storage.py               # Database storage layer
│   └── main.py                  # Pipeline orchestrator
├── config/
│   └── pipeline_config.yaml     # Configuration file
├── run_pipeline_example.py      # Usage examples
├── requirements_pipeline.txt    # Dependencies
└── README_PIPELINE.md          # This file
```

## 🚀 Quick Start

### 1. **Install Dependencies**

```bash
pip install -r requirements_pipeline.txt
```

### 2. **Configure Database**

Update `config/pipeline_config.yaml` with your database credentials:

```yaml
postgres:
  host: localhost
  database: real_estate
  user: postgres
  password: your_password
  port: 5432

chroma:
  host: localhost
  port: 8000
```

### 3. **Run the Pipeline**

```python
from data_pipeline import DataPipeline

# Initialize pipeline
pipeline = DataPipeline()

# Process a CSV file
result = pipeline.process_property_data("data/properties.csv")

# Check results
if result['success']:
    print(f"✅ Processed {result['records_stored']} properties")
else:
    print("❌ Processing failed:", result['errors'])
```

### 4. **Run Example Script**

```bash
python run_pipeline_example.py
```

## 📊 Data Format

### **Property Data Schema**

```csv
address,price_aed,bedrooms,bathrooms,square_feet,property_type,area,developer,completion_date,view,amenities,service_charges,agent,agency
"Marina Gate 1, Dubai Marina",2500000,2,2,1200,Apartment,Dubai Marina,Emaar Properties,2016,Sea View,"Pool,Gym,Parking",18000,"Ahmed Ali","Emaar Properties"
```

### **Market Data Schema**

```json
{
  "area": "Dubai Marina",
  "market_trend": "Stable",
  "average_price_per_sqft": 1200,
  "rental_yield": 6.5,
  "demand_level": "High",
  "market_volatility": "Low",
  "investment_grade": "A",
  "appreciation_rate": 3.5
}
```

## 🔧 Configuration

### **Pipeline Configuration**

The `pipeline_config.yaml` file contains:

- **Database Settings**: PostgreSQL and ChromaDB connections
- **Web Scraping**: Headers, rate limiting, retry settings
- **Data Validation**: Price ranges, field requirements
- **Market Data**: Area-specific market intelligence
- **Processing**: Batch sizes, timeouts, quality thresholds

### **Market Intelligence**

Pre-configured market data for major Dubai areas:

- Dubai Marina
- Downtown Dubai
- Palm Jumeirah
- Business Bay
- Dubai Hills Estate
- Jumeirah Beach Residence
- Dubai Silicon Oasis
- Dubai Sports City
- Dubai Production City
- Dubai Creek Harbour

## 📈 Usage Examples

### **Process Single File**

```python
pipeline = DataPipeline()
result = pipeline.process_property_data("data/properties.csv")
```

### **Batch Processing**

```python
# Process all CSV and JSON files in a directory
batch_result = pipeline.run_batch_processing("data/", ["csv", "json"])
```

### **Process Market Data**

```python
market_data = [
    {
        'area': 'Dubai Marina',
        'market_trend': 'Stable',
        'average_price_per_sqft': 1200,
        'rental_yield': 6.5,
        'demand_level': 'High',
        'investment_grade': 'A'
    }
]
result = pipeline.process_market_data(market_data)
```

### **Get Processing Statistics**

```python
stats = pipeline.get_processing_stats()
print(f"Total properties: {stats['total_properties']}")
print(f"Recent runs: {stats['recent_runs']}")
```

### **Role-Based Data Access**

```python
# Get properties filtered by user role
properties = pipeline.storage.get_properties_by_role(
    role="agent",  # client, agent, listing_agent, manager
    filters={
        'area': 'Dubai Marina',
        'min_price': 1000000,
        'max_price': 5000000
    }
)
```

## 🔍 Data Quality Features

### **Automatic Validation**

- **Price Validation**: Reasonable ranges for Dubai market
- **Bedroom/Bathroom Validation**: Logical count ranges
- **Square Footage Validation**: Realistic property sizes
- **Address Standardization**: Dubai area name normalization
- **Duplicate Detection**: Intelligent duplicate removal

### **Quality Metrics**

- **Completeness Score**: Percentage of required fields filled
- **Data Quality Score**: Overall data quality assessment
- **Validation Flags**: Detailed validation results
- **Processing Reports**: Comprehensive processing statistics

## 🛡️ Security & Access Control

### **Role-Based Access**

| Role | Address Visibility | Price Access | Market Data | Investment Metrics |
|------|-------------------|--------------|-------------|-------------------|
| Client | ❌ | ✅ | ✅ | ✅ |
| Agent | Partial | ✅ | ✅ | ✅ |
| Listing Agent | ✅ | ✅ | ✅ | ✅ |
| Manager | ✅ | ✅ | ✅ | ✅ |

### **Data Protection**

- **Address Masking**: Partial addresses for non-listing agents
- **Audit Logging**: Complete access and processing logs
- **Validation**: Input sanitization and validation
- **Error Handling**: Secure error messages

## 📊 Monitoring & Analytics

### **Processing Logs**

- **File Processing**: Success/failure rates
- **Data Quality**: Quality scores and validation results
- **Performance**: Processing times and throughput
- **Errors**: Detailed error tracking and resolution

### **Statistics Dashboard**

- **Total Properties**: Database property count
- **Processing Runs**: Recent processing activity
- **Quality Metrics**: Average data quality scores
- **Performance**: Average processing times

## 🔄 Integration with Main System

### **Chat System Integration**

The processed data integrates with the main RAG chat system:

```python
# Query properties for chat responses
properties = pipeline.storage.get_properties_by_role("client", filters)

# Semantic search for property-related queries
search_results = pipeline.storage.search_properties_semantic(
    query="luxury apartments in Dubai Marina",
    role="client"
)
```

### **API Integration**

The pipeline can be integrated with the main FastAPI backend:

```python
# Add pipeline endpoints to main API
from data_pipeline import DataPipeline

@app.post("/api/process-data")
async def process_data(file_path: str):
    pipeline = DataPipeline()
    result = pipeline.process_property_data(file_path)
    return result
```

## 🚀 Advanced Features

### **Web Scraping Framework**

```python
# Process data from web sources
urls = [
    "https://propertyfinder.ae/dubai/properties-for-sale",
    "https://bayut.com/dubai/properties-for-sale"
]
result = pipeline.process_web_data(urls, "property_sites")
```

### **Market Intelligence**

```python
# Get market context for properties
market_context = pipeline.enricher._get_market_context(property_data)

# Calculate investment metrics
investment_metrics = pipeline.enricher._calculate_investment_metrics(property_data)
```

### **Batch Processing**

```python
# Process entire directories
batch_result = pipeline.run_batch_processing(
    input_directory="data/",
    file_types=["csv", "xlsx", "json"]
)
```

## 🐛 Troubleshooting

### **Common Issues**

1. **Database Connection Failed**
   - Check PostgreSQL and ChromaDB are running
   - Verify credentials in `pipeline_config.yaml`
   - Ensure ports are accessible

2. **Data Validation Errors**
   - Check data format matches expected schema
   - Verify price ranges are reasonable for Dubai market
   - Ensure required fields are present

3. **Processing Timeouts**
   - Increase timeout values in configuration
   - Reduce batch sizes for large datasets
   - Check system resources

### **Logging**

All processing activity is logged to `data_pipeline.log`:

```bash
tail -f data_pipeline.log
```

## 📚 Next Steps

### **Immediate Actions**

1. **Install Dependencies**: `pip install -r requirements_pipeline.txt`
2. **Configure Database**: Update `pipeline_config.yaml`
3. **Test Pipeline**: Run `python run_pipeline_example.py`
4. **Add Your Data**: Place property files in `data/` directory
5. **Process Data**: Run pipeline on your real estate data

### **Future Enhancements**

- **Web Scraping**: Add site-specific scrapers for Dubai property sites
- **API Integration**: Integrate with DLD and RERA APIs
- **Machine Learning**: Add predictive analytics and market forecasting
- **Real-time Updates**: Implement real-time data processing
- **Advanced Analytics**: Add market trend analysis and reporting

## 🤝 Support

For questions or issues:

1. Check the troubleshooting section
2. Review processing logs in `data_pipeline.log`
3. Validate pipeline configuration
4. Test with sample data first

---

**🎉 The Data Processing Pipeline is ready to transform your Dubai real estate data into intelligent, actionable insights!**
