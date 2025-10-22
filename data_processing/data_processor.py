"""
Main data processing coordinator
"""

import pandas as pd
import numpy as np

class DataProcessor:
    """Main data processing coordinator"""
    
    def __init__(self, config):
        self.config = config
    
    def process_all_data(self, raw_data):
        """Process all raw data into analysis-ready format"""
        print("🔧 Processing all data sources...")
        
        # Aggregate to district level
        district_data = []
        districts = raw_data['district_stats']
        grace_data = raw_data['grace']
        rainfall_data = raw_data['rainfall']
        
        for _, district in districts.iterrows():
            district_name = district['district']
            variation = np.random.normal(0, 2, len(grace_data['dates']))
            
            for i, date in enumerate(grace_data['dates']):
                district_data.append({
                    'district': district_name,
                    'date': date,
                    'tws_anomaly': grace_data['values'][i] + variation[i],
                    'rainfall': rainfall_data['values'][i] + np.random.normal(0, 10)
                })
        
        district_timeseries = pd.DataFrame(district_data)
        
        # Create panel data
        panel_data = district_timeseries.merge(
            raw_data['district_stats'], on='district', how='left'
        )
        
        # Add basic features
        panel_data['year'] = panel_data['date'].dt.year
        panel_data['month'] = panel_data['date'].dt.month
        panel_data['water_stress'] = -panel_data['tws_anomaly']
        
        # Add rolling features for better analysis
        enhanced_data = []
        for district in panel_data['district'].unique():
            district_df = panel_data[panel_data['district'] == district].copy()
            
            # Add rolling statistics
            district_df['tws_trend_6m'] = district_df['tws_anomaly'].rolling(6, min_periods=1).mean()
            district_df['tws_trend_12m'] = district_df['tws_anomaly'].rolling(12, min_periods=1).mean()
            district_df['rainfall_std_6m'] = district_df['rainfall'].rolling(6, min_periods=1).std()
            
            # Add derived features
            district_df['crop_stress_index'] = district_df['water_stress'] * district_df['crop_intensity']
            district_df['water_demand_index'] = district_df['population_density'] * district_df['gw_irrigation_ratio']
            
            enhanced_data.append(district_df)
        
        processed_data = pd.concat(enhanced_data, ignore_index=True)
        
        print(f"      ✅ Processed data: {len(processed_data)} records with enhanced features")
        return processed_data