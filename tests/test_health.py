def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "version" in response.json()


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert {"status", "model_loaded", "version"}.issubset(data.keys())

