#!/bin/bash

# Script para testar a API
set -e

API_URL="${1:-http://localhost:8080}"

echo "🧪 Testando API em: $API_URL"

# Testa health check
echo "1. Testando health check..."
curl -s "$API_URL/health" | jq . || echo "Resposta: $(curl -s $API_URL/health)"

# Testa informações do modelo
echo -e "\n2. Testando informações do modelo..."
curl -s "$API_URL/model/info" | jq . || echo "Resposta: $(curl -s $API_URL/model/info)"

# Testa predição
echo -e "\n3. Testando predição..."
curl -X POST "$API_URL/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "price_per_night_usd": 150.0,
    "rating": 4.2,
    "avaliação_clientes": 8.5,
    "distância_do_centro_km": 2.5,
    "energia_renovável": 75.0,
    "gestão_resíduos_índice": 0.8,
    "consumo_água_por_hóspede": 120.0,
    "carbon_footprint_score": 0.7,
    "reciclagem_score": 0.9,
    "energia_limpa_score": 0.8,
    "water_usage_index": 0.6,
    "sustainability_index": 0.85,
    "eco_impact_index": 0.75,
    "eco_value_ratio": 1.2,
    "sentimento_score": 0.8,
    "eco_keyword_count": 5,
    "região_encoded": 2,
    "possui_selo_sustentável_encoded": 1,
    "sentimento_sustentabilidade_encoded": 1,
    "price_sust_ratio": 1.5,
    "eco_value_score": 0.8,
    "total_sust_score": 0.85,
    "price_category": 2,
    "water_consumption_ratio": 0.7
  }' | jq . || echo "Resposta: $(curl -s -X POST ...)"

echo -e "\nTestes concluídos!"