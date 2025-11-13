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
os.environ.setdefault("MODEL_REGISTRY_PATH", str(PROJECT_ROOT / "models" / "latest" / "model.pkl"))
os.environ.setdefault("METADATA_FILE", str(PROJECT_ROOT / "models" / "metadata.json"))

# Recarrega settings para garantir que as variáveis de teste sejam utilizadas
from app import config  # noqa: E402

reload(config)

# Importa o módulo main mas ainda não cria a app
import app.main as app_main  # noqa: E402  pylint: disable=wrong-import-position

# Tenta carregar o modelo real ou rihs_model.pkl ANTES de criar a app
# (para evitar que o lifespan tente carregar e falhe)
model_path = os.environ.get("MODEL_REGISTRY_PATH", str(PROJECT_ROOT / "models" / "latest" / "model.pkl"))
metadata_path = os.environ.get("METADATA_FILE", str(PROJECT_ROOT / "models" / "metadata.json"))

# Tenta carregar o modelo principal primeiro
if Path(model_path).exists():
    try:
        app_main.model.load(model_path=model_path, metadata_path=metadata_path)
    except Exception:
        # Se falhar, tenta carregar rihs_model.pkl no mesmo diretório
        rihs_model_path = Path(model_path).parent / "rihs_model.pkl"
        if rihs_model_path.exists():
            try:
                app_main.model.load(model_path=str(rihs_model_path), metadata_path=metadata_path)
            except Exception:
                pass  # Se ambos falharem, o lifespan tentará novamente

# Agora importa a app (o lifespan verá se o modelo já está carregado ou tentará carregar)
from app.main import app  # noqa: E402  pylint: disable=wrong-import-position


@pytest.fixture(scope="session")
def api_key() -> str:
    return os.environ["API_KEY"]


@pytest.fixture(scope="session")
def client(api_key: str) -> Generator[TestClient, None, None]:
    """Fixture que garante que o modelo esteja carregado antes dos testes."""
    # Se o modelo ainda não estiver carregado, tenta carregar rihs_model.pkl
    if not app_main.model.is_loaded():
        model_path = os.environ.get("MODEL_REGISTRY_PATH", str(PROJECT_ROOT / "models" / "latest" / "model.pkl"))
        metadata_path = os.environ.get("METADATA_FILE", str(PROJECT_ROOT / "models" / "metadata.json"))
        
        # Tenta carregar rihs_model.pkl no mesmo diretório
        rihs_model_path = Path(model_path).parent / "rihs_model.pkl"
        if rihs_model_path.exists():
            try:
                app_main.model.load(model_path=str(rihs_model_path), metadata_path=metadata_path)
            except Exception:
                pass  # Se falhar, continua sem modelo (os testes irão falhar apropriadamente)
    
    # Garante que o modelo está carregado antes de retornar o cliente
    assert app_main.model.is_loaded(), "Modelo deve estar carregado antes dos testes (tente rihs_model.pkl)"

    with TestClient(app) as test_client:
        yield test_client

