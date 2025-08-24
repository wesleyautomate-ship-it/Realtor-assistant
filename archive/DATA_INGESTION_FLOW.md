# 🔄 Data Ingestion Flow Diagram

## Complete Data Flow

```
📁 Your Data Files
    │
    ├── 📊 CSV Files (market_data.csv, properties.csv, etc.)
    ├── 📄 PDF Files (reports.pdf, regulations.pdf)
    ├── 📈 Excel Files (financial_data.xlsx)
    ├── 🌐 Web Content (market_forecasts.html)
    └── 🔌 API Data (developer_profiles.json)
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│                    UNIFIED DATA INGESTION PIPELINE          │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
🔍 CONTENT TYPE DETECTION
    │
    ├── 📊 CSV → "csv"
    ├── 📄 PDF → "pdf" 
    ├── 📈 Excel → "excel"
    ├── 🌐 Web → "web"
    └── 🔌 API → "api"
    │
    ▼
⚙️ FILE PROCESSING
    │
    ├── 📊 CSV Processor
    │   ├── Schema Detection (market_data, properties, etc.)
    │   ├── Data Cleaning
    │   └── Structured Data Extraction
    │
    ├── 📄 PDF Processor
    │   ├── Text Extraction
    │   ├── Document Classification
    │   └── Content Analysis
    │
    ├── 📈 Excel Processor
    │   ├── Multi-sheet Processing
    │   ├── Financial Data Extraction
    │   └── Complex Data Handling
    │
    ├── 🌐 Web Processor
    │   ├── HTML Parsing
    │   ├── Content Scraping
    │   └── Market Data Extraction
    │
    └── 🔌 API Processor
        ├── JSON Processing
        ├── Real-time Data Handling
        └── Developer Profile Extraction
    │
    ▼
✅ DATA VALIDATION
    │
    ├── Schema Validation (required columns, data types)
    ├── Quality Checker (data ranges, consistency)
    └── Duplicate Detector (identify duplicates)
    │
    ▼
🎯 STORAGE STRATEGY DETERMINATION
    │
    ├── CSV Files:
    │   ├── market_data → PostgreSQL: market_data table
    │   ├── properties → PostgreSQL: properties table
    │   ├── regulatory_updates → PostgreSQL: regulatory_updates table
    │   ├── developers → PostgreSQL: developers table
    │   └── investment_insights → PostgreSQL: investment_insights table
    │
    ├── PDF Files:
    │   ├── Market reports → ChromaDB: market_analysis collection
    │   ├── Regulations → ChromaDB: regulatory_framework collection
    │   └── Transaction guides → ChromaDB: transaction_guidance collection
    │
    ├── Excel Files:
    │   ├── Financial data → PostgreSQL: market_data, investment_insights
    │   └── ChromaDB: financial_insights collection
    │
    ├── Web Content:
    │   ├── Market forecasts → ChromaDB: market_forecasts collection
    │   └── Agent resources → ChromaDB: agent_resources collection
    │
    └── API Data:
        ├── Developer profiles → PostgreSQL: developers table
        ├── Neighborhood data → PostgreSQL: neighborhood_profiles table
        └── ChromaDB: developer_profiles, neighborhood_profiles collections
    │
    ▼
💾 STORAGE EXECUTION
    │
    ├── 🗄️ PostgreSQL Storage
    │   ├── Structured data storage
    │   ├── Relational queries
    │   └── Data integrity
    │
    └── 🔍 ChromaDB Storage
        ├── Semantic search
        ├── Vector embeddings
        └── Document retrieval
    │
    ▼
📊 INGESTION REPORT
    │
    ├── Processing statistics
    ├── Success/failure rates
    ├── Data quality metrics
    └── Storage locations
    │
    ▼
🎯 READY FOR RAG QUERIES
    │
    ├── Chat interface can now access:
    │   ├── Structured data from PostgreSQL
    │   └── Semantic content from ChromaDB
    │
    └── Users can ask questions like:
        ├── "What's the average price in Dubai Marina?"
        ├── "Show me recent regulatory changes"
        ├── "Which developers are most reliable?"
        └── "What are the best investment opportunities?"
```

## Key Decision Points

### 1. **Content Type Detection**
- **File Extension**: Primary method (`.csv`, `.pdf`, `.xlsx`)
- **File Header**: Fallback for unknown extensions
- **Content Analysis**: For ambiguous files

### 2. **Schema Detection (CSV Only)**
- **Column Analysis**: Checks for required columns
- **Pattern Matching**: Identifies data patterns
- **Content Validation**: Ensures data makes sense

### 3. **Storage Strategy**
- **Content Type Rules**: Different types go to different places
- **Schema-Specific Routing**: CSV schemas determine PostgreSQL tables
- **Dual Storage**: Most data goes to both PostgreSQL (structured) and ChromaDB (searchable)

### 4. **Quality Gates**
- **Validation**: Ensures data meets requirements
- **Cleaning**: Fixes common data issues
- **Deduplication**: Prevents duplicate entries

## Example: Processing `dubai_marina_prices.csv`

```
1. 📁 File: dubai_marina_prices.csv
   │
2. 🔍 Detection: .csv extension → "csv" content type
   │
3. ⚙️ Processing: CSV Processor
   ├── Columns: date, neighborhood, property_type, avg_price_per_sqft
   ├── Schema Detection: "market_data" (has date + neighborhood)
   └── Data Cleaning: Remove duplicates, fix data types
   │
4. ✅ Validation: Schema valid, quality checks pass
   │
5. 🎯 Strategy: 
   ├── PostgreSQL: market_data table
   └── ChromaDB: market_analysis collection
   │
6. 💾 Storage:
   ├── Structured data → PostgreSQL for queries
   └── Text content → ChromaDB for semantic search
   │
7. 📊 Result: Data now searchable via chat interface
```

## Benefits of This Flow

1. **Automatic**: No manual intervention required
2. **Intelligent**: Makes smart decisions about data organization
3. **Flexible**: Handles multiple file types and formats
4. **Reliable**: Built-in validation and error handling
5. **Scalable**: Easy to add new data types and storage locations
6. **Auditable**: Complete tracking of data processing
