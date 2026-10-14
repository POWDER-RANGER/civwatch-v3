"""Contract tests for the predecessor/reference service."""
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_discloses_reference_role_and_mode():
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "civwatch-v3"
    assert body["role"] == "reference_only"
    assert body["observation_mode"] in {"device_metadata", "synthetic_demo"}


def test_capabilities_do_not_overstate_capture():
    response = client.get("/api/capabilities")
    assert response.status_code == 200
    body = response.json()
    assert body["role"] == "predecessor_reference_only"
    domains = {domain["id"]: domain for domain in body["domains"]}
    assert domains["d2d"]["measurement_class"] == "synthetic"
    assert any("Synthetic samples are not real-world detections" in item for item in body["limitations"])
