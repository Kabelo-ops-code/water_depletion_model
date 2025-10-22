"""
Choropleth map creation for risk visualization
"""

import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd
from config import Config

class MapVisualizer:
    """Create choropleth maps for risk visualization"""
    
    def __init__(self):
        self.config = Config
    
    def create_maps(self, risk_data):
        """Create static and interactive maps"""
        print("   🗺️ Creating choropleth maps...")
        
        risk_gdf = risk_data['risk_map_data']
        output_files = []
        
        # Create static matplotlib maps
        static_maps = self._create_static_maps(risk_gdf)
        output_files.extend(static_maps)
        
        # Create interactive Plotly maps
        interactive_maps = self._create_interactive_maps(risk_gdf)
        output_files.extend(interactive_maps)
        
        print("   ✅ Choropleth maps created")
        return output_files
    
    def _create_static_maps(self, risk_gdf):
        """Create static matplotlib maps"""
        output_files = []
        
        fig, axes = plt.subplots(2, 2, figsize=(20, 16))
        
        # Risk level map
        risk_gdf.plot(column='risk_level', categorical=True, 
                     legend=True, ax=axes[0,0], cmap=self.config.COLOR_MAP_RISK)
        axes[0,0].set_title('Groundwater Depletion Risk Level', fontsize=14, fontweight='bold')
        
        # Risk score map
        risk_gdf.plot(column='risk_score', legend=True, ax=axes[0,1], cmap='Reds')
        axes[0,1].set_title('Groundwater Depletion Risk Score', fontsize=14, fontweight='bold')
        
        # Water stress map
        risk_gdf.plot(column='water_stress', legend=True, ax=axes[1,0], cmap='Blues')
        axes[1,0].set_title('Water Stress Index', fontsize=14, fontweight='bold')
        
        # Crop stress map
        risk_gdf.plot(column='crop_stress_index', legend=True, ax=axes[1,1], cmap='Oranges')
        axes[1,1].set_title('Crop Stress Index', fontsize=14, fontweight='bold')
        
        for ax in axes.flat:
            ax.set_axis_off()
        
        plt.tight_layout()
        static_map_path = self.config.get_output_path('risk_maps.png')
        plt.savefig(static_map_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        output_files.append(static_map_path)
        return output_files
    
    def _create_interactive_maps(self, risk_gdf):
        """Create interactive Plotly maps"""
        output_files = []
        
        # Interactive risk level map
        fig = px.choropleth(risk_gdf,
                           geojson=risk_gdf.geometry,
                           locations=risk_gdf.index,
                           color='risk_level',
                           color_discrete_map={'Low': 'green', 'Moderate': 'yellow', 'Critical': 'red'},
                           title='District-wise Groundwater Depletion Risk')
        fig.update_geos(fitbounds="locations", visible=False)
        
        interactive_map_path = self.config.get_output_path('interactive_risk_map.html')
        fig.write_html(interactive_map_path)
        output_files.append(interactive_map_path)
        
        return output_files