from fastapi.testclient import TestClient
from app.main import app


def test_model_info_success(client, api_key):
    """Testa endpoint /model/info com modelo carregado."""
    resp = client.get("/model/info", headers={"X-API-KEY": api_key})
    assert resp.status_code == 200
    data = resp.json()
    assert data["model_loaded"] is True
    assert "feature_names" in data
    assert "version" in data


def test_metadata_success(client, api_key):
    """Testa endpoint /metadata com modelo carregado."""
    resp = client.get("/metadata", headers={"X-API-KEY": api_key})
    assert resp.status_code == 200
    data = resp.json()
    assert "version" in data


def test_invalid_api_key_rejected(client):
    """Testa rejeição de API key inválida."""
    resp = client.get("/model/info", headers={"X-API-KEY": "wrong"})
    assert resp.status_code == 403

