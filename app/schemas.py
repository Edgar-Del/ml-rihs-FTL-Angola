from typing import Dict, List

from pydantic import BaseModel, ConfigDict, Field


class PredictionInput(BaseModel):
    """Schema para input de predição"""
    model_config = ConfigDict(populate_by_name=True, extra="forbid", allow_population_by_field_name=True)

    price_per_night_usd: float = Field(..., alias="price_per_night_usd", example=150.0)
    rating: float = Field(..., alias="rating", example=4.2)
    avaliacao_clientes: float = Field(..., alias="avaliação_clientes", example=8.5)
    distancia_do_centro_km: float = Field(..., alias="distância_do_centro_km", example=2.5)
    energia_renovavel: float = Field(..., alias="energia_renovável", example=75.0)
    gestao_residuos_indice: float = Field(..., alias="gestão_resíduos_índice", example=0.8)
    consumo_agua_por_hospede: float = Field(..., alias="consumo_água_por_hóspede", example=120.0)
    carbon_footprint_score: float = Field(..., alias="carbon_footprint_score", example=0.7)
    reciclagem_score: float = Field(..., alias="reciclagem_score", example=0.9)
    energia_limpa_score: float = Field(..., alias="energia_limpa_score", example=0.8)
    water_usage_index: float = Field(..., alias="water_usage_index", example=0.6)
    sustainability_index: float = Field(..., alias="sustainability_index", example=0.85)
    eco_impact_index: float = Field(..., alias="eco_impact_index", example=0.75)
    eco_value_ratio: float = Field(..., alias="eco_value_ratio", example=1.2)
    sentimento_score: float = Field(..., alias="sentimento_score", example=0.8)
    eco_keyword_count: int = Field(..., alias="eco_keyword_count", example=5)
    regiao_encoded: int = Field(..., alias="região_encoded", example=2)
    possui_selo_sustentavel_encoded: int = Field(..., alias="possui_selo_sustentável_encoded", example=1)
    sentimento_sustentabilidade_encoded: int = Field(..., alias="sentimento_sustentabilidade_encoded", example=1)
    price_sust_ratio: float = Field(..., alias="price_sust_ratio", example=1.5)
    eco_value_score: float = Field(..., alias="eco_value_score", example=0.8)
    total_sust_score: float = Field(..., alias="total_sust_score", example=0.85)
    price_category: int = Field(..., alias="price_category", example=2)
    water_consumption_ratio: float = Field(..., alias="water_consumption_ratio", example=0.7)

    def to_feature_dict(self) -> Dict[str, float | int]:
        """Retorna o payload com chaves ASCII prontas para inferência."""
        return self.model_dump(by_alias=False)


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