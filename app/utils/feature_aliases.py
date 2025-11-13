from __future__ import annotations

from typing import Dict

# Definição das features canónicas utilizadas pelo modelo.
CANONICAL_FEATURES = [
    "price_per_night_usd",
    "rating",
    "avaliacao_clientes",
    "distancia_do_centro_km",
    "energia_renovavel",
    "gestao_residuos_indice",
    "consumo_agua_por_hospede",
    "carbon_footprint_score",
    "reciclagem_score",
    "energia_limpa_score",
    "water_usage_index",
    "sustainability_index",
    "eco_impact_index",
    "eco_value_ratio",
    "sentimento_score",
    "eco_keyword_count",
    "regiao_encoded",
    "possui_selo_sustentavel_encoded",
    "sentimento_sustentabilidade_encoded",
    "price_sust_ratio",
    "eco_value_score",
    "total_sust_score",
    "price_category",
    "water_consumption_ratio",
]

# Mapeamento de aliases (incluindo acentos) para nomes canónicos.
FEATURE_ALIASES: Dict[str, str] = {
    "avaliação_clientes": "avaliacao_clientes",
    "distância_do_centro_km": "distancia_do_centro_km",
    "energia_renovável": "energia_renovavel",
    "gestão_resíduos_índice": "gestao_residuos_indice",
    "consumo_água_por_hóspede": "consumo_agua_por_hospede",
    "região_encoded": "regiao_encoded",
    "possui_selo_sustentável_encoded": "possui_selo_sustentavel_encoded",
}

# Permite que uma feature já normalizada continue igual.
for canonical_feature in CANONICAL_FEATURES:
    FEATURE_ALIASES.setdefault(canonical_feature, canonical_feature)


def resolve_feature_name(raw_key: str) -> str:
    """Retorna o nome canónico da feature, quando suportado."""
    return FEATURE_ALIASES.get(raw_key, raw_key)

