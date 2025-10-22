"""
Visualization module for creating maps, graphs, and dashboards
"""

from .choropleth_maps import MapVisualizer
from .timelapse_graphs import TimeSeriesVisualizer
from .dashboard import DashboardBuilder

class VisualizationEngine:
    """Main visualization coordinator"""
    
    def __init__(self):
        self.map_visualizer = MapVisualizer()
        self.timeseries_visualizer = TimeSeriesVisualizer()
        self.dashboard_builder = DashboardBuilder()
    
    def create_all_visualizations(self, processed_data, models_results):
        """Create all visualizations"""
        print("\n📊 4. Visualization Phase...")
        
        # Create risk maps
        risk_map_data = self._prepare_risk_map_data(processed_data, models_results)
        map_files = self.map_visualizer.create_maps(risk_map_data)
        
        # Create time series graphs
        timeseries_files = self.timeseries_visualizer.create_graphs(
            models_results['features_data']
        )
        
        # Create interactive dashboard
        dashboard_files = self.dashboard_builder.build_dashboard(
            risk_map_data, models_results
        )
        
        all_files = map_files + timeseries_files + dashboard_files
        
        print("✅ Visualization completed successfully!")
        return all_files
    
    def _prepare_risk_map_data(self, processed_data, models_results):
        """Prepare data for risk mapping"""
        risk_assessment = models_results['risk_assessment']
        districts_gdf = processed_data['districts_gdf']
        
        # Merge risk assessment with geographic data
        risk_map_data = districts_gdf.merge(
            risk_assessment[['district', 'risk_score', 'risk_level', 'water_stress', 'crop_stress_index']],
            on='district'
        )
        
        return {
            'risk_map_data': risk_map_data,
            'risk_assessment': risk_assessment,
            'feature_importance': models_results['model_results']['feature_importance']
        }