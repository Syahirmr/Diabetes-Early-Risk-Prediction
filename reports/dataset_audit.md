# Dataset Audit Report
- **Shape**: (100000, 17)
- **Column Count**: 17
- **Target Distribution**: {0: 91500, 1: 8500}
- **Duplicates**: 14

## Missing Values
- year: 0
- gender: 0
- age: 0
- location: 0
- race:AfricanAmerican: 0
- race:Asian: 0
- race:Caucasian: 0
- race:Hispanic: 0
- race:Other: 0
- hypertension: 0
- heart_disease: 0
- smoking_history: 0
- bmi: 0
- hbA1c_level: 0
- blood_glucose_level: 0
- diabetes: 0
- clinical_notes: 0

## Data Types
- year: int64
- gender: str
- age: float64
- location: str
- race:AfricanAmerican: int64
- race:Asian: int64
- race:Caucasian: int64
- race:Hispanic: int64
- race:Other: int64
- hypertension: int64
- heart_disease: int64
- smoking_history: str
- bmi: float64
- hbA1c_level: float64
- blood_glucose_level: int64
- diabetes: int64
- clinical_notes: str

## Outlier Indication (IQR Method)
- year: 20255 potential outliers
- age: 0 potential outliers
- race:AfricanAmerican: 20223 potential outliers
- race:Asian: 20015 potential outliers
- race:Caucasian: 19876 potential outliers
- race:Hispanic: 19888 potential outliers
- race:Other: 19998 potential outliers
- hypertension: 7485 potential outliers
- heart_disease: 3942 potential outliers
- bmi: 7086 potential outliers
- hbA1c_level: 1315 potential outliers
- blood_glucose_level: 2038 potential outliers
- diabetes: 8500 potential outliers
