#!/usr/bin/env python3
"""
Dubai Real Estate Property Scraper
Collects property data from various Dubai real estate websites
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import json
import re
from typing import List, Dict, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DubaiPropertyScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Dubai areas and their URL mappings
        self.dubai_areas = {
            'dubai-marina': 'Dubai Marina',
            'downtown-dubai': 'Downtown Dubai',
            'palm-jumeirah': 'Palm Jumeirah',
            'jumeirah-beach-residence': 'JBR',
            'business-bay': 'Business Bay',
            'dubai-hills-estate': 'Dubai Hills Estate',
            'arabian-ranches': 'Arabian Ranches',
            'emirates-hills': 'Emirates Hills',
            'springs': 'The Springs',
            'meadows': 'The Meadows',
            'lakes': 'The Lakes',
            'silicon-oasis': 'Dubai Silicon Oasis',
            'sports-city': 'Dubai Sports City',
            'motor-city': 'Dubai Motor City',
            'production-city': 'Dubai Production City',
            'knowledge-village': 'Dubai Knowledge Village',
            'media-city': 'Dubai Media City',
            'internet-city': 'Dubai Internet City'
        }
        
        # Property types
        self.property_types = ['apartment', 'villa', 'townhouse', 'penthouse', 'studio']
    
    def scrape_dubizzle(self, area: str, property_type: str, max_pages: int = 5) -> List[Dict]:
        """
        Scrape property listings from Dubizzle
        """
        properties = []
        base_url = "https://dubai.dubizzle.com/property-for-sale"
        
        logger.info(f"Starting Dubizzle scrape for {area} - {property_type}")
        
        for page in range(1, max_pages + 1):
            try:
                # Construct URL
                if page == 1:
                    url = f"{base_url}/{area}/{property_type}/"
                else:
                    url = f"{base_url}/{area}/{property_type}/?page={page}"
                
                logger.info(f"Scraping page {page}: {url}")
                
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find property listings
                listings = soup.find_all('div', class_='listing-item')
                
                if not listings:
                    logger.warning(f"No listings found on page {page}")
                    break
                
                for listing in listings:
                    try:
                        property_data = self._extract_dubizzle_property_data(listing)
                        if property_data:
                            properties.append(property_data)
                    except Exception as e:
                        logger.error(f"Error extracting property data: {e}")
                        continue
                
                # Add delay to be respectful
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error scraping page {page}: {e}")
                continue
        
        logger.info(f"Completed Dubizzle scrape. Found {len(properties)} properties")
        return properties
    
    def _extract_dubizzle_property_data(self, listing_element) -> Optional[Dict]:
        """
        Extract property data from a Dubizzle listing element
        """
        try:
            # Extract title
            title_elem = listing_element.find('h2', class_='listing-title')
            title = title_elem.text.strip() if title_elem else "N/A"
            
            # Extract price
            price_elem = listing_element.find('span', class_='price')
            price = self._extract_price(price_elem.text if price_elem else "N/A")
            
            # Extract location
            location_elem = listing_element.find('span', class_='location')
            location = location_elem.text.strip() if location_elem else "N/A"
            
            # Extract bedrooms
            bedrooms = self._extract_bedrooms(listing_element)
            
            # Extract bathrooms
            bathrooms = self._extract_bathrooms(listing_element)
            
            # Extract area
            area_sqft = self._extract_area(listing_element)
            
            # Extract property type
            property_type = self._extract_property_type(listing_element)
            
            # Extract developer
            developer = self._extract_developer(listing_element)
            
            # Extract amenities
            amenities = self._extract_amenities(listing_element)
            
            # Extract description
            description_elem = listing_element.find('div', class_='description')
            description = description_elem.text.strip() if description_elem else ""
            
            # Extract listing URL
            link_elem = listing_element.find('a', href=True)
            listing_url = f"https://dubai.dubizzle.com{link_elem['href']}" if link_elem else ""
            
            return {
                'title': title,
                'price': price,
                'price_currency': 'AED',
                'location': location,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'area_sqft': area_sqft,
                'property_type': property_type,
                'developer': developer,
                'amenities': amenities,
                'description': description,
                'listing_url': listing_url,
                'source': 'Dubizzle',
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error extracting property data: {e}")
            return None
    
    def _extract_price(self, price_text: str) -> float:
        """Extract numeric price from price text"""
        try:
            # Remove currency symbols and commas
            price_clean = re.sub(r'[^\d.]', '', price_text)
            return float(price_clean) if price_clean else 0.0
        except:
            return 0.0
    
    def _extract_bedrooms(self, listing_element) -> int:
        """Extract number of bedrooms"""
        try:
            # Look for bedroom indicators
            text = listing_element.get_text().lower()
            bedroom_match = re.search(r'(\d+)\s*(?:bed|bedroom)', text)
            return int(bedroom_match.group(1)) if bedroom_match else 0
        except:
            return 0
    
    def _extract_bathrooms(self, listing_element) -> int:
        """Extract number of bathrooms"""
        try:
            text = listing_element.get_text().lower()
            bathroom_match = re.search(r'(\d+)\s*(?:bath|bathroom)', text)
            return int(bathroom_match.group(1)) if bathroom_match else 0
        except:
            return 0
    
    def _extract_area(self, listing_element) -> float:
        """Extract area in square feet"""
        try:
            text = listing_element.get_text()
            # Look for area patterns like "1,200 sq ft" or "1200 sqft"
            area_match = re.search(r'([\d,]+)\s*sq\s*(?:ft|feet)', text, re.IGNORECASE)
            if area_match:
                area_str = area_match.group(1).replace(',', '')
                return float(area_str)
            return 0.0
        except:
            return 0.0
    
    def _extract_property_type(self, listing_element) -> str:
        """Extract property type"""
        try:
            text = listing_element.get_text().lower()
            if 'apartment' in text:
                return 'Apartment'
            elif 'villa' in text:
                return 'Villa'
            elif 'townhouse' in text:
                return 'Townhouse'
            elif 'penthouse' in text:
                return 'Penthouse'
            elif 'studio' in text:
                return 'Studio'
            else:
                return 'Unknown'
        except:
            return 'Unknown'
    
    def _extract_developer(self, listing_element) -> str:
        """Extract developer name"""
        try:
            # Common Dubai developers
            developers = ['Emaar', 'Nakheel', 'Dubai Properties', 'Meraas', 'Azizi', 'Damac']
            text = listing_element.get_text()
            
            for developer in developers:
                if developer.lower() in text.lower():
                    return developer
            
            return 'Unknown'
        except:
            return 'Unknown'
    
    def _extract_amenities(self, listing_element) -> List[str]:
        """Extract amenities list"""
        try:
            amenities = []
            text = listing_element.get_text().lower()
            
            # Common amenities to look for
            amenity_keywords = [
                'parking', 'gym', 'pool', 'garden', 'balcony', 'elevator',
                'security', 'concierge', 'maid', 'storage', 'terrace',
                'beach access', 'metro', 'school', 'hospital', 'mall'
            ]
            
            for amenity in amenity_keywords:
                if amenity in text:
                    amenities.append(amenity.title())
            
            return amenities
        except:
            return []
    
    def scrape_all_areas(self, property_type: str = 'apartment', max_pages_per_area: int = 3) -> List[Dict]:
        """
        Scrape properties from all Dubai areas
        """
        all_properties = []
        
        for area_key, area_name in self.dubai_areas.items():
            logger.info(f"Scraping {area_name} ({area_key})")
            
            try:
                properties = self.scrape_dubizzle(area_key, property_type, max_pages_per_area)
                all_properties.extend(properties)
                
                # Add delay between areas
                time.sleep(5)
                
            except Exception as e:
                logger.error(f"Error scraping {area_name}: {e}")
                continue
        
        logger.info(f"Total properties collected: {len(all_properties)}")
        return all_properties
    
    def save_to_csv(self, properties: List[Dict], filename: str = None) -> str:
        """
        Save properties to CSV file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dubai_properties_{timestamp}.csv"
        
        df = pd.DataFrame(properties)
        df.to_csv(filename, index=False)
        
        logger.info(f"Saved {len(properties)} properties to {filename}")
        return filename
    
    def save_to_json(self, properties: List[Dict], filename: str = None) -> str:
        """
        Save properties to JSON file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dubai_properties_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(properties, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(properties)} properties to {filename}")
        return filename

def main():
    """
    Main function to run the scraper
    """
    scraper = DubaiPropertyScraper()
    
    # Example: Scrape Dubai Marina apartments
    print("Starting Dubai Marina apartment scrape...")
    properties = scraper.scrape_dubizzle('dubai-marina', 'apartment', max_pages=3)
    
    if properties:
        # Save to CSV
        csv_file = scraper.save_to_csv(properties, 'dubai_marina_apartments.csv')
        print(f"Saved {len(properties)} properties to {csv_file}")
        
        # Save to JSON
        json_file = scraper.save_to_json(properties, 'dubai_marina_apartments.json')
        print(f"Saved {len(properties)} properties to {json_file}")
        
        # Display sample data
        print("\nSample property data:")
        print(json.dumps(properties[0], indent=2))
    else:
        print("No properties found")

if __name__ == "__main__":
    main()

