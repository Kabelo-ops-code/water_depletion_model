"""
Model evaluation and validation
"""

import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, explained_variance_score

class ModelEvaluator:
    """Evaluate model performance and validate results"""
    
    def __init__(self, config):
        self.config = config
    
    def evaluate_models(self, model_results, processed_data):
        """Comprehensive model evaluation"""
        evaluation = {}
        
        # Basic performance metrics
        perf = model_results['model_performance']
        evaluation['basic_metrics'] = {
            'r2_score': perf['r2'],
            'rmse': perf['rmse'],
            'mse': perf['mse'],
            'cv_score_mean': perf['cv_mean'],
            'cv_score_std': perf['cv_std']
        }
        
        # Feature importance analysis
        feature_importance = model_results['feature_importance']
        evaluation['feature_analysis'] = {
            'top_features': feature_importance.head(10).to_dict('records'),
            'total_features': len(feature_importance),
            'dominant_features': feature_importance[feature_importance['importance'] > 0.1]['feature'].tolist()
        }
        
        # Model interpretability metrics
        evaluation['interpretability'] = {
            'feature_diversity': self._calculate_feature_diversity(feature_importance),
            'model_stability': perf['cv_std']  # Lower CV std = more stable
        }
        
        # Business metrics
        evaluation['business_metrics'] = {
            'prediction_accuracy': 'High' if perf['r2'] > 0.7 else 'Medium' if perf['r2'] > 0.5 else 'Low',
            'reliability': 'High' if perf['cv_std'] < 0.1 else 'Medium' if perf['cv_std'] < 0.2 else 'Low',
            'feature_quality': 'Good' if len(evaluation['feature_analysis']['dominant_features']) >= 3 else 'Adequate'
        }
        
        print(f"      ✅ Model evaluation completed")
        print(f"      📊 R² Score: {perf['r2']:.3f}")
        print(f"      📊 Cross-validation consistency: {perf['cv_std']:.3f}")
        print(f"      🔍 Top features: {', '.join(feature_importance.head(3)['feature'].tolist())}")
        
        return evaluation
    
    def _calculate_feature_diversity(self, feature_importance):
        """Calculate how evenly distributed feature importance is"""
        importance_values = feature_importance['importance'].values
        if len(importance_values) == 0:
            return 0
        
        # Calculate entropy of feature importance
        normalized_importance = importance_values / importance_values.sum()
        entropy = -np.sum(normalized_importance * np.log(normalized_importance + 1e-8))
        max_entropy = np.log(len(importance_values))
        
        return entropy / max_entropy if max_entropy > 0 else 0