#!/bin/bash
set -e

# Script de entrada para o container Docker
# Permite configuração flexível via variáveis de ambiente

# Valores padrão
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
WORKERS=${WORKERS:-1}

# Log de configuração
echo "=========================================="
echo "RIHS API - Iniciando..."
echo "=========================================="
echo "Host: ${HOST}"
echo "Port: ${PORT}"
echo "Workers: ${WORKERS}"
echo "Environment: ${ENVIRONMENT:-production}"
echo "=========================================="

# Verifica se o modelo existe (aviso, não erro fatal)
if [ -n "${MODEL_REGISTRY_PATH}" ]; then
    if [ ! -f "${MODEL_REGISTRY_PATH}" ]; then
        echo "AVISO: Modelo não encontrado em ${MODEL_REGISTRY_PATH}"
        echo "Certifique-se de que o caminho está correto ou que o modelo foi copiado para o container."
    else
        echo "Modelo encontrado: ${MODEL_REGISTRY_PATH}"
    fi
fi

# Executa uvicorn com os parâmetros configurados
exec uvicorn app.main:app \
    --host "${HOST}" \
    --port "${PORT}" \
    --workers "${WORKERS}" \
    --no-access-log

