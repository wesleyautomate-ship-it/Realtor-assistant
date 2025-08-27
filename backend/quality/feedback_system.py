"""
Feedback and Quality Improvement System for Dubai Real Estate RAG
===============================================================

This module implements a comprehensive feedback system to continuously improve
response quality and user satisfaction.
"""

import logging
import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

class FeedbackType(Enum):
    """Types of feedback"""
    THUMBS_UP = "thumbs_up"
    THUMBS_DOWN = "thumbs_down"
    RATING = "rating"
    TEXT_FEEDBACK = "text_feedback"
    BUG_REPORT = "bug_report"
    FEATURE_REQUEST = "feature_request"

class FeedbackCategory(Enum):
    """Categories for feedback analysis"""
    ACCURACY = "accuracy"
    RELEVANCE = "relevance"
    COMPLETENESS = "completeness"
    CLARITY = "clarity"
    SPEED = "speed"
    DATA_QUALITY = "data_quality"
    USER_EXPERIENCE = "user_experience"

@dataclass
class FeedbackEntry:
    """Feedback entry with metadata"""
    id: Optional[int] = None
    session_id: str = ""
    user_id: str = ""
    user_role: str = ""
    query: str = ""
    response: str = ""
    feedback_type: FeedbackType = FeedbackType.THUMBS_UP
    rating: Optional[int] = None
    text_feedback: str = ""
    category: FeedbackCategory = FeedbackCategory.ACCURACY
    created_at: datetime = None
    analyzed: bool = False
    improvement_suggestions: List[str] = None
    metadata: Dict[str, Any] = None

class FeedbackSystem:
    """Comprehensive feedback and quality improvement system"""
    
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Feedback analysis cache
        self.feedback_patterns: Dict[str, List[str]] = {}
        self.quality_metrics: Dict[str, float] = {}
        
        # Initialize feedback patterns
        self._initialize_feedback_patterns()
    
    def _initialize_feedback_patterns(self):
        """Initialize common feedback patterns"""
        self.feedback_patterns = {
            "accuracy_issues": [
                "wrong information", "incorrect data", "outdated", "not accurate",
                "false information", "wrong price", "wrong location"
            ],
            "relevance_issues": [
                "not relevant", "off topic", "doesn't answer", "unrelated",
                "not what I asked", "irrelevant information"
            ],
            "completeness_issues": [
                "incomplete", "missing information", "not enough details",
                "partial answer", "need more info", "incomplete response"
            ],
            "clarity_issues": [
                "unclear", "confusing", "hard to understand", "vague",
                "not clear", "ambiguous", "unclear explanation"
            ],
            "speed_issues": [
                "too slow", "slow response", "takes too long", "delayed",
                "response time", "slow system"
            ],
            "data_quality_issues": [
                "poor data", "bad information", "low quality", "unreliable",
                "data issues", "information quality"
            ]
        }
    
    async def submit_feedback(self, feedback: FeedbackEntry) -> bool:
        """Submit user feedback"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO feedback_log (
                        session_id, user_id, user_role, query, response,
                        feedback_type, rating, text_feedback, category,
                        created_at, analyzed, improvement_suggestions, metadata
                    ) VALUES (
                        :session_id, :user_id, :user_role, :query, :response,
                        :feedback_type, :rating, :text_feedback, :category,
                        :created_at, :analyzed, :improvement_suggestions, :metadata
                    )
                """), {
                    "session_id": feedback.session_id,
                    "user_id": feedback.user_id,
                    "user_role": feedback.user_role,
                    "query": feedback.query,
                    "response": feedback.response,
                    "feedback_type": feedback.feedback_type.value,
                    "rating": feedback.rating,
                    "text_feedback": feedback.text_feedback,
                    "category": feedback.category.value,
                    "created_at": feedback.created_at or datetime.now(),
                    "analyzed": feedback.analyzed,
                    "improvement_suggestions": json.dumps(feedback.improvement_suggestions or []),
                    "metadata": json.dumps(feedback.metadata or {})
                })
                conn.commit()
                
            # Analyze feedback for patterns
            await self._analyze_feedback(feedback)
            
            logger.info(f"Feedback submitted for session {feedback.session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error submitting feedback: {e}")
            return False
    
    async def _analyze_feedback(self, feedback: FeedbackEntry) -> List[str]:
        """Analyze feedback for improvement suggestions"""
        try:
            suggestions = []
            
            # Analyze text feedback
            if feedback.text_feedback:
                text_lower = feedback.text_feedback.lower()
                
                # Check for accuracy issues
                if any(pattern in text_lower for pattern in self.feedback_patterns["accuracy_issues"]):
                    suggestions.append("Improve data accuracy and verification")
                    suggestions.append("Update outdated information")
                
                # Check for relevance issues
                if any(pattern in text_lower for pattern in self.feedback_patterns["relevance_issues"]):
                    suggestions.append("Improve query understanding")
                    suggestions.append("Enhance response relevance")
                
                # Check for completeness issues
                if any(pattern in text_lower for pattern in self.feedback_patterns["completeness_issues"]):
                    suggestions.append("Provide more comprehensive responses")
                    suggestions.append("Include additional relevant information")
                
                # Check for clarity issues
                if any(pattern in text_lower for pattern in self.feedback_patterns["clarity_issues"]):
                    suggestions.append("Improve response clarity and structure")
                    suggestions.append("Use simpler language when appropriate")
                
                # Check for speed issues
                if any(pattern in text_lower for pattern in self.feedback_patterns["speed_issues"]):
                    suggestions.append("Optimize response generation speed")
                    suggestions.append("Implement better caching strategies")
                
                # Check for data quality issues
                if any(pattern in text_lower for pattern in self.feedback_patterns["data_quality_issues"]):
                    suggestions.append("Improve data quality and validation")
                    suggestions.append("Enhance data source reliability")
            
            # Analyze rating
            if feedback.rating is not None:
                if feedback.rating <= 2:
                    suggestions.append("Significant improvement needed")
                elif feedback.rating <= 3:
                    suggestions.append("Moderate improvement needed")
                elif feedback.rating >= 4:
                    suggestions.append("Maintain current quality level")
            
            # Update feedback with suggestions
            feedback.improvement_suggestions = suggestions
            feedback.analyzed = True
            
            # Store updated feedback
            await self._update_feedback_analysis(feedback)
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Error analyzing feedback: {e}")
            return []
    
    async def _update_feedback_analysis(self, feedback: FeedbackEntry) -> bool:
        """Update feedback with analysis results"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("""
                    UPDATE feedback_log 
                    SET analyzed = :analyzed, improvement_suggestions = :suggestions
                    WHERE session_id = :session_id AND created_at = :created_at
                """), {
                    "analyzed": feedback.analyzed,
                    "suggestions": json.dumps(feedback.improvement_suggestions or []),
                    "session_id": feedback.session_id,
                    "created_at": feedback.created_at
                })
                conn.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating feedback analysis: {e}")
            return False
    
    async def get_feedback_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get feedback summary for quality analysis"""
        try:
            with self.engine.connect() as conn:
                # Get feedback statistics
                result = conn.execute(text("""
                    SELECT 
                        feedback_type,
                        category,
                        COUNT(*) as count,
                        AVG(rating) as avg_rating
                    FROM feedback_log 
                    WHERE created_at >= :start_date
                    GROUP BY feedback_type, category
                """), {
                    "start_date": datetime.now() - timedelta(days=days)
                })
                
                feedback_stats = {}
                for row in result:
                    feedback_type = row[0]
                    category = row[1]
                    count = row[2]
                    avg_rating = row[3]
                    
                    if feedback_type not in feedback_stats:
                        feedback_stats[feedback_type] = {}
                    
                    feedback_stats[feedback_type][category] = {
                        "count": count,
                        "avg_rating": avg_rating
                    }
                
                # Get recent feedback
                recent_result = conn.execute(text("""
                    SELECT 
                        session_id, user_role, feedback_type, rating, 
                        text_feedback, category, created_at
                    FROM feedback_log 
                    WHERE created_at >= :start_date
                    ORDER BY created_at DESC
                    LIMIT 50
                """), {
                    "start_date": datetime.now() - timedelta(days=days)
                })
                
                recent_feedback = []
                for row in recent_result:
                    recent_feedback.append({
                        "session_id": row[0],
                        "user_role": row[1],
                        "feedback_type": row[2],
                        "rating": row[3],
                        "text_feedback": row[4],
                        "category": row[5],
                        "created_at": str(row[6])
                    })
                
                # Calculate quality metrics
                quality_metrics = self._calculate_quality_metrics(feedback_stats)
                
                return {
                    "period_days": days,
                    "feedback_stats": feedback_stats,
                    "recent_feedback": recent_feedback,
                    "quality_metrics": quality_metrics,
                    "total_feedback": sum(
                        sum(cat["count"] for cat in stats.values())
                        for stats in feedback_stats.values()
                    )
                }
                
        except Exception as e:
            logger.error(f"Error getting feedback summary: {e}")
            return {}
    
    def _calculate_quality_metrics(self, feedback_stats: Dict) -> Dict[str, float]:
        """Calculate quality metrics from feedback"""
        try:
            metrics = {}
            
            # Overall satisfaction rate
            total_feedback = 0
            positive_feedback = 0
            
            for feedback_type, categories in feedback_stats.items():
                for category, data in categories.items():
                    count = data["count"]
                    total_feedback += count
                    
                    if feedback_type == "thumbs_up" or (data["avg_rating"] and data["avg_rating"] >= 4):
                        positive_feedback += count
            
            if total_feedback > 0:
                metrics["satisfaction_rate"] = (positive_feedback / total_feedback) * 100
            else:
                metrics["satisfaction_rate"] = 0
            
            # Category-specific metrics
            for feedback_type, categories in feedback_stats.items():
                for category, data in categories.items():
                    metric_key = f"{category}_{feedback_type}"
                    if data["avg_rating"]:
                        metrics[metric_key] = data["avg_rating"]
                    else:
                        metrics[metric_key] = 0
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating quality metrics: {e}")
            return {}
    
    async def get_improvement_recommendations(self) -> List[Dict[str, Any]]:
        """Get improvement recommendations based on feedback"""
        try:
            with self.engine.connect() as conn:
                # Get common improvement suggestions
                result = conn.execute(text("""
                    SELECT 
                        improvement_suggestions,
                        COUNT(*) as frequency
                    FROM feedback_log 
                    WHERE analyzed = TRUE AND improvement_suggestions IS NOT NULL
                    GROUP BY improvement_suggestions
                    ORDER BY frequency DESC
                    LIMIT 20
                """))
                
                recommendations = []
                for row in result:
                    suggestions = json.loads(row[0]) if row[0] else []
                    frequency = row[1]
                    
                    for suggestion in suggestions:
                        recommendations.append({
                            "suggestion": suggestion,
                            "frequency": frequency,
                            "priority": "high" if frequency > 10 else "medium" if frequency > 5 else "low"
                        })
                
                # Remove duplicates and sort by priority
                unique_recommendations = []
                seen_suggestions = set()
                
                for rec in recommendations:
                    if rec["suggestion"] not in seen_suggestions:
                        unique_recommendations.append(rec)
                        seen_suggestions.add(rec["suggestion"])
                
                # Sort by priority and frequency
                unique_recommendations.sort(
                    key=lambda x: (x["priority"] == "high", x["frequency"]),
                    reverse=True
                )
                
                return unique_recommendations[:10]  # Top 10 recommendations
                
        except Exception as e:
            logger.error(f"Error getting improvement recommendations: {e}")
            return []
    
    async def track_response_quality(self, session_id: str, user_id: str, user_role: str,
                                   query: str, response: str, response_time: float) -> None:
        """Track response quality metrics"""
        try:
            # Calculate quality indicators
            quality_indicators = {
                "response_length": len(response),
                "response_time": response_time,
                "query_complexity": len(query.split()),
                "user_role": user_role,
                "has_sources": "source" in response.lower() or "according" in response.lower(),
                "has_structure": any(marker in response for marker in ["•", "-", "1.", "2.", "**"])
            }
            
            # Store quality metrics
            with self.engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO response_quality_log (
                        session_id, user_id, user_role, query, response,
                        response_time, quality_indicators, created_at
                    ) VALUES (
                        :session_id, :user_id, :user_role, :query, :response,
                        :response_time, :quality_indicators, :created_at
                    )
                """), {
                    "session_id": session_id,
                    "user_id": user_id,
                    "user_role": user_role,
                    "query": query,
                    "response": response,
                    "response_time": response_time,
                    "quality_indicators": json.dumps(quality_indicators),
                    "created_at": datetime.now()
                })
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error tracking response quality: {e}")

# Global feedback system instance
feedback_system = None

def initialize_feedback_system(db_url: str):
    """Initialize the global feedback system"""
    global feedback_system
    feedback_system = FeedbackSystem(db_url)
    logger.info("✅ Feedback System initialized successfully")

def get_feedback_system() -> FeedbackSystem:
    """Get the global feedback system instance"""
    if feedback_system is None:
        raise RuntimeError("Feedback System not initialized. Call initialize_feedback_system() first.")
    return feedback_system
