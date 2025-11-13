import json
from pathlib import Path

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression

from app.models import SustainabilityModel
from app.utils.feature_aliases import CANONICAL_FEATURES


def _create_dummy_model(artifact_path: Path) -> None:
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    X = np.random.rand(50, len(CANONICAL_FEATURES))
    y = np.random.randint(0, 2, size=50)
    clf = LogisticRegression(max_iter=100)
    clf.fit(X, y)
    joblib.dump(clf, artifact_path)


def _write_metadata(metadata_path: Path, version: str, artifact_path: Path) -> None:
    metadata = {
        "default_version": version,
        "models": {
            version: {
                "artifact_path": str(artifact_path),
                "trained_at": "2025-11-10T00:00:00Z",
                "metrics": {"accuracy": 0.75},
            }
        },
    }
    metadata_path.write_text(json.dumps(metadata), encoding="utf-8")


def test_load_model_with_metadata(tmp_path):
    registry_path = tmp_path / "registry"
    metadata_path = tmp_path / "metadata.json"
    artifact_path = registry_path / "v1" / "model.pkl"

    _create_dummy_model(artifact_path)
    _write_metadata(metadata_path, "v1", artifact_path)

    model = SustainabilityModel()
    assert model.load(
        model_path=str(artifact_path),
        metadata_path=str(metadata_path),
    )
    assert model.is_loaded()
    assert model.model_version == "v1"
    assert model.metadata["metrics"]["accuracy"] == 0.75


def test_predict_normalizes_features(tmp_path):
    registry_path = tmp_path / "registry"
    metadata_path = tmp_path / "metadata.json"
    artifact_path = registry_path / "v2" / "model.pkl"

    _create_dummy_model(artifact_path)
    _write_metadata(metadata_path, "v2", artifact_path)

    model = SustainabilityModel()
    assert model.load(
        model_path=str(artifact_path),
        metadata_path=str(metadata_path),
    )

    payload = {feature: float(idx) for idx, feature in enumerate(CANONICAL_FEATURES)}
    # injeta chave com acento para validar normalização
    payload["energia_renovável"] = payload.pop("energia_renovavel")

    result = model.predict(payload)
    assert "prediction" in result
    assert len(result["probabilities"]) > 0

