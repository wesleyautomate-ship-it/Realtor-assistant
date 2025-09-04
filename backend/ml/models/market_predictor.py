"""
Market Predictor - Real Estate Market Trend Analysis

This module provides:
- Market trend predictions
- Price forecasting models
- Market cycle analysis
- Seasonal pattern detection
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union, Any
import logging
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ML imports
try:
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.linear_model import LinearRegression, Ridge, Lasso
    from sklearn.svm import SVR
    from sklearn.neural_network import MLPRegressor
    from sklearn.preprocessing import StandardScaler, RobustScaler
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
    from sklearn.pipeline import Pipeline
    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    logging.warning("scikit-learn not available. ML models will not work.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketPredictor:
    """Real estate market trend prediction and analysis"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.feature_importance = {}
        self.prediction_history = []
        self.model_performance = {}
        
        if not ML_AVAILABLE:
            logger.warning("ML libraries not available. Using simplified models.")
        
        # Initialize models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize ML models for different prediction tasks"""
        try:
            if ML_AVAILABLE:
                # Price prediction models
                self.models['price_rf'] = RandomForestRegressor(
                    n_estimators=100, random_state=42, n_jobs=-1
                )
                self.models['price_gb'] = GradientBoostingRegressor(
                    n_estimators=100, random_state=42
                )
                self.models['price_linear'] = LinearRegression()
                
                # Trend prediction models
                self.models['trend_rf'] = RandomForestRegressor(
                    n_estimators=100, random_state=42, n_jobs=-1
                )
                self.models['trend_svr'] = SVR(kernel='rbf', C=1.0)
                
                # Market cycle models
                self.models['cycle_rf'] = RandomForestRegressor(
                    n_estimators=100, random_state=42, n_jobs=-1
                )
                
                # Initialize scalers
                self.scalers['standard'] = StandardScaler()
                self.scalers['robust'] = RobustScaler()
                
                logger.info("ML models initialized successfully")
            else:
                logger.info("Using simplified statistical models")
                
        except Exception as e:
            logger.error(f"Error initializing models: {e}")
    
    def predict_property_prices(self, market_data: pd.DataFrame, 
                               property_features: Dict[str, Any],
                               prediction_horizon: int = 12) -> Dict[str, Any]:
        """
        Predict property prices based on market data and property features
        
        Args:
            market_data: Historical market data
            property_features: Property-specific features
            prediction_horizon: Months ahead to predict
            
        Returns:
            Dict[str, Any]: Price predictions and confidence intervals
        """
        try:
            if market_data.empty:
                return {'error': 'No market data provided'}
            
            # Prepare features for prediction
            features = self._prepare_price_features(market_data, property_features)
            
            if not features:
                return {'error': 'Failed to prepare features'}
            
            # Make predictions using different models
            predictions = {}
            confidence_intervals = {}
            
            for model_name, model in self.models.items():
                if 'price' in model_name:
                    try:
                        # Train model if not already trained
                        if not hasattr(model, 'fitted_'):
                            self._train_price_model(model, market_data)
                        
                        # Make prediction
                        pred = model.predict([features])[0]
                        predictions[model_name] = pred
                        
                        # Calculate confidence interval (simplified)
                        if hasattr(model, 'estimators_'):
                            # For ensemble models, use predictions from all estimators
                            all_preds = [est.predict([features])[0] for est in model.estimators_]
                            std_pred = np.std(all_preds)
                            confidence_intervals[model_name] = {
                                'lower': pred - 1.96 * std_pred,
                                'upper': pred + 1.96 * std_pred,
                                'confidence': 0.95
                            }
                        else:
                            # For linear models, use a simple confidence interval
                            confidence_intervals[model_name] = {
                                'lower': pred * 0.9,
                                'upper': pred * 1.1,
                                'confidence': 0.8
                            }
                            
                    except Exception as e:
                        logger.error(f"Error with model {model_name}: {e}")
                        predictions[model_name] = None
            
            # Ensemble prediction (average of all models)
            valid_predictions = [p for p in predictions.values() if p is not None]
            if valid_predictions:
                ensemble_pred = np.mean(valid_predictions)
                ensemble_std = np.std(valid_predictions)
                
                predictions['ensemble'] = ensemble_pred
                confidence_intervals['ensemble'] = {
                    'lower': ensemble_pred - 1.96 * ensemble_std,
                    'upper': ensemble_pred + 1.96 * ensemble_std,
                    'confidence': 0.95
                }
            
            # Store prediction history
            prediction_record = {
                'timestamp': datetime.now().isoformat(),
                'property_features': property_features,
                'predictions': predictions,
                'confidence_intervals': confidence_intervals,
                'horizon': prediction_horizon
            }
            self.prediction_history.append(prediction_record)
            
            return {
                'predictions': predictions,
                'confidence_intervals': confidence_intervals,
                'prediction_horizon': prediction_horizon,
                'timestamp': datetime.now().isoformat(),
                'model_count': len([p for p in predictions.values() if p is not None])
            }
            
        except Exception as e:
            logger.error(f"Error predicting property prices: {e}")
            return {'error': str(e)}
    
    def predict_market_trends(self, market_data: pd.DataFrame,
                             location: str,
                             property_type: str,
                             forecast_periods: int = 12) -> Dict[str, Any]:
        """
        Predict market trends for a specific location and property type
        
        Args:
            market_data: Historical market data
            location: Geographic location
            property_type: Type of property
            forecast_periods: Number of periods to forecast
            
        Returns:
            Dict[str, Any]: Market trend predictions
        """
        try:
            if market_data.empty:
                return {'error': 'No market data provided'}
            
            # Filter data for location and property type
            filtered_data = market_data[
                (market_data['location'].str.contains(location, case=False, na=False)) &
                (market_data['property_type'].str.contains(property_type, case=False, na=False))
            ].copy()
            
            if filtered_data.empty:
                return {'error': f'No data found for {location} - {property_type}'}
            
            # Prepare time series data
            time_series = self._prepare_time_series_data(filtered_data)
            
            if time_series.empty:
                return {'error': 'Failed to prepare time series data'}
            
            # Make trend predictions
            trend_predictions = {}
            
            # Simple trend analysis
            trend_predictions['linear_trend'] = self._calculate_linear_trend(time_series)
            
            # Seasonal decomposition
            trend_predictions['seasonal_patterns'] = self._analyze_seasonality(time_series)
            
            # ML-based trend prediction
            if ML_AVAILABLE:
                trend_predictions['ml_forecast'] = self._ml_trend_forecast(time_series, forecast_periods)
            
            # Market cycle analysis
            trend_predictions['market_cycle'] = self._analyze_market_cycle(time_series)
            
            # Generate trend summary
            trend_summary = self._generate_trend_summary(trend_predictions)
            
            return {
                'location': location,
                'property_type': property_type,
                'forecast_periods': forecast_periods,
                'trend_predictions': trend_predictions,
                'trend_summary': trend_summary,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error predicting market trends: {e}")
            return {'error': str(e)}
    
    def analyze_market_cycles(self, market_data: pd.DataFrame,
                             location: str = None,
                             property_type: str = None) -> Dict[str, Any]:
        """
        Analyze market cycles and identify phases
        
        Args:
            market_data: Historical market data
            location: Geographic location (optional)
            property_type: Type of property (optional)
            
        Returns:
            Dict[str, Any]: Market cycle analysis
        """
        try:
            if market_data.empty:
                return {'error': 'No market data provided'}
            
            # Filter data if location/property type specified
            if location or property_type:
                mask = pd.Series([True] * len(market_data))
                if location:
                    mask &= market_data['location'].str.contains(location, case=False, na=False)
                if property_type:
                    mask &= market_data['property_type'].str.contains(property_type, case=False, na=False)
                filtered_data = market_data[mask].copy()
            else:
                filtered_data = market_data.copy()
            
            if filtered_data.empty:
                return {'error': 'No data found for specified filters'}
            
            # Prepare time series
            time_series = self._prepare_time_series_data(filtered_data)
            
            if time_series.empty:
                return {'error': 'Failed to prepare time series data'}
            
            # Perform cycle analysis
            cycle_analysis = {
                'current_phase': self._identify_market_phase(time_series),
                'cycle_length': self._estimate_cycle_length(time_series),
                'phase_duration': self._estimate_phase_duration(time_series),
                'cycle_strength': self._measure_cycle_strength(time_series),
                'next_phase_prediction': self._predict_next_phase(time_series),
                'cycle_indicators': self._calculate_cycle_indicators(time_series)
            }
            
            return {
                'cycle_analysis': cycle_analysis,
                'data_summary': {
                    'total_periods': len(time_series),
                    'date_range': f"{time_series.index.min()} to {time_series.index.max()}",
                    'location': location,
                    'property_type': property_type
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing market cycles: {e}")
            return {'error': str(e)}
    
    def _prepare_price_features(self, market_data: pd.DataFrame, 
                               property_features: Dict[str, Any]) -> List[float]:
        """Prepare features for price prediction"""
        try:
            features = []
            
            # Basic property features
            features.extend([
                property_features.get('bedrooms', 0),
                property_features.get('bathrooms', 0),
                property_features.get('square_feet', 0),
                property_features.get('age', 0)
            ])
            
            # Market features (averages from market data)
            if not market_data.empty:
                features.extend([
                    market_data['price'].mean(),
                    market_data['price'].std(),
                    market_data['price'].median(),
                    market_data['price'].quantile(0.25),
                    market_data['price'].quantile(0.75)
                ])
            else:
                features.extend([0, 0, 0, 0, 0])
            
            # Location features (simplified)
            features.extend([
                property_features.get('location_score', 0),
                property_features.get('accessibility_score', 0),
                property_features.get('amenity_score', 0)
            ])
            
            # Time features
            current_date = datetime.now()
            features.extend([
                current_date.year,
                current_date.month,
                current_date.day,
                current_date.weekday()
            ])
            
            return features
            
        except Exception as e:
            logger.error(f"Error preparing price features: {e}")
            return []
    
    def _prepare_time_series_data(self, data: pd.DataFrame) -> pd.Series:
        """Prepare time series data for trend analysis"""
        try:
            # Ensure we have date and price columns
            if 'date' not in data.columns or 'price' not in data.columns:
                logger.error("Missing required columns: date and price")
                return pd.Series()
            
            # Convert date column to datetime
            data['date'] = pd.to_datetime(data['date'])
            
            # Group by date and calculate average price
            time_series = data.groupby('date')['price'].mean().sort_index()
            
            # Resample to monthly frequency if needed
            if len(time_series) > 12:  # Only resample if we have enough data
                time_series = time_series.resample('M').mean()
            
            # Remove any NaN values
            time_series = time_series.dropna()
            
            return time_series
            
        except Exception as e:
            logger.error(f"Error preparing time series data: {e}")
            return pd.Series()
    
    def _calculate_linear_trend(self, time_series: pd.Series) -> Dict[str, float]:
        """Calculate linear trend from time series data"""
        try:
            if len(time_series) < 2:
                return {'slope': 0, 'intercept': 0, 'r_squared': 0}
            
            # Create numeric index for regression
            X = np.arange(len(time_series)).reshape(-1, 1)
            y = time_series.values
            
            # Fit linear regression
            from sklearn.linear_model import LinearRegression
            model = LinearRegression()
            model.fit(X, y)
            
            # Calculate R-squared
            y_pred = model.predict(X)
            r_squared = r2_score(y, y_pred)
            
            return {
                'slope': model.coef_[0],
                'intercept': model.intercept_,
                'r_squared': r_squared,
                'trend_direction': 'increasing' if model.coef_[0] > 0 else 'decreasing'
            }
            
        except Exception as e:
            logger.error(f"Error calculating linear trend: {e}")
            return {'slope': 0, 'intercept': 0, 'r_squared': 0}
    
    def _analyze_seasonality(self, time_series: pd.Series) -> Dict[str, Any]:
        """Analyze seasonal patterns in the data"""
        try:
            if len(time_series) < 12:
                return {'seasonal_strength': 0, 'seasonal_pattern': 'insufficient_data'}
            
            # Calculate seasonal averages
            seasonal_avg = time_series.groupby(time_series.index.month).mean()
            
            # Calculate seasonal strength
            overall_mean = time_series.mean()
            seasonal_variance = ((seasonal_avg - overall_mean) ** 2).mean()
            total_variance = time_series.var()
            
            if total_variance > 0:
                seasonal_strength = seasonal_variance / total_variance
            else:
                seasonal_strength = 0
            
            # Identify peak and trough months
            peak_month = seasonal_avg.idxmax()
            trough_month = seasonal_avg.idxmin()
            
            return {
                'seasonal_strength': seasonal_strength,
                'seasonal_pattern': 'strong' if seasonal_strength > 0.3 else 'weak',
                'peak_month': peak_month,
                'trough_month': trough_month,
                'seasonal_averages': seasonal_avg.to_dict()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing seasonality: {e}")
            return {'seasonal_strength': 0, 'seasonal_pattern': 'error'}
    
    def _ml_trend_forecast(self, time_series: pd.Series, periods: int) -> Dict[str, Any]:
        """Make ML-based trend forecast"""
        try:
            if not ML_AVAILABLE or len(time_series) < 12:
                return {'forecast': [], 'confidence': 0}
            
            # Prepare features for ML model
            X, y = self._create_ml_features(time_series)
            
            if len(X) < 2:
                return {'forecast': [], 'confidence': 0}
            
            # Train trend model
            model = self.models.get('trend_rf')
            if model is None:
                return {'forecast': [], 'confidence': 0}
            
            model.fit(X, y)
            
            # Make future predictions
            future_features = self._create_future_features(time_series, periods)
            forecast = model.predict(future_features)
            
            return {
                'forecast': forecast.tolist(),
                'confidence': 0.8,  # Simplified confidence
                'model_type': 'RandomForest'
            }
            
        except Exception as e:
            logger.error(f"Error in ML trend forecast: {e}")
            return {'forecast': [], 'confidence': 0}
    
    def _create_ml_features(self, time_series: pd.Series) -> Tuple[np.ndarray, np.ndarray]:
        """Create features for ML models"""
        try:
            features = []
            targets = []
            
            # Use lagged values as features
            for i in range(6, len(time_series)):
                feature_row = [
                    time_series.iloc[i-1],  # Previous value
                    time_series.iloc[i-2],  # Two periods ago
                    time_series.iloc[i-3],  # Three periods ago
                    time_series.iloc[i-6],  # Six periods ago
                    time_series.iloc[i-12] if i >= 12 else time_series.iloc[i-6],  # Year ago
                    time_series.index[i].month,  # Month
                    time_series.index[i].year,   # Year
                ]
                features.append(feature_row)
                targets.append(time_series.iloc[i])
            
            return np.array(features), np.array(targets)
            
        except Exception as e:
            logger.error(f"Error creating ML features: {e}")
            return np.array([]), np.array([])
    
    def _create_future_features(self, time_series: pd.Series, periods: int) -> np.ndarray:
        """Create features for future predictions"""
        try:
            future_features = []
            last_date = time_series.index[-1]
            
            for i in range(1, periods + 1):
                future_date = last_date + pd.DateOffset(months=i)
                feature_row = [
                    time_series.iloc[-1],      # Last known value
                    time_series.iloc[-2],      # Second to last
                    time_series.iloc[-3],      # Third to last
                    time_series.iloc[-6] if len(time_series) >= 6 else time_series.iloc[-1],
                    time_series.iloc[-12] if len(time_series) >= 12 else time_series.iloc[-1],
                    future_date.month,
                    future_date.year
                ]
                future_features.append(feature_row)
            
            return np.array(future_features)
            
        except Exception as e:
            logger.error(f"Error creating future features: {e}")
            return np.array([])
    
    def _identify_market_phase(self, time_series: pd.Series) -> str:
        """Identify current market phase"""
        try:
            if len(time_series) < 6:
                return 'insufficient_data'
            
            # Calculate recent trend
            recent_data = time_series.tail(6)
            trend = self._calculate_linear_trend(recent_data)
            
            # Calculate volatility
            volatility = time_series.tail(12).std() / time_series.tail(12).mean()
            
            # Determine phase based on trend and volatility
            if trend['slope'] > 0 and trend['r_squared'] > 0.5:
                if volatility > 0.1:
                    return 'expansion_volatile'
                else:
                    return 'expansion_stable'
            elif trend['slope'] < 0 and trend['r_squared'] > 0.5:
                if volatility > 0.1:
                    return 'contraction_volatile'
                else:
                    return 'contraction_stable'
            else:
                if volatility > 0.15:
                    return 'transition_volatile'
                else:
                    return 'transition_stable'
                    
        except Exception as e:
            logger.error(f"Error identifying market phase: {e}")
            return 'unknown'
    
    def _estimate_cycle_length(self, time_series: pd.Series) -> int:
        """Estimate market cycle length in months"""
        try:
            if len(time_series) < 24:
                return 0
            
            # Simple autocorrelation-based estimation
            autocorr = time_series.autocorr(lag=12)
            
            if autocorr > 0.7:
                return 12  # Annual cycle
            elif autocorr > 0.5:
                return 24  # Biennial cycle
            elif autocorr > 0.3:
                return 36  # Triennial cycle
            else:
                return 48  # Four-year cycle
                
        except Exception as e:
            logger.error(f"Error estimating cycle length: {e}")
            return 0
    
    def _estimate_phase_duration(self, time_series: pd.Series) -> Dict[str, int]:
        """Estimate duration of different market phases"""
        try:
            if len(time_series) < 12:
                return {'expansion': 0, 'contraction': 0, 'transition': 0}
            
            # Simplified phase duration estimation
            # This is a basic implementation - more sophisticated methods could be used
            return {
                'expansion': 18,      # 18 months average
                'contraction': 12,    # 12 months average
                'transition': 6       # 6 months average
            }
            
        except Exception as e:
            logger.error(f"Error estimating phase duration: {e}")
            return {'expansion': 0, 'contraction': 0, 'transition': 0}
    
    def _measure_cycle_strength(self, time_series: pd.Series) -> float:
        """Measure the strength of market cycles"""
        try:
            if len(time_series) < 12:
                return 0.0
            
            # Calculate cycle strength using variance ratio
            overall_variance = time_series.var()
            
            if overall_variance == 0:
                return 0.0
            
            # Calculate trend-adjusted variance
            trend = self._calculate_linear_trend(time_series)
            if trend['r_squared'] > 0.5:
                # Remove trend effect
                trend_values = trend['slope'] * np.arange(len(time_series)) + trend['intercept']
                detrended = time_series.values - trend_values
                cycle_variance = np.var(detrended)
            else:
                cycle_variance = overall_variance
            
            # Cycle strength is the ratio of cycle variance to total variance
            cycle_strength = cycle_variance / overall_variance
            
            return min(1.0, max(0.0, cycle_strength))
            
        except Exception as e:
            logger.error(f"Error measuring cycle strength: {e}")
            return 0.0
    
    def _predict_next_phase(self, time_series: pd.Series) -> Dict[str, Any]:
        """Predict the next market phase"""
        try:
            current_phase = self._identify_market_phase(time_series)
            cycle_length = self._estimate_cycle_length(time_series)
            
            if current_phase == 'insufficient_data' or cycle_length == 0:
                return {'next_phase': 'unknown', 'confidence': 0}
            
            # Simple phase transition logic
            phase_transitions = {
                'expansion_stable': 'transition_stable',
                'expansion_volatile': 'transition_volatile',
                'contraction_stable': 'transition_stable',
                'contraction_volatile': 'transition_volatile',
                'transition_stable': 'expansion_stable',
                'transition_volatile': 'expansion_volatile'
            }
            
            next_phase = phase_transitions.get(current_phase, 'unknown')
            
            # Estimate timing
            phase_durations = self._estimate_phase_duration(time_series)
            current_phase_duration = phase_durations.get(current_phase.split('_')[0], 12)
            
            return {
                'next_phase': next_phase,
                'estimated_months': current_phase_duration,
                'confidence': 0.6  # Moderate confidence
            }
            
        except Exception as e:
            logger.error(f"Error predicting next phase: {e}")
            return {'next_phase': 'unknown', 'confidence': 0}
    
    def _calculate_cycle_indicators(self, time_series: pd.Series) -> Dict[str, float]:
        """Calculate various cycle indicators"""
        try:
            if len(time_series) < 12:
                return {}
            
            indicators = {}
            
            # Price momentum
            if len(time_series) >= 3:
                indicators['price_momentum'] = (time_series.iloc[-1] - time_series.iloc[-3]) / time_series.iloc[-3]
            
            # Volatility
            indicators['volatility'] = time_series.tail(12).std() / time_series.tail(12).mean()
            
            # Trend strength
            trend = self._calculate_linear_trend(time_series)
            indicators['trend_strength'] = trend['r_squared']
            
            # Cycle regularity
            indicators['cycle_regularity'] = self._measure_cycle_strength(time_series)
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating cycle indicators: {e}")
            return {}
    
    def _train_price_model(self, model, market_data: pd.DataFrame):
        """Train price prediction model"""
        try:
            if market_data.empty:
                return
            
            # Prepare training data
            X = []
            y = []
            
            for _, row in market_data.iterrows():
                features = [
                    row.get('bedrooms', 0),
                    row.get('bathrooms', 0),
                    row.get('square_feet', 0),
                    row.get('age', 0),
                    row.get('location_score', 0),
                    row.get('accessibility_score', 0),
                    row.get('amenity_score', 0)
                ]
                
                if all(isinstance(f, (int, float)) for f in features):
                    X.append(features)
                    y.append(row.get('price', 0))
            
            if len(X) > 10:  # Only train if we have enough data
                X = np.array(X)
                y = np.array(y)
                
                # Remove any NaN values
                mask = ~(np.isnan(X).any(axis=1) | np.isnan(y))
                X = X[mask]
                y = y[mask]
                
                if len(X) > 10:
                    model.fit(X, y)
                    model.fitted_ = True
                    logger.info(f"Price model {type(model).__name__} trained successfully")
            
        except Exception as e:
            logger.error(f"Error training price model: {e}")
    
    def _generate_trend_summary(self, trend_predictions: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of trend predictions"""
        try:
            summary = {
                'overall_trend': 'unknown',
                'trend_strength': 'weak',
                'seasonality': 'none',
                'forecast_confidence': 'low'
            }
            
            # Determine overall trend
            if 'linear_trend' in trend_predictions:
                trend = trend_predictions['linear_trend']
                if trend.get('r_squared', 0) > 0.7:
                    summary['trend_strength'] = 'strong'
                elif trend.get('r_squared', 0) > 0.4:
                    summary['trend_strength'] = 'moderate'
                
                if trend.get('slope', 0) > 0:
                    summary['overall_trend'] = 'increasing'
                elif trend.get('slope', 0) < 0:
                    summary['overall_trend'] = 'decreasing'
                else:
                    summary['overall_trend'] = 'stable'
            
            # Determine seasonality
            if 'seasonal_patterns' in trend_predictions:
                seasonal = trend_predictions['seasonal_patterns']
                if seasonal.get('seasonal_strength', 0) > 0.3:
                    summary['seasonality'] = 'strong'
                elif seasonal.get('seasonal_strength', 0) > 0.1:
                    summary['seasonality'] = 'moderate'
            
            # Determine forecast confidence
            if 'ml_forecast' in trend_predictions:
                ml_forecast = trend_predictions['ml_forecast']
                if ml_forecast.get('confidence', 0) > 0.8:
                    summary['forecast_confidence'] = 'high'
                elif ml_forecast.get('confidence', 0) > 0.6:
                    summary['forecast_confidence'] = 'medium'
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating trend summary: {e}")
            return {'overall_trend': 'unknown', 'trend_strength': 'weak'}
    
    def get_prediction_summary(self) -> Dict[str, Any]:
        """Get summary of all predictions made"""
        try:
            return {
                'total_predictions': len(self.prediction_history),
                'recent_predictions': self.prediction_history[-10:] if self.prediction_history else [],
                'model_performance': self.model_performance,
                'feature_importance': self.feature_importance
            }
        except Exception as e:
            logger.error(f"Error getting prediction summary: {e}")
            return {}

# Create global instance
market_predictor = MarketPredictor()
