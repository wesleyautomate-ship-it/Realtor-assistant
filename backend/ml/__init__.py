"""
Dubai Real Estate RAG System - Machine Learning Module

This module provides AI-powered insights including:
- Market trend predictions
- Property valuation AI
- Investment analysis algorithms
- Automated reporting
- Smart notifications

Author: AI Development Team
Version: 1.0.0
Date: September 2025
"""

from .services.prediction_service import PredictionService
from .services.analysis_service import AnalysisService
from .services.optimization_service import OptimizationService
from .services.reporting_service import AutomatedReportingService
from .services.notification_service import SmartNotificationService
from .services.analytics_service import PerformanceAnalyticsService
from .models.market_predictor import MarketPredictor
from .models.property_valuator import PropertyValuator
from .models.investment_analyzer import InvestmentAnalyzer
from .pipeline.data_preprocessing import DataPreprocessor
from .pipeline.feature_engineering import FeatureEngineer
from .pipeline.model_training import ModelTrainer
from .utils.ml_utils import MLUtils
from .utils.model_evaluation import ModelEvaluator

# Initialize core ML services
prediction_service = PredictionService()
analysis_service = AnalysisService()
optimization_service = OptimizationService()

# Initialize Phase 4B services
automated_reporting_service = AutomatedReportingService()
smart_notification_service = SmartNotificationService()
performance_analytics_service = PerformanceAnalyticsService()

# Initialize ML models
market_predictor = MarketPredictor()
property_valuator = PropertyValuator()
investment_analyzer = InvestmentAnalyzer()

# Initialize ML pipeline components
data_preprocessor = DataPreprocessor()
feature_engineer = FeatureEngineer()
model_trainer = ModelTrainer()

# Initialize ML utilities
ml_utils = MLUtils()
model_evaluator = ModelEvaluator()

__all__ = [
    # Services
    'prediction_service',
    'analysis_service', 
    'optimization_service',
    'automated_reporting_service',
    'smart_notification_service',
    'performance_analytics_service',
    
    # Models
    'market_predictor',
    'property_valuator',
    'investment_analyzer',
    
    # Pipeline
    'data_preprocessor',
    'feature_engineer',
    'model_trainer',
    
    # Utilities
    'ml_utils',
    'model_evaluator',
    
    # Classes
    'PredictionService',
    'AnalysisService',
    'OptimizationService',
    'AutomatedReportingService',
    'SmartNotificationService',
    'PerformanceAnalyticsService',
    'MarketPredictor',
    'PropertyValuator',
    'InvestmentAnalyzer',
    'DataPreprocessor',
    'FeatureEngineer',
    'ModelTrainer',
    'MLUtils',
    'ModelEvaluator'
]

# Version information
__version__ = "1.0.0"
__author__ = "AI Development Team"
__description__ = "AI-Powered Insights for Real Estate Intelligence"
