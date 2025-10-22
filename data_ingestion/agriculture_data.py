"""
Agriculture and population data collection
"""

import pandas as pd
import numpy as np

class AgricultureData:
    """Handle agriculture and population data"""
    
    def __init__(self, config):
        self.config = config
    
    def collect_data(self):
        """Collect crop intensity and population data"""
        districts = [f'District_{i:02d}' for i in range(1, self.config.N_DISTRICTS + 1)]
        
        district_stats = pd.DataFrame({
            'district': districts,
            'crop_intensity': np.random.beta(2, 2, len(districts)) * 0.8 + 0.2,
            'population_density': np.random.lognormal(5, 1, len(districts)),
            'gw_irrigation_ratio': np.random.beta(2, 3, len(districts)),
            'center_lat': np.random.uniform(*self.config.LAT_RANGE, len(districts)),
            'center_lon': np.random.uniform(*self.config.LON_RANGE, len(districts))
        })
        
        print(f"      ✅ District data: {len(districts)} districts")
        return district_stats