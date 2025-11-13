from typing import Dict, List

from pydantic import BaseModel, ConfigDict, Field


class PredictionInput(BaseModel):
    """Schema para input de predição"""
    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        protected_namespaces=(),
    )

    price_per_night_usd: float = Field(..., alias="price_per_night_usd")
    rating: float = Field(..., alias="rating")
    avaliacao_clientes: float = Field(..., alias="avaliação_clientes")
    distancia_do_centro_km: float = Field(..., alias="distância_do_centro_km")
    energia_renovavel: float = Field(..., alias="energia_renovável")
    gestao_residuos_indice: float = Field(..., alias="gestão_resíduos_índice")
    consumo_agua_por_hospede: float = Field(..., alias="consumo_água_por_hóspede")
    carbon_footprint_score: float = Field(..., alias="carbon_footprint_score")
    reciclagem_score: float = Field(..., alias="reciclagem_score")
    energia_limpa_score: float = Field(..., alias="energia_limpa_score")
    water_usage_index: float = Field(..., alias="water_usage_index")
    sustainability_index: float = Field(..., alias="sustainability_index")
    eco_impact_index: float = Field(..., alias="eco_impact_index")
    eco_value_ratio: float = Field(..., alias="eco_value_ratio")
    sentimento_score: float = Field(..., alias="sentimento_score")
    eco_keyword_count: int = Field(..., alias="eco_keyword_count")
    regiao_encoded: int = Field(..., alias="região_encoded")
    possui_selo_sustentavel_encoded: int = Field(..., alias="possui_selo_sustentável_encoded")
    sentimento_sustentabilidade_encoded: int = Field(..., alias="sentimento_sustentabilidade_encoded")
    price_sust_ratio: float = Field(..., alias="price_sust_ratio")
    eco_value_score: float = Field(..., alias="eco_value_score")
    total_sust_score: float = Field(..., alias="total_sust_score")
    price_category: int = Field(..., alias="price_category")
    water_consumption_ratio: float = Field(..., alias="water_consumption_ratio")

    def to_feature_dict(self) -> Dict[str, float | int]:
        """Retorna o payload com chaves ASCII prontas para inferência."""
        return self.model_dump(by_alias=False)


class PredictionOutput(BaseModel):
    """Schema para output de predição"""
    model_config = ConfigDict(protected_namespaces=())
    prediction: int
    probabilities: List[float]
    prediction_label: str
    model_version: str


class HealthResponse(BaseModel):
    """Schema para health check"""
    model_config = ConfigDict(protected_namespaces=())
    status: str
    model_loaded: bool
    version: str


class ErrorResponse(BaseModel):
    """Schema para respostas de erro"""
    error: str
    message: str