from fastapi.testclient import TestClient
from backend.main import app
from backend.utils.config import settings

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "env" in data
    assert data["env"] == settings.APP_ENV
    assert "version" in data
