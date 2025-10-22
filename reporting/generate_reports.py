"""
Report generation functionality
"""

import pandas as pd
from datetime import datetime
from config import Config

class ReportGenerator:
    """Generate summary reports"""
    
    def __init__(self):
        self.config = Config
    
    def generate_reports(self, processed_data, models_results):
        """Generate all reports"""
        print("   📄 Generating reports...")
        
        output_files = []
        
        # Generate markdown report
        md_report = self._generate_markdown_report(processed_data, models_results)
        md_path = self.config.get_output_path('risk_assessment_report.md')
        with open(md_path, 'w') as f:
            f.write(md_report)
        output_files.append(md_path)
        
        # Generate PDF report
        pdf_path = self._generate_pdf_report(processed_data, models_results)
        if pdf_path:
            output_files.append(pdf_path)
        
        print("   ✅ Reports generated")
        return output_files
    
    def _generate_markdown_report(self, processed_data, models_results):
        """Generate markdown summary report"""
        
        risk_counts = models_results['risk_assessment']['risk_level'].value_counts()
        total_districts = len(models_results['risk_assessment'])
        model_perf = models_results['model_results']['model_performance']
        feature_importance = models_results['model_results']['feature_importance']
        
        # Format feature importance
        feature_text = ""
        for _, row in feature_importance.head(5).iterrows():
            feature_text += f"- **{row['feature']}**: {row['importance']:.3f}\n"
        
        report = f"""
# Groundwater Depletion Risk Assessment Report

## Executive Summary

**Report Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Total Districts Analyzed**: {total_districts}  
**Analysis Period**: {self.config.START_DATE} to {self.config.END_DATE}

This report presents a comprehensive assessment of groundwater depletion risk across {total_districts} districts, based on analysis of satellite gravity data, rainfall patterns, crop intensity, and population pressure.

## Risk Distribution

| Risk Level | Number of Districts | Percentage |
|------------|---------------------|------------|
| **Critical** | {risk_counts.get('Critical', 0)} | {risk_counts.get('Critical', 0)/total_districts*100:.1f}% |
| **Moderate** | {risk_counts.get('Moderate', 0)} | {risk_counts.get('Moderate', 0)/total_districts*100:.1f}% |
| **Low** | {risk_counts.get('Low', 0)} | {risk_counts.get('Low', 0)/total_districts*100:.1f}% |

## Key Findings

### Model Performance
- **R² Score**: {model_perf['r2']:.3f}
- **Root Mean Square Error (RMSE)**: {model_perf['rmse']:.3f}

### Most Important Risk Factors
{feature_text}

## Recommendations

### 🚨 Critical Risk Districts
- Implement immediate water conservation measures
- Restrict new groundwater extraction permits
- Promote water-efficient irrigation technologies
- Develop alternative water sources

### ⚠️ Moderate Risk Districts
- Monitor groundwater trends regularly
- Develop contingency plans for drought periods
- Promote sustainable agricultural practices
- Invest in water storage infrastructure

### ✅ Low Risk Districts
- Maintain current water management practices
- Continue monitoring and data collection
- Plan for long-term water security
- Share best practices with other districts

## Methodology

### Data Sources
1. **GRACE/GRACE-FO**: NASA Gravity Recovery and Climate Experiment satellite data
2. **CHIRPS**: Climate Hazards Group InfraRed Precipitation with Station data
3. **Agricultural Statistics**: Crop intensity and irrigation data
4. **Population Data**: Census and demographic surveys

### Analytical Approach
- **Spatial Analysis**: Aggregation of satellite data to district level
- **Time Series Modeling**: Random Forest regression for water stress prediction
- **Risk Classification**: Composite scoring based on multiple risk factors
- **Validation**: Train-test split and cross-validation techniques

## Technical Details

### Risk Factors and Weights
- Water Stress: 30%
- Crop Stress Index: 25%
- Rainfall Variability: 20%
- Depletion Acceleration: 15%
- Groundwater Irrigation Ratio: 10%

### Model Specifications
- Algorithm: Random Forest Regressor
- Number of Estimators: {self.config.N_ESTIMATORS}
- Test Size: {self.config.TEST_SIZE*100}%
- Random State: {self.config.RANDOM_STATE}

## Limitations

1. **Data Resolution**: Satellite data spatial resolution may not capture local variations
2. **Temporal Coverage**: Analysis limited to available satellite mission periods
3. **Model Assumptions**: Linear relationships in some risk factor combinations
4. **External Factors**: Climate change impacts and policy changes not fully incorporated

## Conclusion

This assessment provides a scientifically-grounded basis for water resource management and policy planning. The identified risk zones should be prioritized for intervention and monitoring to ensure sustainable groundwater management.

---

*This report was automatically generated by the Water Depletion Risk Modeling System.*
"""
        
        return report
    
    def _generate_pdf_report(self, processed_data, models_results):
        """Generate PDF version of the report"""
        try:
            from fpdf import FPDF
            
            risk_counts = models_results['risk_assessment']['risk_level'].value_counts()
            total_districts = len(models_results['risk_assessment'])
            
            pdf = FPDF()
            pdf.add_page()
            
            # Title
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, "Groundwater Depletion Risk Assessment Report", 0, 1, 'C')
            pdf.ln(10)
            
            # Summary
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, "Executive Summary", 0, 1)
            pdf.set_font("Arial", '', 10)
            pdf.multi_cell(0, 8, f"""
            This report presents groundwater depletion risk assessment across {total_districts} districts.
            
            Risk Distribution:
            - Critical Risk: {risk_counts.get('Critical', 0)} districts
            - Moderate Risk: {risk_counts.get('Moderate', 0)} districts  
            - Low Risk: {risk_counts.get('Low', 0)} districts
            
            Analysis Period: {self.config.START_DATE} to {self.config.END_DATE}
            Report Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            """)
            
            pdf_path = self.config.get_output_path('risk_assessment_report.pdf')
            pdf.output(pdf_path)
            return pdf_path
            
        except ImportError:
            print("   ⚠️  FPDF not installed - PDF report skipped")
            return None