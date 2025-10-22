"""
Generate various analysis plots and charts
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

class PlotGenerator:
    """Generate analysis plots and charts"""
    
    def __init__(self, config):
        self.config = config
        plt.style.use(config.PLOT_STYLE)
    
    def create_analysis_plots(self, processed_data, models_results):
        """Create various analysis plots"""
        output_files = []
        
        # 1. Risk Distribution Plot
        plt.figure(figsize=(10, 6))
        self._create_risk_distribution_plot(models_results['risk_assessment'])
        dist_path = self.config.get_output_path('risk_distribution.png')
        plt.savefig(dist_path, dpi=self.config.DPI, bbox_inches='tight')
        plt.close()
        output_files.append(dist_path)
        
        # 2. Feature Importance Plot
        plt.figure(figsize=(10, 6))
        self._create_feature_importance_plot(models_results['model_results']['feature_importance'])
        importance_path = self.config.get_output_path('feature_importance.png')
        plt.savefig(importance_path, dpi=self.config.DPI, bbox_inches='tight')
        plt.close()
        output_files.append(importance_path)
        
        # 3. Time Series Analysis
        plt.figure(figsize=(12, 8))
        self._create_time_series_plot(processed_data)
        timeseries_path = self.config.get_output_path('time_series_analysis.png')
        plt.savefig(timeseries_path, dpi=self.config.DPI, bbox_inches='tight')
        plt.close()
        output_files.append(timeseries_path)
        
        # 4. Correlation Analysis
        plt.figure(figsize=(10, 8))
        self._create_correlation_plot(processed_data)
        correlation_path = self.config.get_output_path('correlation_analysis.png')
        plt.savefig(correlation_path, dpi=self.config.DPI, bbox_inches='tight')
        plt.close()
        output_files.append(correlation_path)
        
        # 5. Risk Trends Plot
        plt.figure(figsize=(10, 6))
        self._create_risk_trends_plot(models_results['risk_assessment'])
        trends_path = self.config.get_output_path('risk_trends.png')
        plt.savefig(trends_path, dpi=self.config.DPI, bbox_inches='tight')
        plt.close()
        output_files.append(trends_path)
        
        return output_files
    
    def _create_risk_distribution_plot(self, risk_assessment):
        """Create risk level distribution plot"""
        risk_counts = risk_assessment['risk_level'].value_counts()
        colors = {'Critical': 'red', 'Moderate': 'orange', 'Low': 'green'}
        
        bars = plt.bar(risk_counts.index, risk_counts.values, 
                      color=[colors.get(level, 'gray') for level in risk_counts.index])
        
        plt.title('Distribution of Groundwater Depletion Risk Levels')
        plt.xlabel('Risk Level')
        plt.ylabel('Number of Districts')
        
        # Add value labels on bars
        for bar, count in zip(bars, risk_counts.values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    str(count), ha='center', va='bottom')
        
        plt.grid(True, alpha=0.3, axis='y')
    
    def _create_feature_importance_plot(self, feature_importance):
        """Create feature importance visualization"""
        if feature_importance.empty:
            plt.text(0.5, 0.5, 'No feature importance data available', 
                    ha='center', va='center', transform=plt.gca().transAxes)
            return
        
        top_features = feature_importance.head(10)
        
        plt.barh(top_features['feature'], top_features['importance'])
        plt.xlabel('Importance Score')
        plt.title('Top 10 Feature Importance for Water Stress Prediction')
        plt.gca().invert_yaxis()
        plt.grid(True, alpha=0.3, axis='x')
    
    def _create_time_series_plot(self, processed_data):
        """Create time series analysis plot"""
        # Sample a few districts for clarity
        sample_districts = processed_data['district'].unique()[:5]
        
        plt.figure(figsize=(12, 8))
        
        for i, district in enumerate(sample_districts, 1):
            district_data = processed_data[processed_data['district'] == district].sort_values('date')
            
            plt.subplot(2, 3, i)
            plt.plot(district_data['date'], district_data['tws_anomaly'], 
                    label='TWS Anomaly', linewidth=2)
            plt.plot(district_data['date'], district_data['water_stress'], 
                    label='Water Stress', linewidth=2, alpha=0.7)
            
            plt.title(f'District: {district}')
            plt.xlabel('Date')
            plt.ylabel('Value')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            if i >= 5:  # Limit to 5 subplots
                break
        
        plt.tight_layout()
    
    def _create_correlation_plot(self, processed_data):
        """Create correlation heatmap"""
        # Select numeric columns for correlation
        numeric_columns = processed_data.select_dtypes(include=[np.number]).columns
        correlation_data = processed_data[numeric_columns].corr()
        
        # Create heatmap
        mask = np.triu(np.ones_like(correlation_data, dtype=bool))
        sns.heatmap(correlation_data, mask=mask, annot=True, cmap='coolwarm', 
                   center=0, square=True, linewidths=0.5)
        plt.title('Feature Correlation Matrix')
    
    def _create_risk_trends_plot(self, risk_assessment):
        """Create risk trends visualization"""
        if 'risk_trend_slope' not in risk_assessment.columns:
            plt.text(0.5, 0.5, 'No trend data available', 
                    ha='center', va='center', transform=plt.gca().transAxes)
            return
        
        # Scatter plot of risk score vs trend
        colors = {'increasing': 'red', 'decreasing': 'green', 'stable': 'orange', 'unknown': 'gray'}
        
        plt.scatter(risk_assessment['risk_score'], 
                   risk_assessment['risk_trend_slope'],
                   c=[colors.get(direction, 'gray') for direction in risk_assessment['risk_trend_direction']],
                   s=100, alpha=0.7)
        
        plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        plt.axvline(x=self.config.RISK_THRESHOLDS['moderate'], color='red', linestyle='--', alpha=0.5)
        plt.axvline(x=self.config.RISK_THRESHOLDS['low'], color='orange', linestyle='--', alpha=0.5)
        
        plt.xlabel('Current Risk Score')
        plt.ylabel('Risk Trend Slope')
        plt.title('Current Risk vs Risk Trends')
        plt.grid(True, alpha=0.3)
        
        # Add legend
        from matplotlib.lines import Line2D
        legend_elements = [Line2D([0], [0], marker='o', color='w', 
                                 markerfacecolor=color, markersize=8, label=trend)
                          for trend, color in colors.items()]
        plt.legend(handles=legend_elements, title='Trend Direction')