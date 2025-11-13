#!/bin/bash

# Script de deploy para o Recomendador Inteligente de Hospedagem Sustentável.
# Uso:
#   ./scripts/deploy.sh [dev|staging|prod] [IMAGE_TAG]

set -euo pipefail

ENVIRONMENT="${1:-dev}"
IMAGE_TAG="${2:-$(date +%Y%m%d%H%M%S)}"

PROJECT_ID="${PROJECT_ID:-ftl-tourism-ai}"
REGION="${REGION:-europe-west1}"
SERVICE_NAME_BASE="${SERVICE_NAME_BASE:-recomendador-sustentavel}"

case "$ENVIRONMENT" in
  dev)
    SERVICE_NAME="${SERVICE_NAME_BASE}-dev"
    MIN_INSTANCES="${MIN_INSTANCES:-0}"
    MAX_INSTANCES="${MAX_INSTANCES:-2}"
    ;;
  staging)
    SERVICE_NAME="${SERVICE_NAME_BASE}-stg"
    MIN_INSTANCES="${MIN_INSTANCES:-0}"
    MAX_INSTANCES="${MAX_INSTANCES:-3}"
    ;;
  prod)
    SERVICE_NAME="${SERVICE_NAME_BASE}"
    MIN_INSTANCES="${MIN_INSTANCES:-1}"
    MAX_INSTANCES="${MAX_INSTANCES:-5}"
    ;;
  *)
    echo "Ambiente inválido: ${ENVIRONMENT}. Utilize dev, staging ou prod."
    exit 1
    ;;
esac

if [[ -z "${PROJECT_ID}" ]]; then
  echo "Variável PROJECT_ID não definida."
  exit 1
fi

if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
  echo "gcloud não autenticado. Execute 'gcloud auth login'."
  exit 1
fi

gcloud config set project "${PROJECT_ID}"

IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}:${IMAGE_TAG}"

echo "==> Construindo imagem ${IMAGE}"
gcloud builds submit --tag "${IMAGE}"

echo "==> Fazendo deploy no Cloud Run (${ENVIRONMENT})"
gcloud run deploy "${SERVICE_NAME}" \
  --image "${IMAGE}" \
  --region "${REGION}" \
  --platform managed \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --min-instances "${MIN_INSTANCES}" \
  --max-instances "${MAX_INSTANCES}" \
  --set-env-vars "API_KEY=${API_KEY:-change-me},MODEL_REGISTRY_PATH=${MODEL_REGISTRY_PATH:-./models/latest/model.pkl},METADATA_FILE=${METADATA_FILE:-./models/metadata.json},CORS_ORIGINS=${CORS_ORIGINS:-https://painel-sustentavel.org}"

SERVICE_URL="$(gcloud run services describe "${SERVICE_NAME}" --region "${REGION}" --format="value(status.url)")"

echo "==> Deploy concluído: ${SERVICE_URL}"
echo "    Documentação Swagger: ${SERVICE_URL}/docs"
echo "    Métricas Prometheus:  ${SERVICE_URL}/metrics"

echo "==> Verificando health check..."
if curl -fsS "${SERVICE_URL}/health" > /dev/null; then
  echo "Health check OK"
else
  echo "Health check falhou - veja 'gcloud run logs read ${SERVICE_NAME}'"
fi