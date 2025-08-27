"""
Configuration settings for Advanced AI Features and Financial Tools
"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class APIConfig:
    """API configuration for external services"""
    google_api_key: str
    bayut_api_key: Optional[str] = None
    propertyfinder_api_key: Optional[str] = None
    fixer_api_key: Optional[str] = None
    exchange_rate_api_key: Optional[str] = None
    dubai_land_dept_api_key: Optional[str] = None

@dataclass
class ModelConfig:
    """ML model configuration"""
    price_prediction_model_path: str = "models/price_prediction.pkl"
    sentiment_model_path: str = "models/sentiment_analysis.pkl"
    lead_scoring_model_path: str = "models/lead_scoring.pkl"
    confidence_threshold: float = 0.85
    max_prediction_horizon: int = 60  # months

@dataclass
class FinancialConfig:
    """Financial calculator configuration"""
    default_commission_rate: float = 0.025  # 2.5%
    vat_rate: float = 0.05  # 5% UAE VAT
    default_currency: str = "AED"
    supported_currencies: List[str] = None
    rental_yield_api_url: str = "https://api.rentalyield.com/v1"
    
    def __post_init__(self):
        if self.supported_currencies is None:
            self.supported_currencies = ["AED", "USD", "EUR", "GBP", "SAR", "QAR", "KWD"]

@dataclass
class FeatureFlags:
    """Feature flags for enabling/disabling features"""
    enable_price_prediction: bool = True
    enable_market_forecasting: bool = True
    enable_lead_scoring: bool = True
    enable_sentiment_analysis: bool = True
    enable_roi_calculator: bool = True
    enable_commission_calculator: bool = True
    enable_tax_calculator: bool = True
    enable_currency_converter: bool = True
    enable_content_generation: bool = True
    enable_instagram_post_generation: bool = True
    enable_email_generation: bool = True
    enable_whatsapp_broadcast: bool = True
    enable_neighborhood_insights: bool = True

class AdvancedFeaturesConfig:
    """Main configuration class for advanced features"""
    
    def __init__(self):
        self.api = APIConfig(
            google_api_key=os.getenv("GOOGLE_API_KEY", ""),
            bayut_api_key=os.getenv("BAYUT_API_KEY", ""),
            propertyfinder_api_key=os.getenv("PROPERTYFINDER_API_KEY", ""),
            fixer_api_key=os.getenv("FIXER_API_KEY", ""),
            exchange_rate_api_key=os.getenv("EXCHANGE_RATE_API_KEY", ""),
            dubai_land_dept_api_key=os.getenv("DUBAI_LAND_DEPT_API_KEY", "")
        )
        
        self.model = ModelConfig()
        self.financial = FinancialConfig()
        self.features = FeatureFlags()
        
        # Database configuration
        self.database_url = os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/real_estate_db")
        
        # Redis configuration for caching
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        
        # External API endpoints
        self.api_endpoints = {
            "bayut": "https://api.bayut.com/v1",
            "propertyfinder": "https://api.propertyfinder.ae/v1",
            "dubai_land_dept": "https://api.dubailand.gov.ae/v1",
            "exchange_rates": "https://api.exchangerate-api.com/v4/latest",
            "fixer": "http://data.fixer.io/api",
            "schools": "https://api.dubai.gov.ae/schools",
            "crime_stats": "https://api.dubai.gov.ae/crime-statistics"
        }
        
        # Intent patterns for natural language recognition
        self.intent_patterns = {
            "price_prediction": [
                r"what will.*worth.*(\d+)\s*(year|month)",
                r"predict.*market value",
                r"price.*trend.*area",
                r"future.*price",
                r"appreciation.*rate"
            ],
            "market_forecast": [
                r"market trend.*(\w+)",
                r"(\d+)\s*month.*forecast",
                r"good time.*invest",
                r"market.*outlook",
                r"trend.*analysis"
            ],
            "lead_scoring": [
                r"score.*lead",
                r"likely.*buy",
                r"prioritize.*leads",
                r"conversion.*probability",
                r"lead.*quality"
            ],
            "roi_calculation": [
                r"calculate.*roi",
                r"investment.*return",
                r"(\d+)\s*year.*projection",
                r"rental.*yield",
                r"return.*investment"
            ],
            "commission_calculation": [
                r"calculate.*commission",
                r"commission.*sale",
                r"agent.*earnings",
                r"commission.*rate",
                r"agent.*fee"
            ],
            "tax_calculation": [
                r"calculate.*tax",
                r"tax.*implication",
                r"property.*tax",
                r"annual.*cost",
                r"tax.*optimization"
            ],
            "currency_conversion": [
                r"convert.*(\w{3})",
                r"price.*(\w{3})",
                r"currency.*(\w{3})",
                r"exchange.*rate",
                r"(\w{3})\s*to\s*(\w{3})"
            ],
            "neighborhood_insights": [
                r"neighborhood.*info",
                r"school.*rating",
                r"area.*safety",
                r"amenities.*nearby",
                r"area.*analysis"
            ],
            "content_generation": [
                r"create.*brochure",
                r"generate.*report",
                r"write.*description",
                r"create.*listing",
                r"property.*marketing"
            ],
            "create_instagram_post": [
                r"/create post",
                r"/generate post",
                r"create.*instagram.*post",
                r"generate.*instagram.*post",
                r"create.*social.*media.*post"
            ],
            "draft_follow_up_email": [
                r"/draft email",
                r"/generate email",
                r"draft.*follow.*up.*email",
                r"generate.*follow.*up.*email",
                r"create.*email.*for.*client"
            ],
            "generate_whatsapp_broadcast": [
                r"/generate whatsapp",
                r"/create whatsapp",
                r"generate.*whatsapp.*broadcast",
                r"create.*whatsapp.*message",
                r"whatsapp.*broadcast.*for"
            ],
            "sentiment_analysis": [
                r"client.*feeling",
                r"conversation.*mood",
                r"client.*satisfaction",
                r"sentiment.*analysis",
                r"emotion.*detection"
            ]
        }
        
        # Response templates
        self.response_templates = {
            "price_prediction": {
                "success": "Based on my analysis, this property is predicted to be worth {predicted_price} in {timeframe}. Confidence level: {confidence}%",
                "insufficient_data": "I need more information about the property to make an accurate prediction. Please provide details about location, size, and property type.",
                "error": "I'm unable to predict the price at the moment. Please try again later."
            },
            "roi_calculation": {
                "success": "ROI Analysis:\n- Annual Return: {annual_return}%\n- 5-Year Projection: {five_year_return}%\n- Monthly Rental Income: {monthly_rent}\n- Total Investment: {total_investment}",
                "error": "Unable to calculate ROI. Please provide property details and investment amount."
            },
            "commission_calculation": {
                "success": "Commission Breakdown:\n- Property Value: {property_value}\n- Commission Rate: {commission_rate}%\n- Gross Commission: {gross_commission}\n- VAT (5%): {vat_amount}\n- Net Commission: {net_commission}",
                "error": "Unable to calculate commission. Please provide property value and commission rate."
            }
        }

# Global configuration instance
config = AdvancedFeaturesConfig()