from core.settings import Settings


def test_settings_valid_load(monkeypatch, tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "API_KEY=abc123\n"
        "MODEL_REGISTRY_PATH=./models/latest/model.pkl\n"
        "METADATA_FILE=./models/metadata.json\n"
        "CORS_ORIGINS=https://exemplo.com,http://localhost\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("API_KEY", "abc123")
    settings = Settings(_env_file=env_file)
    assert isinstance(settings.CORS_ORIGINS, list)
    assert settings.CORS_ORIGINS == ["https://exemplo.com", "http://localhost"]
    assert settings.API_KEY == "abc123"


def test_settings_invalid_cors(monkeypatch, tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        'API_KEY=abc123\nCORS_ORIGINS=["invalid_format"]\nMODEL_REGISTRY_PATH=./models/latest/model.pkl\nMETADATA_FILE=./models/metadata.json\n',
        encoding="utf-8",
    )
    try:
        Settings(_env_file=env_file)
        assert False, "Expected ValidationError for invalid CORS_ORIGINS"
    except Exception as exc:
        assert "CORS_ORIGINS" in str(exc)

