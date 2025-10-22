"""
Reporting module for generating outputs and summaries
"""

from .export_data import DataExporter
from .generate_reports import ReportGenerator

class ReportGenerator:
    """Main reporting coordinator"""
    
    def __init__(self):
        self.data_exporter = DataExporter()
        self.report_generator = ReportGenerator()
    
    def generate_all_reports(self, processed_data, models_results, visualization_files):
        """Generate all reports and exports"""
        print("\n📋 5. Reporting Phase...")
        
        # Export data files
        export_files = self.data_exporter.export_all_data(processed_data, models_results)
        
        # Generate reports
        report_files = self.report_generator.generate_reports(processed_data, models_results)
        
        all_files = export_files + report_files + visualization_files
        
        print("✅ Reporting completed successfully!")
        return all_files