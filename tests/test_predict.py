from copy import deepcopy

import pytest


@pytest.fixture
def prediction_payload():
    return {
        "price_per_night_usd": 150.0,
        "rating": 4.2,
        "avaliação_clientes": 8.5,
        "distância_do_centro_km": 2.5,
        "energia_renovável": 75.0,
        "gestão_resíduos_índice": 0.8,
        "consumo_água_por_hóspede": 120.0,
        "carbon_footprint_score": 0.7,
        "reciclagem_score": 0.9,
        "energia_limpa_score": 0.8,
        "water_usage_index": 0.6,
        "sustainability_index": 0.85,
        "eco_impact_index": 0.75,
        "eco_value_ratio": 1.2,
        "sentimento_score": 0.8,
        "eco_keyword_count": 5,
        "região_encoded": 2,
        "possui_selo_sustentável_encoded": 1,
        "sentimento_sustentabilidade_encoded": 1,
        "price_sust_ratio": 1.5,
        "eco_value_score": 0.8,
        "total_sust_score": 0.85,
        "price_category": 2,
        "water_consumption_ratio": 0.7,
    }


def test_predict_success(client, prediction_payload):
    response = client.post("/predict", json=prediction_payload)
    assert response.status_code == 200
    body = response.json()
    assert body["prediction_label"]
    assert isinstance(body["probabilities"], list)
    assert "model_version" in body


def test_predict_requires_api_key(client, prediction_payload):
    # Cria um cliente novo sem header padrão para simular ausência do X-API-KEY
    from app.main import app
    from fastapi.testclient import TestClient

    client_no_key = TestClient(app)
    response = client_no_key.post("/predict", json=prediction_payload)
    assert response.status_code == 422  # header obrigatório ausente


def test_predict_missing_feature_returns_422(client, prediction_payload):
    invalid_payload = deepcopy(prediction_payload)
    invalid_payload.pop("eco_value_score")
    response = client.post("/predict", json=invalid_payload)
    assert response.status_code == 422


def test_predict_invalid_type_returns_422(client, prediction_payload):
    invalid_payload = deepcopy(prediction_payload)
    invalid_payload["rating"] = "muito bom"
    response = client.post("/predict", json=invalid_payload)
    assert response.status_code == 422

