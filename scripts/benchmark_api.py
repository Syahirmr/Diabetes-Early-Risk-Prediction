import time
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

payload = {
    "age": 45,
    "gender": "Male",
    "bmi": 31.2,
    "hba1c_level": 7.0,
    "blood_glucose_level": 180,
    "hypertension": 1,
    "heart_disease": 0,
    "smoking_history": "former"
}

times_predict = []
times_explain = []

with TestClient(app) as client:
    for _ in range(50):
        t0 = time.time()
        client.post("/api/v1/predict", json=payload)
        times_predict.append(time.time() - t0)

    for _ in range(50):
        t0 = time.time()
        client.post("/api/v1/explain", json=payload)
        times_explain.append(time.time() - t0)

avg_predict = sum(times_predict) / 50 * 1000 # ms
avg_explain = sum(times_explain) / 50 * 1000 # ms

with open('reports/explain_benchmark.md', 'w') as f:
    f.write("# Explain Benchmark\n")
    f.write(f"- Avg Predict Latency: {avg_predict:.2f} ms\n")
    f.write(f"- Avg Explain Latency: {avg_explain:.2f} ms\n")
    f.write(f"- Ratio Explain/Predict: {avg_explain/avg_predict:.2f}x\n")
    f.write(f"- Target Explain <= 2x predict: {'PASS' if avg_explain <= 2 * avg_predict else 'FAIL'}\n")
