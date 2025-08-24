#!/usr/bin/env python3
"""
PostgreSQL Storage Handler for Dubai Real Estate Research
Stores structured data from data ingestion pipeline into PostgreSQL tables
"""

import os
import sys
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import json

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class PostgresStorage:
    """PostgreSQL storage handler for structured data"""
    
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.engine = create_engine(db_url)
        
        # Table mapping for different data types
        self.table_mapping = {
            "market_data": "market_data",
            "properties": "properties",
            "regulatory_updates": "regulatory_updates",
            "developers": "developers",
            "investment_insights": "investment_insights",
            "neighborhood_profiles": "neighborhood_profiles"
        }
        
        # Column mapping for each table
        self.column_mapping = {
            "market_data": {
                "date": "date",
                "neighborhood": "neighborhood",
                "property_type": "property_type",
                "avg_price_per_sqft": "avg_price_per_sqft",
                "transaction_volume": "transaction_volume",
                "rental_yield": "rental_yield",
                "market_trend": "market_trend",
                "price_change_percent": "price_change_percent",
                "off_plan_percentage": "off_plan_percentage",
                "foreign_investment_percentage": "foreign_investment_percentage"
            },
            "properties": {
                "address": "address",
                "price": "price",
                "bedrooms": "bedrooms",
                "bathrooms": "bathrooms",
                "square_feet": "square_feet",
                "property_type": "property_type",
                "description": "description",
                "neighborhood": "neighborhood",
                "developer": "developer",
                "completion_date": "completion_date",
                "rental_yield": "rental_yield",
                "property_status": "property_status",
                "amenities": "amenities",
                "market_segment": "market_segment",
                "freehold_status": "freehold_status",
                "service_charges": "service_charges",
                "parking_spaces": "parking_spaces"
            },
            "regulatory_updates": {
                "law_name": "law_name",
                "enactment_date": "enactment_date",
                "description": "description",
                "status": "status",
                "impact_areas": "impact_areas",
                "key_provisions": "key_provisions",
                "compliance_requirements": "compliance_requirements",
                "relevant_stakeholders": "relevant_stakeholders"
            },
            "developers": {
                "name": "name",
                "market_share": "market_share",
                "reputation_score": "reputation_score",
                "financial_strength": "financial_strength",
                "total_projects": "total_projects",
                "avg_project_value": "avg_project_value",
                "specialties": "specialties",
                "key_projects": "key_projects",
                "type": "type"
            },
            "investment_insights": {
                "title": "title",
                "category": "category",
                "roi_projection": "roi_projection",
                "investment_amount_min": "investment_amount_min",
                "investment_amount_max": "investment_amount_max",
                "risk_level": "risk_level",
                "target_audience": "target_audience",
                "requirements": "requirements",
                "key_benefits": "key_benefits"
            },
            "neighborhood_profiles": {
                "name": "name",
                "description": "description",
                "location_data": "location_data",
                "amenities": "amenities",
                "price_ranges": "price_ranges",
                "rental_yields": "rental_yields",
                "market_trends": "market_trends",
                "target_audience": "target_audience",
                "pros": "pros",
                "cons": "cons",
                "investment_advice": "investment_advice",
                "transportation_links": "transportation_links",
                "schools_hospitals": "schools_hospitals"
            }
        }
    
    def store(self, data: Dict[str, Any], content_type: str, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Store processed data in PostgreSQL"""
        logger.info(f"Storing {content_type} data in PostgreSQL")
        
        try:
            # Determine target tables from strategy
            target_tables = strategy.get("tables", [])
            
            if not target_tables:
                logger.warning("No target tables specified in strategy")
                return {
                    "status": "skipped",
                    "message": "No target tables specified"
                }
            
            results = {}
            
            # Store data in each target table
            for table_name in target_tables:
                if table_name in self.table_mapping:
                    result = self._store_in_table(data, table_name)
                    results[table_name] = result
                else:
                    logger.warning(f"Unknown table: {table_name}")
                    results[table_name] = {
                        "status": "failed",
                        "error": f"Unknown table: {table_name}"
                    }
            
            return {
                "status": "success",
                "storage_type": "postgresql",
                "tables_processed": len(results),
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Error storing data in PostgreSQL: {e}")
            return {
                "status": "failed",
                "storage_type": "postgresql",
                "error": str(e)
            }
    
    def _store_in_table(self, data: Dict[str, Any], table_name: str) -> Dict[str, Any]:
        """Store data in a specific table"""
        logger.info(f"Storing data in table: {table_name}")
        
        try:
            # Get structured data
            structured_data = data.get("structured_data", {})
            records = structured_data.get("records", [])
            
            if not records:
                logger.warning(f"No records to store in {table_name}")
                return {
                    "status": "skipped",
                    "message": "No records to store",
                    "records_processed": 0
                }
            
            # Get column mapping for this table
            column_mapping = self.column_mapping.get(table_name, {})
            
            # Prepare data for insertion
            prepared_records = []
            for record in records:
                prepared_record = self._prepare_record_for_table(record, column_mapping, table_name)
                if prepared_record:
                    prepared_records.append(prepared_record)
            
            if not prepared_records:
                logger.warning(f"No valid records to store in {table_name}")
                return {
                    "status": "skipped",
                    "message": "No valid records to store",
                    "records_processed": 0
                }
            
            # Insert records into database
            inserted_count = self._insert_records(table_name, prepared_records, column_mapping)
            
            return {
                "status": "success",
                "table": table_name,
                "records_processed": len(prepared_records),
                "records_inserted": inserted_count,
                "message": f"Successfully inserted {inserted_count} records into {table_name}"
            }
            
        except Exception as e:
            logger.error(f"Error storing data in table {table_name}: {e}")
            return {
                "status": "failed",
                "table": table_name,
                "error": str(e)
            }
    
    def _prepare_record_for_table(self, record: Dict[str, Any], column_mapping: Dict[str, str], table_name: str) -> Optional[Dict[str, Any]]:
        """Prepare a record for insertion into a specific table"""
        prepared_record = {}
        
        for source_col, target_col in column_mapping.items():
            if source_col in record:
                value = record[source_col]
                
                # Handle special data types
                if table_name == "properties" and target_col == "amenities":
                    # Convert amenities to JSONB
                    if isinstance(value, str):
                        try:
                            prepared_record[target_col] = json.dumps({"amenities": value.split(",")})
                        except:
                            prepared_record[target_col] = json.dumps({"amenities": [value]})
                    else:
                        prepared_record[target_col] = json.dumps({"amenities": []})
                
                elif table_name == "neighborhood_profiles" and target_col in ["location_data", "amenities", "price_ranges", "rental_yields", "market_trends", "schools_hospitals"]:
                    # Convert to JSONB for neighborhood profiles
                    if isinstance(value, (dict, list)):
                        prepared_record[target_col] = json.dumps(value)
                    else:
                        prepared_record[target_col] = json.dumps({"data": str(value)})
                
                elif target_col in ["date", "enactment_date", "completion_date"]:
                    # Handle date fields
                    if value and str(value).strip():
                        try:
                            # Try to parse date
                            if isinstance(value, str):
                                prepared_record[target_col] = value
                            else:
                                prepared_record[target_col] = str(value)
                        except:
                            prepared_record[target_col] = None
                    else:
                        prepared_record[target_col] = None
                
                else:
                    # Handle regular fields
                    if value is not None and str(value).strip():
                        prepared_record[target_col] = value
                    else:
                        prepared_record[target_col] = None
        
        return prepared_record if prepared_record else None
    
    def _insert_records(self, table_name: str, records: List[Dict[str, Any]], column_mapping: Dict[str, str]) -> int:
        """Insert records into the database table"""
        if not records:
            return 0
        
        # Get target columns
        target_columns = list(column_mapping.values())
        
        # Build INSERT query
        columns_str = ", ".join(target_columns)
        placeholders = ", ".join([f":{col}" for col in target_columns])
        
        insert_query = f"""
        INSERT INTO {table_name} ({columns_str})
        VALUES ({placeholders})
        ON CONFLICT DO NOTHING
        """
        
        inserted_count = 0
        
        try:
            with self.engine.connect() as conn:
                for record in records:
                    try:
                        # Filter record to only include target columns
                        filtered_record = {col: record.get(col) for col in target_columns if col in record}
                        
                        if filtered_record:
                            result = conn.execute(text(insert_query), filtered_record)
                            if result.rowcount > 0:
                                inserted_count += 1
                        
                    except Exception as e:
                        logger.warning(f"Error inserting record into {table_name}: {e}")
                        continue
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error during batch insert into {table_name}: {e}")
            raise
        
        return inserted_count
    
    def _check_table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(f"""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = '{table_name}'
                    )
                """))
                return result.fetchone()[0]
        except Exception as e:
            logger.error(f"Error checking if table {table_name} exists: {e}")
            return False
    
    def _get_table_schema(self, table_name: str) -> Dict[str, str]:
        """Get the schema of a table"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(f"""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_schema = 'public' 
                    AND table_name = '{table_name}'
                    ORDER BY ordinal_position
                """))
                
                schema = {}
                for row in result:
                    schema[row[0]] = row[1]
                
                return schema
        except Exception as e:
            logger.error(f"Error getting schema for table {table_name}: {e}")
            return {}
    
    def validate_data_compatibility(self, data: Dict[str, Any], table_name: str) -> Dict[str, Any]:
        """Validate if data is compatible with table schema"""
        if not self._check_table_exists(table_name):
            return {
                "compatible": False,
                "error": f"Table {table_name} does not exist"
            }
        
        # Get table schema
        table_schema = self._get_table_schema(table_name)
        
        if not table_schema:
            return {
                "compatible": False,
                "error": f"Could not retrieve schema for table {table_name}"
            }
        
        # Get column mapping
        column_mapping = self.column_mapping.get(table_name, {})
        
        # Check if required columns exist
        missing_columns = []
        for target_col in column_mapping.values():
            if target_col not in table_schema:
                missing_columns.append(target_col)
        
        if missing_columns:
            return {
                "compatible": False,
                "error": f"Missing columns in table {table_name}: {missing_columns}"
            }
        
        return {
            "compatible": True,
            "table_schema": table_schema,
            "column_mapping": column_mapping
        }
