from fastapi import Header, HTTPException, status

from app.config import settings


def verify_api_key(x_api_key: str = Header(..., alias="X-API-KEY")) -> None:
    """Verifica se o header X-API-KEY é válido."""
    expected_api_key = settings.API_KEY

    if expected_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API key não configurada no servidor.",
        )

    if x_api_key != expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key inválida.",
        )

