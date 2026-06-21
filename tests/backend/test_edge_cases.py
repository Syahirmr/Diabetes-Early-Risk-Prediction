import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_extreme_values_rejected():
    payload = {
        "age": 150,  # too high
        "gender": "Male",
        "bmi": 800.0, # too high
        "hypertension": 0,
        "heart_disease": 0,
        "smoking_history": "never",
        "hba1c_level": 6.5,
        "blood_glucose_level": 120
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

def test_wrong_data_types_rejected():
    payload = {
        "age": 45,
        "gender": "Male",
        "bmi": 24.5,
        "hypertension": 0,
        "heart_disease": 0,
        "smoking_history": "never",
        "hba1c_level": "string_bukan_float", # salah tipe
        "blood_glucose_level": 120
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

def test_missing_fields_rejected():
    payload = {
        "age": 45,
        "gender": "Male"
        # missing other fields
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
