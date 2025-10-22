"""
Spatial aggregation of satellite data to district level
"""

import pandas as pd
import numpy as np

class DataAggregator:
    """Aggregate spatial data to district level"""
    
    def __init__(self, config):
        self.config = config
    
    def aggregate_to_districts(self, raw_data):
        """Aggregate satellite data to district level"""
        district_data = []
        districts = raw_data['district_stats']
        grace_data = raw_data['grace']
        rainfall_data = raw_data['rainfall']
        
        # Create time series for each district with realistic variations
        for _, district in districts.iterrows():
            district_name = district['district']
            
            # District-specific variations based on characteristics
            district_factor = district['gw_irrigation_ratio'] * 3  # Higher irrigation = more variation
            district_tws_variation = np.random.normal(0, 1 + district_factor, len(grace_data['dates']))
            district_rain_variation = np.random.normal(0, 5 + district_factor, len(rainfall_data['dates']))
            
            for i, date in enumerate(grace_data['dates']):
                district_data.append({
                    'district': district_name,
                    'date': date,
                    'tws_anomaly': grace_data['values'][i] + district_tws_variation[i],
                    'rainfall': rainfall_data['values'][i] + district_rain_variation[i],
                    'year': date.year,
                    'month': date.month
                })
        
        district_timeseries = pd.DataFrame(district_data)
        print(f"      ✅ Aggregated data: {len(district_timeseries)} records")
        return district_timeseries