#!/usr/bin/env python3
"""
Main entry point for Underground Water Depletion Risk Modeling
"""

import sys
import os
import logging

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_ingestion.data_collector import DataCollector
from data_processing.data_processor import DataProcessor
from modeling.model_manager import ModelManager
from visualization.visualization_engine import VisualizationEngine
from reporting.report_manager import ReportManager
from config import Config

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('water_depletion.log'),
            logging.StreamHandler()
        ]
    )

def main():
    """Main execution function"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("🚀 Starting Underground Water Depletion Risk Modeling...")
    logger.info("Initializing Water Depletion Risk Model")
    
    try:
        # Initialize all components
        config = Config()
        data_collector = DataCollector(config)
        data_processor = DataProcessor(config)
        model_manager = ModelManager(config)
        visualizer = VisualizationEngine(config)
        report_manager = ReportManager(config)
        
        # 1. Data Ingestion
        logger.info("Phase 1: Data Ingestion")
        print("\n📥 1. DATA INGESTION PHASE")
        print("-" * 30)
        raw_data = data_collector.collect_all_data()
        
        # 2. Data Processing
        logger.info("Phase 2: Data Processing")
        print("\n🔧 2. DATA PROCESSING PHASE")
        print("-" * 30)
        processed_data = data_processor.process_all_data(raw_data)
        
        # 3. Statistical Modeling
        logger.info("Phase 3: Statistical Modeling")
        print("\n📊 3. STATISTICAL MODELING PHASE")
        print("-" * 30)
        models_results = model_manager.build_models(processed_data)
        
        # 4. Visualization
        logger.info("Phase 4: Visualization")
        print("\n📈 4. VISUALIZATION PHASE")
        print("-" * 30)
        visualization_files = visualizer.create_all_visualizations(processed_data, models_results)
        
        # 5. Reporting
        logger.info("Phase 5: Reporting")
        print("\n📋 5. REPORTING PHASE")
        print("-" * 30)
        report_manager.generate_all_reports(processed_data, models_results, visualization_files)
        
        logger.info("✅ Project completed successfully!")
        print("\n🎉 PROJECT COMPLETED SUCCESSFULLY!")
        
        # Print final summary
        report_manager.print_summary(models_results)
        
    except Exception as e:
        logger.error(f"Project failed with error: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()