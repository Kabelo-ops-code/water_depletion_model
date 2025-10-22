"""
Time series modeling for water depletion
"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import numpy as np
from config import Config

class TimeSeriesModel:
    """Time series modeling implementation"""
    
    def __init__(self):
        self.config = Config
    
    def train_models(self, features_data):
        """Train predictive models"""
        print("   📈 Applying time series modeling...")
        
        df = features_data.dropna().copy()
        
        # Prepare features for prediction
        feature_cols = [
            'tws_anomaly', 'rainfall', 'crop_intensity', 'population_density',
            'gw_irrigation_ratio', 'month', 'crop_stress_index', 
            'rainfall_variability', 'tws_trend_12m'
        ]
        
        # Only use columns that exist
        available_cols = [col for col in feature_cols if col in df.columns]
        X = df[available_cols]
        y = df['water_stress']
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.config.TEST_SIZE, random_state=self.config.RANDOM_STATE
        )
        
        # Train model
        model = RandomForestRegressor(
            n_estimators=self.config.N_ESTIMATORS, 
            random_state=self.config.RANDOM_STATE
        )
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        
        # Model performance
        model_performance = {
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'r2': r2_score(y_test, y_pred)
        }
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': available_cols,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        model_results = {
            'model': model,
            'model_performance': model_performance,
            'feature_importance': feature_importance,
            'feature_cols': available_cols
        }
        
        print(f"   ✅ Time series model trained - R²: {model_performance['r2']:.3f}")
        return model_results