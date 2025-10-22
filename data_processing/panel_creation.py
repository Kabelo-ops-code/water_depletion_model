"""
Create panel dataset from all data sources
"""

import pandas as pd

class PanelCreator:
    """Create panel dataset for analysis"""
    
    def create_panel_dataset(self, district_timeseries, raw_data):
        """Merge all data into panel format"""
        print("   🔄 Creating panel dataset...")
        
        # Merge timeseries with static district data
        panel_data = district_timeseries.merge(
            raw_data['district_stats'], on='district', how='left'
        )
        
        # Add temporal features
        panel_data['year'] = panel_data['date'].dt.year
        panel_data['month'] = panel_data['date'].dt.month
        panel_data['quarter'] = panel_data['date'].dt.quarter
        
        # Calculate derived variables
        panel_data['water_stress'] = -panel_data['tws_anomaly']  # Higher = more stress
        panel_data['rainfall_anomaly'] = panel_data.groupby(['district', 'month'])['rainfall'].transform(
            lambda x: x - x.mean()
        )
        
        print(f"   ✅ Panel dataset created: {len(panel_data)} records")
        return panel_data