# 🏨 Recomendador Inteligente de Hospedagem Sustentável (RIHS)

> **API de classificação de sustentabilidade para hotéis angolanos**  
> Alinhado aos ODS 8, 12 e 13 | Bootcamp Frontier Tech Leaders UNDP Angola 2025

[![Deployment Status](https://img.shields.io/badge/deployment-production-brightgreen)](https://rihs-ftl-undp.ew.r.appspot.com/)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**🌐 Deployment em Produção:** [https://rihs-ftl-undp.ew.r.appspot.com/](https://rihs-ftl-undp.ew.r.appspot.com/)

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Sobre o Projeto](#-sobre-o-projeto)
- [Objectivos de Desenvolvimento Sustentável](#-objectivos-de-desenvolvimento-sustentável)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura Técnica](#-arquitetura-técnica)
- [Casos de Uso Práticos](#-casos-de-uso-práticos)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Uso da API](#-uso-da-api)
- [Deployment](#-deployment)
- [Testes](#-testes)
- [Documentação](#-documentação)
- [Impacto e Contribuições](#-impacto-e-contribuições)
- [Equipa](#-equipa)
- [Referências](#-referências)

---

## 🎯 Visão Geral

O **Recomendador Inteligente de Hospedagem Sustentável (RIHS)** é uma API inteligente baseada em Machine Learning que classifica o nível de sustentabilidade de hotéis angolanos com base em indicadores ambientais, sociais e económicos. O sistema utiliza técnicas avançadas de IA para processar dados multiestruturados e fornecer recomendações personalizadas que promovem o turismo sustentável e consciente.

### 🚀 Características Principais

- ✅ **Classificação Automática** de sustentabilidade usando modelos de ML (XGBoost, Random Forest)
- ✅ **API RESTful** completa com FastAPI e documentação automática
- ✅ **Autenticação Segura** via API Key
- ✅ **Observabilidade** integrada com Prometheus
- ✅ **Deployment em Produção** no Google Cloud Platform
- ✅ **Containerização** com Docker e Docker Compose
- ✅ **Testes Automatizados** com cobertura ≥90%
- ✅ **Versionamento de Modelos** com fallback seguro

---

## 📖 Sobre o Projeto

### Contextualização do Problema

O sector do turismo em Angola representa uma das maiores oportunidades de diversificação económica e desenvolvimento sustentável do país. Contudo, o modelo actual de hospitalidade enfrenta um problema estrutural: **a invisibilidade dos alojamentos sustentáveis** que praticam gestão ambiental responsável, mas permanecem fora dos grandes circuitos digitais.

Em plataformas internacionais como Booking ou TripAdvisor, a maioria dos estabelecimentos é avaliada apenas com base em preço, conforto ou localização, **sem considerar indicadores de sustentabilidade** (uso de energia limpa, gestão de resíduos, impacto social local). Isso gera uma lacuna crítica: os viajantes conscientes não conseguem identificar facilmente opções verdes, enquanto empreendedores comprometidos com práticas ecológicas têm pouca visibilidade e reconhecimento.

### Justificativa

A proposta do RIHS responde directamente às metas dos **Objectivos de Desenvolvimento Sustentável (ODS)**:

- **ODS 8** — Trabalho Decente e Crescimento Económico: promove visibilidade de alojamentos sustentáveis e fomenta microempreendimentos locais
- **ODS 12** — Consumo e Produção Responsáveis: incentiva consumo consciente, orientando viajantes para hospedagens responsáveis
- **ODS 13** — Acção Climática: destaca opções de baixa pegada de carbono e incentiva energias limpas

### Objectivo Geral

Desenvolver um sistema inteligente de recomendação, baseado em machine learning supervisionado, que identifique, classifique e recomende hospedagens sustentáveis em Angola, promovendo práticas ecológicas, consumo responsável e turismo consciente.

---

## 🌍 Objectivos de Desenvolvimento Sustentável

Este projeto está alinhado com os seguintes ODS:

| ODS | Descrição | Contribuição do Projeto |
|-----|-----------|------------------------|
| **ODS 8** | Trabalho Decente e Crescimento Económico | Promove visibilidade de alojamentos sustentáveis, cria empregos verdes e fomenta microempreendimentos locais |
| **ODS 12** | Consumo e Produção Responsáveis | Orienta viajantes para hospedagens que adoptam práticas responsáveis no uso de recursos naturais |
| **ODS 13** | Acção Climática | Destaca opções de baixa pegada de carbono e contribui para mitigação das emissões no sector turístico |

---

## ✨ Funcionalidades

### Endpoints Disponíveis

| Endpoint | Método | Descrição | Autenticação |
|----------|--------|-----------|--------------|
| `/` | GET | Metadata do serviço | Público |
| `/health` | GET | Health check | Público |
| `/docs` | GET | Documentação interativa (Swagger UI) | Público |
| `/redoc` | GET | Documentação alternativa (ReDoc) | Público |
| `/predict` | POST | Classificação de sustentabilidade | Requer API Key |
| `/model/info` | GET | Informações sobre o modelo carregado | Requer API Key |
| `/metadata` | GET | Metadados do modelo | Requer API Key |
| `/metrics` | GET | Métricas Prometheus | Público |

### Características Técnicas

- 🔒 **Autenticação**: Header `X-API-KEY` obrigatório para endpoints sensíveis
- 📊 **Métricas**: Exposição automática de métricas Prometheus
- 🔄 **Versionamento**: Sistema de fallback para modelos (latest → baseline)
- ✅ **Validação**: Validação rigorosa de payloads com Pydantic
- 🌐 **CORS**: Configurável por ambiente
- 📝 **Logging**: Logs estruturados com níveis configuráveis

---

## 🏗️ Arquitetura Técnica

```
┌───────────────────────────────────────────────────────────────┐
│                       Cliente (seguro)                        │
│   - Plataformas de reserva (Booking, Airbnb)                  │
│   - Aplicativos de viagem (TripAdvisor, Google Travel)        │
│   - Órgãos governamentais e certificadoras                    │
│   - Autenticação via X-API-KEY                                │
└───────────────┬───────────────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────────────────┐
│                         FastAPI (app/)                        │
│   • Normalização & validação de payloads                      │
│   • Endpoints REST + métricas Prometheus                      │
│   • Carregamento resiliente de modelos                        │
│   • Autenticação e autorização                                │
└───────────────┬────────────────────┬──────────────────────────┘
                │                    │
                │                    │
                ▼                    ▼
    Modelo scikit-learn      Observabilidade & Segurança
   (models/latest/model)     (Prometheus, API Key, CORS)
```

### Stack Tecnológico

**Backend:**
- Python 3.11
- FastAPI 0.104
- Uvicorn (ASGI server)
- Pydantic (validação de dados)

**Machine Learning:**
- scikit-learn 1.4.0
- XGBoost 2.0.3
- NumPy 1.26.4
- Pandas 2.3.3
- joblib (serialização de modelos)

**Observabilidade:**
- Prometheus Client
- prometheus-fastapi-instrumentator

**Infraestrutura:**
- Docker & Docker Compose
- Google Cloud Platform (Cloud Run)
- Cloud Build

---

## 💼 Casos de Uso Práticos

### 1. 🏨 Plataformas de Reserva Online

**Exemplo:** Booking.com, Airbnb, Decolar.com

**Caso de Uso:** Classificar automaticamente a sustentabilidade de hospedagens

**API Request:**
```json
{
  "energy_efficiency": 0.8,
  "water_management": 0.7,
  "waste_management": 0.6,
  "renewable_energy": 0.5,
  "local_community_support": 0.9
}
```

**API Response:**
```json
{
  "prediction": 2,
  "prediction_label": "MUITO_ALTO",
  "confidence": 87.5,
  "probabilities": {
    "MUITO_BAIXO": 0.02,
    "BAIXO": 0.05,
    "MÉDIO": 0.08,
    "ALTO": 0.15,
    "MUITO_ALTO": 0.70
  }
}
```

### 2. 🏛️ Órgãos Governamentais e Certificadoras

**Exemplo:** Ministério do Turismo, CERTIFIQUE Sustainable

**Caso de Uso:** Avaliação automatizada para certificações verdes

**Uso Prático:**
- Validar automaticamente critérios de sustentabilidade
- Reduzir custos de auditoria presencial
- Escalar programa de certificações
- Monitorar contínuo de hotéis já certificados

### 3. 📊 Agências de Desenvolvimento Regional

**Exemplo:** EMBRATUR, Secretarias Estaduais de Turismo

**Caso de Uso:** Mapeamento do perfil sustentável do destino

**Aplicação:**
- Criar ranking regional de sustentabilidade hoteleira
- Identificar clusters de excelência ambiental
- Direcionar políticas públicas e incentivos
- Desenvolver rotas turísticas sustentáveis

### 4. 🏢 Redes Hoteleiras

**Exemplo:** Marriott, Hilton, Accor

**Caso de Uso:** Benchmarking interno e melhoria contínua

**Implementação:**
- Comparar desempenho entre unidades da rede
- Identificar melhores práticas internas
- Definir metas de sustentabilidade mensuráveis
- Reportar ESG para investidores

### 5. 🌱 Startups de Turismo Sustentável

**Exemplo:** Ecobnb, Responsible Travel

**Caso de Uso:** Diferenciação no mercado

**Valor:**
- Oferecer filtro "verdadeiramente sustentável"
- Validar claims de marketing verde
- Construir confiança com o consumidor
- Atrair turistas conscientes

### 6. 📱 Aplicativos de Viagem

**Exemplo:** TripAdvisor, Google Travel

**Caso de Uso:** Integração como feature premium

**Funcionalidade:**
- Badge de sustentabilidade nos perfis
- Sistema de scoring ambiental
- Recomendações personalizadas por perfil eco
- Gamificação (pontos por escolhas sustentáveis)

### 7. 🎓 Projeto Acadêmico/Educacional

**Caso de Uso:** Demonstração prática de ML aplicado

- Portfólio técnico para oportunidades profissionais
- Case study completo: coleta, treino, deploy, monitoramento
- Base para pesquisas acadêmicas em turismo sustentável
- Material para workshops e palestras

### 8. 📈 Consultorias Especializadas

**Caso de Uso:** Ferramenta para consultorias em sustentabilidade

- Avaliação rápida de clientes hoteleiros
- Data-driven insights para recomendações
- Relatórios automatizados de desempenho
- Análise comparativa do mercado

---

## 🛠️ Tecnologias Utilizadas

### Core
- **Python 3.11** - Linguagem principal
- **FastAPI 0.104** - Framework web assíncrono
- **Uvicorn** - Servidor ASGI de alta performance

### Machine Learning
- **scikit-learn 1.4.0** - Modelos de ML
- **XGBoost 2.0.3** - Gradient boosting
- **NumPy 1.26.4** - Computação numérica
- **Pandas 2.3.3** - Manipulação de dados
- **joblib** - Serialização de modelos

### Validação e Schemas
- **Pydantic 2.5.0** - Validação de dados
- **pydantic-settings** - Gestão de configurações

### Observabilidade
- **Prometheus Client** - Métricas
- **prometheus-fastapi-instrumentator** - Instrumentação automática

### Infraestrutura
- **Docker** - Containerização
- **Docker Compose** - Orquestração local
- **Google Cloud Platform** - Cloud hosting
- **Cloud Run** - Serverless deployment

### Desenvolvimento
- **pytest** - Framework de testes
- **pytest-cov** - Cobertura de código
- **GitHub Actions** - CI/CD

---

## 📁 Estrutura do Projeto

```
FinalProjectFTL/
├── app/                          # Aplicação principal
│   ├── __init__.py
│   ├── main.py                   # Ponto de entrada FastAPI
│   ├── config.py                 # Configurações (compatibilidade)
│   ├── models.py                 # Modelo de ML (SustainabilityModel)
│   ├── schemas.py                # Schemas Pydantic
│   └── utils/                    # Utilitários
│       ├── __init__.py
│       ├── feature_aliases.py   # Aliases de features
│       ├── logging.py            # Configuração de logs
│       ├── metrics.py            # Métricas Prometheus
│       ├── security.py            # Autenticação (API Key)
│       └── validation.py         # Validação de features
│
├── core/                          # Configurações centrais
│   ├── __init__.py
│   └── settings.py               # Settings com Pydantic
│
├── ml/                            # Módulos de ML
│   └── model_loader.py           # Carregamento de modelos
│
├── models/                        # Modelos treinados
│   ├── baseline/                 # Modelo baseline (fallback)
│   │   └── model.pkl
│   ├── latest/                   # Modelo mais recente
│   │   └── sustainability_classification_pipeline.pkl
│   └── metadata.json            # Metadados do modelo
│
├── tests/                         # Testes automatizados
│   ├── __init__.py
│   ├── conftest.py              # Configuração pytest
│   ├── test_endpoints_extra.py
│   ├── test_health.py
│   ├── test_model.py
│   ├── test_predict.py
│   ├── test_settings.py
│   └── test_utils_misc.py
│
├── scripts/                       # Scripts utilitários
│   ├── deploy.sh                # Deploy para GCP
│   ├── test_api.sh              # Testes de API
│   ├── test_api_local.sh
│   └── validate_env.sh          # Validação de ambiente
│
├── monitoring/                    # Configuração de monitorização
│   ├── prometheus/
│   │   └── prometheus.yml
│   └── grafana/
│       ├── provisioning/
│       └── dashboards/
│
├── Dockerfile                     # Imagem Docker
├── docker-entrypoint.sh          # Script de entrada
├── docker-compose.yml            # Compose para produção
├── docker-compose.dev.yml        # Compose para desenvolvimento
├── docker-compose.prod.yml       # Compose para produção
├── .dockerignore                 # Arquivos ignorados no Docker
├── requirements.txt              # Dependências Python
├── cloudbuild.yaml               # Cloud Build config
├── app.yaml                      # App Engine config (GCP)
├── .gcloudignore                 # Arquivos ignorados no GCP
├── Makefile                      # Comandos úteis
├── README.md                      # Este arquivo
├── DOCKER.md                      # Documentação Docker
└── DOCKER_COMPOSE.md             # Documentação Docker Compose
```

---

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.11 ou superior
- Docker 24+ (opcional, para containerização)
- Conta Google Cloud Platform (para deployment)
- Git

### Instalação Local

1. **Clone o repositório:**
```bash
git clone <repository-url>
cd FinalProjectFTL
```

2. **Crie um ambiente virtual:**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**

Crie um arquivo `.env` na raiz do projeto:

```env
# Configurações obrigatórias
API_KEY=seu-api-key-aqui
PORT=8080
ENVIRONMENT=dev

# Caminhos dos modelos
MODEL_REGISTRY_PATH=./models/latest/sustainability_classification_pipeline.pkl
METADATA_FILE=./models/metadata.json

# CORS
CORS_ORIGINS=*

# Logging
LOG_LEVEL=INFO
DEBUG=false

# Aplicação
APP_NAME=Recomendador Inteligente de Hospedagem Sustentável
VERSION=1.0.0
HOST=0.0.0.0
```

5. **Valide a configuração:**
```bash
chmod +x scripts/validate_env.sh
./scripts/validate_env.sh
```

### Execução Local

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

A API estará disponível em:
- **API:** http://localhost:8080
- **Documentação:** http://localhost:8080/docs
- **Health Check:** http://localhost:8080/health

### Execução com Docker

```bash
# Build da imagem
docker build -t rihs-api:latest .

# Execução
docker run -d \
  --name rihs-api \
  -p 8080:8080 \
  --env-file .env \
  rihs-api:latest
```

### Execução com Docker Compose

```bash
# Produção
docker-compose up -d

# Desenvolvimento (com hot-reload)
docker-compose -f docker-compose.dev.yml up
```

---

## 📡 Uso da API

### Exemplo de Requisição

**Endpoint:** `POST /predict`

**Headers:**
```
Content-Type: application/json
X-API-KEY: seu-api-key-aqui
```

**Body:**
```json
{
  "energy_efficiency": 0.8,
  "water_management": 0.7,
  "waste_management": 0.6,
  "renewable_energy": 0.5,
  "local_community_support": 0.9
}
```

**Resposta:**
```json
{
  "prediction": 2,
  "prediction_label": "MUITO_ALTO",
  "confidence": 87.5,
  "probabilities": {
    "MUITO_BAIXO": 0.02,
    "BAIXO": 0.05,
    "MÉDIO": 0.08,
    "ALTO": 0.15,
    "MUITO_ALTO": 0.70
  }
}
```

### Teste com cURL

```bash
curl -X POST "https://rihs-ftl-undp.ew.r.appspot.com/predict" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: seu-api-key" \
  -d '{
    "energy_efficiency": 0.8,
    "water_management": 0.7,
    "waste_management": 0.6,
    "renewable_energy": 0.5,
    "local_community_support": 0.9
  }'
```

### Teste com Python

```python
import requests

url = "https://rihs-ftl-undp.ew.r.appspot.com/predict"
headers = {
    "Content-Type": "application/json",
    "X-API-KEY": "seu-api-key"
}
data = {
    "energy_efficiency": 0.8,
    "water_management": 0.7,
    "waste_management": 0.6,
    "renewable_energy": 0.5,
    "local_community_support": 0.9
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

---

## ☁️ Deployment

### Google Cloud Platform (Cloud Run)

O projeto está deployado em produção no GCP Cloud Run:

**🌐 URL de Produção:** [https://rihs-ftl-undp.ew.r.appspot.com/](https://rihs-ftl-undp.ew.r.appspot.com/)

#### Deploy Manual

```bash
# Autenticação
gcloud auth login
gcloud auth configure-docker

# Deploy usando script
./scripts/deploy.sh prod v1.0.0
```

#### Deploy com Cloud Build

O projeto inclui `cloudbuild.yaml` para builds automatizados:

```bash
gcloud builds submit --config cloudbuild.yaml
```

### Variáveis de Ambiente em Produção

Configure as seguintes variáveis no Cloud Run:

- `API_KEY` - Chave de API (use Secret Manager)
- `MODEL_REGISTRY_PATH` - Caminho do modelo
- `METADATA_FILE` - Caminho dos metadados
- `CORS_ORIGINS` - Origens permitidas
- `LOG_LEVEL` - Nível de log (INFO, DEBUG, etc.)

---

## 🧪 Testes

### Executar Testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=app --cov=tests --cov-fail-under=90 --cov-report=term-missing

# Testes específicos
pytest tests/test_predict.py -v
```

### Cobertura Mínima

O projeto mantém **cobertura mínima de 90%** em todos os módulos principais.

### CI/CD

O projeto inclui GitHub Actions (`.github/workflows/test.yml`) que executa:

- Validação do ambiente
- Instalação de dependências
- Execução de testes com cobertura
- Validação de linting

---

## 📚 Documentação

### Documentação da API

A documentação interativa está disponível em:

- **Swagger UI:** `/docs`
- **ReDoc:** `/redoc`

### Documentação Adicional

- **[DOCKER.md](DOCKER.md)** - Guia completo de Docker
- **[DOCKER_COMPOSE.md](DOCKER_COMPOSE.md)** - Guia de Docker Compose

### Exemplos

Consulte `exemplos.json` para exemplos de payloads de requisição.

---

## 🌟 Impacto e Contribuições

### Impacto Social

- ✅ Fomenta consciência ecológica entre turistas
- ✅ Valoriza empreendimentos locais comprometidos com práticas verdes
- ✅ Fortalece comunidades e gera empregos decentes
- ✅ Incentiva formação e certificação de alojamentos sustentáveis

### Impacto Económico

- ✅ Aumenta procura por hospedagens sustentáveis
- ✅ Impulsiona micro e pequenas empresas do sector hoteleiro
- ✅ Estimula turismo interno e rural baseado em sustentabilidade
- ✅ Apoia políticas públicas de incentivo ao turismo verde

### Impacto Ambiental

- ✅ Reduz indirectamente a pegada de carbono do turismo
- ✅ Estimula adopção de práticas de eficiência energética
- ✅ Promove reciclagem e gestão de resíduos
- ✅ Contribui para preservação de ecossistemas locais

### Contribuições Futuras

O projeto está aberto a contribuições! Áreas de interesse:

- Melhorias no modelo de ML
- Novos endpoints e funcionalidades
- Integração com mais fontes de dados
- Melhorias na documentação
- Testes adicionais

---

## 👥 Equipa

**Grupo 1 - Bootcamp Frontier Tech Leaders UNDP Angola 2025**

| Nome | Contribuição |
|------|--------------|
| **Arsénio Eurico Muassangue** | Desenvolvimento e implementação |
| **Edgar Delfino Tchissingui** | Desenvolvimento e implementação |
| **Francisco Adão Vika Manuel** | Desenvolvimento e implementação |
| **Raquel de Jesus João** | Desenvolvimento e implementação |

---

## 📚 Referências

### Organizações Internacionais

- **UNWTO (2023)** – Tourism for Development
- **UNDP (2022)** – Tourism and Sustainable Development Goals
- **UNEP (2021)** – Making Tourism More Sustainable

### Artigos Científicos

- Iorgulescu, M.-C. (2020). An Insight Into Green Practices and Eco-Labels in the Hotel Industry
- Mzembe, A., et al. (2023). Analysis of integration of sustainability in sustainability certifications in the hotel industry
- Choi, H. M., Kim, W. G., & Kim, Y. J. (2019). Hotel environmental management initiative (HEMI) scale development
- Banerjee, A., et al. (2025). SynthTRIPs: A Knowledge-Grounded Framework for Benchmark Query Generation
- Kumari, M., et al. (2024). Sustainability in tourism and hospitality: Artificial intelligence role in eco-friendly practices

### Relatórios e Políticas

- UNWTO & GSTC (2024). Sustainable Hospitality Trends – Accommodation Sector Report
- African Development Bank (2022). Tourism in Africa: Harnessing the Potential
- World Travel & Tourism Council (2020). Net Zero Carbon Roadmap
- International Labour Organization (2021). Green Jobs in Tourism – A Global Report

---

## 📄 Licença

Este projeto foi desenvolvido como parte do **Bootcamp Frontier Tech Leaders UNDP Angola 2025**.

---

## 🔗 Links Úteis

- **🌐 API em Produção:** [https://rihs-ftl-undp.ew.r.appspot.com/](https://rihs-ftl-undp.ew.r.appspot.com/)
- **📖 Documentação da API:** [https://rihs-ftl-undp.ew.r.appspot.com/docs](https://rihs-ftl-undp.ew.r.appspot.com/docs)
- **🏥 Health Check:** [https://rihs-ftl-undp.ew.r.appspot.com/health](https://rihs-ftl-undp.ew.r.appspot.com/health)

---

## 🙏 Agradecimentos

Agradecemos ao **UNDP Angola** e ao programa **Frontier Tech Leaders** pela oportunidade de desenvolver este projeto e contribuir para o desenvolvimento sustentável do turismo em Angola.

---

**Desenvolvido com ❤️ para promover turismo sustentável em Angola**

*Última atualização: 2025*
