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

from ai_enhancements import ConversationMemory, MessageType
from query_understanding import QueryUnderstanding
from response_enhancer import ResponseEnhancer

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
                        SELECT role, content, message_type, metadata, created_at
                        FROM messages 
                        WHERE conversation_id = :conversation_id
                        ORDER BY created_at DESC 
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
        """Fallback prompt creation method"""
        
        prompt_parts = []
        
        # System context
        prompt_parts.append("""
You are an expert Dubai real estate AI assistant. Provide direct, data-driven responses in a professional format.

RESPONSE REQUIREMENTS:
1. Start with direct answer - No conversational fillers
2. Use structured formatting - Headers, bullet points, bold keywords
3. Present specific data - Include actual numbers, prices, percentages
4. Keep under 200 words unless presenting detailed data tables
5. End with actionable next steps specific to the query
        """)
        
        # Current query
        prompt_parts.append(f"USER QUERY: {message}")
        
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
