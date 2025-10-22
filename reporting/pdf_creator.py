"""
Create PDF reports using matplotlib
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import os

class PDFCreator:
    """Create PDF reports using matplotlib"""
    
    def __init__(self, config):
        self.config = config
        plt.style.use(config.PLOT_STYLE)
    
    def create_pdf_reports(self, processed_data, models_results):
        """Create PDF versions of reports"""
        output_files = []
        
        try:
            # Create executive summary PDF
            exec_pdf = self._create_executive_summary_pdf(models_results)
            output_files.append(exec_pdf)
            
            # Create risk assessment PDF
            risk_pdf = self._create_risk_assessment_pdf(models_results)
            output_files.append(risk_pdf)
            
            print(f"      ✅ PDF reports generated: {len(output_files)} files")
            
        except Exception as e:
            print(f"      ⚠️  PDF creation skipped: {e}")
        
        return output_files
    
    def _create_executive_summary_pdf(self, models_results):
        """Create executive summary PDF"""
        risk_data = models_results['risk_assessment']
        risk_counts = risk_data['risk_level'].value_counts()
        total_districts = len(risk_data)
        model_perf = models_results['model_results']['model_performance']
        
        # Create figure
        fig = plt.figure(figsize=(8.27, 11.69))  # A4 size
        fig.suptitle('Executive Summary: Water Depletion Risk Assessment', 
                    fontsize=16, fontweight='bold', y=0.98)
        
        # Add header information
        plt.figtext(0.1, 0.95, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", fontsize=10)
        plt.figtext(0.1, 0.92, f"Districts Analyzed: {total_districts}", fontsize=10)
        
        # Summary section
        summary_text = f"""
KEY FINDINGS:

Risk Distribution:
• Critical Risk: {risk_counts.get('Critical', 0)} districts
• Moderate Risk: {risk_counts.get('Moderate', 0)} districts
• Low Risk: {risk_counts.get('Low', 0)} districts

Model Performance:
• Prediction Accuracy (R²): {model_perf['r2']:.3f}
• Model Reliability: {'High' if model_perf['cv_std'] < 0.1 else 'Medium'}

Top Critical Districts:
"""
        
        # Add critical districts
        critical_districts = risk_data[risk_data['risk_level'] == 'Critical'].head(5)
        for i, (_, district) in enumerate(critical_districts.iterrows()):
            summary_text += f"• {district['district']} (Risk: {district['risk_score']:.3f})\n"
        
        plt.figtext(0.1, 0.85, summary_text, fontsize=11, fontfamily='monospace')
        
        # Risk distribution plot
        ax1 = fig.add_axes([0.1, 0.5, 0.35, 0.3])
        colors = {'Critical': 'red', 'Moderate': 'orange', 'Low': 'green'}
        risk_colors = [colors.get(level, 'gray') for level in risk_counts.index]
        
        bars = ax1.bar(risk_counts.index, risk_counts.values, color=risk_colors)
        ax1.set_title('Risk Level Distribution', fontweight='bold')
        ax1.set_ylabel('Number of Districts')
        
        for bar, count in zip(bars, risk_counts.values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    str(count), ha='center', va='bottom', fontweight='bold')
        
        # Risk map simulation
        ax2 = fig.add_axes([0.55, 0.5, 0.4, 0.3])
        colors_scatter = {'Critical': 'red', 'Moderate': 'orange', 'Low': 'green'}
        
        for level, color in colors_scatter.items():
            level_data = risk_data[risk_data['risk_level'] == level]
            if not level_data.empty:
                ax2.scatter(level_data['center_lon'], level_data['center_lat'],
                           c=color, label=level, s=50, alpha=0.7)
        
        ax2.set_xlabel('Longitude')
        ax2.set_ylabel('Latitude')
        ax2.set_title('Risk Distribution Map', fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Recommendations section
        recommendations = """
RECOMMENDATIONS:

🚨 Critical Districts:
• Immediate water conservation
• Restrict new groundwater permits
• Emergency monitoring systems

⚠️ Moderate Districts:
• Enhanced monitoring
• Water efficiency programs
• Agricultural best practices

✅ All Districts:
• Sustainable water policies
• Climate resilience planning
• Cross-district collaboration
"""
        
        plt.figtext(0.1, 0.15, recommendations, fontsize=10, fontfamily='monospace')
        
        # Save PDF
        pdf_path = self.config.get_output_path('executive_summary.pdf')
        plt.savefig(pdf_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return pdf_path
    
    def _create_risk_assessment_pdf(self, models_results):
        """Create detailed risk assessment PDF"""
        risk_data = models_results['risk_assessment']
        feature_importance = models_results['model_results']['feature_importance']
        
        # Create figure
        fig = plt.figure(figsize=(8.27, 11.69))
        fig.suptitle('Detailed Risk Assessment Report', fontsize=16, fontweight='bold')
        
        # Risk scores distribution
        ax1 = fig.add_axes([0.1, 0.7, 0.8, 0.25])
        n, bins, patches = ax1.hist(risk_data['risk_score'], bins=20, 
                                   color='skyblue', edgecolor='black', alpha=0.7)
        
        # Color bars by risk level
        for i, (patch, left_edge, right_edge) in enumerate(zip(patches, bins[:-1], bins[1:])):
            if right_edge <= self.config.RISK_THRESHOLDS['low']:
                patch.set_facecolor('green')
            elif left_edge <= self.config.RISK_THRESHOLDS['moderate']:
                patch.set_facecolor('orange')
            else:
                patch.set_facecolor('red')
        
        ax1.axvline(self.config.RISK_THRESHOLDS['low'], color='green', linestyle='--', alpha=0.7, label='Low Threshold')
        ax1.axvline(self.config.RISK_THRESHOLDS['moderate'], color='orange', linestyle='--', alpha=0.7, label='Moderate Threshold')
        ax1.axvline(self.config.RISK_THRESHOLDS['critical'], color='red', linestyle='--', alpha=0.7, label='Critical Threshold')
        
        ax1.set_xlabel('Risk Score')
        ax1.set_ylabel('Number of Districts')
        ax1.set_title('Distribution of Risk Scores', fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Feature importance
        ax2 = fig.add_axes([0.1, 0.35, 0.8, 0.25])
        if not feature_importance.empty:
            top_features = feature_importance.head(8)
            y_pos = np.arange(len(top_features))
            
            bars = ax2.barh(y_pos, top_features['importance'])
            ax2.set_yticks(y_pos)
            ax2.set_yticklabels(top_features['feature'])
            ax2.invert_yaxis()
            ax2.set_xlabel('Importance Score')
            ax2.set_title('Top Feature Importance', fontweight='bold')
            ax2.grid(True, alpha=0.3, axis='x')
            
            # Add value labels
            for bar, importance in zip(bars, top_features['importance']):
                ax2.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                        f'{importance:.3f}', ha='left', va='center', fontsize=9)
        
        # Statistics section
        ax3 = fig.add_axes([0.1, 0.05, 0.8, 0.2])
        ax3.axis('off')
        
        stats_text = f"""
STATISTICAL SUMMARY:

Total Districts: {len(risk_data)}
Critical Risk: {len(risk_data[risk_data['risk_level'] == 'Critical'])}
Moderate Risk: {len(risk_data[risk_data['risk_level'] == 'Moderate'])}
Low Risk: {len(risk_data[risk_data['risk_level'] == 'Low'])}

Risk Score Statistics:
Mean: {risk_data['risk_score'].mean():.3f}
Median: {risk_data['risk_score'].median():.3f}
Std Dev: {risk_data['risk_score'].std():.3f}
Max: {risk_data['risk_score'].max():.3f}
Min: {risk_data['risk_score'].min():.3f}

Model Performance:
R² Score: {models_results['model_results']['model_performance']['r2']:.3f}
RMSE: {models_results['model_results']['model_performance']['rmse']:.3f}
"""
        
        ax3.text(0, 1, stats_text, transform=ax3.transAxes, fontsize=10,
                fontfamily='monospace', verticalalignment='top')
        
        # Save PDF
        pdf_path = self.config.get_output_path('risk_assessment_report.pdf')
        plt.savefig(pdf_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return pdf_path