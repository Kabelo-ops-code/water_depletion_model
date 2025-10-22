"""
Utility helper functions
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime
import logging

class DataValidator:
    """Data validation utilities"""
    
    @staticmethod
    def validate_dataframe(df, required_columns=None, min_rows=1):
        """Validate dataframe structure and content"""
        if df.empty:
            raise ValueError("DataFrame is empty")
        
        if len(df) < min_rows:
            raise ValueError(f"DataFrame has insufficient rows: {len(df)} < {min_rows}")
        
        if required_columns:
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
        
        return True
    
    @staticmethod
    def check_data_quality(df, threshold=0.3):
        """Check data quality and missing values"""
        quality_report = {}
        
        # Check missing values
        missing_ratio = df.isnull().sum() / len(df)
        high_missing = missing_ratio[missing_ratio > threshold]
        
        quality_report['missing_values'] = {
            'total_columns': len(df.columns),
            'columns_with_high_missing': len(high_missing),
            'high_missing_columns': high_missing.index.tolist()
        }
        
        # Check data types
        dtypes_count = df.dtypes.value_counts()
        quality_report['data_types'] = dtypes_count.to_dict()
        
        # Check for constant columns
        constant_columns = [col for col in df.columns if df[col].nunique() <= 1]
        quality_report['constant_columns'] = constant_columns
        
        return quality_report

class FileHandler:
    """File handling utilities"""
    
    @staticmethod
    def ensure_directory(path):
        """Ensure directory exists"""
        os.makedirs(path, exist_ok=True)
        return path
    
    @staticmethod
    def get_file_size(file_path):
        """Get file size in MB"""
        if os.path.exists(file_path):
            return os.path.getsize(file_path) / (1024 * 1024)
        return 0
    
    @staticmethod
    def clean_filename(filename):
        """Clean filename for safe saving"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename
    
    @staticmethod
    def get_file_info(file_path):
        """Get comprehensive file information"""
        if not os.path.exists(file_path):
            return None
        
        stat = os.stat(file_path)
        return {
            'path': file_path,
            'size_mb': stat.st_size / (1024 * 1024),
            'created': datetime.fromtimestamp(stat.st_ctime),
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'extension': os.path.splitext(file_path)[1]
        }

class StatisticsCalculator:
    """Statistical calculation utilities"""
    
    @staticmethod
    def calculate_trend(data, method='linear'):
        """Calculate trend in time series data"""
        if len(data) < 2:
            return 0
        
        if method == 'linear':
            x = np.arange(len(data))
            slope = np.polyfit(x, data, 1)[0]
            return slope
        elif method == 'theil_sen':
            # Robust trend estimation
            from scipy.stats import theilslopes
            x = np.arange(len(data))
            slope, _, _, _ = theilslopes(data, x)
            return slope
        else:
            raise ValueError(f"Unsupported method: {method}")
    
    @staticmethod
    def calculate_anomaly(data, window=12, method='zscore'):
        """Calculate anomaly from rolling statistics"""
        if method == 'zscore':
            rolling_mean = data.rolling(window=window, min_periods=1).mean()
            rolling_std = data.rolling(window=window, min_periods=1).std()
            anomaly = (data - rolling_mean) / (rolling_std + 1e-8)
        elif method == 'percentile':
            rolling_median = data.rolling(window=window, min_periods=1).median()
            anomaly = (data - rolling_median) / rolling_median
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        return anomaly
    
    @staticmethod
    def calculate_seasonal_decomposition(data, period=12):
        """Simple seasonal decomposition"""
        if len(data) < period * 2:
            return None
        
        # Simple moving average for trend
        trend = data.rolling(window=period, center=True).mean()
        
        # Detrended series
        detrended = data - trend
        
        # Seasonal component (average by period)
        seasonal = detrended.groupby(detrended.index % period).mean()
        
        # Residual
        residual = detrended - seasonal.values
        
        return {
            'trend': trend,
            'seasonal': seasonal,
            'residual': residual
        }