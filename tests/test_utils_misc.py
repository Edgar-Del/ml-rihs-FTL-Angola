from app.utils.logging import setup_logging, timing_decorator
from app.utils.security import verify_api_key


def test_setup_logging_no_errors():
    # Apenas garante que a configuração não lança exceções
    setup_logging()


def test_timing_decorator_executes_function():
    @timing_decorator
    def add(a, b):
        return a + b

    assert add(2, 3) == 5


def test_verify_api_key_success(monkeypatch):
    from core.settings import settings

    monkeypatch.setattr(settings, "API_KEY", "k", raising=False)
    from app.utils.security import verify_api_key as verify

    verify(x_api_key="k")


def test_verify_api_key_failure(monkeypatch):
    from core.settings import settings

    monkeypatch.setattr(settings, "API_KEY", "k2", raising=False)
    from app.utils.security import verify_api_key as verify
    try:
        verify(x_api_key="wrong")
        assert False, "Deveria lançar HTTPException com 403"
    except Exception as exc:
        from fastapi import HTTPException

        assert isinstance(exc, HTTPException)

