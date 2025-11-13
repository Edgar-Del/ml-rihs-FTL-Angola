from typing import List

from pydantic import BaseSettings, Field, field_validator


class Settings(BaseSettings):
    """Configurações da app"""
    
    # Application
    APP_NAME: str = "Recomendador Inteligente de Hospedagem Sustentável"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    
    # Model
    MODEL_REGISTRY_PATH: str = Field(default="models")
    MODEL_VERSION: str = Field(default="latest")
    MODEL_FALLBACK_VERSION: str = Field(default="baseline")
    METADATA_FILE: str = Field(default="models/metadata.json")
    
    # GCP
    PROJECT_ID: str = ""
    REGION: str = "europe-west1"
    
    # Security
    API_KEY: str | None = None
    
    # CORS
    CORS_ORIGINS: List[str] = Field(default_factory=lambda: ["https://painel-sustentavel.org"])
    
    class Config:
        env_file = ".env"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def _split_origins(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


# Instância global das configurações
settings = Settings()