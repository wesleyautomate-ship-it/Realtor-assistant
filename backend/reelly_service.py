#!/usr/bin/env python3
"""
Reelly API Service for Dubai Real Estate RAG System
Handles communication with the Reelly.io B2B property and agent discovery platform
"""

import requests
import os
import logging
from typing import List, Dict, Any, Optional
from functools import lru_cache
from datetime import datetime, timedelta
import json
import tenacity
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class ReellyService:
    """
    A service to interact with the Reelly.io API for B2B property and agent discovery.
    """
    
    def __init__(self):
        self.api_key = os.getenv("REELLY_API_KEY")
        # Try different possible Reelly API URLs
        self.base_url = "https://api.reelly.io/v1"  # Updated to more common pattern
        
        if not self.api_key:
            logger.warning("REELLY_API_KEY environment variable not set. Reelly integration will be disabled.")
            self.enabled = False
        else:
            self.enabled = True
            logger.info("✅ Reelly API service initialized successfully")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=tenacity.retry_if_exception_type(
            (requests.exceptions.RequestException, requests.exceptions.Timeout)
        )
    )
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Helper function to make authenticated requests to the Reelly API."""
        if not self.enabled:
            logger.warning("Reelly API is disabled - no API key configured")
            return {}
        
        headers = {
            "X-API-Key": self.api_key,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        try:
            url = f"{self.base_url}{endpoint}"
            logger.debug(f"Making request to Reelly API: {url}")
            
            # Reduced timeout for faster failure detection
            response = requests.get(url, headers=headers, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"Reelly API response: {len(data.get('data', []))} items")
            return data
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout calling Reelly API endpoint '{endpoint}'")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Reelly API endpoint '{endpoint}': {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing Reelly API response: {e}")
            return {}
        except Exception as e:
            logger.error(f"Unexpected error in Reelly API call: {e}")
            return {}

    def search_properties(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Searches for properties using the Reelly API.
        
        Args:
            params: Search parameters including property_type, budget_min, budget_max, bedrooms, etc.
            
        Returns:
            List of property dictionaries from Reelly
        """
        if not self.enabled:
            return []
        
        # Map our internal parameter names to Reelly's expected names
        reelly_params = {
            "property_type": params.get("property_type"),
            "price_from": params.get("budget_min"),
            "price_to": params.get("budget_max"),
            "bedrooms_from": params.get("bedrooms"),
            "bedrooms_to": params.get("bedrooms"),
            "area": params.get("area"),
            "developer": params.get("developer"),
            "page": params.get("page", 1),
            "per_page": params.get("per_page", 20)
        }
        
        # Remove None values
        reelly_params = {k: v for k, v in reelly_params.items() if v is not None}
        
        logger.info(f"Searching Reelly properties with params: {reelly_params}")
        response_data = self._make_request("/properties", params=reelly_params)
        
        properties = response_data.get("data", [])
        logger.info(f"Found {len(properties)} properties from Reelly API")
        
        return properties

    def get_property_details(self, property_id: str) -> Optional[Dict[str, Any]]:
        """
        Gets detailed information about a specific property.
        
        Args:
            property_id: The Reelly property ID
            
        Returns:
            Property details dictionary or None if not found
        """
        if not self.enabled:
            return None
        
        response_data = self._make_request(f"/properties/{property_id}")
        return response_data.get("data")

    @lru_cache(maxsize=1)
    def get_developers(self) -> List[Dict[str, Any]]:
        """
        Returns a list of all developers from Reelly, cached for performance.
        
        Returns:
            List of developer dictionaries
        """
        if not self.enabled:
            return []
        
        logger.info("Fetching developers from Reelly API")
        response_data = self._make_request("/reference/get_developers")
        developers = response_data.get("data", [])
        logger.info(f"Found {len(developers)} developers from Reelly API")
        return developers

    @lru_cache(maxsize=128)
    def get_areas(self, country_id: int = 1) -> List[Dict[str, Any]]:
        """
        Returns a list of areas for a given country, cached for performance.
        
        Args:
            country_id: Country ID (default 1 for UAE)
            
        Returns:
            List of area dictionaries
        """
        if not self.enabled:
            return []
        
        logger.info(f"Fetching areas for country {country_id} from Reelly API")
        response_data = self._make_request(f"/reference/get_areas", params={"country_id": country_id})
        areas = response_data.get("data", [])
        logger.info(f"Found {len(areas)} areas from Reelly API")
        return areas

    def get_agents(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Searches for agents in the Reelly network.
        
        Args:
            params: Search parameters for agents
            
        Returns:
            List of agent dictionaries
        """
        if not self.enabled:
            return []
        
        logger.info("Searching agents from Reelly API")
        response_data = self._make_request("/agents", params=params)
        agents = response_data.get("data", [])
        logger.info(f"Found {len(agents)} agents from Reelly API")
        return agents

    def get_agent_details(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Gets detailed information about a specific agent.
        
        Args:
            agent_id: The Reelly agent ID
            
        Returns:
            Agent details dictionary or None if not found
        """
        if not self.enabled:
            return None
        
        response_data = self._make_request(f"/agents/{agent_id}")
        return response_data.get("data")

    def get_market_insights(self, area: str = None) -> Dict[str, Any]:
        """
        Gets market insights and trends for a specific area.
        
        Args:
            area: Area name to get insights for
            
        Returns:
            Market insights dictionary
        """
        if not self.enabled:
            return {}
        
        params = {"area": area} if area else {}
        response_data = self._make_request("/market/insights", params=params)
        return response_data.get("data", {})

    def format_property_for_display(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formats Reelly property data for consistent display in our application.
        
        Args:
            property_data: Raw property data from Reelly API
            
        Returns:
            Formatted property data
        """
        if not property_data:
            return {}
        
        # Extract and format key information
        formatted = {
            "id": property_data.get("id"),
            "title": property_data.get("title", "N/A"),
            "address": property_data.get("address", "N/A"),
            "price": {
                "amount": property_data.get("price", {}).get("amount", 0),
                "currency": property_data.get("price", {}).get("currency", "AED"),
                "formatted": f"{property_data.get('price', {}).get('amount', 0):,} {property_data.get('price', {}).get('currency', 'AED')}"
            },
            "bedrooms": property_data.get("bedrooms", "N/A"),
            "bathrooms": property_data.get("bathrooms", "N/A"),
            "area_sqft": property_data.get("area_sqft", "N/A"),
            "property_type": property_data.get("property_type", "N/A"),
            "developer": property_data.get("developer", {}).get("name", "N/A"),
            "agent": {
                "name": property_data.get("agent", {}).get("name", "N/A"),
                "company": property_data.get("agent", {}).get("company_name", "N/A"),
                "phone": property_data.get("agent", {}).get("phone", "N/A"),
                "email": property_data.get("agent", {}).get("email", "N/A")
            },
            "description": property_data.get("description", "N/A"),
            "amenities": property_data.get("amenities", []),
            "images": property_data.get("images", []),
            "source": "reelly",
            "listed_date": property_data.get("listed_date"),
            "last_updated": property_data.get("updated_at")
        }
        
        return formatted

    def is_enabled(self) -> bool:
        """Returns whether the Reelly service is enabled and configured."""
        return self.enabled

    def get_service_status(self) -> Dict[str, Any]:
        """
        Returns the current status of the Reelly service.
        
        Returns:
            Status dictionary with enabled flag and configuration info
        """
        return {
            "enabled": self.enabled,
            "base_url": self.base_url,
            "api_key_configured": bool(self.api_key),
            "last_check": datetime.now().isoformat()
        }
