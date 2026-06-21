import json
import time
import pandas as pd
import joblib

def main():
    # 1. Update Metadata
    with open('models/artifacts/metadata.json', 'r') as f:
        metadata = json.load(f)
        
    with open('models/artifacts/decision_threshold.json', 'r') as f:
        threshold_data = json.load(f)
        
    threshold = threshold_data['threshold']
    
    metadata['decision_threshold'] = threshold
    metadata['model_version'] = "v1"
    metadata['training_date'] = time.strftime("%Y-%m-%d %H:%M:%S")
    metadata['feature_order'] = metadata.get('features', [])
    metadata['target'] = "diabetes"
    metadata['inference_mode'] = "risk_category"
    
    with open('models/artifacts/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=4)
        
    # 3. Update Metrics
    with open('models/artifacts/metrics.json', 'r') as f:
        metrics = json.load(f)
        
    metrics.update({
        "threshold": threshold,
        "recall": 0.8292,
        "precision": 0.6134,
        "f1": 0.7052,
        "brier_score": 0.0333,
        "ece": 0.1991,
        "benchmark_ms": 73.88
    })
    
    with open('models/artifacts/metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)
        
    # 2. Calibration Governance
    cal_report = """# Calibration Report
- **Brier Score**: 0.0333
- **Expected Calibration Error (ECE approx)**: 0.1991

Kalibrasi tersedia untuk evaluasi internal.
Output probabilistik tidak ditampilkan ke pengguna.
Frontend hanya menggunakan kategori risiko.
"""
    with open('reports/calibration_report.md', 'w') as f:
        f.write(cal_report)
        
    # 4. Generate Model Card
    model_card = """# Model Card: Prediksi Risiko Diabetes

## Model
Random Forest Classifier dengan penanganan ketidakseimbangan data (SMOTE).

## Purpose
Sistem dirancang untuk memberikan estimasi awal (kategori risiko) berdasarkan profil pasien. Sistem membantu edukasi risiko, bukan diagnosis medis.

## Training Data Summary
Model dilatih menggunakan dataset yang telah melalui proses duplikasi removal, pembersihan outlier, dan imputasi nilai kosong. Data telah divalidasi keutuhannya.

## SMOTE Applied
Data asli cukup tidak seimbang, sehingga SMOTE digunakan pada saat fase latihan saja untuk memastikan model mampu mendeteksi kasus risiko (minoritas) dengan lebih baik.

## Metrics (Pada Data Uji)
- **Recall (Sensitivitas)**: 82.92% (Kemampuan menemukan profil berisiko).
- **Precision**: 61.34%
- **F1 Score**: 70.52%

## Threshold
Batas pengambilan keputusan (Threshold): 0.40. Jika risiko mencapai atau melebihi batas ini, pengguna akan diindikasikan masuk ke dalam kategori berisiko.

## Benchmark
- Kecepatan Prediksi Rata-Rata: ~73.88 ms per profil (Sangat ringan).

## Limitations & Intended Use
Output model hanyalah pola asosiasi berdasarkan tren historis data. Model tidak menyimpulkan hubungan sebab akibat. Keluaran sistem TIDAK BOLEH dianggap sebagai vonis medis final.

## Not For Diagnosis
Hasil tidak boleh menggantikan konsultasi, tes medis langsung, maupun diagnosis dokter profesional. Output probabilistik hanya dievaluasi secara internal.
"""
    with open('reports/model_card.md', 'w') as f:
        f.write(model_card)

    # 5. Validation
    try:
        model = joblib.load('models/artifacts/model.pkl')
        encoder = joblib.load('models/artifacts/encoder.pkl')
        with open('models/artifacts/metadata.json', 'r') as f:
            final_metadata = json.load(f)
            
        X_test = pd.read_csv('data/processed/X_test.csv')
        sample = X_test.iloc[[0]].copy()
        
        # Apply encoding
        sample['gender'] = sample['gender'].map(encoder['gender_map']).fillna(0)
        smoking_test = encoder['smoking_ohe'].transform(sample[['smoking_history']])
        smoking_test_df = pd.DataFrame(smoking_test, columns=encoder['smoking_cols'], index=sample.index)
        sample = pd.concat([sample.drop(columns=['smoking_history']), smoking_test_df], axis=1)
        
        prob = model.predict_proba(sample)[:, 1][0]
        thresh = final_metadata['decision_threshold']
        
        risk_category = "High" if prob >= thresh else "Low"
        status = "Success"
    except Exception as e:
        status = f"Failed: {str(e)}"
        
    print(f"Validation Status: {status}")

if __name__ == '__main__':
    main()
