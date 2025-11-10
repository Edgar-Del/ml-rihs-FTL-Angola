import os
from typing import List
from pydantic import BaseSettings


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
    MODEL_PATH: str = "models/hotel_sustainability_classifier.pkl"
    MODEL_VERSION: str = "1.0.0"
    
    # GCP
    PROJECT_ID: str = ""
    REGION: str = "europe-west1"
    
    # Security
    API_KEY: str = "your-api-key-here"
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"


# Instância global das configurações
settings = Settings()