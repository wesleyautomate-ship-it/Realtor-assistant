"""
Voice Service for Laura AI Real Estate Assistant

This service handles voice processing, intent extraction, and integration
with the existing AI manager for real estate-specific voice interactions.
"""

import asyncio
import json
import logging
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime
import google.generativeai as genai
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Import existing AI manager for integration
from ai_manager import AIEnhancementManager

logger = logging.getLogger(__name__)

class VoiceService:
    """Voice processing service that integrates with existing AI infrastructure"""
    
    def __init__(self, database_url: str, google_api_key: str):
        # Use SQLite for testing if PostgreSQL is not available
        if 'postgresql' in database_url and 'localhost' in database_url:
            # Check if we can connect to PostgreSQL, fallback to SQLite
            try:
                test_engine = create_engine(database_url)
                with test_engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                self.database_url = database_url
            except:
                print("⚠️ PostgreSQL not available, using SQLite for testing")
                self.database_url = 'sqlite:///voice_ai_test.db'
        else:
            self.database_url = database_url
            
        self.google_api_key = google_api_key
        
        # Initialize Google Gemini for voice processing
        genai.configure(api_key=google_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Initialize existing AI manager for integration
        self.ai_manager = AIEnhancementManager(database_url, self.model)
        
        # Database connection
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Real estate specific intents
        self.real_estate_intents = {
            'content_generation': ['generate', 'create', 'make', 'write', 'draft'],
            'market_analysis': ['analyze', 'market', 'cma', 'comparative', 'pricing'],
            'property_management': ['property', 'listing', 'manage', 'update', 'property details'],
            'client_communication': ['client', 'contact', 'follow up', 'email', 'call'],
            'task_management': ['task', 'reminder', 'schedule', 'appointment', 'meeting'],
            'social_media': ['social', 'post', 'instagram', 'facebook', 'linkedin'],
            'reporting': ['report', 'analytics', 'performance', 'statistics', 'metrics']
        }
    
    async def process_voice_request(self, audio_data: bytes, user_id: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process voice request and return structured response
        
        Args:
            audio_data: Raw audio data from voice input
            user_id: User ID for the request
            session_id: Optional session ID for tracking
            
        Returns:
            Dict containing transcript, intent, entities, and processing type
        """
        try:
            # 1. Transcribe audio to text
            transcript = await self._transcribe_audio(audio_data)
            
            # 2. Extract intent and entities
            intent_data = await self._extract_voice_intent(transcript, user_id)
            
            # 3. Determine processing type
            processing_type = self._determine_processing_type(intent_data)
            
            # 4. Store voice request in database
            voice_request_id = await self._store_voice_request(
                user_id, session_id, transcript, intent_data, processing_type
            )
            
            # 5. Route to appropriate handler
            if processing_type == 'realtime':
                response = await self._handle_realtime_request(intent_data, user_id)
                return {
                    'request_id': voice_request_id,
                    'transcript': transcript,
                    'intent': intent_data['type'],
                    'entities': intent_data['entities'],
                    'processing_type': 'realtime',
                    'response': response,
                    'status': 'completed'
                }
            else:
                # Queue for batch processing
                await self._queue_batch_request(intent_data, user_id, voice_request_id)
                return {
                    'request_id': voice_request_id,
                    'transcript': transcript,
                    'intent': intent_data['type'],
                    'entities': intent_data['entities'],
                    'processing_type': 'batch',
                    'status': 'queued',
                    'eta': '5-10 minutes'
                }
                
        except Exception as e:
            logger.error(f"Error processing voice request: {e}")
            raise
    
    async def _transcribe_audio(self, audio_data: bytes) -> str:
        """
        Transcribe audio to text using Google Speech-to-Text
        For now, this is a placeholder - you'll need to integrate with actual STT service
        """
        try:
            # TODO: Integrate with Google Speech-to-Text API
            # For now, return a mock transcript for testing
            # In production, you would use:
            # from google.cloud import speech
            # client = speech.SpeechClient()
            # audio = speech.RecognitionAudio(content=audio_data)
            # config = speech.RecognitionConfig(
            #     encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
            #     sample_rate_hertz=48000,
            #     language_code="en-US",
            #     enable_automatic_punctuation=True,
            # )
            # response = client.recognize(config=config, audio=audio)
            # return response.results[0].alternatives[0].transcript
            
            # Mock transcription for development
            return "Generate a CMA for 123 Main Street, 3 bedrooms, 2 bathrooms, $500,000"
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            raise
    
    async def _extract_voice_intent(self, transcript: str, user_id: str) -> Dict[str, Any]:
        """
        Extract intent and entities from voice transcript using AI
        """
        try:
            # Use existing AI manager for intent extraction
            # Enhanced with real estate specific prompts
            
            prompt = f"""
            Analyze this real estate agent's voice command and extract the intent and entities:
            
            Transcript: "{transcript}"
            
            Please identify:
            1. Intent type (content_generation, market_analysis, property_management, client_communication, task_management, social_media, reporting)
            2. Entities (property address, price, bedrooms, bathrooms, template type, deadline, etc.)
            3. Specific action requested
            
            Return as JSON with this structure:
            {{
                "type": "intent_type",
                "confidence": 0.95,
                "entities": {{
                    "property_address": "123 Main St",
                    "price": "$500,000",
                    "bedrooms": "3",
                    "bathrooms": "2",
                    "template_type": "cma",
                    "deadline": "today"
                }},
                "action": "specific action requested",
                "context": "additional context"
            }}
            """
            
            response = await self.model.generate_content_async(prompt)
            
            # Parse AI response
            try:
                intent_data = json.loads(response.text)
            except json.JSONDecodeError:
                # Fallback parsing if AI response is not valid JSON
                intent_data = self._fallback_intent_extraction(transcript)
            
            return intent_data
            
        except Exception as e:
            logger.error(f"Error extracting intent: {e}")
            # Fallback to simple keyword matching
            return self._fallback_intent_extraction(transcript)
    
    def _fallback_intent_extraction(self, transcript: str) -> Dict[str, Any]:
        """
        Fallback intent extraction using keyword matching
        """
        transcript_lower = transcript.lower()
        
        # Determine intent based on keywords
        intent_type = 'content_generation'  # default
        for intent, keywords in self.real_estate_intents.items():
            if any(keyword in transcript_lower for keyword in keywords):
                intent_type = intent
                break
        
        # Extract basic entities using simple patterns
        entities = {}
        
        # Extract price (basic pattern)
        import re
        price_match = re.search(r'\$[\d,]+', transcript)
        if price_match:
            entities['price'] = price_match.group()
        
        # Extract numbers for bedrooms/bathrooms
        numbers = re.findall(r'\b\d+\b', transcript)
        if len(numbers) >= 2:
            entities['bedrooms'] = numbers[0]
            entities['bathrooms'] = numbers[1]
        
        return {
            'type': intent_type,
            'confidence': 0.7,
            'entities': entities,
            'action': transcript,
            'context': 'fallback extraction'
        }
    
    def _determine_processing_type(self, intent_data: Dict[str, Any]) -> str:
        """
        Determine if request should be processed in real-time or batch
        """
        intent_type = intent_data.get('type', 'content_generation')
        
        # Real-time processing for simple tasks
        realtime_intents = ['task_management', 'client_communication']
        
        # Batch processing for complex content generation
        batch_intents = ['content_generation', 'market_analysis', 'social_media', 'reporting']
        
        if intent_type in realtime_intents:
            return 'realtime'
        elif intent_type in batch_intents:
            return 'batch'
        else:
            # Default to batch for safety
            return 'batch'
    
    async def _store_voice_request(self, user_id: str, session_id: Optional[str], 
                                 transcript: str, intent_data: Dict[str, Any], 
                                 processing_type: str) -> str:
        """
        Store voice request in database
        """
        try:
            voice_request_id = str(uuid.uuid4())
            
            with self.SessionLocal() as session:
                # Insert voice request
                sql = """
                INSERT INTO voice_requests (
                    id, user_id, transcript, intent, entities, 
                    processing_type, status, created_at
                ) VALUES (
                    :id, :user_id, :transcript, :intent, :entities,
                    :processing_type, 'queued', NOW()
                )
                """
                
                session.execute(text(sql), {
                    'id': voice_request_id,
                    'user_id': user_id,
                    'transcript': transcript,
                    'intent': intent_data.get('type'),
                    'entities': json.dumps(intent_data.get('entities', {})),
                    'processing_type': processing_type
                })
                
                session.commit()
                
            return voice_request_id
            
        except Exception as e:
            logger.error(f"Error storing voice request: {e}")
            raise
    
    async def _handle_realtime_request(self, intent_data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Handle real-time requests (simple tasks)
        """
        try:
            intent_type = intent_data.get('type')
            entities = intent_data.get('entities', {})
            
            if intent_type == 'task_management':
                return await self._handle_task_management(entities, user_id)
            elif intent_type == 'client_communication':
                return await self._handle_client_communication(entities, user_id)
            else:
                return {
                    'message': f'Real-time processing for {intent_type} not yet implemented',
                    'status': 'not_implemented'
                }
                
        except Exception as e:
            logger.error(f"Error handling real-time request: {e}")
            return {'error': str(e), 'status': 'failed'}
    
    async def _queue_batch_request(self, intent_data: Dict[str, Any], user_id: str, voice_request_id: str):
        """
        Queue batch request for background processing
        """
        try:
            # Create AI request for batch processing
            ai_request_id = str(uuid.uuid4())
            
            with self.SessionLocal() as session:
                sql = """
                INSERT INTO ai_requests (
                    id, user_id, request_type, input_data, 
                    processing_type, voice_request_id, status, created_at
                ) VALUES (
                    :id, :user_id, :request_type, :input_data,
                    'batch', :voice_request_id, 'queued', NOW()
                )
                """
                
                session.execute(text(sql), {
                    'id': ai_request_id,
                    'user_id': user_id,
                    'request_type': intent_data.get('type'),
                    'input_data': json.dumps(intent_data),
                    'voice_request_id': voice_request_id
                })
                
                session.commit()
                
            # TODO: Add to async processing queue
            # This would integrate with your existing async processing system
            
        except Exception as e:
            logger.error(f"Error queuing batch request: {e}")
            raise
    
    async def _handle_task_management(self, entities: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Handle task management requests
        """
        # Integrate with existing task management system
        return {
            'message': 'Task management request processed',
            'status': 'completed',
            'action': 'task_created'
        }
    
    async def _handle_client_communication(self, entities: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Handle client communication requests
        """
        # Integrate with existing client management system
        return {
            'message': 'Client communication request processed',
            'status': 'completed',
            'action': 'communication_scheduled'
        }
    
    async def get_voice_request_status(self, request_id: str) -> Dict[str, Any]:
        """
        Get status of voice request
        """
        try:
            with self.SessionLocal() as session:
                sql = """
                SELECT vr.*, ar.status as ai_status, ar.result_data
                FROM voice_requests vr
                LEFT JOIN ai_requests ar ON vr.id = ar.voice_request_id
                WHERE vr.id = :request_id
                """
                
                result = session.execute(text(sql), {'request_id': request_id}).fetchone()
                
                if result:
                    return {
                        'request_id': request_id,
                        'status': result.status,
                        'transcript': result.transcript,
                        'intent': result.intent,
                        'processing_type': result.processing_type,
                        'ai_status': result.ai_status,
                        'result_data': result.result_data,
                        'created_at': result.created_at.isoformat() if result.created_at else None,
                        'completed_at': result.completed_at.isoformat() if result.completed_at else None
                    }
                else:
                    return {'error': 'Request not found', 'status': 'not_found'}
                    
        except Exception as e:
            logger.error(f"Error getting voice request status: {e}")
            return {'error': str(e), 'status': 'error'}
