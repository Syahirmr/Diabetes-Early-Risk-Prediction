from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

valid_payload = {
    "age": 45,
    "gender": "Male",
    "bmi": 31.2,
    "hba1c_level": 7.0,
    "blood_glucose_level": 180,
    "hypertension": 1,
    "heart_disease": 0,
    "smoking_history": "former"
}

def test_feature_alignment():
    with TestClient(app) as client:
        # Input A: normal payload
        response_a = client.post("/api/v1/predict", json=valid_payload)
        assert response_a.status_code == 200
        res_a = response_a.json()
        
        # Input B: shuffled payload
        shuffled_payload = {
            "smoking_history": "former",
            "hba1c_level": 7.0,
            "age": 45,
            "hypertension": 1,
            "gender": "Male",
            "bmi": 31.2,
            "heart_disease": 0,
            "blood_glucose_level": 180
        }
        response_b = client.post("/api/v1/predict", json=shuffled_payload)
        assert response_b.status_code == 200
        res_b = response_b.json()
        
        # Assert identical
        assert res_a["risk_level"] == res_b["risk_level"]
        assert res_a["summary"] == res_b["summary"]
        
        # Explain endpoint
        response_exp_a = client.post("/api/v1/explain", json=valid_payload)
        response_exp_b = client.post("/api/v1/explain", json=shuffled_payload)
        
        assert response_exp_a.json()["top_factors"] == response_exp_b.json()["top_factors"]
