"""
Feature engineering for risk modeling
"""

import pandas as pd
import numpy as np
from config import Config

class FeatureEngineer:
    """Create features for risk modeling"""
    
    def __init__(self):
        self.config = Config
    
    def create_features(self, panel_data):
        """Create engineered features"""
        print("   🛠️ Engineering features...")
        
        df = panel_data.copy()
        features = []
        
        for district in df['district'].unique():
            district_data = df[df['district'] == district].sort_values('date')
            
            # Rolling averages and trends
            for window in [6, 12, 24]:  # 6-month, 1-year, 2-year windows
                district_data[f'tws_trend_{window}m'] = district_data['tws_anomaly'].rolling(window=window).mean()
                district_data[f'rainfall_std_{window}m'] = district_data['rainfall'].rolling(window=window).std()
            
            # Crop stress index
            district_data['crop_stress_index'] = (
                district_data['water_stress'] * district_data['crop_intensity'] +
                abs(district_data['rainfall_anomaly']) * 0.5
            )
            
            # Rainfall variability index
            district_data['rainfall_variability'] = (
                district_data['rainfall_std_12m'] / district_data['rainfall'].rolling(window=12).mean()
            )
            
            # Depletion acceleration
            district_data['depletion_acceleration'] = district_data['tws_anomaly'].diff().diff()
            
            features.append(district_data)
        
        features_data = pd.concat(features, ignore_index=True)
        print("   ✅ Feature engineering complete")
        return features_data