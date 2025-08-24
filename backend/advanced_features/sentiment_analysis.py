"""
Sentiment Analysis Engine for Real Estate RAG Chat System

This module provides advanced sentiment analysis capabilities including:
- Real-time conversation mood detection
- Client emotion analysis
- Response adjustment based on sentiment
- Sentiment tracking and reporting
"""

import logging
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import numpy as np
from textblob import TextBlob
from .config import config

logger = logging.getLogger(__name__)

@dataclass
class SentimentResult:
    """Represents sentiment analysis results"""
    sentiment_score: float  # -1 to 1 (negative to positive)
    sentiment_label: str    # 'positive', 'negative', 'neutral'
    confidence: float       # 0 to 1
    emotions: Dict[str, float]  # Emotion scores
    dominant_emotion: str
    conversation_mood: str
    response_adjustment: str
    timestamp: datetime

@dataclass
class ConversationAnalysis:
    """Represents overall conversation analysis"""
    conversation_id: str
    overall_sentiment: float
    sentiment_trend: str
    key_emotions: List[str]
    engagement_level: str
    urgency_level: str
    satisfaction_score: float
    recommendations: List[str]
    analysis_date: datetime

class SentimentAnalyzer:
    """
    Advanced sentiment analysis engine for real estate conversations
    """
    
    def __init__(self):
        self.emotion_keywords = self._load_emotion_keywords()
        self.response_templates = self._load_response_templates()
        self.conversation_history = {}
        
    def _load_emotion_keywords(self) -> Dict[str, List[str]]:
        """Load emotion keywords for analysis"""
        return {
            'excited': [
                'amazing', 'fantastic', 'excellent', 'perfect', 'love', 'great',
                'wonderful', 'beautiful', 'stunning', 'impressive', 'dream',
                'excited', 'thrilled', 'happy', 'interested', 'wow', 'incredible'
            ],
            'frustrated': [
                'frustrated', 'annoyed', 'upset', 'angry', 'disappointed',
                'unhappy', 'dissatisfied', 'problem', 'issue', 'wrong',
                'bad', 'terrible', 'awful', 'hate', 'dislike', 'complaint'
            ],
            'hesitant': [
                'maybe', 'perhaps', 'not sure', 'unsure', 'doubt', 'concerned',
                'worried', 'anxious', 'nervous', 'cautious', 'careful',
                'think', 'consider', 'might', 'could', 'would', 'if'
            ],
            'interested': [
                'interested', 'curious', 'tell me more', 'explain', 'details',
                'information', 'learn', 'understand', 'show me', 'see',
                'view', 'visit', 'schedule', 'appointment', 'meeting'
            ],
            'urgent': [
                'urgent', 'asap', 'quick', 'immediate', 'soon', 'fast',
                'hurry', 'rush', 'deadline', 'time', 'quickly', 'now',
                'today', 'tomorrow', 'this week', 'immediately'
            ],
            'satisfied': [
                'satisfied', 'happy', 'pleased', 'content', 'good', 'fine',
                'okay', 'alright', 'acceptable', 'suitable', 'perfect',
                'exactly', 'precisely', 'right', 'correct', 'yes'
            ]
        }
    
    def _load_response_templates(self) -> Dict[str, Dict[str, str]]:
        """Load response templates based on sentiment"""
        return {
            'positive': {
                'greeting': "I'm glad you're excited about this! 😊",
                'information': "Great! Let me provide you with detailed information about this property.",
                'suggestion': "Since you're interested, I'd recommend scheduling a viewing to see it in person.",
                'closing': "I'm here to help make your property dreams come true! 🏠✨"
            },
            'negative': {
                'greeting': "I understand your concerns. Let me address them directly.",
                'information': "I want to make sure we find the right property for you. Let me clarify some details.",
                'suggestion': "Would you like to explore other options that might better suit your needs?",
                'closing': "I'm committed to finding the perfect solution for you. Let's work together on this."
            },
            'neutral': {
                'greeting': "Thank you for your inquiry. I'm here to help!",
                'information': "Let me provide you with comprehensive information about this property.",
                'suggestion': "Would you like to know more about this property or explore other options?",
                'closing': "Feel free to ask any questions. I'm here to assist you."
            },
            'frustrated': {
                'greeting': "I apologize for any inconvenience. Let me help resolve this for you.",
                'information': "I understand your frustration. Let me provide clear, accurate information.",
                'suggestion': "Let's work together to find a solution that meets your needs.",
                'closing': "I appreciate your patience. I'm here to help make this right."
            },
            'hesitant': {
                'greeting': "I understand you want to make the right decision. Let me help you with that.",
                'information': "Take your time to review this information. I'm here to answer any questions.",
                'suggestion': "Would you like to explore this further or discuss other options?",
                'closing': "No pressure at all. Take your time, and I'm here when you're ready."
            }
        }
    
    def analyze_sentiment(self, text: str, conversation_context: Dict = None) -> Optional[SentimentResult]:
        """
        Analyze sentiment of a text message
        
        Args:
            text: Text to analyze
            conversation_context: Previous conversation context
            
        Returns:
            SentimentResult object with analysis results
        """
        try:
            if not text or not text.strip():
                return None
            
            # Clean text
            cleaned_text = self._clean_text(text)
            
            # Get basic sentiment using TextBlob
            blob = TextBlob(cleaned_text)
            sentiment_score = blob.sentiment.polarity
            
            # Analyze emotions
            emotions = self._analyze_emotions(cleaned_text)
            dominant_emotion = self._get_dominant_emotion(emotions)
            
            # Determine sentiment label
            sentiment_label = self._classify_sentiment(sentiment_score, emotions)
            
            # Calculate confidence
            confidence = self._calculate_confidence(sentiment_score, emotions)
            
            # Determine conversation mood
            conversation_mood = self._determine_conversation_mood(sentiment_score, emotions, conversation_context)
            
            # Get response adjustment
            response_adjustment = self._get_response_adjustment(sentiment_label, dominant_emotion)
            
            return SentimentResult(
                sentiment_score=sentiment_score,
                sentiment_label=sentiment_label,
                confidence=confidence,
                emotions=emotions,
                dominant_emotion=dominant_emotion,
                conversation_mood=conversation_mood,
                response_adjustment=response_adjustment,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return None
    
    def analyze_conversation(self, conversation_id: str, messages: List[Dict]) -> Optional[ConversationAnalysis]:
        """
        Analyze overall conversation sentiment and trends
        
        Args:
            conversation_id: Unique conversation identifier
            messages: List of conversation messages
            
        Returns:
            ConversationAnalysis object with overall analysis
        """
        try:
            if not messages:
                return None
            
            # Analyze each message
            sentiment_results = []
            for message in messages:
                if message.get('role') == 'user':
                    result = self.analyze_sentiment(message.get('content', ''))
                    if result:
                        sentiment_results.append(result)
            
            if not sentiment_results:
                return None
            
            # Calculate overall sentiment
            overall_sentiment = np.mean([r.sentiment_score for r in sentiment_results])
            
            # Determine sentiment trend
            sentiment_trend = self._determine_sentiment_trend(sentiment_results)
            
            # Get key emotions
            key_emotions = self._get_key_emotions(sentiment_results)
            
            # Calculate engagement level
            engagement_level = self._calculate_engagement_level(messages)
            
            # Calculate urgency level
            urgency_level = self._calculate_urgency_level(sentiment_results)
            
            # Calculate satisfaction score
            satisfaction_score = self._calculate_satisfaction_score(sentiment_results)
            
            # Generate recommendations
            recommendations = self._generate_conversation_recommendations(
                overall_sentiment, key_emotions, engagement_level, urgency_level
            )
            
            return ConversationAnalysis(
                conversation_id=conversation_id,
                overall_sentiment=overall_sentiment,
                sentiment_trend=sentiment_trend,
                key_emotions=key_emotions,
                engagement_level=engagement_level,
                urgency_level=urgency_level,
                satisfaction_score=satisfaction_score,
                recommendations=recommendations,
                analysis_date=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error in conversation analysis: {e}")
            return None
    
    def adjust_response_tone(self, response: str, sentiment_result: SentimentResult) -> str:
        """
        Adjust response tone based on sentiment analysis
        
        Args:
            response: Original response text
            sentiment_result: Sentiment analysis result
            
        Returns:
            Adjusted response with appropriate tone
        """
        try:
            if not sentiment_result:
                return response
            
            # Get appropriate template
            templates = self.response_templates.get(sentiment_result.sentiment_label, {})
            
            # Add sentiment-appropriate prefix/suffix
            adjusted_response = response
            
            # Add greeting based on sentiment
            if templates.get('greeting'):
                adjusted_response = f"{templates['greeting']}\n\n{adjusted_response}"
            
            # Add closing based on sentiment
            if templates.get('closing'):
                adjusted_response = f"{adjusted_response}\n\n{templates['closing']}"
            
            # Add urgency indicators if needed
            if sentiment_result.dominant_emotion == 'urgent':
                adjusted_response = f"🚨 {adjusted_response}"
            
            # Add positive reinforcement for positive sentiment
            if sentiment_result.sentiment_label == 'positive':
                adjusted_response = f"{adjusted_response} ✨"
            
            return adjusted_response
            
        except Exception as e:
            logger.error(f"Error adjusting response tone: {e}")
            return response
    
    def _clean_text(self, text: str) -> str:
        """Clean text for analysis"""
        # Remove special characters but keep emojis
        cleaned = re.sub(r'[^\w\s\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002600-\U000027BF]', ' ', text)
        return cleaned.lower().strip()
    
    def _analyze_emotions(self, text: str) -> Dict[str, float]:
        """Analyze emotions in text"""
        emotions = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text:
                    score += 1
            
            # Normalize score
            emotions[emotion] = min(score / len(keywords), 1.0)
        
        return emotions
    
    def _get_dominant_emotion(self, emotions: Dict[str, float]) -> str:
        """Get the dominant emotion"""
        if not emotions:
            return 'neutral'
        
        max_score = max(emotions.values())
        if max_score == 0:
            return 'neutral'
        
        dominant_emotions = [emotion for emotion, score in emotions.items() if score == max_score]
        return dominant_emotions[0]
    
    def _classify_sentiment(self, sentiment_score: float, emotions: Dict[str, float]) -> str:
        """Classify sentiment based on score and emotions"""
        # Check for specific emotions first
        if emotions.get('frustrated', 0) > 0.3:
            return 'frustrated'
        elif emotions.get('hesitant', 0) > 0.3:
            return 'hesitant'
        elif emotions.get('excited', 0) > 0.3:
            return 'positive'
        elif emotions.get('interested', 0) > 0.3:
            return 'positive'
        
        # Use sentiment score
        if sentiment_score > 0.1:
            return 'positive'
        elif sentiment_score < -0.1:
            return 'negative'
        else:
            return 'neutral'
    
    def _calculate_confidence(self, sentiment_score: float, emotions: Dict[str, float]) -> float:
        """Calculate confidence in sentiment analysis"""
        # Base confidence on sentiment score strength
        base_confidence = abs(sentiment_score)
        
        # Boost confidence if strong emotions detected
        max_emotion = max(emotions.values()) if emotions else 0
        emotion_boost = max_emotion * 0.3
        
        return min(base_confidence + emotion_boost, 1.0)
    
    def _determine_conversation_mood(self, sentiment_score: float, emotions: Dict[str, float], context: Dict = None) -> str:
        """Determine overall conversation mood"""
        if emotions.get('urgent', 0) > 0.3:
            return 'urgent'
        elif emotions.get('excited', 0) > 0.3:
            return 'excited'
        elif emotions.get('frustrated', 0) > 0.3:
            return 'frustrated'
        elif emotions.get('hesitant', 0) > 0.3:
            return 'cautious'
        elif emotions.get('interested', 0) > 0.3:
            return 'engaged'
        elif sentiment_score > 0.1:
            return 'positive'
        elif sentiment_score < -0.1:
            return 'negative'
        else:
            return 'neutral'
    
    def _get_response_adjustment(self, sentiment_label: str, dominant_emotion: str) -> str:
        """Get response adjustment strategy"""
        adjustments = {
            'positive': 'maintain_enthusiasm',
            'negative': 'show_empathy',
            'neutral': 'provide_information',
            'frustrated': 'address_concerns',
            'hesitant': 'build_confidence',
            'excited': 'channel_enthusiasm',
            'interested': 'provide_details',
            'urgent': 'prioritize_speed'
        }
        
        return adjustments.get(sentiment_label, 'provide_information')
    
    def _determine_sentiment_trend(self, sentiment_results: List[SentimentResult]) -> str:
        """Determine sentiment trend over time"""
        if len(sentiment_results) < 2:
            return 'stable'
        
        scores = [r.sentiment_score for r in sentiment_results]
        
        # Calculate trend
        if len(scores) >= 3:
            recent_avg = np.mean(scores[-3:])
            earlier_avg = np.mean(scores[:-3])
            
            if recent_avg > earlier_avg + 0.1:
                return 'improving'
            elif recent_avg < earlier_avg - 0.1:
                return 'declining'
            else:
                return 'stable'
        else:
            return 'stable'
    
    def _get_key_emotions(self, sentiment_results: List[SentimentResult]) -> List[str]:
        """Get key emotions from conversation"""
        emotion_counts = {}
        
        for result in sentiment_results:
            for emotion, score in result.emotions.items():
                if score > 0.2:  # Threshold for significant emotion
                    emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Return top 3 emotions
        sorted_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)
        return [emotion for emotion, count in sorted_emotions[:3]]
    
    def _calculate_engagement_level(self, messages: List[Dict]) -> str:
        """Calculate engagement level from conversation"""
        if not messages:
            return 'low'
        
        # Count user messages
        user_messages = [msg for msg in messages if msg.get('role') == 'user']
        
        # Analyze message length and frequency
        avg_length = np.mean([len(msg.get('content', '')) for msg in user_messages])
        message_count = len(user_messages)
        
        if message_count > 10 and avg_length > 50:
            return 'high'
        elif message_count > 5 and avg_length > 30:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_urgency_level(self, sentiment_results: List[SentimentResult]) -> str:
        """Calculate urgency level from sentiment results"""
        urgency_scores = [r.emotions.get('urgent', 0) for r in sentiment_results]
        max_urgency = max(urgency_scores) if urgency_scores else 0
        
        if max_urgency > 0.5:
            return 'high'
        elif max_urgency > 0.2:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_satisfaction_score(self, sentiment_results: List[SentimentResult]) -> float:
        """Calculate overall satisfaction score"""
        if not sentiment_results:
            return 0.5
        
        # Weight recent sentiments more heavily
        weights = np.linspace(0.5, 1.0, len(sentiment_results))
        weighted_scores = [score * weight for score, weight in zip([r.sentiment_score for r in sentiment_results], weights)]
        
        return np.mean(weighted_scores)
    
    def _generate_conversation_recommendations(self, overall_sentiment: float, key_emotions: List[str], 
                                            engagement_level: str, urgency_level: str) -> List[str]:
        """Generate recommendations based on conversation analysis"""
        recommendations = []
        
        # Sentiment-based recommendations
        if overall_sentiment < -0.2:
            recommendations.append("Address client concerns immediately")
            recommendations.append("Provide additional support and reassurance")
        elif overall_sentiment > 0.2:
            recommendations.append("Maintain positive momentum")
            recommendations.append("Leverage enthusiasm for closing")
        
        # Emotion-based recommendations
        if 'frustrated' in key_emotions:
            recommendations.append("Focus on problem resolution")
            recommendations.append("Provide clear, accurate information")
        
        if 'hesitant' in key_emotions:
            recommendations.append("Build confidence through education")
            recommendations.append("Provide detailed explanations")
        
        if 'urgent' in key_emotions:
            recommendations.append("Prioritize speed and efficiency")
            recommendations.append("Provide immediate solutions")
        
        # Engagement-based recommendations
        if engagement_level == 'low':
            recommendations.append("Increase engagement through questions")
            recommendations.append("Provide more interactive content")
        
        # Urgency-based recommendations
        if urgency_level == 'high':
            recommendations.append("Respond immediately to urgent requests")
            recommendations.append("Provide quick, actionable solutions")
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def get_sentiment_summary(self, conversation_id: str) -> Dict[str, Any]:
        """Get sentiment summary for a conversation"""
        if conversation_id not in self.conversation_history:
            return {}
        
        analysis = self.conversation_history[conversation_id]
        
        return {
            'conversation_id': conversation_id,
            'overall_sentiment': analysis.overall_sentiment,
            'sentiment_trend': analysis.sentiment_trend,
            'key_emotions': analysis.key_emotions,
            'engagement_level': analysis.engagement_level,
            'urgency_level': analysis.urgency_level,
            'satisfaction_score': analysis.satisfaction_score,
            'recommendations': analysis.recommendations,
            'analysis_date': analysis.analysis_date.isoformat()
        }