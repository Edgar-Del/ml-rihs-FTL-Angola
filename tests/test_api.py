import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_root():
    """Testa o endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200
    assert "version" in response.json()


def test_health_check():
    """Testa o health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()


def test_model_info():
    """Testa informações do modelo"""
    response = client.get("/model/info")
    assert response.status_code == 200
    assert "model_loaded" in response.json()


def test_predict():
    """Testa a predição"""
    test_data = {
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
        "water_consumption_ratio": 0.7
    }
    
    response = client.post("/predict", json=test_data)
    
    # Pode retornar 200 (modelo carregado) ou 503 (modelo não carregado)
    assert response.status_code in [200, 503]
    
    if response.status_code == 200:
        data = response.json()
        assert "prediction" in data
        assert "probabilities" in data
        assert "prediction_label" in data


def test_invalid_predict():
    """Testa predição com dados inválidos"""
    invalid_data = {"invalid": "data"}
    response = client.post("/predict", json=invalid_data)
    assert response.status_code == 422  # Validation error