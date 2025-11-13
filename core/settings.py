from __future__ import annotations

import logging
from pathlib import Path
from typing import Annotated, List, Union

from pydantic import Field, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações globais da aplicação."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
        env_parse_none_str="",
    )

    APP_NAME: str = "Recomendador Inteligente de Hospedagem Sustentável"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "dev"
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    DEBUG: bool = False
    MODEL_REGISTRY_PATH: str = "./models/latest/model.pkl"
    METADATA_FILE: str = "./models/metadata.json"
    API_KEY: str = Field(..., min_length=3)
    CORS_ORIGINS: Union[str, List[str]] = Field(default="*")
    LOG_LEVEL: str = "INFO"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors(cls, value):
        # Trata valores vazios ou None
        if not value or (isinstance(value, str) and not value.strip()):
            return ["*"]  # Retorna default se vazio
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            cleaned = value.strip()
            # Remove colchetes se presentes
            if cleaned.startswith("[") and cleaned.endswith("]"):
                cleaned = cleaned[1:-1]
            # Remove aspas
            cleaned = cleaned.replace('"', "").replace("'", "")
            # Split por vírgula e filtra vazios
            items = [item.strip() for item in cleaned.split(",") if item.strip()]
            return items if items else ["*"]
        return value

    @field_validator("CORS_ORIGINS", mode="after")
    @classmethod
    def ensure_list(cls, value):
        # Garante que sempre retorna List[str]
        if isinstance(value, str):
            return [value] if value else ["*"]
        return value if isinstance(value, list) else ["*"]

    @field_validator("API_KEY")
    @classmethod
    def validate_api_key(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("API_KEY is required and cannot be empty")
        return value.strip()

    @field_validator("MODEL_REGISTRY_PATH", "METADATA_FILE", mode="after")
    @classmethod
    def validate_paths(cls, value: str, info):
        if not value:
            raise ValueError(f"{info.field_name} is required")
        # Normaliza para path relativo/absoluto consistente
        normalized = str(Path(value))
        return normalized

    @property
    def cors_origins_list(self) -> List[str]:
        """Garante que CORS_ORIGINS sempre retorna List[str]."""
        value = self.CORS_ORIGINS
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [value] if value else ["*"]
        return ["*"]


try:
    settings = Settings()
    logging.info("Settings loaded successfully")
except ValidationError as exc:
    logging.error("Settings initialization failed: %s", exc)
    raise RuntimeError(f"Settings initialization failed: {exc}") from exc

