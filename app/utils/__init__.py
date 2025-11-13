"""Utilitários compartilhados da aplicação."""

from .logging import setup_logging, timing_decorator  # noqa: F401
from .validation import (  # noqa: F401
    REQUIRED_FEATURES,
    normalize_features,
    validate_feature_payload,
)
from .security import verify_api_key  # noqa: F401
from .metrics import init_metrics  # noqa: F401

