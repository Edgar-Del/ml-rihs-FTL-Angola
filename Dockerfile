ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

# Definir argumentos de build
ARG BUILD_DATE
ARG PYTHON_VERSION

# Definir metadados
LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.python-version=$PYTHON_VERSION

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPYCACHEPREFIX=/tmp/__pycache__ \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de requirements primeiro (para aproveitar cache do Docker)
COPY requirements.txt .

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante da aplicação
COPY . .

# Expor porta
EXPOSE 8000

# Comando para executar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]