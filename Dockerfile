# ============================================
# Dockerfile - RIHS API
# Recomendador Inteligente de Hospedagem Sustentável
# ============================================
# Multi-stage build otimizado para produção
# Python 3.11 com FastAPI, scikit-learn, XGBoost
# ============================================

# ============================================
# Stage 1: Builder - Compilação e Dependências
# ============================================
FROM python:3.11-slim AS builder

# Metadados do stage
LABEL stage=builder
LABEL maintainer="FTL Grupo-01"
LABEL description="Builder stage para compilação de dependências Python"

# Variáveis de build
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION=1.0.0

# Variáveis de ambiente para build
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /build

# Instala dependências de sistema necessárias para compilação
# Inclui compiladores e bibliotecas para numpy, scipy, scikit-learn, xgboost
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Atualiza pip e instala ferramentas de build
RUN pip install --upgrade pip setuptools wheel

# Copia requirements.txt primeiro para aproveitar cache do Docker
COPY requirements.txt .

# Instala dependências Python em diretório isolado
# Usa --user para instalar em /root/.local (será copiado no stage final)
RUN pip install --user --no-cache-dir -r requirements.txt

# Verifica instalação das dependências críticas
RUN python -c "import fastapi, sklearn, xgboost, numpy, pandas; print('Dependências críticas instaladas com sucesso')" || \
    (echo "ERRO: Falha na instalação de dependências críticas" && exit 1)

# ============================================
# Stage 2: Runtime - Imagem Final Otimizada
# ============================================
FROM python:3.11-slim AS runtime

# Metadados da imagem final
LABEL maintainer="FTL Grupo-01" \
      description="Recomendador Inteligente de Hospedagem Sustentável - API FastAPI" \
      version="1.0.0" \
      org.opencontainers.image.title="RIHS API" \
      org.opencontainers.image.description="API de classificação de sustentabilidade de hotéis" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.authors="FTL Grupo-01"

# Variáveis de build (para metadata)
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION=1.0.0

# Labels de build metadata
LABEL org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.version="${VERSION}"

WORKDIR /app

# Instala apenas dependências de runtime necessárias
# curl para healthcheck, ca-certificates para SSL
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && apt-get autoremove -y

# Cria usuário não-root para segurança
# UID 1000 é padrão e compatível com a maioria dos sistemas
RUN groupadd -r -g 1000 appuser && \
    useradd -r -u 1000 -g appuser -d /app -s /bin/bash appuser

# Copia dependências Python instaladas do builder
COPY --from=builder /root/.local /home/appuser/.local

# Ajusta permissões do diretório .local
RUN chown -R appuser:appuser /home/appuser/.local

# Adiciona /home/appuser/.local/bin ao PATH
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PORT=8080 \
    HOST=0.0.0.0

# Cria estrutura de diretórios necessária
RUN mkdir -p /app/logs /app/models && \
    chown -R appuser:appuser /app

# Copia script de entrada (antes de mudar para appuser)
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh && \
    chown appuser:appuser /app/docker-entrypoint.sh

# Copia código da aplicação
# Ordem otimizada: código muda mais frequentemente, então copia por último
COPY --chown=appuser:appuser app/ ./app/
COPY --chown=appuser:appuser core/ ./core/
COPY --chown=appuser:appuser ml/ ./ml/

# Copia modelos de ML (read-only)
# Modelos são grandes e mudam raramente, então podem ser cached
COPY --chown=appuser:appuser models/ ./models/

# Verifica se os arquivos críticos existem
RUN test -f ./app/main.py || (echo "ERRO: app/main.py não encontrado" && exit 1) && \
    test -f ./core/settings.py || (echo "ERRO: core/settings.py não encontrado" && exit 1) && \
    test -d ./models || (echo "ERRO: diretório models não encontrado" && exit 1)

# Verifica se o modelo padrão existe (aviso, não erro)
RUN if [ ! -f "./models/latest/sustainability_classification_pipeline.pkl" ]; then \
        echo "AVISO: Modelo padrão não encontrado. Certifique-se de configurar MODEL_REGISTRY_PATH corretamente."; \
    fi

# Healthcheck otimizado
# Usa variável PORT para flexibilidade
HEALTHCHECK --interval=30s \
            --timeout=10s \
            --start-period=40s \
            --retries=3 \
            CMD curl -f http://localhost:${PORT}/health || exit 1

# Expõe porta da aplicação
EXPOSE 8080

# Muda para usuário não-root ANTES de copiar código
# Isso garante que todos os arquivos criados sejam do usuário correto
USER appuser

# Verifica que o Python e as dependências estão acessíveis
RUN python --version && \
    python -c "import sys; print(f'Python {sys.version}')" && \
    python -c "import fastapi; print(f'FastAPI {fastapi.__version__}')" && \
    python -c "import uvicorn; print('Uvicorn disponível')" || \
    (echo "ERRO: Verificação de dependências falhou" && exit 1)

# Define script de entrada como ponto de entrada
# O script permite configuração flexível via variáveis de ambiente
ENTRYPOINT ["/app/docker-entrypoint.sh"]
