#!/bin/bash

# Script de deploy para FinalProjectFTL
set -e

echo "Iniciando deploy do FinalProjectFTL..."

# Configurações (edite estas variáveis)
PROJECT_ID="seu-projeto-id"
REGION="Africa"
SERVICE_NAME="hotel-sustainability-api"
IMAGE_TAG="v1.0.0"

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Função para imprimir com cor
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Verifica se gcloud está autenticado
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
    print_error "gcloud não está autenticado. Execute 'gcloud auth login' primeiro."
    exit 1
fi

# Define projeto
print_status "Configurando projeto: $PROJECT_ID"
gcloud config set project $PROJECT_ID

# Habilita APIs necessárias
print_status "Habilitando APIs..."
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable artifactregistry.googleapis.com

# Cria repositório no Artifact Registry se não existir
print_status "Configurando Artifact Registry..."
if ! gcloud artifacts repositories describe $SERVICE_NAME --location=$REGION &>/dev/null; then
    gcloud artifacts repositories create $SERVICE_NAME \
        --repository-format=docker \
        --location=$REGION \
        --description="Repositório Docker para Hotel Sustainability API"
fi

# Build da imagem Docker
print_status "Construindo imagem Docker..."
docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/$SERVICE_NAME/$SERVICE_NAME:$IMAGE_TAG .

# Push da imagem
print_status "Enviando imagem para Artifact Registry..."
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$SERVICE_NAME/$SERVICE_NAME:$IMAGE_TAG

# Deploy no Cloud Run
print_status "Realizando deploy no Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $REGION-docker.pkg.dev/$PROJECT_ID/$SERVICE_NAME/$SERVICE_NAME:$IMAGE_TAG \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --memory 512Mi \
    --cpu 1 \
    --set-env-vars "MODEL_PATH=models/hotel_sustainability_classifier.pkl" \
    --min-instances 0 \
    --max-instances 5

# Obtém URL do serviço
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format="value(status.url)")

print_status "Deploy concluído com sucesso!"
echo ""
echo "URL do serviço: $SERVICE_URL"
echo "Documentação: $SERVICE_URL/docs"
echo "Health check: $SERVICE_URL/health"

# Testa o health check
print_status "Testando health check..."
sleep 10
if curl -f "$SERVICE_URL/health" > /dev/null 2>&1; then
    print_status "Health check passou!"
else
    print_warning "Health check falhou - verifique os logs"
fi

echo ""
print_status "Deploy finalizado! A API está pronta para uso."