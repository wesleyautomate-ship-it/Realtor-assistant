"""
AI Enhancement Manager
=====================

Main manager that integrates all AI enhancement modules:
- Conversation Memory Management
- Query Understanding
- Response Enhancement
- Context Optimization
- Multi-modal Processing
"""

import json
import logging
import os
from typing import Dict, Any, Optional, List
from sqlalchemy import create_engine, text
from datetime import datetime

try:
    from ai_enhancements import ConversationMemory, MessageType
except ImportError:
    # Fallback if ai_enhancements module is not available
    class ConversationMemory:
        pass
    class MessageType:
        pass
try:
    from query_understanding import QueryUnderstanding
except ImportError:
    class QueryUnderstanding:
        pass

try:
    from response_enhancer import ResponseEnhancer
except ImportError:
    class ResponseEnhancer:
        pass

logger = logging.getLogger(__name__)

def get_daily_briefing_prompt(agent_name: str, market_summary: dict, new_listings: list, new_leads: list):
    """Generates a prompt for a daily agent briefing."""

    # Format the data for the prompt
    listings_str = "\n".join([f"- {l['bedrooms']}BR {l['type']} in {l['area']} for AED {l['price']}" for l in new_listings])
    leads_str = "\n".join([f"- {lead['name']}, interested in {lead['interest']}" for lead in new_leads])

    prompt = f"""
You are "MarketPulse AI," an elite real estate analyst. Your task is to generate a personalized morning briefing for a top-performing Dubai real estate agent.

**Agent Name:** {agent_name}
**Date:** {datetime.now().strftime('%A, %B %d, %Y')}

**Tone:** Professional, data-first, concise, and highly scannable. Use emojis to delineate sections.

**Instructions:**
Based on the provided real-time data, create a morning briefing with the following strict structure.

---
**[REAL-TIME DATA INPUT]**

**Market Summary:**
- Overall Market Trend: {market_summary['trend']}
- Average Price Change (24h): {market_summary['price_change_pct']}%
- Hotspot Area of the Day: {market_summary['hotspot_area']}

**New Listings in Your Sector:**
{listings_str}

**New Leads Assigned to You:**
{leads_str}

---
**[END OF DATA INPUT]**

**[GENERATION TASK]**

Generate the briefing now. Follow this format exactly:

###  Morning Briefing: {agent_name}

**📈 Market Snapshot**
- A 1-2 sentence summary of today's market pulse based on the data.

**🔑 New Key Listings**
- A bulleted list of the most important new listings. Rephrase them professionally.

**👤 New Client Opportunities**
- A bulleted list of new leads. Highlight what makes each one a key opportunity.

**✅ Your Top 3 Priorities Today**
- Based on all the data, generate three specific, actionable priorities for the agent. For example: "Follow up with [Lead Name] regarding the new listing in [Area]" or "Analyze the price drop in [Area] for potential client outreach."
"""
    return prompt


def get_social_media_prompt(platform: str, topic: str, key_points: list, audience: str, call_to_action: str):
    """Generates a prompt for social media content creation."""
    
    points_str = "\n".join([f"- {point}" for point in key_points])
    
    prompt = f"""
You are "RealtyScribe AI," a Dubai real estate social media expert. Create engaging, platform-optimized content.

**Platform:** {platform}
**Topic:** {topic}
**Key Points:** {points_str}
**Target Audience:** {audience}
**Call to Action:** {call_to_action}

**Tone:** Engaging, professional, with Dubai real estate expertise. Use relevant hashtags and emojis.

**Instructions:**
Create a social media post optimized for {platform} that includes:
- Compelling headline/hook
- Key property highlights
- Dubai market context
- Relevant hashtags
- Clear call to action
- Platform-specific formatting

**Format:** Return only the post content, ready to publish.
"""
    return prompt


def get_email_prompt(client_name: str, client_context: str, email_goal: str, listings_to_mention: list):
    """Generates a prompt for follow-up email creation."""
    
    listings_str = "\n".join([f"- {listing}" for listing in listings_to_mention]) if listings_to_mention else "None specified"
    
    prompt = f"""
You are "AgentAssist AI," a Dubai real estate communication specialist. Draft a personalized follow-up email.

**Client Name:** {client_name}
**Client Context:** {client_context}
**Email Goal:** {email_goal}
**Listings to Mention:** {listings_str}

**Tone:** Warm, professional, Dubai-focused. Show understanding of local market.

**Instructions:**
Create a personalized email that:
- Addresses the client by name
- References their specific context
- Achieves the stated goal
- Mentions relevant listings if provided
- Includes Dubai market insights
- Has a clear next step

**Format:** Professional email with subject line and body.
"""
    return prompt


def get_market_report_prompt(neighborhood: str, property_type: str, time_period: str, market_data: dict):
    """Generates a prompt for market report creation."""
    
    prompt = f"""
You are "Dubai Data Insights," a RERA-certified market analyst. Create a comprehensive market report.

**Neighborhood:** {neighborhood}
**Property Type:** {property_type}
**Time Period:** {time_period}
**Market Data:** {json.dumps(market_data, indent=2)}

**Tone:** Formal, analytical, data-driven. Dubai real estate expertise.

**Instructions:**
Generate a professional market report including:
- Executive summary
- Market trends analysis
- Price movement insights
- Supply and demand factors
- Future outlook
- Recommendations

**Format:** Structured report with clear sections and data visualization suggestions.
"""
    return prompt


def get_property_brochure_prompt(property_details: dict):
    """Generates a prompt for luxury property brochure creation."""
    
    prompt = f"""
You are "LuxeNarratives," a luxury real estate copywriter specializing in Dubai's premium market.

**Property Details:** {json.dumps(property_details, indent=2)}

**Tone:** Aspirational, sophisticated, luxury-focused. Dubai premium real estate expertise.

**Instructions:**
Create a compelling property brochure that includes:
- Luxury headline and tagline
- Property highlights and features
- Lifestyle benefits
- Location advantages
- Investment potential
- Professional photography suggestions
- Contact information section

**Format:** Professional brochure layout with sections for different aspects of the property.
"""
    return prompt


def get_cma_prompt(subject_property: dict, comparable_properties: list):
    """Generates a prompt for Comparative Market Analysis creation."""
    
    comps_str = "\n".join([f"- {json.dumps(comp, indent=2)}" for comp in comparable_properties])
    
    prompt = f"""
You are a "RERA-Certified Valuator," a Dubai property valuation expert. Create a professional CMA report.

**Subject Property:** {json.dumps(subject_property, indent=2)}

**Comparable Properties:** {comps_str}

**Tone:** Objective, data-driven, professional. RERA compliance focus.

**Instructions:**
Generate a comprehensive CMA report including:
- Property overview
- Market analysis
- Comparable property analysis
- Valuation methodology
- Price range recommendation
- Market positioning
- Risk factors

**Format:** Professional valuation report with clear sections and supporting data.
"""
    return prompt

class AIEnhancementManager:
    """Main manager for all AI enhancements"""
    
    def __init__(self, db_url: str, model):
        self.db_url = db_url
        self.engine = create_engine(db_url)
        self.model = model
        self.response_enhancer = ResponseEnhancer(model)
        
        # Cache for conversation memories
        self.memory_cache = {}
        
        # Dubai real estate knowledge base (from enhanced version)
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
                           session_id: str,
                           role: str,
                           file_upload: Optional[Dict] = None) -> Dict[str, Any]:
        """Process a complete chat request with all enhancements"""
        
        try:
            # Get or create conversation memory
            memory = self._get_conversation_memory(session_id)
            
            # Add user message to memory
            message_type = MessageType.DOCUMENT if file_upload else MessageType.TEXT
            memory.add_message('user', message, message_type, file_upload)
            
            # Process file upload if present
            file_analysis = None
            if file_upload:
                file_analysis = self._process_file_upload(file_upload)
            
            # Analyze query
            conversation_history = list(memory.messages)
            query_understanding = QueryUnderstanding.analyze(message, conversation_history)
            
            # Get user preferences
            user_preferences = memory.get_user_preferences()
            
            # Get conversation context
            recent_context = memory.get_recent_context(10)
            
            # Use enhanced response generation
            query_analysis = self._analyze_query(message)
            base_response = self._generate_enhanced_response(message, query_analysis)
            
            # Enhance response
            enhanced_response = self.response_enhancer.enhance_response(
                base_response=base_response,
                query_understanding=query_understanding,
                user_preferences=user_preferences,
                conversation_history=recent_context
            )
            
            # Add AI response to memory
            memory.add_message('assistant', enhanced_response, MessageType.TEXT)
            
            # Update memory cache
            self.memory_cache[session_id] = memory
            
            return {
                'response': enhanced_response,
                'query_analysis': query_analysis,
                'user_preferences': user_preferences,
                'file_analysis': file_analysis,
                'conversation_id': memory.conversation_id
            }
            
        except Exception as e:
            logger.error(f"Error in AI enhancement manager: {e}")
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
                'conversation_id': None
            }
    
    def _get_conversation_memory(self, session_id: str) -> ConversationMemory:
        """Get or create conversation memory for a session"""
        if session_id in self.memory_cache:
            return self.memory_cache[session_id]
        
        # Try to load from database
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT id FROM conversations 
                    WHERE session_id = :session_id AND is_active = TRUE
                """), {"session_id": session_id})
                row = result.fetchone()
                
                memory = ConversationMemory(session_id=session_id)
                if row:
                    memory.conversation_id = row[0]
                    
                    # Load recent messages
                    messages_result = conn.execute(text("""
                        SELECT role, content, message_type, metadata, timestamp
                        FROM messages 
                        WHERE conversation_id = :conversation_id
                        ORDER BY timestamp DESC 
                        LIMIT 20
                    """), {"conversation_id": row[0]})
                    
                    for msg_row in messages_result:
                        memory.add_message(
                            role=msg_row[0],
                            content=msg_row[1],
                            message_type=MessageType(msg_row[2]),
                            metadata=json.loads(msg_row[3]) if msg_row[3] else None
                        )
                
                self.memory_cache[session_id] = memory
                return memory
                
        except Exception as e:
            logger.error(f"Error loading conversation memory: {e}")
            memory = ConversationMemory(session_id=session_id)
            self.memory_cache[session_id] = memory
            return memory
    
    def _process_file_upload(self, file_upload: Dict) -> Optional[Dict]:
        """Process file upload for analysis"""
        try:
            file_type = file_upload.get('content_type', '')
            
            if file_type.startswith('image/'):
                # For now, return basic image analysis
                return {
                    "file_type": "image",
                    "analysis": "Image uploaded for property analysis",
                    "supported": True
                }
            
            elif file_type in ['application/pdf', 'text/plain', 'application/msword']:
                # For now, return basic document analysis
                return {
                    "file_type": "document",
                    "analysis": "Document uploaded for analysis",
                    "supported": True
                }
            
            else:
                return {
                    "error": f"Unsupported file type: {file_type}",
                    "supported_types": ["image/*", "application/pdf", "text/plain", "application/msword"]
                }
                
        except Exception as e:
            logger.error(f"Error processing file upload: {e}")
            return {"error": str(e)}
    
    def _create_enhanced_prompt(self,
                               message: str,
                               query_understanding: QueryUnderstanding,
                               user_preferences: Dict[str, Any],
                               conversation_history: List[Dict],
                               file_analysis: Optional[Dict] = None) -> str:
        """Create an enhanced prompt using the improved RAG service method"""
        
        try:
            # Use the improved RAG service to get context and create improved prompt
            from rag_service import ImprovedRAGService, QueryIntent, QueryAnalysis
            
            # Create a temporary RAG service instance for this request
            rag_service = ImprovedRAGService(
                db_url=self.db_url,
                chroma_host=os.getenv("CHROMA_HOST", "localhost"),
                chroma_port=int(os.getenv("CHROMA_PORT", "8000"))
            )
            
            # Analyze the query
            analysis = rag_service.analyze_query(message)
            
            # Get relevant context
            context_items = rag_service.get_relevant_context(message, analysis, max_items=5)
            
            # Build context string
            context = rag_service.build_context_string(context_items)
            
            # Create improved prompt using the new method
            improved_prompt = rag_service.create_improved_prompt(
                query=message,
                analysis=analysis,
                context=context,
                user_role="agent"  # Default role, can be enhanced later
            )
            
            return improved_prompt
            
        except Exception as e:
            logger.error(f"Error creating improved prompt: {e}")
            # Fallback to original prompt creation
            return self._create_fallback_prompt(message, query_understanding, user_preferences, conversation_history, file_analysis)
    
    def _create_fallback_prompt(self,
                               message: str,
                               query_understanding: QueryUnderstanding,
                               user_preferences: Dict[str, Any],
                               conversation_history: List[Dict],
                               file_analysis: Optional[Dict] = None) -> str:
        """Enhanced prompt creation method with specific Dubai real estate context"""
        
        prompt_parts = []
        
        # Enhanced system context with specific Dubai real estate expertise
        prompt_parts.append("""
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

RESPONSE FORMAT:
**Direct Answer** (1-2 sentences)
**Key Data Points** (bullet points with specific numbers)
**Market Context** (current trends and conditions)
**Recommendations** (specific actionable steps)
**Next Steps** (what the user should do next)
        """)
        
        # Add conversation context if available
        if conversation_history:
            recent_context = "\n".join([
                f"{msg.get('role', 'user')}: {msg.get('content', '')[:100]}..."
                for msg in conversation_history[-3:]  # Last 3 messages
            ])
            prompt_parts.append(f"RECENT CONVERSATION CONTEXT:\n{recent_context}")
        
        # Current query with enhanced context
        prompt_parts.append(f"""
CURRENT USER QUERY: {message}

IMPORTANT: Provide specific Dubai real estate information, actual prices, and actionable recommendations. Avoid generic responses.
        """)
        
        return "\n\n".join(prompt_parts)
    
    def get_conversation_summary(self, session_id: str) -> Dict[str, Any]:
        """Get a summary of the conversation for a session"""
        try:
            memory = self._get_conversation_memory(session_id)
            
            # Extract key information from conversation
            user_messages = [msg for msg in memory.messages if msg['role'] == 'user']
            assistant_messages = [msg for msg in memory.messages if msg['role'] == 'assistant']
            
            # Get user preferences
            user_preferences = memory.get_user_preferences()
            
            # Analyze conversation topics
            topics = self._extract_conversation_topics(memory.messages)
            
            return {
                'session_id': session_id,
                'conversation_id': memory.conversation_id,
                'message_count': len(memory.messages),
                'user_messages': len(user_messages),
                'assistant_messages': len(assistant_messages),
                'user_preferences': user_preferences,
                'topics': topics,
                'last_updated': memory.last_updated.isoformat(),
                'duration': self._calculate_conversation_duration(memory.messages)
            }
            
        except Exception as e:
            logger.error(f"Error getting conversation summary: {e}")
            return {
                'session_id': session_id,
                'error': str(e)
            }
    
    def _extract_conversation_topics(self, messages: List[Dict]) -> List[str]:
        """Extract main topics from conversation"""
        topics = []
        all_content = " ".join([msg['content'].lower() for msg in messages])
        
        topic_keywords = {
            'property_search': ['property', 'apartment', 'villa', 'house', 'buy', 'rent', 'search'],
            'investment': ['investment', 'roi', 'return', 'profit', 'yield', 'golden visa'],
            'market_analysis': ['market', 'trend', 'price', 'analysis', 'forecast'],
            'legal_questions': ['legal', 'regulation', 'rera', 'law', 'documentation'],
            'area_information': ['area', 'neighborhood', 'location', 'amenities', 'schools'],
            'financing': ['mortgage', 'financing', 'payment', 'budget', 'loan']
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in all_content for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _calculate_conversation_duration(self, messages: List[Dict]) -> str:
        """Calculate the duration of the conversation"""
        if len(messages) < 2:
            return "0 minutes"
        
        try:
            first_message = messages[0]
            last_message = messages[-1]
            
            first_time = datetime.fromisoformat(first_message['timestamp'])
            last_time = datetime.fromisoformat(last_message['timestamp'])
            
            duration = last_time - first_time
            minutes = int(duration.total_seconds() / 60)
            
            if minutes < 60:
                return f"{minutes} minutes"
            else:
                hours = minutes // 60
                remaining_minutes = minutes % 60
                return f"{hours} hours {remaining_minutes} minutes"
                
        except Exception:
            return "Unknown duration"
    
    def clear_conversation_memory(self, session_id: str) -> bool:
        """Clear conversation memory for a session"""
        try:
            if session_id in self.memory_cache:
                del self.memory_cache[session_id]
            return True
        except Exception as e:
            logger.error(f"Error clearing conversation memory: {e}")
            return False
    
    def get_user_insights(self, session_id: str) -> Dict[str, Any]:
        """Get insights about the user based on conversation history"""
        try:
            memory = self._get_conversation_memory(session_id)
            user_preferences = memory.get_user_preferences()
            
            # Analyze user behavior
            user_messages = [msg for msg in memory.messages if msg['role'] == 'user']
            
            insights = {
                'preferences': user_preferences,
                'engagement_level': self._calculate_engagement_level(user_messages),
                'primary_interests': self._identify_primary_interests(user_messages),
                'urgency_pattern': self._analyze_urgency_pattern(user_messages),
                'complexity_preference': self._analyze_complexity_preference(user_messages)
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Error getting user insights: {e}")
            return {'error': str(e)}
    
    def _calculate_engagement_level(self, user_messages: List[Dict]) -> str:
        """Calculate user engagement level"""
        if not user_messages:
            return "new_user"
        
        avg_message_length = sum(len(msg['content']) for msg in user_messages) / len(user_messages)
        
        if avg_message_length > 100:
            return "highly_engaged"
        elif avg_message_length > 50:
            return "engaged"
        else:
            return "casual"
    
    def _identify_primary_interests(self, user_messages: List[Dict]) -> List[str]:
        """Identify user's primary interests"""
        interests = []
        all_content = " ".join([msg['content'].lower() for msg in user_messages])
        
        interest_patterns = {
            'investment': ['investment', 'roi', 'return', 'profit', 'golden visa'],
            'family_living': ['family', 'schools', 'children', 'kids', 'playground'],
            'luxury': ['luxury', 'premium', 'high-end', 'exclusive', 'penthouse'],
            'budget_conscious': ['budget', 'affordable', 'cheap', 'economical'],
            'location_focused': ['location', 'area', 'neighborhood', 'community']
        }
        
        for interest, keywords in interest_patterns.items():
            if any(keyword in all_content for keyword in keywords):
                interests.append(interest)
        
        return interests
    
    def _analyze_urgency_pattern(self, user_messages: List[Dict]) -> str:
        """Analyze user's urgency pattern"""
        urgent_keywords = ['urgent', 'asap', 'immediately', 'quick', 'fast', 'now', 'soon']
        
        urgent_count = 0
        for msg in user_messages:
            if any(keyword in msg['content'].lower() for keyword in urgent_keywords):
                urgent_count += 1
        
        if urgent_count > len(user_messages) * 0.5:
            return "high_urgency"
        elif urgent_count > 0:
            return "moderate_urgency"
        else:
            return "low_urgency"
    
    def _analyze_complexity_preference(self, user_messages: List[Dict]) -> str:
        """Analyze user's complexity preference"""
        complex_keywords = ['detailed', 'explain', 'how', 'what', 'why', 'process', 'requirements']
        simple_keywords = ['simple', 'basic', 'overview', 'summary']
        
        complex_count = sum(1 for msg in user_messages 
                          if any(keyword in msg['content'].lower() for keyword in complex_keywords))
        simple_count = sum(1 for msg in user_messages 
                          if any(keyword in msg['content'].lower() for keyword in simple_keywords))
        
        if complex_count > simple_count:
            return "detailed_explanations"
        elif simple_count > complex_count:
            return "simple_overviews"
        else:
            return "balanced"
    
    def generate_daily_briefing_for_agent(self, agent_id: int) -> str:
        """Generate daily briefing for a specific agent"""
        try:
            # Fetch data for the agent
            stale_leads = self._get_stale_leads(agent_id)
            recent_viewings = self._get_recent_viewings(agent_id)
            todays_meetings = self._get_todays_meetings(agent_id)
            
            # Construct prompt for Gemini
            prompt = self._create_daily_briefing_prompt(stale_leads, recent_viewings, todays_meetings)
            
            # Generate response using Gemini
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                logger.error(f"Error generating daily briefing: {e}")
                return "No priority actions today. A good day to prospect for new leads!"
                
        except Exception as e:
            logger.error(f"Error in generate_daily_briefing_for_agent: {e}")
            return "Unable to generate daily briefing at this time."
    
    def _get_stale_leads(self, agent_id: int) -> List[Dict]:
        """Get leads not contacted in the last 3 days"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT name, email, phone, status, last_contacted, notes
                    FROM leads 
                    WHERE agent_id = :agent_id 
                    AND (last_contacted IS NULL OR last_contacted < NOW() - INTERVAL '3 days')
                    AND status IN ('new', 'contacted', 'qualified')
                    ORDER BY last_contacted ASC NULLS FIRST
                """), {"agent_id": agent_id})
                
                return [dict(row._mapping) for row in result.fetchall()]
        except Exception as e:
            logger.error(f"Error fetching stale leads: {e}")
            return []
    
    def _get_recent_viewings(self, agent_id: int) -> List[Dict]:
        """Get viewings that occurred yesterday, requiring follow-up"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT client_name, property_address, viewing_time, client_feedback
                    FROM viewings 
                    WHERE agent_id = :agent_id 
                    AND viewing_date = CURRENT_DATE - 1
                    AND follow_up_required = TRUE
                    ORDER BY viewing_time ASC
                """), {"agent_id": agent_id})
                
                return [dict(row._mapping) for row in result.fetchall()]
        except Exception as e:
            logger.error(f"Error fetching recent viewings: {e}")
            return []
    
    def _get_todays_meetings(self, agent_id: int) -> List[Dict]:
        """Get appointments scheduled for the current day"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT client_name, appointment_time, appointment_type, notes
                    FROM appointments 
                    WHERE agent_id = :agent_id 
                    AND appointment_date = CURRENT_DATE
                    AND status = 'scheduled'
                    ORDER BY appointment_time ASC
                """), {"agent_id": agent_id})
                
                return [dict(row._mapping) for row in result.fetchall()]
        except Exception as e:
            logger.error(f"Error fetching today's meetings: {e}")
            return []
    
    def _create_daily_briefing_prompt(self, stale_leads: List[Dict], recent_viewings: List[Dict], todays_meetings: List[Dict]) -> str:
        """Create a detailed prompt for the daily briefing"""
        
        prompt_parts = []
        
        # System context
        prompt_parts.append("""
You are an expert real estate sales coach in Dubai. Generate a concise, actionable daily briefing for a real estate agent.

FORMAT REQUIREMENTS:
- Start with a motivational greeting
- Use clear sections with headers
- Provide specific, actionable next steps
- Keep each section under 100 words
- End with a positive, encouraging message

TONE: Professional, motivating, and action-oriented
        """)
        
        # Stale leads section
        if stale_leads:
            leads_text = "\n".join([
                f"- {lead['name']} ({lead['status']}): {lead.get('notes', 'No notes')}"
                for lead in stale_leads
            ])
            prompt_parts.append(f"""
STALE LEADS (Not contacted in 3+ days):
{leads_text}

Provide specific follow-up strategies for each lead.
            """)
        else:
            prompt_parts.append("STALE LEADS: No stale leads found - great job staying on top of follow-ups!")
        
        # Recent viewings section
        if recent_viewings:
            viewings_text = "\n".join([
                f"- {viewing['client_name']} at {viewing['property_address']}: {viewing.get('client_feedback', 'No feedback')}"
                for viewing in recent_viewings
            ])
            prompt_parts.append(f"""
YESTERDAY'S VIEWINGS (Requiring follow-up):
{viewings_text}

Suggest specific follow-up messages based on client feedback.
            """)
        else:
            prompt_parts.append("YESTERDAY'S VIEWINGS: No viewings yesterday requiring follow-up.")
        
        # Today's meetings section
        if todays_meetings:
            meetings_text = "\n".join([
                f"- {meeting['appointment_time']}: {meeting['client_name']} ({meeting['appointment_type']}) - {meeting.get('notes', 'No notes')}"
                for meeting in todays_meetings
            ])
            prompt_parts.append(f"""
TODAY'S MEETINGS:
{meetings_text}

Provide preparation tips for each meeting.
            """)
        else:
            prompt_parts.append("TODAY'S MEETINGS: No meetings scheduled for today.")
        
        return "\n\n".join(prompt_parts)
    
    def handle_content_generation_command(self, command: str, intent: str, agent_id: int) -> str:
        """Handle content generation commands based on intent"""
        try:
            if intent == 'create_instagram_post':
                return self._generate_instagram_post(command, agent_id)
            elif intent == 'draft_follow_up_email':
                return self._generate_follow_up_email(command, agent_id)
            elif intent == 'generate_whatsapp_broadcast':
                return self._generate_whatsapp_broadcast(command, agent_id)
            else:
                return f"Unsupported content generation command: {intent}"
                
        except Exception as e:
            logger.error(f"Error in handle_content_generation_command: {e}")
            return "I'm having trouble generating content right now. Please try again."
    
    def _generate_instagram_post(self, command: str, agent_id: int) -> str:
        """Generate Instagram post for a property"""
        try:
            # Parse command to extract property ID and target audience
            import re
            property_match = re.search(r'property\s*#?(\d+)', command, re.IGNORECASE)
            audience_match = re.search(r'targeting\s+(.+)', command, re.IGNORECASE)
            
            if not property_match:
                return "Please specify a property ID (e.g., 'property #123')"
            
            property_id = int(property_match.group(1))
            target_audience = audience_match.group(1) if audience_match else "general audience"
            
            # Get property details
            property_details = self._get_property_details(property_id)
            if not property_details:
                return f"Property #{property_id} not found in the database."
            
            # Create prompt for Instagram post
            prompt = f"""
You are a social media expert for Dubai real estate. Create a compelling Instagram post for this property:

PROPERTY DETAILS:
- Address: {property_details['address']}
- Price: AED {property_details['price']:,}
- Type: {property_details['property_type']}
- Bedrooms: {property_details['bedrooms']}
- Bathrooms: {property_details['bathrooms']}
- Size: {property_details['square_feet']} sq ft
- Description: {property_details['description']}

TARGET AUDIENCE: {target_audience}

REQUIREMENTS:
- Create an engaging caption (max 2200 characters)
- Include relevant hashtags (max 30)
- Add a compelling call-to-action
- Make it Dubai-specific and luxury-focused
- Use emojis appropriately

FORMAT: Return the caption and hashtags in a clear, structured format.
            """
            
            # Generate content
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating Instagram post: {e}")
            return "Unable to generate Instagram post. Please check the property ID and try again."
    
    def _generate_follow_up_email(self, command: str, agent_id: int) -> str:
        """Generate follow-up email for a client"""
        try:
            # Parse command to extract client and property details
            import re
            client_match = re.search(r'client\s+(.+)', command, re.IGNORECASE)
            property_match = re.search(r'property\s*#?(\d+)', command, re.IGNORECASE)
            
            if not client_match:
                return "Please specify a client name (e.g., 'client Sarah Johnson')"
            
            client_name = client_match.group(1).strip()
            property_id = None
            if property_match:
                property_id = int(property_match.group(1))
            
            # Get client details
            client_details = self._get_client_details(client_name, agent_id)
            if not client_details:
                return f"Client '{client_name}' not found in your leads."
            
            # Get property details if specified
            property_details = None
            if property_id:
                property_details = self._get_property_details(property_id)
            
            # Create prompt for follow-up email
            prompt = f"""
You are a professional real estate agent in Dubai. Write a personalized follow-up email for this client:

CLIENT DETAILS:
- Name: {client_details['name']}
- Email: {client_details['email']}
- Budget: AED {client_details['budget_min']:,} - {client_details['budget_max']:,}
- Preferred Areas: {client_details['preferred_areas']}
- Property Type: {client_details['property_type']}
- Notes: {client_details.get('notes', 'No notes')}

{f"PROPERTY DETAILS: {property_details['address']} - AED {property_details['price']:,}" if property_details else "PROPERTY: Not specified"}

REQUIREMENTS:
- Professional and friendly tone
- Reference their specific preferences
- Include a clear call-to-action
- Keep it concise (max 200 words)
- Add your contact information

FORMAT: Return a complete email with subject line and body.
            """
            
            # Generate content
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating follow-up email: {e}")
            return "Unable to generate follow-up email. Please check the client name and try again."
    
    def _generate_whatsapp_broadcast(self, command: str, agent_id: int) -> str:
        """Generate WhatsApp broadcast message"""
        try:
            # Parse command to extract target audience and message type
            import re
            audience_match = re.search(r'for\s+(.+)', command, re.IGNORECASE)
            message_type_match = re.search(r'about\s+(.+)', command, re.IGNORECASE)
            
            target_audience = audience_match.group(1).strip() if audience_match else "all clients"
            message_type = message_type_match.group(1).strip() if message_type_match else "general update"
            
            # Create prompt for WhatsApp broadcast
            prompt = f"""
You are a real estate agent in Dubai. Create a WhatsApp broadcast message for your clients:

TARGET AUDIENCE: {target_audience}
MESSAGE TYPE: {message_type}

REQUIREMENTS:
- Keep it under 500 characters
- Use WhatsApp-friendly formatting
- Include relevant emojis
- Make it personal and engaging
- Add a clear call-to-action
- Include your contact information

FORMAT: Return the complete message ready to send.
            """
            
            # Generate content
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating WhatsApp broadcast: {e}")
            return "Unable to generate WhatsApp broadcast. Please try again."
    
    def _get_property_details(self, property_id: int) -> Optional[Dict]:
        """Get property details by ID"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT address, price, bedrooms, bathrooms, square_feet, property_type, description
                    FROM properties 
                    WHERE id = :property_id
                """), {"property_id": property_id})
                
                row = result.fetchone()
                return dict(row._mapping) if row else None
        except Exception as e:
            logger.error(f"Error fetching property details: {e}")
            return None
    
    def _get_client_details(self, client_name: str, agent_id: int) -> Optional[Dict]:
        """Get client details by name and agent ID"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT name, email, phone, budget_min, budget_max, preferred_areas, property_type, notes
                    FROM leads 
                    WHERE agent_id = :agent_id 
                    AND LOWER(name) LIKE LOWER(:client_name)
                """), {"agent_id": agent_id, "client_name": f"%{client_name}%"})
                
                row = result.fetchone()
                return dict(row._mapping) if row else None
        except Exception as e:
            logger.error(f"Error fetching client details: {e}")
            return None

    # ============================================================================
    # CONTENT GENERATION FUNCTIONS
    # ============================================================================

    def generate_daily_briefing(self, agent_name: str, market_summary: dict, new_listings: list, new_leads: list) -> str:
        """Generate a daily briefing for a real estate agent"""
        try:
            # Create the specialized prompt
            prompt = get_daily_briefing_prompt(agent_name, market_summary, new_listings, new_leads)
            
            # Generate content using the AI model
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating daily briefing: {e}")
            return "Unable to generate daily briefing at this time."

    def generate_social_media_post(self, platform: str, topic: str, key_points: list, audience: str, call_to_action: str) -> str:
        """Generate a social media post for the specified platform"""
        try:
            # Create the specialized prompt
            prompt = get_social_media_prompt(platform, topic, key_points, audience, call_to_action)
            
            # Generate content using the AI model
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating social media post: {e}")
            return "Unable to generate social media post at this time."

    def draft_follow_up_email(self, client_name: str, client_context: str, email_goal: str, listings_to_mention: list = None) -> str:
        """Draft a personalized follow-up email for a client"""
        try:
            # Create the specialized prompt
            prompt = get_email_prompt(client_name, client_context, email_goal, listings_to_mention)
            
            # Generate content using the AI model
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error drafting follow-up email: {e}")
            return "Unable to draft follow-up email at this time."

    def generate_market_report(self, neighborhood: str, property_type: str, time_period: str, market_data: dict) -> str:
        """Generate a detailed market report for a specific neighborhood"""
        try:
            # Create the specialized prompt
            prompt = get_market_report_prompt(neighborhood, property_type, time_period, market_data)
            
            # Generate content using the AI model
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating market report: {e}")
            return "Unable to generate market report at this time."

    def build_property_brochure(self, property_details: dict) -> str:
        """Build a persuasive property brochure"""
        try:
            # Create the specialized prompt
            prompt = get_property_brochure_prompt(property_details)
            
            # Generate content using the AI model
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error building property brochure: {e}")
            return "Unable to build property brochure at this time."

    def generate_cma_content(self, subject_property: dict, comparable_properties: list) -> str:
        """Generate Comparative Market Analysis content"""
        try:
            # Create the specialized prompt
            prompt = get_cma_prompt(subject_property, comparable_properties)
            
            # Generate content using the AI model
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating CMA content: {e}")
            return "Unable to generate CMA content at this time."

    def generate_content_by_type(self, content_type: str, **kwargs) -> str:
        """Universal content generation function that routes to the appropriate generator"""
        try:
            if content_type == "daily_briefing":
                return self.generate_daily_briefing(
                    kwargs.get('agent_name'),
                    kwargs.get('market_summary'),
                    kwargs.get('new_listings', []),
                    kwargs.get('new_leads', [])
                )
            elif content_type == "social_media":
                return self.generate_social_media_post(
                    kwargs.get('platform'),
                    kwargs.get('topic'),
                    kwargs.get('key_points', []),
                    kwargs.get('audience'),
                    kwargs.get('call_to_action')
                )
            elif content_type == "follow_up_email":
                return self.draft_follow_up_email(
                    kwargs.get('client_name'),
                    kwargs.get('client_context'),
                    kwargs.get('email_goal'),
                    kwargs.get('listings_to_mention')
                )
            elif content_type == "market_report":
                return self.generate_market_report(
                    kwargs.get('neighborhood'),
                    kwargs.get('property_type'),
                    kwargs.get('time_period'),
                    kwargs.get('market_data', {})
                )
            elif content_type == "property_brochure":
                return self.build_property_brochure(kwargs.get('property_details', {}))
            elif content_type == "cma":
                return self.generate_cma_content(
                    kwargs.get('subject_property', {}),
                    kwargs.get('comparable_properties', [])
                )
            else:
                return f"Unsupported content type: {content_type}"
                
        except Exception as e:
            logger.error(f"Error in generate_content_by_type: {e}")
            return f"Unable to generate {content_type} content at this time."

    def get_available_content_types(self) -> list:
        """Get list of available content generation types"""
        return [
            "daily_briefing",
            "social_media", 
            "follow_up_email",
            "market_report",
            "property_brochure",
            "cma"
        ]
    
    # Blueprint 2.0: HTML Document Generation Methods
    
    def generate_cma_html_document(self, subject_property: dict, comparable_properties: list, agent_id: int) -> Dict[str, Any]:
        """Generate HTML CMA document with preview summary"""
        try:
            from document_generator import DocumentGenerator
            document_generator = DocumentGenerator(self.db_url, self.model)
            return document_generator.generate_cma_html(subject_property, comparable_properties, agent_id)
        except Exception as e:
            logger.error(f"Error generating CMA HTML document: {e}")
            return {"error": f"Unable to generate CMA HTML document: {str(e)}"}
    
    def generate_brochure_html_document(self, property_details: dict, agent_id: int) -> Dict[str, Any]:
        """Generate HTML property brochure with preview summary"""
        try:
            from document_generator import DocumentGenerator
            document_generator = DocumentGenerator(self.db_url, self.model)
            return document_generator.generate_brochure_html(property_details, agent_id)
        except Exception as e:
            logger.error(f"Error generating brochure HTML document: {e}")
            return {"error": f"Unable to generate brochure HTML document: {str(e)}"}
    
    def get_document_preview(self, document_id: int) -> Dict[str, Any]:
        """Get document preview data"""
        try:
            from document_generator import DocumentGenerator
            document_generator = DocumentGenerator(self.db_url, self.model)
            return document_generator.get_document(document_id)
        except Exception as e:
            logger.error(f"Error getting document preview: {e}")
            return {"error": f"Unable to get document preview: {str(e)}"}
    
    # Enhanced AI Response Methods (from ai_manager_enhanced.py)
    
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