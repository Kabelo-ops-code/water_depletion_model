"""
Build interactive dashboard components
"""

import pandas as pd
import os

class DashboardBuilder:
    """Build interactive dashboard components"""
    
    def __init__(self, config):
        self.config = config
    
    def build_dashboard(self, processed_data, models_results):
        """Create interactive dashboard"""
        output_files = []
        
        # Create HTML dashboard
        dashboard_html = self._create_dashboard_html(processed_data, models_results)
        dashboard_path = self.config.get_output_path('interactive_dashboard.html')
        
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(dashboard_html)
        
        output_files.append(dashboard_path)
        
        # Create summary report with embedded images
        summary_html = self._create_summary_report(processed_data, models_results)
        summary_path = self.config.get_output_path('summary_report.html')
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_html)
        
        output_files.append(summary_path)
        
        return output_files
    
    def _create_dashboard_html(self, processed_data, models_results):
        """Create interactive HTML dashboard"""
        risk_data = models_results['risk_assessment']
        risk_counts = risk_data['risk_level'].value_counts()
        model_perf = models_results['model_results']['model_performance']
        feature_importance = models_results['model_results']['feature_importance']
        
        # Format feature importance for display
        feature_html = ""
        if not feature_importance.empty:
            for _, row in feature_importance.head(5).iterrows():
                feature_html += f"""
                <div class="feature-row">
                    <span class="feature-name">{row['feature']}</span>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {row['importance']*100:.1f}%"></div>
                    </div>
                    <span class="feature-value">{row['importance']:.3f}</span>
                </div>
                """
        
        # Critical districts table
        critical_districts = risk_data[risk_data['risk_level'] == 'Critical'].head(10)
        critical_html = ""
        for _, district in critical_districts.iterrows():
            critical_html += f"""
            <tr>
                <td>{district['district']}</td>
                <td>{district['risk_score']:.3f}</td>
                <td>{district['water_stress']:.2f}</td>
                <td>{district['population_density']:.0f}</td>
            </tr>
            """
        
        dashboard_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Water Depletion Risk Dashboard</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                }}
                .dashboard {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 20px;
                    max-width: 1200px;
                    margin: 0 auto;
                }}
                .card {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .card-full {{ grid-column: span 2; }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 15px;
                    margin-bottom: 20px;
                }}
                .stat-card {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                }}
                .stat-number {{
                    font-size: 2em;
                    font-weight: bold;
                    margin: 10px 0;
                }}
                .feature-row {{
                    display: flex;
                    align-items: center;
                    margin: 8px 0;
                    padding: 5px;
                }}
                .progress-bar {{
                    flex-grow: 1;
                    height: 20px;
                    background: #ecf0f1;
                    border-radius: 10px;
                    margin: 0 10px;
                    overflow: hidden;
                }}
                .progress-fill {{
                    height: 100%;
                    background: linear-gradient(90deg, #3498db, #2ecc71);
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #34495e;
                    color: white;
                }}
                .critical {{ color: #e74c3c; font-weight: bold; }}
                .moderate {{ color: #f39c12; }}
                .low {{ color: #27ae60; }}
            </style>
        </head>
        <body>
            <h1>🚰 Groundwater Depletion Risk Dashboard</h1>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div>Critical Risk</div>
                    <div class="stat-number">{risk_counts.get('Critical', 0)}</div>
                    <div>Districts</div>
                </div>
                <div class="stat-card">
                    <div>Moderate Risk</div>
                    <div class="stat-number">{risk_counts.get('Moderate', 0)}</div>
                    <div>Districts</div>
                </div>
                <div class="stat-card">
                    <div>Low Risk</div>
                    <div class="stat-number">{risk_counts.get('Low', 0)}</div>
                    <div>Districts</div>
                </div>
            </div>
            
            <div class="dashboard">
                <div class="card">
                    <h3>📊 Risk Distribution</h3>
                    <img src="risk_distribution.png" width="100%" alt="Risk Distribution">
                </div>
                
                <div class="card">
                    <h3>🔍 Top Risk Factors</h3>
                    <div class="feature-list">
                        {feature_html}
                    </div>
                </div>
                
                <div class="card">
                    <h3>🚨 Critical Districts</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>District</th>
                                <th>Risk Score</th>
                                <th>Water Stress</th>
                                <th>Population Density</th>
                            </tr>
                        </thead>
                        <tbody>
                            {critical_html}
                        </tbody>
                    </table>
                </div>
                
                <div class="card">
                    <h3>📈 Model Performance</h3>
                    <p><strong>R² Score:</strong> {model_perf['r2']:.3f}</p>
                    <p><strong>RMSE:</strong> {model_perf['rmse']:.3f}</p>
                    <p><strong>Cross-validation Score:</strong> {model_perf['cv_mean']:.3f} ± {model_perf['cv_std']:.3f}</p>
                </div>
                
                <div class="card card-full">
                    <h3>🗺️ Risk Map</h3>
                    <img src="risk_level_map.png" width="100%" alt="Risk Map">
                </div>
                
                <div class="card card-full">
                    <h3>📈 Time Series Analysis</h3>
                    <img src="time_series_analysis.png" width="100%" alt="Time Series">
                </div>
            </div>
        </body>
        </html>
        """
        
        return dashboard_html
    
    def _create_summary_report(self, processed_data, models_results):
        """Create summary HTML report"""
        risk_data = models_results['risk_assessment']
        total_districts = len(risk_data)
        
        summary_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Water Depletion Risk Summary</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .summary-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
                .image-container {{ text-align: center; margin: 20px 0; }}
                img {{ max-width: 100%; height: auto; border: 1px solid #ddd; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Water Depletion Risk Assessment Summary</h1>
                <p>Analysis of {total_districts} districts | Generated on {pd.Timestamp.now().strftime('%Y-%m-%d')}</p>
            </div>
            
            <div class="summary-grid">
                <div class="image-container">
                    <h3>Risk Distribution</h3>
                    <img src="risk_distribution.png" alt="Risk Distribution">
                </div>
                
                <div class="image-container">
                    <h3>Feature Importance</h3>
                    <img src="feature_importance.png" alt="Feature Importance">
                </div>
                
                <div class="image-container">
                    <h3>Risk Map</h3>
                    <img src="risk_level_map.png" alt="Risk Map">
                </div>
                
                <div class="image-container">
                    <h3>Correlation Analysis</h3>
                    <img src="correlation_analysis.png" alt="Correlation">
                </div>
            </div>
        </body>
        </html>
        """
        
        return summary_html