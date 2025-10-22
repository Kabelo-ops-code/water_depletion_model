"""
Data processing module for cleaning and transforming data
"""

from .spatial_aggregation import SpatialAggregator
from .panel_creation import PanelCreator

class DataProcessor:
    """Main data processing coordinator"""
    
    def __init__(self):
        self.spatial_aggregator = SpatialAggregator()
        self.panel_creator = PanelCreator()
    
    def process_all_data(self, raw_data):
        """Process all raw data into analysis-ready format"""
        print("\n🔧 2. Data Processing Phase...")
        
        # Aggregate spatial data to district level
        district_timeseries = self.spatial_aggregator.aggregate_to_districts(raw_data)
        
        # Create panel dataset
        panel_data = self.panel_creator.create_panel_dataset(district_timeseries, raw_data)
        
        processed_data = {
            'district_timeseries': district_timeseries,
            'panel_data': panel_data,
            'district_stats': raw_data['district_stats'],
            'districts_gdf': raw_data['districts_gdf']
        }
        
        print("✅ Data processing completed successfully!")
        return processed_data