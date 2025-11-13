# Guia de Docker para a Aplicação

Este guia explica como construir e executar a aplicação usando Docker.

## Pré-requisitos

- Docker instalado (versão 20.10+)
- Docker Compose (opcional, mas recomendado)

## Construção da Imagem

### Build básico

```bash
docker build -t rihs-api:latest .
```

### Build com tag específica e metadata

```bash
docker build \
  --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
  --build-arg VCS_REF=$(git rev-parse --short HEAD) \
  --build-arg VERSION=1.0.0 \
  -t rihs-api:v1.0.0 \
  -t rihs-api:latest \
  .
```

### Build otimizado (usando cache)

```bash
docker build --cache-from rihs-api:latest -t rihs-api:latest .
```

### Build com workers customizados

O Dockerfile suporta a variável `WORKERS` para controlar o número de workers do uvicorn:

```bash
docker run -d \
  -e WORKERS=4 \
  -e API_KEY=your-key \
  rihs-api:latest
```

## Executando o Container

### Modo básico

```bash
docker run -d \
  --name rihs-api \
  -p 8080:8080 \
  -e API_KEY=your-api-key-here \
  -e MODEL_REGISTRY_PATH=./models/latest/sustainability_classification_pipeline.pkl \
  -e METADATA_FILE=./models/metadata.json \
  rihs-api:latest
```

### Com variáveis de ambiente do arquivo .env

```bash
docker run -d \
  --name rihs-api \
  -p 8080:8080 \
  --env-file .env \
  rihs-api:latest
```

### Com volume para modelos (desenvolvimento)

```bash
docker run -d \
  --name rihs-api \
  -p 8080:8080 \
  -e API_KEY=your-api-key-here \
  -v $(pwd)/models:/app/models:ro \
  rihs-api:latest
```

## Usando Docker Compose

### Iniciar

```bash
docker-compose up -d
```

### Ver logs

```bash
docker-compose logs -f api
```

### Parar

```bash
docker-compose down
```

### Reconstruir após mudanças

```bash
docker-compose up -d --build
```

## Variáveis de Ambiente

As seguintes variáveis podem ser configuradas:

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `API_KEY` | Chave de API para autenticação | **Obrigatório** |
| `MODEL_REGISTRY_PATH` | Caminho para o modelo | `./models/latest/sustainability_classification_pipeline.pkl` |
| `METADATA_FILE` | Caminho para metadados | `./models/metadata.json` |
| `CORS_ORIGINS` | Origens permitidas (CORS) | `*` |
| `LOG_LEVEL` | Nível de log | `INFO` |
| `DEBUG` | Modo debug | `false` |
| `PORT` | Porta da aplicação | `8080` |
| `HOST` | Host da aplicação | `0.0.0.0` |
| `WORKERS` | Número de workers do uvicorn | `1` |

## Verificando o Container

### Ver logs

```bash
docker logs rihs-api
```

### Ver logs em tempo real

```bash
docker logs -f rihs-api
```

### Verificar saúde

```bash
docker inspect --format='{{.State.Health.Status}}' rihs-api
```

### Executar comandos no container

```bash
docker exec -it rihs-api /bin/bash
```

## Testando a API

Após iniciar o container:

```bash
# Health check
curl http://localhost:8080/health

# Teste de predição
curl -X POST "http://localhost:8080/predict" \
  -H "X-API-KEY: your-api-key-here" \
  -H "Content-Type: application/json" \
  -d @test_payload.json
```

## Otimizações

### Multi-stage Build

O Dockerfile usa multi-stage build otimizado para:
- **Stage 1 (builder)**: Compila dependências que requerem compiladores (numpy, scipy, scikit-learn, xgboost)
- **Stage 2 (runtime)**: Imagem final minimalista apenas com dependências de runtime
- Reduz tamanho da imagem final (~500-700MB vs ~2GB se tudo fosse incluído)
- Separa dependências de build das de runtime
- Melhora cache do Docker

### Cache de Layers

O Dockerfile está otimizado para aproveitar o cache:
1. **requirements.txt** é copiado primeiro (muda raramente)
2. Dependências são instaladas antes do código (código muda frequentemente)
3. Modelos são copiados separadamente (mudam raramente)
4. Código é copiado por último (muda frequentemente)
5. `.dockerignore` exclui arquivos desnecessários

### Melhorias Implementadas

- ✅ **Compiladores otimizados**: Inclui gfortran, libopenblas-dev para melhor performance de ML
- ✅ **Verificações de integridade**: Valida instalação de dependências críticas durante build
- ✅ **Metadata OCI**: Labels padronizados para rastreabilidade
- ✅ **Segurança**: Usuário não-root (UID 1000), permissões corretas
- ✅ **Flexibilidade**: Suporta variável WORKERS para ajuste de performance
- ✅ **Healthcheck**: Verificação automática de saúde do container
- ✅ **Validação**: Verifica existência de arquivos críticos durante build

## Troubleshooting

### Container não inicia

```bash
# Ver logs de erro
docker logs rihs-api

# Verificar se a porta está em uso
lsof -i :8080
```

### Modelo não carrega

```bash
# Verificar se o modelo existe no container
docker exec rihs-api ls -la /app/models/latest/

# Verificar variáveis de ambiente
docker exec rihs-api env | grep MODEL
```

### Erro de permissão

O container roda como usuário não-root (`appuser`) por segurança. Se houver problemas de permissão:

```bash
# Verificar permissões
docker exec rihs-api ls -la /app
```

## Deploy em Produção

### Google Cloud Run

```bash
# Build e push para GCR
gcloud builds submit --tag gcr.io/PROJECT_ID/rihs-api

# Deploy
gcloud run deploy rihs-api \
  --image gcr.io/PROJECT_ID/rihs-api \
  --platform managed \
  --region europe-west1 \
  --set-env-vars API_KEY=your-secret-key \
  --set-secrets API_KEY=api-key-secret:latest
```

### Usando o script de deploy

```bash
./scripts/deploy.sh
```

## Segurança

- ✅ Container roda como usuário não-root
- ✅ Apenas dependências de runtime na imagem final
- ✅ Healthcheck configurado
- ✅ Variáveis sensíveis via secrets (produção)

## Tamanho da Imagem

A imagem final deve ter aproximadamente:
- **~500-700MB** (com todas as dependências ML: numpy, scipy, scikit-learn, xgboost, pandas)

### Estrutura de Tamanho

- **Base Python 3.11-slim**: ~120MB
- **Dependências Python**: ~350-450MB
- **Modelos ML**: ~50-100MB (depende dos modelos incluídos)
- **Código da aplicação**: ~5-10MB

### Otimizações Aplicadas

- ✅ Multi-stage build remove compiladores e ferramentas de build
- ✅ Apenas dependências de runtime na imagem final
- ✅ Cache de layers otimizado
- ✅ `.dockerignore` exclui arquivos desnecessários

### Para Reduzir Ainda Mais (Avançado)

- Use imagens Alpine (pode ter problemas com algumas dependências ML)
- Remova dependências não utilizadas do requirements.txt
- Use distroless images (mais complexo, requer ajustes)
- Compile modelos para formato mais compacto

