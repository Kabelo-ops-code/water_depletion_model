"""
Statistical modeling module for risk assessment
"""

from .feature_engineering import FeatureEngineer
from .time_series_model import TimeSeriesModel
from .risk_classification import RiskClassifier

class ModelBuilder:
    """Main modeling coordinator"""
    
    def __init__(self):
        self.feature_engineer = FeatureEngineer()
        self.time_series_model = TimeSeriesModel()
        self.risk_classifier = RiskClassifier()
    
    def build_models(self, processed_data):
        """Build all models and classifications"""
        print("\n📊 3. Statistical Modeling Phase...")
        
        # Feature engineering
        features_data = self.feature_engineer.create_features(processed_data['panel_data'])
        
        # Time series modeling
        model_results = self.time_series_model.train_models(features_data)
        
        # Risk classification
        risk_assessment = self.risk_classifier.classify_risk(features_data, model_results)
        
        results = {
            'features_data': features_data,
            'model_results': model_results,
            'risk_assessment': risk_assessment
        }
        
        print("✅ Statistical modeling completed successfully!")
        return results