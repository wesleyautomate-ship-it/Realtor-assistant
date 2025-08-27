"""
Enhanced AI Manager for Better Response Quality
==============================================

This module provides improved AI responses with:
- No generic error prefixes
- Dubai-specific real estate knowledge
- Structured, actionable responses
- Better context understanding
"""

import json
import logging
import os
from typing import Dict, Any, Optional, List
from sqlalchemy import create_engine, text
from datetime import datetime
import google.generativeai as genai

logger = logging.getLogger(__name__)

class EnhancedAIEnhancementManager:
    """Enhanced AI manager with better response quality"""
    
    def __init__(self, db_url: str = None, model = None):
        self.db_url = db_url or os.getenv('DATABASE_URL', 'postgresql://admin:password123@localhost:5432/real_estate_db')
        if db_url:
            self.engine = create_engine(db_url)
        
        # Initialize Google Gemini model
        if not model:
            api_key = os.getenv('GOOGLE_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
            else:
                self.model = None
        else:
            self.model = model
        
        # Dubai real estate knowledge base
        self.dubai_knowledge = {
            "areas": {
                "dubai_marina": {
                    "price_range": "AED 1.2M - 8M",
                    "rental_yield": "6-8%",
                    "description": "Waterfront lifestyle with luxury apartments and marina views",
                    "popular_properties": ["Marina Gate", "Marina Heights", "Marina Promenade"]
                },
                "downtown_dubai": {
                    "price_range": "AED 1.5M - 15M",
                    "rental_yield": "5-7%",
                    "description": "Premium location with Burj Khalifa and Dubai Mall",
                    "popular_properties": ["Burj Vista", "The Address", "Opera Grand"]
                },
                "palm_jumeirah": {
                    "price_range": "AED 3M - 50M",
                    "rental_yield": "4-6%",
                    "description": "Luxury island living with beachfront properties",
                    "popular_properties": ["Palm Tower", "One Palm", "Palm Vista"]
                },
                "dubai_hills_estate": {
                    "price_range": "AED 800K - 5M",
                    "rental_yield": "6-8%",
                    "description": "Family-friendly community with golf course",
                    "popular_properties": ["Golf Place", "Park Views", "Hills Ridge"]
                },
                "arabian_ranches": {
                    "price_range": "AED 2M - 12M",
                    "rental_yield": "5-7%",
                    "description": "Premium villa community with equestrian facilities",
                    "popular_properties": ["Al Reem", "Al Mahra", "Al Ghadeer"]
                }
            },
            "developers": {
                "emaar": "Leading developer with premium properties",
                "damac": "Luxury developer with high-end projects",
                "nakheel": "Master developer of Palm Jumeirah and other iconic projects",
                "sobha": "Premium developer known for quality construction",
                "dubai_properties": "Government-backed developer with diverse portfolio"
            },
            "market_trends": {
                "appreciation": "15-20% annual growth in 2024",
                "rental_yields": "5-8% average across prime locations",
                "demand": "Strong demand for 1-2 bedroom apartments",
                "investment_benefits": "Golden Visa eligibility, 0% income tax, high rental yields"
            },
            "golden_visa": {
                "requirements": "AED 2M+ property investment",
                "benefits": "10-year residency, work permit, sponsor family",
                "process": "Property purchase → Application submission → Approval"
            }
        }
    
    def process_chat_request(self, 
                           message: str,
                           session_id: str = None,
                           role: str = "client",
                           file_upload: Optional[Dict] = None) -> Dict[str, Any]:
        """Process chat request with enhanced response quality"""
        
        try:
            # Analyze the query to understand intent
            query_analysis = self._analyze_query(message)
            
            # Generate enhanced response
            response = self._generate_enhanced_response(message, query_analysis)
            
            # Extract user preferences from the conversation
            user_preferences = self._extract_user_preferences(message, query_analysis)
            
            return {
                'response': response,
                'query_analysis': query_analysis,
                'user_preferences': user_preferences,
                'file_analysis': file_upload,
                'conversation_id': session_id
            }
            
        except Exception as e:
            logger.error(f"Error in enhanced AI manager: {e}")
            # Provide a helpful fallback response instead of generic error
            return {
                'response': self._generate_fallback_response(message),
                'query_analysis': {
                    'intent': 'general_inquiry',
                    'sentiment': 'neutral',
                    'urgency_level': 1,
                    'complexity_level': 1,
                    'suggested_actions': ['contact_agent', 'schedule_viewing'],
                    'entities': {}
                },
                'user_preferences': {},
                'file_analysis': file_upload,
                'conversation_id': session_id
            }
    
    def _analyze_query(self, message: str) -> Dict[str, Any]:
        """Analyze user query to understand intent and extract entities"""
        message_lower = message.lower()
        
        # Intent detection
        intent = "general_inquiry"
        if any(word in message_lower for word in ["find", "search", "looking for", "property", "apartment", "villa"]):
            intent = "property_search"
        elif any(word in message_lower for word in ["price", "cost", "value", "worth", "market"]):
            intent = "market_analysis"
        elif any(word in message_lower for word in ["golden visa", "visa", "residency"]):
            intent = "golden_visa"
        elif any(word in message_lower for word in ["rental", "rent", "yield", "roi"]):
            intent = "rental_analysis"
        elif any(word in message_lower for word in ["process", "procedure", "step", "how to"]):
            intent = "procedure_guidance"
        
        # Entity extraction
        entities = {}
        for area, data in self.dubai_knowledge["areas"].items():
            if area.replace("_", " ") in message_lower or area.replace("_", "") in message_lower:
                entities["area"] = area
                break
        
        # Sentiment analysis
        sentiment = "neutral"
        if any(word in message_lower for word in ["urgent", "quick", "asap", "immediately"]):
            sentiment = "urgent"
        elif any(word in message_lower for word in ["thank", "great", "excellent", "amazing"]):
            sentiment = "positive"
        
        return {
            'intent': intent,
            'sentiment': sentiment,
            'urgency_level': 3 if sentiment == "urgent" else 1,
            'complexity_level': 2 if intent in ["market_analysis", "golden_visa"] else 1,
            'suggested_actions': self._get_suggested_actions(intent),
            'entities': entities
        }
    
    def _generate_enhanced_response(self, message: str, query_analysis: Dict[str, Any]) -> str:
        """Generate high-quality, Dubai-specific response"""
        
        intent = query_analysis['intent']
        entities = query_analysis['entities']
        
        # Create context-aware prompt
        prompt = self._create_enhanced_prompt(message, intent, entities)
        
        try:
            if self.model:
                response = self.model.generate_content(prompt)
                response_text = response.text
                
                # Clean up response - remove any generic error prefixes
                if "I'm having trouble processing" in response_text:
                    response_text = self._clean_response(response_text)
                
                return response_text
            else:
                # Fallback to template-based response
                return self._generate_template_response(message, intent, entities)
                
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            return self._generate_template_response(message, intent, entities)
    
    def _create_enhanced_prompt(self, message: str, intent: str, entities: Dict[str, Any]) -> str:
        """Create enhanced prompt for better AI responses"""
        
        area_info = ""
        if "area" in entities:
            area_data = self.dubai_knowledge["areas"][entities["area"]]
            area_info = f"""
SPECIFIC AREA INFORMATION:
- Area: {entities['area'].replace('_', ' ').title()}
- Price Range: {area_data['price_range']}
- Rental Yield: {area_data['rental_yield']}
- Description: {area_data['description']}
- Popular Properties: {', '.join(area_data['popular_properties'])}
"""
        
        return f"""
You are an expert Dubai real estate AI assistant with deep knowledge of the local market.

USER QUERY: {message}
QUERY INTENT: {intent}

RESPONSE REQUIREMENTS:
1. **NO GENERIC ERROR MESSAGES** - Do not start with "I'm having trouble processing" or similar
2. **Provide specific Dubai real estate information** - Include actual prices, areas, developers
3. **Use structured formatting** - Headers, bullet points, bold keywords
4. **Include actionable insights** - Specific next steps and recommendations
5. **Be professional and expert-like** - Use real estate terminology
6. **Focus on the specific intent** - {intent}

DUBAI REAL ESTATE KNOWLEDGE:
{area_info}
- **Popular Areas**: Dubai Marina (AED 1.2M-8M), Downtown Dubai (AED 1.5M-15M), Palm Jumeirah (AED 3M-50M)
- **Developers**: Emaar, Damac, Nakheel, Sobha, Dubai Properties, Meraas, Azizi, Ellington
- **Market Trends**: 2024 shows 15-20% appreciation, rental yields 5-8%, strong demand for 1-2BR apartments
- **Investment Benefits**: Golden Visa eligibility, 0% income tax, high rental yields, strong capital appreciation

Provide a direct, helpful response without any error prefixes. Focus on being informative and actionable.
"""
    
    def _generate_template_response(self, message: str, intent: str, entities: Dict[str, Any]) -> str:
        """Generate template-based response when AI model is unavailable"""
        
        if intent == "property_search":
            return self._generate_property_search_response(message, entities)
        elif intent == "market_analysis":
            return self._generate_market_analysis_response(message, entities)
        elif intent == "golden_visa":
            return self._generate_golden_visa_response(message, entities)
        elif intent == "rental_analysis":
            return self._generate_rental_analysis_response(message, entities)
        elif intent == "procedure_guidance":
            return self._generate_procedure_response(message, entities)
        else:
            return self._generate_general_response(message, entities)
    
    def _generate_property_search_response(self, message: str, entities: Dict[str, Any]) -> str:
        """Generate property search response"""
        area = entities.get("area", "Dubai")
        area_data = self.dubai_knowledge["areas"].get(area, self.dubai_knowledge["areas"]["dubai_marina"])
        
        return f"""
🏢 **Property Search Results - {area.replace('_', ' ').title()}**

Based on your search criteria, here are the key details:

💡 **Market Overview:**
• **Price Range**: {area_data['price_range']}
• **Rental Yield**: {area_data['rental_yield']}
• **Description**: {area_data['description']}

🏗️ **Popular Properties:**
• {', '.join(area_data['popular_properties'])}

📊 **Investment Benefits:**
• Strong capital appreciation potential
• High rental demand
• Golden Visa eligibility for AED 2M+ investments
• 0% income tax on rental income

🎯 **Next Steps:**
1. Schedule a property viewing with our agents
2. Review financing options with local banks
3. Consider off-plan vs. ready properties
4. Evaluate rental vs. investment potential

Would you like specific property listings or information about other areas?
"""
    
    def _generate_market_analysis_response(self, message: str, entities: Dict[str, Any]) -> str:
        """Generate market analysis response"""
        return f"""
📊 **Dubai Real Estate Market Analysis**

Current market insights based on your query:

📈 **Market Performance:**
• **Annual Appreciation**: 15-20% in 2024
• **Rental Yields**: 5-8% across prime locations
• **Demand**: Strong for 1-2 bedroom apartments
• **Supply**: Balanced with new developments

🏗️ **Developer Activity:**
• Emaar: Premium developments in prime locations
• Damac: Luxury projects with high-end finishes
• Nakheel: Iconic projects like Palm Jumeirah
• Sobha: Quality construction and design

💰 **Investment Benefits:**
• Golden Visa eligibility (AED 2M+ investment)
• 0% income tax on rental income
• Freehold ownership for foreigners
• Strong capital appreciation potential

🎯 **Market Outlook:**
• Continued growth expected in 2025
• Strong demand from international investors
• Government support through various initiatives
• Infrastructure development driving value

Would you like specific analysis for any particular area or property type?
"""
    
    def _generate_golden_visa_response(self, message: str, entities: Dict[str, Any]) -> str:
        """Generate Golden Visa response"""
        return f"""
🏛️ **Golden Visa - Real Estate Investment**

Comprehensive guide for Golden Visa through property investment:

📋 **Requirements:**
• **Minimum Investment**: AED 2,000,000 in real estate
• **Property Type**: Freehold properties only
• **Location**: Any emirate in UAE
• **Ownership**: 100% ownership required

✅ **Benefits:**
• **10-year residency** renewable
• **Work permit** without sponsor
• **Sponsor family** members
• **Multiple entry** visa
• **Access to services** like banking, healthcare

🔄 **Application Process:**
1. Purchase qualifying property (AED 2M+)
2. Obtain property title deed
3. Submit application through ICP or GDRFA
4. Provide required documents
5. Await approval (typically 2-4 weeks)

📄 **Required Documents:**
• Valid passport
• Property title deed
• Bank statements
• Medical fitness certificate
• Security clearance

🎯 **Next Steps:**
1. Consult with our Golden Visa specialists
2. Review qualifying properties
3. Understand financing options
4. Begin application process

Would you like to explore qualifying properties or get detailed application guidance?
"""
    
    def _generate_rental_analysis_response(self, message: str, entities: Dict[str, Any]) -> str:
        """Generate rental analysis response"""
        return f"""
🏠 **Rental Market Analysis**

Comprehensive rental market insights:

📊 **Rental Yields by Area:**
• **Dubai Marina**: 6-8% (AED 80K-120K annually for 2BR)
• **Downtown Dubai**: 5-7% (AED 100K-150K annually for 2BR)
• **Palm Jumeirah**: 4-6% (AED 150K-300K annually for 2BR)
• **Dubai Hills Estate**: 6-8% (AED 60K-100K annually for 2BR)

💰 **Rental Benefits:**
• **Tax-free income**: 0% tax on rental income
• **High demand**: Strong tenant demand year-round
• **Stable returns**: Consistent rental yields
• **Capital appreciation**: Property value growth

📈 **Market Trends:**
• Rental rates increased 15-20% in 2024
• Strong demand from expatriates and tourists
• Short-term rental market booming
• Long-term stability in prime locations

🎯 **Investment Strategy:**
1. Focus on areas with 6%+ rental yields
2. Consider short-term vs. long-term rentals
3. Factor in service charges and maintenance
4. Evaluate tenant demand patterns

Would you like specific rental analysis for any area or property type?
"""
    
    def _generate_procedure_response(self, message: str, entities: Dict[str, Any]) -> str:
        """Generate procedure guidance response"""
        return f"""
📋 **Dubai Real Estate Procedures Guide**

Step-by-step process for real estate transactions:

🏠 **Property Purchase Process:**
1. **Property Selection**: Choose property and area
2. **Reservation**: Pay reservation fee (5-10% of price)
3. **Agreement**: Sign Memorandum of Understanding (MOU)
4. **Payment Plan**: Agree on payment schedule
5. **Title Deed**: Transfer ownership at DLD
6. **Registration**: Register with Dubai Land Department

💰 **Financing Process:**
1. **Pre-approval**: Get mortgage pre-approval
2. **Property Valuation**: Bank conducts valuation
3. **Loan Application**: Submit complete application
4. **Approval**: Receive loan approval
5. **Disbursement**: Bank transfers funds to seller

📄 **Required Documents:**
• Valid passport and visa
• Emirates ID
• Bank statements (3-6 months)
• Salary certificate
• Property documents

🎯 **Key Considerations:**
• Service charges and maintenance fees
• Property insurance requirements
• Utility connection procedures
• Community rules and regulations

Would you like detailed guidance on any specific step or document requirements?
"""
    
    def _generate_general_response(self, message: str, entities: Dict[str, Any]) -> str:
        """Generate general response"""
        return f"""
🏢 **Dubai Real Estate Expert Response**

Thank you for your inquiry about "{message}". Here's what you need to know:

💡 **Key Market Insights:**
• Dubai's real estate market is experiencing strong growth
• 15-20% annual appreciation in prime locations
• Rental yields average 5-8% across the city
• Golden Visa eligibility for AED 2M+ investments

📊 **Popular Investment Areas:**
• **Dubai Marina**: AED 1.2M-8M, waterfront lifestyle
• **Downtown Dubai**: AED 1.5M-15M, premium location
• **Palm Jumeirah**: AED 3M-50M, luxury segment
• **Dubai Hills Estate**: AED 800K-5M, family-friendly

🎯 **How We Can Help:**
1. Property search and selection
2. Market analysis and investment advice
3. Financing and mortgage guidance
4. Golden Visa application support
5. Property management services

Would you like to explore any specific area or get detailed information about a particular aspect?
"""
    
    def _generate_fallback_response(self, message: str) -> str:
        """Generate helpful fallback response"""
        return f"""
🏢 **Dubai Real Estate Assistance**

I understand you're asking about "{message}". Let me provide you with helpful information:

💡 **Quick Market Overview:**
• Dubai real estate offers excellent investment opportunities
• Strong market growth with 15-20% annual appreciation
• High rental yields of 5-8% in prime locations
• Golden Visa benefits for qualifying investments

🎯 **How to Proceed:**
1. **Property Search**: Browse available properties in your preferred area
2. **Market Analysis**: Get detailed market insights and trends
3. **Investment Guidance**: Understand financing and investment strategies
4. **Professional Support**: Connect with our expert agents

Would you like me to help you with any specific aspect of Dubai real estate?
"""
    
    def _clean_response(self, response_text: str) -> str:
        """Clean response by removing generic error prefixes"""
        error_prefixes = [
            "I'm having trouble processing your request right now",
            "I'm experiencing some technical difficulties",
            "I apologize, but I'm having issues",
            "Let me break it down for you: I'm having trouble"
        ]
        
        for prefix in error_prefixes:
            if prefix in response_text:
                parts = response_text.split(prefix)
                if len(parts) > 1:
                    cleaned = parts[1].strip()
                    if cleaned.startswith("."):
                        cleaned = cleaned[1:].strip()
                    if cleaned.startswith("Please try again"):
                        cleaned = self._generate_fallback_response("your inquiry")
                    return cleaned
        
        return response_text
    
    def _get_suggested_actions(self, intent: str) -> List[str]:
        """Get suggested actions based on intent"""
        actions_map = {
            "property_search": ["schedule_viewing", "get_property_list", "area_analysis"],
            "market_analysis": ["market_report", "investment_consultation", "trend_analysis"],
            "golden_visa": ["visa_consultation", "property_selection", "application_guidance"],
            "rental_analysis": ["rental_report", "yield_calculation", "investment_advice"],
            "procedure_guidance": ["process_consultation", "document_guidance", "legal_advice"]
        }
        return actions_map.get(intent, ["contact_agent", "schedule_consultation"])
    
    def _extract_user_preferences(self, message: str, query_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Extract user preferences from the message"""
        preferences = {}
        
        # Extract budget preferences
        if "budget" in message.lower() or "price" in message.lower():
            preferences["budget_conscious"] = True
        
        # Extract area preferences
        if "area" in query_analysis.get("entities", {}):
            preferences["preferred_area"] = query_analysis["entities"]["area"]
        
        # Extract property type preferences
        if "apartment" in message.lower():
            preferences["property_type"] = "apartment"
        elif "villa" in message.lower():
            preferences["property_type"] = "villa"
        
        return preferences
