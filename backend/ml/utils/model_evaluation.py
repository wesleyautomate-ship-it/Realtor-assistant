"""
Model Evaluation - Comprehensive ML Model Assessment

This module provides tools for:
- Model performance evaluation
- Cross-validation strategies
- Hyperparameter tuning
- Model comparison and selection
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union, Any
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    classification_report, confusion_matrix, accuracy_score,
    precision_score, recall_score, f1_score, roc_auc_score
)
from sklearn.model_selection import (
    cross_val_score, GridSearchCV, RandomizedSearchCV,
    train_test_split, KFold, StratifiedKFold
)
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelEvaluator:
    """Comprehensive model evaluation and validation"""
    
    def __init__(self):
        self.evaluation_history = []
        self.best_models = {}
        
    def evaluate_regression_model(self, model: Any, X_test: np.ndarray, y_test: np.ndarray,
                                X_train: Optional[np.ndarray] = None, y_train: Optional[np.ndarray] = None,
                                model_name: str = "Unknown") -> Dict[str, float]:
        """
        Evaluate regression model performance
        
        Args:
            model: Trained regression model
            X_test: Test features
            y_test: Test targets
            X_train: Training features (optional, for overfitting check)
            y_train: Training targets (optional, for overfitting check)
            model_name: Name of the model for logging
            
        Returns:
            Dict[str, float]: Dictionary of evaluation metrics
        """
        try:
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Calculate basic metrics
            metrics = {
                'model_name': model_name,
                'evaluation_date': datetime.now().isoformat(),
                'mae': mean_absolute_error(y_test, y_pred),
                'mse': mean_squared_error(y_test, y_pred),
                'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
                'r2': r2_score(y_test, y_pred),
                'mape': np.mean(np.abs((y_test - y_pred) / (y_test + 1e-8))) * 100
            }
            
            # Check for overfitting if training data provided
            if X_train is not None and y_train is not None:
                y_train_pred = model.predict(X_train)
                train_r2 = r2_score(y_train, y_train_pred)
                metrics['train_r2'] = train_r2
                metrics['overfitting_score'] = train_r2 - metrics['r2']
                
            # Calculate additional metrics
            metrics['explained_variance'] = np.var(y_pred) / np.var(y_test) if np.var(y_test) > 0 else 0
            metrics['max_error'] = np.max(np.abs(y_test - y_pred))
            metrics['mean_absolute_percentage_error'] = metrics['mape']
            
            # Store evaluation results
            self.evaluation_history.append(metrics)
            
            logger.info(f"Regression model '{model_name}' evaluation completed")
            logger.info(f"R² Score: {metrics['r2']:.4f}, RMSE: {metrics['rmse']:.4f}")
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error evaluating regression model: {e}")
            return {}
    
    def evaluate_classification_model(self, model: Any, X_test: np.ndarray, y_test: np.ndarray,
                                   X_train: Optional[np.ndarray] = None, y_train: Optional[np.ndarray] = None,
                                   model_name: str = "Unknown", average: str = 'weighted') -> Dict[str, float]:
        """
        Evaluate classification model performance
        
        Args:
            model: Trained classification model
            X_test: Test features
            y_test: Test targets
            X_train: Training features (optional, for overfitting check)
            y_train: Training targets (optional, for overfitting check)
            model_name: Name of the model for logging
            average: Averaging method for multi-class metrics
            
        Returns:
            Dict[str, float]: Dictionary of evaluation metrics
        """
        try:
            # Make predictions
            y_pred = model.predict(X_test)
            y_pred_proba = None
            
            # Try to get prediction probabilities if available
            try:
                y_pred_proba = model.predict_proba(X_test)
            except:
                pass
            
            # Calculate basic metrics
            metrics = {
                'model_name': model_name,
                'evaluation_date': datetime.now().isoformat(),
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, average=average, zero_division=0),
                'recall': recall_score(y_test, y_pred, average=average, zero_division=0),
                'f1': f1_score(y_test, y_pred, average=average, zero_division=0)
            }
            
            # Calculate ROC AUC if probabilities available and binary classification
            if y_pred_proba is not None and len(np.unique(y_test)) == 2:
                try:
                    metrics['roc_auc'] = roc_auc_score(y_test, y_pred_proba[:, 1])
                except:
                    pass
            
            # Check for overfitting if training data provided
            if X_train is not None and y_train is not None:
                y_train_pred = model.predict(X_train)
                train_accuracy = accuracy_score(y_train, y_train_pred)
                metrics['train_accuracy'] = train_accuracy
                metrics['overfitting_score'] = train_accuracy - metrics['accuracy']
            
            # Store evaluation results
            self.evaluation_history.append(metrics)
            
            logger.info(f"Classification model '{model_name}' evaluation completed")
            logger.info(f"Accuracy: {metrics['accuracy']:.4f}, F1: {metrics['f1']:.4f}")
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error evaluating classification model: {e}")
            return {}
    
    def cross_validate_model(self, model: Any, X: np.ndarray, y: np.ndarray,
                           cv_folds: int = 5, scoring: str = 'r2',
                           model_name: str = "Unknown") -> Dict[str, float]:
        """
        Perform cross-validation on a model
        
        Args:
            model: Model to cross-validate
            X: Features
            y: Targets
            cv_folds: Number of cross-validation folds
            scoring: Scoring metric
            model_name: Name of the model for logging
            
        Returns:
            Dict[str, float]: Cross-validation results
        """
        try:
            # Perform cross-validation
            cv_scores = cross_val_score(model, X, y, cv=cv_folds, scoring=scoring)
            
            # Calculate statistics
            cv_results = {
                'model_name': model_name,
                'cv_folds': cv_folds,
                'scoring': scoring,
                'cv_scores': cv_scores.tolist(),
                'mean_score': np.mean(cv_scores),
                'std_score': np.std(cv_scores),
                'min_score': np.min(cv_scores),
                'max_score': np.max(cv_scores),
                'evaluation_date': datetime.now().isoformat()
            }
            
            # Store results
            self.evaluation_history.append(cv_results)
            
            logger.info(f"Cross-validation for '{model_name}' completed")
            logger.info(f"Mean {scoring}: {cv_results['mean_score']:.4f} ± {cv_results['std_score']:.4f}")
            
            return cv_results
            
        except Exception as e:
            logger.error(f"Error in cross-validation: {e}")
            return {}
    
    def hyperparameter_tuning(self, model: Any, param_grid: Dict, X: np.ndarray, y: np.ndarray,
                             cv_folds: int = 5, scoring: str = 'r2', n_iter: int = 100,
                             model_name: str = "Unknown") -> Dict[str, Any]:
        """
        Perform hyperparameter tuning using grid search or random search
        
        Args:
            model: Base model for tuning
            param_grid: Parameter grid to search
            X: Features
            y: Targets
            cv_folds: Number of cross-validation folds
            scoring: Scoring metric
            n_iter: Number of iterations for random search
            model_name: Name of the model for logging
            
        Returns:
            Dict[str, Any]: Tuning results and best model
        """
        try:
            # Choose search method based on parameter grid size
            if len(param_grid) <= 20:  # Small grid, use GridSearchCV
                search = GridSearchCV(
                    model, param_grid, cv=cv_folds, scoring=scoring,
                    n_jobs=-1, verbose=1
                )
                search_method = "GridSearchCV"
            else:  # Large grid, use RandomizedSearchCV
                search = RandomizedSearchCV(
                    model, param_grid, n_iter=n_iter, cv=cv_folds,
                    scoring=scoring, n_jobs=-1, verbose=1, random_state=42
                )
                search_method = "RandomizedSearchCV"
            
            # Perform search
            search.fit(X, y)
            
            # Extract results
            tuning_results = {
                'model_name': model_name,
                'search_method': search_method,
                'best_params': search.best_params_,
                'best_score': search.best_score_,
                'best_estimator': search.best_estimator_,
                'cv_results': search.cv_results_,
                'evaluation_date': datetime.now().isoformat()
            }
            
            # Store best model
            self.best_models[model_name] = search.best_estimator_
            
            # Store results
            self.evaluation_history.append(tuning_results)
            
            logger.info(f"Hyperparameter tuning for '{model_name}' completed")
            logger.info(f"Best {scoring}: {tuning_results['best_score']:.4f}")
            logger.info(f"Best parameters: {tuning_results['best_params']}")
            
            return tuning_results
            
        except Exception as e:
            logger.error(f"Error in hyperparameter tuning: {e}")
            return {}
    
    def compare_models(self, models: Dict[str, Any], X_test: np.ndarray, y_test: np.ndarray,
                      task_type: str = 'regression') -> pd.DataFrame:
        """
        Compare multiple models on the same test set
        
        Args:
            models: Dictionary of {model_name: model} pairs
            X_test: Test features
            y_test: Test targets
            task_type: Type of task ('regression' or 'classification')
            
        Returns:
            pd.DataFrame: Comparison results
        """
        try:
            comparison_results = []
            
            for model_name, model in models.items():
                if task_type == 'regression':
                    metrics = self.evaluate_regression_model(model, X_test, y_test, model_name=model_name)
                else:
                    metrics = self.evaluate_classification_model(model, X_test, y_test, model_name=model_name)
                
                if metrics:
                    comparison_results.append(metrics)
            
            # Create comparison DataFrame
            if comparison_results:
                comparison_df = pd.DataFrame(comparison_results)
                comparison_df = comparison_df.sort_values('r2' if task_type == 'regression' else 'accuracy', ascending=False)
                
                logger.info(f"Model comparison completed for {len(models)} models")
                return comparison_df
            else:
                logger.warning("No valid comparison results")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error comparing models: {e}")
            return pd.DataFrame()
    
    def plot_model_performance(self, model_name: str, save_path: Optional[str] = None) -> bool:
        """
        Plot model performance metrics
        
        Args:
            model_name: Name of the model to plot
            save_path: Path to save the plot (optional)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Find model evaluations
            model_evals = [eval for eval in self.evaluation_history if eval.get('model_name') == model_name]
            
            if not model_evals:
                logger.warning(f"No evaluations found for model: {model_name}")
                return False
            
            # Create performance plot
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            fig.suptitle(f'Model Performance: {model_name}', fontsize=16)
            
            # Extract metrics
            dates = [eval.get('evaluation_date', '') for eval in model_evals]
            metrics_data = {}
            
            # Determine which metrics to plot based on available data
            if 'r2' in model_evals[0]:
                # Regression metrics
                metrics_data['r2'] = [eval.get('r2', 0) for eval in model_evals]
                metrics_data['rmse'] = [eval.get('rmse', 0) for eval in model_evals]
                metrics_data['mae'] = [eval.get('mae', 0) for eval in model_evals]
                metrics_data['mape'] = [eval.get('mape', 0) for eval in model_evals]
            else:
                # Classification metrics
                metrics_data['accuracy'] = [eval.get('accuracy', 0) for eval in model_evals]
                metrics_data['precision'] = [eval.get('precision', 0) for eval in model_evals]
                metrics_data['recall'] = [eval.get('recall', 0) for eval in model_evals]
                metrics_data['f1'] = [eval.get('f1', 0) for eval in model_evals]
            
            # Plot metrics over time
            for i, (metric_name, values) in enumerate(metrics_data.items()):
                row, col = i // 2, i % 2
                axes[row, col].plot(range(len(values)), values, marker='o', linewidth=2, markersize=6)
                axes[row, col].set_title(f'{metric_name.upper()} Over Time')
                axes[row, col].set_xlabel('Evaluation Number')
                axes[row, col].set_ylabel(metric_name.upper())
                axes[row, col].grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Save plot if path provided
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logger.info(f"Performance plot saved to {save_path}")
            
            plt.show()
            return True
            
        except Exception as e:
            logger.error(f"Error plotting model performance: {e}")
            return False
    
    def generate_evaluation_report(self, model_name: str, output_path: Optional[str] = None) -> str:
        """
        Generate comprehensive evaluation report
        
        Args:
            model_name: Name of the model to report on
            output_path: Path to save the report (optional)
            
        Returns:
            str: Generated report content
        """
        try:
            # Find model evaluations
            model_evals = [eval for eval in self.evaluation_history if eval.get('model_name') == model_name]
            
            if not model_evals:
                return f"No evaluations found for model: {model_name}"
            
            # Generate report
            report = f"""
# Model Evaluation Report: {model_name}

## Overview
- **Total Evaluations**: {len(model_evals)}
- **First Evaluation**: {model_evals[0].get('evaluation_date', 'Unknown')}
- **Latest Evaluation**: {model_evals[-1].get('evaluation_date', 'Unknown')}

## Performance Summary
"""
            
            # Add performance metrics
            if 'r2' in model_evals[0]:
                # Regression report
                latest = model_evals[-1]
                report += f"""
### Regression Metrics (Latest)
- **R² Score**: {latest.get('r2', 'N/A'):.4f}
- **RMSE**: {latest.get('rmse', 'N/A'):.4f}
- **MAE**: {latest.get('mae', 'N/A'):.4f}
- **MAPE**: {latest.get('mape', 'N/A'):.2f}%
"""
            else:
                # Classification report
                latest = model_evals[-1]
                report += f"""
### Classification Metrics (Latest)
- **Accuracy**: {latest.get('accuracy', 'N/A'):.4f}
- **Precision**: {latest.get('precision', 'N/A'):.4f}
- **Recall**: {latest.get('recall', 'N/A'):.4f}
- **F1 Score**: {latest.get('f1', 'N/A'):.4f}
"""
            
            # Add trend analysis
            report += "\n## Performance Trends\n"
            if len(model_evals) > 1:
                if 'r2' in model_evals[0]:
                    r2_scores = [eval.get('r2', 0) for eval in model_evals]
                    trend = "improving" if r2_scores[-1] > r2_scores[0] else "declining"
                    report += f"- **R² Trend**: {trend} ({r2_scores[0]:.4f} → {r2_scores[-1]:.4f})\n"
                else:
                    acc_scores = [eval.get('accuracy', 0) for eval in model_evals]
                    trend = "improving" if acc_scores[-1] > acc_scores[0] else "declining"
                    report += f"- **Accuracy Trend**: {trend} ({acc_scores[0]:.4f} → {acc_scores[-1]:.4f})\n"
            else:
                report += "- **Trend**: Insufficient data for trend analysis\n"
            
            # Add recommendations
            report += "\n## Recommendations\n"
            if len(model_evals) > 1:
                if 'r2' in model_evals[0]:
                    if model_evals[-1].get('r2', 0) < 0.7:
                        report += "- Consider hyperparameter tuning to improve R² score\n"
                    if model_evals[-1].get('overfitting_score', 0) > 0.1:
                        report += "- Model shows signs of overfitting, consider regularization\n"
                else:
                    if model_evals[-1].get('accuracy', 0) < 0.8:
                        report += "- Consider hyperparameter tuning to improve accuracy\n"
                    if model_evals[-1].get('overfitting_score', 0) > 0.1:
                        report += "- Model shows signs of overfitting, consider regularization\n"
            else:
                report += "- Perform additional evaluations to assess model stability\n"
            
            # Save report if path provided
            if output_path:
                with open(output_path, 'w') as f:
                    f.write(report)
                logger.info(f"Evaluation report saved to {output_path}")
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating evaluation report: {e}")
            return f"Error generating report: {e}"
    
    def get_best_model(self, model_name: str) -> Optional[Any]:
        """
        Get the best performing model for a given name
        
        Args:
            model_name: Name of the model
            
        Returns:
            Any: Best model instance or None
        """
        return self.best_models.get(model_name)
    
    def clear_history(self):
        """Clear evaluation history"""
        self.evaluation_history.clear()
        self.best_models.clear()
        logger.info("Evaluation history cleared")

# Create global instance
model_evaluator = ModelEvaluator()
