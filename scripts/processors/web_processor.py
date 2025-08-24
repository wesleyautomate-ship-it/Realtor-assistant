#!/usr/bin/env python3
"""
Web Processor for Dubai Real Estate Research
Handles web scraping and processing of real estate websites, market forecasts
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import json
import re
from pathlib import Path
from urllib.parse import urlparse, urljoin
import time

# Try to import web scraping libraries
try:
    import requests
    from bs4 import BeautifulSoup
    WEB_LIBRARY = "requests_beautifulsoup"
except ImportError:
    try:
        import urllib.request
        import html.parser
        WEB_LIBRARY = "urllib"
    except ImportError:
        WEB_LIBRARY = None

logger = logging.getLogger(__name__)

class WebProcessor:
    """Processor for web content containing Dubai real estate information"""
    
    def __init__(self):
        self.content_types = {
            "market_forecast": {
                "keywords": ["forecast", "prediction", "outlook", "trend", "future", "2024", "2025"],
                "collections": ["market_forecasts", "market_analysis"]
            },
            "agent_resources": {
                "keywords": ["agent", "broker", "listing", "property", "sale", "rent"],
                "collections": ["agent_resources", "transaction_guidance"]
            },
            "market_news": {
                "keywords": ["news", "update", "announcement", "development", "project"],
                "collections": ["market_analysis", "market_forecasts"]
            },
            "neighborhood_guide": {
                "keywords": ["neighborhood", "area", "community", "location", "amenities"],
                "collections": ["neighborhood_profiles", "market_analysis"]
            },
            "developer_news": {
                "keywords": ["developer", "company", "project", "launch", "emaar", "damac"],
                "collections": ["developer_profiles", "market_analysis"]
            }
        }
        
        # Common Dubai real estate websites
        self.trusted_domains = [
            "propertyfinder.ae",
            "bayut.com",
            "dubizzle.com",
            "emirates.estate",
            "dubaiproperties.ae",
            "emaar.com",
            "damacproperties.com",
            "nakheel.com",
            "dubailand.gov.ae",
            "dubai.gov.ae"
        ]
        
        if not WEB_LIBRARY:
            logger.warning("No web scraping library available. Install requests and beautifulsoup4.")
    
    def process(self, url_or_file: str) -> Dict[str, Any]:
        """Process web content from URL or HTML file"""
        logger.info(f"Processing web content: {url_or_file}")
        
        try:
            # Determine if it's a URL or file
            if url_or_file.startswith(('http://', 'https://')):
                content = self._fetch_web_content(url_or_file)
                source_type = "url"
            else:
                content = self._read_html_file(url_or_file)
                source_type = "file"
            
            if not content:
                raise ValueError("Could not extract content from source")
            
            # Classify content type
            content_type = self._classify_content(content)
            logger.info(f"Classified content as: {content_type}")
            
            # Extract structured data
            structured_data = self._extract_structured_data(content, content_type, url_or_file)
            
            # Generate metadata
            metadata = self._generate_metadata(url_or_file, content_type, source_type, content)
            
            return {
                "content_type": "web",
                "source": url_or_file,
                "source_type": source_type,
                "content_type_classified": content_type,
                "processed_at": datetime.now().isoformat(),
                "content_length": len(content),
                "structured_data": structured_data,
                "metadata": metadata,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error processing web content {url_or_file}: {e}")
            return {
                "content_type": "web",
                "source": url_or_file,
                "status": "failed",
                "error": str(e)
            }
    
    def _fetch_web_content(self, url: str) -> str:
        """Fetch content from web URL"""
        if not WEB_LIBRARY:
            raise ImportError("No web scraping library available")
        
        try:
            # Add headers to mimic browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            if WEB_LIBRARY == "requests_beautifulsoup":
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Extract text content
                text_content = soup.get_text()
                
                # Clean up whitespace
                lines = (line.strip() for line in text_content.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text_content = ' '.join(chunk for chunk in chunks if chunk)
                
                return text_content
            
            elif WEB_LIBRARY == "urllib":
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=10) as response:
                    html_content = response.read().decode('utf-8')
                
                # Simple HTML tag removal
                text_content = re.sub(r'<[^>]+>', '', html_content)
                text_content = re.sub(r'\s+', ' ', text_content).strip()
                
                return text_content
            
        except Exception as e:
            logger.error(f"Error fetching web content from {url}: {e}")
            raise
    
    def _read_html_file(self, file_path: str) -> str:
        """Read content from HTML file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
            
            # Simple HTML tag removal
            text_content = re.sub(r'<[^>]+>', '', html_content)
            text_content = re.sub(r'\s+', ' ', text_content).strip()
            
            return text_content
            
        except Exception as e:
            logger.error(f"Error reading HTML file {file_path}: {e}")
            raise
    
    def _classify_content(self, content: str) -> str:
        """Classify content type based on text content"""
        content_lower = content.lower()
        
        # Count keyword matches for each content type
        type_scores = {}
        
        for content_type, config in self.content_types.items():
            score = 0
            for keyword in config["keywords"]:
                score += content_lower.count(keyword)
            type_scores[content_type] = score
        
        # Return the content type with highest score
        if type_scores:
            return max(type_scores, key=type_scores.get)
        else:
            return "general_content"
    
    def _extract_structured_data(self, content: str, content_type: str, source: str) -> Dict[str, Any]:
        """Extract structured data based on content type"""
        structured_data = {
            "content_type": content_type,
            "key_entities": [],
            "key_metrics": {},
            "summary": "",
            "links": []
        }
        
        # Extract key entities
        structured_data["key_entities"] = self._extract_entities(content)
        
        # Extract key metrics based on content type
        if content_type == "market_forecast":
            structured_data["key_metrics"] = self._extract_forecast_metrics(content)
        elif content_type == "agent_resources":
            structured_data["key_metrics"] = self._extract_agent_metrics(content)
        elif content_type == "market_news":
            structured_data["key_metrics"] = self._extract_news_metrics(content)
        elif content_type == "neighborhood_guide":
            structured_data["key_metrics"] = self._extract_neighborhood_metrics(content)
        elif content_type == "developer_news":
            structured_data["key_metrics"] = self._extract_developer_metrics(content)
        
        # Extract links if it's a URL
        if source.startswith(('http://', 'https://')):
            structured_data["links"] = self._extract_links(content)
        
        # Generate summary
        structured_data["summary"] = self._generate_summary(content, content_type)
        
        return structured_data
    
    def _extract_entities(self, content: str) -> List[str]:
        """Extract key entities from content"""
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
        
        # Check for entities in content
        content_lower = content.lower()
        for entity in neighborhoods + developers:
            if entity.lower() in content_lower:
                entities.append(entity)
        
        return list(set(entities))
    
    def _extract_forecast_metrics(self, content: str) -> Dict[str, Any]:
        """Extract forecast-related metrics"""
        metrics = {}
        
        # Extract price predictions
        price_pattern = r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:AED|dirhams?|dhs?)'
        prices = re.findall(price_pattern, content, re.IGNORECASE)
        if prices:
            metrics["price_mentions"] = len(prices)
            metrics["price_range"] = f"{min(prices)} - {max(prices)} AED"
        
        # Extract percentage predictions
        percent_pattern = r'(\d+(?:\.\d+)?)\s*%\s*(?:increase|growth|rise|fall|decline)'
        percentages = re.findall(percent_pattern, content, re.IGNORECASE)
        if percentages:
            metrics["growth_predictions"] = len(percentages)
            metrics["avg_growth"] = sum([float(p) for p in percentages]) / len(percentages)
        
        # Extract years
        year_pattern = r'\b(202[4-9]|203[0-5])\b'
        years = re.findall(year_pattern, content)
        if years:
            metrics["forecast_years"] = list(set(years))
        
        return metrics
    
    def _extract_agent_metrics(self, content: str) -> Dict[str, Any]:
        """Extract agent-related metrics"""
        metrics = {}
        
        # Count agent-related terms
        agent_terms = ["agent", "broker", "listing", "property", "sale", "rent"]
        for term in agent_terms:
            count = content.lower().count(term)
            if count > 0:
                metrics[f"{term}_mentions"] = count
        
        # Extract contact information patterns
        phone_pattern = r'\+971\s*\d{1,3}\s*\d{3,4}\s*\d{3,4}'
        phones = re.findall(phone_pattern, content)
        if phones:
            metrics["phone_numbers"] = len(phones)
        
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, content)
        if emails:
            metrics["email_addresses"] = len(emails)
        
        return metrics
    
    def _extract_news_metrics(self, content: str) -> Dict[str, Any]:
        """Extract news-related metrics"""
        metrics = {}
        
        # Count news-related terms
        news_terms = ["announcement", "launch", "development", "project", "news", "update"]
        for term in news_terms:
            count = content.lower().count(term)
            if count > 0:
                metrics[f"{term}_mentions"] = count
        
        # Extract dates
        date_pattern = r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b'
        dates = re.findall(date_pattern, content, re.IGNORECASE)
        if dates:
            metrics["date_mentions"] = len(dates)
        
        return metrics
    
    def _extract_neighborhood_metrics(self, content: str) -> Dict[str, Any]:
        """Extract neighborhood-related metrics"""
        metrics = {}
        
        # Count neighborhood-related terms
        neighborhood_terms = ["neighborhood", "area", "community", "location", "amenities", "schools", "hospitals"]
        for term in neighborhood_terms:
            count = content.lower().count(term)
            if count > 0:
                metrics[f"{term}_mentions"] = count
        
        # Extract distance information
        distance_pattern = r'(\d+(?:\.\d+)?)\s*(?:km|kilometers?|miles?)'
        distances = re.findall(distance_pattern, content, re.IGNORECASE)
        if distances:
            metrics["distance_mentions"] = len(distances)
        
        return metrics
    
    def _extract_developer_metrics(self, content: str) -> Dict[str, Any]:
        """Extract developer-related metrics"""
        metrics = {}
        
        # Count developer-related terms
        developer_terms = ["developer", "company", "project", "launch", "portfolio"]
        for term in developer_terms:
            count = content.lower().count(term)
            if count > 0:
                metrics[f"{term}_mentions"] = count
        
        # Extract project values
        value_pattern = r'(\d+(?:\.\d+)?)\s*(?:million|billion)\s*(?:AED|dirhams?|dhs?)'
        values = re.findall(value_pattern, content, re.IGNORECASE)
        if values:
            metrics["project_values"] = len(values)
        
        return metrics
    
    def _extract_links(self, content: str) -> List[str]:
        """Extract relevant links from content"""
        links = []
        
        # Simple URL extraction
        url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
        urls = re.findall(url_pattern, content)
        
        for url in urls:
            # Filter for relevant domains
            domain = urlparse(url).netloc
            if any(trusted_domain in domain for trusted_domain in self.trusted_domains):
                links.append(url)
        
        return list(set(links))  # Remove duplicates
    
    def _generate_summary(self, content: str, content_type: str) -> str:
        """Generate a summary of the content"""
        # Take first 300 characters as summary
        summary = content[:300].strip()
        if len(content) > 300:
            summary += "..."
        
        return summary
    
    def _generate_metadata(self, source: str, content_type: str, source_type: str, content: str) -> Dict[str, Any]:
        """Generate metadata for the web content"""
        metadata = {
            "source": source,
            "source_type": source_type,
            "content_type": content_type,
            "processing_library": WEB_LIBRARY,
            "content_length": len(content),
            "word_count": len(content.split()),
            "extraction_timestamp": datetime.now().isoformat()
        }
        
        # Add domain information if it's a URL
        if source_type == "url":
            try:
                domain = urlparse(source).netloc
                metadata["domain"] = domain
                metadata["is_trusted_domain"] = any(trusted_domain in domain for trusted_domain in self.trusted_domains)
            except:
                pass
        
        return metadata
