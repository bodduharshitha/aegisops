from fastapi.testclient import TestClient

from app.api.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ready():
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_status():
    response = client.get("/api/status")

    assert response.status_code == 200

    data = response.json()

    assert data["application"] == "AegisOps"
    assert data["status"] == "operational"


def test_metrics():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "aegisops_http_requests_total" in response.text