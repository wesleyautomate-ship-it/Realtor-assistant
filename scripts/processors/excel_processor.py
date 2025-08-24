#!/usr/bin/env python3
"""
Excel Processor for Dubai Real Estate Research
Handles Excel files with multiple sheets containing financial data, market analysis
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import json
import re
from pathlib import Path

# Try to import Excel processing libraries
try:
    import pandas as pd
    import openpyxl
    EXCEL_LIBRARY = "pandas_openpyxl"
except ImportError:
    try:
        import xlrd
        EXCEL_LIBRARY = "xlrd"
    except ImportError:
        EXCEL_LIBRARY = None

logger = logging.getLogger(__name__)

class ExcelProcessor:
    """Processor for Excel files containing Dubai real estate financial data"""
    
    def __init__(self):
        self.sheet_types = {
            "market_data": {
                "keywords": ["price", "market", "trend", "analysis", "forecast"],
                "required_columns": ["date", "neighborhood", "property_type"],
                "collections": ["market_analysis", "financial_insights"]
            },
            "financial_analysis": {
                "keywords": ["roi", "investment", "return", "profit", "revenue"],
                "required_columns": ["investment_amount", "roi", "period"],
                "collections": ["financial_insights", "investment_insights"]
            },
            "property_listings": {
                "keywords": ["property", "listing", "address", "price", "bedrooms"],
                "required_columns": ["address", "price", "property_type"],
                "collections": ["market_analysis", "properties"]
            },
            "developer_portfolio": {
                "keywords": ["developer", "project", "portfolio", "company"],
                "required_columns": ["developer_name", "project_name"],
                "collections": ["developer_profiles", "market_analysis"]
            },
            "transaction_history": {
                "keywords": ["transaction", "sale", "purchase", "date", "amount"],
                "required_columns": ["transaction_date", "amount", "property_type"],
                "collections": ["market_analysis", "transaction_guidance"]
            }
        }
        
        if not EXCEL_LIBRARY:
            logger.warning("No Excel processing library available. Install pandas and openpyxl.")
    
    def process(self, file_path: str) -> Dict[str, Any]:
        """Process an Excel file and extract structured data from all sheets"""
        logger.info(f"Processing Excel file: {file_path}")
        
        try:
            # Read all sheets from Excel file
            sheets_data = self._read_all_sheets(file_path)
            if not sheets_data:
                raise ValueError("Could not read any sheets from Excel file")
            
            # Process each sheet
            processed_sheets = []
            total_rows = 0
            
            for sheet_name, sheet_data in sheets_data.items():
                logger.info(f"Processing sheet: {sheet_name}")
                
                # Classify sheet type
                sheet_type = self._classify_sheet(sheet_data, sheet_name)
                
                # Extract structured data
                structured_data = self._extract_structured_data(sheet_data, sheet_type, sheet_name)
                
                processed_sheets.append({
                    "sheet_name": sheet_name,
                    "sheet_type": sheet_type,
                    "row_count": len(sheet_data),
                    "column_count": len(sheet_data.columns) if hasattr(sheet_data, 'columns') else 0,
                    "structured_data": structured_data
                })
                
                total_rows += len(sheet_data)
            
            # Generate metadata
            metadata = self._generate_metadata(file_path, processed_sheets)
            
            return {
                "content_type": "excel",
                "file_path": file_path,
                "processed_at": datetime.now().isoformat(),
                "total_sheets": len(processed_sheets),
                "total_rows": total_rows,
                "processed_sheets": processed_sheets,
                "metadata": metadata,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error processing Excel file {file_path}: {e}")
            return {
                "content_type": "excel",
                "file_path": file_path,
                "status": "failed",
                "error": str(e)
            }
    
    def _read_all_sheets(self, file_path: str) -> Dict[str, pd.DataFrame]:
        """Read all sheets from Excel file"""
        if not EXCEL_LIBRARY:
            raise ImportError("No Excel processing library available")
        
        sheets_data = {}
        
        try:
            if EXCEL_LIBRARY == "pandas_openpyxl":
                # Read all sheets
                excel_file = pd.ExcelFile(file_path)
                
                for sheet_name in excel_file.sheet_names:
                    try:
                        df = pd.read_excel(file_path, sheet_name=sheet_name)
                        if not df.empty:
                            sheets_data[sheet_name] = df
                            logger.info(f"Read sheet '{sheet_name}' with {len(df)} rows")
                    except Exception as e:
                        logger.warning(f"Could not read sheet '{sheet_name}': {e}")
            
            elif EXCEL_LIBRARY == "xlrd":
                # Fallback to xlrd for older Excel files
                workbook = xlrd.open_workbook(file_path)
                
                for sheet_name in workbook.sheet_names():
                    try:
                        sheet = workbook.sheet_by_name(sheet_name)
                        data = []
                        headers = []
                        
                        for row_idx in range(sheet.nrows):
                            row_data = sheet.row_values(row_idx)
                            if row_idx == 0:
                                headers = row_data
                            else:
                                data.append(row_data)
                        
                        if data:
                            df = pd.DataFrame(data, columns=headers)
                            sheets_data[sheet_name] = df
                            logger.info(f"Read sheet '{sheet_name}' with {len(df)} rows")
                    except Exception as e:
                        logger.warning(f"Could not read sheet '{sheet_name}': {e}")
            
            return sheets_data
            
        except Exception as e:
            logger.error(f"Error reading Excel file: {e}")
            raise
    
    def _classify_sheet(self, sheet_data: pd.DataFrame, sheet_name: str) -> str:
        """Classify sheet type based on content and column names"""
        # Convert column names to string for analysis
        columns_str = " ".join([str(col) for col in sheet_data.columns]).lower()
        sheet_name_lower = sheet_name.lower()
        
        # Count keyword matches for each sheet type
        type_scores = {}
        
        for sheet_type, config in self.sheet_types.items():
            score = 0
            
            # Check keywords in sheet name and column names
            for keyword in config["keywords"]:
                score += sheet_name_lower.count(keyword)
                score += columns_str.count(keyword)
            
            # Bonus for required columns match
            required_cols = config.get("required_columns", [])
            for col in required_cols:
                if col.lower() in columns_str:
                    score += 2  # Higher weight for required columns
            
            type_scores[sheet_type] = score
        
        # Return the sheet type with highest score
        if type_scores:
            return max(type_scores, key=type_scores.get)
        else:
            return "general_data"
    
    def _extract_structured_data(self, sheet_data: pd.DataFrame, sheet_type: str, sheet_name: str) -> Dict[str, Any]:
        """Extract structured data based on sheet type"""
        structured_data = {
            "sheet_type": sheet_type,
            "key_metrics": {},
            "data_summary": {},
            "entities": []
        }
        
        # Extract key metrics based on sheet type
        if sheet_type == "market_data":
            structured_data["key_metrics"] = self._extract_market_metrics(sheet_data)
        elif sheet_type == "financial_analysis":
            structured_data["key_metrics"] = self._extract_financial_metrics(sheet_data)
        elif sheet_type == "property_listings":
            structured_data["key_metrics"] = self._extract_property_metrics(sheet_data)
        elif sheet_type == "developer_portfolio":
            structured_data["key_metrics"] = self._extract_developer_metrics(sheet_data)
        elif sheet_type == "transaction_history":
            structured_data["key_metrics"] = self._extract_transaction_metrics(sheet_data)
        
        # Extract entities
        structured_data["entities"] = self._extract_entities(sheet_data)
        
        # Generate data summary
        structured_data["data_summary"] = self._generate_data_summary(sheet_data)
        
        return structured_data
    
    def _extract_market_metrics(self, sheet_data: pd.DataFrame) -> Dict[str, Any]:
        """Extract market-related metrics"""
        metrics = {}
        
        # Find price-related columns
        price_columns = [col for col in sheet_data.columns if 'price' in str(col).lower()]
        if price_columns:
            for col in price_columns:
                try:
                    numeric_data = pd.to_numeric(sheet_data[col], errors='coerce').dropna()
                    if not numeric_data.empty:
                        metrics[f"{col}_avg"] = numeric_data.mean()
                        metrics[f"{col}_min"] = numeric_data.min()
                        metrics[f"{col}_max"] = numeric_data.max()
                except:
                    pass
        
        # Find date columns
        date_columns = [col for col in sheet_data.columns if 'date' in str(col).lower()]
        if date_columns:
            metrics["date_range"] = f"{len(date_columns)} date columns found"
        
        # Count neighborhoods if present
        neighborhood_columns = [col for col in sheet_data.columns if 'neighborhood' in str(col).lower()]
        if neighborhood_columns:
            for col in neighborhood_columns:
                unique_neighborhoods = sheet_data[col].nunique()
                metrics[f"{col}_unique_count"] = unique_neighborhoods
        
        return metrics
    
    def _extract_financial_metrics(self, sheet_data: pd.DataFrame) -> Dict[str, Any]:
        """Extract financial-related metrics"""
        metrics = {}
        
        # Find ROI columns
        roi_columns = [col for col in sheet_data.columns if 'roi' in str(col).lower()]
        if roi_columns:
            for col in roi_columns:
                try:
                    numeric_data = pd.to_numeric(sheet_data[col], errors='coerce').dropna()
                    if not numeric_data.empty:
                        metrics[f"{col}_avg"] = numeric_data.mean()
                        metrics[f"{col}_max"] = numeric_data.max()
                except:
                    pass
        
        # Find investment amount columns
        investment_columns = [col for col in sheet_data.columns if 'investment' in str(col).lower() or 'amount' in str(col).lower()]
        if investment_columns:
            for col in investment_columns:
                try:
                    numeric_data = pd.to_numeric(sheet_data[col], errors='coerce').dropna()
                    if not numeric_data.empty:
                        metrics[f"{col}_total"] = numeric_data.sum()
                        metrics[f"{col}_avg"] = numeric_data.mean()
                except:
                    pass
        
        return metrics
    
    def _extract_property_metrics(self, sheet_data: pd.DataFrame) -> Dict[str, Any]:
        """Extract property-related metrics"""
        metrics = {}
        
        # Count property types
        property_type_columns = [col for col in sheet_data.columns if 'type' in str(col).lower()]
        if property_type_columns:
            for col in property_type_columns:
                property_counts = sheet_data[col].value_counts()
                metrics[f"{col}_distribution"] = property_counts.to_dict()
        
        # Bedroom/bathroom counts
        bedroom_columns = [col for col in sheet_data.columns if 'bedroom' in str(col).lower()]
        if bedroom_columns:
            for col in bedroom_columns:
                try:
                    numeric_data = pd.to_numeric(sheet_data[col], errors='coerce').dropna()
                    if not numeric_data.empty:
                        metrics[f"{col}_avg"] = numeric_data.mean()
                        metrics[f"{col}_max"] = numeric_data.max()
                except:
                    pass
        
        return metrics
    
    def _extract_developer_metrics(self, sheet_data: pd.DataFrame) -> Dict[str, Any]:
        """Extract developer-related metrics"""
        metrics = {}
        
        # Count developers
        developer_columns = [col for col in sheet_data.columns if 'developer' in str(col).lower()]
        if developer_columns:
            for col in developer_columns:
                developer_counts = sheet_data[col].value_counts()
                metrics[f"{col}_count"] = len(developer_counts)
                metrics[f"{col}_top_5"] = developer_counts.head(5).to_dict()
        
        # Count projects
        project_columns = [col for col in sheet_data.columns if 'project' in str(col).lower()]
        if project_columns:
            for col in project_columns:
                project_counts = sheet_data[col].value_counts()
                metrics[f"{col}_total"] = len(project_counts)
        
        return metrics
    
    def _extract_transaction_metrics(self, sheet_data: pd.DataFrame) -> Dict[str, Any]:
        """Extract transaction-related metrics"""
        metrics = {}
        
        # Transaction amounts
        amount_columns = [col for col in sheet_data.columns if 'amount' in str(col).lower()]
        if amount_columns:
            for col in amount_columns:
                try:
                    numeric_data = pd.to_numeric(sheet_data[col], errors='coerce').dropna()
                    if not numeric_data.empty:
                        metrics[f"{col}_total"] = numeric_data.sum()
                        metrics[f"{col}_avg"] = numeric_data.mean()
                        metrics[f"{col}_count"] = len(numeric_data)
                except:
                    pass
        
        # Transaction dates
        date_columns = [col for col in sheet_data.columns if 'date' in str(col).lower()]
        if date_columns:
            metrics["date_columns"] = len(date_columns)
        
        return metrics
    
    def _extract_entities(self, sheet_data: pd.DataFrame) -> List[str]:
        """Extract key entities from sheet data"""
        entities = []
        
        # Dubai neighborhoods
        neighborhoods = [
            "Dubai Marina", "Downtown Dubai", "Palm Jumeirah", "JBR", "Jumeirah Beach",
            "Arabian Ranches", "Emirates Hills", "Dubai Hills Estate", "Meydan",
            "Business Bay", "Dubai Creek Harbour", "Dubai South", "Dubai Silicon Oasis"
        ]
        
        # Major developers
        developers = [
            "Emaar Properties", "DAMAC Properties", "Nakheel", "Meraas", "Dubai Properties",
            "Sobha Realty", "Azizi Developments", "Omniyat", "Select Group"
        ]
        
        # Check for entities in column names and data
        all_text = " ".join([str(col) for col in sheet_data.columns]).lower()
        
        for entity in neighborhoods + developers:
            if entity.lower() in all_text:
                entities.append(entity)
        
        return list(set(entities))
    
    def _generate_data_summary(self, sheet_data: pd.DataFrame) -> Dict[str, Any]:
        """Generate summary statistics for the sheet data"""
        summary = {
            "total_rows": len(sheet_data),
            "total_columns": len(sheet_data.columns),
            "column_names": list(sheet_data.columns),
            "data_types": {}
        }
        
        # Analyze data types
        for col in sheet_data.columns:
            try:
                summary["data_types"][str(col)] = str(sheet_data[col].dtype)
            except:
                summary["data_types"][str(col)] = "unknown"
        
        return summary
    
    def _generate_metadata(self, file_path: str, processed_sheets: List[Dict]) -> Dict[str, Any]:
        """Generate metadata for the Excel file"""
        file_info = Path(file_path)
        
        return {
            "filename": file_info.name,
            "file_size": file_info.stat().st_size,
            "processing_library": EXCEL_LIBRARY,
            "total_sheets": len(processed_sheets),
            "sheet_types": [sheet["sheet_type"] for sheet in processed_sheets],
            "extraction_timestamp": datetime.now().isoformat()
        }
