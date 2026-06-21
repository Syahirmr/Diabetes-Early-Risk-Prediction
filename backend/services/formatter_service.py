from backend.schemas.response import PredictResponse, Factor, ExplainResponse

def format_prediction_response(prob: float, threshold: float, shap_vals: list, features: list) -> PredictResponse:
    is_high_risk = prob >= threshold
    
    risk_level = "Tinggi" if is_high_risk else "Rendah"
    summary = "Berdasarkan data yang dimasukkan, terdapat indikasi risiko yang perlu diperhatikan." if is_high_risk else "Berdasarkan data yang dimasukkan, profil pasien saat ini tidak menunjukkan indikasi risiko signifikan."
    recommendation = "Pertimbangkan pemeriksaan lanjutan. Konsultasikan dengan tenaga medis." if is_high_risk else "Pertahankan pola hidup sehat dan lakukan pemeriksaan rutin berkala."
    disclaimer = "Hasil prediksi ini bukan diagnosis medis. Sistem hanya memberikan estimasi risiko berdasarkan pola data."
    
    top_factors = []
    shap_pairs = list(zip(features, shap_vals))
    shap_pairs.sort(key=lambda x: abs(x[1]), reverse=True)
    
    for feat, sval in shap_pairs[:5]:
        direction = "increase" if sval > 0 else "decrease"
        impact_desc = "Memberi pengaruh terhadap peningkatan risiko." if sval > 0 else "Memberi pengaruh terhadap penurunan risiko."
        top_factors.append(Factor(feature=feat, direction=direction, impact=impact_desc))
        
    return PredictResponse(
        risk_level=risk_level,
        summary=summary,
        top_factors=top_factors,
        recommendation=recommendation,
        disclaimer=disclaimer
    )

def format_explain_response(shap_vals: list, features: list) -> ExplainResponse:
    shap_pairs = list(zip(features, shap_vals))
    shap_pairs.sort(key=lambda x: abs(x[1]), reverse=True)
    top_factors = []
    for feat, sval in shap_pairs[:10]:
        direction = "increase" if sval > 0 else "decrease"
        impact_desc = "Memberi pengaruh terhadap peningkatan risiko." if sval > 0 else "Memberi pengaruh terhadap penurunan risiko."
        top_factors.append(Factor(feature=feat, direction=direction, impact=impact_desc))
    return ExplainResponse(top_factors=top_factors)
