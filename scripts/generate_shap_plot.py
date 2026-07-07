import os
import joblib
import shap
import pandas as pd
import matplotlib.pyplot as plt

def generate_shap_summary_plot():
    print("Memuat dataset X_test...")
    # Load test dataset
    X_test = pd.read_csv("data/processed/X_test.csv")
    
    # Mengambil sampel untuk visualisasi agar proses berjalan lebih cepat dan plot tidak over-cluttered
    if len(X_test) > 5000:
        print("Data terlalu besar, mengambil sampel 5000 baris untuk efisiensi visualisasi...")
        X_test_sample = X_test.sample(5000, random_state=42)
    else:
        X_test_sample = X_test

    print("Memuat objek explainer dan encoder...")
    explainer = joblib.load("models/artifacts/explainer.pkl")
    encoder = joblib.load("models/artifacts/encoder.pkl")
    
    print("Melakukan encoding pada X_test_sample...")
    # 1. Encode gender
    X_test_sample['gender'] = X_test_sample['gender'].map(encoder['gender_map']).fillna(0)
    
    # 2. Encode smoking_history
    ohe = encoder['smoking_ohe']
    smoking_cols = encoder['smoking_cols']
    smoking_test = ohe.transform(X_test_sample[['smoking_history']])
    smoking_test_df = pd.DataFrame(smoking_test, columns=smoking_cols, index=X_test_sample.index)
    X_test_sample = pd.concat([X_test_sample.drop(columns=['smoking_history']), smoking_test_df], axis=1)
    
    print("Menghitung SHAP values...")
    # Menghitung SHAP values
    shap_values = explainer.shap_values(X_test_sample)

    # Ambil index 1 (kelas positif/diabetes) jika model adalah classifier biner yang mengembalikan list atau array 3D
    if isinstance(shap_values, list) and len(shap_values) == 2:
        shap_values_to_plot = shap_values[1]
    elif hasattr(shap_values, 'shape') and len(shap_values.shape) == 3:
        shap_values_to_plot = shap_values[:, :, 1]
    else:
        shap_values_to_plot = shap_values

    print("Membuat Summary Plot...")
    plt.figure(figsize=(10, 8))
    shap.summary_plot(shap_values_to_plot, X_test_sample, show=False)
    
    # Pastikan direktori reports ada
    os.makedirs("reports", exist_ok=True)
    
    plt.tight_layout()
    output_path = "reports/shap_summary_plot.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Selesai! Plot SHAP telah berhasil disimpan pada: {output_path}")

if __name__ == "__main__":
    generate_shap_summary_plot()
