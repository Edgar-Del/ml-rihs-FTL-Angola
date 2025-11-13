import os
from importlib import reload
from typing import Generator

import pytest
from fastapi.testclient import TestClient

# Configura API_KEY antes de carregar módulos da aplicação
os.environ.setdefault("API_KEY", "test-api-key")

# Recarrega settings para garantir que a API key de teste seja utilizada
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

