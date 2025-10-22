"""
Machine learning model training
"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import numpy as np

class ModelTrainer:
    """Train machine learning models for water stress prediction"""
    
    def __init__(self, config):
        self.config = config
    
    def train_models(self, processed_data):
        """Train predictive models"""
        # Prepare features for modeling
        feature_columns = [
            'tws_anomaly', 'rainfall', 'crop_intensity', 'population_density',
            'gw_irrigation_ratio', 'month'
        ]
        
        # Use only available columns with data
        available_features = []
        for col in feature_columns:
            if col in processed_data.columns:
                available_features.append(col)
        
        if not available_features:
            available_features = ['tws_anomaly', 'rainfall', 'month']
        
        # Prepare data
        modeling_data = processed_data.dropna(subset=available_features + ['water_stress'])
        
        X = modeling_data[available_features]
        y = modeling_data['water_stress']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=self.config.TEST_SIZE, 
            random_state=self.config.RANDOM_STATE
        )
        
        print(f"      ✅ Training data: {len(X_train)} samples")
        
        # Train Random Forest model
        model = RandomForestRegressor(
            n_estimators=self.config.N_ESTIMATORS,
            random_state=self.config.RANDOM_STATE
        )
        
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        
        # Calculate performance metrics
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': available_features,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        results = {
            'model': model,
            'model_performance': {
                'r2': r2,
                'rmse': rmse,
                'mse': mse
            },
            'feature_importance': feature_importance
        }
        
        print(f"      ✅ Model trained - R²: {r2:.3f}")
        return results