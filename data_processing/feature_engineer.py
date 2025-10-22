"""
Feature engineering for risk modeling
"""

import pandas as pd
import numpy as np

class FeatureEngineer:
    """Create features for risk modeling"""
    
    def __init__(self, config):
        self.config = config
    
    def create_features(self, district_data, raw_data):
        """Create engineered features"""
        # Merge with district statistics
        panel_data = district_data.merge(
            raw_data['district_stats'], on='district', how='left'
        )
        
        # Add temporal features
        panel_data['quarter'] = panel_data['date'].dt.quarter
        panel_data['season'] = panel_data['month'] % 12 // 3 + 1
        
        # Calculate derived variables
        panel_data['water_stress'] = -panel_data['tws_anomaly']  # Higher = more stress
        
        # Rainfall anomalies (deviation from monthly mean)
        panel_data['rainfall_anomaly'] = panel_data.groupby(['district', 'month'])['rainfall'].transform(
            lambda x: x - x.mean()
        )
        
        # Create rolling features for each district
        features_list = []
        
        for district in panel_data['district'].unique():
            district_df = panel_data[panel_data['district'] == district].sort_values('date').copy()
            
            # Rolling statistics for different time windows
            for window in [6, 12, 24]:
                # TWS trends
                district_df[f'tws_trend_{window}m'] = district_df['tws_anomaly'].rolling(
                    window=window, min_periods=1
                ).mean()
                
                # Rainfall variability
                district_df[f'rainfall_std_{window}m'] = district_df['rainfall'].rolling(
                    window=window, min_periods=1
                ).std()
                
                # Water stress trends
                district_df[f'stress_trend_{window}m'] = district_df['water_stress'].rolling(
                    window=window, min_periods=1
                ).mean()
            
            # Crop stress index (combination of water stress and agricultural factors)
            district_df['crop_stress_index'] = (
                district_df['water_stress'] * district_df['crop_intensity'] +
                abs(district_df['rainfall_anomaly']) * 0.5 +
                district_df['gw_irrigation_ratio'] * 2
            )
            
            # Rainfall variability index
            district_df['rainfall_variability'] = (
                district_df['rainfall_std_12m'] / 
                district_df['rainfall'].rolling(window=12, min_periods=1).mean()
            )
            
            # Depletion metrics
            district_df['depletion_rate'] = district_df['tws_anomaly'].diff()
            district_df['depletion_acceleration'] = district_df['depletion_rate'].diff()
            
            # Water availability index
            district_df['water_availability'] = (
                district_df['rainfall'] - district_df['water_stress'] * 10
            )
            
            features_list.append(district_df)
        
        features_data = pd.concat(features_list, ignore_index=True)
        print(f"      ✅ Engineered features: {len(features_data.columns)} total features")
        return features_data