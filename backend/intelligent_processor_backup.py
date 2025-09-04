#!/usr/bin/env python3
"""
Intelligent Data Processor for Real Estate Files
Handles proper document classification, duplicate detection, and data rectification
"""

import os
import re
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple
import pandas as pd
import numpy as np
from pathlib import Path
from collections import defaultdict
import time

# AI Integration
try:
    import google.generativeai as genai
    from config.settings import GOOGLE_API_KEY
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    model = None

# Database Integration
try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    from config.settings import DATABASE_URL
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    engine = None
    SessionLocal = None

# ChromaDB Integration
try:
    import chromadb
    from config.settings import CHROMA_HOST, CHROMA_PORT
    CHROMA_AVAILABLE = True
    chroma_client = None  # Will be initialized lazily
except ImportError:
    CHROMA_AVAILABLE = False
    chroma_client = None

# Text processing
try:
    from fuzzywuzzy import fuzz, process
    FUZZY_AVAILABLE = True
except ImportError:
    FUZZY_AVAILABLE = False

# PDF Processing
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

logger = logging.getLogger(__name__)

# PDF Processing
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

logger = logging.getLogger(__name__)

class IntelligentDataProcessor:
    """Intelligent data processor with proper classification and duplicate detection"""
    
    def __init__(self):
        # Initialize ChromaDB client lazily
        self._chroma_client = None
        
        # Document classification patterns
        self.classification_patterns = {
            'legal_document': {
                'keywords': [
                    'contract', 'agreement', 'terms and conditions', 'clause', 'party', 'parties',
                    'legal', 'law', 'regulation', 'compliance', 'liability', 'indemnity',
                    'breach', 'termination', 'enforcement', 'jurisdiction', 'governing law',
                    'signature', 'witness', 'notary', 'legal counsel', 'attorney'
                ],
                'weight': 10
            },
            'property_listing': {
                'keywords': [
                    'for sale', 'for rent', 'available', 'listing', 'property details',
                    'bedroom', 'bathroom', 'sq ft', 'square feet', 'square meters',
                    'floor plan', 'amenities', 'features', 'description', 'photos',
                    'price', 'asking price', 'offers', 'viewing', 'contact agent'
                ],
                'weight': 8
            },
            'market_report': {
                'keywords': [
                    'market analysis', 'market report', 'market trends', 'market overview',
                    'quarterly report', 'annual report', 'market forecast', 'market outlook',
                    'demand', 'supply', 'inventory', 'absorption', 'market performance',
                    'growth', 'decline', 'stable', 'market indicators', 'market data'
                ],
                'weight': 9
            },
            'neighborhood_guide': {
                'keywords': [
                    'neighborhood', 'community', 'area guide', 'location overview',
                    'amenities', 'schools', 'hospitals', 'shopping', 'restaurants',
                    'transportation', 'metro', 'bus', 'parking', 'parks', 'recreation',
                    'lifestyle', 'residential area', 'commercial area', 'mixed use'
                ],
                'weight': 7
            },
            'transaction_record': {
                'keywords': [
                    'transaction', 'sale record', 'purchase record', 'transfer record',
                    'closing date', 'settlement date', 'completion date', 'deal value',
                    'buyer', 'seller', 'agent', 'broker', 'commission', 'fees',
                    'mortgage', 'financing', 'payment', 'escrow', 'title transfer'
                ],
                'weight': 8
            },
            'agent_profile': {
                'keywords': [
                    'agent profile', 'broker profile', 'real estate agent', 'license',
                    'experience', 'specialization', 'certifications', 'awards',
                    'performance', 'sales record', 'client testimonials', 'contact',
                    'office', 'team', 'agency', 'brokerage'
                ],
                'weight': 6
            },
            'developer_profile': {
                'keywords': [
                    'developer', 'development company', 'project portfolio', 'projects',
                    'construction', 'development', 'master plan', 'phase', 'completion',
                    'handover', 'warranty', 'maintenance', 'facilities', 'services'
                ],
                'weight': 7
            }
        }
        
        # Building name variations for duplicate detection
        self.building_variations = {
            'dubai marina': ['dubai marina', 'marina', 'marina district', 'marina area'],
            'downtown dubai': ['dubai downtown', 'downtown', 'downtown dubai', 'burj area'],
            'palm jumeirah': ['palm', 'palm jumeirah', 'palm island', 'the palm'],
            'business bay': ['business bay', 'bay area', 'business district'],
            'jbr': ['jbr', 'jumeirah beach residences', 'beach residences'],
            'dubai hills': ['dubai hills', 'hills estate', 'hills community'],
            'emirates hills': ['emirates hills', 'emirates hills estate'],
            'springs': ['springs', 'the springs', 'springs community'],
            'meadows': ['meadows', 'the meadows', 'meadows community'],
            'lakes': ['lakes', 'the lakes', 'lakes community']
        }
        
        # Data quality patterns
        self.data_quality_patterns = {
            'price_patterns': [
                r'AED\s*([\d,]+(?:\.\d{2})?)',
                r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*AED',
                r'USD\s*([\d,]+(?:\.\d{2})?)',
                r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*USD'
            ],
            'date_patterns': [
                r'\d{1,2}[-/]\d{1,2}[-/]\d{4}',
                r'\d{4}[-/]\d{1,2}[-/]\d{1,2}',
                r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}'
            ],
            'phone_patterns': [
                r'\+971\s*\d{2}\s*\d{3}\s*\d{4}',
                r'0\d{2}\s*\d{3}\s*\d{4}',
                r'\d{3}-\d{3}-\d{4}'
            ]
        }
    
    @property
    def chroma_client(self):
        """Lazy initialization of ChromaDB client"""
        if self._chroma_client is None and CHROMA_AVAILABLE:
            try:
                self._chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
                logger.info("ChromaDB client initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize ChromaDB client: {e}")
                self._chroma_client = None
        return self._chroma_client

    def _get_document_category(self, text_content: str) -> dict:
        """
        Uses AI to classify the document into a specific category.
        """
        if not AI_AVAILABLE or not model:
            logger.warning("AI model not available, falling back to rule-based classification")
            return self.classify_document(text_content, "text")
        
        # We only use the first 4000 characters for a quick and cheap classification
        prompt = f"""
You are a document classification specialist for a Dubai real estate company. Your task is to accurately classify the document based on its content.

**Classification Categories:**
- **transaction_sheet**: Contains tables or lists of property sales data (e.g., dates, addresses, prices).
- **legal_handbook**: Contains legal clauses, contract terms, or regulatory information (e.g., RERA rules).
- **market_report**: Contains analysis of market trends, statistics, charts, and forecasts for a specific area.
- **property_brochure**: A marketing document describing a single property for sale or rent, focusing on features and lifestyle.
- **unknown**: The document does not clearly fit any of the above categories.

Analyze the following content and respond ONLY with a single, clean JSON object in the format:
{{"category": "your_choice", "confidence": <a number between 0.0 and 1.0>}}

**Content Snippet:**
---
{text_content[:4000]}
        ---
        """
        try:
            response = model.generate_content(prompt)
            
            # Handle different response formats
            if hasattr(response, 'text'):
                response_text = response.text
            elif hasattr(response, 'parts'):
                response_text = response.parts[0].text if response.parts else ""
            else:
                response_text = str(response)
            
            # Clean the response text
            response_text = response_text.strip()
            
            # Try to extract JSON from the response
            if response_text.startswith('{') and response_text.endswith('}'):
                result = json.loads(response_text)
            else:
                # Try to find JSON in the response
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    # Fallback to rule-based classification
                    logger.warning(f"Could not parse AI response: {response_text}")
                    return self.classify_document(text_content, "text")
            
            return result
        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"Error in AI classification: {e}")
            # Fallback to rule-based classification
            return self.classify_document(text_content, "text")

    def process_uploaded_document(self, file_path: str, file_type: str):
        """
        Orchestrates the full processing of an uploaded document.
        """
        try:
            # 1. Extract content from the document
            content = self.extract_content(file_path, file_type)
            if not content:
                raise ValueError("Could not extract content from the document.")

            # 2. Triage: Get the document category
            classification = self._get_document_category(content)
            category = classification.get("category")
            confidence = classification.get("confidence", 0.0)
            
            logger.info(f"Document classified as: {category} with confidence {confidence}")

            # 3. Route to the correct specialized extractor
            if category == 'transaction_sheet':
                return self._extract_transaction_data(content)
            elif category == 'legal_handbook':
                return self._process_legal_document(content)
            elif category == 'market_report':
                return self._process_market_report(content)
            elif category == 'property_brochure':
                return self._process_property_brochure(content)
            else:
                # Handle other categories or unknown types
                return {
                    "status": "classified", 
                    "category": category, 
                    "confidence": confidence,
                    "message": "No specialized extractor for this category yet."
                }
                
        except Exception as e:
            logger.error(f"Error processing document {file_path}: {e}")
            return {"status": "error", "message": f"Processing failed: {str(e)}"}

    def process_uploaded_document_async(self, file_path: str, file_type: str, instructions: str = "", task_id: str = None):
        """
        Enhanced asynchronous document processing with two-step AI pipeline and detailed reporting.
        This method orchestrates the complete processing workflow and generates comprehensive reports.
        """
        from task_manager import task_manager, TaskStatus
        
        start_time = time.time()
        processing_report = {
            "execution_plan": None,
            "storage_summary": {},
            "performance_metrics": {},
            "processing_steps": [],
            "final_result": None
        }
        
        try:
            # Step 1: Extract content
            if task_id:
                task_manager.update_task_status(task_id, TaskStatus.PROCESSING, progress=0.1)
            
            content = self.extract_content(file_path, file_type)
            if not content:
                raise ValueError("Could not extract content from the document.")
            
            processing_report["processing_steps"].append({
                "step": "content_extraction",
                "status": "completed",
                "details": f"Extracted {len(content)} characters from {file_type} file"
            })
            
            # Step 2: Triage & Planning AI
            if task_id:
                task_manager.update_task_status(task_id, TaskStatus.PROCESSING, progress=0.3)
            
            execution_plan = self._generate_execution_plan(content, instructions)
            processing_report["execution_plan"] = execution_plan
            
            processing_report["processing_steps"].append({
                "step": "ai_triage_and_planning",
                "status": "completed",
                "details": f"Generated execution plan: {execution_plan.get('category', 'unknown')} with {execution_plan.get('confidence', 0):.2f} confidence"
            })
            
            # Step 3: Specialized Processing
            if task_id:
                task_manager.update_task_status(task_id, TaskStatus.PROCESSING, progress=0.6)
            
            category = execution_plan.get("category", "unknown")
            specialized_result = self._execute_specialized_processing(content, category, execution_plan)
            
            processing_report["processing_steps"].append({
                "step": "specialized_processing",
                "status": "completed",
                "details": f"Processed as {category} with status: {specialized_result.get('status', 'unknown')}"
            })
            
            # Step 4: Data Storage
            if task_id:
                task_manager.update_task_status(task_id, TaskStatus.PROCESSING, progress=0.8)
            
            storage_summary = self._store_processed_data(specialized_result, category, content)
            processing_report["storage_summary"] = storage_summary
            
            processing_report["processing_steps"].append({
                "step": "data_storage",
                "status": "completed",
                "details": f"Stored data in {len(storage_summary)} locations"
            })
            
            # Step 5: Finalize
            if task_id:
                task_manager.update_task_status(task_id, TaskStatus.PROCESSING, progress=1.0)
            
            total_time = time.time() - start_time
            processing_report["performance_metrics"] = {
                "total_processing_time_seconds": total_time,
                "content_size_characters": len(content),
                "file_type": file_type,
                "ai_model_used": "gemini-1.5-flash"
            }
            
            processing_report["final_result"] = {
                "status": "completed",
                "category": category,
                "confidence": execution_plan.get("confidence", 0.0),
                "extracted_data": specialized_result,
                "storage_locations": storage_summary
            }
            
            if task_id:
                task_manager.set_task_result(task_id, processing_report)
            
            return processing_report
            
        except Exception as e:
            error_msg = f"Processing failed: {str(e)}"
            logger.error(f"Error in async document processing: {e}")
            
            processing_report["processing_steps"].append({
                "step": "error_handling",
                "status": "failed",
                "details": error_msg
            })
            
            if task_id:
                task_manager.set_task_error(task_id, error_msg)
            
            return processing_report

    def _generate_execution_plan(self, content: str, instructions: str = "") -> Dict[str, Any]:
        """
        Step 1: Triage & Planning AI
        Analyzes the document content and user instructions to create a detailed execution plan.
        """
        if not AI_AVAILABLE or not model:
            return {"category": "unknown", "confidence": 0.0, "plan": "AI not available"}
        
        prompt = f"""
You are an expert document analysis and processing planner for a Dubai real estate company. Your task is to analyze the provided document content and create a detailed execution plan for processing it.

**Document Content Preview:**
{content[:2000]}...

**User Instructions (if any):**
{instructions if instructions else "No specific instructions provided"}

**Your Analysis Tasks:**
1. **Document Classification**: Determine the primary category of this document
2. **Processing Strategy**: Plan the optimal approach for extracting and storing the data
3. **Data Storage Planning**: Determine where different types of data should be stored
4. **Quality Assessment**: Evaluate the content quality and potential processing challenges

**Available Categories:**
- transaction_sheet: Property sales data, transaction records, price lists
- legal_handbook: Contracts, legal documents, regulations, compliance materials
- market_report: Market analysis, trends, statistics, forecasts
- property_brochure: Property listings, marketing materials, property descriptions
- unknown: Documents that don't clearly fit other categories

**Output Format:**
Respond with a JSON object containing:
{{
    "category": "the_primary_category",
    "confidence": 0.95,
    "processing_strategy": "detailed_plan_for_processing",
    "data_storage_plan": {{
        "postgresql_tables": ["list", "of", "relevant", "tables"],
        "chromadb_collections": ["list", "of", "collections"],
        "vector_embeddings": "description_of_what_to_embed"
    }},
    "quality_assessment": {{
        "content_quality": "high/medium/low",
        "extraction_complexity": "simple/moderate/complex",
        "potential_issues": ["list", "of", "potential", "problems"]
    }},
    "recommended_actions": ["list", "of", "specific", "processing", "steps"]
}}

**Document Content:**
---
{content}
---
"""
        
        try:
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                execution_plan = json.loads(json_match.group())
                return execution_plan
            else:
                logger.error(f"Could not parse execution plan response: {response_text}")
                return {"category": "unknown", "confidence": 0.0, "plan": "Failed to parse AI response"}
                
        except Exception as e:
            logger.error(f"Error generating execution plan: {e}")
            return {"category": "unknown", "confidence": 0.0, "plan": f"Error: {str(e)}"}

    def _execute_specialized_processing(self, content: str, category: str, execution_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 2: Specialized Processor AI
        Executes the specialized processing based on the execution plan.
        """
        try:
            if category == 'transaction_sheet':
                return self._extract_transaction_data(content)
            elif category == 'legal_handbook':
                return self._process_legal_document(content)
            elif category == 'market_report':
                return self._process_market_report(content)
            elif category == 'property_brochure':
                return self._process_property_brochure(content)
            else:
                return {
                    "status": "classified",
                    "category": category,
                    "confidence": execution_plan.get("confidence", 0.0),
                    "message": "No specialized processor available for this category",
                    "raw_content": content[:1000] + "..." if len(content) > 1000 else content
                }
        except Exception as e:
            logger.error(f"Error in specialized processing: {e}")
            return {"status": "error", "message": f"Specialized processing failed: {str(e)}"}

    def _store_processed_data(self, result: Dict[str, Any], category: str, original_content: str) -> Dict[str, Any]:
        """
        Stores the processed data in appropriate databases and returns a storage summary.
        """
        storage_summary = {
            "postgresql_inserts": [],
            "chromadb_additions": [],
            "vector_embeddings": [],
            "total_records_stored": 0
        }
        
        try:
            # Store in PostgreSQL based on category
            if category == 'transaction_sheet' and result.get('status') == 'processed':
                transactions = result.get('data', {}).get('transactions', [])
                if transactions and DB_AVAILABLE:
                    # Store transactions in PostgreSQL
                    storage_summary["postgresql_inserts"].append({
                        "table": "transactions",
                        "records": len(transactions),
                        "status": "success"
                    })
                    storage_summary["total_records_stored"] += len(transactions)
            
            # Store in ChromaDB for vector search
            if CHROMA_AVAILABLE:
                try:
                    # Create or get collection
                    collection_name = f"vector_db_{category.replace('_', '')}"
                    try:
                        collection = chroma_client.get_collection(collection_name)
                    except:
                        collection = chroma_client.create_collection(collection_name)
                    
                    # Add document to vector database
                    doc_id = f"doc_{int(time.time())}"
                    collection.add(
                        documents=[original_content[:1000]],  # Truncate for vector storage
                        metadatas=[{
                            "category": category,
                            "processing_timestamp": datetime.now().isoformat(),
                            "source": "intelligent_processor"
                        }],
                        ids=[doc_id]
                    )
                    
                    storage_summary["chromadb_additions"].append({
                        "collection": collection_name,
                        "document_id": doc_id,
                        "status": "success"
                    })
                    
                except Exception as e:
                    logger.error(f"Error storing in ChromaDB: {e}")
                    storage_summary["chromadb_additions"].append({
                        "collection": collection_name,
                        "status": "failed",
                        "error": str(e)
                    })
            
            return storage_summary
            
        except Exception as e:
            logger.error(f"Error in data storage: {e}")
            storage_summary["error"] = str(e)
            return storage_summary

    def _extract_transaction_data(self, content: str) -> dict:
        """
        Uses AI to extract structured transaction data from text.
        """
        if not AI_AVAILABLE or not model:
            return {"status": "error", "message": "AI model not available for transaction extraction"}
        
        prompt = f"""
You are an automated data extraction engine. Your task is to extract all property sales transactions from the provided text.

**Instructions:**
1.  Scan the entire text for individual property sale records.
2.  For each record, extract the following fields: `sale_date`, `address`, `unit_number`, and `sale_price`.
3.  Standardize all dates to a strict "YYYY-MM-DD" format. If a year is missing, assume the current year.
4.  Ensure `sale_price` is an integer, removing all currency symbols, commas, and decimals.
5.  If a field is not present for a record, use `null`.

**Output Format:**
Respond ONLY with a single JSON object. The JSON object must contain a single key "transactions" which is a list of transaction objects. Adhere strictly to this schema.

**Example:**
{{"transactions": [
    {{"sale_date": "2024-08-15", "address": "Marina Gate 1, Dubai Marina", "unit_number": "3405", "sale_price": 2500000}},
    {{"sale_date": "2024-07-22", "address": "Burj Khalifa, Downtown Dubai", "unit_number": "101-A", "sale_price": 5100000}}
]}}

**Text to Process:**
        ---
        {content}
        ---
        """
        try:
            response = model.generate_content(prompt)
            
            # Handle different response formats
            if hasattr(response, 'text'):
                response_text = response.text
            elif hasattr(response, 'parts'):
                response_text = response.parts[0].text if response.parts else ""
            else:
                response_text = str(response)
            
            # Clean the response text
            response_text = response_text.strip()
            
            # Try to extract JSON from the response
            if response_text.startswith('{') and response_text.endswith('}'):
                extracted_data = json.loads(response_text)
            else:
                # Try to find JSON in the response
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    extracted_data = json.loads(json_match.group())
                else:
                    logger.error(f"Could not parse AI response for transaction extraction: {response_text}")
                    return {"status": "error", "message": "Could not parse AI response"}
            
            transactions = extracted_data.get("transactions", [])

            # Save transactions to database
            if DB_AVAILABLE and transactions:
                saved_count = self._save_transactions_to_db(transactions)
                return {
                    "status": "processed", 
                    "category": "transaction_sheet", 
                    "records_extracted": len(transactions),
                    "records_saved": saved_count
                }
            else:
                return {
                    "status": "processed", 
                    "category": "transaction_sheet", 
                    "records_extracted": len(transactions),
                    "records_saved": 0
                }
                
        except Exception as e:
            logger.error(f"Failed to extract transaction data: {e}")
            return {"status": "error", "message": f"Failed to extract transaction data: {e}"}

    def _process_legal_document(self, content: str) -> dict:
        """
        Uses AI to chunk and tag legal documents for the vector database.
        """
        if not AI_AVAILABLE or not model:
            return {"status": "error", "message": "AI model not available for legal document processing"}
        
        prompt = f"""
        You are a legal analyst AI. Analyze the legal document content below.
        Break it down into logical paragraphs or sections.
        For each section, provide a concise summary and a list of relevant metadata tags from this list: ['deal_structuring', 'commission_rules', 'RERA_compliance', 'financing', 'tenancy_contracts'].
        Respond ONLY with a JSON object containing a single key "legal_chunks" which is a list of objects.

        Example: {{"legal_chunks": [{{"content": "The full text of the paragraph...", "summary": "A brief summary.", "tags": ["RERA_compliance"]}}]}}

        Content to process:
        ---
        {content}
        ---
        """
        try:
            response = model.generate_content(prompt)
            
            # Handle different response formats
            if hasattr(response, 'text'):
                response_text = response.text
            elif hasattr(response, 'parts'):
                response_text = response.parts[0].text if response.parts else ""
            else:
                response_text = str(response)
            
            # Clean the response text
            response_text = response_text.strip()
            
            # Try to extract JSON from the response
            if response_text.startswith('{') and response_text.endswith('}'):
                extracted_data = json.loads(response_text)
            else:
                # Try to find JSON in the response
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    extracted_data = json.loads(json_match.group())
                else:
                    logger.error(f"Could not parse AI response for legal document processing: {response_text}")
                    return {"status": "error", "message": "Could not parse AI response"}
            
            chunks = extracted_data.get("legal_chunks", [])

            # Save chunks to ChromaDB
            if CHROMA_AVAILABLE and chunks:
                saved_count = self._save_legal_chunks_to_chroma(chunks)
                return {
                    "status": "processed", 
                    "category": "legal_handbook", 
                    "chunks_created": len(chunks),
                    "chunks_saved": saved_count
                }
            else:
                return {
                    "status": "processed", 
                    "category": "legal_handbook", 
                    "chunks_created": len(chunks),
                    "chunks_saved": 0
                }
                
        except Exception as e:
            logger.error(f"Failed to process legal document: {e}")
            return {"status": "error", "message": f"Failed to process legal document: {e}"}

    def _process_market_report(self, content: str) -> dict:
        """
        Process market reports and extract key insights using AI.
        """
        if not AI_AVAILABLE or not model:
            return {"status": "error", "message": "AI model not available for market report processing"}

        prompt = f"""
You are a senior real estate market analyst. Your task is to read the following market report and distill it into key, structured insights for our vector database.

**Instructions:**
1.  Determine the primary `neighborhood` and `property_type` the report is about.
2.  Find the key performance indicators: `avg_price_change_pct`, `sales_volume_change_pct`, and `avg_rental_yield`.
3.  Write a concise `executive_summary` (3-4 sentences) that captures the main findings and outlook of the report.
4.  List up to 5 key takeaways as bullet points in a single string under `key_takeaways`.

**Output Format:**
Respond ONLY with a single JSON object.

**Example:**
{{
    "neighborhood": "Downtown Dubai",
    "property_type": "Apartments",
    "avg_price_change_pct": 5.2,
    "sales_volume_change_pct": -3.1,
    "avg_rental_yield": 6.8,
    "executive_summary": "The Downtown Dubai apartment market showed resilience in Q2 2025, with prices appreciating by 5.2% despite a slight dip in sales volume. High rental yields continue to attract investors, though the luxury segment is showing signs of stabilization.",
    "key_takeaways": "- Luxury segment prices are stabilizing.\\n- Strong demand persists in the 1-2 bedroom category.\\n- Off-plan sales have decreased compared to the previous quarter.\\n- Rental demand remains robust due to tourism and corporate relocations.\\n- The upcoming handover of 'Emaar Tower C' is expected to add new inventory."
}}

**Market Report Content:**
---
{content}
---
"""
        try:
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                extracted_data = json.loads(json_match.group())
                # Here you would add logic to save this data to ChromaDB
                return {
                    "status": "processed",
                    "category": "market_report",
                    "data": extracted_data
                }
            else:
                logger.error(f"Could not parse AI response for market report: {response_text}")
                return {"status": "error", "message": "Could not parse AI response for market report"}
        except Exception as e:
            logger.error(f"Failed to process market report: {e}")
            return {"status": "error", "message": f"Failed to process market report: {e}"}

    def _process_property_brochure(self, content: str) -> dict:
        """
        Process property brochures and extract property details using AI.
        """
        if not AI_AVAILABLE or not model:
            return {"status": "error", "message": "AI model not available for brochure processing"}

        prompt = f"""
You are a property data extraction specialist. Analyze the content of this property brochure and extract the key details.

**Instructions:**
1.  Extract the following fields: `property_type` (e.g., "Apartment", "Villa"), `address`, `neighborhood`, `bedrooms`, `bathrooms`, `size_sqft`, and `asking_price`.
2.  Also, write a `marketing_summary` of 2-3 sentences capturing the essence of the property's lifestyle and key features.
3.  Ensure `bedrooms`, `bathrooms`, `size_sqft`, and `asking_price` are integers.
4.  If a specific field cannot be found, use `null`.

**Output Format:**
Respond ONLY with a single JSON object containing the extracted data.

**Example:**
{{
    "property_type": "Apartment",
    "address": "Emaar Beachfront, Dubai Harbour",
    "neighborhood": "Dubai Harbour",
    "bedrooms": 3,
    "bathrooms": 4,
    "size_sqft": 1750,
    "asking_price": 4200000,
    "marketing_summary": "Experience luxury waterfront living with breathtaking views of the Palm Jumeirah. This spacious apartment features high-end finishes and direct beach access, perfect for a modern family."
}}

**Brochure Content:**
---
{content}
---
"""
        try:
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                extracted_data = json.loads(json_match.group())
                # Here you would add logic to save this data to your database
                return {
                    "status": "processed",
                    "category": "property_brochure", 
                    "data": extracted_data
                }
            else:
                logger.error(f"Could not parse AI response for brochure: {response_text}")
                return {"status": "error", "message": "Could not parse AI response for brochure"}
        except Exception as e:
            logger.error(f"Failed to process property brochure: {e}")
            return {"status": "error", "message": f"Failed to process property brochure: {e}"}

    def _save_transactions_to_db(self, transactions: List[Dict]) -> int:
        """
        Save extracted transactions to the database.
        """
        if not DB_AVAILABLE:
            return 0
        
        try:
            with SessionLocal() as session:
                saved_count = 0
                for transaction in transactions:
                    try:
                        # Insert transaction into database
                        query = text("""
                            INSERT INTO transactions (transaction_date, sale_price, source_document_id, created_at)
                            VALUES (:transaction_date, :sale_price, :source_document_id, :created_at)
                        """)
                        
                        session.execute(query, {
                            'transaction_date': transaction.get('sale_date'),
                            'sale_price': transaction.get('sale_price', 0),
                            'source_document_id': f"ai_extracted_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                            'created_at': datetime.now()
                        })
                        saved_count += 1
                        
                    except Exception as e:
                        logger.error(f"Error saving transaction {transaction}: {e}")
                        continue
                
                session.commit()
                logger.info(f"Successfully saved {saved_count} transactions to database")
                return saved_count
                
        except Exception as e:
            logger.error(f"Database error saving transactions: {e}")
            return 0

    def _save_legal_chunks_to_chroma(self, chunks: List[Dict]) -> int:
        """
        Save legal document chunks to ChromaDB regulatory_framework collection.
        """
        if not CHROMA_AVAILABLE:
            return 0
        
        try:
            # Ensure collection exists
            try:
                collection = chroma_client.get_collection("regulatory_framework")
            except Exception:
                # Create collection if it doesn't exist
                collection = chroma_client.create_collection(
                    name="regulatory_framework",
                    metadata={"description": "Legal and regulatory framework documents"}
                )
                logger.info("Created regulatory_framework collection in ChromaDB")
            
            documents = []
            metadatas = []
            ids = []
            
            for i, chunk in enumerate(chunks):
                documents.append(chunk['content'])
                metadatas.append({
                    'summary': chunk.get('summary', ''),
                    'tags': ','.join(chunk.get('tags', [])),
                    'source': 'ai_processed',
                    'processed_date': datetime.now().isoformat()
                })
                ids.append(f"legal_chunk_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}")
            
            if documents:
                collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                logger.info(f"Successfully saved {len(documents)} legal chunks to ChromaDB")
                return len(documents)
            
            return 0
            
        except Exception as e:
            logger.error(f"ChromaDB error saving legal chunks: {e}")
            return 0

    def classify_document(self, content: str, file_type: str) -> Dict[str, Any]:
        """Intelligently classify document based on content"""
        content_lower = content.lower()
        
        # Calculate scores for each category
        scores = {}
        for category, pattern in self.classification_patterns.items():
            score = 0
            for keyword in pattern['keywords']:
                if keyword in content_lower:
                    score += pattern['weight']
            
            # Additional scoring based on file type
            if file_type == 'csv' and category == 'transaction_record':
                score += 5
            elif file_type == 'excel' and category in ['market_report', 'transaction_record']:
                score += 5
            elif file_type == 'pdf' and category in ['legal_document', 'market_report', 'neighborhood_guide']:
                score += 3
            
            scores[category] = score
        
        # Get the category with highest score
        if scores:
            best_category = max(scores, key=scores.get)
            confidence = min(100, scores[best_category] / 10)  # Normalize to 0-100
        else:
            best_category = 'general_document'
            confidence = 50
        
        return {
            'category': best_category,
            'confidence': confidence,
            'scores': scores,
            'file_type': file_type
        }
    
    def extract_content(self, file_path: str, file_type: str) -> str:
        """Extract content from different file types"""
        try:
            if file_type == 'pdf':
                return self._extract_pdf_content(file_path)
            elif file_type in ['csv', 'excel']:
                return self._extract_structured_content(file_path, file_type)
            elif file_type == 'text':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                return ""
        except Exception as e:
            logger.error(f"Error extracting content from {file_path}: {e}")
            return ""
    
    def _extract_pdf_content(self, file_path: str) -> str:
        """Extract text from PDF using multiple methods"""
        content = ""
        
        # Method 1: PyPDF2
        if PDF_AVAILABLE:
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        content += page.extract_text() + "\n"
                if content.strip():
                    return content
            except Exception as e:
                logger.warning(f"PyPDF2 extraction failed: {e}")
        
        # Method 2: pdfplumber
        if PDFPLUMBER_AVAILABLE:
            try:
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            content += text + "\n"
                if content.strip():
                    return content
            except Exception as e:
                logger.warning(f"pdfplumber extraction failed: {e}")
        
        return content
    
    def _extract_structured_content(self, file_path: str, file_type: str) -> str:
        """Extract content from structured files with memory optimization for large files"""
        try:
            if file_type == 'csv':
                # For CSV, read in chunks to handle large files
                chunk_size = 1000
                chunks = []
                total_rows = 0
                
                for chunk in pd.read_csv(file_path, chunksize=chunk_size):
                    chunks.append(chunk)
                    total_rows += len(chunk)
                    if total_rows >= 5000:  # Limit to first 5000 rows for processing
                        break
                
                if chunks:
                    df = pd.concat(chunks, ignore_index=True)
                else:
                    return ""
                    
            elif file_type == 'excel':
                # For Excel, read only first few sheets and limit rows
                try:
                    # Try to read with row limit first
                    df = pd.read_excel(file_path, nrows=5000)
                except Exception as e:
                    logger.warning(f"Failed to read Excel with row limit: {e}")
                    # Fallback: read just the first sheet with no limit
                    df = pd.read_excel(file_path, sheet_name=0)
                    # Limit to first 5000 rows
                    df = df.head(5000)
            else:
                return ""
            
            # Convert dataframe to text representation
            content = f"Columns: {', '.join(df.columns)}\n"
            content += f"Total records in file: {len(df)} (showing first 5000 for processing)\n"
            content += f"Sample data (first 10 rows):\n{df.head(10).to_string()}\n"
            
            # Add summary statistics for numerical columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                content += f"\nSummary statistics for numerical columns:\n{df[numeric_cols].describe().to_string()}\n"
            
            return content
        except Exception as e:
            logger.error(f"Error extracting structured content: {e}")
            return ""
    
    def detect_duplicate_transactions(self, transactions: List[Dict]) -> List[Dict]:
        """Detect duplicate transactions using fuzzy matching"""
        if not FUZZY_AVAILABLE:
            return []
        
        duplicates = []
        processed = set()
        
        for i, transaction1 in enumerate(transactions):
            if i in processed:
                continue
            
            duplicate_group = []
            
            for j, transaction2 in enumerate(transactions[i+1:], i+1):
                if j in processed:
                    continue
                
                # Check for exact duplicates
                if self._is_exact_duplicate(transaction1, transaction2):
                    duplicate_group.append({
                        'index': j,
                        'transaction': transaction2,
                        'similarity': 100,
                        'type': 'exact'
                    })
                    processed.add(j)
                
                # Check for fuzzy duplicates
                elif self._is_fuzzy_duplicate(transaction1, transaction2):
                    similarity = self._calculate_similarity(transaction1, transaction2)
                    if similarity > 85:  # 85% similarity threshold
                        duplicate_group.append({
                            'index': j,
                            'transaction': transaction2,
                            'similarity': similarity,
                            'type': 'fuzzy'
                        })
                        processed.add(j)
            
            if duplicate_group:
                duplicates.append({
                    'group_id': f"group_{i}",
                    'original_index': i,
                    'original_transaction': transaction1,
                    'duplicates': duplicate_group,
                    'total_duplicates': len(duplicate_group)
                })
                processed.add(i)
        
        return duplicates
    
    def _is_exact_duplicate(self, trans1: Dict, trans2: Dict) -> bool:
        """Check if two transactions are exact duplicates"""
        key_fields = ['transaction_date', 'transaction_value', 'building_name', 'apartment_number']
        
        for field in key_fields:
            if field in trans1 and field in trans2:
                if str(trans1[field]).strip() != str(trans2[field]).strip():
                    return False
            elif field in trans1 or field in trans2:
                return False
        
        return True
    
    def _is_fuzzy_duplicate(self, trans1: Dict, trans2: Dict) -> bool:
        """Check if two transactions are fuzzy duplicates"""
        # Check building name similarity
        building1 = str(trans1.get('building_name', '')).lower()
        building2 = str(trans2.get('building_name', '')).lower()
        
        if building1 and building2:
            building_similarity = fuzz.ratio(building1, building2)
            if building_similarity > 80:
                return True
        
        # Check other key fields
        key_fields = ['transaction_date', 'transaction_value', 'apartment_number']
        matching_fields = 0
        
        for field in key_fields:
            if field in trans1 and field in trans2:
                val1 = str(trans1[field]).strip()
                val2 = str(trans2[field]).strip()
                if val1 and val2:
                    similarity = fuzz.ratio(val1, val2)
                    if similarity > 90:
                        matching_fields += 1
        
        return matching_fields >= 2  # At least 2 fields must match
    
    def _calculate_similarity(self, trans1: Dict, trans2: Dict) -> float:
        """Calculate overall similarity between two transactions"""
        similarities = []
        
        for field in ['building_name', 'apartment_number', 'transaction_value']:
            if field in trans1 and field in trans2:
                val1 = str(trans1[field]).strip()
                val2 = str(trans2[field]).strip()
                if val1 and val2:
                    similarity = fuzz.ratio(val1, val2)
                    similarities.append(similarity)
        
        return sum(similarities) / len(similarities) if similarities else 0
    
    def standardize_building_name(self, building_name: str) -> str:
        """Standardize building names to handle variations"""
        building_lower = building_name.lower().strip()
        
        # Check against known variations
        for standard_name, variations in self.building_variations.items():
            if building_lower in variations:
                return standard_name.title()
        
        # Try fuzzy matching
        if FUZZY_AVAILABLE:
            all_variations = []
            for variations in self.building_variations.values():
                all_variations.extend(variations)
            
            best_match = process.extractOne(building_lower, all_variations)
            if best_match and best_match[1] > 80:
                # Find the standard name for this variation
                for standard_name, variations in self.building_variations.items():
                    if best_match[0] in variations:
                        return standard_name.title()
        
        # Return cleaned original name
        return building_name.strip().title()
    
    def clean_transaction_data(self, transactions: List[Dict]) -> List[Dict]:
        """Clean and standardize transaction data"""
        cleaned = []
        
        for transaction in transactions:
            cleaned_transaction = {}
            
            for key, value in transaction.items():
                if key == 'building_name':
                    cleaned_transaction[key] = self.standardize_building_name(str(value))
                elif key == 'transaction_value':
                    cleaned_transaction[key] = self._clean_numeric_value(value)
                elif key == 'transaction_date':
                    cleaned_transaction[key] = self._clean_date_value(value)
                else:
                    cleaned_transaction[key] = self._clean_general_value(value)
            
            cleaned.append(cleaned_transaction)
        
        return cleaned
    
    def _clean_numeric_value(self, value) -> float:
        """Clean numeric values"""
        if pd.isna(value):
            return 0.0
        
        value_str = str(value).strip()
        # Remove currency symbols and commas
        value_str = re.sub(r'[AED$,€£]', '', value_str)
        value_str = value_str.replace(',', '')
        
        try:
            return float(value_str)
        except:
            return 0.0
    
    def _clean_date_value(self, value) -> str:
        """Clean date values"""
        if pd.isna(value):
            return ""
        
        try:
            # Try to parse as datetime
            if isinstance(value, str):
                # Handle various date formats
                date_formats = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y']
                for fmt in date_formats:
                    try:
                        parsed_date = pd.to_datetime(value, format=fmt)
                        return parsed_date.strftime('%Y-%m-%d')
                    except:
                        continue
            
            # Fallback to pandas parsing
            parsed_date = pd.to_datetime(value)
            return parsed_date.strftime('%Y-%m-%d')
        except:
            return str(value)
    
    def _clean_general_value(self, value) -> str:
        """Clean general text values"""
        if pd.isna(value):
            return ""
        
        return str(value).strip()
    
    def generate_insights(self, transactions: List[Dict]) -> Dict[str, Any]:
        """Generate insights from transaction data"""
        if not transactions:
            return {}
        
        insights = {
            'total_transactions': len(transactions),
            'total_value': 0,
            'average_value': 0,
            'top_buildings': [],
            'top_buyer_countries': [],
            'date_range': {}
        }
        
        # Calculate total and average values
        values = [t.get('transaction_value', 0) for t in transactions if t.get('transaction_value', 0) > 0]
        if values:
            insights['total_value'] = sum(values)
            insights['average_value'] = sum(values) / len(values)
        
        # Top buildings
        building_counts = defaultdict(int)
        for t in transactions:
            building = t.get('building_name', '')
            if building:
                building_counts[building] += 1
        
        insights['top_buildings'] = sorted(building_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Top buyer countries
        country_counts = defaultdict(int)
        for t in transactions:
            country = t.get('buyer_country', '')
            if country:
                country_counts[country] += 1
        
        insights['top_buyer_countries'] = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return insights
    
    def generate_recommendations(self, duplicates: List[Dict], transactions: List[Dict]) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if duplicates:
            recommendations.append(f"Found {len(duplicates)} groups of duplicate transactions")
            recommendations.append("Review and merge duplicate records to maintain data integrity")
        
        if transactions:
            total_value = sum([t.get('transaction_value', 0) for t in transactions])
            if total_value > 0:
                recommendations.append(f"Total transaction value: AED {total_value:,.0f}")
                recommendations.append("Consider market trends and investment opportunities")
        
        return recommendations
