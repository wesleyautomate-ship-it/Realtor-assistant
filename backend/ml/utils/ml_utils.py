"""
ML Utilities - Common Machine Learning Functions

This module provides utility functions for:
- Data validation and cleaning
- Model performance metrics
- Data transformation helpers
- ML pipeline utilities
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union, Any
from datetime import datetime, timedelta
import logging
import json
import pickle
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MLUtils:
    """Utility class for common ML operations"""
    
    def __init__(self):
        self.supported_formats = ['.csv', '.json', '.pkl', '.parquet']
        self.numeric_types = [np.int64, np.float64, int, float]
        
    def validate_data(self, data: Union[pd.DataFrame, np.ndarray, List, Dict]) -> bool:
        """
        Validate input data for ML operations
        
        Args:
            data: Input data to validate
            
        Returns:
            bool: True if data is valid, False otherwise
        """
        try:
            if data is None:
                logger.error("Data is None")
                return False
                
            if isinstance(data, pd.DataFrame):
                if data.empty:
                    logger.error("DataFrame is empty")
                    return False
                if data.isnull().all().all():
                    logger.error("DataFrame contains only null values")
                    return False
                    
            elif isinstance(data, np.ndarray):
                if data.size == 0:
                    logger.error("NumPy array is empty")
                    return False
                if np.isnan(data).all():
                    logger.error("NumPy array contains only NaN values")
                    return False
                    
            elif isinstance(data, List):
                if len(data) == 0:
                    logger.error("List is empty")
                    return False
                    
            elif isinstance(data, Dict):
                if len(data) == 0:
                    logger.error("Dictionary is empty")
                    return False
                    
            return True
            
        except Exception as e:
            logger.error(f"Data validation error: {e}")
            return False
    
    def clean_numeric_data(self, data: pd.Series, method: str = 'median') -> pd.Series:
        """
        Clean numeric data by handling missing values and outliers
        
        Args:
            data: Input numeric series
            method: Method for handling missing values ('median', 'mean', 'drop')
            
        Returns:
            pd.Series: Cleaned numeric data
        """
        try:
            if not self.validate_data(data):
                return data
                
            # Handle missing values
            if method == 'median':
                data = data.fillna(data.median())
            elif method == 'mean':
                data = data.fillna(data.mean())
            elif method == 'drop':
                data = data.dropna()
                
            # Handle outliers using IQR method
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Cap outliers instead of removing them
            data = data.clip(lower=lower_bound, upper=upper_bound)
            
            return data
            
        except Exception as e:
            logger.error(f"Error cleaning numeric data: {e}")
            return data
    
    def normalize_features(self, data: np.ndarray, method: str = 'standard') -> Tuple[np.ndarray, Dict]:
        """
        Normalize features using various methods
        
        Args:
            data: Input features array
            method: Normalization method ('standard', 'minmax', 'robust')
            
        Returns:
            Tuple[np.ndarray, Dict]: Normalized data and normalization parameters
        """
        try:
            if not self.validate_data(data):
                return data, {}
                
            params = {}
            
            if method == 'standard':
                # Z-score normalization
                mean = np.mean(data, axis=0)
                std = np.std(data, axis=0)
                data_normalized = (data - mean) / (std + 1e-8)
                params = {'mean': mean, 'std': std, 'method': 'standard'}
                
            elif method == 'minmax':
                # Min-max normalization
                min_val = np.min(data, axis=0)
                max_val = np.max(data, axis=0)
                data_normalized = (data - min_val) / (max_val - min_val + 1e-8)
                params = {'min': min_val, 'max': max_val, 'method': 'minmax'}
                
            elif method == 'robust':
                # Robust normalization using median and IQR
                median = np.median(data, axis=0)
                Q1 = np.percentile(data, 25, axis=0)
                Q3 = np.percentile(data, 75, axis=0)
                IQR = Q3 - Q1
                data_normalized = (data - median) / (IQR + 1e-8)
                params = {'median': median, 'IQR': IQR, 'method': 'robust'}
                
            else:
                logger.warning(f"Unknown normalization method: {method}. Using standard normalization.")
                return self.normalize_features(data, 'standard')
                
            return data_normalized, params
            
        except Exception as e:
            logger.error(f"Error normalizing features: {e}")
            return data, {}
    
    def calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        Calculate common ML performance metrics
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            Dict[str, float]: Dictionary of performance metrics
        """
        try:
            if not self.validate_data(y_true) or not self.validate_data(y_pred):
                return {}
                
            # Ensure arrays have same shape
            if y_true.shape != y_pred.shape:
                logger.error("Shape mismatch between y_true and y_pred")
                return {}
                
            # Calculate metrics
            metrics = {}
            
            # Mean Absolute Error
            metrics['mae'] = np.mean(np.abs(y_true - y_pred))
            
            # Mean Squared Error
            metrics['mse'] = np.mean((y_true - y_pred) ** 2)
            
            # Root Mean Squared Error
            metrics['rmse'] = np.sqrt(metrics['mse'])
            
            # Mean Absolute Percentage Error
            metrics['mape'] = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-8))) * 100
            
            # R-squared (coefficient of determination)
            ss_res = np.sum((y_true - y_pred) ** 2)
            ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
            metrics['r2'] = 1 - (ss_res / (ss_tot + 1e-8))
            
            # Adjusted R-squared
            n = len(y_true)
            p = 1  # Number of features (simplified)
            metrics['r2_adj'] = 1 - (1 - metrics['r2']) * (n - 1) / (n - p - 1)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating metrics: {e}")
            return {}
    
    def save_model(self, model: Any, filepath: str, format: str = 'pickle') -> bool:
        """
        Save ML model to file
        
        Args:
            model: ML model to save
            filepath: Path to save the model
            format: Save format ('pickle', 'joblib', 'json')
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            filepath = Path(filepath)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            if format == 'pickle':
                with open(filepath, 'wb') as f:
                    pickle.dump(model, f)
                    
            elif format == 'joblib':
                try:
                    import joblib
                    joblib.dump(model, filepath)
                except ImportError:
                    logger.warning("joblib not available, falling back to pickle")
                    with open(filepath, 'wb') as f:
                        pickle.dump(model, f)
                        
            elif format == 'json':
                if hasattr(model, 'get_params'):
                    params = model.get_params()
                    with open(filepath, 'w') as f:
                        json.dump(params, f, indent=2)
                else:
                    logger.warning("Model doesn't support JSON serialization, using pickle")
                    with open(filepath, 'wb') as f:
                        pickle.dump(model, f)
                        
            else:
                logger.warning(f"Unknown format: {format}. Using pickle.")
                with open(filepath, 'wb') as f:
                    pickle.dump(model, f)
                    
            logger.info(f"Model saved successfully to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            return False
    
    def load_model(self, filepath: str, format: str = 'pickle') -> Any:
        """
        Load ML model from file
        
        Args:
            filepath: Path to the saved model
            format: Save format ('pickle', 'joblib', 'json')
            
        Returns:
            Any: Loaded ML model
        """
        try:
            filepath = Path(filepath)
            
            if not filepath.exists():
                logger.error(f"Model file not found: {filepath}")
                return None
                
            if format == 'pickle':
                with open(filepath, 'rb') as f:
                    model = pickle.load(f)
                    
            elif format == 'joblib':
                try:
                    import joblib
                    model = joblib.load(filepath)
                except ImportError:
                    logger.warning("joblib not available, falling back to pickle")
                    with open(filepath, 'rb') as f:
                        model = pickle.load(f)
                        
            elif format == 'json':
                with open(filepath, 'r') as f:
                    params = json.load(f)
                # Note: JSON only stores parameters, not the full model
                logger.warning("JSON format only stores parameters, not the full model")
                return params
                
            else:
                logger.warning(f"Unknown format: {format}. Using pickle.")
                with open(filepath, 'rb') as f:
                    model = pickle.load(f)
                    
            logger.info(f"Model loaded successfully from {filepath}")
            return model
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return None
    
    def create_time_features(self, dates: pd.Series) -> pd.DataFrame:
        """
        Create time-based features from date series
        
        Args:
            dates: Series of dates
            
        Returns:
            pd.DataFrame: DataFrame with time features
        """
        try:
            if not self.validate_data(dates):
                return pd.DataFrame()
                
            # Convert to datetime if needed
            if not pd.api.types.is_datetime64_any_dtype(dates):
                dates = pd.to_datetime(dates)
                
            time_features = pd.DataFrame()
            
            # Basic time features
            time_features['year'] = dates.dt.year
            time_features['month'] = dates.dt.month
            time_features['day'] = dates.dt.day
            time_features['day_of_week'] = dates.dt.dayofweek
            time_features['day_of_year'] = dates.dt.dayofyear
            time_features['quarter'] = dates.dt.quarter
            
            # Cyclical features (better for ML models)
            time_features['month_sin'] = np.sin(2 * np.pi * dates.dt.month / 12)
            time_features['month_cos'] = np.cos(2 * np.pi * dates.dt.month / 12)
            time_features['day_sin'] = np.sin(2 * np.pi * dates.dt.day / 31)
            time_features['day_cos'] = np.cos(2 * np.pi * dates.dt.day / 31)
            
            # Seasonality features
            time_features['is_spring'] = dates.dt.month.isin([3, 4, 5]).astype(int)
            time_features['is_summer'] = dates.dt.month.isin([6, 7, 8]).astype(int)
            time_features['is_fall'] = dates.dt.month.isin([9, 10, 11]).astype(int)
            time_features['is_winter'] = dates.dt.month.isin([12, 1, 2]).astype(int)
            
            # Holiday features (simplified)
            time_features['is_weekend'] = dates.dt.dayofweek.isin([5, 6]).astype(int)
            
            return time_features
            
        except Exception as e:
            logger.error(f"Error creating time features: {e}")
            return pd.DataFrame()
    
    def handle_categorical_features(self, data: pd.DataFrame, method: str = 'onehot') -> Tuple[pd.DataFrame, Dict]:
        """
        Handle categorical features using various encoding methods
        
        Args:
            data: Input DataFrame
            method: Encoding method ('onehot', 'label', 'target')
            
        Returns:
            Tuple[pd.DataFrame, Dict]: Encoded DataFrame and encoding parameters
        """
        try:
            if not self.validate_data(data):
                return data, {}
                
            # Identify categorical columns
            categorical_cols = data.select_dtypes(include=['object', 'category']).columns
            if len(categorical_cols) == 0:
                return data, {}
                
            encoded_data = data.copy()
            encoding_params = {}
            
            for col in categorical_cols:
                if method == 'onehot':
                    # One-hot encoding
                    dummies = pd.get_dummies(data[col], prefix=col, drop_first=True)
                    encoded_data = pd.concat([encoded_data, dummies], axis=1)
                    encoded_data.drop(col, axis=1, inplace=True)
                    encoding_params[col] = {'method': 'onehot', 'columns': dummies.columns.tolist()}
                    
                elif method == 'label':
                    # Label encoding
                    from sklearn.preprocessing import LabelEncoder
                    le = LabelEncoder()
                    encoded_data[col] = le.fit_transform(data[col])
                    encoding_params[col] = {'method': 'label', 'classes': le.classes_.tolist()}
                    
                elif method == 'target':
                    # Target encoding (mean encoding)
                    target_col = None
                    # Find a numeric column to use as target (simplified)
                    numeric_cols = data.select_dtypes(include=self.numeric_types).columns
                    if len(numeric_cols) > 0:
                        target_col = numeric_cols[0]
                        target_means = data.groupby(col)[target_col].mean()
                        encoded_data[col] = data[col].map(target_means)
                        encoding_params[col] = {'method': 'target', 'target_means': target_means.to_dict()}
                    else:
                        logger.warning(f"No numeric columns found for target encoding of {col}")
                        # Fall back to label encoding
                        from sklearn.preprocessing import LabelEncoder
                        le = LabelEncoder()
                        encoded_data[col] = le.fit_transform(data[col])
                        encoding_params[col] = {'method': 'label', 'classes': le.classes_.tolist()}
                        
            return encoded_data, encoding_params
            
        except Exception as e:
            logger.error(f"Error handling categorical features: {e}")
            return data, {}
    
    def split_data(self, data: pd.DataFrame, target_col: str, test_size: float = 0.2, 
                   val_size: float = 0.1, random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Split data into train, validation, and test sets
        
        Args:
            data: Input DataFrame
            target_col: Name of target column
            test_size: Proportion of data for test set
            val_size: Proportion of data for validation set
            random_state: Random seed for reproducibility
            
        Returns:
            Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Train, validation, and test DataFrames
        """
        try:
            if not self.validate_data(data):
                return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
                
            if target_col not in data.columns:
                logger.error(f"Target column '{target_col}' not found in data")
                return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
                
            # Calculate split sizes
            total_size = len(data)
            test_size_actual = int(total_size * test_size)
            val_size_actual = int(total_size * val_size)
            train_size_actual = total_size - test_size_actual - val_size_actual
            
            # Shuffle data
            data_shuffled = data.sample(frac=1, random_state=random_state).reset_index(drop=True)
            
            # Split data
            train_data = data_shuffled.iloc[:train_size_actual]
            val_data = data_shuffled.iloc[train_size_actual:train_size_actual + val_size_actual]
            test_data = data_shuffled.iloc[train_size_actual + val_size_actual:]
            
            logger.info(f"Data split: Train={len(train_data)}, Validation={len(val_data)}, Test={len(test_data)}")
            
            return train_data, val_data, test_data
            
        except Exception as e:
            logger.error(f"Error splitting data: {e}")
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# Create global instance
ml_utils = MLUtils()
