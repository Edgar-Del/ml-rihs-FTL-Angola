from typing import Dict, List

from pydantic import BaseModel, ConfigDict, Field


class PredictionInput(BaseModel):
    """
    Schema de entrada para classificação de sustentabilidade de hotéis.
    
    Este schema recebe todas as características necessárias para avaliar
    o nível de sustentabilidade de um estabelecimento hoteleiro, incluindo
    indicadores ambientais, sociais e económicos.
    
    **Nota:** Todos os campos são obrigatórios e devem seguir os tipos e
    intervalos especificados para garantir predições precisas.
    """
    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        protected_namespaces=(),
        json_schema_extra={
            "example": {
                "price_per_night_usd": 150.0,
                "rating": 4.5,
                "avaliação_clientes": 4.6,
                "distância_do_centro_km": 5.0,
                "energia_renovável": 75.0,
                "gestão_resíduos_índice": 80.0,
                "consumo_água_por_hóspede": 180.0,
                "carbon_footprint_score": 70.0,
                "reciclagem_score": 75.0,
                "energia_limpa_score": 78.0,
                "water_usage_index": 25.0,
                "sustainability_index": 75.0,
                "eco_impact_index": 72.0,
                "eco_value_ratio": 0.6,
                "sentimento_score": 0.7,
                "eco_keyword_count": 4,
                "região_encoded": 1,
                "possui_selo_sustentável_encoded": 1,
                "sentimento_sustentabilidade_encoded": 1,
                "price_sust_ratio": 0.3,
                "eco_value_score": 70.0,
                "total_sust_score": 73.0,
                "price_category": 2,
                "water_consumption_ratio": 0.2
            }
        }
    )

    price_per_night_usd: float = Field(
        ...,
        alias="price_per_night_usd",
        description="Preço médio por noite em dólares americanos (USD)",
        ge=0,
        le=10000,
        examples=[150.0, 250.0, 500.0]
    )
    
    rating: float = Field(
        ...,
        alias="rating",
        description="Avaliação geral do hotel (escala de 0 a 5)",
        ge=0,
        le=5,
        examples=[4.5, 4.0, 3.5]
    )
    
    avaliacao_clientes: float = Field(
        ...,
        alias="avaliação_clientes",
        description="Avaliação média dos clientes (escala de 0 a 5)",
        ge=0,
        le=5,
        examples=[4.6, 4.2, 3.8]
    )
    
    distancia_do_centro_km: float = Field(
        ...,
        alias="distância_do_centro_km",
        description="Distância do hotel ao centro da cidade em quilómetros",
        ge=0,
        examples=[5.0, 10.0, 2.0]
    )
    
    energia_renovavel: float = Field(
        ...,
        alias="energia_renovável",
        description="Percentagem de energia renovável utilizada (0-100)",
        ge=0,
        le=100,
        examples=[75.0, 90.0, 50.0]
    )
    
    gestao_residuos_indice: float = Field(
        ...,
        alias="gestão_resíduos_índice",
        description="Índice de gestão de resíduos (0-100, onde 100 é excelente)",
        ge=0,
        le=100,
        examples=[80.0, 95.0, 60.0]
    )
    
    consumo_agua_por_hospede: float = Field(
        ...,
        alias="consumo_água_por_hóspede",
        description="Consumo médio de água por hóspede por noite em litros",
        ge=0,
        examples=[180.0, 120.0, 250.0]
    )
    
    carbon_footprint_score: float = Field(
        ...,
        alias="carbon_footprint_score",
        description="Score de pegada de carbono (0-100, onde valores maiores indicam menor pegada)",
        ge=0,
        le=100,
        examples=[70.0, 85.0, 50.0]
    )
    
    reciclagem_score: float = Field(
        ...,
        alias="reciclagem_score",
        description="Score de práticas de reciclagem (0-100)",
        ge=0,
        le=100,
        examples=[75.0, 90.0, 55.0]
    )
    
    energia_limpa_score: float = Field(
        ...,
        alias="energia_limpa_score",
        description="Score de uso de energia limpa (0-100)",
        ge=0,
        le=100,
        examples=[78.0, 92.0, 60.0]
    )
    
    water_usage_index: float = Field(
        ...,
        alias="water_usage_index",
        description="Índice de uso de água (0-100, onde valores menores são melhores)",
        ge=0,
        le=100,
        examples=[25.0, 15.0, 45.0]
    )
    
    sustainability_index: float = Field(
        ...,
        alias="sustainability_index",
        description="Índice geral de sustentabilidade (0-100)",
        ge=0,
        le=100,
        examples=[75.0, 88.0, 55.0]
    )
    
    eco_impact_index: float = Field(
        ...,
        alias="eco_impact_index",
        description="Índice de impacto ecológico (0-100, onde valores maiores são melhores)",
        ge=0,
        le=100,
        examples=[72.0, 85.0, 50.0]
    )
    
    eco_value_ratio: float = Field(
        ...,
        alias="eco_value_ratio",
        description="Razão entre valor ecológico e preço (0-1, onde valores maiores são melhores)",
        ge=0,
        le=1,
        examples=[0.6, 0.8, 0.4]
    )
    
    sentimento_score: float = Field(
        ...,
        alias="sentimento_score",
        description="Score de sentimento extraído de reviews sobre sustentabilidade (-1 a 1)",
        ge=-1,
        le=1,
        examples=[0.7, 0.9, 0.3]
    )
    
    eco_keyword_count: int = Field(
        ...,
        alias="eco_keyword_count",
        description="Número de palavras-chave ecológicas mencionadas em reviews",
        ge=0,
        examples=[4, 6, 2]
    )
    
    regiao_encoded: int = Field(
        ...,
        alias="região_encoded",
        description="Código numérico da região (0-4)",
        ge=0,
        le=4,
        examples=[1, 2, 0]
    )
    
    possui_selo_sustentavel_encoded: int = Field(
        ...,
        alias="possui_selo_sustentável_encoded",
        description="Indica se possui selo de sustentabilidade (0=Não, 1=Sim)",
        ge=0,
        le=1,
        examples=[1, 0]
    )
    
    sentimento_sustentabilidade_encoded: int = Field(
        ...,
        alias="sentimento_sustentabilidade_encoded",
        description="Sentimento codificado sobre sustentabilidade (0=Negativo, 1=Positivo)",
        ge=0,
        le=1,
        examples=[1, 0]
    )
    
    price_sust_ratio: float = Field(
        ...,
        alias="price_sust_ratio",
        description="Razão entre preço e sustentabilidade (0-1, onde valores menores são melhores)",
        ge=0,
        le=1,
        examples=[0.3, 0.5, 0.2]
    )
    
    eco_value_score: float = Field(
        ...,
        alias="eco_value_score",
        description="Score de valor ecológico (0-100)",
        ge=0,
        le=100,
        examples=[70.0, 85.0, 55.0]
    )
    
    total_sust_score: float = Field(
        ...,
        alias="total_sust_score",
        description="Score total de sustentabilidade (0-100)",
        ge=0,
        le=100,
        examples=[73.0, 88.0, 60.0]
    )
    
    price_category: int = Field(
        ...,
        alias="price_category",
        description="Categoria de preço (0=Económico, 1=Médio, 2=Alto, 3=Luxo)",
        ge=0,
        le=3,
        examples=[2, 1, 3]
    )
    
    water_consumption_ratio: float = Field(
        ...,
        alias="water_consumption_ratio",
        description="Razão de consumo de água (0-1, onde valores menores são melhores)",
        ge=0,
        le=1,
        examples=[0.2, 0.15, 0.35]
    )

    def to_feature_dict(self) -> Dict[str, float | int]:
        """Retorna o payload com chaves ASCII prontas para inferência."""
        return self.model_dump(by_alias=False)


class PredictionOutput(BaseModel):
    """
    Schema de saída da classificação de sustentabilidade.
    
    Contém a predição do modelo, probabilidades para todas as classes,
    e informações sobre a confiança da predição.
    """
    model_config = ConfigDict(
        protected_namespaces=(),
        json_schema_extra={
            "example": {
                "prediction": 3,
                "probabilities": [0.02, 0.05, 0.08, 0.15, 0.70],
                "prediction_label": "Alto",
                "confidence": 70.0,
                "all_probabilities": {
                    "Muito Baixo": 0.02,
                    "Baixo": 0.05,
                    "Médio": 0.08,
                    "Alto": 0.15,
                    "Muito Alto": 0.70
                },
                "model_version": "1.0.0"
            }
        }
    )
    
    prediction: int = Field(
        ...,
        description="Classe predita (0=Muito Baixo, 1=Baixo, 2=Médio, 3=Alto, 4=Muito Alto)",
        ge=0,
        le=4,
        examples=[3, 4, 2]
    )
    
    probabilities: List[float] = Field(
        ...,
        description="Lista de probabilidades para cada classe (ordem: Muito Baixo, Baixo, Médio, Alto, Muito Alto)",
        min_length=5,
        max_length=5,
        examples=[[0.02, 0.05, 0.08, 0.15, 0.70]]
    )
    
    prediction_label: str = Field(
        ...,
        description="Rótulo textual da classe predita",
        examples=["Muito Alto", "Alto", "Médio", "Baixo", "Muito Baixo"]
    )
    
    confidence: float = Field(
        ...,
        description="Confiança da predição em percentagem (0-100)",
        ge=0,
        le=100,
        examples=[70.0, 85.5, 92.3]
    )
    
    all_probabilities: Dict[str, float] = Field(
        ...,
        description="Todas as probabilidades mapeadas para nomes de classes",
        examples=[{
            "Muito Baixo": 0.02,
            "Baixo": 0.05,
            "Médio": 0.08,
            "Alto": 0.15,
            "Muito Alto": 0.70
        }]
    )
    
    model_version: str = Field(
        ...,
        description="Versão do modelo utilizado para a predição",
        examples=["1.0.0", "1.1.0"]
    )


class HealthResponse(BaseModel):
    """
    Schema de resposta para o health check.
    
    Indica o estado de saúde da API e se o modelo está carregado e pronto para uso.
    """
    model_config = ConfigDict(
        protected_namespaces=(),
        json_schema_extra={
            "example": {
                "status": "healthy",
                "model_loaded": True,
                "version": "1.0.0"
            }
        }
    )
    
    status: str = Field(
        ...,
        description="Estado de saúde da API (healthy ou unhealthy)",
        examples=["healthy", "unhealthy"]
    )
    
    model_loaded: bool = Field(
        ...,
        description="Indica se o modelo de ML está carregado e pronto para uso",
        examples=[True, False]
    )
    
    version: str = Field(
        ...,
        description="Versão da API",
        examples=["1.0.0"]
    )


class ModelInfoResponse(BaseModel):
    """
    Schema de resposta com informações detalhadas sobre o modelo.
    """
    model_config = ConfigDict(
        protected_namespaces=(),
        json_schema_extra={
            "example": {
                "model_loaded": True,
                "feature_names": ["price_per_night_usd", "rating", "sustainability_index"],
                "class_labels": {
                    "0": "Muito Baixo",
                    "1": "Baixo",
                    "2": "Médio",
                    "3": "Alto",
                    "4": "Muito Alto"
                },
                "version": "1.0.0",
                "metadata": {
                    "accuracy": 0.92,
                    "f1_weighted": 0.91
                }
            }
        }
    )
    
    model_loaded: bool = Field(..., description="Indica se o modelo está carregado")
    feature_names: List[str] = Field(..., description="Lista de nomes das features utilizadas pelo modelo")
    class_labels: Dict[str, str] = Field(..., description="Mapeamento de classes (código -> rótulo)")
    version: str = Field(..., description="Versão do modelo")
    metadata: Dict = Field(..., description="Metadados adicionais do modelo (métricas, performance, etc.)")


class ErrorResponse(BaseModel):
    """
    Schema para respostas de erro da API.
    """
    model_config = ConfigDict(
        protected_namespaces=(),
        json_schema_extra={
            "example": {
                "detail": "API key missing or invalid"
            }
        }
    )
    
    detail: str = Field(..., description="Mensagem de erro descritiva")
