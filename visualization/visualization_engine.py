"""
Main visualization coordinator
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

class VisualizationEngine:
    """Main visualization coordinator"""
    
    def __init__(self, config):
        self.config = config
        plt.style.use('seaborn-v0_8')
    
    def create_all_visualizations(self, processed_data, models_results):
        """Create all visualizations"""
        print("📈 Creating comprehensive visualizations...")
        
        output_files = []
        
        # 1. Risk Distribution Plot
        print("   📊 Creating risk distribution...")
        dist_file = self._create_risk_distribution(models_results['risk_assessment'])
        output_files.append(dist_file)
        
        # 2. Risk Map
        print("   🗺️ Creating risk map...")
        map_file = self._create_risk_map(models_results['risk_assessment'])
        output_files.append(map_file)
        
        # 3. Time Series Analysis
        print("   📈 Creating time series plots...")
        ts_file = self._create_time_series_plots(processed_data)
        output_files.append(ts_file)
        
        # 4. Feature Importance
        print("   🔍 Creating feature importance plot...")
        fi_file = self._create_feature_importance(models_results['model_results']['feature_importance'])
        output_files.append(fi_file)
        
        # 5. Risk Score Distribution
        print("   📋 Creating risk score distribution...")
        score_file = self._create_risk_score_distribution(models_results['risk_assessment'])
        output_files.append(score_file)
        
        # 6. Correlation Heatmap
        print("   🔗 Creating correlation heatmap...")
        corr_file = self._create_correlation_heatmap(processed_data)
        output_files.append(corr_file)
        
        print(f"✅ Visualization completed: {len(output_files)} visualizations created")
        return output_files
    
    def _create_risk_distribution(self, risk_assessment):
        """Create risk level distribution plot"""
        plt.figure(figsize=(12, 8))
        
        risk_counts = risk_assessment['risk_level'].value_counts()
        colors = {'Critical': 'red', 'Moderate': 'orange', 'Low': 'green'}
        
        # Create bar plot
        bars = plt.bar(risk_counts.index, risk_counts.values, 
                      color=[colors.get(level, 'gray') for level in risk_counts.index],
                      edgecolor='black', linewidth=1.5, alpha=0.8)
        
        plt.title('Groundwater Depletion Risk Distribution Across Districts', 
                 fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Risk Level', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Districts', fontsize=12, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, count in zip(bars, risk_counts.values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{count} districts', ha='center', va='bottom', 
                    fontweight='bold', fontsize=11)
        
        # Add percentage labels
        total = len(risk_assessment)
        for i, (level, count) in enumerate(risk_counts.items()):
            percentage = (count / total) * 100
            plt.text(i, count/2, f'{percentage:.1f}%', ha='center', va='center',
                    fontweight='bold', fontsize=14, color='white')
        
        plt.tight_layout()
        file_path = self.config.get_output_path('risk_distribution.png')
        plt.savefig(file_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return file_path
    
    def _create_risk_map(self, risk_assessment):
        """Create geographic risk map"""
        plt.figure(figsize=(14, 10))
        
        colors = {'Critical': 'red', 'Moderate': 'orange', 'Low': 'green'}
        sizes = {'Critical': 150, 'Moderate': 100, 'Low': 80}
        
        # Plot each risk level with different colors and sizes
        for level, color in colors.items():
            level_data = risk_assessment[risk_assessment['risk_level'] == level]
            if not level_data.empty:
                plt.scatter(level_data['center_lon'], level_data['center_lat'],
                           c=color, label=f'{level} Risk', 
                           s=sizes[level], alpha=0.7, edgecolors='black', linewidth=0.8)
        
        # Add labels for critical districts
        critical_districts = risk_assessment[risk_assessment['risk_level'] == 'Critical']
        for _, district in critical_districts.iterrows():
            plt.annotate(district['district'], 
                        (district['center_lon'], district['center_lat']),
                        xytext=(8, 8), textcoords='offset points',
                        fontsize=8, fontweight='bold', alpha=0.8,
                        bbox=dict(boxstyle="round,pad=0.3", facecolor='red', alpha=0.2))
        
        plt.xlabel('Longitude', fontsize=12, fontweight='bold')
        plt.ylabel('Latitude', fontsize=12, fontweight='bold')
        plt.title('District-wise Groundwater Depletion Risk Map', 
                 fontsize=16, fontweight='bold', pad=20)
        plt.legend(title='Risk Level', title_fontsize=12, fontsize=10)
        plt.grid(True, alpha=0.3)
        
        # Add map styling
        plt.gca().set_facecolor('#f5f5f5')
        
        plt.tight_layout()
        file_path = self.config.get_output_path('risk_map.png')
        plt.savefig(file_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return file_path
    
    def _create_time_series_plots(self, processed_data):
        """Create time series analysis plots"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Groundwater Depletion Time Series Analysis', 
                    fontsize=16, fontweight='bold', y=0.98)
        
        # Sample 4 districts for demonstration
        sample_districts = processed_data['district'].unique()[:4]
        
        for i, district in enumerate(sample_districts):
            ax = axes[i//2, i%2]
            district_data = processed_data[processed_data['district'] == district].sort_values('date')
            
            # Plot TWS anomaly
            ax.plot(district_data['date'], district_data['tws_anomaly'], 
                   label='TWS Anomaly', color='blue', linewidth=2, alpha=0.8)
            
            # Plot water stress
            ax_twin = ax.twinx()
            ax_twin.plot(district_data['date'], district_data['water_stress'], 
                        label='Water Stress', color='red', linewidth=2, alpha=0.8, linestyle='--')
            
            ax.set_title(f'District: {district}', fontweight='bold')
            ax.set_xlabel('Date')
            ax.set_ylabel('TWS Anomaly (cm)', color='blue')
            ax_twin.set_ylabel('Water Stress', color='red')
            
            ax.grid(True, alpha=0.3)
            ax.legend(loc='upper left')
            ax_twin.legend(loc='upper right')
        
        plt.tight_layout()
        file_path = self.config.get_output_path('time_series_analysis.png')
        plt.savefig(file_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return file_path
    
    def _create_feature_importance(self, feature_importance):
        """Create feature importance visualization"""
        plt.figure(figsize=(12, 8))
        
        if feature_importance.empty:
            plt.text(0.5, 0.5, 'No feature importance data available', 
                    ha='center', va='center', transform=plt.gca().transAxes,
                    fontsize=14, fontweight='bold')
        else:
            # Get top 10 features
            top_features = feature_importance.head(10)
            
            # Create horizontal bar plot
            bars = plt.barh(top_features['feature'], top_features['importance'],
                           color=plt.cm.viridis(np.linspace(0, 1, len(top_features))),
                           edgecolor='black', linewidth=0.5, alpha=0.8)
            
            plt.xlabel('Feature Importance Score', fontsize=12, fontweight='bold')
            plt.title('Top Feature Importance for Water Stress Prediction', 
                     fontsize=16, fontweight='bold', pad=20)
            plt.gca().invert_yaxis()
            plt.grid(True, alpha=0.3, axis='x')
            
            # Add value labels
            for bar, importance in zip(bars, top_features['importance']):
                plt.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                        f'{importance:.3f}', ha='left', va='center', 
                        fontweight='bold', fontsize=10)
        
        plt.tight_layout()
        file_path = self.config.get_output_path('feature_importance.png')
        plt.savefig(file_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return file_path
    
    def _create_risk_score_distribution(self, risk_assessment):
        """Create risk score distribution histogram"""
        plt.figure(figsize=(12, 8))
        
        # Create histogram with different colors for risk levels
        colors = {'Critical': 'red', 'Moderate': 'orange', 'Low': 'green'}
        
        for level, color in colors.items():
            level_data = risk_assessment[risk_assessment['risk_level'] == level]
            if not level_data.empty:
                plt.hist(level_data['risk_score'], bins=20, alpha=0.6, 
                        color=color, label=f'{level} Risk', edgecolor='black', linewidth=0.5)
        
        # Add threshold lines
        plt.axvline(x=0.33, color='green', linestyle='--', linewidth=2, alpha=0.8, label='Low Threshold')
        plt.axvline(x=0.66, color='orange', linestyle='--', linewidth=2, alpha=0.8, label='Moderate Threshold')
        plt.axvline(x=1.0, color='red', linestyle='--', linewidth=2, alpha=0.8, label='Critical Threshold')
        
        plt.xlabel('Risk Score', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Districts', fontsize=12, fontweight='bold')
        plt.title('Distribution of Groundwater Depletion Risk Scores', 
                 fontsize=16, fontweight='bold', pad=20)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Add statistics text
        stats_text = f"""Statistics:
Mean: {risk_assessment['risk_score'].mean():.3f}
Std: {risk_assessment['risk_score'].std():.3f}
Max: {risk_assessment['risk_score'].max():.3f}
Min: {risk_assessment['risk_score'].min():.3f}"""
        
        plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle="round", facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        file_path = self.config.get_output_path('risk_score_distribution.png')
        plt.savefig(file_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return file_path
    
    def _create_correlation_heatmap(self, processed_data):
        """Create correlation heatmap of key variables"""
        plt.figure(figsize=(12, 10))
        
        # Select key numeric columns for correlation
        numeric_columns = ['tws_anomaly', 'rainfall', 'water_stress', 
                          'crop_intensity', 'population_density', 'gw_irrigation_ratio']
        
        available_columns = [col for col in numeric_columns if col in processed_data.columns]
        
        if len(available_columns) >= 3:
            # Calculate correlation matrix
            corr_matrix = processed_data[available_columns].corr()
            
            # Create heatmap
            mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
            sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm', 
                       center=0, square=True, linewidths=0.5,
                       cbar_kws={"shrink": .8}, fmt='.2f',
                       annot_kws={'size': 10, 'weight': 'bold'})
            
            plt.title('Correlation Matrix of Key Variables', 
                     fontsize=16, fontweight='bold', pad=20)
        else:
            plt.text(0.5, 0.5, 'Insufficient data for correlation analysis', 
                    ha='center', va='center', transform=plt.gca().transAxes,
                    fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        file_path = self.config.get_output_path('correlation_heatmap.png')
        plt.savefig(file_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return file_path