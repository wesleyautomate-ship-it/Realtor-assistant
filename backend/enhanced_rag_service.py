import os
import re
import json
from typing import List, Dict, Any, Optional, Tuple
import chromadb
from sqlalchemy import create_engine, text
import logging
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

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
    TRANSACTION_GUIDANCE = "transaction_guidance"
    FINANCIAL_INSIGHTS = "financial_insights"
    URBAN_PLANNING = "urban_planning"
    GENERAL = "general"

@dataclass
class QueryAnalysis:
    intent: QueryIntent
    entities: Dict[str, Any]
    parameters: Dict[str, Any]
    confidence: float
    dubai_specific: bool = False

@dataclass
class ContextItem:
    content: str
    source: str
    relevance_score: float
    metadata: Dict[str, Any]
    data_type: str = "text"  # text, structured, hybrid

class EnhancedRAGService:
    def __init__(self, db_url: str, chroma_host: str = "localhost", chroma_port: int = 8000):
        self.engine = create_engine(db_url)
        self.chroma_client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
        
        # Enhanced intent classification patterns for Dubai real estate
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
                r'\b(rental yield|investment return|property investment)\b',
                r'\b(roi|return.*investment|investment.*return)\b.*\b(dubai|real estate|property)\b',
                r'\b(investing|investment)\b.*\b(dubai|real estate)\b'
            ],
            QueryIntent.REGULATORY_QUESTION: [
                r'\b(law|regulation|rera|escrow|legal|compliance)\b',
                r'\b(golden visa|visa requirements|residency visa)\b',
                r'\b(freehold|leasehold|ownership rights)\b',
                r'\b(dubai land department|dld|mortgage regulations)\b',
                r'\b(regulatory|regulations|legal.*requirement)\b',
                r'\b(foreign.*investor|international.*investor|expat.*regulation)\b'
            ],
            QueryIntent.NEIGHBORHOOD_QUESTION: [
                r'\b(dubai marina|downtown|palm jumeirah|business bay|jbr|jumeirah|dubai hills|arabian ranches|emirates hills)\b.*\b(area|neighborhood|community|amenities)\b',
                r'\b(tell me about|describe|what is)\b.*\b(dubai marina|downtown|palm jumeirah|business bay)\b',
                r'\b(schools|hospitals|transport|metro|amenities)\b.*\b(area|neighborhood)\b',
                r'\b(schools|hospitals|amenities)\b.*\b(available|are there|what)\b',
                r'\b(what)\b.*\b(schools|hospitals|amenities)\b.*\b(available|in)\b'
            ],
            QueryIntent.DEVELOPER_QUESTION: [
                r'\b(emaar|damac|nakheel|sobha|dubai properties|meraas)\b',
                r'\b(developer|builder|construction company)\b',
                r'\b(who built|who developed|which developer)\b'
            ],
            QueryIntent.TRANSACTION_GUIDANCE: [
                r'\b(how to buy|purchase process|buying process|transaction|process|deal structure|structuring)\b',
                r'\b(legal requirements|documentation|contract|agreement|documents)\b',
                r'\b(escrow|payment|financing|mortgage)\b',
                r'\b(transfer|registration|title deed)\b',
                r'\b(what.*process|how.*buy|steps.*purchase|how.*structure|deal.*structure)\b',
                r'\b(transaction.*guidance|deal.*guidance|purchase.*guidance)\b',
                r'\b(what.*documents|documents.*need|documentation.*required)\b',
                r'\b(process.*buying|buying.*process|purchase.*process)\b'
            ],
            QueryIntent.FINANCIAL_INSIGHTS: [
                r'\b(mortgage|financing|loan|lending)\b',
                r'\b(interest rate|ltv|down payment|mortgage rate)\b',
                r'\b(bank|lender|financial institution)\b',
                r'\b(payment plan|installment|financing option)\b',
                r'\b(ltv ratio|loan.*value|financing.*option)\b',
                r'\b(roi|return.*investment|investment.*return|profit|yield)\b',
                r'\b(financial.*insight|financial.*analysis|financial.*guidance)\b',
                r'\b(mortgage.*rate|current.*mortgage|mortgage.*rates)\b',
                r'\b(what.*mortgage|mortgage.*what|rates.*mortgage)\b'
            ],
            QueryIntent.URBAN_PLANNING: [
                r'\b(dubai 2040|master plan|urban development|urban planning)\b',
                r'\b(infrastructure|transport|metro|tram|infrastructure.*project)\b',
                r'\b(sustainability|green building|smart city)\b',
                r'\b(future development|planned project|development.*plan)\b',
                r'\b(master.*plan|urban.*planning|city.*planning)\b'
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
            ]
        }
        
        # Enhanced entity extraction patterns for Dubai-specific entities
        self.entity_patterns = {
            'budget': [
                r'\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:k|thousand|million|m)?',
                r'(\d+)\s*(?:k|thousand|million|m)\s*(?:dollars?|aed)?',
                r'budget.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
                r'price.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
            ],
            'location': [
                r'\b(dubai marina|downtown|palm jumeirah|business bay|jbr|jumeirah|dubai hills|arabian ranches|emirates hills)\b',
                r'\b(area|neighborhood|location)\b.*?\b(\w+(?:\s+\w+)*)\b',
                r'in\s+(\w+(?:\s+\w+)*)',
                r'(\w+(?:\s+\w+)*)\s+area'
            ],
            'property_type': [
                r'\b(apartment|condo|villa|house|townhouse|penthouse|studio)\b',
                r'\b(residential|commercial|office|retail)\b'
            ],
            'developer': [
                r'\b(emaar|damac|nakheel|sobha|dubai properties|meraas|azizi|ellington)\b',
                r'\b(developer|builder)\b.*?\b(\w+(?:\s+\w+)*)\b'
            ],
            'bedrooms': [
                r'(\d+)\s*bedroom',
                r'(\d+)\s*br',
                r'(\d+)\s*bed'
            ],
            'bathrooms': [
                r'(\d+(?:\.\d+)?)\s*bathroom',
                r'(\d+(?:\.\d+)?)\s*bath'
            ]
        }
        
        # Enhanced collection mapping for Dubai real estate collections
        self.collection_mapping = {
            QueryIntent.PROPERTY_SEARCH: ["neighborhood_profiles", "market_analysis", "developer_profiles"],
            QueryIntent.MARKET_INFO: ["market_analysis", "market_forecasts", "neighborhood_profiles"],
            QueryIntent.INVESTMENT_QUESTION: ["investment_insights", "financial_insights", "market_analysis"],
            QueryIntent.REGULATORY_QUESTION: ["regulatory_framework", "transaction_guidance"],
            QueryIntent.NEIGHBORHOOD_QUESTION: ["neighborhood_profiles", "urban_planning", "market_analysis"],
            QueryIntent.DEVELOPER_QUESTION: ["developer_profiles", "market_analysis"],
            QueryIntent.TRANSACTION_GUIDANCE: ["transaction_guidance", "regulatory_framework"],
            QueryIntent.FINANCIAL_INSIGHTS: ["financial_insights", "investment_insights"],
            QueryIntent.URBAN_PLANNING: ["urban_planning", "market_forecasts"],
            QueryIntent.POLICY_QUESTION: ["transaction_guidance", "regulatory_framework"],
            QueryIntent.AGENT_SUPPORT: ["agent_resources", "transaction_guidance"],
            QueryIntent.GENERAL: ["market_analysis", "neighborhood_profiles", "regulatory_framework"]
        }

    def analyze_query(self, query: str) -> QueryAnalysis:
        """Analyze user query to extract intent, entities, and parameters with Dubai-specific detection"""
        query_lower = query.lower()
        
        # Check if query is Dubai-specific
        dubai_keywords = [
            'dubai', 'marina', 'downtown', 'palm jumeirah', 'business bay', 'jbr',
            'jumeirah', 'arabian ranches', 'emirates hills', 'emaar', 'damac', 'nakheel',
            'golden visa', 'rera', 'escrow', 'freehold', 'aed', 'dirham'
        ]
        dubai_specific = any(keyword in query_lower for keyword in dubai_keywords)
        
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
            confidence=confidence,
            dubai_specific=dubai_specific
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
        
        # Developer
        if 'developer' in entities:
            parameters['developer'] = entities['developer']
        
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

    def get_relevant_context(self, query: str, analysis: QueryAnalysis, max_items: int = 8) -> List[ContextItem]:
        """Get relevant context from multiple sources based on query analysis with optimized performance"""
        context_items = []
        
        # Determine which collections to query based on intent
        collections = self.collection_mapping.get(analysis.intent, ["market_analysis"])
        
        # Limit the number of collections to query for better performance
        if len(collections) > 3:
            collections = collections[:3]
        
        # Get relevant documents from ChromaDB with optimized query
        doc_context = self._get_document_context_optimized(query, analysis.intent, collections, max_items // 2)
        context_items.extend(doc_context)
        
        # Get relevant structured data from PostgreSQL only if needed
        structured_context = []
        if analysis.intent in [QueryIntent.NEIGHBORHOOD_QUESTION, QueryIntent.DEVELOPER_QUESTION, 
                              QueryIntent.MARKET_INFO, QueryIntent.INVESTMENT_QUESTION, QueryIntent.REGULATORY_QUESTION]:
            structured_context = self._get_structured_context(analysis, max_items // 2)
        context_items.extend(structured_context)
        
        # Sort by relevance and return top items
        context_items.sort(key=lambda x: x.relevance_score, reverse=True)
        return context_items[:max_items]

    def _get_document_context_optimized(self, query: str, intent: QueryIntent, collections: List[str], max_items: int) -> List[ContextItem]:
        """Optimized ChromaDB context retrieval with reduced queries"""
        context_items = []
        
        # Calculate items per collection
        items_per_collection = max(1, max_items // len(collections))
        
        for collection_name in collections:
            try:
                collection = self.chroma_client.get_collection(collection_name)
                
                # Use more specific query with higher n_results for better relevance
                results = collection.query(
                    query_texts=[query],
                    n_results=items_per_collection
                )
                
                if results['documents'] and results['documents'][0]:
                    for i, doc in enumerate(results['documents'][0]):
                        score = 1.0 - (results['distances'][0][i] if results['distances'] and results['distances'][0] else 0.5)
                        metadata = results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {}
                        
                        context_items.append(ContextItem(
                            content=doc,
                            source=f"chroma_{collection_name}",
                            relevance_score=score,
                            metadata=metadata,
                            data_type="text"
                        ))
            except Exception as e:
                logger.warning(f"Error querying collection {collection_name}: {e}")
                continue
        
        return context_items

    def _get_document_context(self, query: str, intent: QueryIntent, max_items: int) -> List[ContextItem]:
        """Get relevant documents from ChromaDB collections"""
        context_items = []
        
        collections = self.collection_mapping.get(intent, ["market_analysis"])
        
        for collection_name in collections:
            try:
                collection = self.chroma_client.get_collection(collection_name)
                results = collection.query(
                    query_texts=[query],
                    n_results=max_items
                )
                
                if results['documents'] and results['documents'][0]:
                    for i, doc in enumerate(results['documents'][0]):
                        score = 1.0 - (results['distances'][0][i] if results['distances'] and results['distances'][0] else 0.5)
                        metadata = results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {}
                        
                        context_items.append(ContextItem(
                            content=doc,
                            source=f"chroma_{collection_name}",
                            relevance_score=score,
                            metadata=metadata,
                            data_type="text"
                        ))
            except Exception as e:
                logger.warning(f"Error querying collection {collection_name}: {e}")
                continue
        
        return context_items

    def _get_structured_context(self, analysis: QueryAnalysis, max_items: int) -> List[ContextItem]:
        """Get relevant structured data from PostgreSQL tables"""
        context_items = []
        
        # Get data from different tables based on intent
        if analysis.intent == QueryIntent.NEIGHBORHOOD_QUESTION:
            context_items.extend(self._get_neighborhood_data(analysis, max_items))
        elif analysis.intent == QueryIntent.DEVELOPER_QUESTION:
            context_items.extend(self._get_developer_data(analysis, max_items))
        elif analysis.intent == QueryIntent.MARKET_INFO:
            context_items.extend(self._get_market_data(analysis, max_items))
        elif analysis.intent == QueryIntent.INVESTMENT_QUESTION:
            context_items.extend(self._get_investment_data(analysis, max_items))
        elif analysis.intent == QueryIntent.REGULATORY_QUESTION:
            context_items.extend(self._get_regulatory_data(analysis, max_items))
        
        return context_items

    def _get_neighborhood_data(self, analysis: QueryAnalysis, max_items: int) -> List[ContextItem]:
        """Get neighborhood profile data"""
        context_items = []
        
        try:
            with self.engine.connect() as conn:
                # Query neighborhood_profiles table
                sql = """
                SELECT name, description, amenities, price_ranges, 
                       rental_yields, market_trends, transportation_links
                FROM neighborhood_profiles 
                WHERE name ILIKE :search_term OR description ILIKE :search_term
                LIMIT :limit
                """
                
                search_term = f"%{analysis.entities.get('location', 'dubai')}%"
                result = conn.execute(text(sql), {"search_term": search_term, "limit": max_items})
                
                for row in result:
                    content = f"Neighborhood: {row.name}\n"
                    content += f"Description: {row.description}\n"
                    if row.amenities:
                        amenities = json.loads(row.amenities) if isinstance(row.amenities, str) else row.amenities
                        if isinstance(amenities, list):
                            content += f"Amenities: {', '.join(amenities[:5])}\n"
                        elif isinstance(amenities, dict):
                            content += f"Amenities: {', '.join(list(amenities.keys())[:5])}\n"
                    if row.price_ranges:
                        price_ranges = json.loads(row.price_ranges) if isinstance(row.price_ranges, str) else row.price_ranges
                        if isinstance(price_ranges, dict):
                            content += f"Price Range: {price_ranges.get('min', 'N/A')} - {price_ranges.get('max', 'N/A')} AED/sqft\n"
                    if row.transportation_links:
                        transport = row.transportation_links if isinstance(row.transportation_links, list) else []
                        if transport:
                            content += f"Transportation: {', '.join(transport[:3])}\n"
                    
                    context_items.append(ContextItem(
                        content=content,
                        source="postgres_neighborhood_profiles",
                        relevance_score=0.9,
                        metadata={
                            'neighborhood': row.name,
                            'data_type': 'neighborhood_profile'
                        },
                        data_type="structured"
                    ))
        except Exception as e:
            logger.error(f"Error querying neighborhood data: {e}")
        
        return context_items

    def _get_developer_data(self, analysis: QueryAnalysis, max_items: int) -> List[ContextItem]:
        """Get developer profile data"""
        context_items = []
        
        try:
            with self.engine.connect() as conn:
                # Query developers table
                sql = """
                SELECT name, type, market_share, total_projects, 
                       avg_project_value, reputation_score, specialties, key_projects
                FROM developers 
                WHERE name ILIKE :search_term OR type ILIKE :search_term
                LIMIT :limit
                """
                
                search_term = f"%{analysis.entities.get('developer', 'developer')}%"
                result = conn.execute(text(sql), {"search_term": search_term, "limit": max_items})
                
                for row in result:
                    content = f"Developer: {row.name}\n"
                    content += f"Type: {row.type}\n"
                    if row.market_share:
                        content += f"Market Share: {row.market_share}%\n"
                    if row.total_projects:
                        content += f"Total Projects: {row.total_projects}\n"
                    if row.avg_project_value:
                        content += f"Average Project Value: AED {row.avg_project_value:,.0f}\n"
                    if row.reputation_score:
                        content += f"Reputation Score: {row.reputation_score}/10\n"
                    if row.specialties:
                        specialties = row.specialties if isinstance(row.specialties, list) else []
                        if specialties:
                            content += f"Specialties: {', '.join(specialties[:3])}\n"
                    
                    context_items.append(ContextItem(
                        content=content,
                        source="postgres_developers",
                        relevance_score=0.9,
                        metadata={
                            'developer': row.name,
                            'market_share': row.market_share,
                            'reputation_score': row.reputation_score,
                            'data_type': 'developer_profile'
                        },
                        data_type="structured"
                    ))
        except Exception as e:
            logger.error(f"Error querying developer data: {e}")
        
        return context_items

    def _get_market_data(self, analysis: QueryAnalysis, max_items: int) -> List[ContextItem]:
        """Get market data"""
        context_items = []
        
        try:
            with self.engine.connect() as conn:
                # Query market_data table
                sql = """
                SELECT date, neighborhood, property_type, avg_price_per_sqft, 
                       transaction_volume, price_change_percent, rental_yield, market_trend
                FROM market_data 
                WHERE neighborhood ILIKE :search_term OR property_type ILIKE :search_term
                ORDER BY date DESC
                LIMIT :limit
                """
                
                search_term = f"%{analysis.entities.get('location', 'dubai')}%"
                result = conn.execute(text(sql), {"search_term": search_term, "limit": max_items})
                
                for row in result:
                    content = f"Market Data ({row.date}): {row.neighborhood}\n"
                    content += f"Property Type: {row.property_type}\n"
                    if row.avg_price_per_sqft:
                        content += f"Average Price: AED {row.avg_price_per_sqft:,.0f}/sqft\n"
                    if row.transaction_volume:
                        content += f"Transaction Volume: {row.transaction_volume}\n"
                    if row.price_change_percent:
                        content += f"Price Change: {row.price_change_percent}%\n"
                    if row.rental_yield:
                        content += f"Rental Yield: {row.rental_yield}%\n"
                    if row.market_trend:
                        content += f"Market Trend: {row.market_trend}\n"
                    
                    context_items.append(ContextItem(
                        content=content,
                        source="postgres_market_data",
                        relevance_score=0.8,
                        metadata={
                            'date': str(row.date),
                            'neighborhood': row.neighborhood,
                            'price_per_sqft': row.avg_price_per_sqft,
                            'rental_yield': row.rental_yield,
                            'data_type': 'market_data'
                        },
                        data_type="structured"
                    ))
        except Exception as e:
            logger.error(f"Error querying market data: {e}")
        
        return context_items

    def _get_investment_data(self, analysis: QueryAnalysis, max_items: int) -> List[ContextItem]:
        """Get investment insights data"""
        context_items = []
        
        try:
            with self.engine.connect() as conn:
                # Query investment_insights table
                sql = """
                SELECT category, title, description, roi_projection, 
                       risk_level, investment_amount_min, investment_amount_max, key_benefits
                FROM investment_insights 
                WHERE category ILIKE :search_term OR title ILIKE :search_term
                LIMIT :limit
                """
                
                search_term = f"%{analysis.entities.get('property_type', 'investment')}%"
                result = conn.execute(text(sql), {"search_term": search_term, "limit": max_items})
                
                for row in result:
                    content = f"Investment Insight: {row.title}\n"
                    content += f"Category: {row.category}\n"
                    content += f"Description: {row.description}\n"
                    if row.roi_projection:
                        content += f"Expected ROI: {row.roi_projection}%\n"
                    if row.risk_level:
                        content += f"Risk Level: {row.risk_level}\n"
                    if row.investment_amount_min and row.investment_amount_max:
                        content += f"Investment Range: AED {row.investment_amount_min:,.0f} - {row.investment_amount_max:,.0f}\n"
                    if row.key_benefits:
                        benefits = row.key_benefits if isinstance(row.key_benefits, list) else []
                        if benefits:
                            content += f"Key Benefits: {', '.join(benefits[:3])}\n"
                    
                    context_items.append(ContextItem(
                        content=content,
                        source="postgres_investment_insights",
                        relevance_score=0.85,
                        metadata={
                            'title': row.title,
                            'category': row.category,
                            'roi': row.roi_projection,
                            'risk_level': row.risk_level,
                            'data_type': 'investment_insight'
                        },
                        data_type="structured"
                    ))
        except Exception as e:
            logger.error(f"Error querying investment data: {e}")
        
        return context_items

    def _get_regulatory_data(self, analysis: QueryAnalysis, max_items: int) -> List[ContextItem]:
        """Get regulatory framework data"""
        context_items = []
        
        try:
            with self.engine.connect() as conn:
                # Query regulatory_updates table
                sql = """
                SELECT law_name, description, enactment_date, status, 
                       impact_areas, key_provisions, compliance_requirements
                FROM regulatory_updates 
                WHERE law_name ILIKE :search_term OR description ILIKE :search_term
                ORDER BY enactment_date DESC
                LIMIT :limit
                """
                
                search_term = f"%{analysis.entities.get('location', 'regulation')}%"
                result = conn.execute(text(sql), {"search_term": search_term, "limit": max_items})
                
                for row in result:
                    content = f"Regulation: {row.law_name}\n"
                    content += f"Description: {row.description}\n"
                    if row.enactment_date:
                        content += f"Enactment Date: {row.enactment_date}\n"
                    if row.status:
                        content += f"Status: {row.status}\n"
                    if row.impact_areas:
                        impact_areas = row.impact_areas if isinstance(row.impact_areas, list) else []
                        if impact_areas:
                            content += f"Impact Areas: {', '.join(impact_areas[:3])}\n"
                    if row.key_provisions:
                        provisions = row.key_provisions if isinstance(row.key_provisions, list) else []
                        if provisions:
                            content += f"Key Provisions: {', '.join(provisions[:3])}\n"
                    
                    context_items.append(ContextItem(
                        content=content,
                        source="postgres_regulatory_updates",
                        relevance_score=0.9,
                        metadata={
                            'title': row.law_name,
                            'status': row.status,
                            'enactment_date': str(row.enactment_date),
                            'data_type': 'regulatory_update'
                        },
                        data_type="structured"
                    ))
        except Exception as e:
            logger.error(f"Error querying regulatory data: {e}")
        
        return context_items

    def build_context_string(self, context_items: List[ContextItem]) -> str:
        """Build a formatted context string from context items"""
        if not context_items:
            return "No relevant information found."
        
        context_parts = []
        
        # Add documents context
        doc_items = [item for item in context_items if item.source.startswith('chroma_')]
        if doc_items:
            context_parts.append("RELEVANT DOCUMENTS:")
            for item in doc_items:
                context_parts.append(f"- {item.content}")
        
        # Add structured data context
        structured_items = [item for item in context_items if item.source.startswith('postgres_')]
        if structured_items:
            context_parts.append("\nRELEVANT STRUCTURED DATA:")
            for item in structured_items:
                context_parts.append(f"- {item.content}")
        
        return "\n".join(context_parts)

    def create_dynamic_prompt(self, query: str, analysis: QueryAnalysis, context: str, user_role: str) -> str:
        """Create a dynamic, focused prompt based on query analysis with Dubai-specific enhancements"""
        
        # Enhanced prompts for different intents including Dubai-specific contexts
        intent_prompts = {
            QueryIntent.PROPERTY_SEARCH: f"""You are a Dubai real estate expert helping a {user_role} find properties.

CONTEXT:
{context}

USER QUERY: {query}

TASK: Help the user find suitable properties based on their requirements. Be specific about Dubai locations, prices in AED, and features. Consider Dubai-specific factors like freehold areas, Golden Visa eligibility, and proximity to key attractions. Suggest follow-up questions to better understand their needs.""",

            QueryIntent.MARKET_INFO: f"""You are a Dubai real estate market analyst providing comprehensive market insights to a {user_role}.

CONTEXT:
{context}

USER QUERY: {query}

TASK: Provide detailed Dubai market analysis, trends, and insights. Include specific data points, price ranges in AED, transaction volumes, and market predictions. Reference Dubai-specific factors like the Dubai 2040 plan, major developments, and economic indicators.""",

            QueryIntent.INVESTMENT_QUESTION: f"""You are a Dubai real estate investment advisor helping a {user_role} with investment decisions.

CONTEXT:
{context}

USER QUERY: {query}

TASK: Provide investment guidance including ROI analysis, rental yields, Golden Visa requirements, and market opportunities. Focus on Dubai-specific investment benefits like tax advantages, capital appreciation trends, and visa benefits.""",

            QueryIntent.REGULATORY_QUESTION: f"""You are a Dubai real estate legal expert helping a {user_role} understand regulations and laws.

CONTEXT:
{context}

USER QUERY: {query}

TASK: Explain Dubai real estate laws, RERA regulations, Golden Visa requirements, freehold vs leasehold, and legal procedures. Provide clear, accurate information about compliance requirements and legal processes in Dubai.""",

            QueryIntent.NEIGHBORHOOD_QUESTION: f"""You are a Dubai area specialist providing detailed neighborhood information to a {user_role}.

CONTEXT:
{context}

USER QUERY: {query}

TASK: Provide comprehensive information about Dubai neighborhoods including amenities, lifestyle, transportation, schools, hospitals, shopping, dining, and investment potential. Compare areas when relevant.""",

            QueryIntent.DEVELOPER_QUESTION: f"""You are a Dubai real estate market expert with extensive knowledge about developers and their projects.

CONTEXT:
{context}

USER QUERY: {query}

TASK: Provide detailed information about Dubai developers, their track record, current projects, reputation, and specialties. Include insights about project quality, delivery timelines, and investment potential.""",

            QueryIntent.TRANSACTION_GUIDANCE: f"""You are a Dubai real estate transaction expert helping a {user_role} with buying/selling processes.

CONTEXT:
{context}

USER QUERY: {query}

TASK: Provide step-by-step guidance on Dubai real estate transactions including legal requirements, documentation, escrow processes, and best practices. Focus on Dubai-specific procedures and requirements.""",

            QueryIntent.FINANCIAL_INSIGHTS: f"""You are a Dubai real estate financial advisor helping a {user_role} with financing and financial planning.

CONTEXT:
{context}

USER QUERY: {query}

TASK: Provide comprehensive financial guidance including mortgage options, financing strategies, payment plans, and financial planning for Dubai real estate investments.""",

            QueryIntent.URBAN_PLANNING: f"""You are a Dubai urban planning expert providing insights on future developments and city planning to a {user_role}.

CONTEXT:
{context}

USER QUERY: {query}

TASK: Provide detailed information about Dubai's urban development plans, infrastructure projects, sustainability initiatives, and future growth areas. Reference the Dubai 2040 plan and major development projects.""",

            QueryIntent.POLICY_QUESTION: f"""You are a real estate policy expert helping a {user_role} understand company policies and procedures.

CONTEXT:
{context}

USER QUERY: {query}

TASK: Explain relevant policies, procedures, and requirements clearly. Provide step-by-step guidance when applicable. Focus on Dubai market-specific procedures when relevant.""",

            QueryIntent.AGENT_SUPPORT: f"""You are a senior Dubai real estate sales coach providing guidance to a {user_role}.

CONTEXT:
{context}

USER QUERY: {query}

TASK: Provide practical sales advice, techniques, and strategies specific to the Dubai market. Focus on actionable steps, best practices, and Dubai-specific selling points like Golden Visa benefits and lifestyle advantages.""",

            QueryIntent.GENERAL: f"""You are a helpful Dubai real estate assistant with comprehensive knowledge responding to a {user_role}.

CONTEXT:
{context}

USER QUERY: {query}

TASK: Provide helpful, accurate information based on the available context. Focus on Dubai real estate market specifics when relevant."""
        }
        
        return intent_prompts.get(analysis.intent, intent_prompts[QueryIntent.GENERAL])
