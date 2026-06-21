# Model Card: Prediksi Risiko Diabetes

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

## Operating Threshold
- **Threshold**: 0.4
- **Interpretation**:
  - >= threshold -> Risiko Diabetes: Tinggi
  - < threshold -> Risiko Diabetes: Rendah

*Catatan: Kategori risiko digunakan untuk tampilan pengguna. Nilai probabilitas tidak ditampilkan.*
