import os
import re
from typing import List, Dict, Any, Optional, Tuple
import chromadb
from sqlalchemy import create_engine, text
import logging
from dataclasses import dataclass
from enum import Enum

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

class RAGService:
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
        
        # Get relevant documents from ChromaDB
        doc_context = self._get_document_context(query, analysis.intent, max_items)
        context_items.extend(doc_context)
        
        # Get relevant properties from database
        prop_context = self._get_property_context(analysis.parameters, max_items)
        context_items.extend(prop_context)
        
        # Sort by relevance and return top items
        context_items.sort(key=lambda x: x.relevance_score, reverse=True)
        return context_items[:max_items]

    def _get_document_context(self, query: str, intent: QueryIntent, max_items: int) -> List[ContextItem]:
        """Get relevant documents from ChromaDB collections"""
        context_items = []
        
        # Enhanced collection mapping for Dubai real estate collections
        collection_mapping = {
            QueryIntent.PROPERTY_SEARCH: ["neighborhood_profiles", "market_analysis", "developer_profiles"],
            QueryIntent.MARKET_INFO: ["market_analysis", "market_forecasts", "neighborhood_profiles"],
            QueryIntent.INVESTMENT_QUESTION: ["investment_insights", "financial_insights", "market_analysis"],
            QueryIntent.REGULATORY_QUESTION: ["regulatory_framework", "transaction_guidance"],
            QueryIntent.NEIGHBORHOOD_QUESTION: ["neighborhood_profiles", "urban_planning", "market_analysis"],
            QueryIntent.DEVELOPER_QUESTION: ["developer_profiles", "market_analysis"],
            QueryIntent.POLICY_QUESTION: ["real_estate_docs", "transaction_guidance"],
            QueryIntent.AGENT_SUPPORT: ["agent_resources", "transaction_guidance", "real_estate_docs"],
            QueryIntent.GENERAL: ["market_analysis", "real_estate_docs", "neighborhood_profiles"]
        }
        
        collections = collection_mapping.get(intent, ["real_estate_docs"])
        
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
        
        if 'budget_min' in parameters and 'budget_max' in parameters:
            sql_parts.append("AND price BETWEEN :budget_min AND :budget_max")
            query_params['budget_min'] = parameters['budget_min']
            query_params['budget_max'] = parameters['budget_max']
        
        if 'location' in parameters:
            sql_parts.append("AND address ILIKE :location")
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
        query_params['limit'] = max_items
        
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
        
        # Add properties context
        prop_items = [item for item in context_items if item.source == 'database_properties']
        if prop_items:
            context_parts.append("\nRELEVANT PROPERTIES:")
            for item in prop_items:
                context_parts.append(f"- {item.content}")
        
        return "\n".join(context_parts)

    def create_dynamic_prompt(self, query: str, analysis: QueryAnalysis, context: str, user_role: str) -> str:
        """Create a dynamic, focused prompt based on query analysis"""
        
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
