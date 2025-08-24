#!/usr/bin/env python3
"""
Dubai Real Estate Research Data Ingestion Script
This script creates the enhanced ChromaDB collections and ingests Dubai research data
"""

import os
import sys
import json
import uuid
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import chromadb
from pathlib import Path
import logging
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DubaiResearchIngester:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/real_estate_db")
        self.engine = create_engine(self.db_url)
        self.chroma_client = chromadb.HttpClient(host="localhost", port=8000)
        
        # Dubai real estate collections configuration
        self.dubai_collections = {
            "market_analysis": {
                "description": "Market trends, price dynamics, transaction volumes 2005-2025",
                "content_types": ["price_analysis", "transaction_data", "market_cycles", "growth_trajectories"],
                "key_topics": ["Price dynamics", "Transaction volumes", "Market cycles", "Recovery patterns"]
            },
            "regulatory_framework": {
                "description": "Laws, regulations, compliance requirements 2002-2025",
                "content_types": ["legislation", "regulatory_updates", "compliance_guidelines", "legal_framework"],
                "key_topics": ["Law No. 3 of 2002", "RERA", "Escrow Law", "Golden Visa", "Mortgage regulations"]
            },
            "neighborhood_profiles": {
                "description": "Area-specific information, amenities, demographics",
                "content_types": ["area_guides", "neighborhood_data", "community_info", "location_analysis"],
                "key_topics": ["Dubai Marina", "Downtown Dubai", "Palm Jumeirah", "Business Bay", "Dubai South"]
            },
            "investment_insights": {
                "description": "Investment strategies, ROI analysis, market opportunities",
                "content_types": ["investment_guides", "roi_analysis", "market_opportunities", "investor_behavior"],
                "key_topics": ["Golden Visa benefits", "Foreign investment", "ROI projections", "Investment hotspots"]
            },
            "developer_profiles": {
                "description": "Major developers, their projects, track records",
                "content_types": ["company_profiles", "project_portfolios", "developer_ratings", "market_share"],
                "key_topics": ["Emaar Properties", "DAMAC", "Nakheel", "Government developers", "Private developers"]
            },
            "transaction_guidance": {
                "description": "Buying/selling processes, legal requirements, best practices",
                "content_types": ["transaction_guides", "legal_requirements", "process_steps", "documentation"],
                "key_topics": ["Property purchase process", "Legal requirements", "Documentation", "Financing"]
            },
            "market_forecasts": {
                "description": "Future predictions, growth trajectories, emerging trends",
                "content_types": ["forecasts", "trend_analysis", "future_outlook", "predictions"],
                "key_topics": ["2025 market predictions", "Dubai 2040 plan", "Growth trajectories", "Emerging trends"]
            },
            "agent_resources": {
                "description": "Sales techniques, client management, professional development",
                "content_types": ["sales_techniques", "client_management", "professional_skills", "negotiation"],
                "key_topics": ["Closing strategies", "Client objections", "Negotiation techniques", "Deal structuring"]
            },
            "urban_planning": {
                "description": "Dubai 2040 plan, infrastructure, master planning",
                "content_types": ["master_plans", "infrastructure", "urban_development", "sustainability"],
                "key_topics": ["Dubai 2040", "Infrastructure projects", "Sustainability goals", "Urban centers"]
            },
            "financial_insights": {
                "description": "Financing options, mortgage trends, investment vehicles",
                "content_types": ["financing_guides", "mortgage_trends", "investment_vehicles", "financial_analysis"],
                "key_topics": ["Mortgage rates", "LTV ratios", "Financing options", "Investment vehicles"]
            }
        }

    def create_collections(self):
        """Create or verify all Dubai research ChromaDB collections"""
        logger.info("Creating Dubai research ChromaDB collections...")
        
        for collection_name, config in self.dubai_collections.items():
            try:
                # Try to get existing collection or create new one
                collection = self.chroma_client.get_or_create_collection(
                    name=collection_name,
                    metadata={
                        "description": config["description"],
                        "content_types": ", ".join(config["content_types"]),
                        "key_topics": ", ".join(config["key_topics"]),
                        "created_at": datetime.now().isoformat()
                    }
                )
                logger.info(f"✅ Collection '{collection_name}' ready - {config['description']}")
                
            except Exception as e:
                logger.error(f"❌ Error creating collection '{collection_name}': {e}")
                continue
        
        logger.info("Dubai research collections setup complete!")

    def ingest_sample_data(self):
        """Ingest sample Dubai research data into collections"""
        logger.info("Ingesting sample Dubai research data...")
        
        # Sample data for each collection
        sample_data = self._get_sample_data()
        
        for collection_name, documents in sample_data.items():
            try:
                collection = self.chroma_client.get_collection(collection_name)
                
                # Prepare data for ChromaDB
                ids = []
                contents = []
                metadatas = []
                
                for i, doc in enumerate(documents):
                    ids.append(f"{collection_name}_{i}_{uuid.uuid4().hex[:8]}")
                    contents.append(doc["content"])
                    metadatas.append(doc["metadata"])
                
                # Add documents to collection
                if contents:
                    collection.add(
                        documents=contents,
                        metadatas=metadatas,
                        ids=ids
                    )
                    logger.info(f"✅ Ingested {len(contents)} documents into '{collection_name}'")
                
            except Exception as e:
                logger.error(f"❌ Error ingesting data into '{collection_name}': {e}")
                continue
        
        logger.info("Sample data ingestion complete!")

    def _get_sample_data(self) -> Dict[str, List[Dict]]:
        """Get sample Dubai research data for each collection"""
        return {
            "market_analysis": [
                {
                    "content": "Dubai's real estate market experienced explosive growth from 2002-2008 with property prices nearly quadrupling. The market peaked in 2014 with average price per square foot reaching AED 1,003. Post-2014 saw a correction period with double-digit price drops through 2019, hitting a low in 2020 at AED 794/sqft. The market rebounded dramatically in 2021, reaching AED 1,524/sqft in 2024 and AED 1,607/sqft in Q2 2025.",
                    "metadata": {
                        "source": "dubai_market_research",
                        "content_type": "price_analysis",
                        "time_period": "2002-2025",
                        "key_metrics": "price_dynamics, market_cycles, recovery_patterns",
                        "relevance_score": 0.95
                    }
                },
                {
                    "content": "Transaction volumes surged from 132,628 in 2023 to 169,000 in 2024, valued at AED 488 billion. Q1 2025 saw 53,118 transactions worth AED 184 billion, representing 48.8% year-on-year increase. Off-plan sales dominate with 66% of transaction volume and value in Q2 2025, driven by flexible payment plans.",
                    "metadata": {
                        "source": "dubai_market_research",
                        "content_type": "transaction_data",
                        "time_period": "2023-2025",
                        "key_metrics": "transaction_volumes, off_plan_sales, payment_trends",
                        "relevance_score": 0.90
                    }
                }
            ],
            "regulatory_framework": [
                {
                    "content": "Law No. 3 of 2002 granted foreign nationals property ownership rights in designated freehold areas. Law No. 7 of 2006 expanded this to 100% foreign ownership in specific zones. RERA was established in 2007 to oversee developer compliance and protect off-plan purchasers. The Escrow Law of 2008 mandated secure escrow accounts for off-plan project funds.",
                    "metadata": {
                        "source": "dubai_regulatory_research",
                        "content_type": "legislation",
                        "time_period": "2002-2008",
                        "key_areas": "foreign_ownership, developer_regulation, consumer_protection",
                        "relevance_score": 0.92
                    }
                },
                {
                    "content": "Central Bank Circular No. 31/2013 set LTV limits for mortgages, initially capping non-UAE nationals at 75% for properties up to AED 5 million and 65% above that threshold. Rent regulation through Decree No. 43 of 2013 introduced rent calculator to cap annual increases.",
                    "metadata": {
                        "source": "dubai_regulatory_research",
                        "content_type": "financial_regulation",
                        "time_period": "2013",
                        "key_areas": "mortgage_regulation, rent_control, affordability",
                        "relevance_score": 0.88
                    }
                }
            ],
            "investment_insights": [
                {
                    "content": "The Golden Visa program, introduced in 2019, offers residency visas of 5, 10, or 25 years for significant property investments. A property investment of AED 2 million grants a 10-year visa, while AED 1 million qualifies for a 2-year visa. This program has boosted transaction volumes and encouraged long-term ownership over speculation.",
                    "metadata": {
                        "source": "dubai_investment_research",
                        "content_type": "visa_programs",
                        "time_period": "2019-present",
                        "key_benefits": "long_term_residency, tax_advantages, investment_incentives",
                        "relevance_score": 0.94
                    }
                },
                {
                    "content": "Foreign nationals account for over 40% of Dubai's real estate ownership, with Indians (22-28%), British (12-17%), Chinese (8-14%), Russians (9%), and Saudis (11%) as top investors. Each nationality brings distinct motivations: Indians favor Dubai Marina for rental income, British seek luxury properties in Palm Jumeirah, Chinese diversify from domestic market.",
                    "metadata": {
                        "source": "dubai_investment_research",
                        "content_type": "investor_demographics",
                        "time_period": "2025",
                        "key_insights": "foreign_ownership, nationality_preferences, investment_motivations",
                        "relevance_score": 0.89
                    }
                }
            ],
            "neighborhood_profiles": [
                {
                    "content": "Dubai Marina is a master-planned waterfront community featuring luxury high-rise apartments and penthouses. Average property prices range from AED 1,800-2,500/sqft with rental yields of 6-8%. Amenities include yacht clubs, beach access, Marina Walk promenade, JBR Beach proximity, and excellent connectivity to Dubai Metro.",
                    "metadata": {
                        "source": "dubai_neighborhood_research",
                        "content_type": "area_profile",
                        "location": "Dubai Marina",
                        "key_features": "waterfront, luxury, high_yield, metro_connected",
                        "relevance_score": 0.93
                    }
                },
                {
                    "content": "Downtown Dubai houses the iconic Burj Khalifa and Dubai Mall. Properties command premium prices of AED 2,000-4,000/sqft with lower rental yields of 4-6% due to high capital values. The area offers world-class dining, shopping, and entertainment with excellent transport links including Dubai Metro.",
                    "metadata": {
                        "source": "dubai_neighborhood_research",
                        "content_type": "area_profile",
                        "location": "Downtown Dubai",
                        "key_features": "iconic, premium, entertainment, transport_hub",
                        "relevance_score": 0.91
                    }
                }
            ],
            "developer_profiles": [
                {
                    "content": "Emaar Properties is Dubai's largest developer, responsible for iconic projects like Burj Khalifa, Dubai Mall, and Dubai Marina. With a market share of ~25%, Emaar focuses on master-planned communities and luxury developments. Recent projects include Dubai Hills Estate and Creek Harbour with strong delivery track record.",
                    "metadata": {
                        "source": "dubai_developer_research",
                        "content_type": "company_profile",
                        "developer": "Emaar Properties",
                        "key_strengths": "market_leader, iconic_projects, reliable_delivery",
                        "relevance_score": 0.96
                    }
                },
                {
                    "content": "DAMAC Properties specializes in luxury and branded residences, including partnerships with Versace, Fendi, and Trump brands. Known for premium finishes and unique designs, DAMAC has delivered over 44,000 units since 2002 with focus on high-end market segments.",
                    "metadata": {
                        "source": "dubai_developer_research",
                        "content_type": "company_profile",
                        "developer": "DAMAC Properties",
                        "key_strengths": "luxury_focus, branded_residences, premium_finishes",
                        "relevance_score": 0.87
                    }
                }
            ]
        }

    def test_collections(self):
        """Test that all collections are accessible and contain data"""
        logger.info("Testing Dubai research collections...")
        
        for collection_name in self.dubai_collections.keys():
            try:
                collection = self.chroma_client.get_collection(collection_name)
                
                # Test query functionality
                test_results = collection.query(
                    query_texts=["Dubai property market"],
                    n_results=1
                )
                
                if test_results['documents'] and test_results['documents'][0]:
                    logger.info(f"✅ Collection '{collection_name}' is working correctly")
                else:
                    logger.warning(f"⚠️ Collection '{collection_name}' is empty or not responding")
                    
            except Exception as e:
                logger.error(f"❌ Error testing collection '{collection_name}': {e}")
        
        logger.info("Collection testing complete!")

    def run_full_setup(self):
        """Run the complete Dubai research collections setup"""
        logger.info("🚀 Starting Dubai Real Estate Research Collections Setup...")
        
        # Step 1: Create collections
        self.create_collections()
        
        # Step 2: Ingest sample data
        self.ingest_sample_data()
        
        # Step 3: Test collections
        self.test_collections()
        
        logger.info("🎉 Dubai research collections setup completed successfully!")
        logger.info("\n📊 Collections Summary:")
        for name, config in self.dubai_collections.items():
            logger.info(f"   - {name}: {config['description']}")

if __name__ == "__main__":
    ingester = DubaiResearchIngester()
    ingester.run_full_setup()
