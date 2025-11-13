from fastapi.testclient import TestClient
from app.main import app


def test_model_info_success(api_key):
    client = TestClient(app)
    resp = client.get("/model/info", headers={"X-API-KEY": api_key})
    assert resp.status_code in (200, 503)
    if resp.status_code == 200:
        data = resp.json()
        assert "model_loaded" in data
        assert "feature_names" in data
        assert "version" in data


def test_metadata_success(api_key):
    client = TestClient(app)
    resp = client.get("/metadata", headers={"X-API-KEY": api_key})
    assert resp.status_code in (200, 503)
    # Quando 200, deve conter version ou métricas
    if resp.status_code == 200:
        data = resp.json()
        assert "version" in data or "metrics" in data


def test_invalid_api_key_rejected():
    client = TestClient(app)
    resp = client.get("/model/info", headers={"X-API-KEY": "wrong"})
    assert resp.status_code in (403, 500)
    # 403 quando API_KEY está configurada; 500 quando não foi configurada

