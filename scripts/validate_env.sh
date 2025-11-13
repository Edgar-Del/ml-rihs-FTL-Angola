#!/bin/bash

set -euo pipefail

if [ ! -f ".env" ]; then
  echo "Arquivo .env não encontrado na raiz."
  exit 1
fi

set -o allexport
source .env
set +o allexport

echo "Validating environment..."

if [ -z "${API_KEY:-}" ]; then
  echo "API_KEY missing"
  exit 1
fi

if [ -z "${MODEL_REGISTRY_PATH:-}" ]; then
  echo "MODEL_REGISTRY_PATH missing"
  exit 1
fi

if [ -z "${METADATA_FILE:-}" ]; then
  echo "METADATA_FILE missing"
  exit 1
fi

# Prioriza Python do venv se estiver activo
if [ -n "${VIRTUAL_ENV:-}" ] && [ -f "${VIRTUAL_ENV}/bin/python" ]; then
  PYTHON_BIN="${VIRTUAL_ENV}/bin/python"
elif [ -n "${PYTHON_BIN:-}" ]; then
  # Usa PYTHON_BIN se fornecido
  :
else
  PYTHON_BIN="$(command -v python3 || command -v python || echo '')"
fi

if [ -z "${PYTHON_BIN}" ] || [ ! -f "${PYTHON_BIN}" ]; then
  echo "Python interpreter not found. Configure PYTHON_BIN ou ative o venv."
  exit 1
fi

"${PYTHON_BIN}" - <<'PYCODE'
from core.settings import settings
print("Settings loaded successfully")
print(f"   • Environment: {settings.ENVIRONMENT}")
print(f"   • Model path: {settings.MODEL_REGISTRY_PATH}")
print(f"   • Metadata: {settings.METADATA_FILE}")
print(f"   • CORS origins: {settings.CORS_ORIGINS}")
PYCODE

