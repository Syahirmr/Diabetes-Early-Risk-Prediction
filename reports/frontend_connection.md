# Frontend Early Connection Report
## Output
```text
Pinging health endpoint...
Health Status: 200 { status: 'ok', env: 'development', version: 'v1' }

Pinging predict endpoint...
Predict Status: 200 {
  risk_level: 'Rendah',
  summary: 'Berdasarkan data yang dimasukkan, profil pasien saat ini tidak menunjukkan indikasi risiko signifikan.',
  top_factors: [
    {
      feature: 'bmi',
      direction: 'decrease',
      impact: 'Memberi pengaruh terhadap penurunan risiko.'
    },
    {
      feature: 'hba1c_level',
      direction: 'decrease',
      impact: 'Memberi pengaruh terhadap penurunan risiko.'
    },
    {
      feature: 'blood_glucose_level',
      direction: 'decrease',
      impact: 'Memberi pengaruh terhadap penurunan risiko.'
    },
    {
      feature: 'age',
      direction: 'increase',
      impact: 'Memberi pengaruh terhadap peningkatan risiko.'
    },
    {
      feature: 'smoking_history_No Info',
      direction: 'increase',
      impact: 'Memberi pengaruh terhadap peningkatan risiko.'
    }
  ],
  recommendation: 'Pertahankan pola hidup sehat dan lakukan pemeriksaan rutin berkala.',
  disclaimer: 'Hasil prediksi ini bukan diagnosis medis. Sistem hanya memberikan estimasi risiko berdasarkan pola data.'
}

Pinging predict endpoint (422 test)...
Error 422 Status: 422 {
  error: {
    code: 'VALIDATION_ERROR',
    message: 'Input tidak valid sesuai kontrak data.'
  }
}

Connection OK.

```

## Status
PASS
