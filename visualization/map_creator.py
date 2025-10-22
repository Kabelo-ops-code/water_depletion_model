"""
Create choropleth maps for risk visualization
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

class MapCreator:
    """Create geographic visualizations of risk"""
    
    def __init__(self, config):
        self.config = config
        plt.style.use(config.PLOT_STYLE)
    
    def create_risk_maps(self, risk_assessment):
        """Create risk visualization maps"""
        output_files = []
        
        # 1. Risk Level Map
        plt.figure(figsize=(12, 8))
        self._create_risk_level_map(risk_assessment)
        risk_map_path = self.config.get_output_path('risk_level_map.png')
        plt.savefig(risk_map_path, dpi=self.config.DPI, bbox_inches='tight')
        plt.close()
        output_files.append(risk_map_path)
        
        # 2. Risk Score Map
        plt.figure(figsize=(12, 8))
        self._create_risk_score_map(risk_assessment)
        score_map_path = self.config.get_output_path('risk_score_map.png')
        plt.savefig(score_map_path, dpi=self.config.DPI, bbox_inches='tight')
        plt.close()
        output_files.append(score_map_path)
        
        # 3. Water Stress Map
        plt.figure(figsize=(12, 8))
        self._create_water_stress_map(risk_assessment)
        stress_map_path = self.config.get_output_path('water_stress_map.png')
        plt.savefig(stress_map_path, dpi=self.config.DPI, bbox_inches='tight')
        plt.close()
        output_files.append(stress_map_path)
        
        return output_files
    
    def _create_risk_level_map(self, risk_assessment):
        """Create map showing risk levels"""
        colors = {'Critical': 'red', 'Moderate': 'orange', 'Low': 'green', 'Unknown': 'gray'}
        
        plt.scatter(risk_assessment['center_lon'], risk_assessment['center_lat'],
                   c=[colors.get(level, 'gray') for level in risk_assessment['risk_level']],
                   s=risk_assessment['population_density']/10,  # Size based on population
                   alpha=0.7, edgecolors='black', linewidth=0.5)
        
        # Add labels for critical districts
        critical_districts = risk_assessment[risk_assessment['risk_level'] == 'Critical']
        for _, district in critical_districts.iterrows():
            plt.annotate(district['district'], 
                        (district['center_lon'], district['center_lat']),
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=8, alpha=0.8)
        
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Groundwater Depletion Risk Levels by District')
        plt.grid(True, alpha=0.3)
        
        # Create custom legend
        from matplotlib.lines import Line2D
        legend_elements = [Line2D([0], [0], marker='o', color='w', 
                                 markerfacecolor=color, markersize=8, label=level)
                          for level, color in colors.items() if level != 'Unknown']
        plt.legend(handles=legend_elements, title='Risk Level')
    
    def _create_risk_score_map(self, risk_assessment):
        """Create map showing continuous risk scores"""
        scatter = plt.scatter(risk_assessment['center_lon'], risk_assessment['center_lat'],
                            c=risk_assessment['risk_score'], cmap='RdYlGn_r',
                            s=100, alpha=0.7, edgecolors='black', linewidth=0.5)
        
        plt.colorbar(scatter, label='Risk Score (0-1)')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Groundwater Depletion Risk Scores by District')
        plt.grid(True, alpha=0.3)
    
    def _create_water_stress_map(self, risk_assessment):
        """Create map showing water stress levels"""
        scatter = plt.scatter(risk_assessment['center_lon'], risk_assessment['center_lat'],
                            c=risk_assessment['water_stress'], cmap='Blues',
                            s=risk_assessment['agricultural_area']/1000,  # Size based on ag area
                            alpha=0.7, edgecolors='black', linewidth=0.5)
        
        plt.colorbar(scatter, label='Water Stress Index')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Water Stress Levels by District (Size = Agricultural Area)')
        plt.grid(True, alpha=0.3)