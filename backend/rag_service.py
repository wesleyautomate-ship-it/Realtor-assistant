#!/usr/bin/env python3
"""
Improved RAG Service for Dubai Real Estate
Addresses core issues: conversational tone, data presentation, information architecture, and generic content
"""

import os
import re
from typing import List, Dict, Any, Optional, Tuple
import chromadb
from sqlalchemy import create_engine, text
import logging
from dataclasses import dataclass
from enum import Enum

# Import Reelly service
try:
    from reelly_service import ReellyService
    RELLY_AVAILABLE = True
except ImportError:
    ReellyService = None
    RELLY_AVAILABLE = False

logger = logging.getLogger(__name__)

class QueryIntent(Enum):
    PROPERTY_SEARCH = "property_search"
    MARKET_INFO = "market_info"
    POLICY_QUESTION = "policy_question"
    AGENT_SUPPORT = "agent_support"
    INVESTMENT_QUESTION = "investment_question"
    REGULATORY_QUESTION = "regulatory_question"
    NEIGHBORHOOD_QUESTION = "neighborhood_question"
    DEVELOPER_QUESTION = "developer_question"
    # New Action Intents for Phase 3
    UPDATE_LEAD = "update_lead"
    LOG_INTERACTION = "log_interaction"
    SCHEDULE_FOLLOW_UP = "schedule_follow_up"
    GENERAL = "general"

@dataclass
class QueryAnalysis:
    intent: QueryIntent
    entities: Dict[str, Any]
    parameters: Dict[str, Any]
    confidence: float

@dataclass
class ContextItem:
    content: str
    source: str
    relevance_score: float
    metadata: Dict[str, Any]

class ImprovedRAGService:
    def __init__(self, db_url: str, chroma_host: str = "localhost", chroma_port: int = 8002):
        self.engine = create_engine(db_url)
        self.chroma_client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
        
        # Initialize Reelly service for hybrid search
        if RELLY_AVAILABLE:
            try:
                self.reelly_service = ReellyService()
                logger.info("✅ Reelly service integrated for hybrid search")
            except Exception as e:
                logger.error(f"Failed to initialize Reelly service: {e}")
                self.reelly_service = None
        else:
            self.reelly_service = None
        
        # Enhanced intent classification patterns
        self.intent_patterns = {
            QueryIntent.PROPERTY_SEARCH: [
                r'\b(buy|rent|purchase|find|search|looking for|need)\b.*\b(property|house|apartment|condo|villa|home)\b',
                r'\b(bedroom|bathroom|price|budget|location|area)\b',
                r'\b(show me|display|list)\b.*\b(properties|houses|apartments)\b',
                r'\b(dubai marina|downtown|palm jumeirah|business bay|jbr|jumeirah|dubai hills|arabian ranches)\b.*\b(property|apartment|villa)\b'
            ],
            QueryIntent.MARKET_INFO: [
                r'\b(market|trend|price|investment|rental|yield|forecast|growth|appreciation)\b',
                r'\b(how much|what is the price|market value|property prices)\b',
                r'\b(area|neighborhood|community)\b.*\b(market|trends|prices)\b',
                r'\b(dubai real estate|property market|real estate trends)\b'
            ],
            QueryIntent.INVESTMENT_QUESTION: [
                r'\b(investment|roi|return|profit|yield|capital appreciation)\b',
                r'\b(golden visa|residency|visa)\b.*\b(property|investment)\b',
                r'\b(foreign|international|expat)\b.*\b(invest|buy|purchase)\b',
                r'\b(rental yield|investment return|property investment)\b'
            ],
            QueryIntent.REGULATORY_QUESTION: [
                r'\b(law|regulation|rera|escrow|legal|compliance)\b',
                r'\b(golden visa|visa requirements|residency visa)\b',
                r'\b(freehold|leasehold|ownership rights)\b',
                r'\b(dubai land department|dld|mortgage regulations)\b'
            ],
            QueryIntent.NEIGHBORHOOD_QUESTION: [
                r'\b(dubai marina|downtown|palm jumeirah|business bay|jbr|jumeirah|dubai hills|arabian ranches|emirates hills)\b.*\b(area|neighborhood|community|amenities)\b',
                r'\b(tell me about|describe|what is)\b.*\b(dubai marina|downtown|palm jumeirah|business bay)\b',
                r'\b(schools|hospitals|transport|metro|amenities)\b.*\b(area|neighborhood)\b'
            ],
            QueryIntent.DEVELOPER_QUESTION: [
                r'\b(emaar|damac|nakheel|sobha|dubai properties|meraas)\b',
                r'\b(developer|builder|construction company)\b',
                r'\b(who built|who developed|which developer)\b'
            ],
            QueryIntent.POLICY_QUESTION: [
                r'\b(policy|procedure|how to|what is|process|requirement)\b',
                r'\b(commission|fee|cost|charge|payment)\b',
                r'\b(contract|agreement|terms|conditions)\b'
            ],
            QueryIntent.AGENT_SUPPORT: [
                r'\b(deal|close|negotiate|client|commission|strategy)\b',
                r'\b(sales|objection|technique|approach|method)\b',
                r'\b(how to handle|deal with|manage)\b.*\b(client|situation)\b'
            ],
            # New Action Intents for Phase 3
            QueryIntent.UPDATE_LEAD: [
                r'\b(update|change|set)\b.*\b(lead|client|status)\b',
                r'\b(status to)\b',
                r'\b(mark|move)\b.*\b(lead|client)\b.*\b(to|as)\b'
            ],
            QueryIntent.LOG_INTERACTION: [
                r'\b(log|note|add a note|just finished|feedback)\b',
                r'\b(viewing with|call with|meeting with)\b',
                r'\b(record|document)\b.*\b(interaction|conversation)\b'
            ],
            QueryIntent.SCHEDULE_FOLLOW_UP: [
                r'\b(schedule|remind me|set a reminder|follow up)\b',
                r'\b(call|meeting|email)\b.*\b(tomorrow|monday|next week|at \d+[ap]m)\b',
                r'\b(book|arrange)\b.*\b(appointment|meeting)\b'
            ]
        }
        
        # Entity extraction patterns
        self.entity_patterns = {
            'budget': [
                r'\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:k|thousand|million|m)?',
                r'(\d+)\s*(?:k|thousand|million|m)\s*(?:dollars?|aed)?',
                r'budget.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
                r'price.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
            ],
            'location': [
                r'\b(dubai marina|downtown|palm jumeirah|business bay|jbr|jumeirah)\b',
                r'\b(area|neighborhood|location)\b.*?\b(\w+(?:\s+\w+)*)\b',
                r'in\s+(\w+(?:\s+\w+)*)',
                r'(\w+(?:\s+\w+)*)\s+area'
            ],
            'property_type': [
                r'\b(apartment|condo|villa|house|townhouse|penthouse|studio)\b',
                r'\b(residential|commercial|office|retail)\b'
            ],
            'bedrooms': [
                r'(\d+)\s*bedroom',
                r'(\d+)\s*br',
                r'(\d+)\s*bed'
            ],
            'bathrooms': [
                r'(\d+(?:\.\d+)?)\s*bathroom',
                r'(\d+(?:\.\d+)?)\s*bath'
            ],
            # Enhanced Entity Extraction patterns for Phase 3
            'lead_name': [
                r'\b(with|for|client|lead)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',
                r'\b(update|change)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b.*\b(status|lead)\b'
            ],
            'new_status': [
                r'\b(status to)\s+[\'"]?(\w+)[\'"]?\b',
                r'\b(mark|move)\b.*\b(to|as)\s+[\'"]?(\w+)[\'"]?\b',
                r'\b(set|change)\b.*\b(status)\b.*\b(to)\s+[\'"]?(\w+)[\'"]?\b'
            ],
            'task_datetime': [
                r'\b(tomorrow|today|monday|tuesday|wednesday|thursday|friday|saturday|sunday|next week)\b(?:\s+at\s+(\d{1,2}(?::\d{2})?\s*[ap]m))?',
                r'\b(at)\s+(\d{1,2}(?::\d{2})?\s*[ap]m)\b',
                r'\b(on)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b'
            ],
            'interaction_notes': [
                r'\b(note is|feedback was|said that|felt that)\s+(.+)',
                r'\b(call|meeting|viewing)\b.*\b(went|was)\s+(.+)',
                r'\b(client|lead)\b.*\b(mentioned|said|expressed)\s+(.+)'
            ]
        }

    def analyze_query(self, query: str) -> QueryAnalysis:
        """Analyze user query to extract intent, entities, and parameters"""
        query_lower = query.lower()
        
        # Determine intent
        intent_scores = {}
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, query_lower, re.IGNORECASE):
                    score += 1
            intent_scores[intent] = score
        
        # Get the intent with highest score
        if intent_scores:
            intent = max(intent_scores, key=intent_scores.get)
            confidence = intent_scores[intent] / max(len(patterns) for patterns in self.intent_patterns.values())
        else:
            intent = QueryIntent.GENERAL
            confidence = 0.0
        
        # Extract entities
        entities = {}
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, query_lower, re.IGNORECASE)
                if matches:
                    entities[entity_type] = matches[0] if isinstance(matches[0], str) else matches[0][0]
                    break
        
        # Extract parameters
        parameters = self._extract_parameters(query_lower, entities)
        
        return QueryAnalysis(
            intent=intent,
            entities=entities,
            parameters=parameters,
            confidence=confidence
        )

    def _extract_parameters(self, query: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Extract search parameters from entities"""
        parameters = {}
        
        # Budget parameters
        if 'budget' in entities:
            budget_str = entities['budget']
            try:
                # Handle different budget formats
                if 'k' in budget_str or 'thousand' in budget_str:
                    budget = float(budget_str.replace('k', '').replace('thousand', '')) * 1000
                elif 'm' in budget_str or 'million' in budget_str:
                    budget = float(budget_str.replace('m', '').replace('million', '')) * 1000000
                else:
                    budget = float(budget_str.replace(',', ''))
                
                # Set budget range (±20%)
                parameters['budget_min'] = budget * 0.8
                parameters['budget_max'] = budget * 1.2
            except:
                pass
        
        # Location parameter
        if 'location' in entities:
            parameters['location'] = entities['location']
        
        # Property type
        if 'property_type' in entities:
            parameters['property_type'] = entities['property_type']
        
        # Bedrooms
        if 'bedrooms' in entities:
            try:
                parameters['bedrooms'] = int(entities['bedrooms'])
            except:
                pass
        
        # Bathrooms
        if 'bathrooms' in entities:
            try:
                parameters['bathrooms'] = float(entities['bathrooms'])
            except:
                pass
        
        return parameters

    def get_relevant_context(self, query: str, analysis: QueryAnalysis, max_items: int = 5) -> List[ContextItem]:
        """Get relevant context from multiple sources based on query analysis"""
        context_items = []
        
        # 1. Get relevant documents from ChromaDB
        doc_context = self._get_document_context(query, analysis.intent, max_items)
        context_items.extend(doc_context)
        
        # 2. Get relevant properties from internal database
        if analysis.intent == QueryIntent.PROPERTY_SEARCH:
            prop_context = self._get_property_context(analysis.parameters, max_items * 2)
            context_items.extend(prop_context)
        else:
            prop_context = self._get_property_context(analysis.parameters, max_items)
            context_items.extend(prop_context)
        
        # 3. Get LIVE context from Reelly API for property searches
        if analysis.intent == QueryIntent.PROPERTY_SEARCH and self.reelly_service and self.reelly_service.is_enabled():
            reelly_context = self._get_reelly_property_context(analysis.parameters, max_items)
            context_items.extend(reelly_context)
        
        # 4. Get relevant neighborhoods and market data
        if analysis.intent in [QueryIntent.NEIGHBORHOOD_QUESTION, QueryIntent.MARKET_INFO]:
            neighborhood_context = self._get_neighborhood_context(query, max_items)
            context_items.extend(neighborhood_context)
            
            market_context = self._get_market_context(query, max_items)
            context_items.extend(market_context)
        
        # 5. Sort all combined context items by relevance and return the best ones
        context_items.sort(key=lambda x: x.relevance_score, reverse=True)
        return context_items[:max_items]

    def _get_document_context(self, query: str, intent: QueryIntent, max_items: int) -> List[ContextItem]:
        """Get relevant documents from ChromaDB collections"""
        context_items = []
        
        # Enhanced collection mapping to use ALL specialized collections
        collection_mapping = {
            QueryIntent.PROPERTY_SEARCH: ["real_estate_docs", "market_analysis", "neighborhood_profiles", "developer_profiles"],
            QueryIntent.MARKET_INFO: ["market_analysis", "market_forecasts", "financial_insights", "investment_insights"],
            QueryIntent.INVESTMENT_QUESTION: ["investment_insights", "market_analysis", "financial_insights", "market_forecasts"],
            QueryIntent.REGULATORY_QUESTION: ["regulatory_framework", "transaction_guidance", "real_estate_docs"],
            QueryIntent.NEIGHBORHOOD_QUESTION: ["neighborhood_profiles", "urban_planning", "market_analysis"],
            QueryIntent.DEVELOPER_QUESTION: ["developer_profiles", "market_analysis", "investment_insights"],
            QueryIntent.POLICY_QUESTION: ["regulatory_framework", "agent_resources", "transaction_guidance"],
            QueryIntent.AGENT_SUPPORT: ["agent_resources", "transaction_guidance", "market_analysis"],
            QueryIntent.GENERAL: ["real_estate_docs", "comprehensive_data", "market_analysis"]
        }
        
        collections = collection_mapping.get(intent, ["comprehensive_data"])
        
        for collection_name in collections:
            try:
                collection = self.chroma_client.get_collection(collection_name)
                results = collection.query(
                    query_texts=[query],
                    n_results=max_items * 2  # Get more results to filter better
                )
                
                if results['documents'] and results['documents'][0]:
                    for i, doc in enumerate(results['documents'][0]):
                        score = 1.0 - (results['distances'][0][i] if results['distances'] and results['distances'][0] else 0.5)
                        metadata = results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {}
                        
                        # Boost score for specific data types
                        if metadata.get('type') in ['properties', 'neighborhoods', 'market_data']:
                            score += 0.2
                        
                        context_items.append(ContextItem(
                            content=doc,
                            source=f"chroma_{collection_name}",
                            relevance_score=score,
                            metadata=metadata
                        ))
            except Exception as e:
                logger.warning(f"Error querying collection {collection_name}: {e}")
                continue
        
        return context_items

    def _get_property_context(self, parameters: Dict[str, Any], max_items: int) -> List[ContextItem]:
        """Get relevant properties from database based on parameters"""
        context_items = []
        
        # Build SQL query based on parameters - use correct properties table
        sql_parts = ["SELECT * FROM properties WHERE 1=1"]
        sql_parts.append("AND listing_status = 'live'")  # This ensures only public listings are shown
        query_params = {}
        
        # Always get some properties even without specific parameters
        if not parameters:
            sql_parts.append("AND price > 0")
        
        if 'budget_min' in parameters and 'budget_max' in parameters:
            sql_parts.append("AND price BETWEEN :budget_min AND :budget_max")
            query_params['budget_min'] = parameters['budget_min']
            query_params['budget_max'] = parameters['budget_max']
        elif 'budget_max' in parameters:
            sql_parts.append("AND price <= :budget_max")
            query_params['budget_max'] = parameters['budget_max']
        
        if 'location' in parameters:
            sql_parts.append("AND location ILIKE :location")
            query_params['location'] = f"%{parameters['location']}%"
        
        if 'property_type' in parameters:
            sql_parts.append("AND property_type ILIKE :property_type")
            query_params['property_type'] = f"%{parameters['property_type']}%"
        
        if 'bedrooms' in parameters:
            sql_parts.append("AND bedrooms >= :bedrooms")
            query_params['bedrooms'] = parameters['bedrooms']
        
        if 'bathrooms' in parameters:
            sql_parts.append("AND bathrooms >= :bathrooms")
            query_params['bathrooms'] = parameters['bathrooms']
        
        sql_parts.append("ORDER BY price ASC LIMIT :limit")
        query_params['limit'] = max_items * 2  # Get more to filter better
        
        sql = " ".join(sql_parts)
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(sql), query_params)
                for row in result:
                    property_info = f"Address: {row.address}, Price: ${row.price:,.0f}, Bedrooms: {row.bedrooms}, Bathrooms: {row.bathrooms}, Type: {row.property_type}"
                    if row.description:
                        property_info += f", Description: {row.description}"
                    
                    # Calculate relevance score based on parameter match
                    relevance_score = self._calculate_property_relevance(row, parameters)
                    
                    context_items.append(ContextItem(
                        content=property_info,
                        source="database_properties",
                        relevance_score=relevance_score,
                        metadata={
                            'address': row.address,
                            'price': float(row.price) if row.price else 0,
                            'bedrooms': row.bedrooms,
                            'bathrooms': float(row.bathrooms) if row.bathrooms else 0,
                            'property_type': row.property_type
                        }
                    ))
        except Exception as e:
            logger.error(f"Error querying properties: {e}")
        
        return context_items

    def _calculate_property_relevance(self, property_row, parameters: Dict[str, Any]) -> float:
        """Calculate relevance score for a property based on parameters"""
        score = 0.5  # Base score
        
        # Budget relevance
        if 'budget_min' in parameters and 'budget_max' in parameters and property_row.price:
            price = float(property_row.price)
            if parameters['budget_min'] <= price <= parameters['budget_max']:
                score += 0.3
            elif price <= parameters['budget_max'] * 1.5:  # Within 50% of max budget
                score += 0.1
        
        # Location relevance
        if 'location' in parameters and property_row.address:
            if parameters['location'].lower() in property_row.address.lower():
                score += 0.2
        
        # Property type relevance
        if 'property_type' in parameters and property_row.property_type:
            if parameters['property_type'].lower() in property_row.property_type.lower():
                score += 0.2
        
        # Bedrooms relevance
        if 'bedrooms' in parameters and property_row.bedrooms:
            if property_row.bedrooms >= parameters['bedrooms']:
                score += 0.1
        
        # Bathrooms relevance
        if 'bathrooms' in parameters and property_row.bathrooms:
            if float(property_row.bathrooms) >= parameters['bathrooms']:
                score += 0.1
        
        return min(score, 1.0)

    def _get_reelly_property_context(self, parameters: Dict[str, Any], max_items: int) -> List[ContextItem]:
        """Fetches and formats property context from the Reelly API."""
        reelly_items = []
        
        if not self.reelly_service or not self.reelly_service.is_enabled():
            return reelly_items
        
        try:
            logger.info(f"Fetching live properties from Reelly API with params: {parameters}")
            properties = self.reelly_service.search_properties(parameters)
            
            for prop in properties[:max_items]:
                # Format the property data for display
                formatted_prop = self.reelly_service.format_property_for_display(prop)
                
                # Create content string for the context
                content = (
                    f"LIVE LISTING (Reelly Network): {formatted_prop.get('title', 'N/A')}. "
                    f"Price: {formatted_prop.get('price', {}).get('formatted', 'N/A')}. "
                    f"Beds: {formatted_prop.get('bedrooms', 'N/A')}. "
                    f"Listed by: Agent {formatted_prop.get('agent', {}).get('name', 'N/A')} "
                    f"from {formatted_prop.get('agent', {}).get('company', 'N/A')}. "
                    f"Address: {formatted_prop.get('address', 'N/A')}"
                )
                
                reelly_items.append(ContextItem(
                    content=content,
                    source="reelly_api_live",
                    relevance_score=0.95,  # Give live data a higher score
                    metadata=formatted_prop
                ))
                
            logger.info(f"Successfully fetched {len(reelly_items)} live properties from Reelly API")
            
        except Exception as e:
            logger.error(f"Failed to get context from Reelly API: {e}")
        
        return reelly_items

    def build_structured_context(self, context_items: List[ContextItem]) -> str:
        """Build a structured, scannable context string"""
        if not context_items:
            return "No relevant data found."
        
        # Separate different types of data
        properties = [item for item in context_items if item.source == 'database_properties']
        reelly_properties = [item for item in context_items if item.source == 'reelly_api_live']
        neighborhoods = [item for item in context_items if item.source == 'comprehensive_neighborhoods']
        market_data = [item for item in context_items if item.source == 'comprehensive_market_data']
        documents = [item for item in context_items if item.source.startswith('chroma_')]
        
        context_parts = []
        
        # Properties section with structured data
        if properties:
            context_parts.append("**INTERNAL PROPERTY DATA:**")
            for i, prop in enumerate(properties[:5], 1):  # Limit to top 5
                metadata = prop.metadata
                context_parts.append(f"{i}. **{metadata.get('address', 'N/A')}**")
                context_parts.append(f"   • Price: AED {metadata.get('price', 0):,.0f}")
                context_parts.append(f"   • Type: {metadata.get('property_type', 'N/A')}")
                context_parts.append(f"   • Bedrooms: {metadata.get('bedrooms', 'N/A')}")
                context_parts.append(f"   • Bathrooms: {metadata.get('bathrooms', 'N/A')}")
                context_parts.append("")
        
        # Reelly live properties section
        if reelly_properties:
            context_parts.append("**LIVE PROPERTY LISTINGS (Reelly Network):**")
            for i, prop in enumerate(reelly_properties[:5], 1):  # Limit to top 5
                metadata = prop.metadata
                context_parts.append(f"{i}. **{metadata.get('title', 'N/A')}**")
                context_parts.append(f"   • Price: {metadata.get('price', {}).get('formatted', 'N/A')}")
                context_parts.append(f"   • Type: {metadata.get('property_type', 'N/A')}")
                context_parts.append(f"   • Bedrooms: {metadata.get('bedrooms', 'N/A')}")
                context_parts.append(f"   • Agent: {metadata.get('agent', {}).get('name', 'N/A')} ({metadata.get('agent', {}).get('company', 'N/A')})")
                context_parts.append(f"   • Address: {metadata.get('address', 'N/A')}")
                context_parts.append("")
        
        # Market data section
        if market_data:
            context_parts.append("**MARKET INSIGHTS:**")
            for data in market_data[:3]:  # Limit to top 3
                context_parts.append(f"• {data.content}")
            context_parts.append("")
        
        # Neighborhood data section
        if neighborhoods:
            context_parts.append("**NEIGHBORHOOD INFORMATION:**")
            for hood in neighborhoods[:2]:  # Limit to top 2
                context_parts.append(f"• {hood.content}")
            context_parts.append("")
        
        # Document data section
        if documents:
            context_parts.append("**ADDITIONAL DATA:**")
            for doc in documents[:2]:  # Limit to top 2
                context_parts.append(f"• {doc.content[:200]}...")
            context_parts.append("")
        
        return "\n".join(context_parts)

    def build_context_string(self, context_items: List[ContextItem]) -> str:
        """Build context string for prompt creation (alias for build_structured_context)"""
        return self.build_structured_context(context_items)

    def create_improved_prompt(self, query: str, analysis: QueryAnalysis, context: str, user_role: str = "client") -> str:
        """Create an improved prompt with enhanced Dubai real estate context"""
        
        # Enhanced system prompt with specific Dubai real estate expertise
        system_prompt = f"""
You are an expert Dubai real estate AI assistant with deep knowledge of the local market. Provide specific, data-driven responses with actual Dubai real estate information.

RESPONSE REQUIREMENTS:
1. **Start with direct answer** - No conversational fillers like "Hello" or "I understand"
2. **Use specific Dubai data** - Include actual prices, areas, developers, and market statistics
3. **Structured formatting** - Use headers, bullet points, bold keywords, and tables
4. **Actionable insights** - Provide specific next steps and recommendations
5. **Dubai-specific context** - Reference actual neighborhoods, developers, and market conditions

DUBAI REAL ESTATE CONTEXT:
- **Popular Areas**: Dubai Marina (AED 1.2M-8M), Downtown Dubai (AED 1.5M-15M), Palm Jumeirah (AED 3M-50M), Business Bay (AED 800K-5M), JBR (AED 1M-6M), Dubai Hills Estate (AED 1.5M-12M)
- **Developers**: Emaar, Damac, Nakheel, Sobha, Dubai Properties, Meraas, Azizi, Ellington
- **Market Trends**: 2024 shows 15-20% appreciation, rental yields 5-8%, strong demand for 1-2BR apartments
- **Investment Benefits**: Golden Visa eligibility, 0% income tax, high rental yields, strong capital appreciation
- **Regulations**: RERA protection, escrow accounts, freehold ownership for expats in designated areas

USER ROLE: {user_role.upper()}

RESPONSE FORMAT:
**Direct Answer** (1-2 sentences)
**Key Data Points** (bullet points with specific numbers)
**Market Context** (current trends and conditions)
**Recommendations** (specific actionable steps)
**Next Steps** (what the user should do next)
"""

        # Role-specific context
        role_context = ""
        if user_role == "client":
            role_context = """
CLIENT ROLE CONTEXT:
- Focus on property search, market information, and investment opportunities
- Provide pricing guidance and area recommendations
- Include financing options and payment plans
- Mention Golden Visa benefits and residency requirements
"""
        elif user_role == "agent":
            role_context = """
AGENT ROLE CONTEXT:
- Provide market analysis and competitive insights
- Include lead generation and client management tips
- Share sales strategies and negotiation techniques
- Offer property valuation and listing optimization advice
"""
        elif user_role == "admin":
            role_context = """
ADMIN ROLE CONTEXT:
- Focus on system management and data analysis
- Provide performance metrics and reporting insights
- Include user management and security considerations
- Offer business intelligence and market forecasting
"""

        # Intent-specific context
        intent_context = ""
        if analysis.intent == QueryIntent.PROPERTY_SEARCH:
            intent_context = """
PROPERTY SEARCH CONTEXT:
- Provide specific property recommendations based on budget and preferences
- Include current market prices and availability
- Mention payment plans and financing options
- Suggest similar properties and alternatives
"""
        elif analysis.intent == QueryIntent.MARKET_INFO:
            intent_context = """
MARKET INFORMATION CONTEXT:
- Provide current market statistics and trends
- Include price movements and market forecasts
- Mention investment opportunities and risks
- Compare different areas and property types
"""
        elif analysis.intent == QueryIntent.INVESTMENT_QUESTION:
            intent_context = """
INVESTMENT CONTEXT:
- Focus on ROI and investment returns
- Include rental yields and capital appreciation
- Mention Golden Visa benefits and tax advantages
- Provide investment strategy recommendations
"""

        # Build the complete prompt
        prompt = f"""
{system_prompt}

{role_context}

{intent_context}

RELEVANT CONTEXT FROM DATABASE:
{context}

USER QUERY: {query}

QUERY ANALYSIS:
- Intent: {analysis.intent.value}
- Entities: {analysis.entities}
- Parameters: {analysis.parameters}
- Confidence: {analysis.confidence:.2f}

IMPORTANT: Provide specific Dubai real estate information, actual prices, and actionable recommendations. Avoid generic responses.
"""

        return prompt

    def _get_neighborhood_context(self, query: str, max_items: int) -> List[ContextItem]:
        """Get relevant neighborhood information from database"""
        context_items = []
        
        try:
            with self.engine.connect() as conn:
                sql = """
                    SELECT name, description, price_ranges, rental_yields, amenities, pros, cons, source_file
                    FROM neighborhood_profiles 
                    WHERE name ILIKE :query OR description ILIKE :query
                    LIMIT :limit
                """
                
                result = conn.execute(text(sql), {
                    'query': f"%{query}%",
                    'limit': max_items
                })
                
                for row in result:
                    content = f"""
                    Neighborhood: {row.name}
                    Description: {row.description}
                    Price Ranges: {row.price_ranges}
                    Rental Yields: {row.rental_yields}
                    Amenities: {row.amenities}
                    Pros: {row.pros}
                    Cons: {row.cons}
                    Source: {row.source_file}
                    """
                    
                    context_items.append(ContextItem(
                        content=content,
                        source="comprehensive_neighborhoods",
                        relevance_score=0.9,
                        metadata={'type': 'neighborhood', 'name': row.name}
                    ))
                    
        except Exception as e:
            logger.warning(f"Error getting neighborhood context: {e}")
        
        return context_items

    def _get_market_context(self, query: str, max_items: int) -> List[ContextItem]:
        """Get relevant market information from database"""
        context_items = []
        
        try:
            with self.engine.connect() as conn:
                sql = """
                    SELECT content, type, source_file
                    FROM market_data 
                    WHERE content ILIKE :query OR type ILIKE :query
                    LIMIT :limit
                """
                
                result = conn.execute(text(sql), {
                    'query': f"%{query}%",
                    'limit': max_items
                })
                
                for row in result:
                    context_items.append(ContextItem(
                        content=row.content,
                        source="comprehensive_market_data",
                        relevance_score=0.8,
                        metadata={'type': 'market_data', 'data_type': row.type}
                    ))
                    
        except Exception as e:
            logger.warning(f"Error getting market context: {e}")
        
        return context_items

    # TODO: [CLEANUP] - Review for removal - Duplicate method definition
    # def analyze_query(self, query: str) -> QueryAnalysis:
    #     """Analyze query to determine intent and extract entities"""
    #     # Determine intent
    #     intent = QueryIntent.GENERAL
    #     max_confidence = 0.0
    #     
    #     for query_intent, patterns in self.intent_patterns.items():
    #         for pattern in patterns:
    #             if re.search(pattern, query, re.IGNORECASE):
    #                 confidence = len(re.findall(pattern, query, re.IGNORECASE)) / len(query.split())
    #                 if confidence > max_confidence:
    #                     max_confidence = confidence
    #                     intent = query_intent
    #     
    #     # Extract entities
    #     entities = {}
    #     for entity_type, patterns in self.entity_patterns.items():
    #         for pattern in patterns:
    #             matches = re.findall(pattern, query, re.IGNORECASE)
    #             if matches:
    #                 entities[entity_type] = matches[0] if isinstance(matches[0], str) else matches[0][0]
    #     
    #     # Extract parameters
    #     parameters = self._extract_parameters(entities)
    #     
    #     return QueryAnalysis(
    #         intent=intent,
    #         entities=entities,
    #         parameters=parameters,
    #         confidence=max_confidence
    #     )

    # TODO: [CLEANUP] - Review for removal - Duplicate method definition
    # def _extract_parameters(self, entities: Dict[str, Any]) -> Dict[str, Any]:
    #     """Extract and normalize parameters from entities"""
    #     parameters = {}
    #     
    #     # Budget parameters
    #     if 'budget' in entities:
    #         try:
    #             budget_str = str(entities['budget']).lower()
    #             if 'million' in budget_str or 'm' in budget_str:
    #                 # Convert to AED (assuming 1M = 1,000,000 AED)
    #                 budget_val = float(re.findall(r'[\d.]+', budget_str)[0]) * 1000000
    #                 parameters['budget_max'] = budget_val
    #                 parameters['budget_min'] = budget_val * 0.8
    #             elif 'thousand' in budget_str or 'k' in budget_str:
    #                 budget_val = float(re.findall(r'[\d.]+', budget_str)[0]) * 1000
    #                 parameters['budget_max'] = budget_val
    #                 parameters['budget_min'] = budget_val * 0.8
    #             else:
    #                 budget_val = float(re.findall(r'[\d,]+', budget_str)[0].replace(',', ''))
    #                 parameters['budget_max'] = budget_val
    #                 parameters['budget_min'] = budget_val * 0.8
    #         except:
    #             pass
    #     
    #     # Location parameters
    #     if 'location' in entities:
    #         parameters['location'] = entities['location']
    #     
    #     # Property type parameters
    #     if 'property_type' in entities:
    #         parameters['property_type'] = entities['property_type']
    #     
    #     # Bedrooms
    #     if 'bedrooms' in entities:
    #         try:
    #             parameters['bedrooms'] = int(entities['bedrooms'])
    #         except:
    #             pass
    #     
    #     # Bathrooms
    #     if 'bathrooms' in entities:
    #         try:
    #             parameters['bathrooms'] = float(entities['bathrooms'])
    #         except:
    #             pass
    #     
    #     return parameters

    # TODO: [CLEANUP] - Review for removal - Duplicate method definition
    # def get_relevant_context(self, query: str, analysis: QueryAnalysis, max_items: int = 5) -> List[ContextItem]:
    #     """Get relevant context from multiple sources based on query analysis"""
    #     context_items = []
    #     
    #     # Get relevant documents from ChromaDB
    #     doc_context = self._get_document_context(query, analysis.intent, max_items)
    #     context_items.extend(doc_context)
    #     
    #     # Get relevant properties from database
        if analysis.intent == QueryIntent.PROPERTY_SEARCH:
            prop_context = self._get_property_context(analysis.parameters, max_items * 2)
            context_items.extend(prop_context)
        else:
            prop_context = self._get_property_context(analysis.parameters, max_items)
            context_items.extend(prop_context)
        
        # Get relevant neighborhoods and market data
        if analysis.intent in [QueryIntent.NEIGHBORHOOD_QUESTION, QueryIntent.MARKET_INFO]:
            neighborhood_context = self._get_neighborhood_context(query, max_items)
            context_items.extend(neighborhood_context)
            
            market_context = self._get_market_context(query, max_items)
            context_items.extend(market_context)
        
        # Sort by relevance and return top items
        context_items.sort(key=lambda x: x.relevance_score, reverse=True)
        return context_items[:max_items]

    def _get_document_context(self, query: str, intent: QueryIntent, max_items: int) -> List[ContextItem]:
        """Get relevant documents from ChromaDB collections"""
        context_items = []
        
        # Enhanced collection mapping to use ALL specialized collections
        collection_mapping = {
            QueryIntent.PROPERTY_SEARCH: ["real_estate_docs", "market_analysis", "neighborhood_profiles", "developer_profiles"],
            QueryIntent.MARKET_INFO: ["market_analysis", "market_forecasts", "financial_insights", "investment_insights"],
            QueryIntent.INVESTMENT_QUESTION: ["investment_insights", "market_analysis", "financial_insights", "market_forecasts"],
            QueryIntent.REGULATORY_QUESTION: ["regulatory_framework", "transaction_guidance", "real_estate_docs"],
            QueryIntent.NEIGHBORHOOD_QUESTION: ["neighborhood_profiles", "urban_planning", "market_analysis"],
            QueryIntent.DEVELOPER_QUESTION: ["developer_profiles", "market_analysis", "investment_insights"],
            QueryIntent.POLICY_QUESTION: ["regulatory_framework", "agent_resources", "transaction_guidance"],
            QueryIntent.AGENT_SUPPORT: ["agent_resources", "transaction_guidance", "market_analysis"],
            QueryIntent.GENERAL: ["real_estate_docs", "comprehensive_data", "market_analysis"]
        }
        
        collections = collection_mapping.get(intent, ["comprehensive_data"])
        
        for collection_name in collections:
            try:
                collection = self.chroma_client.get_collection(collection_name)
                results = collection.query(
                    query_texts=[query],
                    n_results=max_items * 2
                )
                
                if results['documents'] and results['documents'][0]:
                    for i, doc in enumerate(results['documents'][0]):
                        score = 1.0 - (results['distances'][0][i] if results['distances'] and results['distances'][0] else 0.5)
                        metadata = results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {}
                        
                        context_items.append(ContextItem(
                            content=doc,
                            source=f"chroma_{collection_name}",
                            relevance_score=score,
                            metadata=metadata
                        ))
            except Exception as e:
                logger.warning(f"Error querying collection {collection_name}: {e}")
                continue
        
        return context_items

    def _get_property_context(self, parameters: Dict[str, Any], max_items: int) -> List[ContextItem]:
        """Get relevant properties from database based on parameters"""
        context_items = []
        
        # Build SQL query based on parameters
        sql_parts = ["SELECT * FROM properties WHERE 1=1"]
        query_params = {}
        
        if not parameters:
            sql_parts.append("AND price > 0")
        
        if 'budget_min' in parameters and 'budget_max' in parameters:
            sql_parts.append("AND price BETWEEN :budget_min AND :budget_max")
        
        if 'location' in parameters:
            sql_parts.append("AND location ILIKE :location")
        
        if 'property_type' in parameters:
            sql_parts.append("AND property_type ILIKE :property_type")
        
        if 'bedrooms' in parameters:
            sql_parts.append("AND bedrooms >= :bedrooms")
        
        if 'bathrooms' in parameters:
            sql_parts.append("AND bathrooms >= :bathrooms")
        
        sql_parts.append("ORDER BY price ASC LIMIT :limit")
        query_params['limit'] = max_items
        
        try:
            with self.engine.connect() as conn:
                sql = " ".join(sql_parts)
                result = conn.execute(text(sql), query_params)
                
                for row in result:
                    content = f"""
                    Property: {row.address}
                    Price: AED {row.price:,.0f}
                    Type: {row.property_type}
                    Bedrooms: {row.bedrooms}
                    Bathrooms: {row.bathrooms}
                    Location: {row.location}
                    """
                    
                    context_items.append(ContextItem(
                        content=content,
                        source="properties",
                        relevance_score=0.9,
                        metadata={
                            'type': 'property',
                            'address': row.address,
                            'price': row.price,
                            'property_type': row.property_type,
                            'bedrooms': row.bedrooms,
                            'bathrooms': row.bathrooms,
                            'location': row.location
                        }
                    ))
                    
        except Exception as e:
            logger.warning(f"Error getting property context: {e}")
        
        return context_items
