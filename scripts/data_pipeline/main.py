"""
Data Processing Pipeline - Main Orchestrator

Coordinates the entire data processing pipeline from ingestion to storage.
"""

import logging
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml
import json

from .ingestion import DataIngestion
from .cleaning import DataCleaner
from .enrichment import DataEnricher
from .storage import DataStorage

class DataPipeline:
    """Main data processing pipeline orchestrator"""
    
    def __init__(self, config_path: str = "config/pipeline_config.yaml"):
        self.config = self._load_config(config_path)
        self.setup_logging()
        
        # Initialize components
        self.ingestion = DataIngestion(self.config)
        self.cleaner = DataCleaner(self.config)
        self.enricher = DataEnricher(self.config)
        self.storage = DataStorage(self.config)
        
        self.logger = logging.getLogger(__name__)
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load pipeline configuration"""
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            # Return default config
            return {
                'postgres': {
                    'host': 'localhost',
                    'database': 'real_estate',
                    'user': 'postgres',
                    'password': 'password',
                    'port': 5432
                },
                'chroma': {
                    'host': 'localhost',
                    'port': 8000
                },
                'web_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                },
                'rate_limiting': {
                    'requests_per_minute': 60,
                    'delay_between_requests': 1.0
                },
                'data_validation': {
                    'min_price': 100000,
                    'max_price': 100000000,
                    'min_bedrooms': 0,
                    'max_bedrooms': 10,
                    'required_fields': ['address', 'price_aed', 'property_type']
                }
            }
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('data_pipeline.log'),
                logging.StreamHandler()
            ]
        )
    
    def process_property_data(self, input_path: str) -> Dict[str, Any]:
        """Process property data from various sources"""
        start_time = time.time()
        processing_result = {
            'success': False,
            'source_file': input_path,
            'records_processed': 0,
            'records_stored': 0,
            'processing_time': 0,
            'errors': [],
            'warnings': [],
            'quality_metrics': {}
        }
        
        try:
            self.logger.info(f"Starting property data processing for: {input_path}")
            
            # 1. Data Ingestion
            self.logger.info("Step 1: Data Ingestion")
            ingested_data = self._ingest_data(input_path)
            if not ingested_data:
                processing_result['errors'].append("Failed to ingest data")
                return processing_result
            
            processing_result['records_processed'] = len(ingested_data)
            
            # 2. Data Cleaning
            self.logger.info("Step 2: Data Cleaning")
            cleaned_data = self.cleaner.clean_property_data(ingested_data)
            if not cleaned_data:
                processing_result['errors'].append("Failed to clean data")
                return processing_result
            
            # Remove duplicates
            original_count = len(cleaned_data)
            cleaned_data = self.cleaner.remove_duplicates(cleaned_data)
            duplicates_removed = original_count - len(cleaned_data)
            
            if duplicates_removed > 0:
                processing_result['warnings'].append(f"Removed {duplicates_removed} duplicate records")
            
            # 3. Data Enrichment
            self.logger.info("Step 3: Data Enrichment")
            enriched_data = self.enricher.enrich_property_data(cleaned_data)
            if not enriched_data:
                processing_result['errors'].append("Failed to enrich data")
                return processing_result
            
            # 4. Data Storage
            self.logger.info("Step 4: Data Storage")
            self.storage.connect_databases()
            self.storage.create_tables_if_not_exist()
            
            pg_success = self.storage.store_properties_postgres(enriched_data)
            chroma_success = self.storage.store_properties_chroma(enriched_data)
            
            if pg_success and chroma_success:
                processing_result['records_stored'] = len(enriched_data)
                processing_result['success'] = True
                self.logger.info("Property data processing completed successfully")
            else:
                processing_result['errors'].append("Failed to store data in databases")
            
            # 5. Generate quality metrics
            validation_flags = [item.get('validation_flags', {}) for item in enriched_data]
            quality_report = self.cleaner.generate_cleaning_report(
                processing_result['records_processed'],
                processing_result['records_stored'],
                validation_flags
            )
            processing_result['quality_metrics'] = quality_report
            
            # 6. Log processing result
            processing_time = time.time() - start_time
            processing_result['processing_time'] = processing_time
            
            self.storage.log_processing_result(
                input_path,
                processing_result['records_processed'],
                processing_result['records_stored'],
                processing_time,
                'SUCCESS' if processing_result['success'] else 'FAILED',
                processing_result['errors']
            )
            
            self.storage.close_connections()
            
        except Exception as e:
            processing_result['errors'].append(f"Unexpected error: {str(e)}")
            self.logger.error(f"Error in property data processing: {e}")
            
            # Log failed processing
            processing_time = time.time() - start_time
            processing_result['processing_time'] = processing_time
            
            try:
                self.storage.log_processing_result(
                    input_path,
                    processing_result['records_processed'],
                    processing_result['records_stored'],
                    processing_time,
                    'FAILED',
                    processing_result['errors']
                )
            except:
                pass
        
        return processing_result
    
    def process_web_data(self, urls: List[str], scraper_type: str) -> Dict[str, Any]:
        """Process data from web sources"""
        start_time = time.time()
        processing_result = {
            'success': False,
            'source_type': 'web',
            'urls_processed': len(urls),
            'records_processed': 0,
            'records_stored': 0,
            'processing_time': 0,
            'errors': [],
            'warnings': []
        }
        
        try:
            self.logger.info(f"Starting web data processing for {len(urls)} URLs")
            
            all_data = []
            
            for url in urls:
                try:
                    web_data = self.ingestion.ingest_web_data(url, scraper_type)
                    if web_data:
                        # Process web data (would need specific parsers for each site)
                        processed_data = self._process_web_data(web_data)
                        all_data.extend(processed_data)
                    else:
                        processing_result['warnings'].append(f"Failed to scrape {url}")
                except Exception as e:
                    processing_result['errors'].append(f"Error processing {url}: {str(e)}")
                    continue
            
            if all_data:
                processing_result['records_processed'] = len(all_data)
                
                # Clean and enrich web data
                cleaned_data = self.cleaner.clean_property_data(all_data)
                enriched_data = self.enricher.enrich_property_data(cleaned_data)
                
                # Store data
                self.storage.connect_databases()
                pg_success = self.storage.store_properties_postgres(enriched_data)
                chroma_success = self.storage.store_properties_chroma(enriched_data)
                self.storage.close_connections()
                
                if pg_success and chroma_success:
                    processing_result['records_stored'] = len(enriched_data)
                    processing_result['success'] = True
                else:
                    processing_result['errors'].append("Failed to store web data")
            else:
                processing_result['errors'].append("No data extracted from web sources")
            
            processing_result['processing_time'] = time.time() - start_time
            
        except Exception as e:
            processing_result['errors'].append(f"Unexpected error: {str(e)}")
            self.logger.error(f"Error in web data processing: {e}")
        
        return processing_result
    
    def process_market_data(self, market_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process market intelligence data"""
        start_time = time.time()
        processing_result = {
            'success': False,
            'source_type': 'market_data',
            'records_processed': len(market_data),
            'records_stored': 0,
            'processing_time': 0,
            'errors': []
        }
        
        try:
            self.logger.info(f"Processing {len(market_data)} market data records")
            
            # Store market data
            self.storage.connect_databases()
            
            pg_success = self.storage.store_market_data_postgres(market_data)
            chroma_success = self.storage.store_market_data_chroma(market_data)
            
            self.storage.close_connections()
            
            if pg_success and chroma_success:
                processing_result['records_stored'] = len(market_data)
                processing_result['success'] = True
                self.logger.info("Market data processing completed successfully")
            else:
                processing_result['errors'].append("Failed to store market data")
            
            processing_result['processing_time'] = time.time() - start_time
            
        except Exception as e:
            processing_result['errors'].append(f"Unexpected error: {str(e)}")
            self.logger.error(f"Error in market data processing: {e}")
        
        return processing_result
    
    def _ingest_data(self, input_path: str) -> List[Dict[str, Any]]:
        """Ingest data based on file type"""
        path = Path(input_path)
        
        if path.suffix.lower() == '.csv':
            data = self.ingestion.ingest_csv(input_path)
            return data.get('data', []) if data else []
        
        elif path.suffix.lower() == '.xlsx':
            data = self.ingestion.ingest_excel(input_path)
            # Combine all sheets
            combined_data = []
            for sheet_data in data.get('sheets', {}).values():
                combined_data.extend(sheet_data.get('data', []))
            return combined_data
        
        elif path.suffix.lower() == '.json':
            data = self.ingestion.ingest_json(input_path)
            if isinstance(data.get('data'), list):
                return data.get('data', [])
            else:
                return [data.get('data', {})]
        
        elif path.suffix.lower() == '.pdf':
            data = self.ingestion.ingest_pdf(input_path)
            # PDF processing would need more sophisticated parsing
            # For now, return empty list
            return []
        
        else:
            self.logger.error(f"Unsupported file type: {path.suffix}")
            return []
    
    def _process_web_data(self, web_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process web scraped data (placeholder for site-specific parsers)"""
        # This would contain site-specific parsing logic
        # For now, return empty list
        return []
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get overall processing statistics"""
        try:
            self.storage.connect_databases()
            stats = self.storage.get_processing_stats()
            self.storage.close_connections()
            return stats
        except Exception as e:
            self.logger.error(f"Error getting processing stats: {e}")
            return {}
    
    def validate_pipeline(self) -> Dict[str, Any]:
        """Validate pipeline configuration and connections"""
        validation_result = {
            'config_valid': True,
            'database_connections': False,
            'components_initialized': True,
            'errors': []
        }
        
        # Validate configuration
        required_configs = ['postgres', 'chroma']
        for config in required_configs:
            if config not in self.config:
                validation_result['config_valid'] = False
                validation_result['errors'].append(f"Missing {config} configuration")
        
        # Test database connections
        try:
            self.storage.connect_databases()
            validation_result['database_connections'] = True
            self.storage.close_connections()
        except Exception as e:
            validation_result['database_connections'] = False
            validation_result['errors'].append(f"Database connection failed: {str(e)}")
        
        return validation_result
    
    def run_batch_processing(self, input_directory: str, file_types: List[str] = None) -> Dict[str, Any]:
        """Run batch processing on all files in a directory"""
        if file_types is None:
            file_types = ['csv', 'xlsx', 'json']
        
        batch_result = {
            'total_files': 0,
            'successful_files': 0,
            'failed_files': 0,
            'total_records_processed': 0,
            'total_records_stored': 0,
            'processing_time': 0,
            'file_results': []
        }
        
        start_time = time.time()
        
        try:
            # Get all files of specified types
            directory = Path(input_directory)
            files_to_process = []
            
            for file_type in file_types:
                files_to_process.extend(directory.glob(f"*.{file_type}"))
                files_to_process.extend(directory.glob(f"*.{file_type.upper()}"))
            
            batch_result['total_files'] = len(files_to_process)
            
            for file_path in files_to_process:
                try:
                    self.logger.info(f"Processing file: {file_path}")
                    result = self.process_property_data(str(file_path))
                    
                    batch_result['file_results'].append({
                        'file': str(file_path),
                        'success': result['success'],
                        'records_processed': result['records_processed'],
                        'records_stored': result['records_stored'],
                        'errors': result['errors']
                    })
                    
                    if result['success']:
                        batch_result['successful_files'] += 1
                        batch_result['total_records_processed'] += result['records_processed']
                        batch_result['total_records_stored'] += result['records_stored']
                    else:
                        batch_result['failed_files'] += 1
                        
                except Exception as e:
                    batch_result['failed_files'] += 1
                    batch_result['file_results'].append({
                        'file': str(file_path),
                        'success': False,
                        'records_processed': 0,
                        'records_stored': 0,
                        'errors': [str(e)]
                    })
            
            batch_result['processing_time'] = time.time() - start_time
            
        except Exception as e:
            batch_result['errors'] = [str(e)]
            self.logger.error(f"Error in batch processing: {e}")
        
        return batch_result

# Usage example
if __name__ == "__main__":
    pipeline = DataPipeline()
    
    # Validate pipeline
    validation = pipeline.validate_pipeline()
    print(f"Pipeline validation: {validation}")
    
    # Process CSV file
    result = pipeline.process_property_data("data/real_properties.csv")
    print(f"Processing result: {result}")
    
    # Get processing stats
    stats = pipeline.get_processing_stats()
    print(f"Processing stats: {stats}")
