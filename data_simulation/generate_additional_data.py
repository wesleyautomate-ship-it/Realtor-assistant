#!/usr/bin/env python3
"""
Additional Data Generation Script for Enhanced Dubai Real Estate Simulation
Creates additional data files for comprehensive company operations simulation
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import json
import os
from fpdf import FPDF

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

class AdditionalDataGenerator:
    def __init__(self):
        self.output_dir = "generated_data"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Additional data for comprehensive simulation
        self.lead_sources = ['website', 'referral', 'social_media', 'walk_in', 'cold_call', 'property_portal', 'email_campaign', 'event']
        self.property_amenities = ['gym', 'pool', 'parking', 'security', 'balcony', 'garden', 'elevator', 'concierge', 'playground', 'tennis_court']
        self.transaction_statuses = ['pending', 'in_progress', 'completed', 'cancelled', 'expired']
        self.client_preferences = ['family_home', 'investment', 'luxury', 'budget_friendly', 'city_center', 'suburban', 'beachfront', 'mountain_view']

    def generate_lead_data(self, num_leads=5000):
        """Generate comprehensive lead data"""
        print(f"Generating {num_leads} lead records...")
        
        leads = []
        for i in range(num_leads):
            lead = {
                'lead_id': f"LEAD-{str(i+1).zfill(6)}",
                'first_name': f"Lead{i+1}",
                'last_name': f"Contact{i+1}",
                'email': f"lead{i+1}@email.com",
                'phone': f"+9715{random.randint(10000000, 99999999)}",
                'lead_source': random.choice(self.lead_sources),
                'lead_score': random.randint(1, 100),
                'budget_min': random.randint(500000, 5000000),
                'budget_max': random.randint(1000000, 10000000),
                'preferred_areas': random.choice(['Dubai Marina', 'Downtown Dubai', 'Palm Jumeirah', 'Business Bay', 'JBR']),
                'property_type': random.choice(['apartment', 'villa', 'townhouse', 'penthouse']),
                'bedrooms': random.randint(1, 5),
                'timeline': random.choice(['immediate', '1-3_months', '3-6_months', '6+_months']),
                'lead_status': random.choice(['new', 'contacted', 'qualified', 'proposal_sent', 'negotiating', 'closed', 'lost']),
                'assigned_agent': random.choice(['Ahmed Al Mansouri', 'Sarah Johnson', 'Mohammed Al Rashid', 'Emily Chen']),
                'created_date': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d'),
                'last_contact': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
                'notes': f"Lead {i+1} notes - {random.choice(['interested in investment', 'looking for family home', 'luxury buyer', 'first time buyer'])}"
            }
            leads.append(lead)
        
        df = pd.DataFrame(leads)
        df.to_csv(f"{self.output_dir}/leads.csv", index=False)
        print(f"✅ Generated {len(leads)} lead records")
        return df

    def generate_property_analytics(self):
        """Generate property analytics and insights"""
        print("Generating property analytics...")
        
        analytics = []
        areas = ['Dubai Marina', 'Downtown Dubai', 'Palm Jumeirah', 'Business Bay', 'JBR', 'Jumeirah', 'DIFC', 'Emirates Hills', 'Arabian Ranches']
        
        for area in areas:
            for month in range(12):
                date = (datetime.now() - timedelta(days=30*month)).strftime('%Y-%m')
                
                analytics_entry = {
                    'area': area,
                    'month': date,
                    'total_listings': random.randint(100, 800),
                    'active_listings': random.randint(50, 400),
                    'sold_listings': random.randint(10, 100),
                    'average_days_on_market': random.randint(15, 120),
                    'average_price_per_sqft': random.randint(800, 2500),
                    'price_trend': random.choice(['increasing', 'stable', 'decreasing']),
                    'demand_level': random.choice(['high', 'medium', 'low']),
                    'supply_level': random.choice(['high', 'medium', 'low']),
                    'investment_score': random.uniform(1.0, 10.0),
                    'rental_yield': random.uniform(3.0, 8.0),
                    'capital_appreciation': random.uniform(-5.0, 15.0),
                    'market_sentiment': random.choice(['positive', 'neutral', 'negative']),
                    'top_property_types': random.choice(['apartments', 'villas', 'mixed']),
                    'average_bedrooms': random.uniform(1.5, 4.5),
                    'luxury_market_share': random.uniform(10.0, 40.0)
                }
                analytics.append(analytics_entry)
        
        df = pd.DataFrame(analytics)
        df.to_csv(f"{self.output_dir}/property_analytics.csv", index=False)
        print(f"✅ Generated property analytics for {len(areas)} areas over 12 months")
        return df

    def generate_commission_data(self, num_commissions=10000):
        """Generate commission and financial data"""
        print(f"Generating {num_commissions} commission records...")
        
        commissions = []
        for i in range(num_commissions):
            transaction_amount = random.randint(500000, 15000000)
            commission_rate = random.uniform(2.0, 5.0)
            commission_amount = int(transaction_amount * commission_rate / 100)
            
            commission = {
                'commission_id': f"COM-{str(i+1).zfill(8)}",
                'transaction_id': f"TXN-{str(random.randint(1, 50000)).zfill(8)}",
                'agent_id': random.choice(['Ahmed Al Mansouri', 'Sarah Johnson', 'Mohammed Al Rashid', 'Emily Chen', 'Ali Hassan', 'Lisa Thompson']),
                'transaction_amount': transaction_amount,
                'commission_rate': commission_rate,
                'commission_amount': commission_amount,
                'commission_type': random.choice(['sale', 'rental', 'referral']),
                'payment_status': random.choice(['pending', 'paid', 'cancelled']),
                'payment_date': (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d'),
                'payment_method': random.choice(['bank_transfer', 'check', 'cash']),
                'split_percentage': random.uniform(60.0, 100.0),
                'company_share': 100.0 - random.uniform(60.0, 100.0),
                'notes': f"Commission for transaction {i+1}"
            }
            commissions.append(commission)
        
        df = pd.DataFrame(commissions)
        df.to_csv(f"{self.output_dir}/commissions.csv", index=False)
        print(f"✅ Generated {len(commissions)} commission records")
        return df

    def generate_market_reports(self):
        """Generate market research reports"""
        print("Creating market research reports...")
        
        reports = [
            {
                'title': 'Dubai Real Estate Market Q4 2024 Report',
                'content': """
                Dubai Real Estate Market Q4 2024 Analysis
                
                Executive Summary:
                The Dubai real estate market continues to show strong performance with sustained growth across all segments. 
                Luxury properties are leading the market with premium developments in Palm Jumeirah and Downtown Dubai.
                
                Key Findings:
                - Overall market growth: 8.5% year-over-year
                - Luxury segment growth: 12.3%
                - Average rental yields: 5.8%
                - Days on market: 45 days (down from 60 days)
                
                Market Drivers:
                - Strong foreign investment
                - Golden Visa program expansion
                - Infrastructure development
                - Economic diversification
                
                Outlook 2025:
                - Expected growth: 6-8%
                - New supply: 25,000 units
                - Price stability in mid-market
                - Continued luxury segment growth
                """
            },
            {
                'title': 'Investment Opportunities in Dubai Marina',
                'content': """
                Investment Analysis: Dubai Marina
                
                Market Overview:
                Dubai Marina remains the premier waterfront destination with consistent demand from both local and international investors.
                
                Investment Highlights:
                - Average rental yield: 6.2%
                - Capital appreciation: 9.1% annually
                - Occupancy rate: 94%
                - Average price per sqft: AED 1,850
                
                Best Investment Options:
                1. 2-bedroom apartments (highest rental demand)
                2. Studio units (lowest entry point)
                3. Penthouses (luxury segment growth)
                
                Risk Factors:
                - Market volatility
                - Regulatory changes
                - Economic fluctuations
                
                Recommendations:
                - Focus on quality developments
                - Consider long-term investment
                - Diversify across property types
                """
            },
            {
                'title': 'Luxury Real Estate Market Trends',
                'content': """
                Luxury Real Estate Market Analysis
                
                Market Performance:
                The luxury segment (properties >10M AED) has shown exceptional growth with increasing demand from high-net-worth individuals.
                
                Key Trends:
                - Ultra-luxury properties (>50M AED) growing 15%
                - International buyer demand up 25%
                - Customization requests increasing
                - Technology integration demand
                
                Popular Areas:
                1. Palm Jumeirah - Premium villas and penthouses
                2. Emirates Hills - Exclusive villa communities
                3. Downtown Dubai - Luxury apartments
                4. Dubai Marina - High-end waterfront properties
                
                Buyer Profiles:
                - 40% International investors
                - 35% Local high-net-worth individuals
                - 25% Corporate buyers
                
                Future Outlook:
                - Continued growth expected
                - New luxury developments planned
                - Increasing international interest
                """
            }
        ]
        
        for i, report in enumerate(reports):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=16)
            
            # Title
            pdf.cell(200, 10, txt=report['title'], ln=True, align='C')
            pdf.ln(10)
            
            # Content
            pdf.set_font("Arial", size=10)
            pdf.multi_cell(0, 5, txt=report['content'])
            
            filename = f"market_report_{i+1}.pdf"
            pdf.output(f"{self.output_dir}/{filename}")
        
        print(f"✅ Created {len(reports)} market research reports")

    def generate_legal_documents(self):
        """Generate legal and compliance documents"""
        print("Creating legal and compliance documents...")
        
        documents = [
            {
                'title': 'Dubai Real Estate Regulations Guide',
                'content': """
                Dubai Real Estate Regulations and Compliance Guide
                
                Regulatory Framework:
                - RERA (Real Estate Regulatory Agency) regulations
                - Dubai Land Department requirements
                - Anti-money laundering (AML) compliance
                - Know Your Customer (KYC) procedures
                
                Key Requirements:
                1. Agent Licensing: All agents must be RERA licensed
                2. Transaction Registration: All deals must be registered with DLD
                3. Commission Disclosure: Transparent commission structure required
                4. Client Documentation: Complete KYC documentation mandatory
                
                Compliance Procedures:
                - Client identity verification
                - Source of funds verification
                - Transaction monitoring
                - Suspicious activity reporting
                
                Penalties:
                - Unlicensed activity: AED 50,000 fine
                - Non-compliance: AED 25,000 fine
                - False information: AED 100,000 fine
                
                Best Practices:
                - Regular compliance training
                - Document retention (7 years)
                - Regular audits and reviews
                - Updated procedures and policies
                """
            },
            {
                'title': 'Property Transaction Legal Guide',
                'content': """
                Legal Guide for Property Transactions in Dubai
                
                Transaction Process:
                1. Offer and Acceptance
                2. Memorandum of Understanding (MOU)
                3. Due Diligence Period
                4. Contract Signing
                5. Transfer of Ownership
                
                Required Documents:
                - Valid passport/Emirates ID
                - Proof of funds
                - NOC from developer (if applicable)
                - Title deed or sales agreement
                - Utility clearance certificates
                
                Legal Considerations:
                - Property title verification
                - Outstanding payments check
                - Service charge verification
                - Building completion certificate
                
                Common Legal Issues:
                - Title deed disputes
                - Service charge arrears
                - Building defects
                - Developer delays
                
                Resolution Procedures:
                - RERA dispute resolution
                - Dubai Courts
                - Arbitration (if specified in contract)
                """
            }
        ]
        
        for i, doc in enumerate(documents):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=16)
            
            # Title
            pdf.cell(200, 10, txt=doc['title'], ln=True, align='C')
            pdf.ln(10)
            
            # Content
            pdf.set_font("Arial", size=10)
            pdf.multi_cell(0, 5, txt=doc['content'])
            
            filename = f"legal_guide_{i+1}.pdf"
            pdf.output(f"{self.output_dir}/{filename}")
        
        print(f"✅ Created {len(documents)} legal documents")

    def generate_training_materials(self):
        """Generate training and educational materials"""
        print("Creating training materials...")
        
        materials = [
            {
                'title': 'New Agent Onboarding Guide',
                'content': """
                New Agent Onboarding Program
                
                Week 1: Company Introduction
                - Company history and values
                - Organizational structure
                - Policies and procedures
                - Technology systems overview
                
                Week 2: Market Knowledge
                - Dubai real estate market overview
                - Area-specific information
                - Property types and characteristics
                - Market trends and analysis
                
                Week 3: Sales Skills
                - Lead generation techniques
                - Client communication skills
                - Property presentation methods
                - Negotiation strategies
                
                Week 4: Legal and Compliance
                - RERA regulations
                - Transaction procedures
                - Documentation requirements
                - Compliance best practices
                
                Week 5: Technology Training
                - CRM system usage
                - Property portals
                - Digital marketing tools
                - Virtual tour platforms
                
                Week 6: Practical Application
                - Shadow experienced agents
                - Handle real leads
                - Conduct property showings
                - Complete first transaction
                """
            },
            {
                'title': 'Advanced Sales Techniques',
                'content': """
                Advanced Sales Techniques for Real Estate Professionals
                
                Building Client Relationships:
                - Understanding client psychology
                - Building trust and rapport
                - Long-term relationship management
                - Referral generation strategies
                
                Advanced Negotiation:
                - Win-win negotiation techniques
                - Handling difficult clients
                - Price negotiation strategies
                - Closing techniques
                
                Market Positioning:
                - Competitive analysis
                - Unique value proposition
                - Brand building
                - Market differentiation
                
                Technology Integration:
                - Social media marketing
                - Digital lead generation
                - Virtual reality tours
                - AI-powered tools
                
                Performance Optimization:
                - Time management
                - Productivity tools
                - Goal setting and tracking
                - Continuous improvement
                """
            }
        ]
        
        for i, material in enumerate(materials):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=16)
            
            # Title
            pdf.cell(200, 10, txt=material['title'], ln=True, align='C')
            pdf.ln(10)
            
            # Content
            pdf.set_font("Arial", size=10)
            pdf.multi_cell(0, 5, txt=material['content'])
            
            filename = f"training_material_{i+1}.pdf"
            pdf.output(f"{self.output_dir}/{filename}")
        
        print(f"✅ Created {len(materials)} training materials")

    def generate_all_additional_data(self):
        """Generate all additional simulation data"""
        print("🚀 Starting additional data generation...")
        
        # Generate additional CSV files
        self.generate_lead_data(5000)
        self.generate_property_analytics()
        self.generate_commission_data(10000)
        
        # Generate additional PDF documents
        self.generate_market_reports()
        self.generate_legal_documents()
        self.generate_training_materials()
        
        print("\n🎉 Additional data generation completed!")
        print(f"📁 All data saved to: {self.output_dir}/")

if __name__ == "__main__":
    generator = AdditionalDataGenerator()
    generator.generate_all_additional_data()
