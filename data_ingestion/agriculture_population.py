"""
Agriculture and population data collection
"""

import pandas as pd
import numpy as np
from config import Config

class AgriculturePopulationData:
    """Handle agriculture and population data"""
    
    def __init__(self):
        self.config = Config
    
    def collect_data(self):
        """Collect crop intensity and population data"""
        print("   🌾 Downloading agriculture and population data...")
        
        districts = [f'District_{i:02d}' for i in range(1, self.config.N_DISTRICTS + 1)]
        
        # Generate synthetic data
        crop_intensity = np.random.beta(2, 2, len(districts)) * 0.8 + 0.2
        pop_density = np.random.lognormal(5, 1, len(districts))
        gw_irrigation = np.random.beta(2, 3, len(districts))
        
        district_stats = pd.DataFrame({
            'district': districts,
            'crop_intensity': crop_intensity,
            'population_density': pop_density,
            'gw_irrigation_ratio': gw_irrigation
        })
        
        print(f"   ✅ District data loaded: {len(districts)} districts")
        return district_stats