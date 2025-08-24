# 📥 Data Ingestion Pipeline Guide

## Overview

The data ingestion pipeline is a sophisticated system that automatically processes, validates, and stores different types of data into the appropriate storage systems. Here's how it works:

## 🔄 How Data Ingestion Works

### 1. **Content Type Detection**
The pipeline first determines what type of file you're uploading:

```python
def detect_content_type(self, file_path: str) -> str:
    # Checks file extension (.csv, .pdf, .xlsx, etc.)
    # For unknown extensions, reads file header to detect type
    # Returns: "csv", "pdf", "excel", "web", "api", or "unknown"
```

**Examples:**
- `market_data.csv` → `"csv"`
- `regulations.pdf` → `"pdf"`
- `developers.xlsx` → `"excel"`

### 2. **File Processing**
Each file type has a specialized processor:

#### **CSV Processor** (`scripts/processors/csv_processor.py`)
- **Schema Detection**: Automatically identifies what type of data the CSV contains
- **Supported Schemas**:
  - `market_data` (price trends, transaction volumes)
  - `properties` (property listings)
  - `regulatory_updates` (law changes)
  - `developers` (developer information)
  - `investment_insights` (investment opportunities)

#### **PDF Processor** (placeholder)
- Extracts text from PDF documents
- Identifies regulatory documents, market reports, etc.

#### **Excel Processor** (placeholder)
- Processes Excel files with multiple sheets
- Handles complex financial data

### 3. **Data Validation**
The pipeline validates data quality:
- **Schema Validation**: Ensures required columns are present
- **Quality Checker**: Validates data types and ranges
- **Duplicate Detector**: Identifies duplicate records

### 4. **Storage Strategy Determination**
The system automatically decides where to store your data:

```python
def _determine_storage_strategy(self, content_type: str, validation_results: Dict[str, Any]) -> Dict[str, Any]:
    if content_type == "csv":
        strategy["postgres"] = {"tables": ["market_data", "properties"]}
        strategy["chromadb"] = {"collections": ["market_analysis"]}
    elif content_type == "pdf":
        strategy["chromadb"] = {"collections": ["regulatory_framework", "transaction_guidance"]}
    # ... more rules
```

## 🗂️ How Data Organization Works

### **Storage Decision Matrix**

| File Type | Content | PostgreSQL Tables | ChromaDB Collections |
|-----------|---------|-------------------|---------------------|
| **CSV** | Market data, property listings | `market_data`, `properties` | `market_analysis` |
| **CSV** | Regulatory updates | `regulatory_updates` | `regulatory_framework` |
| **CSV** | Developer info | `developers` | `developer_profiles` |
| **CSV** | Investment insights | `investment_insights` | `financial_insights` |
| **PDF** | Market reports | - | `market_analysis`, `regulatory_framework` |
| **PDF** | Transaction guides | - | `transaction_guidance` |
| **Excel** | Financial data | `market_data`, `investment_insights` | `financial_insights` |
| **Web** | Market forecasts | - | `market_forecasts`, `agent_resources` |
| **API** | Developer profiles | `developers`, `neighborhood_profiles` | `developer_profiles`, `neighborhood_profiles` |

### **Schema Detection Logic**

The CSV processor automatically detects what type of data you're uploading:

```python
def _detect_schema_type(self, df: pd.DataFrame) -> str:
    # Checks column names to determine schema
    if "date" in df.columns and "neighborhood" in df.columns:
        return "market_data"
    elif "address" in df.columns and "price" in df.columns:
        return "properties"
    elif "law_name" in df.columns:
        return "regulatory_updates"
    # ... more detection rules
```

## 📊 Data Flow Example

Let's trace a typical data ingestion:

### **Step 1: Upload `dubai_marina_prices.csv`**
```csv
date,neighborhood,property_type,avg_price_per_sqft,transaction_volume
2024-01-01,Dubai Marina,Apartment,1200.50,45
2024-01-02,Dubai Marina,Penthouse,1800.75,23
```

### **Step 2: Content Detection**
- File extension: `.csv` → Content type: `"csv"`

### **Step 3: Schema Detection**
- Columns: `date`, `neighborhood`, `property_type` → Schema: `"market_data"`

### **Step 4: Processing**
- Clean data (remove duplicates, fix data types)
- Extract structured information
- Generate metadata

### **Step 5: Storage Strategy**
```python
strategy = {
    "postgres": {
        "tables": ["market_data", "properties"]
    },
    "chromadb": {
        "collections": ["market_analysis"]
    }
}
```

### **Step 6: Storage Execution**
- **PostgreSQL**: Data goes to `market_data` table
- **ChromaDB**: Text content goes to `market_analysis` collection for semantic search

## 🎯 How to Use the Pipeline

### **Method 1: Single File Processing**
```python
from scripts.unified_data_ingestion import UnifiedDataIngestionPipeline

pipeline = UnifiedDataIngestionPipeline()
result = pipeline.process_file("path/to/your/data.csv")
```

### **Method 2: Directory Processing**
```python
# Process all files in a directory
results = pipeline.process_directory("path/to/data/folder")
```

### **Method 3: Command Line**
```bash
python scripts/unified_data_ingestion.py --input path/to/data --output report.json
```

## 🔧 Customization Options

### **Adding New Data Types**
1. **Create a new processor** in `scripts/processors/`
2. **Update storage strategy** in `_determine_storage_strategy()`
3. **Add table mappings** in `PostgresStorage`

### **Modifying Storage Rules**
Edit the `_determine_storage_strategy()` method to change where different file types are stored.

### **Adding Validation Rules**
Create new validators in `scripts/validators/` for custom data quality checks.

## 📈 Benefits of This System

1. **Automatic Organization**: No manual sorting required
2. **Intelligent Routing**: Data goes to the right place automatically
3. **Quality Assurance**: Built-in validation prevents bad data
4. **Scalable**: Easy to add new data types and storage locations
5. **Auditable**: Complete tracking of what was processed and where it went

## 🚀 Next Steps

The pipeline is ready to handle your Dubai real estate data! Simply:

1. **Prepare your data** in CSV, PDF, or Excel format
2. **Upload to the pipeline** using any of the methods above
3. **Review the ingestion report** to see where your data was stored
4. **Query your data** through the RAG system

The system will automatically organize everything and make it searchable through the chat interface!
