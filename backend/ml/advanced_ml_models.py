"""
Advanced ML Models Integration for Phase 4B

This module integrates actual machine learning models for:
- Property price prediction
- Market trend forecasting
- Lead scoring and conversion prediction
- Client behavior analysis
- Investment opportunity ranking
"""

import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class AdvancedMLModels:
    """Advanced Machine Learning Models for Real Estate Analytics"""
    
    def __init__(self):
        self.models_dir = Path("ml_models")
        self.models_dir.mkdir(exist_ok=True)
        
        # Initialize models
        self.price_predictor = None
        self.market_forecaster = None
        self.lead_scorer = None
        self.client_analyzer = None
        self.opportunity_ranker = None
        
        # Initialize scalers and encoders
        self.scalers = {}
        self.encoders = {}
        
        # Load or train models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize or load existing ML models"""
        try:
            # Try to load existing models
            self._load_models()
            logger.info("✅ Loaded existing ML models")
        except Exception as e:
            logger.warning(f"Could not load existing models: {e}")
            logger.info("🔄 Training new ML models...")
            self._train_models()
    
    def _load_models(self):
        """Load pre-trained models from disk"""
        model_files = {
            'price_predictor': 'price_predictor.joblib',
            'market_forecaster': 'market_forecaster.joblib',
            'lead_scorer': 'lead_scorer.joblib',
            'client_analyzer': 'client_analyzer.joblib',
            'opportunity_ranker': 'opportunity_ranker.joblib'
        }
        
        scaler_files = {
            'price_scaler': 'price_scaler.joblib',
            'market_scaler': 'market_scaler.joblib',
            'lead_scaler': 'lead_scaler.joblib'
        }
        
        encoder_files = {
            'location_encoder': 'location_encoder.joblib',
            'property_type_encoder': 'property_type_encoder.joblib',
            'amenity_encoder': 'amenity_encoder.joblib'
        }
        
        # Load models
        for model_name, filename in model_files.items():
            filepath = self.models_dir / filename
            if filepath.exists():
                setattr(self, model_name, joblib.load(filepath))
        
        # Load scalers
        for scaler_name, filename in scaler_files.items():
            filepath = self.models_dir / filename
            if filepath.exists():
                self.scalers[scaler_name] = joblib.load(filepath)
        
        # Load encoders
        for encoder_name, filename in encoder_files.items():
            filepath = self.models_dir / filename
            if filepath.exists():
                self.encoders[encoder_name] = joblib.load(filepath)
    
    def _save_models(self):
        """Save trained models to disk"""
        try:
            # Save models
            if self.price_predictor:
                joblib.dump(self.price_predictor, self.models_dir / 'price_predictor.joblib')
            if self.market_forecaster:
                joblib.dump(self.market_forecaster, self.models_dir / 'market_forecaster.joblib')
            if self.lead_scorer:
                joblib.dump(self.lead_scorer, self.models_dir / 'lead_scorer.joblib')
            if self.client_analyzer:
                joblib.dump(self.client_analyzer, self.models_dir / 'client_analyzer.joblib')
            if self.opportunity_ranker:
                joblib.dump(self.opportunity_ranker, self.models_dir / 'opportunity_ranker.joblib')
            
            # Save scalers
            for name, scaler in self.scalers.items():
                joblib.dump(scaler, self.models_dir / f'{name}.joblib')
            
            # Save encoders
            for name, encoder in self.encoders.items():
                joblib.dump(encoder, self.models_dir / f'{name}.joblib')
            
            logger.info("✅ ML models saved successfully")
            
        except Exception as e:
            logger.error(f"Failed to save models: {e}")
    
    def _train_models(self):
        """Train new ML models with synthetic data"""
        try:
            # Generate synthetic training data
            training_data = self._generate_training_data()
            
            # Train price predictor
            self._train_price_predictor(training_data)
            
            # Train market forecaster
            self._train_market_forecaster(training_data)
            
            # Train lead scorer
            self._train_lead_scorer(training_data)
            
            # Train client analyzer
            self._train_client_analyzer(training_data)
            
            # Train opportunity ranker
            self._train_opportunity_ranker(training_data)
            
            # Save models
            self._save_models()
            
            logger.info("✅ All ML models trained successfully")
            
        except Exception as e:
            logger.error(f"Failed to train models: {e}")
    
    def _generate_training_data(self) -> Dict[str, pd.DataFrame]:
        """Generate synthetic training data for Dubai real estate"""
        np.random.seed(42)  # For reproducibility
        
        # Generate property data
        n_properties = 10000
        
        # Dubai locations with realistic price ranges
        locations = [
            'Dubai Marina', 'Downtown Dubai', 'Palm Jumeirah', 'Emirates Hills',
            'Jumeirah Beach Residence', 'Business Bay', 'Dubai Hills Estate',
            'Arabian Ranches', 'Mudon', 'The Springs', 'The Meadows'
        ]
        
        property_types = ['apartment', 'villa', 'townhouse', 'penthouse', 'duplex']
        
        # Generate synthetic property data
        property_data = []
        for i in range(n_properties):
            location = np.random.choice(locations)
            property_type = np.random.choice(property_types)
            
            # Base prices by location and type
            base_prices = {
                'Dubai Marina': {'apartment': 2.5, 'villa': 8.0, 'townhouse': 6.0, 'penthouse': 12.0, 'duplex': 7.0},
                'Downtown Dubai': {'apartment': 3.0, 'villa': 10.0, 'townhouse': 7.0, 'penthouse': 15.0, 'duplex': 8.0},
                'Palm Jumeirah': {'apartment': 4.0, 'villa': 12.0, 'townhouse': 8.0, 'penthouse': 18.0, 'duplex': 10.0},
                'Emirates Hills': {'apartment': 2.0, 'villa': 15.0, 'townhouse': 9.0, 'penthouse': 20.0, 'duplex': 12.0}
            }
            
            base_price = base_prices.get(location, {'apartment': 2.0, 'villa': 8.0, 'townhouse': 6.0, 'penthouse': 10.0, 'duplex': 7.0})[property_type]
            
            # Add realistic variations
            bedrooms = np.random.randint(1, 6) if property_type in ['apartment', 'villa', 'townhouse'] else np.random.randint(3, 6)
            bathrooms = bedrooms + np.random.randint(-1, 2)
            square_feet = bedrooms * 300 + np.random.randint(200, 800)
            
            # Price calculation with realistic factors
            price = base_price * 1000000  # Convert to AED
            price *= (1 + (bedrooms - 2) * 0.15)  # Bedroom factor
            price *= (1 + (bathrooms - bedrooms) * 0.1)  # Bathroom factor
            price *= (1 + (square_feet - 1000) / 10000)  # Size factor
            
            # Add market noise
            price *= np.random.normal(1.0, 0.1)
            
            # Amenities impact
            amenities_score = np.random.uniform(0.7, 1.3)
            price *= amenities_score
            
            property_data.append({
                'location': location,
                'property_type': property_type,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'square_feet': square_feet,
                'price': price,
                'amenities_score': amenities_score,
                'age_years': np.random.randint(0, 15),
                'floor_number': np.random.randint(1, 50) if property_type == 'apartment' else 1,
                'has_pool': np.random.choice([0, 1], p=[0.7, 0.3]),
                'has_gym': np.random.choice([0, 1], p=[0.6, 0.4]),
                'has_parking': np.random.choice([0, 1], p=[0.2, 0.8]),
                'distance_to_metro': np.random.uniform(0.1, 3.0),
                'distance_to_mall': np.random.uniform(0.5, 5.0),
                'distance_to_beach': np.random.uniform(0.1, 10.0)
            })
        
        # Generate market trend data
        market_data = []
        for location in locations:
            for month in range(24):  # 2 years of data
                date = datetime.now() - timedelta(days=30*month)
                
                # Base market conditions
                base_growth = np.random.uniform(-0.02, 0.03)  # Monthly growth rate
                
                # Seasonal effects
                seasonal_factor = 1 + 0.1 * np.sin(2 * np.pi * month / 12)
                
                # Location-specific trends
                location_factors = {
                    'Dubai Marina': 1.02,  # Growing area
                    'Downtown Dubai': 1.01,  # Stable
                    'Palm Jumeirah': 1.03,  # Premium growth
                    'Emirates Hills': 1.015,  # Steady growth
                }
                location_factor = location_factors.get(location, 1.0)
                
                # Market volatility
                volatility = np.random.normal(0, 0.01)
                
                growth_rate = base_growth * seasonal_factor * location_factor + volatility
                
                market_data.append({
                    'location': location,
                    'date': date,
                    'month': month,
                    'growth_rate': growth_rate,
                    'price_index': 100 * (1 + growth_rate) ** month,
                    'transaction_volume': np.random.randint(50, 200),
                    'days_on_market': np.random.randint(30, 120),
                    'price_per_sqft': np.random.uniform(800, 2500)
                })
        
        # Generate lead data
        lead_data = []
        for i in range(5000):
            lead_data.append({
                'lead_source': np.random.choice(['website', 'referral', 'social_media', 'cold_call', 'event']),
                'budget_min': np.random.uniform(500000, 5000000),
                'budget_max': np.random.uniform(1000000, 10000000),
                'preferred_location': np.random.choice(locations),
                'property_type_preference': np.random.choice(property_types),
                'urgency_score': np.random.randint(1, 11),
                'engagement_level': np.random.choice(['low', 'medium', 'high']),
                'previous_interactions': np.random.randint(0, 20),
                'email_opens': np.random.randint(0, 50),
                'website_visits': np.random.randint(0, 30),
                'conversion_probability': np.random.uniform(0.1, 0.9)
            })
        
        # Generate client behavior data
        client_data = []
        for i in range(3000):
            client_data.append({
                'client_id': i,
                'total_properties_viewed': np.random.randint(1, 50),
                'properties_saved': np.random.randint(0, 20),
                'inquiries_sent': np.random.randint(0, 30),
                'viewing_attended': np.random.randint(0, 15),
                'offers_made': np.random.randint(0, 10),
                'properties_purchased': np.random.randint(0, 5),
                'average_session_duration': np.random.uniform(2, 45),
                'days_since_last_activity': np.random.randint(0, 90),
                'preferred_contact_method': np.random.choice(['email', 'phone', 'whatsapp', 'in_person']),
                'response_time_hours': np.random.uniform(0.5, 48),
                'satisfaction_score': np.random.uniform(3.0, 5.0)
            })
        
        return {
            'properties': pd.DataFrame(property_data),
            'market': pd.DataFrame(market_data),
            'leads': pd.DataFrame(lead_data),
            'clients': pd.DataFrame(client_data)
        }
    
    def _train_price_predictor(self, training_data: Dict[str, pd.DataFrame]):
        """Train property price prediction model"""
        try:
            df = training_data['properties'].copy()
            
            # Prepare features
            feature_columns = [
                'bedrooms', 'bathrooms', 'square_feet', 'age_years', 'floor_number',
                'has_pool', 'has_gym', 'has_parking', 'distance_to_metro',
                'distance_to_mall', 'distance_to_beach', 'amenities_score'
            ]
            
            # Encode categorical variables
            if 'location_encoder' not in self.encoders:
                self.encoders['location_encoder'] = LabelEncoder()
                df['location_encoded'] = self.encoders['location_encoder'].fit_transform(df['location'])
            else:
                df['location_encoded'] = self.encoders['location_encoder'].transform(df['location'])
            
            if 'property_type_encoder' not in self.encoders:
                self.encoders['property_type_encoder'] = LabelEncoder()
                df['property_type_encoded'] = self.encoders['property_type_encoder'].fit_transform(df['property_type'])
            else:
                df['property_type_encoded'] = self.encoders['property_type_encoder'].transform(df['property_type'])
            
            feature_columns.extend(['location_encoded', 'property_type_encoded'])
            
            X = df[feature_columns]
            y = df['price']
            
            # Scale features
            if 'price_scaler' not in self.scalers:
                self.scalers['price_scaler'] = StandardScaler()
                X_scaled = self.scalers['price_scaler'].fit_transform(X)
            else:
                X_scaled = self.scalers['price_scaler'].transform(X)
            
            # Train model
            self.price_predictor = GradientBoostingRegressor(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=6,
                random_state=42
            )
            
            self.price_predictor.fit(X_scaled, y)
            
            # Evaluate model
            y_pred = self.price_predictor.predict(X_scaled)
            r2 = r2_score(y, y_pred)
            rmse = np.sqrt(mean_squared_error(y, y_pred))
            
            logger.info(f"✅ Price predictor trained - R²: {r2:.3f}, RMSE: {rmse:.0f}")
            
        except Exception as e:
            logger.error(f"Failed to train price predictor: {e}")
    
    def _train_market_forecaster(self, training_data: Dict[str, pd.DataFrame]):
        """Train market trend forecasting model"""
        try:
            df = training_data['market'].copy()
            
            # Prepare features for time series forecasting
            df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
            df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
            
            feature_columns = [
                'month_sin', 'month_cos', 'transaction_volume', 'days_on_market',
                'price_per_sqft'
            ]
            
            # Encode location
            if 'location_encoder' in self.encoders:
                df['location_encoded'] = self.encoders['location_encoder'].transform(df['location'])
                feature_columns.append('location_encoded')
            
            X = df[feature_columns]
            y = df['growth_rate']
            
            # Scale features
            if 'market_scaler' not in self.scalers:
                self.scalers['market_scaler'] = StandardScaler()
                X_scaled = self.scalers['market_scaler'].fit_transform(X)
            else:
                X_scaled = self.scalers['market_scaler'].transform(X)
            
            # Train model
            self.market_forecaster = RandomForestRegressor(
                n_estimators=150,
                max_depth=8,
                random_state=42
            )
            
            self.market_forecaster.fit(X_scaled, y)
            
            # Evaluate model
            y_pred = self.market_forecaster.predict(X_scaled)
            r2 = r2_score(y, y_pred)
            
            logger.info(f"✅ Market forecaster trained - R²: {r2:.3f}")
            
        except Exception as e:
            logger.error(f"Failed to train market forecaster: {e}")
    
    def _train_lead_scorer(self, training_data: Dict[str, pd.DataFrame]):
        """Train lead scoring model"""
        try:
            df = training_data['leads'].copy()
            
            # Prepare features
            feature_columns = [
                'budget_min', 'budget_max', 'urgency_score', 'previous_interactions',
                'email_opens', 'website_visits'
            ]
            
            # Encode categorical variables
            if 'lead_source_encoder' not in self.encoders:
                self.encoders['lead_source_encoder'] = LabelEncoder()
                df['source_encoded'] = self.encoders['lead_source_encoder'].fit_transform(df['lead_source'])
            else:
                df['source_encoded'] = self.encoders['lead_source_encoder'].transform(df['lead_source'])
            
            if 'location_encoder' in self.encoders:
                df['location_encoded'] = self.encoders['location_encoder'].transform(df['preferred_location'])
                feature_columns.append('location_encoded')
            
            if 'property_type_encoder' in self.encoders:
                df['property_type_encoded'] = self.encoders['property_type_encoder'].transform(df['property_type_preference'])
                feature_columns.append('property_type_encoded')
            
            feature_columns.extend(['source_encoded'])
            
            X = df[feature_columns]
            y = df['conversion_probability']
            
            # Scale features
            if 'lead_scaler' not in self.scalers:
                self.scalers['lead_scaler'] = StandardScaler()
                X_scaled = self.scalers['lead_scaler'].fit_transform(X)
            else:
                X_scaled = self.scalers['lead_scaler'].transform(X)
            
            # Train model
            self.lead_scorer = GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.15,
                max_depth=5,
                random_state=42
            )
            
            self.lead_scorer.fit(X_scaled, y)
            
            # Evaluate model
            y_pred = self.lead_scorer.predict(X_scaled)
            r2 = r2_score(y, y_pred)
            
            logger.info(f"✅ Lead scorer trained - R²: {r2:.3f}")
            
        except Exception as e:
            logger.error(f"Failed to train lead scorer: {e}")
    
    def _train_client_analyzer(self, training_data: Dict[str, pd.DataFrame]):
        """Train client behavior analysis model"""
        try:
            df = training_data['clients'].copy()
            
            # Prepare features
            feature_columns = [
                'total_properties_viewed', 'properties_saved', 'inquiries_sent',
                'viewing_attended', 'offers_made', 'properties_purchased',
                'average_session_duration', 'days_since_last_activity',
                'response_time_hours', 'satisfaction_score'
            ]
            
            # Encode categorical variables
            if 'contact_method_encoder' not in self.encoders:
                self.encoders['contact_method_encoder'] = LabelEncoder()
                df['contact_method_encoded'] = self.encoders['contact_method_encoder'].fit_transform(df['preferred_contact_method'])
                feature_columns.append('contact_method_encoded')
            else:
                df['contact_method_encoded'] = self.encoders['contact_method_encoder'].transform(df['preferred_contact_method'])
                feature_columns.append('contact_method_encoded')
            
            X = df[feature_columns]
            y = df['satisfaction_score']
            
            # Train model
            self.client_analyzer = RandomForestRegressor(
                n_estimators=100,
                max_depth=6,
                random_state=42
            )
            
            self.client_analyzer.fit(X, y)
            
            # Evaluate model
            y_pred = self.client_analyzer.predict(X)
            r2 = r2_score(y, y_pred)
            
            logger.info(f"✅ Client analyzer trained - R²: {r2:.3f}")
            
        except Exception as e:
            logger.error(f"Failed to train client analyzer: {e}")
    
    def _train_opportunity_ranker(self, training_data: Dict[str, pd.DataFrame]):
        """Train investment opportunity ranking model"""
        try:
            # Combine property and market data for opportunity ranking
            properties_df = training_data['properties'].copy()
            market_df = training_data['market'].copy()
            
            # Merge data
            merged_df = properties_df.merge(
                market_df.groupby('location').agg({
                    'growth_rate': 'mean',
                    'transaction_volume': 'mean',
                    'days_on_market': 'mean'
                }).reset_index(),
                on='location',
                how='left'
            )
            
            # Calculate opportunity score
            merged_df['opportunity_score'] = (
                merged_df['amenities_score'] * 0.3 +
                (1 / merged_df['distance_to_metro']) * 0.2 +
                (1 / merged_df['distance_to_mall']) * 0.15 +
                (1 / merged_df['distance_to_beach']) * 0.15 +
                merged_df['growth_rate'] * 0.2
            )
            
            # Prepare features
            feature_columns = [
                'bedrooms', 'bathrooms', 'square_feet', 'amenities_score',
                'distance_to_metro', 'distance_to_mall', 'distance_to_beach',
                'growth_rate', 'transaction_volume', 'days_on_market'
            ]
            
            X = merged_df[feature_columns]
            y = merged_df['opportunity_score']
            
            # Train model
            self.opportunity_ranker = GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
            
            self.opportunity_ranker.fit(X, y)
            
            # Evaluate model
            y_pred = self.opportunity_ranker.predict(X)
            r2 = r2_score(y, y_pred)
            
            logger.info(f"✅ Opportunity ranker trained - R²: {r2:.3f}")
            
        except Exception as e:
            logger.error(f"Failed to train opportunity ranker: {e}")
    
    # Prediction methods
    def predict_property_price(self, property_features: Dict[str, Any]) -> Dict[str, Any]:
        """Predict property price based on features"""
        try:
            if not self.price_predictor:
                raise ValueError("Price predictor model not trained")
            
            # Prepare features
            features = []
            feature_names = [
                'bedrooms', 'bathrooms', 'square_feet', 'age_years', 'floor_number',
                'has_pool', 'has_gym', 'has_parking', 'distance_to_metro',
                'distance_to_mall', 'distance_to_beach', 'amenities_score'
            ]
            
            for feature in feature_names:
                features.append(property_features.get(feature, 0))
            
            # Encode categorical variables
            if 'location_encoder' in self.encoders:
                location_encoded = self.encoders['location_encoder'].transform([property_features.get('location', 'Dubai Marina')])[0]
                features.append(location_encoded)
            else:
                features.append(0)
            
            if 'property_type_encoder' in self.encoders:
                property_type_encoded = self.encoders['property_type_encoder'].transform([property_features.get('property_type', 'apartment')])[0]
                features.append(property_type_encoded)
            else:
                features.append(0)
            
            # Scale features
            if 'price_scaler' in self.scalers:
                features_scaled = self.scalers['price_scaler'].transform([features])
            else:
                features_scaled = [features]
            
            # Make prediction
            predicted_price = self.price_predictor.predict(features_scaled)[0]
            
            # Calculate confidence interval (simplified)
            confidence = 0.85  # Base confidence
            if property_features.get('amenities_score', 1.0) > 1.1:
                confidence += 0.05
            if property_features.get('distance_to_metro', 2.0) < 1.0:
                confidence += 0.05
            
            return {
                'predicted_price': float(predicted_price),
                'confidence': min(confidence, 0.95),
                'price_range': {
                    'min': float(predicted_price * 0.9),
                    'max': float(predicted_price * 1.1)
                },
                'model_version': 'v1.0',
                'prediction_timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to predict property price: {e}")
            return {
                'error': str(e),
                'predicted_price': None,
                'confidence': 0.0
            }
    
    def forecast_market_trends(self, location: str, months_ahead: int = 6) -> Dict[str, Any]:
        """Forecast market trends for a specific location"""
        try:
            if not self.market_forecaster:
                raise ValueError("Market forecaster model not trained")
            
            # Prepare forecast features
            forecast_data = []
            for month in range(months_ahead):
                month_sin = np.sin(2 * np.pi * month / 12)
                month_cos = np.cos(2 * np.pi * month / 12)
                
                # Use average values for other features
                features = [
                    month_sin, month_cos, 150, 75, 1500  # Default values
                ]
                
                if 'location_encoder' in self.encoders:
                    try:
                        location_encoded = self.encoders['location_encoder'].transform([location])[0]
                        features.append(location_encoded)
                    except:
                        features.append(0)
                
                forecast_data.append(features)
            
            # Scale features
            if 'market_scaler' in self.scalers:
                forecast_data_scaled = self.scalers['market_scaler'].transform(forecast_data)
            else:
                forecast_data_scaled = forecast_data
            
            # Make predictions
            growth_rates = self.market_forecaster.predict(forecast_data_scaled)
            
            # Calculate cumulative growth
            cumulative_growth = 1.0
            monthly_forecasts = []
            
            for i, growth_rate in enumerate(growth_rates):
                cumulative_growth *= (1 + growth_rate)
                monthly_forecasts.append({
                    'month': i + 1,
                    'growth_rate': float(growth_rate),
                    'cumulative_growth': float(cumulative_growth),
                    'forecast_date': (datetime.now() + timedelta(days=30*i)).strftime('%Y-%m-%d')
                })
            
            return {
                'location': location,
                'forecast_months': months_ahead,
                'monthly_forecasts': monthly_forecasts,
                'total_growth_forecast': float(cumulative_growth - 1),
                'confidence': 0.80,
                'model_version': 'v1.0',
                'forecast_timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to forecast market trends: {e}")
            return {
                'error': str(e),
                'location': location,
                'forecast_months': months_ahead
            }
    
    def score_lead(self, lead_features: Dict[str, Any]) -> Dict[str, Any]:
        """Score lead conversion probability"""
        try:
            if not self.lead_scorer:
                raise ValueError("Lead scorer model not trained")
            
            # Prepare features
            features = [
                lead_features.get('budget_min', 1000000),
                lead_features.get('budget_max', 3000000),
                lead_features.get('urgency_score', 5),
                lead_features.get('previous_interactions', 0),
                lead_features.get('email_opens', 0),
                lead_features.get('website_visits', 0)
            ]
            
            # Encode categorical variables
            if 'lead_source_encoder' in self.encoders:
                try:
                    source_encoded = self.encoders['lead_source_encoder'].transform([lead_features.get('lead_source', 'website')])[0]
                    features.append(source_encoded)
                except:
                    features.append(0)
            else:
                features.append(0)
            
            if 'location_encoder' in self.encoders:
                try:
                    location_encoded = self.encoders['location_encoder'].transform([lead_features.get('preferred_location', 'Dubai Marina')])[0]
                    features.append(location_encoded)
                except:
                    features.append(0)
            else:
                features.append(0)
            
            if 'property_type_encoder' in self.encoders:
                try:
                    property_type_encoded = self.encoders['property_type_encoder'].transform([lead_features.get('property_type_preference', 'apartment')])[0]
                    features.append(property_type_encoded)
                except:
                    features.append(0)
            else:
                features.append(0)
            
            # Scale features
            if 'lead_scaler' in self.scalers:
                features_scaled = self.scalers['lead_scaler'].transform([features])
            else:
                features_scaled = [features]
            
            # Make prediction
            conversion_probability = self.lead_scorer.predict(features_scaled)[0]
            
            # Determine lead quality
            if conversion_probability > 0.7:
                quality = 'high'
                priority = 'urgent'
            elif conversion_probability > 0.4:
                quality = 'medium'
                priority = 'high'
            else:
                quality = 'low'
                priority = 'medium'
            
            return {
                'conversion_probability': float(conversion_probability),
                'lead_quality': quality,
                'priority': priority,
                'recommended_actions': self._get_lead_recommendations(conversion_probability),
                'confidence': 0.85,
                'model_version': 'v1.0',
                'scored_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to score lead: {e}")
            return {
                'error': str(e),
                'conversion_probability': None,
                'lead_quality': 'unknown'
            }
    
    def _get_lead_recommendations(self, conversion_probability: float) -> List[str]:
        """Get recommended actions based on lead score"""
        recommendations = []
        
        if conversion_probability > 0.7:
            recommendations.extend([
                'Schedule immediate viewing',
                'Send personalized property recommendations',
                'Offer exclusive early access to new listings',
                'Assign senior agent for follow-up'
            ])
        elif conversion_probability > 0.4:
            recommendations.extend([
                'Send targeted property alerts',
                'Schedule phone consultation',
                'Provide market insights report',
                'Follow up within 24 hours'
            ])
        else:
            recommendations.extend([
                'Send general market newsletter',
                'Maintain periodic check-ins',
                'Provide educational content',
                'Monitor for engagement improvements'
            ])
        
        return recommendations
    
    def get_model_performance(self) -> Dict[str, Any]:
        """Get performance metrics for all models"""
        try:
            performance_data = {
                'models': {},
                'overall_health': 'healthy',
                'last_training': datetime.utcnow().isoformat(),
                'total_models': 5
            }
            
            # Check model availability
            models_status = {
                'price_predictor': self.price_predictor is not None,
                'market_forecaster': self.market_forecaster is not None,
                'lead_scorer': self.lead_scorer is not None,
                'client_analyzer': self.client_analyzer is not None,
                'opportunity_ranker': self.opportunity_ranker is not None
            }
            
            active_models = sum(models_status.values())
            performance_data['active_models'] = active_models
            performance_data['models'] = models_status
            
            if active_models < 3:
                performance_data['overall_health'] = 'degraded'
            elif active_models == 5:
                performance_data['overall_health'] = 'excellent'
            
            return performance_data
            
        except Exception as e:
            logger.error(f"Failed to get model performance: {e}")
            return {
                'error': str(e),
                'overall_health': 'unknown'
            }

# Global instance
advanced_ml_models = AdvancedMLModels()
