from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import joblib
import numpy as np

from app.utils.feature_aliases import CANONICAL_FEATURES
from app.utils.validation import (
    ensure_only_known_features,
    normalize_features,
    validate_feature_payload,
)

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

    def load_model(
        self,
        registry_path: str,
        version: str,
        fallback_version: str,
        metadata_file: str,
    ) -> bool:
        """Carrega o modelo com suporte a metadata e fallback."""
        try:
            metadata = self._load_metadata(Path(metadata_file))
            target_path, resolved_version = self._resolve_artifact(
                metadata, Path(registry_path), version, fallback_version
            )

            if target_path is None or not target_path.exists():
                logger.error("Nenhum artefacto de modelo disponível para carregar.")
                return False

            logger.info("Carregando modelo de %s (versão %s)", target_path, resolved_version)
            self.model = joblib.load(target_path)
            self.metadata = metadata.get("models", {}).get(resolved_version, {})
            self.metadata["version"] = resolved_version
            self.model_version = resolved_version
            logger.info("Modelo carregado com sucesso!")
            return True
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Erro ao carregar modelo: %s", exc)
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

    @staticmethod
    def _load_metadata(metadata_path: Path) -> Dict[str, Any]:
        if metadata_path.exists():
            with metadata_path.open(encoding="utf-8") as metadata_file:
                return json.load(metadata_file)
        logger.warning("Arquivo de metadata não encontrado em %s", metadata_path)
        return {}

    @staticmethod
    def _resolve_artifact(
        metadata: Dict[str, Any],
        registry_path: Path,
        requested_version: str,
        fallback_version: str,
    ) -> Tuple[Optional[Path], str]:
        models_metadata: Dict[str, Dict[str, Any]] = metadata.get("models", {})
        default_version = metadata.get("default_version")

        candidate_order = [
            requested_version,
            default_version,
            fallback_version,
        ]

        for version in candidate_order:
            if not version:
                continue

            model_info = models_metadata.get(version, {})
            artifact_path = model_info.get("artifact_path")

            if artifact_path:
                path = Path(artifact_path)
            else:
                path = registry_path / version / "model.pkl"

            if path.exists():
                return path, version

        # fallback final: procurar primeiro artefato existente
        for version, model_info in models_metadata.items():
            artifact_path = model_info.get("artifact_path")
            path = Path(artifact_path) if artifact_path else registry_path / version / "model.pkl"
            if path.exists():
                return path, version

        # compatibilidade retroativa com caminho antigo
        legacy_path = registry_path / "hotel_sustainability_classifier.pkl"
        if legacy_path.exists():
            return legacy_path, "legacy"

        return None, "desconhecido"