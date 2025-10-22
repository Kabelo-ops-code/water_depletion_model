"""
Data validation utilities
"""

import pandas as pd
import numpy as np

class DataValidator:
    """Validate data quality and consistency"""
    
    def __init__(self, config):
        self.config = config
    
    def validate_raw_data(self, raw_data):
        """Validate raw input data"""
        required_keys = ['grace', 'rainfall', 'district_stats', 'districts_gdf']
        
        for key in required_keys:
            if key not in raw_data:
                raise ValueError(f"Missing required data: {key}")
        
        # Validate GRACE data
        grace_data = raw_data['grace']
        if len(grace_data['dates']) != len(grace_data['values']):
            raise ValueError("GRACE data dates and values length mismatch")
        
        # Validate district data
        districts = raw_data['district_stats']
        if len(districts) != self.config.N_DISTRICTS:
            raise ValueError(f"Expected {self.config.N_DISTRICTS} districts, got {len(districts)}")
        
        print("      ✅ Raw data validation passed")
    
    def validate_processed_data(self, processed_data):
        """Validate processed data"""
        required_columns = ['district', 'date', 'tws_anomaly', 'rainfall', 'water_stress']
        
        for col in required_columns:
            if col not in processed_data.columns:
                raise ValueError(f"Missing required column: {col}")
        
        # Check for excessive missing values
        missing_ratio = processed_data.isnull().sum() / len(processed_data)
        high_missing = missing_ratio[missing_ratio > 0.5]
        
        if not high_missing.empty:
            print(f"      ⚠️  High missing values in: {list(high_missing.index)}")
        
        print("      ✅ Processed data validation passed")