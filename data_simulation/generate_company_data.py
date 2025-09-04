#!/usr/bin/env python3
"""
Comprehensive Data Generation Script for Dubai Real Estate Company Simulation
Creates realistic data for CRM, transactions, policies, and operational documents
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import json
import os
from fpdf import FPDF
import uuid

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

class DubaiRealEstateDataGenerator:
    def __init__(self):
        self.output_dir = "generated_data"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Dubai areas and neighborhoods
        self.dubai_areas = {
            'Dubai Marina': ['Marina Heights', 'Marina Gate', 'Marina Promenade', 'Marina Shores', 'Marina Heights 2'],
            'Downtown Dubai': ['Burj Vista', 'The Address', 'Burj Views', 'Downtown Views', 'The Residences'],
            'Palm Jumeirah': ['Palm Tower', 'Palm Vista', 'Palm Heights', 'Palm Gardens', 'Palm Residences'],
            'Business Bay': ['Bay Square', 'Bay Central', 'Bay Heights', 'Bay Views', 'Bay Residences'],
            'JBR': ['JBR Heights', 'JBR Views', 'JBR Central', 'JBR Residences', 'JBR Gardens'],
            'Jumeirah': ['Jumeirah Heights', 'Jumeirah Views', 'Jumeirah Central', 'Jumeirah Residences'],
            'DIFC': ['DIFC Heights', 'DIFC Views', 'DIFC Central', 'DIFC Residences'],
            'Emirates Hills': ['Hills Heights', 'Hills Views', 'Hills Central', 'Hills Residences'],
            'Arabian Ranches': ['Ranches Heights', 'Ranches Views', 'Ranches Central', 'Ranches Residences']
        }
        
        # Property types and their characteristics
        self.property_types = {
            'apartment': {'min_price': 500000, 'max_price': 8000000, 'min_bedrooms': 1, 'max_bedrooms': 4},
            'villa': {'min_price': 2000000, 'max_price': 25000000, 'min_bedrooms': 3, 'max_bedrooms': 7},
            'townhouse': {'min_price': 1500000, 'max_price': 12000000, 'min_bedrooms': 2, 'max_bedrooms': 5},
            'penthouse': {'min_price': 3000000, 'max_price': 50000000, 'min_bedrooms': 2, 'max_bedrooms': 6},
            'studio': {'min_price': 300000, 'max_price': 1500000, 'min_bedrooms': 0, 'max_bedrooms': 1}
        }
        
        # Developers
        self.developers = [
            'Emaar Properties', 'Damac Properties', 'Nakheel', 'Sobha Realty', 'Meraas',
            'Dubai Properties', 'Azizi Developments', 'Deyaar Development', 'Union Properties',
            'Al Habtoor Group', 'Omniyat', 'Select Group', 'Binghatti Developers'
        ]
        
        # Agent names
        self.agents = [
            'Ahmed Al Mansouri', 'Sarah Johnson', 'Mohammed Al Rashid', 'Emily Chen',
            'Ali Hassan', 'Lisa Thompson', 'Omar Al Zaabi', 'Jennifer Smith',
            'Fatima Al Qassimi', 'David Wilson', 'Aisha Al Falasi', 'Michael Brown',
            'Khalid Al Suwaidi', 'Rachel Green', 'Abdullah Al Muhairi', 'Amanda Davis'
        ]

    def generate_property_listings(self, num_listings=8000):
        """Generate comprehensive property listings with agent assignments"""
        print(f"Generating {num_listings} property listings...")
        
        listings = []
        for i in range(num_listings):
            # Select random area and building
            area = random.choice(list(self.dubai_areas.keys()))
            building = random.choice(self.dubai_areas[area])
            
            # Select property type
            prop_type = random.choice(list(self.property_types.keys()))
            type_config = self.property_types[prop_type]
            
            # Generate realistic property data
            bedrooms = random.randint(type_config['min_bedrooms'], type_config['max_bedrooms'])
            bathrooms = bedrooms + random.randint(0, 2)
            area_sqft = random.randint(500 + bedrooms * 200, 2000 + bedrooms * 300)
            
            # Generate realistic price based on area, type, and size
            base_price = type_config['min_price'] + (area_sqft - 500) * 1000
            price_variation = random.uniform(0.8, 1.4)
            price = int(base_price * price_variation)
            
            # Ensure price is within bounds
            price = max(type_config['min_price'], min(price, type_config['max_price']))
            
            # Generate listing data
            listing = {
                'listing_id': f"LST-{str(i+1).zfill(6)}",
                'title': f"{bedrooms}BR {prop_type.title()} in {building}",
                'property_type': prop_type,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'area_sqft': area_sqft,
                'price_aed': price,
                'price_per_sqft': int(price / area_sqft),
                'location': area,
                'building': building,
                'developer': random.choice(self.developers),
                'agent_id': random.choice(self.agents),
                'listing_status': random.choice(['active', 'under_contract', 'sold', 'withdrawn']),
                'listing_date': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d'),
                'last_updated': datetime.now().strftime('%Y-%m-%d'),
                'views_count': random.randint(50, 2000),
                'furnished': random.choice([True, False]),
                'parking_spaces': random.randint(0, 3),
                'balcony': random.choice([True, False]),
                'gym_access': random.choice([True, False]),
                'pool_access': random.choice([True, False]),
                'security': random.choice([True, False]),
                'description': f"Beautiful {bedrooms}-bedroom {prop_type} in prestigious {building}, {area}. "
                             f"Features {bathrooms} bathrooms, {area_sqft} sqft of living space. "
                             f"Perfect for {'families' if bedrooms > 2 else 'professionals'}."
            }
            listings.append(listing)
        
        # Convert to DataFrame and save
        df = pd.DataFrame(listings)
        df.to_csv(f"{self.output_dir}/property_listings.csv", index=False)
        print(f"✅ Generated {len(listings)} property listings")
        return df

    def generate_transactions(self, num_transactions=50000):
        """Generate transaction data for the last 6 months"""
        print(f"Generating {num_transactions} transactions...")
        
        transactions = []
        start_date = datetime.now() - timedelta(days=180)
        
        for i in range(num_transactions):
            # Generate transaction date within last 6 months
            transaction_date = start_date + timedelta(days=random.randint(0, 180))
            
            # Generate realistic transaction data
            transaction = {
                'transaction_id': f"TXN-{str(i+1).zfill(8)}",
                'listing_id': f"LST-{str(random.randint(1, 8000)).zfill(6)}",
                'buyer_name': f"Buyer {random.randint(1, 1000)}",
                'seller_name': f"Seller {random.randint(1, 500)}",
                'agent_id': random.choice(self.agents),
                'transaction_type': random.choice(['sale', 'rental']),
                'transaction_date': transaction_date.strftime('%Y-%m-%d'),
                'closing_date': (transaction_date + timedelta(days=random.randint(30, 90))).strftime('%Y-%m-%d'),
                'transaction_amount': random.randint(500000, 15000000),
                'commission_amount': random.randint(10000, 500000),
                'commission_rate': random.uniform(2.0, 5.0),
                'payment_method': random.choice(['cash', 'mortgage', 'bank_transfer']),
                'status': random.choice(['completed', 'pending', 'cancelled']),
                'notes': f"Transaction {i+1} notes"
            }
            transactions.append(transaction)
        
        # Convert to DataFrame and save
        df = pd.DataFrame(transactions)
        df.to_csv(f"{self.output_dir}/transactions.csv", index=False)
        print(f"✅ Generated {len(transactions)} transactions")
        return df

    def generate_agent_performance(self):
        """Generate agent performance metrics"""
        print("Generating agent performance data...")
        
        performance_data = []
        for agent in self.agents:
            performance = {
                'agent_id': agent,
                'total_listings': random.randint(50, 300),
                'active_listings': random.randint(10, 100),
                'sold_listings': random.randint(20, 150),
                'total_sales_volume': random.randint(50000000, 500000000),
                'average_commission_rate': random.uniform(2.5, 4.5),
                'client_satisfaction_score': random.uniform(3.5, 5.0),
                'response_time_hours': random.uniform(1, 24),
                'showings_per_month': random.randint(20, 100),
                'conversion_rate': random.uniform(0.1, 0.3),
                'years_experience': random.randint(1, 15),
                'specializations': random.choice(['residential', 'commercial', 'luxury', 'investment']),
                'languages': random.choice(['English', 'Arabic', 'English, Arabic', 'English, Hindi', 'English, Russian'])
            }
            performance_data.append(performance)
        
        df = pd.DataFrame(performance_data)
        df.to_csv(f"{self.output_dir}/agent_performance.csv", index=False)
        print(f"✅ Generated agent performance data for {len(self.agents)} agents")
        return df

    def generate_market_data(self):
        """Generate market trends and analytics data"""
        print("Generating market data...")
        
        market_data = []
        areas = list(self.dubai_areas.keys())
        
        for area in areas:
            for month in range(6):
                date = (datetime.now() - timedelta(days=30*month)).strftime('%Y-%m')
                
                market_entry = {
                    'area': area,
                    'month': date,
                    'average_price_per_sqft': random.randint(800, 2500),
                    'price_change_percent': random.uniform(-10, 15),
                    'days_on_market': random.randint(15, 120),
                    'inventory_count': random.randint(50, 500),
                    'sales_count': random.randint(10, 100),
                    'rental_yield_percent': random.uniform(4.0, 8.0),
                    'demand_score': random.uniform(0.3, 1.0),
                    'supply_score': random.uniform(0.3, 1.0),
                    'market_sentiment': random.choice(['positive', 'neutral', 'negative'])
                }
                market_data.append(market_entry)
        
        df = pd.DataFrame(market_data)
        df.to_csv(f"{self.output_dir}/market_trends.csv", index=False)
        print(f"✅ Generated market data for {len(areas)} areas over 6 months")
        return df

    def generate_client_data(self, num_clients=2000):
        """Generate client database"""
        print(f"Generating {num_clients} client records...")
        
        clients = []
        for i in range(num_clients):
            client = {
                'client_id': f"CLT-{str(i+1).zfill(6)}",
                'first_name': f"Client{i+1}",
                'last_name': f"Name{i+1}",
                'email': f"client{i+1}@email.com",
                'phone': f"+9715{random.randint(10000000, 99999999)}",
                'nationality': random.choice(['UAE', 'UK', 'USA', 'India', 'Pakistan', 'Russia', 'China', 'Saudi Arabia']),
                'client_type': random.choice(['buyer', 'seller', 'investor', 'tenant']),
                'budget_range': random.choice(['500K-1M', '1M-2M', '2M-5M', '5M-10M', '10M+']),
                'preferred_areas': random.choice(list(self.dubai_areas.keys())),
                'agent_assigned': random.choice(self.agents),
                'lead_source': random.choice(['website', 'referral', 'social_media', 'walk_in', 'cold_call']),
                'lead_score': random.randint(1, 100),
                'last_contact': (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d'),
                'status': random.choice(['active', 'qualified', 'proposal', 'negotiation', 'closed', 'lost'])
            }
            clients.append(client)
        
        df = pd.DataFrame(clients)
        df.to_csv(f"{self.output_dir}/clients.csv", index=False)
        print(f"✅ Generated {len(clients)} client records")
        return df

    def create_company_policies_pdf(self):
        """Create company policies PDF"""
        print("Creating company policies PDF...")
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=16)
        
        # Title
        pdf.cell(200, 10, txt="Dubai Real Estate Company - Policies & Procedures", ln=True, align='C')
        pdf.ln(10)
        
        policies = [
            ("Commission Structure", "Standard commission rate is 3% for residential properties and 4% for commercial properties. Luxury properties (>10M AED) have a 2% commission rate."),
            ("Client Communication", "All client communications must be responded to within 4 hours during business hours. Weekend responses within 12 hours."),
            ("Property Showings", "Agents must accompany all property showings. Virtual tours are acceptable for international clients."),
            ("Documentation", "All transactions require complete documentation including ID verification, proof of funds, and legal compliance checks."),
            ("Marketing Guidelines", "All property marketing materials must be approved by the marketing department before publication."),
            ("Data Protection", "Client information must be handled according to UAE data protection laws. No sharing of client data without consent."),
            ("Conflict Resolution", "Any conflicts between agents or with clients must be escalated to the management team immediately."),
            ("Professional Standards", "Agents must maintain professional appearance and conduct at all times. Business attire required for client meetings.")
        ]
        
        pdf.set_font("Arial", size=12)
        for title, content in policies:
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, txt=title, ln=True)
            pdf.set_font("Arial", size=10)
            pdf.multi_cell(0, 5, txt=content)
            pdf.ln(5)
        
        pdf.output(f"{self.output_dir}/company_policies.pdf")
        print("✅ Created company policies PDF")

    def create_agent_guide_pdf(self):
        """Create comprehensive agent guide PDF"""
        print("Creating agent guide PDF...")
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=16)
        
        # Title
        pdf.cell(200, 10, txt="Dubai Real Estate Agent Guide", ln=True, align='C')
        pdf.ln(10)
        
        sections = [
            ("Sales Techniques", [
                "Building rapport with clients",
                "Understanding client needs",
                "Presenting properties effectively",
                "Handling objections professionally",
                "Closing techniques and strategies"
            ]),
            ("Market Knowledge", [
                "Dubai real estate market trends",
                "Area-specific information",
                "Property valuation methods",
                "Investment opportunities",
                "Legal and regulatory requirements"
            ]),
            ("Client Management", [
                "Lead generation strategies",
                "Client relationship building",
                "Follow-up procedures",
                "CRM system usage",
                "Client satisfaction measurement"
            ]),
            ("Technology Tools", [
                "CRM software training",
                "Virtual tour platforms",
                "Social media marketing",
                "Digital marketing tools",
                "Mobile app usage"
            ])
        ]
        
        pdf.set_font("Arial", size=12)
        for section_title, items in sections:
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, txt=section_title, ln=True)
            pdf.set_font("Arial", size=10)
            for item in items:
                pdf.cell(200, 8, txt=f"- {item}", ln=True)
            pdf.ln(5)
        
        pdf.output(f"{self.output_dir}/agent_guide.pdf")
        print("✅ Created agent guide PDF")

    def create_neighborhood_profiles(self):
        """Create neighborhood profile documents"""
        print("Creating neighborhood profiles...")
        
        for area, buildings in self.dubai_areas.items():
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=16)
            
            # Title
            pdf.cell(200, 10, txt=f"{area} - Neighborhood Profile", ln=True, align='C')
            pdf.ln(10)
            
            # Content
            pdf.set_font("Arial", size=12)
            content = f"""
            {area} is one of Dubai's most prestigious residential areas, known for its luxury properties and world-class amenities.
            
            Key Features:
            - Average property prices: AED {random.randint(800, 2500)} per sqft
            - Popular property types: Apartments, Villas, Penthouses
            - Average rental yield: {random.uniform(4.0, 8.0):.1f}%
            - Days on market: {random.randint(15, 120)} days
            
            Amenities:
            - Shopping centers and retail outlets
            - Restaurants and cafes
            - Schools and educational institutions
            - Healthcare facilities
            - Transportation links
            
            Notable Buildings: {', '.join(buildings[:3])}
            
            Market Outlook:
            The {area} market shows strong demand with steady price appreciation. 
            Investment opportunities are available for both residential and commercial properties.
            """
            
            pdf.multi_cell(0, 5, txt=content)
            pdf.output(f"{self.output_dir}/{area.replace(' ', '_')}_profile.pdf")
        
        print(f"✅ Created neighborhood profiles for {len(self.dubai_areas)} areas")

    def create_service_charges_guide(self):
        """Create service charges guide"""
        print("Creating service charges guide...")
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=16)
        
        # Title
        pdf.cell(200, 10, txt="Dubai Service Charges Guide", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font("Arial", size=12)
        content = """
        Service Charges in Dubai Real Estate
        
        Standard Service Charges:
        - Residential Apartments: AED 12-25 per sqft annually
        - Villas: AED 8-15 per sqft annually
        - Commercial Properties: AED 15-35 per sqft annually
        - Luxury Properties: AED 20-40 per sqft annually
        
        What's Included:
        - Building maintenance and repairs
        - Security services
        - Cleaning and landscaping
        - Common area utilities
        - Building insurance
        - Management fees
        
        Additional Charges:
        - Parking: AED 500-2000 annually
        - Storage: AED 300-1000 annually
        - Gym membership: AED 1000-3000 annually
        - Pool access: AED 500-1500 annually
        
        Payment Schedule:
        - Quarterly payments (most common)
        - Annual payments (with discount)
        - Monthly payments (for some developments)
        
        Important Notes:
        - Service charges are mandatory for all properties
        - Non-payment can result in legal action
        - Charges are reviewed annually
        - Disputes can be filed with RERA
        """
        
        pdf.multi_cell(0, 5, txt=content)
        pdf.output(f"{self.output_dir}/service_charges_guide.pdf")
        print("✅ Created service charges guide")

    def generate_all_data(self):
        """Generate all simulation data"""
        print("🚀 Starting comprehensive data generation...")
        
        # Generate CSV files
        self.generate_property_listings(8000)
        self.generate_transactions(50000)
        self.generate_agent_performance()
        self.generate_market_data()
        self.generate_client_data(2000)
        
        # Generate PDF documents
        self.create_company_policies_pdf()
        self.create_agent_guide_pdf()
        self.create_neighborhood_profiles()
        self.create_service_charges_guide()
        
        print("\n🎉 All data generation completed!")
        print(f"📁 Data saved to: {self.output_dir}/")
        
        # Create summary
        self.create_data_summary()

    def create_data_summary(self):
        """Create a summary of all generated data"""
        summary = {
            "generated_files": {
                "csv_files": [
                    "property_listings.csv - 8,000 property listings with agent assignments",
                    "transactions.csv - 50,000 transactions from last 6 months",
                    "agent_performance.csv - Performance metrics for 16 agents",
                    "market_trends.csv - Market trends for 9 areas over 6 months",
                    "clients.csv - 2,000 client records with lead scoring"
                ],
                "pdf_files": [
                    "company_policies.pdf - Company policies and procedures",
                    "agent_guide.pdf - Comprehensive agent training guide",
                    "neighborhood_profiles.pdf - 9 area-specific profiles",
                    "service_charges_guide.pdf - Service charges information"
                ]
            },
            "data_characteristics": {
                "total_properties": 8000,
                "total_transactions": 50000,
                "total_clients": 2000,
                "total_agents": 16,
                "total_areas": 9,
                "property_types": 5,
                "developers": 13
            },
            "usage_instructions": [
                "1. Upload CSV files through the UI for property and transaction data",
                "2. Upload PDF files for policies, guides, and documentation",
                "3. The intelligent processor will categorize and vectorize all data",
                "4. Data will be available for RAG queries and AI responses"
            ]
        }
        
        with open(f"{self.output_dir}/data_summary.json", 'w') as f:
            json.dump(summary, f, indent=2)
        
        print("✅ Created data summary")

if __name__ == "__main__":
    generator = DubaiRealEstateDataGenerator()
    generator.generate_all_data()
