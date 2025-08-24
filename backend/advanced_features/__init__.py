"""
Advanced AI-Powered Features and Financial Tools for Real Estate RAG Chat System

This module contains advanced features that will be integrated in future upgrades:
- Predictive Analytics & AI Intelligence
- Financial Calculators & Tools
- Content Generation & Reports

All features are designed to be triggered through natural language intent in the chat interface.
"""

__version__ = "1.0.0"
__author__ = "Real Estate RAG Team"

# Import main feature modules
from .predictive_analytics import PredictiveAnalyticsEngine
from .financial_tools import FinancialCalculatorSuite
from .content_generation import ContentGenerationEngine
from .intent_recognition import IntentRecognitionEngine
from .sentiment_analysis import SentimentAnalyzer

__all__ = [
    'PredictiveAnalyticsEngine',
    'FinancialCalculatorSuite', 
    'ContentGenerationEngine',
    'IntentRecognitionEngine',
    'SentimentAnalyzer'
]