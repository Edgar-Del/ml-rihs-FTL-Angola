# Docker Compose - Guia de Uso

Este documento descreve como usar o `docker-compose.yml` para executar a aplicação RIHS com todos os serviços necessários.

## 📋 Visão Geral

O `docker-compose.yml` inclui os seguintes serviços:

- **API** - Aplicação FastAPI principal (porta 8080)
- **Prometheus** - Coleta de métricas (porta 9090)
- **Grafana** - Visualização de métricas e dashboards (porta 3000)
- **PostgreSQL** - Banco de dados (comentado, para uso futuro)
- **PgAdmin** - Interface web para PostgreSQL (comentado, para uso futuro)

## 🚀 Início Rápido

### 1. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# API
API_KEY=seu-api-key-aqui
PORT=8080
ENVIRONMENT=production
LOG_LEVEL=INFO
DEBUG=false

# Modelos
MODEL_REGISTRY_PATH=./models/latest/sustainability_classification_pipeline.pkl
METADATA_FILE=./models/metadata.json

# CORS
CORS_ORIGINS=*

# Grafana (opcional)
GRAFANA_USER=admin
GRAFANA_PASSWORD=admin

# PostgreSQL (quando descomentado)
# POSTGRES_DB=rihs_db
# POSTGRES_USER=rihs_user
# POSTGRES_PASSWORD=rihs_password
```

### 2. Iniciar Todos os Serviços

```bash
docker-compose up -d
```

### 3. Verificar Status

```bash
docker-compose ps
```

### 4. Ver Logs

```bash
# Todos os serviços
docker-compose logs -f

# Apenas API
docker-compose logs -f api

# Apenas Prometheus
docker-compose logs -f prometheus

# Apenas Grafana
docker-compose logs -f grafana
```

## 🔧 Comandos Úteis

### Parar Serviços

```bash
docker-compose down
```

### Parar e Remover Volumes

```bash
docker-compose down -v
```

### Reconstruir Imagens

```bash
docker-compose build --no-cache
docker-compose up -d
```

### Reiniciar um Serviço Específico

```bash
docker-compose restart api
```

### Executar Comandos Dentro de um Container

```bash
# Acessar shell da API
docker-compose exec api /bin/bash

# Acessar shell do Prometheus
docker-compose exec prometheus /bin/sh
```

## 📊 Acessar Serviços

Após iniciar os serviços, você pode acessar:

- **API**: http://localhost:8080
  - Documentação: http://localhost:8080/docs
  - Health Check: http://localhost:8080/health
  - Métricas: http://localhost:8080/metrics

- **Prometheus**: http://localhost:9090
  - Interface web para consultar métricas
  - Targets: http://localhost:9090/targets (verificar se API está sendo coletada)

- **Grafana**: http://localhost:3000
  - Usuário padrão: `admin`
  - Senha padrão: `admin` (altere no primeiro login)
  - Fonte de dados Prometheus já configurada automaticamente

## 🔍 Monitorização

### Verificar Métricas da API no Prometheus

1. Acesse http://localhost:9090
2. Na barra de busca, digite: `http_requests_total`
3. Execute a query para ver métricas da API

### Criar Dashboards no Grafana

1. Acesse http://localhost:3000
2. Faça login com as credenciais configuradas
3. Vá em "Dashboards" > "New Dashboard"
4. Adicione painéis usando a fonte de dados Prometheus
5. Dashboards criados serão salvos em `monitoring/grafana/dashboards/`

### Métricas Disponíveis

A API expõe automaticamente as seguintes métricas via `/metrics`:

- `http_requests_total` - Total de requisições HTTP
- `http_request_duration_seconds` - Duração das requisições
- `http_request_size_bytes` - Tamanho das requisições
- `http_response_size_bytes` - Tamanho das respostas

## 🗄️ Habilitar PostgreSQL (Futuro)

Quando necessário usar PostgreSQL:

1. Descomente as seções `postgres` e `pgadmin` no `docker-compose.yml`
2. Descomente os volumes `postgres-data` e `pgadmin-data`
3. Configure as variáveis de ambiente no `.env`:
   ```
   POSTGRES_DB=rihs_db
   POSTGRES_USER=rihs_user
   POSTGRES_PASSWORD=senha-segura
   PGADMIN_EMAIL=admin@rihs.local
   PGADMIN_PASSWORD=admin
   ```
4. Reinicie os serviços:
   ```bash
   docker-compose up -d
   ```
5. Acesse PgAdmin em http://localhost:5050

## 🛠️ Desenvolvimento

### Modo Desenvolvimento com Hot Reload

Use o `docker-compose.dev.yml` para desenvolvimento:

```bash
docker-compose -f docker-compose.dev.yml up
```

Este arquivo monta o código como volume para hot-reload.

### Testar API Localmente

```bash
# Health check
curl http://localhost:8080/health

# Predição (substitua YOUR_API_KEY)
curl -X POST "http://localhost:8080/predict" \
  -H "X-API-KEY: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "energy_efficiency": 0.8,
    "water_management": 0.7,
    "waste_management": 0.6,
    "renewable_energy": 0.5,
    "local_community_support": 0.9
  }'
```

## 🔒 Segurança

### Produção

Para produção, considere:

1. **Alterar senhas padrão** do Grafana
2. **Usar secrets** para API_KEY e senhas do banco
3. **Restringir CORS** para domínios específicos
4. **Usar HTTPS** com reverse proxy (nginx/traefik)
5. **Limitar recursos** dos containers (já configurado no `docker-compose.prod.yml`)

### Variáveis Sensíveis

Nunca commite o arquivo `.env` no repositório. Use `.env.example` como template:

```bash
cp .env.example .env
# Edite .env com seus valores
```

## 📁 Estrutura de Arquivos

```
.
├── docker-compose.yml          # Configuração principal
├── docker-compose.dev.yml      # Configuração para desenvolvimento
├── docker-compose.prod.yml     # Configuração para produção
├── monitoring/
│   ├── prometheus/
│   │   └── prometheus.yml      # Configuração do Prometheus
│   └── grafana/
│       ├── provisioning/       # Configuração automática do Grafana
│       │   ├── datasources/
│       │   └── dashboards/
│       └── dashboards/         # Dashboards salvos
└── logs/                       # Logs da aplicação
```

## 🐛 Troubleshooting

### API não inicia

```bash
# Verificar logs
docker-compose logs api

# Verificar se o modelo existe
docker-compose exec api ls -la /app/models/latest/

# Verificar variáveis de ambiente
docker-compose exec api env | grep MODEL
```

### Prometheus não coleta métricas

1. Verifique se a API está rodando: `docker-compose ps`
2. Acesse http://localhost:9090/targets
3. Verifique se o target `rihs-api` está "UP"
4. Verifique se ambos estão na mesma rede: `docker network inspect rihs-monitoring`

### Grafana não conecta ao Prometheus

1. Verifique se o Prometheus está rodando: `docker-compose ps prometheus`
2. Verifique o arquivo de configuração: `monitoring/grafana/provisioning/datasources/prometheus.yml`
3. Verifique os logs: `docker-compose logs grafana`

### Porta já em uso

Se alguma porta estiver em uso, altere no `docker-compose.yml`:

```yaml
ports:
  - "8081:8080"  # Mude 8080 para outra porta
```

## 📚 Recursos Adicionais

- [Documentação Docker Compose](https://docs.docker.com/compose/)
- [Documentação Prometheus](https://prometheus.io/docs/)
- [Documentação Grafana](https://grafana.com/docs/)
- [Documentação FastAPI](https://fastapi.tiangolo.com/)

## 🤝 Suporte

Para problemas ou dúvidas, consulte:
- README.md principal do projeto
- DOCKER.md para detalhes sobre o Dockerfile
- Issues no repositório do projeto
