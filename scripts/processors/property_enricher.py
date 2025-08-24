#!/usr/bin/env python3
"""
Property Data Enricher
Enhances property data with additional insights, coordinates, and market analysis
"""

import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import json
import logging
from typing import Dict, List, Tuple, Optional
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PropertyDataEnricher:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="dubai_real_estate_enricher")
        
        # Key Dubai locations with coordinates
        self.key_locations = {
            'Dubai Mall': (25.197197, 55.274376),
            'Dubai Marina': (25.0920, 55.1381),
            'Dubai Airport': (25.2532, 55.3657),
            'Palm Jumeirah': (25.1124, 55.1390),
            'Downtown Dubai': (25.1972, 55.2744),
            'Business Bay': (25.1867, 55.2767),
            'JBR': (25.0920, 55.1381),
            'Dubai Hills Estate': (25.0587, 55.2387),
            'Arabian Ranches': (25.0587, 55.2387),
            'Dubai Silicon Oasis': (25.1124, 55.1390),
            'Dubai Sports City': (25.0587, 55.2387),
            'Dubai Motor City': (25.0587, 55.2387),
            'Dubai Media City': (25.1124, 55.1390),
            'Dubai Internet City': (25.1124, 55.1390),
            'Dubai Knowledge Village': (25.1124, 55.1390)
        }
        
        # Dubai area coordinates (approximate centers)
        self.area_coordinates = {
            'Dubai Marina': (25.0920, 55.1381),
            'Downtown Dubai': (25.1972, 55.2744),
            'Palm Jumeirah': (25.1124, 55.1390),
            'JBR': (25.0920, 55.1381),
            'Business Bay': (25.1867, 55.2767),
            'Dubai Hills Estate': (25.0587, 55.2387),
            'Arabian Ranches': (25.0587, 55.2387),
            'Emirates Hills': (25.0587, 55.2387),
            'The Springs': (25.0587, 55.2387),
            'The Meadows': (25.0587, 55.2387),
            'The Lakes': (25.0587, 55.2387),
            'Dubai Silicon Oasis': (25.1124, 55.1390),
            'Dubai Sports City': (25.0587, 55.2387),
            'Dubai Motor City': (25.0587, 55.2387),
            'Dubai Production City': (25.1124, 55.1390),
            'Dubai Knowledge Village': (25.1124, 55.1390),
            'Dubai Media City': (25.1124, 55.1390),
            'Dubai Internet City': (25.1124, 55.1390)
        }
    
    def enrich_properties(self, properties_df: pd.DataFrame) -> pd.DataFrame:
        """
        Enhance property data with additional insights
        """
        logger.info("Starting property enrichment process")
        
        # Create a copy to avoid modifying original
        enriched_df = properties_df.copy()
        
        # Add coordinates
        enriched_df = self._add_coordinates(enriched_df)
        
        # Add distance calculations
        enriched_df = self._add_distance_calculations(enriched_df)
        
        # Add market insights
        enriched_df = self._add_market_insights(enriched_df)
        
        # Add investment scores
        enriched_df = self._add_investment_scores(enriched_df)
        
        # Add area classifications
        enriched_df = self._add_area_classifications(enriched_df)
        
        # Add price analysis
        enriched_df = self._add_price_analysis(enriched_df)
        
        logger.info("Property enrichment completed")
        return enriched_df
    
    def _add_coordinates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add coordinates to properties"""
        logger.info("Adding coordinates to properties")
        
        df['latitude'] = None
        df['longitude'] = None
        
        for idx, row in df.iterrows():
            try:
                # Try to get coordinates from location
                location_query = f"{row['location']}, Dubai, UAE"
                location = self.geolocator.geocode(location_query, timeout=10)
                
                if location:
                    df.at[idx, 'latitude'] = location.latitude
                    df.at[idx, 'longitude'] = location.longitude
                else:
                    # Fallback to area coordinates
                    area_name = self._extract_area_name(row['location'])
                    if area_name in self.area_coordinates:
                        lat, lon = self.area_coordinates[area_name]
                        df.at[idx, 'latitude'] = lat
                        df.at[idx, 'longitude'] = lon
                
                # Add delay to be respectful to geocoding service
                time.sleep(1)
                
            except Exception as e:
                logger.warning(f"Error getting coordinates for property {idx}: {e}")
                continue
        
        return df
    
    def _extract_area_name(self, location: str) -> str:
        """Extract area name from location string"""
        location_lower = location.lower()
        
        for area in self.area_coordinates.keys():
            if area.lower() in location_lower:
                return area
        
        return "Unknown"
    
    def _add_distance_calculations(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add distance calculations to key locations"""
        logger.info("Adding distance calculations")
        
        for location_name, coords in self.key_locations.items():
            distance_col = f'distance_to_{location_name.lower().replace(" ", "_")}'
            df[distance_col] = None
            
            for idx, row in df.iterrows():
                if pd.notna(row['latitude']) and pd.notna(row['longitude']):
                    try:
                        property_coords = (row['latitude'], row['longitude'])
                        distance = geodesic(property_coords, coords).kilometers
                        df.at[idx, distance_col] = round(distance, 2)
                    except Exception as e:
                        logger.warning(f"Error calculating distance for property {idx}: {e}")
                        continue
        
        return df
    
    def _add_market_insights(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add market insights and analysis"""
        logger.info("Adding market insights")
        
        # Calculate price per square foot
        df['price_per_sqft'] = df.apply(
            lambda row: row['price'] / row['area_sqft'] if row['area_sqft'] > 0 else 0, 
            axis=1
        )
        
        # Calculate price per bedroom
        df['price_per_bedroom'] = df.apply(
            lambda row: row['price'] / row['bedrooms'] if row['bedrooms'] > 0 else 0, 
            axis=1
        )
        
        # Add area-based price statistics
        df = self._add_area_price_stats(df)
        
        return df
    
    def _add_area_price_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add area-based price statistics"""
        # Calculate area statistics
        area_stats = df.groupby('location').agg({
            'price': ['mean', 'median', 'std', 'count'],
            'price_per_sqft': ['mean', 'median'],
            'area_sqft': ['mean', 'median']
        }).round(2)
        
        # Flatten column names
        area_stats.columns = ['_'.join(col).strip() for col in area_stats.columns]
        area_stats = area_stats.reset_index()
        
        # Merge back to main dataframe
        df = df.merge(area_stats, on='location', how='left', suffixes=('', '_area_avg'))
        
        # Calculate price position relative to area average
        df['price_vs_area_avg'] = df.apply(
            lambda row: ((row['price'] - row['price_mean']) / row['price_mean'] * 100) 
            if pd.notna(row['price_mean']) and row['price_mean'] > 0 else 0, 
            axis=1
        )
        
        return df
    
    def _add_investment_scores(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate investment potential scores"""
        logger.info("Adding investment scores")
        
        # Initialize investment score
        df['investment_score'] = 0
        
        for idx, row in df.iterrows():
            score = 0
            
            # Price factor (lower price = higher score)
            if row['price'] > 0:
                price_score = max(0, 10 - (row['price'] / 1000000))  # Score decreases with price
                score += price_score * 0.3
            
            # Location factor (proximity to key areas)
            if pd.notna(row['distance_to_dubai_marina']):
                marina_score = max(0, 10 - row['distance_to_dubai_marina'])
                score += marina_score * 0.2
            
            if pd.notna(row['distance_to_dubai_mall']):
                mall_score = max(0, 10 - row['distance_to_dubai_mall'])
                score += mall_score * 0.2
            
            # Size factor (larger properties get higher score)
            if row['area_sqft'] > 0:
                size_score = min(10, row['area_sqft'] / 1000)
                score += size_score * 0.15
            
            # Bedroom factor
            bedroom_score = min(10, row['bedrooms'] * 2)
            score += bedroom_score * 0.15
            
            df.at[idx, 'investment_score'] = round(score, 2)
        
        return df
    
    def _add_area_classifications(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add area classifications and categories"""
        logger.info("Adding area classifications")
        
        # Define area categories
        area_categories = {
            'Luxury': ['Palm Jumeirah', 'Emirates Hills', 'Downtown Dubai'],
            'Premium': ['Dubai Marina', 'JBR', 'Business Bay'],
            'Family': ['Arabian Ranches', 'Dubai Hills Estate', 'The Springs', 'The Meadows', 'The Lakes'],
            'Business': ['Dubai Silicon Oasis', 'Dubai Media City', 'Dubai Internet City', 'Dubai Knowledge Village'],
            'Sports': ['Dubai Sports City', 'Dubai Motor City']
        }
        
        # Add area category
        df['area_category'] = 'Other'
        for category, areas in area_categories.items():
            for area in areas:
                mask = df['location'].str.contains(area, case=False, na=False)
                df.loc[mask, 'area_category'] = category
        
        # Add property size category
        df['size_category'] = df['area_sqft'].apply(self._categorize_size)
        
        # Add price category
        df['price_category'] = df['price'].apply(self._categorize_price)
        
        return df
    
    def _categorize_size(self, area_sqft: float) -> str:
        """Categorize property by size"""
        if area_sqft < 500:
            return 'Studio'
        elif area_sqft < 1000:
            return 'Small'
        elif area_sqft < 2000:
            return 'Medium'
        elif area_sqft < 4000:
            return 'Large'
        else:
            return 'Extra Large'
    
    def _categorize_price(self, price: float) -> str:
        """Categorize property by price"""
        if price < 500000:
            return 'Budget'
        elif price < 1000000:
            return 'Mid-Range'
        elif price < 3000000:
            return 'High-End'
        elif price < 10000000:
            return 'Luxury'
        else:
            return 'Ultra-Luxury'
    
    def _add_price_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add price analysis and trends"""
        logger.info("Adding price analysis")
        
        # Calculate price ranges
        df['price_range'] = df['price'].apply(self._get_price_range)
        
        # Add market positioning
        df['market_position'] = df['price_vs_area_avg'].apply(self._get_market_position)
        
        # Add value indicators
        df['value_indicator'] = df.apply(self._calculate_value_indicator, axis=1)
        
        return df
    
    def _get_price_range(self, price: float) -> str:
        """Get price range category"""
        if price < 300000:
            return 'Under 300K'
        elif price < 500000:
            return '300K-500K'
        elif price < 1000000:
            return '500K-1M'
        elif price < 2000000:
            return '1M-2M'
        elif price < 5000000:
            return '2M-5M'
        else:
            return '5M+'
    
    def _get_market_position(self, price_vs_avg: float) -> str:
        """Get market positioning based on price vs area average"""
        if price_vs_avg < -20:
            return 'Below Market'
        elif price_vs_avg < -5:
            return 'Slightly Below Market'
        elif price_vs_avg < 5:
            return 'Market Rate'
        elif price_vs_avg < 20:
            return 'Slightly Above Market'
        else:
            return 'Above Market'
    
    def _calculate_value_indicator(self, row) -> str:
        """Calculate value indicator based on price and features"""
        if row['price'] == 0 or row['area_sqft'] == 0:
            return 'Unknown'
        
        price_per_sqft = row['price'] / row['area_sqft']
        
        # Compare with area average
        if pd.notna(row['price_per_sqft_mean']):
            if price_per_sqft < row['price_per_sqft_mean'] * 0.8:
                return 'Good Value'
            elif price_per_sqft < row['price_per_sqft_mean']:
                return 'Fair Value'
            elif price_per_sqft < row['price_per_sqft_mean'] * 1.2:
                return 'Premium'
            else:
                return 'Overpriced'
        
        return 'Unknown'
    
    def generate_market_report(self, df: pd.DataFrame) -> Dict:
        """Generate market analysis report"""
        logger.info("Generating market report")
        
        report = {
            'summary': {
                'total_properties': len(df),
                'avg_price': df['price'].mean(),
                'median_price': df['price'].median(),
                'avg_price_per_sqft': df['price_per_sqft'].mean(),
                'total_value': df['price'].sum()
            },
            'by_area': {},
            'by_property_type': {},
            'by_price_range': {},
            'top_areas': [],
            'investment_opportunities': []
        }
        
        # Area analysis
        area_stats = df.groupby('location').agg({
            'price': ['count', 'mean', 'median'],
            'price_per_sqft': 'mean',
            'investment_score': 'mean'
        }).round(2)
        
        for area in area_stats.index:
            report['by_area'][area] = {
                'count': int(area_stats.loc[area, ('price', 'count')]),
                'avg_price': float(area_stats.loc[area, ('price', 'mean')]),
                'median_price': float(area_stats.loc[area, ('price', 'median')]),
                'avg_price_per_sqft': float(area_stats.loc[area, ('price_per_sqft', 'mean')]),
                'avg_investment_score': float(area_stats.loc[area, ('investment_score', 'mean')])
            }
        
        # Top investment opportunities
        top_opportunities = df.nlargest(10, 'investment_score')[
            ['title', 'location', 'price', 'area_sqft', 'bedrooms', 'investment_score']
        ]
        report['investment_opportunities'] = top_opportunities.to_dict('records')
        
        return report
    
    def save_enriched_data(self, df: pd.DataFrame, filename: str = None) -> str:
        """Save enriched data to CSV"""
        if not filename:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"enriched_dubai_properties_{timestamp}.csv"
        
        df.to_csv(filename, index=False)
        logger.info(f"Saved enriched data to {filename}")
        return filename

def main():
    """Main function to test the enricher"""
    # Load sample data
    try:
        df = pd.read_csv('dubai_marina_apartments.csv')
        print(f"Loaded {len(df)} properties")
        
        # Initialize enricher
        enricher = PropertyDataEnricher()
        
        # Enrich data
        enriched_df = enricher.enrich_properties(df)
        
        # Save enriched data
        filename = enricher.save_enriched_data(enriched_df)
        print(f"Enriched data saved to {filename}")
        
        # Generate market report
        report = enricher.generate_market_report(enriched_df)
        print("\nMarket Report Summary:")
        print(f"Total Properties: {report['summary']['total_properties']}")
        print(f"Average Price: AED {report['summary']['avg_price']:,.0f}")
        print(f"Average Price per Sq Ft: AED {report['summary']['avg_price_per_sqft']:,.0f}")
        
    except FileNotFoundError:
        print("No sample data found. Please run the scraper first.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

