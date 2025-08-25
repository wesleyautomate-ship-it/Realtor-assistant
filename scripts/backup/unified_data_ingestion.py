#!/usr/bin/env python3
"""
Unified Data Ingestion Pipeline for Dubai Real Estate Research
Main orchestration script for processing multiple content types
"""

import os
import sys
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import json

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from dotenv import load_dotenv
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class UnifiedDataIngestionPipeline:
    """
    Main orchestration class for unified data ingestion pipeline
    Handles multiple content types and routes to appropriate processors
    """
    
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/real_estate_db")
        self.chroma_client = None
        self.processors = {}
        self.validators = {}
        self.storage_handlers = {}
        self.ingestion_stats = {
            "total_files": 0,
            "processed_files": 0,
            "failed_files": 0,
            "start_time": None,
            "end_time": None,
            "errors": []
        }
        
        # Initialize components
        self._initialize_processors()
        self._initialize_validators()
        self._initialize_storage_handlers()
    
    def _initialize_processors(self):
        """Initialize content type processors"""
        logger.info("Initializing content type processors...")
        
        # Import processors
        try:
            from processors.csv_processor import CSVProcessor
            self.processors = {"csv": CSVProcessor()}
            logger.info("✅ CSV processor initialized successfully")
        except ImportError as e:
            logger.warning(f"⚠️ CSV processor not available: {e}")
            self.processors = {"csv": PlaceholderProcessor("CSV")}
        
        try:
            from processors.pdf_processor import PDFProcessor
            self.processors["pdf"] = PDFProcessor()
            logger.info("✅ PDF processor initialized successfully")
        except ImportError as e:
            logger.warning(f"⚠️ PDF processor not available: {e}")
            self.processors["pdf"] = PlaceholderProcessor("PDF")
        
        try:
            from processors.excel_processor import ExcelProcessor
            self.processors["excel"] = ExcelProcessor()
            logger.info("✅ Excel processor initialized successfully")
        except ImportError as e:
            logger.warning(f"⚠️ Excel processor not available: {e}")
            self.processors["excel"] = PlaceholderProcessor("Excel")
        
        try:
            from processors.web_processor import WebProcessor
            self.processors["web"] = WebProcessor()
            logger.info("✅ Web processor initialized successfully")
        except ImportError as e:
            logger.warning(f"⚠️ Web processor not available: {e}")
            self.processors["web"] = PlaceholderProcessor("Web")
        
        try:
            from processors.api_processor import APIProcessor
            self.processors["api"] = APIProcessor()
            logger.info("✅ API processor initialized successfully")
        except ImportError as e:
            logger.warning(f"⚠️ API processor not available: {e}")
            self.processors["api"] = PlaceholderProcessor("API")
    
    def _initialize_validators(self):
        """Initialize data validators"""
        logger.info("Initializing data validators...")
        
        try:
            from validators.schema_validator import SchemaValidator
            from validators.quality_checker import QualityChecker
            from validators.duplicate_detector import DuplicateDetector
            
            self.validators = {
                "schema": SchemaValidator(),
                "quality": QualityChecker(),
                "duplicates": DuplicateDetector()
            }
            logger.info("✅ All validators initialized successfully")
        except ImportError as e:
            logger.warning(f"⚠️ Some validators not available: {e}")
            # Create placeholder validators for now
            self.validators = {
                "schema": PlaceholderValidator("Schema"),
                "quality": PlaceholderValidator("Quality"),
                "duplicates": PlaceholderValidator("Duplicates")
            }
    
    def _initialize_storage_handlers(self):
        """Initialize storage handlers"""
        logger.info("Initializing storage handlers...")
        
        try:
            from storage.postgres_storage import PostgresStorage
            from storage.chromadb_storage import ChromaDBStorage
            from storage.data_mapper import DataMapper
            
            self.storage_handlers = {
                "postgres": PostgresStorage(self.db_url),
                "chromadb": ChromaDBStorage(),
                "mapper": DataMapper()
            }
            logger.info("✅ All storage handlers initialized successfully")
        except ImportError as e:
            logger.warning(f"⚠️ Some storage handlers not available: {e}")
            # Create placeholder storage handlers for now
            self.storage_handlers = {
                "postgres": PlaceholderStorage("PostgreSQL"),
                "chromadb": PlaceholderStorage("ChromaDB"),
                "mapper": PlaceholderStorage("DataMapper")
            }
    
    def detect_content_type(self, file_path: str) -> str:
        """Detect content type based on file extension and content"""
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        # File extension mapping
        extension_mapping = {
            ".pdf": "pdf",
            ".csv": "csv",
            ".xlsx": "excel",
            ".xls": "excel",
            ".json": "api",
            ".xml": "api",
            ".html": "web",
            ".htm": "web"
        }
        
        if extension in extension_mapping:
            return extension_mapping[extension]
        
        # Try to detect by content for unknown extensions
        try:
            with open(file_path, 'rb') as f:
                header = f.read(1024)
                
            if header.startswith(b'%PDF'):
                return "pdf"
            elif b'<html' in header.lower() or b'<!doctype' in header.lower():
                return "web"
            elif b'{' in header or b'[' in header:
                return "api"
            else:
                return "unknown"
        except Exception as e:
            logger.warning(f"Could not detect content type for {file_path}: {e}")
            return "unknown"
    
    def process_file(self, file_path: str, content_type: str = None) -> Dict[str, Any]:
        """Process a single file through the pipeline"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Detect content type if not provided
        if not content_type:
            content_type = self.detect_content_type(str(file_path))
        
        logger.info(f"Processing {file_path} as {content_type}")
        
        try:
            # Step 1: Process the file
            if content_type not in self.processors:
                raise ValueError(f"No processor available for content type: {content_type}")
            
            processor = self.processors[content_type]
            processed_data = processor.process(str(file_path))
            
            # Step 2: Validate the data
            validation_results = self._validate_data(processed_data, content_type)
            
            # Step 3: Store the data
            storage_results = self._store_data(processed_data, content_type, validation_results)
            
            return {
                "file_path": str(file_path),
                "content_type": content_type,
                "processed_data": processed_data,
                "validation_results": validation_results,
                "storage_results": storage_results,
                "status": "success"
            }
            
        except Exception as e:
            error_msg = f"Error processing {file_path}: {str(e)}"
            logger.error(error_msg)
            self.ingestion_stats["errors"].append(error_msg)
            return {
                "file_path": str(file_path),
                "content_type": content_type,
                "status": "failed",
                "error": str(e)
            }
    
    def _validate_data(self, data: Dict[str, Any], content_type: str) -> Dict[str, Any]:
        """Validate processed data"""
        validation_results = {}
        
        for validator_name, validator in self.validators.items():
            try:
                result = validator.validate(data, content_type)
                validation_results[validator_name] = result
            except Exception as e:
                logger.warning(f"Validation {validator_name} failed: {e}")
                validation_results[validator_name] = {"status": "failed", "error": str(e)}
        
        return validation_results
    
    def _store_data(self, data: Dict[str, Any], content_type: str, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Store processed data in appropriate storage systems"""
        storage_results = {}
        
        # Determine storage strategy based on content type and validation results
        storage_strategy = self._determine_storage_strategy(content_type, validation_results)
        
        for storage_name, storage_handler in self.storage_handlers.items():
            if storage_name in storage_strategy:
                try:
                    result = storage_handler.store(data, content_type, storage_strategy[storage_name])
                    storage_results[storage_name] = result
                except Exception as e:
                    logger.warning(f"Storage {storage_name} failed: {e}")
                    storage_results[storage_name] = {"status": "failed", "error": str(e)}
        
        return storage_results
    
    def _determine_storage_strategy(self, content_type: str, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Determine storage strategy based on content type and validation results"""
        strategy = {}
        
        # Default strategy based on content type
        if content_type == "csv":
            strategy["postgres"] = {"tables": ["market_data", "properties"]}
            strategy["chromadb"] = {"collections": ["market_analysis"]}
        elif content_type == "pdf":
            strategy["chromadb"] = {"collections": ["regulatory_framework", "transaction_guidance"]}
        elif content_type == "excel":
            strategy["postgres"] = {"tables": ["market_data", "investment_insights"]}
            strategy["chromadb"] = {"collections": ["market_analysis", "financial_insights"]}
        elif content_type == "web":
            strategy["chromadb"] = {"collections": ["market_forecasts", "agent_resources"]}
        elif content_type == "api":
            strategy["postgres"] = {"tables": ["developers", "neighborhood_profiles"]}
            strategy["chromadb"] = {"collections": ["developer_profiles", "neighborhood_profiles"]}
        
        return strategy
    
    def process_directory(self, directory_path: str, file_patterns: List[str] = None) -> Dict[str, Any]:
        """Process all files in a directory"""
        directory_path = Path(directory_path)
        
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        if not file_patterns:
            file_patterns = ["*.pdf", "*.csv", "*.xlsx", "*.xls", "*.json", "*.html"]
        
        # Find all matching files
        files_to_process = []
        for pattern in file_patterns:
            files_to_process.extend(directory_path.glob(pattern))
        
        logger.info(f"Found {len(files_to_process)} files to process in {directory_path}")
        
        # Initialize ingestion stats
        self.ingestion_stats = {
            "total_files": len(files_to_process),
            "processed_files": 0,
            "failed_files": 0,
            "start_time": datetime.now(),
            "end_time": None,
            "errors": []
        }
        
        results = []
        
        # Process each file
        for file_path in files_to_process:
            try:
                result = self.process_file(str(file_path))
                results.append(result)
                
                if result["status"] == "success":
                    self.ingestion_stats["processed_files"] += 1
                else:
                    self.ingestion_stats["failed_files"] += 1
                    
            except Exception as e:
                error_msg = f"Error processing {file_path}: {str(e)}"
                logger.error(error_msg)
                self.ingestion_stats["errors"].append(error_msg)
                self.ingestion_stats["failed_files"] += 1
                
                results.append({
                    "file_path": str(file_path),
                    "status": "failed",
                    "error": str(e)
                })
        
        self.ingestion_stats["end_time"] = datetime.now()
        
        return {
            "ingestion_stats": self.ingestion_stats,
            "results": results
        }
    
    def generate_ingestion_report(self) -> str:
        """Generate a comprehensive ingestion report"""
        if not self.ingestion_stats["start_time"]:
            return "No ingestion session to report"
        
        duration = self.ingestion_stats["end_time"] - self.ingestion_stats["start_time"]
        
        success_rate = (self.ingestion_stats['processed_files']/self.ingestion_stats['total_files']*100) if self.ingestion_stats['total_files'] > 0 else 0
        
        report = f"""
🧪 UNIFIED DATA INGESTION PIPELINE REPORT
{'='*60}

📊 Processing Summary:
   Total Files: {self.ingestion_stats['total_files']}
   Successfully Processed: {self.ingestion_stats['processed_files']}
   Failed: {self.ingestion_stats['failed_files']}
   Success Rate: {success_rate:.1f}%

⏱️ Performance:
   Start Time: {self.ingestion_stats['start_time']}
   End Time: {self.ingestion_stats['end_time']}
   Duration: {duration}

❌ Errors ({len(self.ingestion_stats['errors'])}):
"""
        
        for error in self.ingestion_stats['errors']:
            report += f"   - {error}\n"
        
        report += f"\n{'='*60}"
        return report


class PlaceholderProcessor:
    """Placeholder processor for content types not yet implemented"""
    
    def __init__(self, content_type: str):
        self.content_type = content_type
    
    def process(self, file_path: str) -> Dict[str, Any]:
        logger.info(f"Placeholder processing for {self.content_type}: {file_path}")
        return {
            "content_type": self.content_type,
            "file_path": file_path,
            "processed_at": datetime.now().isoformat(),
            "status": "placeholder",
            "data": f"Placeholder data for {self.content_type} file"
        }


class PlaceholderValidator:
    """Placeholder validator for validation modules not yet implemented"""
    
    def __init__(self, validator_type: str):
        self.validator_type = validator_type
    
    def validate(self, data: Dict[str, Any], content_type: str) -> Dict[str, Any]:
        logger.info(f"Placeholder validation for {self.validator_type}")
        return {
            "validator_type": self.validator_type,
            "status": "placeholder",
            "score": 0.8,
            "message": f"Placeholder validation for {self.validator_type}"
        }


class PlaceholderStorage:
    """Placeholder storage handler for storage modules not yet implemented"""
    
    def __init__(self, storage_type: str):
        self.storage_type = storage_type
    
    def store(self, data: Dict[str, Any], content_type: str, strategy: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Placeholder storage for {self.storage_type}")
        return {
            "storage_type": self.storage_type,
            "status": "placeholder",
            "message": f"Placeholder storage for {self.storage_type}"
        }


def main():
    """Main function to run the unified data ingestion pipeline"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Unified Data Ingestion Pipeline for Dubai Real Estate Research")
    parser.add_argument("--input", "-i", required=True, help="Input file or directory path")
    parser.add_argument("--content-type", "-t", help="Force content type detection")
    parser.add_argument("--patterns", "-p", nargs="+", help="File patterns to process (for directories)")
    
    args = parser.parse_args()
    
    # Initialize pipeline
    pipeline = UnifiedDataIngestionPipeline()
    
    input_path = Path(args.input)
    
    if input_path.is_file():
        # Process single file
        result = pipeline.process_file(str(input_path), args.content_type)
        print(f"File processing result: {result['status']}")
        if result['status'] == 'failed':
            print(f"Error: {result.get('error', 'Unknown error')}")
    elif input_path.is_dir():
        # Process directory
        results = pipeline.process_directory(str(input_path), args.patterns)
        print(pipeline.generate_ingestion_report())
    else:
        print(f"Error: {args.input} is not a valid file or directory")


if __name__ == "__main__":
    main()
