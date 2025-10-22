"""
Main data collection coordinator
"""

from .grace_data import GRACEData
from .rainfall_data import RainfallData
from .agriculture_data import AgricultureData
from .boundaries import BoundaryData

class DataCollector:
    """Main data collection coordinator"""
    
    def __init__(self, config):
        self.config = config
        self.data = {}
        
    def collect_all_data(self):
        """Collect all required datasets"""
        print("📥 Collecting all data sources...")
        
        # Initialize data collectors WITH config parameter
        grace_collector = GRACEData(self.config)
        rainfall_collector = RainfallData(self.config)
        agriculture_collector = AgricultureData(self.config)
        boundary_collector = BoundaryData(self.config)
        
        # Collect GRACE data
        print("   📡 Downloading GRACE gravity anomaly data...")
        self.data['grace'] = grace_collector.download_data()
        
        # Collect rainfall data
        print("   🌧️ Downloading rainfall data...")
        self.data['rainfall'] = rainfall_collector.download_data()
        
        # Collect agriculture and population data
        print("   🌾 Collecting agriculture and population data...")
        self.data['district_stats'] = agriculture_collector.collect_data()
        
        # Load district boundaries
        print("   🗺️ Loading district boundaries...")
        self.data['districts_gdf'] = boundary_collector.load_boundaries()
        
        print("✅ Data ingestion completed successfully!")
        return self.data