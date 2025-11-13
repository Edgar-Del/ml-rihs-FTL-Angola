from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict

import numpy as np

from app.utils.feature_aliases import CANONICAL_FEATURES
from app.utils.validation import (
    ensure_only_known_features,
    normalize_features,
    validate_feature_payload,
)
from ml.model_loader import load_metadata, load_model

logger = logging.getLogger(__name__)


class SustainabilityModel:
    """Classe para gerenciar o ciclo de vida do modelo de sustentabilidade."""

    def __init__(self) -> None:
        self.model = None
        self.feature_names = CANONICAL_FEATURES
        self.class_labels = {
            0: "Muito Baixa Sustentabilidade",
            1: "Baixa Sustentabilidade",
            2: "Média Sustentabilidade",
            3: "Alta Sustentabilidade",
            4: "Muito Alta Sustentabilidade",
        }
        self.metadata: Dict[str, Any] = {}
        self.model_version: str = "desconhecido"
        self.loaded_path: Path | None = None

    def load(self, model_path: str, metadata_path: str) -> bool:
        try:
            self.model, resolved_path = load_model(model_path)
            self.loaded_path = resolved_path
            metadata = load_metadata(metadata_path)
            selected_metadata = metadata
            version = metadata.get("version", "unknown")

            models_info = metadata.get("models")
            if isinstance(models_info, dict):
                for candidate_version, info in models_info.items():
                    artifact = info.get("artifact_path")
                    if artifact and Path(artifact).resolve() == resolved_path.resolve():
                        selected_metadata = {**info, "version": candidate_version}
                        version = candidate_version
                        break
                else:
                    default_version = metadata.get("default_version")
                    if default_version and default_version in models_info:
                        info = models_info[default_version]
                        selected_metadata = {**info, "version": default_version}
                        version = default_version

            self.metadata = selected_metadata
            self.model_version = version
            return True
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Erro ao carregar modelo principal: %s", exc)
            self.model = None
            return False

    def predict(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Realiza uma predição a partir de um payload de features."""
        if not self.is_loaded():
            raise RuntimeError("Modelo não está carregado.")

        normalized_features = normalize_features(payload)
        ensure_only_known_features(normalized_features)
        validate_feature_payload(normalized_features)

        feature_vector = np.array(
            [[normalized_features[feature] for feature in self.feature_names]]
        )

        prediction = int(self.model.predict(feature_vector)[0])
        probabilities = self.model.predict_proba(feature_vector)[0].tolist()
        prediction_label = self.class_labels.get(prediction, "Desconhecido")

        return {
            "prediction": prediction,
            "probabilities": probabilities,
            "prediction_label": prediction_label,
            "model_version": self.model_version,
        }

    def is_loaded(self) -> bool:
        """Verifica se o modelo está carregado."""
        return self.model is not None