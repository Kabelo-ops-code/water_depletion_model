"""
Data ingestion module for collecting all required datasets
"""

from .grace_data import GRACEData
from .rainfall_data import RainfallData
from .agriculture_population import AgriculturePopulationData
from .boundaries import BoundaryData

class DataCollector:
    """Main data collection coordinator"""
    
    def __init__(self):
        self.data = {}
        self.grace = GRACEData()
        self.rainfall = RainfallData()
        self.agriculture = AgriculturePopulationData()
        self.boundaries = BoundaryData()
    
    def collect_all_data(self):
        """Collect all required datasets"""
        print("📥 1. Data Ingestion Phase...")
        
        # Collect GRACE data
        self.data['grace'] = self.grace.download_data()
        
        # Collect rainfall data
        self.data['rainfall'] = self.rainfall.download_data()
        
        # Collect agriculture and population data
        self.data['district_stats'] = self.agriculture.collect_data()
        
        # Load district boundaries
        self.data['districts_gdf'] = self.boundaries.load_boundaries()
        
        print("✅ Data ingestion completed successfully!")
        return self.data