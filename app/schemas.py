from pydantic import BaseModel, Field
from typing import List, Optional


class PredictionInput(BaseModel):
    """Schema para input de predição"""
    price_per_night_usd: float = Field(..., example=150.0)
    rating: float = Field(..., example=4.2)
    avaliação_clientes: float = Field(..., example=8.5)
    distância_do_centro_km: float = Field(..., example=2.5)
    energia_renovável: float = Field(..., example=75.0)
    gestão_resíduos_índice: float = Field(..., example=0.8)
    consumo_água_por_hóspede: float = Field(..., example=120.0)
    carbon_footprint_score: float = Field(..., example=0.7)
    reciclagem_score: float = Field(..., example=0.9)
    energia_limpa_score: float = Field(..., example=0.8)
    water_usage_index: float = Field(..., example=0.6)
    sustainability_index: float = Field(..., example=0.85)
    eco_impact_index: float = Field(..., example=0.75)
    eco_value_ratio: float = Field(..., example=1.2)
    sentimento_score: float = Field(..., example=0.8)
    eco_keyword_count: int = Field(..., example=5)
    região_encoded: int = Field(..., example=2)
    possui_selo_sustentável_encoded: int = Field(..., example=1)
    sentimento_sustentabilidade_encoded: int = Field(..., example=1)
    price_sust_ratio: float = Field(..., example=1.5)
    eco_value_score: float = Field(..., example=0.8)
    total_sust_score: float = Field(..., example=0.85)
    price_category: int = Field(..., example=2)
    water_consumption_ratio: float = Field(..., example=0.7)


class PredictionOutput(BaseModel):
    """Schema para output de predição"""
    prediction: int = Field(..., example=3)
    probabilities: List[float] = Field(..., example=[0.1, 0.2, 0.3, 0.35, 0.05])
    prediction_label: str = Field(..., example="Alta Sustentabilidade")
    model_version: str = Field(..., example="1.0.0")


class HealthResponse(BaseModel):
    """Schema para health check"""
    status: str
    model_loaded: bool
    version: str


class ErrorResponse(BaseModel):
    """Schema para respostas de erro"""
    error: str
    message: str