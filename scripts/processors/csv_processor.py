#!/usr/bin/env python3
"""
CSV Processor for Dubai Real Estate Research
Handles CSV files containing market data, property listings, regulatory info
"""

import pandas as pd
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import json
import re

logger = logging.getLogger(__name__)

class CSVProcessor:
    """Processor for CSV files containing Dubai real estate data"""
    
    def __init__(self):
        self.supported_schemas = {
            "market_data": {
                "required_columns": ["date", "neighborhood", "property_type"],
                "optional_columns": ["avg_price_per_sqft", "transaction_volume", "rental_yield", "market_trend"],
                "data_types": {
                    "date": "datetime",
                    "avg_price_per_sqft": "float",
                    "transaction_volume": "int",
                    "rental_yield": "float"
                }
            },
            "properties": {
                "required_columns": ["address", "price", "bedrooms", "bathrooms"],
                "optional_columns": ["neighborhood", "developer", "completion_date", "rental_yield"],
                "data_types": {
                    "price": "float",
                    "bedrooms": "int",
                    "bathrooms": "int",
                    "rental_yield": "float"
                }
            },
            "regulatory_updates": {
                "required_columns": ["law_name", "enactment_date"],
                "optional_columns": ["description", "status", "impact_areas"],
                "data_types": {
                    "enactment_date": "datetime"
                }
            },
            "developers": {
                "required_columns": ["name"],
                "optional_columns": ["market_share", "reputation_score", "total_projects"],
                "data_types": {
                    "market_share": "float",
                    "reputation_score": "float",
                    "total_projects": "int"
                }
            },
            "investment_insights": {
                "required_columns": ["title", "category"],
                "optional_columns": ["roi_projection", "investment_amount_min", "risk_level"],
                "data_types": {
                    "roi_projection": "float",
                    "investment_amount_min": "float",
                    "investment_amount_max": "float"
                }
            }
        }
    
    def process(self, file_path: str) -> Dict[str, Any]:
        """Process a CSV file and extract structured data"""
        logger.info(f"Processing CSV file: {file_path}")
        
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            logger.info(f"Loaded CSV with {len(df)} rows and {len(df.columns)} columns")
            
            # Detect schema type
            schema_type = self._detect_schema_type(df)
            logger.info(f"Detected schema type: {schema_type}")
            
            # Clean and validate data
            cleaned_df = self._clean_data(df, schema_type)
            
            # Extract structured data
            structured_data = self._extract_structured_data(cleaned_df, schema_type)
            
            # Generate metadata
            metadata = self._generate_metadata(df, schema_type, file_path)
            
            return {
                "content_type": "csv",
                "file_path": file_path,
                "schema_type": schema_type,
                "processed_at": datetime.now().isoformat(),
                "row_count": len(df),
                "column_count": len(df.columns),
                "structured_data": structured_data,
                "metadata": metadata,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error processing CSV file {file_path}: {e}")
            return {
                "content_type": "csv",
                "file_path": file_path,
                "status": "failed",
                "error": str(e)
            }
    
    def _detect_schema_type(self, df: pd.DataFrame) -> str:
        """Detect the schema type based on column names and data"""
        column_names = [col.lower() for col in df.columns]
        
        # Score each schema based on column matches
        schema_scores = {}
        
        for schema_name, schema_config in self.supported_schemas.items():
            score = 0
            required_cols = schema_config["required_columns"]
            optional_cols = schema_config["optional_columns"]
            
            # Check required columns
            for req_col in required_cols:
                if req_col in column_names:
                    score += 2  # Higher weight for required columns
                elif any(req_col in col for col in column_names):
                    score += 1
            
            # Check optional columns
            for opt_col in optional_cols:
                if opt_col in column_names:
                    score += 1
                elif any(opt_col in col for col in column_names):
                    score += 0.5
            
            schema_scores[schema_name] = score
        
        # Return the schema with highest score
        best_schema = max(schema_scores, key=schema_scores.get)
        
        # If no clear match, default to market_data
        if schema_scores[best_schema] < 1:
            return "market_data"
        
        return best_schema
    
    def _clean_data(self, df: pd.DataFrame, schema_type: str) -> pd.DataFrame:
        """Clean and standardize the data"""
        logger.info(f"Cleaning data for schema: {schema_type}")
        
        # Make a copy to avoid modifying original
        cleaned_df = df.copy()
        
        # Convert column names to lowercase
        cleaned_df.columns = cleaned_df.columns.str.lower()
        
        # Remove leading/trailing whitespace from string columns
        for col in cleaned_df.select_dtypes(include=['object']).columns:
            cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
        
        # Handle missing values
        cleaned_df = cleaned_df.fillna('')
        
        # Convert data types based on schema
        schema_config = self.supported_schemas.get(schema_type, {})
        data_types = schema_config.get("data_types", {})
        
        for col, dtype in data_types.items():
            if col in cleaned_df.columns:
                try:
                    if dtype == "datetime":
                        cleaned_df[col] = pd.to_datetime(cleaned_df[col], errors='coerce')
                    elif dtype == "float":
                        cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
                    elif dtype == "int":
                        cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce').astype('Int64')
                except Exception as e:
                    logger.warning(f"Could not convert column {col} to {dtype}: {e}")
        
        return cleaned_df
    
    def _extract_structured_data(self, df: pd.DataFrame, schema_type: str) -> Dict[str, Any]:
        """Extract structured data based on schema type"""
        logger.info(f"Extracting structured data for schema: {schema_type}")
        
        if schema_type == "market_data":
            return self._extract_market_data(df)
        elif schema_type == "properties":
            return self._extract_properties_data(df)
        elif schema_type == "regulatory_updates":
            return self._extract_regulatory_data(df)
        elif schema_type == "developers":
            return self._extract_developers_data(df)
        elif schema_type == "investment_insights":
            return self._extract_investment_data(df)
        else:
            return self._extract_generic_data(df)
    
    def _extract_market_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract market data specific information"""
        data = {
            "data_type": "market_data",
            "records": []
        }
        
        for _, row in df.iterrows():
            record = {
                "date": str(row.get("date", "")),
                "neighborhood": str(row.get("neighborhood", "")),
                "property_type": str(row.get("property_type", "")),
                "avg_price_per_sqft": float(row.get("avg_price_per_sqft", 0)) if pd.notna(row.get("avg_price_per_sqft")) else None,
                "transaction_volume": int(row.get("transaction_volume", 0)) if pd.notna(row.get("transaction_volume")) else None,
                "rental_yield": float(row.get("rental_yield", 0)) if pd.notna(row.get("rental_yield")) else None,
                "market_trend": str(row.get("market_trend", "")),
                "price_change_percent": float(row.get("price_change_percent", 0)) if pd.notna(row.get("price_change_percent")) else None
            }
            data["records"].append(record)
        
        return data
    
    def _extract_properties_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract properties specific information"""
        data = {
            "data_type": "properties",
            "records": []
        }
        
        for _, row in df.iterrows():
            record = {
                "address": str(row.get("address", "")),
                "price": float(row.get("price", 0)) if pd.notna(row.get("price")) else None,
                "bedrooms": int(row.get("bedrooms", 0)) if pd.notna(row.get("bedrooms")) else None,
                "bathrooms": int(row.get("bathrooms", 0)) if pd.notna(row.get("bathrooms")) else None,
                "neighborhood": str(row.get("neighborhood", "")),
                "developer": str(row.get("developer", "")),
                "completion_date": str(row.get("completion_date", "")),
                "rental_yield": float(row.get("rental_yield", 0)) if pd.notna(row.get("rental_yield")) else None,
                "property_status": str(row.get("property_status", "")),
                "market_segment": str(row.get("market_segment", ""))
            }
            data["records"].append(record)
        
        return data
    
    def _extract_regulatory_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract regulatory updates specific information"""
        data = {
            "data_type": "regulatory_updates",
            "records": []
        }
        
        for _, row in df.iterrows():
            record = {
                "law_name": str(row.get("law_name", "")),
                "enactment_date": str(row.get("enactment_date", "")),
                "description": str(row.get("description", "")),
                "status": str(row.get("status", "")),
                "impact_areas": str(row.get("impact_areas", "")),
                "key_provisions": str(row.get("key_provisions", "")),
                "compliance_requirements": str(row.get("compliance_requirements", ""))
            }
            data["records"].append(record)
        
        return data
    
    def _extract_developers_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract developers specific information"""
        data = {
            "data_type": "developers",
            "records": []
        }
        
        for _, row in df.iterrows():
            record = {
                "name": str(row.get("name", "")),
                "market_share": float(row.get("market_share", 0)) if pd.notna(row.get("market_share")) else None,
                "reputation_score": float(row.get("reputation_score", 0)) if pd.notna(row.get("reputation_score")) else None,
                "total_projects": int(row.get("total_projects", 0)) if pd.notna(row.get("total_projects")) else None,
                "financial_strength": str(row.get("financial_strength", "")),
                "specialties": str(row.get("specialties", "")),
                "key_projects": str(row.get("key_projects", ""))
            }
            data["records"].append(record)
        
        return data
    
    def _extract_investment_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract investment insights specific information"""
        data = {
            "data_type": "investment_insights",
            "records": []
        }
        
        for _, row in df.iterrows():
            record = {
                "title": str(row.get("title", "")),
                "category": str(row.get("category", "")),
                "roi_projection": float(row.get("roi_projection", 0)) if pd.notna(row.get("roi_projection")) else None,
                "investment_amount_min": float(row.get("investment_amount_min", 0)) if pd.notna(row.get("investment_amount_min")) else None,
                "investment_amount_max": float(row.get("investment_amount_max", 0)) if pd.notna(row.get("investment_amount_max")) else None,
                "risk_level": str(row.get("risk_level", "")),
                "target_audience": str(row.get("target_audience", "")),
                "requirements": str(row.get("requirements", "")),
                "key_benefits": str(row.get("key_benefits", ""))
            }
            data["records"].append(record)
        
        return data
    
    def _extract_generic_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract generic data for unknown schemas"""
        data = {
            "data_type": "generic",
            "records": []
        }
        
        for _, row in df.iterrows():
            record = {}
            for col in df.columns:
                value = row[col]
                if pd.isna(value):
                    record[col] = None
                elif isinstance(value, (int, float)):
                    record[col] = value
                else:
                    record[col] = str(value)
            data["records"].append(record)
        
        return data
    
    def _generate_metadata(self, df: pd.DataFrame, schema_type: str, file_path: str) -> Dict[str, Any]:
        """Generate metadata about the processed file"""
        metadata = {
            "file_path": file_path,
            "schema_type": schema_type,
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "column_names": list(df.columns),
            "data_types": df.dtypes.to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "processing_timestamp": datetime.now().isoformat()
        }
        
        # Add schema-specific metadata
        if schema_type in self.supported_schemas:
            schema_config = self.supported_schemas[schema_type]
            metadata["required_columns"] = schema_config["required_columns"]
            metadata["optional_columns"] = schema_config["optional_columns"]
            metadata["data_types_expected"] = schema_config["data_types"]
        
        return metadata
