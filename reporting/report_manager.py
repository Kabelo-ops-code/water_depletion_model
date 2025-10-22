"""
Main reporting coordinator
"""

import os
import pandas as pd
from datetime import datetime

class ReportManager:
    """Main reporting coordinator"""
    
    def __init__(self, config):
        self.config = config
    
    def generate_all_reports(self, processed_data, models_results, visualization_files):
        """Generate all reports and exports"""
        print("📋 Generating reports and exports...")
        
        # Export data files
        risk_data = models_results['risk_assessment']
        risk_csv_path = self.config.get_output_path('district_risk_assessment.csv')
        risk_data.to_csv(risk_csv_path, index=False)
        
        # Generate simple report
        risk_counts = risk_data['risk_level'].value_counts()
        total_districts = len(risk_data)
        model_perf = models_results['model_results']['model_performance']
        
        report = f"""# Water Depletion Risk Assessment Report

## Summary
- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Districts Analyzed: {total_districts}
- Critical Risk: {risk_counts.get('Critical', 0)} districts
- Moderate Risk: {risk_counts.get('Moderate', 0)} districts
- Low Risk: {risk_counts.get('Low', 0)} districts

## Model Performance
- R² Score: {model_perf['r2']:.3f}
- RMSE: {model_perf['rmse']:.3f}

## Output Files
- district_risk_assessment.csv
- risk_distribution.png
"""
        
        report_path = self.config.get_output_path('report.md')
        with open(report_path, 'w') as f:
            f.write(report)
        
        print("✅ Reporting completed successfully!")
        return [risk_csv_path, report_path]
    
    def print_summary(self, models_results):
        """Print final summary to console"""
        risk_data = models_results['risk_assessment']
        risk_counts = risk_data['risk_level'].value_counts()
        total_districts = len(risk_data)
        model_perf = models_results['model_results']['model_performance']
        
        print("\n" + "="*60)
        print("📊 FINAL PROJECT SUMMARY")
        print("="*60)
        print(f"\n🏘️  Districts: {total_districts}")
        print(f"🔴 Critical: {risk_counts.get('Critical', 0)}")
        print(f"🟡 Moderate: {risk_counts.get('Moderate', 0)}")
        print(f"🟢 Low: {risk_counts.get('Low', 0)}")
        print(f"\n🤖 Model R²: {model_perf['r2']:.3f}")
        print(f"\n💾 Output directory: {os.path.abspath(self.config.OUTPUT_DIR)}")