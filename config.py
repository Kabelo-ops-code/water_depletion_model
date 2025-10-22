"""
Configuration settings for the Water Depletion Model
"""

import os
from datetime import datetime

class Config:
    """Project configuration"""
    
    def __init__(self):
        # Project settings
        self.PROJECT_NAME = "Underground Water Depletion Risk Modeling"
        self.VERSION = "1.0.0"
        
        # Directory paths
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.DATA_DIR = os.path.join(self.BASE_DIR, "data")
        self.OUTPUT_DIR = os.path.join(self.BASE_DIR, "output")
        self.MODELS_DIR = os.path.join(self.BASE_DIR, "models")
        
        # Create directories
        self._create_directories()
        
        # Time settings
        self.START_DATE = "2010-01-01"
        self.END_DATE = "2023-12-31"
        self.FREQUENCY = "M"  # Monthly data
        
        # Spatial settings
        self.N_DISTRICTS = 50
        self.LAT_RANGE = (20, 30)
        self.LON_RANGE = (70, 80)
        
        # Model parameters
        self.TEST_SIZE = 0.2
        self.RANDOM_STATE = 42
        self.N_ESTIMATORS = 100
        self.CROSS_VALIDATION = 5  # This was missing!
        
        # Risk classification thresholds
        self.RISK_THRESHOLDS = {
            'low': 0.33,
            'moderate': 0.66,
            'critical': 1.0
        }
        
        # Risk factor weights
        self.RISK_WEIGHTS = {
            'water_stress': 0.3,
            'crop_stress_index': 0.25,
            'rainfall_variability': 0.2,
            'depletion_acceleration': 0.15,
            'gw_irrigation_ratio': 0.1
        }
        
        # Visualization settings
        self.PLOT_STYLE = "seaborn-v0_8"
        self.COLOR_MAP_RISK = "RdYlGn_r"
        self.COLOR_MAP_STRESS = "Blues"
        self.FIGURE_SIZE = (12, 8)
        self.DPI = 300
        
    def _create_directories(self):
        """Create necessary directories"""
        directories = [self.DATA_DIR, self.OUTPUT_DIR, self.MODELS_DIR]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def get_output_path(self, filename):
        """Get full output path for file"""
        return os.path.join(self.OUTPUT_DIR, filename)
    
    def get_data_path(self, filename):
        """Get full data path for file"""
        return os.path.join(self.DATA_DIR, filename)
    
    def get_model_path(self, filename):
        """Get full model path for file"""
        return os.path.join(self.MODELS_DIR, filename)