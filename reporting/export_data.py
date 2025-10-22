"""
Data export functionality
"""

import pandas as pd
from config import Config

class DataExporter:
    """Handle data export operations"""
    
    def __init__(self):
        self.config = Config
    
    def export_all_data(self, processed_data, models_results):
        """Export all data files"""
        print("   💾 Exporting data files...")
        
        output_files = []
        
        # Export risk assessment data
        risk_csv_path = self.config.get_output_path('district_risk_assessment.csv')
        models_results['risk_assessment'].to_csv(risk_csv_path, index=False)
        output_files.append(risk_csv_path)
        
        # Export panel data
        panel_csv_path = self.config.get_output_path('panel_data.csv')
        processed_data['panel_data'].to_csv(panel_csv_path, index=False)
        output_files.append(panel_csv_path)
        
        # Export feature importance
        importance_path = self.config.get_output_path('feature_importance.csv')
        models_results['model_results']['feature_importance'].to_csv(importance_path, index=False)
        output_files.append(importance_path)
        
        # Export model performance
        performance_path = self.config.get_output_path('model_performance.csv')
        pd.DataFrame([models_results['model_results']['model_performance']]).to_csv(performance_path, index=False)
        output_files.append(performance_path)
        
        print("   ✅ Data exports completed")
        return output_files