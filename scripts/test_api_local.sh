#!/bin/bash

# Script para testar a API localmente passo a passo
set -euo pipefail

API_URL="http://localhost:8080"
API_KEY="${API_KEY:-ftl-sustainable-ai-key}"

echo "=========================================="
echo "🧪 Teste da API - Passo a Passo"
echo "=========================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${GREEN}▶${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Passo 1: Validar ambiente
print_step "Passo 1: Validando ambiente..."
if ./scripts/validate_env.sh > /dev/null 2>&1; then
    print_success "Ambiente validado"
else
    print_error "Falha na validação do ambiente"
    exit 1
fi
echo ""

# Passo 2: Verificar modelos
print_step "Passo 2: Verificando modelos..."
if [ -f "models/latest/model.pkl" ]; then
    print_success "model.pkl encontrado"
else
    print_warning "model.pkl não encontrado"
fi

if [ -f "models/latest/rihs_model.pkl" ]; then
    print_success "rihs_model.pkl encontrado (fallback)"
else
    print_warning "rihs_model.pkl não encontrado"
fi
echo ""

# Passo 3: Iniciar API em background
print_step "Passo 3: Iniciando API..."
echo "Executando: uvicorn app.main:app --host 0.0.0.0 --port 8080"
echo ""

# Mata qualquer processo anterior na porta 8080
lsof -ti:8080 | xargs kill -9 2>/dev/null || true

# Inicia a API em background
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8080 > /tmp/api.log 2>&1 &
API_PID=$!

# Aguarda a API iniciar
echo "Aguardando API iniciar..."
for i in {1..10}; do
    if curl -s http://localhost:8080/health > /dev/null 2>&1; then
        print_success "API iniciada (PID: $API_PID)"
        break
    fi
    sleep 1
    if [ $i -eq 10 ]; then
        print_error "API não iniciou após 10 segundos"
        echo "Logs:"
        tail -20 /tmp/api.log
        kill $API_PID 2>/dev/null || true
        exit 1
    fi
done
echo ""

# Passo 4: Testar endpoint raiz
print_step "Passo 4: Testando endpoint raiz (/)..."
ROOT_RESPONSE=$(curl -s http://localhost:8080/)
if echo "$ROOT_RESPONSE" | grep -q "Bem-vindo"; then
    print_success "Endpoint raiz funcionando"
    echo "$ROOT_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$ROOT_RESPONSE"
else
    print_error "Endpoint raiz falhou"
    echo "$ROOT_RESPONSE"
fi
echo ""

# Passo 5: Testar health check
print_step "Passo 5: Testando health check (/health)..."
HEALTH_RESPONSE=$(curl -s http://localhost:8080/health)
if echo "$HEALTH_RESPONSE" | grep -q "status"; then
    print_success "Health check funcionando"
    echo "$HEALTH_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$HEALTH_RESPONSE"
    
    # Verifica se o modelo está carregado
    if echo "$HEALTH_RESPONSE" | grep -q '"model_loaded": true'; then
        print_success "Modelo está carregado"
    else
        print_warning "Modelo não está carregado"
    fi
else
    print_error "Health check falhou"
    echo "$HEALTH_RESPONSE"
fi
echo ""

# Passo 6: Testar /model/info (requer API key)
print_step "Passo 6: Testando /model/info (requer API key)..."
MODEL_INFO_RESPONSE=$(curl -s -H "X-API-KEY: $API_KEY" http://localhost:8080/model/info)
if echo "$MODEL_INFO_RESPONSE" | grep -q "model_loaded"; then
    print_success "Endpoint /model/info funcionando"
    echo "$MODEL_INFO_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$MODEL_INFO_RESPONSE"
else
    print_error "Endpoint /model/info falhou"
    echo "$MODEL_INFO_RESPONSE"
fi
echo ""

# Passo 7: Testar /metadata
print_step "Passo 7: Testando /metadata..."
METADATA_RESPONSE=$(curl -s -H "X-API-KEY: $API_KEY" http://localhost:8080/metadata)
if echo "$METADATA_RESPONSE" | grep -q "version"; then
    print_success "Endpoint /metadata funcionando"
    echo "$METADATA_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$METADATA_RESPONSE"
else
    print_error "Endpoint /metadata falhou"
    echo "$METADATA_RESPONSE"
fi
echo ""

# Passo 8: Testar /predict
print_step "Passo 8: Testando /predict..."
PREDICT_PAYLOAD='{
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
}'

PREDICT_RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d "$PREDICT_PAYLOAD" \
  http://localhost:8080/predict)

if echo "$PREDICT_RESPONSE" | grep -q "prediction"; then
    print_success "Endpoint /predict funcionando"
    echo "$PREDICT_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$PREDICT_RESPONSE"
else
    print_error "Endpoint /predict falhou"
    echo "$PREDICT_RESPONSE"
fi
echo ""

# Passo 9: Testar /metrics
print_step "Passo 9: Testando /metrics (Prometheus)..."
METRICS_RESPONSE=$(curl -s http://localhost:8080/metrics)
if echo "$METRICS_RESPONSE" | grep -q "http_requests_total"; then
    print_success "Endpoint /metrics funcionando"
    echo "$METRICS_RESPONSE" | head -20
else
    print_warning "Endpoint /metrics não retornou métricas esperadas"
    echo "$METRICS_RESPONSE" | head -10
fi
echo ""

# Passo 10: Testar autenticação (sem API key)
print_step "Passo 10: Testando segurança (sem API key)..."
UNAUTH_RESPONSE=$(curl -s -w "\n%{http_code}" http://localhost:8080/predict -X POST \
  -H "Content-Type: application/json" \
  -d "$PREDICT_PAYLOAD" | tail -1)

if [ "$UNAUTH_RESPONSE" = "422" ] || [ "$UNAUTH_RESPONSE" = "403" ]; then
    print_success "Segurança funcionando (retornou $UNAUTH_RESPONSE)"
else
    print_warning "Segurança pode não estar funcionando (retornou $UNAUTH_RESPONSE)"
fi
echo ""

# Resumo final
echo "=========================================="
echo "📊 Resumo dos Testes"
echo "=========================================="
echo ""
echo "API rodando em: $API_URL"
echo "Documentação Swagger: $API_URL/docs"
echo "Documentação ReDoc: $API_URL/redoc"
echo ""
echo "Para parar a API, execute:"
echo "  kill $API_PID"
echo "  ou: lsof -ti:8080 | xargs kill -9"
echo ""
print_success "Testes concluídos!"

