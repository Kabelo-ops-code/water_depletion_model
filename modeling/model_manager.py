"""
Main modeling coordinator
"""

from .model_trainer import ModelTrainer
from .risk_classifier import RiskClassifier

class ModelManager:
    """Main modeling coordinator"""
    
    def __init__(self, config):
        self.config = config
        self.model_trainer = ModelTrainer(config)
        self.risk_classifier = RiskClassifier(config)
    
    def build_models(self, processed_data):
        """Build all models and classifications"""
        print("📊 Building statistical models...")
        
        # Train predictive models
        print("   🤖 Training predictive models...")
        model_results = self.model_trainer.train_models(processed_data)
        
        # Classify risk levels
        print("   🚨 Classifying risk levels...")
        risk_assessment = self.risk_classifier.classify_risk(processed_data, model_results)
        
        # Combine all results
        final_results = {
            'model_results': model_results,
            'risk_assessment': risk_assessment
        }
        
        print("✅ Statistical modeling completed successfully!")
        return final_results