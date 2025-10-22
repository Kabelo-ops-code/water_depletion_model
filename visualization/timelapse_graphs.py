"""
Time-lapse graphs and time series visualizations
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
from config import Config

class TimeSeriesVisualizer:
    """Create time series visualizations"""
    
    def __init__(self):
        self.config = Config
    
    def create_graphs(self, features_data):
        """Create time series graphs"""
        print("   📈 Creating time-lapse graphs...")
        
        output_files = []
        
        # Create district time series
        timeseries_file = self._create_district_timeseries(features_data)
        output_files.append(timeseries_file)
        
        # Create risk evolution graph
        risk_evolution_file = self._create_risk_evolution(features_data)
        output_files.append(risk_evolution_file)
        
        # Create feature importance graph
        importance_file = self._create_feature_importance(features_data)
        output_files.append(importance_file)
        
        print("   ✅ Time-lapse graphs created")
        return output_files
    
    def _create_district_timeseries(self, features_data):
        """Create time series plots for sample districts"""
        df = features_data.copy()
        
        # Select sample districts for time series plots
        sample_districts = df['district'].unique()[:6]
        
        # Create time series subplots
        fig = make_subplots(rows=3, cols=2, 
                           subplot_titles=[f'District: {d}' for d in sample_districts],
                           vertical_spacing=0.1)
        
        for i, district in enumerate(sample_districts):
            district_data = df[df['district'] == district].sort_values('date')
            row = i // 2 + 1
            col = i % 2 + 1
            
            fig.add_trace(
                go.Scatter(x=district_data['date'], y=district_data['tws_anomaly'],
                          name=f'{district} - TWS', line=dict(color='blue')),
                row=row, col=col
            )
            
            fig.add_trace(
                go.Scatter(x=district_data['date'], y=district_data['water_stress'],
                          name=f'{district} - Stress', line=dict(color='red'),
                          yaxis='y2'),
                row=row, col=col
            )
        
        fig.update_layout(height=800, title_text="Groundwater Depletion Time Series", 
                         showlegend=False)
        
        timeseries_path = self.config.get_output_path('depletion_timeseries.html')
        fig.write_html(timeseries_path)
        return timeseries_path
    
    def _create_risk_evolution(self, features_data):
        """Create risk evolution over time graph"""
        df = features_data.copy()
        
        # Calculate risk counts over time
        risk_evolution = df.groupby(['date', 'risk_level']).size().reset_index(name='count')
        
        fig_risk = px.area(risk_evolution, x='date', y='count', color='risk_level',
                          color_discrete_map={'Low': 'green', 'Moderate': 'yellow', 'Critical': 'red'},
                          title='Evolution of Risk Levels Over Time')
        
        risk_evolution_path = self.config.get_output_path('risk_evolution.html')
        fig_risk.write_html(risk_evolution_path)
        return risk_evolution_path
    
    def _create_feature_importance(self, features_data):
        """Create feature importance visualization"""
        # This would typically use model results
        # For now, create a correlation heatmap
        numeric_cols = features_data.select_dtypes(include=[np.number]).columns
        correlation_data = features_data[numeric_cols].corr()
        
        fig = px.imshow(correlation_data, 
                       title='Feature Correlation Heatmap',
                       color_continuous_scale='RdBu_r',
                       aspect="auto")
        
        importance_path = self.config.get_output_path('feature_correlations.html')
        fig.write_html(importance_path)
        return importance_path