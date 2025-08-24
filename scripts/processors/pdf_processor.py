#!/usr/bin/env python3
"""
PDF Processor for Dubai Real Estate Research
Handles PDF files containing market reports, regulations, transaction guides
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import json
import re
from pathlib import Path

# Try to import PDF processing libraries
try:
    import PyPDF2
    PDF_LIBRARY = "PyPDF2"
except ImportError:
    try:
        import pdfplumber
        PDF_LIBRARY = "pdfplumber"
    except ImportError:
        PDF_LIBRARY = None

logger = logging.getLogger(__name__)

class PDFProcessor:
    """Processor for PDF files containing Dubai real estate documents"""
    
    def __init__(self):
        self.document_types = {
            "market_report": {
                "keywords": ["market", "analysis", "trend", "forecast", "price", "demand", "supply"],
                "collections": ["market_analysis", "market_forecasts"]
            },
            "regulatory_document": {
                "keywords": ["law", "regulation", "compliance", "rera", "dld", "government", "policy"],
                "collections": ["regulatory_framework", "transaction_guidance"]
            },
            "transaction_guide": {
                "keywords": ["transaction", "process", "procedure", "step", "guide", "how to", "buy", "sell"],
                "collections": ["transaction_guidance", "agent_resources"]
            },
            "developer_profile": {
                "keywords": ["developer", "company", "project", "portfolio", "emaar", "damac", "nakheel"],
                "collections": ["developer_profiles", "market_analysis"]
            },
            "neighborhood_guide": {
                "keywords": ["neighborhood", "area", "community", "location", "amenities", "schools", "hospitals"],
                "collections": ["neighborhood_profiles", "market_analysis"]
            }
        }
        
        if not PDF_LIBRARY:
            logger.warning("No PDF processing library available. Install PyPDF2 or pdfplumber.")
    
    def process(self, file_path: str) -> Dict[str, Any]:
        """Process a PDF file and extract structured data"""
        logger.info(f"Processing PDF file: {file_path}")
        
        try:
            # Extract text from PDF
            text_content = self._extract_text(file_path)
            if not text_content:
                raise ValueError("Could not extract text from PDF")
            
            # Classify document type
            document_type = self._classify_document(text_content)
            logger.info(f"Classified document as: {document_type}")
            
            # Extract structured data
            structured_data = self._extract_structured_data(text_content, document_type)
            
            # Generate metadata
            metadata = self._generate_metadata(text_content, document_type, file_path)
            
            return {
                "content_type": "pdf",
                "file_path": file_path,
                "document_type": document_type,
                "processed_at": datetime.now().isoformat(),
                "text_length": len(text_content),
                "structured_data": structured_data,
                "metadata": metadata,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error processing PDF file {file_path}: {e}")
            return {
                "content_type": "pdf",
                "file_path": file_path,
                "status": "failed",
                "error": str(e)
            }
    
    def _extract_text(self, file_path: str) -> str:
        """Extract text from PDF file"""
        if not PDF_LIBRARY:
            raise ImportError("No PDF processing library available")
        
        text_content = ""
        
        try:
            if PDF_LIBRARY == "PyPDF2":
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text_content += page.extract_text() + "\n"
            
            elif PDF_LIBRARY == "pdfplumber":
                import pdfplumber
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        text_content += page.extract_text() + "\n"
            
            return text_content.strip()
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise
    
    def _classify_document(self, text_content: str) -> str:
        """Classify document type based on content"""
        text_lower = text_content.lower()
        
        # Count keyword matches for each document type
        type_scores = {}
        
        for doc_type, config in self.document_types.items():
            score = 0
            for keyword in config["keywords"]:
                score += text_lower.count(keyword)
            type_scores[doc_type] = score
        
        # Return the document type with highest score
        if type_scores:
            return max(type_scores, key=type_scores.get)
        else:
            return "general_document"
    
    def _extract_structured_data(self, text_content: str, document_type: str) -> Dict[str, Any]:
        """Extract structured data based on document type"""
        structured_data = {
            "document_type": document_type,
            "key_entities": [],
            "key_metrics": {},
            "summary": ""
        }
        
        # Extract key entities (neighborhoods, developers, etc.)
        structured_data["key_entities"] = self._extract_entities(text_content)
        
        # Extract key metrics based on document type
        if document_type == "market_report":
            structured_data["key_metrics"] = self._extract_market_metrics(text_content)
        elif document_type == "regulatory_document":
            structured_data["key_metrics"] = self._extract_regulatory_metrics(text_content)
        elif document_type == "developer_profile":
            structured_data["key_metrics"] = self._extract_developer_metrics(text_content)
        
        # Generate summary
        structured_data["summary"] = self._generate_summary(text_content, document_type)
        
        return structured_data
    
    def _extract_entities(self, text_content: str) -> List[str]:
        """Extract key entities from text"""
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
        
        # Check for entities in text
        for entity in neighborhoods + developers:
            if entity.lower() in text_content.lower():
                entities.append(entity)
        
        return list(set(entities))  # Remove duplicates
    
    def _extract_market_metrics(self, text_content: str) -> Dict[str, Any]:
        """Extract market-related metrics"""
        metrics = {}
        
        # Extract price ranges
        price_pattern = r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:AED|dirhams?|dhs?)'
        prices = re.findall(price_pattern, text_content, re.IGNORECASE)
        if prices:
            metrics["price_mentions"] = len(prices)
            metrics["price_range"] = f"{min(prices)} - {max(prices)} AED"
        
        # Extract percentages
        percent_pattern = r'(\d+(?:\.\d+)?)\s*%'
        percentages = re.findall(percent_pattern, text_content)
        if percentages:
            metrics["percentage_mentions"] = len(percentages)
        
        # Extract dates
        date_pattern = r'\b(?:202[3-4]|202[0-9])\b'
        dates = re.findall(date_pattern, text_content)
        if dates:
            metrics["date_mentions"] = len(dates)
        
        return metrics
    
    def _extract_regulatory_metrics(self, text_content: str) -> Dict[str, Any]:
        """Extract regulatory-related metrics"""
        metrics = {}
        
        # Count regulatory terms
        regulatory_terms = ["law", "regulation", "compliance", "rera", "dld", "government"]
        for term in regulatory_terms:
            count = text_content.lower().count(term)
            if count > 0:
                metrics[f"{term}_mentions"] = count
        
        # Extract law numbers
        law_pattern = r'Law\s+No\.?\s*(\d+)'
        laws = re.findall(law_pattern, text_content, re.IGNORECASE)
        if laws:
            metrics["law_numbers"] = laws
        
        return metrics
    
    def _extract_developer_metrics(self, text_content: str) -> Dict[str, Any]:
        """Extract developer-related metrics"""
        metrics = {}
        
        # Count project mentions
        project_pattern = r'(\d+)\s+(?:projects?|developments?)'
        projects = re.findall(project_pattern, text_content, re.IGNORECASE)
        if projects:
            metrics["project_count"] = max([int(p) for p in projects])
        
        # Extract market share
        share_pattern = r'(\d+(?:\.\d+)?)\s*%\s*(?:market\s+)?share'
        shares = re.findall(share_pattern, text_content, re.IGNORECASE)
        if shares:
            metrics["market_share"] = max([float(s) for s in shares])
        
        return metrics
    
    def _generate_summary(self, text_content: str, document_type: str) -> str:
        """Generate a summary of the document"""
        # Take first 200 characters as summary
        summary = text_content[:200].strip()
        if len(text_content) > 200:
            summary += "..."
        
        return summary
    
    def _generate_metadata(self, text_content: str, document_type: str, file_path: str) -> Dict[str, Any]:
        """Generate metadata for the document"""
        file_info = Path(file_path)
        
        return {
            "filename": file_info.name,
            "file_size": file_info.stat().st_size,
            "document_type": document_type,
            "processing_library": PDF_LIBRARY,
            "text_length": len(text_content),
            "word_count": len(text_content.split()),
            "extraction_timestamp": datetime.now().isoformat()
        }
