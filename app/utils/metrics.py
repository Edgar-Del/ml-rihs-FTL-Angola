from __future__ import annotations

from prometheus_fastapi_instrumentator import Instrumentator


def init_metrics(app) -> None:
    """Configura o Prometheus Instrumentator para expor métricas em /metrics."""
    Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)

