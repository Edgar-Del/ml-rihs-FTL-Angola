from __future__ import annotations

from typing import Any, Dict

from .feature_aliases import CANONICAL_FEATURES, FEATURE_ALIASES, resolve_feature_name

REQUIRED_FEATURES = tuple(CANONICAL_FEATURES)


def normalize_features(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Normaliza as chaves do payload para o formato ASCII esperado pelo modelo."""
    normalized: Dict[str, Any] = {}
    for raw_key, value in payload.items():
        canonical_key = resolve_feature_name(raw_key)
        normalized[canonical_key] = value
    return normalized


def validate_feature_payload(features: Dict[str, Any]) -> None:
    """
    Valida se todas as features obrigatórias estão presentes e não são None.

    Lança ValueError com uma mensagem amigável em caso de problema.
    """
    missing = [feature for feature in REQUIRED_FEATURES if feature not in features]
    null_features = [feature for feature, value in features.items() if value is None]

    if missing:
        raise ValueError(
            f"Features obrigatórias ausentes: {', '.join(sorted(missing))}"
        )

    if null_features:
        raise ValueError(
            f"Features sem valor (None) detectadas: {', '.join(sorted(null_features))}"
        )


def ensure_only_known_features(features: Dict[str, Any]) -> None:
    """Garante que o payload não contém features desconhecidas."""
    unknown = [
        feature for feature in features if feature not in FEATURE_ALIASES.values()
    ]
    if unknown:
        raise ValueError(f"Features desconhecidas recebidas: {', '.join(unknown)}")

