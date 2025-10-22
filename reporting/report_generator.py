"""
Generate comprehensive text reports
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

class ReportGenerator:
    """Generate comprehensive text reports"""
    
    def __init__(self, config):
        self.config = config
    
    def generate_reports(self, processed_data, models_results):
        """Generate all text reports"""
        output_files = []
        
        # 1. Main technical report
        technical_report = self._generate_technical_report(processed_data, models_results)
        tech_path = self.config.get_output_path('technical_report.md')
        with open(tech_path, 'w', encoding='utf-8') as f:
            f.write(technical_report)
        output_files.append(tech_path)
        
        # 2. Executive summary
        executive_summary = self._generate_executive_summary(models_results)
        exec_path = self.config.get_output_path('executive_summary.md')
        with open(exec_path, 'w', encoding='utf-8') as f:
            f.write(executive_summary)
        output_files.append(exec_path)
        
        # 3. Risk assessment details
        risk_details = self._generate_risk_details_report(models_results)
        risk_path = self.config.get_output_path('risk_assessment_details.md')
        with open(risk_path, 'w', encoding='utf-8') as f:
            f.write(risk_details)
        output_files.append(risk_path)
        
        print(f"      ✅ Text reports generated: {len(output_files)} files")
        return output_files
    
    def _generate_technical_report(self, processed_data, models_results):
        """Generate comprehensive technical report"""
        risk_data = models_results['risk_assessment']
        risk_counts = risk_data['risk_level'].value_counts()
        total_districts = len(risk_data)
        model_perf = models_results['model_results']['model_performance']
        feature_importance = models_results['model_results']['feature_importance']
        evaluation = models_results.get('evaluation_results', {})
        
        # Format feature importance table
        feature_table = ""
        if not feature_importance.empty:
            for _, row in feature_importance.iterrows():
                feature_table += f"| {row['feature']} | {row['importance']:.4f} |\n"
        
        # Critical districts table
        critical_districts = risk_data[risk_data['risk_level'] == 'Critical']
        critical_table = ""
        for _, district in critical_districts.iterrows():
            critical_table += f"| {district['district']} | {district['risk_score']:.3f} | {district['water_stress']:.2f} | {district['population_density']:.0f} |\n"
        
        report = f"""# Technical Report: Underground Water Depletion Risk Modeling

## Executive Summary

- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Districts Analyzed**: {total_districts}
- **Critical Risk Districts**: {risk_counts.get('Critical', 0)}
- **Model Performance (R²)**: {model_perf['r2']:.3f}

## 1. Methodology

### 1.1 Data Sources
- **GRACE Satellite Data**: Terrestrial Water Storage anomalies
- **Rainfall Data**: Monthly precipitation estimates
- **Agricultural Statistics**: Crop intensity and irrigation data
- **Population Data**: District-level demographic information

### 1.2 Feature Engineering
- Temporal aggregation and rolling statistics
- Derived indices (Crop Stress, Rainfall Variability)
- Normalization and standardization
- Trend analysis and acceleration metrics

### 1.3 Modeling Approach
- **Algorithm**: Random Forest Regressor
- **Target Variable**: Water Stress Index
- **Cross-validation**: {self.config.CROSS_VALIDATION}-fold
- **Hyperparameters**: 
  - n_estimators: {self.config.N_ESTIMATORS}
  - test_size: {self.config.TEST_SIZE}
  - random_state: {self.config.RANDOM_STATE}

## 2. Model Performance

### 2.1 Key Metrics
| Metric | Value |
|--------|-------|
| R² Score | {model_perf['r2']:.3f} |
| RMSE | {model_perf['rmse']:.3f} |
| MSE | {model_perf['mse']:.3f} |
| Cross-validation Mean | {model_perf['cv_mean']:.3f} |
| Cross-validation Std | {model_perf['cv_std']:.3f} |

### 2.2 Feature Importance
| Feature | Importance |
|---------|------------|
{feature_table}

## 3. Risk Assessment Results

### 3.1 Risk Distribution
| Risk Level | Districts | Percentage |
|------------|-----------|------------|
| Critical | {risk_counts.get('Critical', 0)} | {risk_counts.get('Critical', 0)/total_districts*100:.1f}% |
| Moderate | {risk_counts.get('Moderate', 0)} | {risk_counts.get('Moderate', 0)/total_districts*100:.1f}% |
| Low | {risk_counts.get('Low', 0)} | {risk_counts.get('Low', 0)/total_districts*100:.1f}% |

### 3.2 Critical Districts
| District | Risk Score | Water Stress | Population Density |
|----------|------------|--------------|-------------------|
{critical_table}

## 4. Risk Factor Analysis

### 4.1 Weighting Scheme
| Risk Factor | Weight |
|-------------|--------|
| Water Stress | 30% |
| Crop Stress Index | 25% |
| Rainfall Variability | 20% |
| Depletion Acceleration | 15% |
| Groundwater Irrigation Ratio | 10% |

### 4.2 Thresholds
- **Low Risk**: ≤ {self.config.RISK_THRESHOLDS['low']}
- **Moderate Risk**: {self.config.RISK_THRESHOLDS['low']} - {self.config.RISK_THRESHOLDS['moderate']}
- **Critical Risk**: > {self.config.RISK_THRESHOLDS['moderate']}

## 5. Data Quality Assessment

### 5.1 Data Completeness
- Total records processed: {len(processed_data):,}
- Districts with complete data: {total_districts}
- Temporal coverage: {self.config.START_DATE} to {self.config.END_DATE}

### 5.2 Model Reliability
- **Prediction Accuracy**: {'High' if model_perf['r2'] > 0.7 else 'Medium' if model_perf['r2'] > 0.5 else 'Low'}
- **Model Stability**: {'High' if model_perf['cv_std'] < 0.1 else 'Medium' if model_perf['cv_std'] < 0.2 else 'Low'}
- **Feature Quality**: {'Good' if len(feature_importance[feature_importance['importance'] > 0.1]) >= 3 else 'Adequate'}

## 6. Limitations and Assumptions

### 6.1 Data Limitations
- Synthetic data used for demonstration
- Spatial resolution limited to district level
- Climate change impacts not fully incorporated
- Local hydrological variations may not be captured

### 6.2 Modeling Assumptions
- Linear relationships in some risk factor combinations
- Stationarity assumption in time series analysis
- Independence of some correlated features

## 7. Recommendations for Future Work

1. **Data Enhancement**
   - Incorporate real satellite data streams
   - Add local groundwater monitoring data
   - Include climate projection data

2. **Model Improvements**
   - Experiment with deep learning approaches
   - Incorporate spatial autocorrelation
   - Add uncertainty quantification

3. **Operational Enhancements**
   - Real-time monitoring capabilities
   - Automated alert systems
   - Integration with water management policies

## Appendix

### A. Configuration Parameters
- Analysis period: {self.config.START_DATE} to {self.config.END_DATE}
- Number of districts: {self.config.N_DISTRICTS}
- Random state: {self.config.RANDOM_STATE}
- Test size: {self.config.TEST_SIZE}

### B. Output Files
- Risk assessment data: `district_risk_assessment.csv`
- Model performance: `model_performance.csv`
- Feature importance: `feature_importance.csv`
- Visualizations: Various PNG files
- Interactive dashboard: `interactive_dashboard.html`

---
*Generated automatically by Water Depletion Risk Modeling System v{self.config.VERSION}*
"""
        
        return report
    
    def _generate_executive_summary(self, models_results):
        """Generate executive summary report"""
        risk_data = models_results['risk_assessment']
        risk_counts = risk_data['risk_level'].value_counts()
        total_districts = len(risk_data)
        model_perf = models_results['model_results']['model_performance']
        
        # Get top critical districts
        critical_districts = risk_data[risk_data['risk_level'] == 'Critical'].head(5)
        critical_list = "\n".join([f"- {row['district']} (Risk: {row['risk_score']:.3f})" 
                                 for _, row in critical_districts.iterrows()])
        
        summary = f"""# Executive Summary: Water Depletion Risk Assessment

## Key Findings

### Risk Distribution
- **Total Districts Analyzed**: {total_districts}
- **Critical Risk**: {risk_counts.get('Critical', 0)} districts
- **Moderate Risk**: {risk_counts.get('Moderate', 0)} districts  
- **Low Risk**: {risk_counts.get('Low', 0)} districts

### Model Performance
- **Prediction Accuracy (R²)**: {model_perf['r2']:.3f}
- **Model Reliability**: {'High' if model_perf['cv_std'] < 0.1 else 'Medium' if model_perf['cv_std'] < 0.2 else 'Low'}

## Critical Districts Requiring Immediate Attention

{critical_list if not critical_districts.empty else "No critical districts identified"}

## Recommended Actions

### 🚨 Immediate Actions (Critical Districts)
1. Implement water conservation measures
2. Restrict new groundwater extraction permits
3. Deploy emergency monitoring systems
4. Develop alternative water sources

### ⚠️ Short-term Actions (Moderate Districts)
1. Enhanced monitoring and reporting
2. Water efficiency programs
3. Agricultural best practices promotion
4. Community awareness campaigns

### ✅ Long-term Planning (All Districts)
1. Sustainable water management policies
2. Infrastructure development
3. Climate resilience planning
4. Cross-district collaboration

## Economic and Social Implications

- **Population at Risk**: Approximately {risk_data['population_density'].sum():.0f} people across analyzed districts
- **Agricultural Impact**: {len(critical_districts)} critical districts affecting food production
- **Water Security**: {risk_counts.get('Critical', 0) + risk_counts.get('Moderate', 0)} districts facing water stress

## Next Steps

1. **Validation**: Ground truth verification in critical districts
2. **Stakeholder Engagement**: Present findings to local authorities
3. **Policy Development**: Incorporate results into water management plans
4. **Monitoring**: Establish ongoing assessment system

---
*Report generated on {datetime.now().strftime('%Y-%m-%d')}*
*For detailed technical analysis, refer to the full technical report*
"""
        
        return summary
    
    def _generate_risk_details_report(self, models_results):
        """Generate detailed risk assessment report"""
        risk_data = models_results['risk_assessment']
        
        # Sort by risk score
        risk_data_sorted = risk_data.sort_values('risk_score', ascending=False)
        
        # Create detailed table
        details_table = ""
        for _, row in risk_data_sorted.iterrows():
            risk_color = {
                'Critical': '🔴',
                'Moderate': '🟡', 
                'Low': '🟢'
            }.get(row['risk_level'], '⚪')
            
            details_table += f"| {risk_color} {row['district']} | {row['risk_score']:.3f} | {row['risk_level']} | {row['water_stress']:.2f} | {row['population_density']:.0f} |\n"
        
        report = f"""# Detailed Risk Assessment Report

## Risk Assessment for All Districts

| District | Risk Score | Risk Level | Water Stress | Population Density |
|----------|------------|------------|--------------|-------------------|
{details_table}

## Risk Score Interpretation

- **0.00 - 0.33**: Low Risk - Sustainable conditions
- **0.34 - 0.66**: Moderate Risk - Monitoring recommended  
- **0.67 - 1.00**: Critical Risk - Immediate action required

## Key Metrics Summary

- **Highest Risk Score**: {risk_data['risk_score'].max():.3f}
- **Lowest Risk Score**: {risk_data['risk_score'].min():.3f}
- **Average Risk Score**: {risk_data['risk_score'].mean():.3f}
- **Median Risk Score**: {risk_data['risk_score'].median():.3f}

## Distribution Analysis

- **Standard Deviation**: {risk_data['risk_score'].std():.3f}
- **Risk Score > 0.7**: {len(risk_data[risk_data['risk_score'] > 0.7])} districts
- **Risk Score < 0.3**: {len(risk_data[risk_data['risk_score'] < 0.3])} districts

---
*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Total districts assessed: {len(risk_data)}*
"""
        
        return report