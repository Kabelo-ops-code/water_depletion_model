"""
Risk classification implementation
"""

import pandas as pd
import numpy as np

class RiskClassifier:
    """Classify districts into risk categories"""
    
    def __init__(self, config):
        self.config = config
    
    def classify_risk(self, processed_data, model_results):
        """Classify districts into risk levels"""
        df = processed_data.copy()
        
        # Calculate risk score based on water stress (simplified)
        df['risk_score'] = (df['water_stress'] - df['water_stress'].min()) / (df['water_stress'].max() - df['water_stress'].min())
        
        # Classify risk levels
        conditions = [
            df['risk_score'] <= self.config.RISK_THRESHOLDS['low'],
            (df['risk_score'] > self.config.RISK_THRESHOLDS['low']) & 
            (df['risk_score'] <= self.config.RISK_THRESHOLDS['moderate']),
            df['risk_score'] > self.config.RISK_THRESHOLDS['moderate']
        ]
        choices = ['Low', 'Moderate', 'Critical']
        df['risk_level'] = np.select(conditions, choices, default='Unknown')
        
        # Get latest assessment for each district
        latest_risk = df.sort_values('date').groupby('district').last().reset_index()
        
        risk_counts = latest_risk['risk_level'].value_counts()
        print(f"      ✅ Risk classification: {dict(risk_counts)}")
        
        return latest_risk