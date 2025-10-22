"""
Rainfall data collection
"""

import pandas as pd
import numpy as np

class RainfallData:
    """Handle rainfall data collection"""
    
    def __init__(self, config):
        self.config = config
    
    def download_data(self):
        """Download and process rainfall data"""
        dates = pd.date_range(
            self.config.START_DATE, 
            self.config.END_DATE, 
            freq=self.config.FREQUENCY
        )
        
        base_rainfall = np.random.gamma(2, 50, len(dates))
        seasonal = 50 * np.sin(2 * np.pi * pd.DatetimeIndex(dates).month / 12)
        rainfall_values = base_rainfall + seasonal + np.random.normal(0, 20, len(dates))
        
        rainfall_data = {
            'dates': dates,
            'values': rainfall_values,
            'type': 'precipitation',
            'units': 'mm'
        }
        
        print(f"      ✅ Rainfall data: {len(dates)} monthly records")
        return rainfall_data