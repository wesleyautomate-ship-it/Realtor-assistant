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

class AIEnhancementManager:
    """Main manager for all AI enhancements"""
    
    def __init__(self, db_url: str, model):
        self.db_url = db_url
        self.engine = create_engine(db_url)
        self.model = model
        self.response_enhancer = ResponseEnhancer(model)
        
        # Cache for conversation memories
        self.memory_cache = {}
    
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
            
            # Create enhanced prompt
            enhanced_prompt = self._create_enhanced_prompt(
                message=message,
                query_understanding=query_understanding,
                user_preferences=user_preferences,
                conversation_history=recent_context,
                file_analysis=file_analysis
            )
            
            # Generate base response
            try:
                response = self.model.generate_content(enhanced_prompt)
                base_response = response.text
            except Exception as e:
                logger.error(f"Error generating response: {e}")
                base_response = "I'm having trouble processing your request right now. Please try again in a moment."
            
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
                'query_analysis': {
                    'intent': query_understanding.intent,
                    'sentiment': query_understanding.sentiment.value,
                    'urgency_level': query_understanding.urgency_level,
                    'complexity_level': query_understanding.complexity_level,
                    'suggested_actions': query_understanding.suggested_actions,
                    'entities': query_understanding.entities
                },
                'user_preferences': user_preferences,
                'file_analysis': file_analysis,
                'conversation_id': memory.conversation_id
            }
            
        except Exception as e:
            logger.error(f"Error in AI enhancement manager: {e}")
            return {
                'response': "I apologize, but I'm experiencing some technical difficulties. Please try again in a moment.",
                'query_analysis': {
                    'intent': 'general_inquiry',
                    'sentiment': 'neutral',
                    'urgency_level': 1,
                    'complexity_level': 1,
                    'suggested_actions': [],
                    'entities': {}
                },
                'user_preferences': {},
                'file_analysis': None,
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
            from rag_service_improved import ImprovedRAGService, QueryIntent, QueryAnalysis
            
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