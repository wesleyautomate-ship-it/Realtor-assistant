import json
import os
from pathlib import Path
import chromadb
from chromadb.config import Settings

def add_to_chromadb(collection_name, documents, metadatas=None):
    """Add documents to ChromaDB collection"""
    try:
        # Get or create collection
        collection = chroma_client.get_or_create_collection(collection_name)
        
        # Prepare documents for ChromaDB
        doc_texts = []
        doc_metadatas = []
        doc_ids = []
        
        for i, doc in enumerate(documents):
            if isinstance(doc, dict):
                # Convert dict to text
                doc_text = json.dumps(doc, indent=2)
                doc_metadatas.append({"source": f"{collection_name}_data", "type": "enhanced"})
            else:
                doc_text = str(doc)
                doc_metadatas.append({"source": f"{collection_name}_data", "type": "enhanced"})
            
            doc_texts.append(doc_text)
            doc_ids.append(f"{collection_name}_{i}")
        
        # Add to collection
        collection.add(
            documents=doc_texts,
            metadatas=doc_metadatas,
            ids=doc_ids
        )
        print(f"✅ Added {len(documents)} documents to {collection_name} collection")
        
    except Exception as e:
        print(f"❌ Error adding to {collection_name}: {e}")

def main():
    print("🚀 Adding Enhanced Data to ChromaDB...")
    
    # Add Downtown Dubai neighborhood data
    downtown_data = {
        "name": "Downtown Dubai",
        "description": "The heart of Dubai, featuring the iconic Burj Khalifa and Dubai Mall",
        "lifestyle": {
            "type": "Luxury Urban",
            "atmosphere": "High-end, cosmopolitan, vibrant",
            "best_for": ["Luxury living", "Shopping", "Entertainment", "Tourism", "Business"]
        },
        "amenities": {
            "shopping": ["The Dubai Mall (world's largest mall)", "Souk Al Bahar"],
            "dining": ["Over 200 restaurants", "Michelin-starred establishments"],
            "entertainment": ["Dubai Fountain", "Burj Khalifa observation deck", "Dubai Opera"]
        },
        "price_ranges": {
            "apartments": {
                "studio": "80,000 - 120,000 AED/year",
                "1_bedroom": "120,000 - 180,000 AED/year",
                "2_bedroom": "180,000 - 280,000 AED/year"
            }
        },
        "rental_yields": {
            "average_yield": "5.5% - 7%",
            "investment_potential": "Excellent"
        },
        "service_charges": {
            "average_per_sqft": "12 - 18 AED",
            "includes": ["Building maintenance", "Security", "Cleaning services"]
        },
        "market_trends": {
            "current_trend": "Stable with slight appreciation",
            "price_movement": "+2-4% annually"
        }
    }
    
    # Add February 2024 market update
    february_market_data = {
        "month": "February 2024",
        "summary": "Dubai real estate market shows continued strength with luxury segment leading growth",
        "key_highlights": [
            "Luxury property sales up 15% month-over-month",
            "Average transaction value reaches 2.8M AED",
            "Expat demand increases 25% from European markets"
        ],
        "market_performance": {
            "overall_growth": "+3.2%",
            "luxury_segment": "+4.8%",
            "mid_market": "+2.1%"
        },
        "area_performance": {
            "top_performers": [
                {"area": "Palm Jumeirah", "growth": "+6.2%"},
                {"area": "Downtown Dubai", "growth": "+5.1%"},
                {"area": "Dubai Marina", "growth": "+4.3%"}
            ]
        },
        "investment_insights": {
            "rental_yields": {
                "average_yield": "6.2%",
                "luxury_yield": "5.8%"
            },
            "capital_appreciation": {
                "annual_growth": "8.5%",
                "luxury_growth": "12.3%"
            }
        }
    }
    
    # Add closing strategies
    closing_strategies_data = {
        "title": "Advanced Closing Strategies for Real Estate Agents",
        "description": "Proven techniques to close deals effectively in Dubai's competitive market",
        "techniques": {
            "assumptive_close": {
                "description": "Act as if the deal is already done",
                "technique": "Use phrases like 'When you move in...' instead of 'If you decide to buy...'",
                "examples": [
                    "When you move in next month, you'll love the view from your balcony",
                    "Your new neighbors will be excited to meet you"
                ],
                "success_rate": "85%"
            },
            "urgency_close": {
                "description": "Create legitimate urgency without pressure",
                "technique": "Highlight genuine time-sensitive factors",
                "examples": [
                    "This property has 3 other viewings today",
                    "The seller is considering another offer"
                ],
                "success_rate": "78%"
            }
        },
        "dubai_specific_strategies": {
            "visa_benefits": [
                "Golden Visa eligibility for high-value properties",
                "Tax-free income and capital gains",
                "Access to world-class healthcare and education"
            ],
            "investment_angle": [
                "Strong rental yields (5-8% annually)",
                "Capital appreciation potential",
                "Currency stability (AED pegged to USD)"
            ]
        }
    }
    
    # Add problem-solving guide
    problem_solving_data = {
        "title": "Common Real Estate Issues and Solutions",
        "description": "Comprehensive guide to handling common challenges in Dubai real estate",
        "client_issues": {
            "financing_problems": {
                "issue": "Client can't get mortgage approval",
                "solutions": [
                    "Connect with multiple banks and lenders",
                    "Help improve credit score with financial advisor",
                    "Suggest alternative financing options (Islamic finance)"
                ]
            },
            "negotiation_stalemate": {
                "issue": "Buyer and seller can't agree on price",
                "solutions": [
                    "Provide recent comparable sales data",
                    "Suggest creative deal structures",
                    "Negotiate on closing costs or furniture"
                ]
            }
        },
        "market_challenges": {
            "low_inventory": {
                "issue": "Limited properties available in desired area",
                "solutions": [
                    "Expand search to nearby areas",
                    "Network with other agents for off-market properties",
                    "Consider off-plan developments"
                ]
            }
        }
    }
    
    # Add data to ChromaDB
    add_to_chromadb("neighborhoods", [downtown_data])
    add_to_chromadb("market_updates", [february_market_data])
    add_to_chromadb("agent_resources", [closing_strategies_data, problem_solving_data])
    
    print("✅ Enhanced data added to ChromaDB successfully!")

if __name__ == "__main__":
    # Initialize ChromaDB client
    chroma_client = chromadb.HttpClient(host="localhost", port=8000)
    main()
