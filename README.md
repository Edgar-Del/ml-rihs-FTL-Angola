# Recomendador Inteligente de Hospedagem Sustentável

API de inferência em FastAPI que classifica o nível de sustentabilidade de hotéis angolanos com base em indicadores ambientais, sociais e económicos. O serviço está pronto para execução em produção com Docker + GCP Cloud Run, autenticação por API key, observabilidade Prometheus e versionamento de modelos com fallback seguro.

---

## Estado Actual do Projecto

**✅ Implementado**

- API FastAPI (`/`, `/health`, `/predict`, `/model/info`, `/metadata`, `/metrics`)
- Normalização ASCII das features e validação obrigatória antes da inferência
- Modelo `scikit-learn` serializado com `joblib` e carregamento resiliente (metadata + fallback)
- Autenticação via header `X-API-KEY` e CORS restrito por domínio
- Métricas Prometheus expostas automaticamente (`prometheus-fastapi-instrumentator`)
- Pipeline de testes (`pytest --cov`) com cobertura mínima de 90%
- Deploy containerizado (Dockerfile) e script oficial `scripts/deploy.sh` para GCP Cloud Run
- Workflow de CI (`.github/workflows/test.yml`) executa lint/test em cada push

**🚧 Próximos Passos**

- Pipeline de dados (Airflow) e tracking de experimentos (MLflow)
- Frontend (Next.js) e dashboards interactivos
- Integração com bases externas e ingestão contínua (TripAdvisor, Booking, EcoBnb)
- Monitorização distribuída (Grafana) e alertas automáticos
- A/B testing de modelos e explainability (SHAP/LIME) expostos via API

---

## Arquitectura Técnica

```
┌───────────────────────────────────────────────────────────────┐
│                       Cliente (seguro)                        │
│   - Painel interno (Next.js) / Integrações B2B                │
│   - Autenticação via X-API-KEY                                │
└───────────────┬───────────────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────────────────┐
│                         FastAPI (app/)                        │
│   • Normalização & validação de payloads                      │
│   • Endpoints REST + métricas Prometheus                      │
│   • Carregamento resiliente de modelos                        │
└───────────────┬────────────────────┬──────────────────────────┘
                │                    │
                │                    │
                ▼                    ▼
    Modelo scikit-learn      Observabilidade & Segurança
   (models/latest/model)     (Prometheus, API Key, CORS)

```

---

## Estrutura de Pastas

```
project_root/
├── core/
│   ├── __init__.py
│   └── settings.py
├── app/
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── utils/
│       ├── __init__.py
│       ├── feature_aliases.py
│       ├── logging.py
│       ├── metrics.py
│       ├── security.py
│       └── validation.py
├── ml/
│   └── model_loader.py
├── models/
│   ├── baseline/model.pkl
│   ├── latest/model.pkl
│   └── metadata.json
├── scripts/
│   ├── deploy.sh
│   └── validate_env.sh
├── tests/
│   ├── conftest.py
│   ├── test_endpoints_extra.py
│   ├── test_health.py
│   ├── test_model.py
│   ├── test_predict.py
│   ├── test_settings.py
│   └── test_utils_misc.py
├── Dockerfile
├── requirements.txt
└── .github/workflows/test.yml
```

---

## Requisitos

- Python 3.10+
- Docker 24+
- Conta GCP com Cloud Run + Cloud Build habilitados

---

## Configuração Local

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Crie um `.env` sem aspas ou colchetes, por exemplo:

```
ENVIRONMENT=dev
MODEL_REGISTRY_PATH=./models/latest/model.pkl
METADATA_FILE=./models/metadata.json
API_KEY=ftl-sustainable-ai-key
CORS_ORIGINS=https://localhost,http://127.0.0.1:3000,https://painel-sustentavel.org
LOG_LEVEL=INFO
APP_NAME=Recomendador Inteligente de Hospedagem Sustentável
VERSION=1.0.0
HOST=0.0.0.0
PORT=8080
DEBUG=false
```

Valide a configuração antes de subir a API:

```bash
./scripts/validate_env.sh
```

---

## Execução

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Endpoints úteis:

- `http://localhost:8000/` – metadata do serviço
- `http://localhost:8000/health` – health check (público)
- `http://localhost:8000/predict` – classificação (requer `X-API-KEY`)
- `http://localhost:8000/metrics` – métricas Prometheus

---

## Testes e Qualidade

```bash
./scripts/validate_env.sh
pytest --cov=app --cov=tests --cov-fail-under=90 --cov-report=term-missing
```

A pipeline de CI (`.github/workflows/test.yml`) executa:

- Validação do `.env`
- Instalação de dependências
- Execução de `pytest` com cobertura ≥90%

---

## Observabilidade

- Métricas HTTP expostas via `/metrics` (Prometheus format)
- Latência, contagem e status por endpoint automaticamente instrumentados
- Logs estruturados via `logging` Python
- Recomendado: configurar `gcloud logging read` ou forward para Stackdriver/Grafana

---

## Deploy em GCP Cloud Run

```bash
# Autentique-se uma vez
gcloud auth login
gcloud auth configure-docker

# Deploy (ambiente dev com tag baseada na data)
./scripts/deploy.sh dev

# Deploy produção com tag fixa
PROJECT_ID=ftl-tourism-ai API_KEY=chave-prod ./scripts/deploy.sh prod v1.2.0
```

O script:

- Usa Cloud Build para criar a imagem
- Publica e faz deploy em Cloud Run com autoscaling controlado
- Injeta `API_KEY`, `MODEL_REGISTRY_PATH` e `METADATA_FILE` como variáveis de ambiente quando necessário
- Valida o health check automaticamente após o deploy

---

## Segurança

- Header obrigatório `X-API-KEY` para endpoints sensíveis (`/predict`, `/model/info`, `/metadata`)
- `API_KEY` nunca é hardcoded: configurável via `.env` ou variável de ambiente
- CORS restrito a `https://painel-sustentavel.org` (configurável pelo ambiente)
- Recomenda-se utilizar Secret Manager na infraestrutura final

---

## Versionamento de Modelos

- `MODEL_REGISTRY_PATH` aponta para o artefacto activo (padrão `models/latest/model.pkl`)
- `ml/model_loader.py` fornece fallback automático para `models/baseline/model.pkl`
- `models/metadata.json` armazena métricas e metadados consumidos pelos endpoints
- `/metadata` expõe a versão e métricas carregadas, permitindo observabilidade

---

## Roadmap Futuro

- **Dados & Orquestração**: Airflow, pipelines incrementais e DVC para datasets
- **Experimentação**: MLflow registry, comparação automática e aprovação de modelos
- **Explainability**: Geração de SHAP/LIME com endpoint específico
- **Infraestrutura**: Terraform para infra como código, Grafana dashboards, alertas PagerDuty
- **Produto**: Recomendador personalizado com preferências do utilizador final

---

## Contribuição

1. Crie um fork do repositório
2. Abra uma branch (`git checkout -b feat/nova-funcionalidade`)
3. Garanta que `pytest --cov` passa
4. Abra um Pull Request com descrição detalhada

---

## Equipa

**Grupo 1 - Bootcamp Frontier Tech Leaders UNDP Angola 2025**

- Arsénio Eurico Muassangue
- Edgar Delfino Tchissingui
- Francisco Adão Vika Manuel
- Raquel de Jesus João

---

## Referências

- UNWTO (2023) – Tourism for Development
- UNDP (2022) – Tourism and Sustainable Development Goals
- UNEP (2021) – Making Tourism More Sustainable
