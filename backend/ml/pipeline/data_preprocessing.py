"""
Data Preprocessing Pipeline - Data Cleaning and Preparation

This module provides:
- Data validation and cleaning
- Feature preprocessing
- Data transformation
- Quality assurance
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union, Any
import logging
from datetime import datetime, timedelta
import re
from pathlib import Path
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataPreprocessor:
    """Comprehensive data preprocessing for real estate ML models"""
    
    def __init__(self):
        self.preprocessing_config = {
            'missing_value_strategy': 'median',  # 'median', 'mean', 'drop', 'interpolate'
            'outlier_strategy': 'iqr',  # 'iqr', 'zscore', 'isolation_forest'
            'scaling_method': 'robust',  # 'standard', 'minmax', 'robust'
            'categorical_encoding': 'onehot',  # 'onehot', 'label', 'target'
            'date_features': True,
            'text_features': True,
            'geographic_features': True
        }
        self.preprocessing_history = []
        self.feature_stats = {}
        
    def load_data(self, file_path: str, file_type: str = 'auto') -> pd.DataFrame:
        """
        Load data from various file formats
        
        Args:
            file_path: Path to the data file
            file_type: Type of file ('csv', 'json', 'excel', 'parquet', 'auto')
            
        Returns:
            pd.DataFrame: Loaded data
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Auto-detect file type if not specified
            if file_type == 'auto':
                suffix = file_path.suffix.lower()
                if suffix == '.csv':
                    file_type = 'csv'
                elif suffix == '.json':
                    file_type = 'json'
                elif suffix in ['.xlsx', '.xls']:
                    file_type = 'excel'
                elif suffix == '.parquet':
                    file_type = 'parquet'
                else:
                    file_type = 'csv'  # Default to CSV
            
            # Load data based on file type
            if file_type == 'csv':
                data = pd.read_csv(file_path)
            elif file_type == 'json':
                data = pd.read_json(file_path)
            elif file_type == 'excel':
                data = pd.read_excel(file_path)
            elif file_type == 'parquet':
                data = pd.read_parquet(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            logger.info(f"Data loaded successfully from {file_path}")
            logger.info(f"Shape: {data.shape}, Columns: {list(data.columns)}")
            
            return data
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return pd.DataFrame()
    
    def validate_data_quality(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Comprehensive data quality validation
        
        Args:
            data: Input DataFrame
            
        Returns:
            Dict[str, Any]: Data quality report
        """
        try:
            if data.empty:
                return {'status': 'error', 'message': 'Data is empty'}
            
            quality_report = {
                'timestamp': datetime.now().isoformat(),
                'data_shape': data.shape,
                'total_rows': len(data),
                'total_columns': len(data.columns),
                'missing_values': {},
                'duplicate_rows': data.duplicated().sum(),
                'data_types': {},
                'unique_values': {},
                'outliers': {},
                'quality_score': 0.0
            }
            
            # Analyze each column
            for col in data.columns:
                col_data = data[col]
                
                # Missing values
                missing_count = col_data.isnull().sum()
                missing_pct = (missing_count / len(data)) * 100
                quality_report['missing_values'][col] = {
                    'count': missing_count,
                    'percentage': missing_pct
                }
                
                # Data types
                quality_report['data_types'][col] = str(col_data.dtype)
                
                # Unique values
                unique_count = col_data.nunique()
                quality_report['unique_values'][col] = {
                    'count': unique_count,
                    'percentage': (unique_count / len(data)) * 100
                }
                
                # Outlier detection for numeric columns
                if pd.api.types.is_numeric_dtype(col_data):
                    outliers = self._detect_outliers_iqr(col_data)
                    quality_report['outliers'][col] = {
                        'count': len(outliers),
                        'percentage': (len(outliers) / len(data)) * 100
                    }
            
            # Calculate overall quality score
            quality_score = self._calculate_quality_score(quality_report)
            quality_report['quality_score'] = quality_score
            
            # Store in history
            self.preprocessing_history.append({
                'action': 'data_quality_validation',
                'timestamp': datetime.now().isoformat(),
                'quality_score': quality_score
            })
            
            logger.info(f"Data quality validation completed. Score: {quality_score:.2f}")
            return quality_report
            
        except Exception as e:
            logger.error(f"Error in data quality validation: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def clean_data(self, data: pd.DataFrame, cleaning_config: Optional[Dict] = None) -> pd.DataFrame:
        """
        Clean data based on configuration
        
        Args:
            data: Input DataFrame
            cleaning_config: Cleaning configuration dictionary
            
        Returns:
            pd.DataFrame: Cleaned data
        """
        try:
            if data.empty:
                return data
            
            # Use default config if none provided
            if cleaning_config is None:
                cleaning_config = self.preprocessing_config
            
            cleaned_data = data.copy()
            cleaning_log = {
                'action': 'data_cleaning',
                'timestamp': datetime.now().isoformat(),
                'original_shape': data.shape,
                'changes_made': []
            }
            
            # Handle missing values
            if cleaning_config.get('missing_value_strategy') != 'drop':
                cleaned_data = self._handle_missing_values(cleaned_data, cleaning_config)
                cleaning_log['changes_made'].append('missing_values_handled')
            
            # Handle outliers
            if cleaning_config.get('outlier_strategy') != 'none':
                cleaned_data = self._handle_outliers(cleaned_data, cleaning_config)
                cleaning_log['changes_made'].append('outliers_handled')
            
            # Remove duplicate rows
            original_duplicates = cleaned_data.duplicated().sum()
            cleaned_data = cleaned_data.drop_duplicates()
            if original_duplicates > 0:
                cleaning_log['changes_made'].append(f'duplicates_removed_{original_duplicates}')
            
            # Clean column names
            cleaned_data = self._clean_column_names(cleaned_data)
            cleaning_log['changes_made'].append('column_names_cleaned')
            
            # Store cleaning log
            cleaning_log['final_shape'] = cleaned_data.shape
            cleaning_log['rows_removed'] = data.shape[0] - cleaned_data.shape[0]
            self.preprocessing_history.append(cleaning_log)
            
            logger.info(f"Data cleaning completed. Shape: {data.shape} → {cleaned_data.shape}")
            return cleaned_data
            
        except Exception as e:
            logger.error(f"Error in data cleaning: {e}")
            return data
    
    def create_features(self, data: pd.DataFrame, feature_config: Optional[Dict] = None) -> pd.DataFrame:
        """
        Create new features from existing data
        
        Args:
            data: Input DataFrame
            feature_config: Feature creation configuration
            
        Returns:
            pd.DataFrame: DataFrame with new features
        """
        try:
            if data.empty:
                return data
            
            if feature_config is None:
                feature_config = self.preprocessing_config
            
            enhanced_data = data.copy()
            feature_log = {
                'action': 'feature_creation',
                'timestamp': datetime.now().isoformat(),
                'original_columns': list(data.columns),
                'new_features': []
            }
            
            # Create time-based features
            if feature_config.get('date_features', True):
                enhanced_data = self._create_time_features(enhanced_data)
                feature_log['new_features'].extend(['time_features_created'])
            
            # Create text-based features
            if feature_config.get('text_features', True):
                enhanced_data = self._create_text_features(enhanced_data)
                feature_log['new_features'].extend(['text_features_created'])
            
            # Create geographic features
            if feature_config.get('geographic_features', True):
                enhanced_data = self._create_geographic_features(enhanced_data)
                feature_log['new_features'].extend(['geographic_features_created'])
            
            # Create interaction features
            enhanced_data = self._create_interaction_features(enhanced_data)
            feature_log['new_features'].extend(['interaction_features_created'])
            
            # Store feature creation log
            feature_log['final_columns'] = list(enhanced_data.columns)
            feature_log['new_columns_count'] = len(enhanced_data.columns) - len(data.columns)
            self.preprocessing_history.append(feature_log)
            
            logger.info(f"Feature creation completed. Columns: {len(data.columns)} → {len(enhanced_data.columns)}")
            return enhanced_data
            
        except Exception as e:
            logger.error(f"Error in feature creation: {e}")
            return data
    
    def prepare_ml_data(self, data: pd.DataFrame, target_column: str,
                        feature_columns: Optional[List[str]] = None,
                        test_size: float = 0.2, random_state: int = 42) -> Dict[str, Any]:
        """
        Prepare data for machine learning models
        
        Args:
            data: Input DataFrame
            target_column: Name of target column
            feature_columns: List of feature columns (if None, use all except target)
            test_size: Proportion of data for test set
            random_state: Random seed for reproducibility
            
        Returns:
            Dict[str, Any]: Prepared data dictionary
        """
        try:
            if data.empty:
                return {}
            
            if target_column not in data.columns:
                raise ValueError(f"Target column '{target_column}' not found in data")
            
            # Determine feature columns
            if feature_columns is None:
                feature_columns = [col for col in data.columns if col != target_column]
            
            # Validate feature columns
            missing_features = [col for col in feature_columns if col not in data.columns]
            if missing_features:
                raise ValueError(f"Feature columns not found: {missing_features}")
            
            # Prepare features and target
            X = data[feature_columns].copy()
            y = data[target_column].copy()
            
            # Handle categorical features
            X_encoded, encoding_params = self._encode_categorical_features(X)
            
            # Handle missing values in features
            X_encoded = self._handle_missing_values(X_encoded, self.preprocessing_config)
            
            # Split data
            from sklearn.model_selection import train_test_split
            X_train, X_test, y_train, y_test = train_test_split(
                X_encoded, y, test_size=test_size, random_state=random_state
            )
            
            # Store feature statistics
            self.feature_stats = {
                'feature_columns': feature_columns,
                'target_column': target_column,
                'encoding_params': encoding_params,
                'data_shapes': {
                    'X_train': X_train.shape,
                    'X_test': X_test.shape,
                    'y_train': y_train.shape,
                    'y_test': y_test.shape
                }
            }
            
            # Store preparation log
            preparation_log = {
                'action': 'ml_data_preparation',
                'timestamp': datetime.now().isoformat(),
                'target_column': target_column,
                'feature_columns': feature_columns,
                'test_size': test_size,
                'encoding_params': encoding_params
            }
            self.preprocessing_history.append(preparation_log)
            
            logger.info(f"ML data preparation completed. Train: {X_train.shape}, Test: {X_test.shape}")
            
            return {
                'X_train': X_train,
                'X_test': X_test,
                'y_train': y_train,
                'y_test': y_test,
                'feature_columns': feature_columns,
                'encoding_params': encoding_params
            }
            
        except Exception as e:
            logger.error(f"Error in ML data preparation: {e}")
            return {}
    
    def _handle_missing_values(self, data: pd.DataFrame, config: Dict) -> pd.DataFrame:
        """Handle missing values based on configuration"""
        try:
            cleaned_data = data.copy()
            
            for col in cleaned_data.columns:
                if cleaned_data[col].isnull().any():
                    strategy = config.get('missing_value_strategy', 'median')
                    
                    if strategy == 'drop':
                        cleaned_data = cleaned_data.dropna(subset=[col])
                    elif strategy == 'median' and pd.api.types.is_numeric_dtype(cleaned_data[col]):
                        cleaned_data[col] = cleaned_data[col].fillna(cleaned_data[col].median())
                    elif strategy == 'mean' and pd.api.types.is_numeric_dtype(cleaned_data[col]):
                        cleaned_data[col] = cleaned_data[col].fillna(cleaned_data[col].mean())
                    elif strategy == 'interpolate':
                        cleaned_data[col] = cleaned_data[col].interpolate(method='linear')
                    elif strategy == 'mode':
                        mode_value = cleaned_data[col].mode()[0] if not cleaned_data[col].mode().empty else 'Unknown'
                        cleaned_data[col] = cleaned_data[col].fillna(mode_value)
            
            return cleaned_data
            
        except Exception as e:
            logger.error(f"Error handling missing values: {e}")
            return data
    
    def _handle_outliers(self, data: pd.DataFrame, config: Dict) -> pd.DataFrame:
        """Handle outliers based on configuration"""
        try:
            cleaned_data = data.copy()
            strategy = config.get('outlier_strategy', 'iqr')
            
            for col in cleaned_data.columns:
                if pd.api.types.is_numeric_dtype(cleaned_data[col]):
                    if strategy == 'iqr':
                        outliers = self._detect_outliers_iqr(cleaned_data[col])
                        if len(outliers) > 0:
                            # Cap outliers instead of removing
                            Q1 = cleaned_data[col].quantile(0.25)
                            Q3 = cleaned_data[col].quantile(0.75)
                            IQR = Q3 - Q1
                            lower_bound = Q1 - 1.5 * IQR
                            upper_bound = Q3 + 1.5 * IQR
                            cleaned_data[col] = cleaned_data[col].clip(lower=lower_bound, upper=upper_bound)
                    
                    elif strategy == 'zscore':
                        z_scores = np.abs((cleaned_data[col] - cleaned_data[col].mean()) / cleaned_data[col].std())
                        outliers = z_scores > 3
                        if outliers.any():
                            # Cap outliers at 3 standard deviations
                            mean_val = cleaned_data[col].mean()
                            std_val = cleaned_data[col].std()
                            cleaned_data[col] = cleaned_data[col].clip(
                                lower=mean_val - 3 * std_val,
                                upper=mean_val + 3 * std_val
                            )
            
            return cleaned_data
            
        except Exception as e:
            logger.error(f"Error handling outliers: {e}")
            return data
    
    def _detect_outliers_iqr(self, series: pd.Series) -> pd.Series:
        """Detect outliers using IQR method"""
        try:
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return series[(series < lower_bound) | (series > upper_bound)]
        except Exception as e:
            logger.error(f"Error detecting outliers: {e}")
            return pd.Series()
    
    def _clean_column_names(self, data: pd.DataFrame) -> pd.DataFrame:
        """Clean column names for consistency"""
        try:
            cleaned_data = data.copy()
            
            # Convert to lowercase
            cleaned_data.columns = cleaned_data.columns.str.lower()
            
            # Replace spaces and special characters with underscores
            cleaned_data.columns = cleaned_data.columns.str.replace(r'[^a-zA-Z0-9_]', '_', regex=True)
            
            # Remove multiple consecutive underscores
            cleaned_data.columns = cleaned_data.columns.str.replace(r'_+', '_', regex=True)
            
            # Remove leading/trailing underscores
            cleaned_data.columns = cleaned_data.columns.str.strip('_')
            
            return cleaned_data
            
        except Exception as e:
            logger.error(f"Error cleaning column names: {e}")
            return data
    
    def _create_time_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create time-based features from date columns"""
        try:
            enhanced_data = data.copy()
            date_columns = []
            
            # Identify date columns
            for col in enhanced_data.columns:
                if pd.api.types.is_datetime64_any_dtype(enhanced_data[col]):
                    date_columns.append(col)
                elif enhanced_data[col].dtype == 'object':
                    # Try to convert to datetime
                    try:
                        enhanced_data[col] = pd.to_datetime(enhanced_data[col], errors='coerce')
                        if not enhanced_data[col].isnull().all():
                            date_columns.append(col)
                    except:
                        pass
            
            # Create time features for each date column
            for col in date_columns:
                if enhanced_data[col].isnull().all():
                    continue
                
                # Basic time features
                enhanced_data[f'{col}_year'] = enhanced_data[col].dt.year
                enhanced_data[f'{col}_month'] = enhanced_data[col].dt.month
                enhanced_data[f'{col}_day'] = enhanced_data[col].dt.day
                enhanced_data[f'{col}_day_of_week'] = enhanced_data[col].dt.dayofweek
                enhanced_data[f'{col}_quarter'] = enhanced_data[col].dt.quarter
                
                # Cyclical features
                enhanced_data[f'{col}_month_sin'] = np.sin(2 * np.pi * enhanced_data[col].dt.month / 12)
                enhanced_data[f'{col}_month_cos'] = np.cos(2 * np.pi * enhanced_data[col].dt.month / 12)
                
                # Seasonality
                enhanced_data[f'{col}_is_spring'] = enhanced_data[col].dt.month.isin([3, 4, 5]).astype(int)
                enhanced_data[f'{col}_is_summer'] = enhanced_data[col].dt.month.isin([6, 7, 8]).astype(int)
                enhanced_data[f'{col}_is_fall'] = enhanced_data[col].dt.month.isin([9, 10, 11]).astype(int)
                enhanced_data[f'{col}_is_winter'] = enhanced_data[col].dt.month.isin([12, 1, 2]).astype(int)
            
            return enhanced_data
            
        except Exception as e:
            logger.error(f"Error creating time features: {e}")
            return data
    
    def _create_text_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create text-based features"""
        try:
            enhanced_data = data.copy()
            text_columns = []
            
            # Identify text columns
            for col in enhanced_data.columns:
                if enhanced_data[col].dtype == 'object' and not pd.api.types.is_datetime64_any_dtype(enhanced_data[col]):
                    text_columns.append(col)
            
            # Create text features
            for col in text_columns:
                if enhanced_data[col].isnull().all():
                    continue
                
                # Text length
                enhanced_data[f'{col}_length'] = enhanced_data[col].astype(str).str.len()
                
                # Word count
                enhanced_data[f'{col}_word_count'] = enhanced_data[col].astype(str).str.split().str.len()
                
                # Character count (excluding spaces)
                enhanced_data[f'{col}_char_count'] = enhanced_data[col].astype(str).str.replace(' ', '').str.len()
                
                # Has numbers
                enhanced_data[f'{col}_has_numbers'] = enhanced_data[col].astype(str).str.contains(r'\d').astype(int)
                
                # Has special characters
                enhanced_data[f'{col}_has_special'] = enhanced_data[col].astype(str).str.contains(r'[^a-zA-Z0-9\s]').astype(int)
            
            return enhanced_data
            
        except Exception as e:
            logger.error(f"Error creating text features: {e}")
            return data
    
    def _create_geographic_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create geographic features from location data"""
        try:
            enhanced_data = data.copy()
            
            # Look for common location-related columns
            location_indicators = ['address', 'city', 'state', 'country', 'zip', 'postal', 'location', 'area']
            
            for col in enhanced_data.columns:
                col_lower = col.lower()
                if any(indicator in col_lower for indicator in location_indicators):
                    # Create location-based features
                    if enhanced_data[col].dtype == 'object':
                        # Location type (city, state, etc.)
                        enhanced_data[f'{col}_type'] = col
                        
                        # Location length
                        enhanced_data[f'{col}_length'] = enhanced_data[col].astype(str).str.len()
                        
                        # Has coordinates (simplified check)
                        enhanced_data[f'{col}_has_coords'] = enhanced_data[col].astype(str).str.contains(r'[-+]?\d+\.\d+').astype(int)
            
            return enhanced_data
            
        except Exception as e:
            logger.error(f"Error creating geographic features: {e}")
            return data
    
    def _create_interaction_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create interaction features between numeric columns"""
        try:
            enhanced_data = data.copy()
            numeric_columns = enhanced_data.select_dtypes(include=[np.number]).columns.tolist()
            
            # Create interaction features for pairs of numeric columns
            if len(numeric_columns) >= 2:
                for i in range(len(numeric_columns)):
                    for j in range(i + 1, len(numeric_columns)):
                        col1, col2 = numeric_columns[i], numeric_columns[j]
                        
                        # Multiplication
                        enhanced_data[f'{col1}_x_{col2}'] = enhanced_data[col1] * enhanced_data[col2]
                        
                        # Division (with safety check)
                        if (enhanced_data[col2] != 0).all():
                            enhanced_data[f'{col1}_div_{col2}'] = enhanced_data[col1] / enhanced_data[col2]
                        
                        # Sum
                        enhanced_data[f'{col1}_plus_{col2}'] = enhanced_data[col1] + enhanced_data[col2]
                        
                        # Difference
                        enhanced_data[f'{col1}_minus_{col2}'] = enhanced_data[col1] - enhanced_data[col2]
            
            return enhanced_data
            
        except Exception as e:
            logger.error(f"Error creating interaction features: {e}")
            return data
    
    def _encode_categorical_features(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Encode categorical features"""
        try:
            encoded_data = data.copy()
            encoding_params = {}
            
            categorical_columns = encoded_data.select_dtypes(include=['object', 'category']).columns
            
            for col in categorical_columns:
                if encoded_data[col].nunique() <= 50:  # Only encode if reasonable number of categories
                    # One-hot encoding for categorical variables
                    dummies = pd.get_dummies(encoded_data[col], prefix=col, drop_first=True)
                    encoded_data = pd.concat([encoded_data, dummies], axis=1)
                    encoded_data.drop(col, axis=1, inplace=True)
                    
                    encoding_params[col] = {
                        'method': 'onehot',
                        'columns': dummies.columns.tolist()
                    }
            
            return encoded_data, encoding_params
            
        except Exception as e:
            logger.error(f"Error encoding categorical features: {e}")
            return data, {}
    
    def _calculate_quality_score(self, quality_report: Dict) -> float:
        """Calculate overall data quality score"""
        try:
            score = 100.0
            
            # Penalize for missing values
            for col, missing_info in quality_report.get('missing_values', {}).items():
                missing_pct = missing_info.get('percentage', 0)
                if missing_pct > 50:
                    score -= 30
                elif missing_pct > 20:
                    score -= 15
                elif missing_pct > 10:
                    score -= 5
            
            # Penalize for duplicates
            duplicate_pct = (quality_report.get('duplicate_rows', 0) / quality_report.get('total_rows', 1)) * 100
            if duplicate_pct > 10:
                score -= 20
            elif duplicate_pct > 5:
                score -= 10
            
            # Penalize for outliers
            for col, outlier_info in quality_report.get('outliers', {}).items():
                outlier_pct = outlier_info.get('percentage', 0)
                if outlier_pct > 10:
                    score -= 10
                elif outlier_pct > 5:
                    score -= 5
            
            return max(0.0, score)
            
        except Exception as e:
            logger.error(f"Error calculating quality score: {e}")
            return 0.0
    
    def get_preprocessing_summary(self) -> Dict[str, Any]:
        """Get summary of all preprocessing operations"""
        try:
            return {
                'total_operations': len(self.preprocessing_history),
                'operations': self.preprocessing_history,
                'feature_stats': self.feature_stats,
                'config': self.preprocessing_config
            }
        except Exception as e:
            logger.error(f"Error getting preprocessing summary: {e}")
            return {}

# Create global instance
data_preprocessor = DataPreprocessor()
