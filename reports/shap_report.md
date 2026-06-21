# SHAP Report (Safely Patched)
## Top 10 Features
- **hba1c_level**: Pada data ini fitur tersebut sering muncul pada prediksi risiko lebih tinggi.
- **blood_glucose_level**: Pada data ini fitur tersebut sering muncul pada prediksi risiko lebih tinggi.
- **age**: Pada data ini fitur tersebut sering muncul pada prediksi risiko lebih tinggi.
- **bmi**: Pada data ini fitur tersebut sering muncul pada prediksi risiko lebih tinggi.
- **smoking_history_No Info**: Pada data ini fitur tersebut sering muncul pada prediksi risiko lebih rendah.
- **gender**: Pada data ini fitur tersebut sering muncul pada prediksi risiko lebih rendah.
- **smoking_history_never**: Pada data ini fitur tersebut sering muncul pada prediksi risiko lebih tinggi.
- **smoking_history_former**: Pada data ini fitur tersebut sering muncul pada prediksi risiko lebih rendah.
- **smoking_history_current**: Pada data ini fitur tersebut sering muncul pada prediksi risiko lebih rendah.
- **smoking_history_not current**: Pada data ini fitur tersebut sering muncul pada prediksi risiko lebih rendah.

## Interpretation Limitation
SHAP bukan hubungan sebab akibat (causal). Nilai SHAP hanya merepresentasikan association dan contribution matematis dari setiap fitur terhadap output model berdasarkan observed relation (pola) dalam data latihan. Fitur ini tidak dapat digunakan untuk diagnosis medis pasti atau menyimpulkan penyebab biologis langsung dari diabetes.
