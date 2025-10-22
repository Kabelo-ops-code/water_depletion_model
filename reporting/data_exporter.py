"""
Data export functionality
"""

import pandas as pd
import numpy as np
import os
import joblib

class DataExporter:
    """Handle data export operations"""
    
    def __init__(self, config):
        self.config = config
    
    def export_all_data(self, processed_data, models_results):
        """Export all data files"""
        output_files = []
        
        # 1. Export risk assessment data
        risk_data = models_results['risk_assessment']
        risk_csv_path = self.config.get_output_path('district_risk_assessment.csv')
        risk_data.to_csv(risk_csv_path, index=False)
        output_files.append(risk_csv_path)
        print(f"      ✅ Risk assessment data exported: {len(risk_data)} districts")
        
        # 2. Export panel data sample (avoid huge files)
        panel_data = processed_data
        panel_sample_path = self.config.get_output_path('panel_data_sample.csv')
        sample_size = min(5000, len(panel_data))
        panel_data.sample(sample_size).to_csv(panel_sample_path, index=False)
        output_files.append(panel_sample_path)
        print(f"      ✅ Panel data sample exported: {sample_size} records")
        
        # 3. Export feature importance
        feature_importance = models_results['model_results']['feature_importance']
        feature_path = self.config.get_output_path('feature_importance.csv')
        feature_importance.to_csv(feature_path, index=False)
        output_files.append(feature_path)
        print(f"      ✅ Feature importance exported: {len(feature_importance)} features")
        
        # 4. Export model performance metrics
        model_perf = models_results['model_results']['model_performance']
        perf_df = pd.DataFrame([model_perf])
        perf_path = self.config.get_output_path('model_performance.csv')
        perf_df.to_csv(perf_path, index=False)
        output_files.append(perf_path)
        print(f"      ✅ Model performance metrics exported")
        
        # 5. Export critical districts list
        critical_districts = risk_data[risk_data['risk_level'] == 'Critical']
        if not critical_districts.empty:
            critical_path = self.config.get_output_path('critical_districts.csv')
            critical_districts.to_csv(critical_path, index=False)
            output_files.append(critical_path)
            print(f"      ✅ Critical districts list exported: {len(critical_districts)} districts")
        
        # 6. Export risk trends data
        if 'risk_trend_slope' in risk_data.columns:
            trends_data = risk_data[['district', 'risk_trend_slope', 'risk_trend_direction', 'recent_risk_change']]
            trends_path = self.config.get_output_path('risk_trends.csv')
            trends_data.to_csv(trends_path, index=False)
            output_files.append(trends_path)
            print(f"      ✅ Risk trends data exported")
        
        # 7. Export model metadata
        metadata = {
            'model_training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_districts': len(risk_data),
            'critical_districts': len(critical_districts) if not critical_districts.empty else 0,
            'model_r2_score': model_perf['r2'],
            'model_rmse': model_perf['rmse'],
            'features_used': len(feature_importance),
            'training_samples': models_results['model_results'].get('training_data_size', 'Unknown')
        }
        metadata_df = pd.DataFrame([metadata])
        metadata_path = self.config.get_output_path('model_metadata.csv')
        metadata_df.to_csv(metadata_path, index=False)
        output_files.append(metadata_path)
        
        return output_files