from contextlib import asynccontextmanager
import logging
from pathlib import Path

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.openapi.utils import get_openapi

from core.settings import settings
from app.models import SustainabilityModel
from app.schemas import (
    PredictionInput,
    PredictionOutput,
    HealthResponse,
    ModelInfoResponse,
    ErrorResponse,
)
from app.utils import (
    init_metrics,
    normalize_features,
    validate_feature_payload,
    verify_api_key,
)

# Configura logging
LOG_LEVEL = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

model = SustainabilityModel()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação (startup/shutdown)."""
    logger.info(f"Iniciando {settings.APP_NAME} v{settings.VERSION}")
    
    # Só tenta carregar o modelo se ainda não estiver carregado (útil para testes)
    if not model.is_loaded():
        success = model.load(
            model_path=settings.MODEL_REGISTRY_PATH,
            metadata_path=settings.METADATA_FILE,
        )
        if success:
            logger.info("Modelo carregado com sucesso")
        else:
            logger.error("Falha ao carregar o modelo")
    else:
        logger.info("Modelo já estava carregado (provavelmente injectado para testes)")
    
    if settings.API_KEY is None:
        logger.warning("API_KEY não configurada. Endpoints protegidos irão retornar erro 500.")
    yield
    # teardown (se necessário)


# Cria aplicação FastAPI com documentação completa
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="""
    ## 🏨 Recomendador Inteligente de Hospedagem Sustentável (RIHS)
    
    API de classificação de sustentabilidade para hotéis angolanos baseada em Machine Learning.
    
    ### 📋 Sobre o Projeto
    
    Esta API utiliza modelos de Machine Learning (XGBoost, Random Forest) para classificar
    o nível de sustentabilidade de estabelecimentos hoteleiros com base em indicadores
    ambientais, sociais e económicos.
    
    ### 🔐 Autenticação
    
    A maioria dos endpoints requer autenticação via **API Key**. Inclua o header:
    ```
    X-API-KEY: sua-chave-api-aqui
    ```
    
    ### 📊 Classificações
    
    O modelo classifica hotéis em 5 níveis de sustentabilidade:
    - **0 - Muito Baixo**: Práticas sustentáveis mínimas ou inexistentes
    - **1 - Baixo**: Algumas práticas sustentáveis básicas
    - **2 - Médio**: Práticas sustentáveis moderadas
    - **3 - Alto**: Boas práticas sustentáveis implementadas
    - **4 - Muito Alto**: Excelência em práticas sustentáveis
    
    ### 🌍 Objectivos de Desenvolvimento Sustentável
    
    Este projeto está alinhado com os ODS 8, 12 e 13 da ONU.
    
    ### 📚 Documentação Adicional
    
    - **README:** Consulte o README.md para informações completas do projeto
    - **Docker:** Veja DOCKER.md para instruções de containerização
    - **Deployment:** API disponível em produção: https://rihs-ftl-undp.ew.r.appspot.com/
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    contact={
        "name": "FTL Grupo-01",
        "url": "https://github.com/Edgar-Del/ml-rihs-FTL-Angola",
    },
    license_info={
        "name": "MIT",
    },
    tags_metadata=[
        {
            "name": "Informação",
            "description": "Endpoints públicos de informação sobre a API e estado do serviço.",
        },
        {
            "name": "Classificação",
            "description": "Endpoints para classificação de sustentabilidade de hotéis. Requerem autenticação.",
        },
        {
            "name": "Modelo",
            "description": "Endpoints para obter informações sobre o modelo de ML. Requerem autenticação.",
        },
        {
            "name": "Monitorização",
            "description": "Endpoints para monitorização e métricas do sistema.",
        },
    ],
)

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

init_metrics(app)


@app.get(
    "/",
    tags=["Informação"],
    summary="Informações da API",
    description="Retorna informações básicas sobre a API, incluindo nome, versão e link para documentação.",
    response_description="Informações da API",
)
async def root():
    """
    Endpoint raiz que retorna informações básicas sobre a API.
    
    Este endpoint não requer autenticação e pode ser usado para verificar
    se a API está acessível e obter informações sobre a versão.
    """
    return {
        "message": f"Bem-vindo ao {settings.APP_NAME}",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health",
        "description": "API de classificação de sustentabilidade para hotéis angolanos",
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Informação"],
    summary="Health Check",
    description="Verifica o estado de saúde da API e se o modelo de ML está carregado e pronto para uso.",
    response_description="Estado de saúde da API",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "API está operacional",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "model_loaded": True,
                        "version": "1.0.0"
                    }
                }
            }
        },
        503: {
            "description": "API não está saudável ou modelo não carregado",
            "model": ErrorResponse,
        }
    },
)
async def health_check():
    """
    Health check para monitoramento da API.
    
    Este endpoint verifica:
    - Se a API está respondendo
    - Se o modelo de ML está carregado e pronto para uso
    
    **Uso típico:**
    - Monitorização de saúde em sistemas de orquestração (Kubernetes, Cloud Run)
    - Verificação de disponibilidade antes de fazer requisições
    - Alertas e notificações de sistema
    
    **Respostas:**
    - `status: "healthy"` - API e modelo estão operacionais
    - `status: "unhealthy"` - Modelo não está carregado ou há problemas
    """
    return HealthResponse(
        status="healthy" if model.is_loaded() else "unhealthy",
        model_loaded=model.is_loaded(),
        version=settings.VERSION
    )


@app.get(
    "/metrics",
    tags=["Monitorização"],
    summary="Métricas Prometheus",
    description="Expõe métricas do Prometheus para monitorização do sistema.",
    response_description="Métricas no formato Prometheus",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Métricas disponíveis",
            "content": {
                "text/plain": {
                    "example": "# HELP http_requests_total Total number of HTTP requests\n# TYPE http_requests_total counter\nhttp_requests_total{method=\"GET\",status=\"200\"} 42.0"
                }
            }
        },
        501: {
            "description": "Métricas não disponíveis (prometheus-client não instalado)",
            "model": ErrorResponse,
        }
    },
)
async def metrics():
    """
    Endpoint para métricas do Prometheus.
    
    Expõe métricas HTTP automáticas coletadas pelo `prometheus-fastapi-instrumentator`,
    incluindo:
    - Contagem de requisições por endpoint e método
    - Latência de requisições
    - Tamanho de requisições e respostas
    - Status codes
    
    **Formato:** Text/plain (formato Prometheus)
    
    **Uso:**
    Configure o Prometheus para fazer scraping deste endpoint:
    ```yaml
    scrape_configs:
      - job_name: 'rihs-api'
        metrics_path: '/metrics'
        static_configs:
          - targets: ['api:8080']
    ```
    """
    try:
        from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
        return Response(
            generate_latest(),
            media_type=CONTENT_TYPE_LATEST
        )
    except ImportError:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Métricas não disponíveis (prometheus-client não instalado)"
        )


@app.post(
    "/predict",
    response_model=PredictionOutput,
    tags=["Classificação"],
    summary="Classificar Sustentabilidade",
    description="""
    Classifica o nível de sustentabilidade de um hotel com base em indicadores ambientais, sociais e económicos.
    
    Este é o endpoint principal da API. Recebe características do hotel e retorna:
    - A classe predita (0-4)
    - Probabilidades para todas as classes
    - Confiança da predição
    - Rótulo textual da classificação
    """,
    response_description="Resultado da classificação de sustentabilidade",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Classificação realizada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "prediction": 3,
                        "probabilities": [0.02, 0.05, 0.08, 0.15, 0.70],
                        "prediction_label": "Alto",
                        "confidence": 70.0,
                        "all_probabilities": {
                            "Muito Baixo": 0.02,
                            "Baixo": 0.05,
                            "Médio": 0.08,
                            "Alto": 0.15,
                            "Muito Alto": 0.70
                        },
                        "model_version": "1.0.0"
                    }
                }
            }
        },
        400: {
            "description": "Dados de entrada inválidos (valores fora do intervalo, campos faltando, etc.)",
            "model": ErrorResponse,
        },
        401: {
            "description": "API Key não fornecida ou inválida",
            "model": ErrorResponse,
        },
        403: {
            "description": "Acesso negado (API Key incorreta)",
            "model": ErrorResponse,
        },
        503: {
            "description": "Modelo não disponível ou não carregado",
            "model": ErrorResponse,
        },
        500: {
            "description": "Erro interno do servidor",
            "model": ErrorResponse,
        }
    },
    dependencies=[Depends(verify_api_key)],
)
async def predict(input_data: PredictionInput):
    """
    Endpoint para classificar sustentabilidade de hotel.
    
    Recebe as características do hotel e retorna a classificação
    de sustentabilidade com probabilidades para todas as classes.
    
    ### 📥 Entrada
    
    O payload deve conter **todos** os 24 campos obrigatórios:
    - Indicadores económicos: `price_per_night_usd`, `rating`, `avaliação_clientes`
    - Indicadores ambientais: `energia_renovável`, `carbon_footprint_score`, `reciclagem_score`
    - Indicadores sociais: `sentimento_score`, `eco_keyword_count`
    - Índices compostos: `sustainability_index`, `eco_impact_index`, `total_sust_score`
    - E outros indicadores relevantes
    
    ### 📤 Saída
    
    Retorna:
    - **prediction**: Código numérico da classe (0-4)
    - **prediction_label**: Nome da classe ("Muito Baixo" a "Muito Alto")
    - **confidence**: Confiança da predição em percentagem
    - **probabilities**: Lista de probabilidades para cada classe
    - **all_probabilities**: Dicionário com probabilidades mapeadas por nome
    - **model_version**: Versão do modelo utilizado
    
    ### 🔒 Autenticação
    
    Requer header `X-API-KEY` com uma chave válida.
    
    ### ⚠️ Validação
    
    Todos os campos são validados:
    - Tipos de dados devem estar corretos
    - Valores devem estar dentro dos intervalos permitidos
    - Campos obrigatórios não podem estar ausentes
    
    ### 📊 Exemplo de Uso
    
    ```python
    import requests
    
    url = "https://rihs-ftl-undp.ew.r.appspot.com/predict"
    headers = {"X-API-KEY": "sua-chave-api"}
    data = {
        "price_per_night_usd": 150.0,
        "rating": 4.5,
        # ... todos os outros campos
    }
    
    response = requests.post(url, json=data, headers=headers)
    result = response.json()
    print(f"Classificação: {result['prediction_label']}")
    print(f"Confiança: {result['confidence']}%")
    ```
    """
    try:
        model_path = Path(settings.MODEL_REGISTRY_PATH)
        fallback_path = getattr(model, "loaded_path", None)
        if not model_path.exists() and not (fallback_path and Path(fallback_path).exists()):
            logger.error("Modelo indisponível em %s", model_path)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Model unavailable"
            )

        if not settings.API_KEY:
            logger.error("API key não configurada no servidor")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="API key missing"
            )

        if not model.is_loaded():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Modelo não carregado"
            )
        
        features = normalize_features(input_data.to_feature_dict())
        validate_feature_payload(features)

        # Faz predição
        prediction_result = model.predict(features)
        
        logger.info(
            f"Predição realizada: {prediction_result['prediction_label']} "
            f"(classe {prediction_result['prediction']}) com "
            f"{prediction_result['confidence']}% de confiança"
        )
        
        return PredictionOutput(**prediction_result)
    except HTTPException as http_exc:
        # Propaga HTTPException sem mascarar o status code
        raise http_exc
    except ValueError as err:
        logger.warning("Payload inválido recebido: %s", err)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        ) from err
    except Exception as e:
        logger.error(f"Erro no endpoint /predict: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@app.get(
    "/model/info",
    response_model=ModelInfoResponse,
    tags=["Modelo"],
    summary="Informações do Modelo",
    description="Retorna informações detalhadas sobre o modelo de ML carregado, incluindo features, classes e metadados.",
    response_description="Informações do modelo",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Informações do modelo disponíveis",
            "content": {
                "application/json": {
                    "example": {
                        "model_loaded": True,
                        "feature_names": ["price_per_night_usd", "rating", "sustainability_index"],
                        "class_labels": {
                            "0": "Muito Baixo",
                            "1": "Baixo",
                            "2": "Médio",
                            "3": "Alto",
                            "4": "Muito Alto"
                        },
                        "version": "1.0.0",
                        "metadata": {
                            "accuracy": 0.92,
                            "f1_weighted": 0.91
                        }
                    }
                }
            }
        },
        401: {
            "description": "API Key não fornecida",
            "model": ErrorResponse,
        },
        403: {
            "description": "Acesso negado",
            "model": ErrorResponse,
        },
        503: {
            "description": "Modelo não carregado",
            "model": ErrorResponse,
        }
    },
    dependencies=[Depends(verify_api_key)],
)
async def model_info():
    """
    Retorna informações detalhadas sobre o modelo de ML.
    
    Este endpoint fornece:
    - Lista de features utilizadas pelo modelo
    - Mapeamento de classes (código -> rótulo)
    - Versão do modelo
    - Metadados adicionais (métricas de performance, data de treino, etc.)
    
    **Uso típico:**
    - Verificar quais features são necessárias para fazer predições
    - Entender as classes de classificação disponíveis
    - Verificar métricas de performance do modelo
    - Debugging e desenvolvimento
    
    ### 🔒 Autenticação
    
    Requer header `X-API-KEY` com uma chave válida.
    """
    if not model.is_loaded():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modelo não carregado"
        )
    
    # Converte class_labels de Dict[int, str] para Dict[str, str]
    class_labels_dict = {str(k): v for k, v in model.class_labels.items()}
    
    return ModelInfoResponse(
        model_loaded=model.is_loaded(),
        feature_names=model.feature_names,
        class_labels=class_labels_dict,
        version=model.model_version,
        metadata=model.metadata or {},
    )


@app.get(
    "/metadata",
    tags=["Modelo"],
    summary="Metadados do Modelo",
    description="Expõe metadados do modelo carregado, incluindo métricas de performance e informações de treino.",
    response_description="Metadados do modelo",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Metadados disponíveis",
            "content": {
                "application/json": {
                    "example": {
                        "version": "1.0.0",
                        "accuracy": 0.92,
                        "f1_weighted": 0.91,
                        "training_date": "2025-01-15 10:30:00"
                    }
                }
            }
        },
        401: {
            "description": "API Key não fornecida",
            "model": ErrorResponse,
        },
        403: {
            "description": "Acesso negado",
            "model": ErrorResponse,
        },
        503: {
            "description": "Modelo não carregado",
            "model": ErrorResponse,
        }
    },
    dependencies=[Depends(verify_api_key)],
)
async def metadata():
    """
    Expõe metadados do modelo carregado.
    
    Retorna informações sobre o modelo, incluindo:
    - Versão do modelo
    - Métricas de performance (accuracy, F1-score, etc.)
    - Data de treino
    - Informações adicionais armazenadas no arquivo de metadados
    
    **Diferença de `/model/info`:**
    - `/model/info`: Informações técnicas (features, classes, estrutura)
    - `/metadata`: Informações sobre performance e treino (métricas, datas)
    
    ### 🔒 Autenticação
    
    Requer header `X-API-KEY` com uma chave válida.
    """
    if not model.is_loaded():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modelo não carregado"
        )

    return model.metadata or {"version": model.model_version}


# Customização do OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.VERSION,
        description=app.description,
        routes=app.routes,
    )
    
    # Adiciona informações de servidores
    openapi_schema["servers"] = [
        {
            "url": "https://rihs-ftl-undp.ew.r.appspot.com",
            "description": "Servidor de produção"
        },
        {
            "url": "http://localhost:8080",
            "description": "Servidor local (desenvolvimento)"
        }
    ]
    
    # Adiciona informações de segurança
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-KEY",
            "description": "Chave de API para autenticação. Obtenha uma chave válida para acessar endpoints protegidos."
        }
    }
    
    # Aplica segurança aos endpoints que precisam
    for path, path_item in openapi_schema["paths"].items():
        if path in ["/predict", "/model/info", "/metadata"]:
            for method in path_item:
                if method != "options":
                    path_item[method]["security"] = [{"ApiKeyAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
