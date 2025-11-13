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
os.environ.setdefault("MODEL_REGISTRY_PATH", str(PROJECT_ROOT / "models" / "latest" / "sustainability_classification_pipeline.pkl"))
os.environ.setdefault("METADATA_FILE", str(PROJECT_ROOT / "models" / "metadata.json"))

# Recarrega settings para garantir que as variáveis de teste sejam utilizadas
from app import config  # noqa: E402

reload(config)

# Importa o módulo main mas ainda não cria a app
import app.main as app_main  # noqa: E402  pylint: disable=wrong-import-position

# Tenta carregar o modelo real ou sustainability_classification_pipeline.pkl ANTES de criar a app
# (para evitar que o lifespan tente carregar e falhe)
model_path = os.environ.get("MODEL_REGISTRY_PATH", str(PROJECT_ROOT / "models" / "latest" / "sustainability_classification_pipeline.pkl"))
metadata_path = os.environ.get("METADATA_FILE", str(PROJECT_ROOT / "models" / "metadata.json"))

# Tenta carregar o modelo principal primeiro
if Path(model_path).exists():
    try:
        app_main.model.load(model_path=model_path, metadata_path=metadata_path)
    except Exception:
        # Se falhar, tenta carregar sustainability_classification_pipeline.pkl no mesmo diretório
        pipeline_path = Path(model_path).parent / "sustainability_classification_pipeline.pkl"
        if pipeline_path.exists():
            try:
                app_main.model.load(model_path=str(pipeline_path), metadata_path=metadata_path)
            except Exception:
                # Se falhar, tenta carregar rihs_model.pkl no mesmo diretório
                rihs_model_path = Path(model_path).parent / "rihs_model.pkl"
                if rihs_model_path.exists():
                    try:
                        app_main.model.load(model_path=str(rihs_model_path), metadata_path=metadata_path)
                    except Exception:
                        pass  # Se todos falharem, o lifespan tentará novamente

# Agora importa a app (o lifespan verá se o modelo já está carregado ou tentará carregar)
from app.main import app  # noqa: E402  pylint: disable=wrong-import-position


@pytest.fixture(scope="session")
def api_key() -> str:
    return os.environ["API_KEY"]


@pytest.fixture(scope="session")
def client(api_key: str) -> Generator[TestClient, None, None]:
    """Fixture que garante que o modelo esteja carregado antes dos testes."""
    # Se o modelo ainda não estiver carregado, tenta carregar sustainability_classification_pipeline.pkl ou rihs_model.pkl
    # Se todos falharem ou não forem válidos, injecta um modelo dummy
    if not app_main.model.is_loaded():
        model_path = os.environ.get("MODEL_REGISTRY_PATH", str(PROJECT_ROOT / "models" / "latest" / "sustainability_classification_pipeline.pkl"))
        metadata_path = os.environ.get("METADATA_FILE", str(PROJECT_ROOT / "models" / "metadata.json"))
        
        # Tenta carregar sustainability_classification_pipeline.pkl no mesmo diretório
        pipeline_path = Path(model_path).parent / "sustainability_classification_pipeline.pkl"
        if pipeline_path.exists():
            try:
                app_main.model.load(model_path=str(pipeline_path), metadata_path=metadata_path)
            except Exception:
                pass  # Se falhar, tenta rihs_model.pkl abaixo
        
        # Se ainda não carregou, tenta carregar rihs_model.pkl no mesmo diretório
        if not app_main.model.is_loaded():
            rihs_model_path = Path(model_path).parent / "rihs_model.pkl"
            if rihs_model_path.exists():
                try:
                    app_main.model.load(model_path=str(rihs_model_path), metadata_path=metadata_path)
                except Exception:
                    pass  # Se falhar, injecta dummy abaixo
        
        # Se ainda não carregou (ou o modelo carregado não é válido), injecta dummy
        if not app_main.model.is_loaded():
            import numpy as np
            from sklearn.linear_model import LogisticRegression
            from app.utils.feature_aliases import CANONICAL_FEATURES

            X = np.random.rand(30, len(CANONICAL_FEATURES))
            y = np.random.randint(0, 5, size=30)  # 5 classes para compatibilidade
            clf = LogisticRegression(max_iter=100, multi_class="multinomial", solver="lbfgs")
            clf.fit(X, y)
            
            app_main.model.model = clf
            app_main.model.model_version = "test-dummy"
            app_main.model.metadata = {"version": "test-dummy", "metrics": {"accuracy": 0.5}}
            app_main.model.loaded_path = Path(model_path)
    
    # Garante que o modelo está carregado antes de retornar o cliente
    assert app_main.model.is_loaded(), "Modelo deve estar carregado antes dos testes"

    with TestClient(app) as test_client:
        yield test_client

