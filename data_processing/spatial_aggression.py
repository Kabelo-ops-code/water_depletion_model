"""
Spatial aggregation of satellite data to district level
"""

import pandas as pd
import numpy as np

class SpatialAggregator:
    """Aggregate spatial data to district level"""
    
    def aggregate_to_districts(self, raw_data):
        """Aggregate satellite data to district level"""
        print("   📍 Aggregating data to district level...")
        
        district_data = []
        districts_gdf = raw_data['districts_gdf']
        
        for idx, district in districts_gdf.iterrows():
            district_name = district['district']
            geometry = district['geometry']
            
            # Get bounds for spatial subsetting
            bounds = geometry.bounds
            lon_min, lat_min, lon_max, lat_max = bounds
            
            # Extract data within district bounds
            grace_subset = raw_data['grace'].sel(
                lat=slice(lat_min, lat_max),
                lon=slice(lon_min, lon_max)
            )
            
            rainfall_subset = raw_data['rainfall'].sel(
                lat=slice(lat_min, lat_max),
                lon=slice(lon_min, lon_max)
            )
            
            # Calculate district averages
            grace_mean = grace_subset['tws_anomaly'].mean(dim=['lat', 'lon']).values
            rainfall_mean = rainfall_subset['precipitation'].mean(dim=['lat', 'lon']).values
            
            for i, date in enumerate(raw_data['grace'].time.values):
                district_data.append({
                    'district': district_name,
                    'date': pd.to_datetime(date),
                    'tws_anomaly': grace_mean[i] if not np.isnan(grace_mean[i]) else 0,
                    'rainfall': rainfall_mean[i] if not np.isnan(rainfall_mean[i]) else 0
                })
        
        district_timeseries = pd.DataFrame(district_data)
        print(f"   ✅ District aggregation complete: {len(district_timeseries)} records")
        return district_timeseries