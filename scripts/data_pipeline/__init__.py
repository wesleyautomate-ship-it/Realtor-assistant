"""
Real Estate Data Processing Pipeline

A comprehensive data processing system for Dubai real estate data.
Handles ingestion, cleaning, enrichment, and storage of property data.
"""

__version__ = "1.0.0"
__author__ = "Real Estate AI Team"

from .main import DataPipeline
from .ingestion import DataIngestion
from .cleaning import DataCleaner
from .enrichment import DataEnricher
from .storage import DataStorage

__all__ = [
    "DataPipeline",
    "DataIngestion", 
    "DataCleaner",
    "DataEnricher",
    "DataStorage"
]
