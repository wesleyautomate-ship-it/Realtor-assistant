"""
Advanced ML Model Integration Service
Integrates actual machine learning models for predictions and analytics
"""

import asyncio
import json
import logging
import pickle
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostRegressor
import joblib
import redis
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.ml_models import MLModelPerformance, MLMarketIntelligence
from ..utils.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class AdvancedMLService:
    """Advanced ML Model Integration Service for real estate predictions"""
    
    def __init__(self):
        self.models_dir = Path("backend/ml/models")
        self.models_dir.mkdir(exist_ok=True)
        self.scalers_dir = Path("backend/ml/scalers")
        self.scalers_dir.mkdir(exist_ok=True)
        self.feature_columns = [
            'property_size', 'bedrooms', 'bathrooms', 'floor_number',
            'age', 'distance_to_metro', 'distance_to_mall', 'distance_to_school',
            'parking_spaces', 'balcony', 'garden', 'pool', 'gym',
            'security', 'maintenance_fee', 'service_charges',
            'market_demand_score', 'economic_indicator', 'seasonality_factor'
        ]
        self.target_column = 'price_per_sqm'
        self.current_models = {}
        self.model_performance_cache = {}
        
    async def initialize_models(self):
        """Initialize and load all available ML models"""
        try:
            logger.info("🚀 Initializing Advanced ML Models...")
            
            # Load pre-trained models if they exist
            await self._load_existing_models()
            
            # Initialize default models if none exist
            if not self.current_models:
                await self._initialize_default_models()
            
            logger.info(f"✅ Advanced ML Models initialized: {len(self.current_models)} models loaded")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error initializing ML models: {e}")
            return False
    
    async def _load_existing_models(self):
        """Load existing trained models from disk"""
        try:
            model_files = list(self.models_dir.glob("*.joblib"))
            
            for model_file in model_files:
                model_name = model_file.stem
                try:
                    model = joblib.load(model_file)
                    scaler_file = self.scalers_dir / f"{model_name}_scaler.joblib"
                    
                    if scaler_file.exists():
                        scaler = joblib.load(scaler_file)
                        self.current_models[model_name] = {
                            'model': model,
                            'scaler': scaler,
                            'last_updated': model_file.stat().st_mtime,
                            'file_path': model_file
                        }
                        logger.info(f"📦 Loaded model: {model_name}")
                        
                except Exception as e:
                    logger.warning(f"⚠️ Failed to load model {model_name}: {e}")
                    
        except Exception as e:
            logger.error(f"❌ Error loading existing models: {e}")
    
    async def _initialize_default_models(self):
        """Initialize default ML models with basic configurations"""
        try:
            logger.info("🔧 Initializing default ML models...")
            
            # Random Forest
            rf_model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            
            # XGBoost
            xgb_model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42,
                n_jobs=-1
            )
            
            # LightGBM
            lgb_model = lgb.LGBMRegressor(
                n_estimators=100,
                max_depth=6,
            learning_rate=0.1,
                random_state=42,
                n_jobs=-1
            )
            
            # CatBoost
            cat_model = CatBoostRegressor(
                iterations=100,
                depth=6,
                learning_rate=0.1,
                random_state=42,
                verbose=False
            )
            
            # Store default models
            self.current_models = {
                'random_forest': {
                    'model': rf_model,
                    'scaler': StandardScaler(),
                    'last_updated': datetime.now().timestamp(),
                    'file_path': None
                },
                'xgboost': {
                    'model': xgb_model,
                    'scaler': StandardScaler(),
                    'last_updated': datetime.now().timestamp(),
                    'file_path': None
                },
                'lightgbm': {
                    'model': lgb_model,
                    'scaler': StandardScaler(),
                    'last_updated': datetime.now().timestamp(),
                    'file_path': None
                },
                'catboost': {
                    'model': cat_model,
                    'scaler': StandardScaler(),
                    'last_updated': datetime.now().timestamp(),
                    'file_path': None
                }
            }
            
            logger.info("✅ Default models initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Error initializing default models: {e}")
    
    async def generate_synthetic_training_data(self, num_samples: int = 10000) -> pd.DataFrame:
        """Generate synthetic training data for model training"""
        try:
            logger.info(f"🎲 Generating {num_samples} synthetic training samples...")
            
            np.random.seed(42)
            
            # Generate realistic property features
            data = {
                'property_size': np.random.uniform(50, 500, num_samples),
                'bedrooms': np.random.randint(1, 6, num_samples),
                'bathrooms': np.random.randint(1, 4, num_samples),
                'floor_number': np.random.randint(1, 50, num_samples),
                'age': np.random.randint(0, 30, num_samples),
                'distance_to_metro': np.random.uniform(0.1, 5.0, num_samples),
                'distance_to_mall': np.random.uniform(0.5, 10.0, num_samples),
                'distance_to_school': np.random.uniform(0.2, 8.0, num_samples),
                'parking_spaces': np.random.randint(0, 3, num_samples),
                'balcony': np.random.choice([0, 1], num_samples, p=[0.3, 0.7]),
                'garden': np.random.choice([0, 1], num_samples, p=[0.6, 0.4]),
                'pool': np.random.choice([0, 1], num_samples, p=[0.8, 0.2]),
                'gym': np.random.choice([0, 1], num_samples, p=[0.7, 0.3]),
                'security': np.random.choice([0, 1], num_samples, p=[0.2, 0.8]),
                'maintenance_fee': np.random.uniform(100, 2000, num_samples),
                'service_charges': np.random.uniform(50, 1000, num_samples),
                'market_demand_score': np.random.uniform(0.1, 1.0, num_samples),
                'economic_indicator': np.random.uniform(0.8, 1.2, num_samples),
                'seasonality_factor': np.random.uniform(0.9, 1.1, num_samples)
            }
            
            # Generate realistic target variable (price per sqm)
            base_price = 8000  # Base price per sqm in AED
            price_factors = (
                data['property_size'] * 0.1 +
                data['bedrooms'] * 500 +
                data['bathrooms'] * 300 +
                (50 - data['floor_number']) * 20 +
                (30 - data['age']) * 50 +
                (5.0 - data['distance_to_metro']) * 200 +
                data['parking_spaces'] * 100 +
                data['balcony'] * 150 +
                data['garden'] * 200 +
                data['pool'] * 300 +
                data['gym'] * 100 +
                data['security'] * 150 +
                data['market_demand_score'] * 1000 +
                data['economic_indicator'] * 500 +
                data['seasonality_factor'] * 200
            )
            
            # Add some noise for realism
            noise = np.random.normal(0, 200, num_samples)
            data['price_per_sqm'] = np.maximum(base_price + price_factors + noise, 2000)
            
            df = pd.DataFrame(data)
            logger.info(f"✅ Generated {len(df)} synthetic training samples")
            return df
            
        except Exception as e:
            logger.error(f"❌ Error generating synthetic data: {e}")
            return pd.DataFrame()
    
    async def train_model(self, model_name: str, training_data: pd.DataFrame = None) -> Dict[str, Any]:
        """Train a specific ML model"""
        try:
            if model_name not in self.current_models:
                raise ValueError(f"Model {model_name} not found")
            
            logger.info(f"🏋️ Training {model_name} model...")
            
            # Generate training data if not provided
            if training_data is None:
                training_data = await self.generate_synthetic_training_data()
            
            if training_data.empty:
                raise ValueError("No training data available")
            
            # Prepare features and target
            X = training_data[self.feature_columns].copy()
            y = training_data[self.target_column].copy()
            
            # Handle missing values
            X = X.fillna(X.median())
            y = y.fillna(y.median())
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Get model and scaler
            model_info = self.current_models[model_name]
            model = model_info['model']
            scaler = model_info['scaler']
            
            # Scale features
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train model
            if hasattr(model, 'fit'):
                model.fit(X_train_scaled, y_train)
            else:
                # Handle CatBoost differently
                model.fit(X_train, y_train)
            
            # Make predictions
            if hasattr(model, 'predict'):
                y_pred = model.predict(X_test_scaled if 'scaler' in str(type(model)) else X_test)
            else:
                y_pred = model.predict(X_test)
            
            # Calculate metrics
            metrics = {
                'mse': mean_squared_error(y_test, y_pred),
                'mae': mean_absolute_error(y_test, y_pred),
                'r2': r2_score(y_test, y_pred),
                'rmse': np.sqrt(mean_squared_error(y_test, y_pred))
            }
            
            # Cross-validation score
            cv_scores = cross_val_score(
                model, 
                X_train_scaled if 'scaler' in str(type(model)) else X_train, 
                y_train, 
                cv=5, 
                scoring='r2'
            )
            metrics['cv_r2_mean'] = cv_scores.mean()
            metrics['cv_r2_std'] = cv_scores.std()
            
            # Update model info
            self.current_models[model_name].update({
                'last_updated': datetime.now().timestamp(),
                'metrics': metrics,
                'training_samples': len(training_data),
                'feature_importance': self._get_feature_importance(model, model_name)
            })
            
            # Save model and scaler
            await self._save_model(model_name)
            
            # Log training results
            logger.info(f"✅ {model_name} training completed:")
            logger.info(f"   R² Score: {metrics['r2']:.4f}")
            logger.info(f"   RMSE: {metrics['rmse']:.2f}")
            logger.info(f"   CV R²: {metrics['cv_r2_mean']:.4f} ± {metrics['cv_r2_std']:.4f}")
            
            return {
                'model_name': model_name,
                'status': 'success',
                'metrics': metrics,
                'training_samples': len(training_data),
                'feature_importance': self.current_models[model_name]['feature_importance']
            }
            
        except Exception as e:
            logger.error(f"❌ Error training {model_name} model: {e}")
            return {
                'model_name': model_name,
                'status': 'error',
                'error': str(e)
            }
    
    def _get_feature_importance(self, model, model_name: str) -> Dict[str, float]:
        """Extract feature importance from trained model"""
        try:
            if hasattr(model, 'feature_importances_'):
                importance_dict = dict(zip(self.feature_columns, model.feature_importances_))
                return dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))
            elif hasattr(model, 'coef_'):
                # For linear models
                importance_dict = dict(zip(self.feature_columns, np.abs(model.coef_)))
                return dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))
            else:
                return {}
        except Exception as e:
            logger.warning(f"⚠️ Could not extract feature importance from {model_name}: {e}")
            return {}
    
    async def _save_model(self, model_name: str):
        """Save trained model and scaler to disk"""
        try:
            model_info = self.current_models[model_name]
            
            # Save model
            model_path = self.models_dir / f"{model_name}.joblib"
            joblib.dump(model_info['model'], model_path)
            
            # Save scaler
            scaler_path = self.scalers_dir / f"{model_name}_scaler.joblib"
            joblib.dump(model_info['scaler'], scaler_path)
            
            # Update file paths
            self.current_models[model_name]['file_path'] = model_path
            
            logger.info(f"💾 Saved {model_name} model and scaler")
            
        except Exception as e:
            logger.error(f"❌ Error saving {model_name} model: {e}")
    
    async def predict_property_price(self, property_features: Dict[str, Any], model_name: str = 'ensemble') -> Dict[str, Any]:
        """Predict property price using trained ML models"""
        try:
            logger.info(f"🔮 Making price prediction using {model_name} model...")
            
            # Prepare features
            features = self._prepare_features(property_features)
            
            if features is None:
                raise ValueError("Invalid property features")
            
            # Make prediction
            if model_name == 'ensemble':
                prediction = await self._ensemble_predict(features)
            elif model_name in self.current_models:
                prediction = await self._single_model_predict(features, model_name)
            else:
                raise ValueError(f"Model {model_name} not available")
            
            # Add confidence and explanation
            result = {
                'predicted_price_per_sqm': prediction['price'],
                'confidence_score': prediction['confidence'],
                'model_used': prediction['model'],
                'features_used': self.feature_columns,
                'prediction_timestamp': datetime.now().isoformat(),
                'explanation': self._generate_prediction_explanation(property_features, prediction),
                'market_context': await self._get_market_context(property_features)
            }
            
            logger.info(f"✅ Price prediction completed: {result['predicted_price_per_sqm']:.2f} AED/sqm")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error making price prediction: {e}")
            return {
                'error': str(e),
                'status': 'failed'
            }
    
    def _prepare_features(self, property_features: Dict[str, Any]) -> Optional[np.ndarray]:
        """Prepare and validate property features for prediction"""
        try:
            # Create feature vector
            feature_vector = []
            for col in self.feature_columns:
                if col in property_features:
                    value = property_features[col]
                    # Convert boolean to int
                    if isinstance(value, bool):
                        value = int(value)
                    feature_vector.append(float(value))
                else:
                    # Use default values for missing features
                    default_values = {
                        'property_size': 150.0,
                        'bedrooms': 2.0,
                        'bathrooms': 2.0,
                        'floor_number': 5.0,
                        'age': 5.0,
                        'distance_to_metro': 1.0,
                        'distance_to_mall': 2.0,
                        'distance_to_school': 1.5,
                        'parking_spaces': 1.0,
                        'balcony': 1.0,
                        'garden': 0.0,
                        'pool': 0.0,
                        'gym': 0.0,
                        'security': 1.0,
                        'maintenance_fee': 500.0,
                        'service_charges': 200.0,
                        'market_demand_score': 0.7,
                        'economic_indicator': 1.0,
                        'seasonality_factor': 1.0
                    }
                    feature_vector.append(default_values[col])
            
            return np.array(feature_vector).reshape(1, -1)
            
        except Exception as e:
            logger.error(f"❌ Error preparing features: {e}")
            return None
    
    async def _single_model_predict(self, features: np.ndarray, model_name: str) -> Dict[str, Any]:
        """Make prediction using a single model"""
        model_info = self.current_models[model_name]
        model = model_info['model']
        scaler = model_info['scaler']
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Make prediction
        if hasattr(model, 'predict'):
            prediction = model.predict(features_scaled)[0]
        else:
            prediction = model.predict(features)[0]
        
        # Calculate confidence based on model performance
        confidence = min(0.95, max(0.5, model_info.get('metrics', {}).get('r2', 0.7)))
        
        return {
            'price': float(prediction),
            'confidence': confidence,
            'model': model_name
        }
    
    async def _ensemble_predict(self, features: np.ndarray) -> Dict[str, Any]:
        """Make prediction using ensemble of all available models"""
        predictions = []
        weights = []
        
        for model_name, model_info in self.current_models.items():
            try:
                if 'metrics' in model_info and 'r2' in model_info['metrics']:
                    # Weight by R² score
                    weight = max(0.1, model_info['metrics']['r2'])
                    weights.append(weight)
                    
                    # Get prediction
                    pred = await self._single_model_predict(features, model_name)
                    predictions.append(pred['price'])
                else:
                    # Equal weight if no metrics available
                    weights.append(1.0)
                    pred = await self._single_model_predict(features, model_name)
                    predictions.append(pred['price'])
                    
            except Exception as e:
                logger.warning(f"⚠️ Error with {model_name} in ensemble: {e}")
                continue
        
        if not predictions:
            raise ValueError("No models available for ensemble prediction")
        
        # Calculate weighted average
        total_weight = sum(weights)
        weighted_prediction = sum(p * w for p, w in zip(predictions, weights)) / total_weight
        
        # Calculate confidence based on model agreement
        std_dev = np.std(predictions)
        mean_pred = np.mean(predictions)
        confidence = max(0.5, min(0.95, 1.0 - (std_dev / mean_pred) if mean_pred > 0 else 0.7))
        
        return {
            'price': float(weighted_prediction),
            'confidence': confidence,
            'model': 'ensemble',
            'individual_predictions': dict(zip([name for name in self.current_models.keys() if name in self.current_models], predictions))
        }
    
    def _generate_prediction_explanation(self, features: Dict[str, Any], prediction: Dict[str, Any]) -> str:
        """Generate human-readable explanation of the prediction"""
        try:
            explanation_parts = []
            
            # Key factors
            key_features = []
            if 'property_size' in features and features['property_size'] > 200:
                key_features.append("large property size")
            if 'bedrooms' in features and features['bedrooms'] >= 3:
                key_features.append("multiple bedrooms")
            if 'distance_to_metro' in features and features['distance_to_metro'] < 1.0:
                key_features.append("proximity to metro")
            if 'pool' in features and features['pool']:
                key_features.append("pool availability")
            
            if key_features:
                explanation_parts.append(f"Key positive factors: {', '.join(key_features)}")
            
            # Price range context
            price = prediction['predicted_price_per_sqm']
            if price > 12000:
                price_context = "premium luxury segment"
            elif price > 8000:
                price_context = "high-end segment"
            elif price > 6000:
                price_context = "mid-range segment"
            else:
                price_context = "affordable segment"
            
            explanation_parts.append(f"Predicted price falls in the {price_context}")
            
            # Confidence explanation
            confidence = prediction['confidence']
            if confidence > 0.85:
                conf_text = "high confidence"
            elif confidence > 0.7:
                conf_text = "moderate confidence"
            else:
                conf_text = "lower confidence"
            
            explanation_parts.append(f"Prediction made with {conf_text} based on market data patterns")
            
            return ". ".join(explanation_parts) + "."
            
        except Exception as e:
            logger.warning(f"⚠️ Error generating explanation: {e}")
            return "Prediction based on comprehensive market analysis and property features."
    
    async def _get_market_context(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Get market context for the prediction"""
        try:
            # This would typically fetch from market intelligence service
            # For now, return basic context
            return {
                'market_trend': 'stable',
                'demand_level': 'moderate',
                'supply_availability': 'balanced',
                'price_momentum': 'slight_increase',
                'recommendation': 'good_investment_timing'
            }
        except Exception as e:
            logger.warning(f"⚠️ Error getting market context: {e}")
            return {}
    
    async def get_model_performance(self, model_name: str = None) -> Dict[str, Any]:
        """Get performance metrics for ML models"""
        try:
            if model_name:
                if model_name not in self.current_models:
                    raise ValueError(f"Model {model_name} not found")
                
                model_info = self.current_models[model_name]
                return {
                    'model_name': model_name,
                    'performance': model_info.get('metrics', {}),
                    'last_updated': model_info.get('last_updated'),
                    'training_samples': model_info.get('training_samples', 0),
                    'feature_importance': model_info.get('feature_importance', {})
                }
            else:
                # Return performance for all models
                performance_summary = {}
                for name, info in self.current_models.items():
                    performance_summary[name] = {
                        'metrics': info.get('metrics', {}),
                        'last_updated': info.get('last_updated'),
                        'training_samples': info.get('training_samples', 0),
                        'status': 'active' if info.get('metrics') else 'untrained'
                    }
                
                return {
                    'total_models': len(self.current_models),
                    'active_models': len([m for m in performance_summary.values() if m['status'] == 'active']),
                    'models': performance_summary
                }
                
        except Exception as e:
            logger.error(f"❌ Error getting model performance: {e}")
            return {'error': str(e)}
    
    async def retrain_models(self, force_retrain: bool = False) -> Dict[str, Any]:
        """Retrain all models with fresh data"""
        try:
            logger.info("🔄 Starting model retraining process...")
            
            # Check if retraining is needed
            if not force_retrain:
                last_training = min(
                    info.get('last_updated', 0) 
                    for info in self.current_models.values()
                )
                
                if datetime.now().timestamp() - last_training < 86400:  # 24 hours
                    logger.info("ℹ️ Models are recent, skipping retraining")
                    return {'status': 'skipped', 'reason': 'models_are_recent'}
            
            # Generate fresh training data
            training_data = await self.generate_synthetic_training_data()
            
            if training_data.empty:
                raise ValueError("Failed to generate training data")
            
            # Retrain all models
            results = {}
            for model_name in self.current_models.keys():
                result = await self.train_model(model_name, training_data)
                results[model_name] = result
            
            # Calculate overall success rate
            successful = sum(1 for r in results.values() if r.get('status') == 'success')
            total = len(results)
            
            logger.info(f"✅ Model retraining completed: {successful}/{total} successful")
            
            return {
                'status': 'completed',
                'successful_models': successful,
                'total_models': total,
                'results': results,
                'training_data_size': len(training_data)
            }
            
        except Exception as e:
            logger.error(f"❌ Error during model retraining: {e}")
            return {'status': 'error', 'error': str(e)}
    
    async def optimize_model_hyperparameters(self, model_name: str) -> Dict[str, Any]:
        """Optimize hyperparameters for a specific model"""
        try:
            if model_name not in self.current_models:
                raise ValueError(f"Model {model_name} not found")
            
            logger.info(f"🔧 Optimizing hyperparameters for {model_name}...")
            
            # Generate training data
            training_data = await self.generate_synthetic_training_data()
            X = training_data[self.feature_columns].fillna(training_data[self.feature_columns].median())
            y = training_data[self.target_column].fillna(training_data[self.target_column].median())
            
            # Define hyperparameter grids for different models
            param_grids = {
                'random_forest': {
                    'n_estimators': [50, 100, 200],
                    'max_depth': [5, 10, 15, None],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4]
                },
                'xgboost': {
                    'n_estimators': [50, 100, 200],
                    'max_depth': [3, 6, 9],
                    'learning_rate': [0.01, 0.1, 0.2],
                    'subsample': [0.8, 0.9, 1.0]
                },
                'lightgbm': {
                    'n_estimators': [50, 100, 200],
                    'max_depth': [3, 6, 9],
                    'learning_rate': [0.01, 0.1, 0.2],
                    'num_leaves': [31, 62, 127]
                }
            }
            
            if model_name not in param_grids:
                logger.warning(f"⚠️ No hyperparameter grid defined for {model_name}")
                return {'status': 'skipped', 'reason': 'no_hyperparameter_grid'}
            
            # Perform grid search
            model = self.current_models[model_name]['model']
            param_grid = param_grids[model_name]
            
            grid_search = GridSearchCV(
                model, param_grid, cv=5, scoring='r2', n_jobs=-1, verbose=0
            )
            
            grid_search.fit(X, y)
            
            # Update model with best parameters
            best_model = grid_search.best_estimator_
            self.current_models[model_name]['model'] = best_model
            
            # Save optimized model
            await self._save_model(model_name)
            
            logger.info(f"✅ Hyperparameter optimization completed for {model_name}")
            logger.info(f"   Best parameters: {grid_search.best_params_}")
            logger.info(f"   Best CV score: {grid_search.best_score_:.4f}")
            
            return {
                'status': 'success',
                'model_name': model_name,
                'best_parameters': grid_search.best_params_,
                'best_cv_score': grid_search.best_score_,
                'improvement': grid_search.best_score_ - self.current_models[model_name].get('metrics', {}).get('cv_r2_mean', 0)
            }
            
        except Exception as e:
            logger.error(f"❌ Error optimizing hyperparameters for {model_name}: {e}")
            return {'status': 'error', 'error': str(e)}
    
    async def get_model_insights(self) -> Dict[str, Any]:
        """Get comprehensive insights about all ML models"""
        try:
            insights = {
                'total_models': len(self.current_models),
                'model_status': {},
                'performance_summary': {},
                'recommendations': []
            }
            
            # Analyze each model
            for model_name, model_info in self.current_models.items():
                metrics = model_info.get('metrics', {})
                
                # Model status
                if metrics:
                    r2_score = metrics.get('r2', 0)
                    if r2_score > 0.8:
                        status = 'excellent'
                    elif r2_score > 0.6:
                        status = 'good'
                    elif r2_score > 0.4:
                        status = 'fair'
                    else:
                        status = 'poor'
                else:
                    status = 'untrained'
                
                insights['model_status'][model_name] = status
                
                # Performance summary
                if metrics:
                    insights['performance_summary'][model_name] = {
                        'r2_score': metrics.get('r2', 0),
                        'rmse': metrics.get('rmse', 0),
                        'training_samples': model_info.get('training_samples', 0),
                        'last_updated': model_info.get('last_updated', 0)
                    }
            
            # Generate recommendations
            active_models = [name for name, info in insights['model_status'].items() if info != 'untrained']
            
            if not active_models:
                insights['recommendations'].append("Train all models with fresh data to enable predictions")
            else:
                best_model = max(
                    active_models,
                    key=lambda x: insights['performance_summary'][x]['r2_score']
                )
                insights['recommendations'].append(f"Use {best_model} as primary model for best accuracy")
                
                # Check for models that need retraining
                current_time = datetime.now().timestamp()
                for model_name in active_models:
                    last_updated = insights['performance_summary'][model_name]['last_updated']
                    if current_time - last_updated > 604800:  # 7 days
                        insights['recommendations'].append(f"Consider retraining {model_name} (last updated {int((current_time - last_updated) / 86400)} days ago)")
            
            return insights
            
        except Exception as e:
            logger.error(f"❌ Error getting model insights: {e}")
            return {'error': str(e)}

# Global instance
advanced_ml_service = AdvancedMLService()
