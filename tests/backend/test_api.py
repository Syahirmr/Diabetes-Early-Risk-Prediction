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

def test_startup_and_health():
    with TestClient(app) as client:
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

def test_metadata():
    with TestClient(app) as client:
        response = client.get("/api/v1/metadata")
        assert response.status_code == 200
        data = response.json()
        assert "model_name" in data
        assert "version" in data
        assert "target" in data
        assert "inference_mode" in data

def test_predict_success():
    with TestClient(app) as client:
        response = client.post("/api/v1/predict", json=valid_payload)
        assert response.status_code == 200
        data = response.json()
        assert "risk_level" in data
        assert "summary" in data
        assert "top_factors" in data
        assert "recommendation" in data
        assert "disclaimer" in data

def test_predict_validation_error():
    with TestClient(app) as client:
        invalid_payload = valid_payload.copy()
        invalid_payload["age"] = -10 # invalid age
        response = client.post("/api/v1/predict", json=invalid_payload)
        assert response.status_code == 422
        assert response.json()["error"]["code"] == "VALIDATION_ERROR"

def test_explain_success():
    with TestClient(app) as client:
        response = client.post("/api/v1/explain", json=valid_payload)
        assert response.status_code == 200
        data = response.json()
        assert "top_factors" in data

def test_cors():
    with TestClient(app) as client:
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
        }
        response = client.options("/api/v1/predict", headers=headers)
        # Assuming ALLOWED_ORIGINS contains http://localhost:3000
        assert response.status_code == 200
