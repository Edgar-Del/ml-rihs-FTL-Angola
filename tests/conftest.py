import os
from importlib import reload
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

# Configura variáveis antes de carregar módulos da aplicação
os.environ.setdefault("API_KEY", "test-api-key")
# Força uso de caminhos absolutos para o registry e metadata durante os testes
PROJECT_ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MODEL_REGISTRY_PATH", str(PROJECT_ROOT / "models"))
os.environ.setdefault("METADATA_FILE", str(PROJECT_ROOT / "models" / "metadata.json"))

# Recarrega settings para garantir que as variáveis de teste sejam utilizadas
from app import config  # noqa: E402

reload(config)

from app.main import app  # noqa: E402  pylint: disable=wrong-import-position


@pytest.fixture(scope="session")
def api_key() -> str:
    return os.environ["API_KEY"]


@pytest.fixture(scope="session")
def client(api_key: str) -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        test_client.headers.update({"X-API-KEY": api_key})
        yield test_client

