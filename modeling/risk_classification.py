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
        
        # Calculate risk score based on multiple factors
        risk_factors = self.config.RISK_WEIGHTS
        available_risk_factors = {}
        
        # Check which risk factors are available in the data
        for factor, weight in risk_factors.items():
            if factor in df.columns:
                # Check if factor has sufficient data
                non_null_count = df[factor].notnull().sum()
                if non_null_count > len(df) * 0.5:  # At least 50% non-null
                    available_risk_factors[factor] = weight
        
        if not available_risk_factors:
            # Fallback: use simple water stress
            df['risk_score'] = (df['water_stress'] - df['water_stress'].min()) / \
                             (df['water_stress'].max() - df['water_stress'].min())
        else:
            # Normalize each available risk factor
            for factor in available_risk_factors.keys():
                df[f'{factor}_norm'] = self._normalize_column(df[factor])
            
            # Calculate composite risk score
            df['risk_score'] = 0
            total_weight = sum(available_risk_factors.values())
            
            for factor, weight in available_risk_factors.items():
                norm_col = f'{factor}_norm'
                if norm_col in df.columns:
                    df['risk_score'] += df[norm_col] * (weight / total_weight)
        
        # Ensure risk score is between 0 and 1
        df['risk_score'] = np.clip(df['risk_score'], 0, 1)
        
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
        latest_risk = df.sort_values('date').groupby('district').agg({
            'risk_score': 'last',
            'risk_level': 'last',
            'water_stress': 'last',
            'tws_anomaly': 'last',
            'rainfall': 'last',
            'crop_stress_index': 'last',
            'population_density': 'first',
            'gw_irrigation_ratio': 'first',
            'center_lat': 'first',
            'center_lon': 'first'
        }).reset_index()
        
        # Calculate risk trends
        risk_trends = self._calculate_risk_trends(df)
        latest_risk = latest_risk.merge(risk_trends, on='district', how='left')
        
        risk_counts = latest_risk['risk_level'].value_counts()
        print(f"      ✅ Risk classification: {dict(risk_counts)}")
        
        return latest_risk
    
    def _normalize_column(self, series):
        """Normalize a pandas series to 0-1 range"""
        min_val = series.min()
        max_val = series.max()
        
        if max_val == min_val:
            return np.zeros(len(series))
        
        return (series - min_val) / (max_val - min_val)
    
    def _calculate_risk_trends(self, df):
        """Calculate risk trends over time for each district"""
        trends = []
        
        for district in df['district'].unique():
            district_data = df[df['district'] == district].sort_values('date')
            
            if len(district_data) > 12:  # Need sufficient data for trend calculation
                # Calculate 6-month moving average of risk score
                risk_ma = district_data['risk_score'].rolling(window=6, min_periods=3).mean()
                
                if len(risk_ma) > 6:
                    # Calculate trend (slope of linear regression)
                    x = np.arange(len(risk_ma.dropna()))
                    y = risk_ma.dropna().values
                    
                    if len(y) > 1:
                        slope = np.polyfit(x, y, 1)[0]
                        trend_direction = 'increasing' if slope > 0.01 else 'decreasing' if slope < -0.01 else 'stable'
                    else:
                        slope = 0
                        trend_direction = 'unknown'
                    
                    trends.append({
                        'district': district,
                        'risk_trend_slope': slope,
                        'risk_trend_direction': trend_direction,
                        'recent_risk_change': risk_ma.iloc[-1] - risk_ma.iloc[0] if len(risk_ma) > 1 else 0
                    })
        
        return pd.DataFrame(trends) if trends else pd.DataFrame(columns=['district', 'risk_trend_slope', 'risk_trend_direction', 'recent_risk_change'])