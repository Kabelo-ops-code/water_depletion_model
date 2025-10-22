"""
District boundary data handling
"""

import pandas as pd
import numpy as np

class BoundaryData:
    """Handle district boundary data"""
    
    def __init__(self, config):
        self.config = config
    
    def load_boundaries(self):
        """Load or create district boundaries"""
        districts = [f'District_{i:02d}' for i in range(1, self.config.N_DISTRICTS + 1)]
        
        boundaries_data = pd.DataFrame({
            'district': districts,
            'area_sqkm': np.random.lognormal(9, 0.5, len(districts))
        })
        
        print(f"      ✅ Boundaries data: {len(districts)} districts")
        return boundaries_data