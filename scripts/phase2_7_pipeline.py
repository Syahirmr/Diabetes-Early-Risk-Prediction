import json
import pandas as pd
import joblib

def main():
    # 1. Update Metadata
    with open('models/artifacts/metadata.json', 'r') as f:
        metadata = json.load(f)
        
    X_test_raw = pd.read_csv('data/processed/X_test.csv')
    raw_columns = X_test_raw.columns.tolist()
    
    metadata['schema_version'] = "1.0"
    metadata['feature_order'] = raw_columns
    
    with open('models/artifacts/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=4)
        
    # 2. Update Model Card
    with open('reports/model_card.md', 'r') as f:
        model_card = f.read()
        
    threshold = metadata['decision_threshold']
    
    if "## Operating Threshold" not in model_card:
        operating_threshold_section = f"""
## Operating Threshold
- **Threshold**: {threshold}
- **Interpretation**:
  - >= threshold -> Risiko Diabetes: Tinggi
  - < threshold -> Risiko Diabetes: Rendah

*Catatan: Kategori risiko digunakan untuk tampilan pengguna. Nilai probabilitas tidak ditampilkan.*
"""
        model_card += operating_threshold_section
        
        with open('reports/model_card.md', 'w') as f:
            f.write(model_card)

    # 3. Validation
    try:
        model = joblib.load('models/artifacts/model.pkl')
        encoder = joblib.load('models/artifacts/encoder.pkl')
        with open('models/artifacts/metadata.json', 'r') as f:
            final_metadata = json.load(f)
            
        feature_order = final_metadata['feature_order']
        
        # Test sample with columns out of order
        sample = X_test_raw.iloc[[0]].copy()
        shuffled_sample = sample[feature_order[::-1]] # Reverse the order
        
        # Reorder sample
        reordered_sample = shuffled_sample[feature_order]
        
        # Apply encoding
        reordered_sample['gender'] = reordered_sample['gender'].map(encoder['gender_map']).fillna(0)
        smoking_test = encoder['smoking_ohe'].transform(reordered_sample[['smoking_history']])
        smoking_test_df = pd.DataFrame(smoking_test, columns=encoder['smoking_cols'], index=reordered_sample.index)
        reordered_sample = pd.concat([reordered_sample.drop(columns=['smoking_history']), smoking_test_df], axis=1)
        
        # Predict
        prob = model.predict_proba(reordered_sample)[:, 1][0]
        
        status = "Success"
        feature_alignment_status = "PASS"
    except Exception as e:
        status = f"Failed: {str(e)}"
        feature_alignment_status = "FAIL"
        
    print(f"Feature alignment: {feature_alignment_status}")
    print(f"Validation Status: {status}")

if __name__ == '__main__':
    main()
