from contextlib import asynccontextmanager
import logging
from pathlib import Path

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from core.settings import settings
from app.models import SustainabilityModel
from app.schemas import PredictionInput, PredictionOutput, HealthResponse
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


# Cria aplicação FastAPI com lifespan
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="API para classificação de sustentabilidade de hotéis",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
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

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": f"Bem-vindo ao {settings.APP_NAME}",
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check para monitoramento"""
    return HealthResponse(
        status="healthy" if model.is_loaded() else "unhealthy",
        model_loaded=model.is_loaded(),
        version=settings.VERSION
    )


    """Endpoint para métricas do Prometheus"""
    try:
        from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
        from fastapi.responses import Response
        return Response(
            generate_latest(),
            media_type=CONTENT_TYPE_LATEST
        )
    except ImportError:
        raise HTTPException(
            status_code=501, 
            detail="Métricas não disponíveis"
        )
    

@app.post("/predict", response_model=PredictionOutput)
async def predict(
    input_data: PredictionInput,
    _: None = Depends(verify_api_key),
):
    """
    Endpoint para classificar sustentabilidade de hotel
    
    Recebe as características do hotel e retorna a classificação
    de sustentabilidade com probabilidades.
    """
    try:
        model_path = Path(settings.MODEL_REGISTRY_PATH)
        fallback_path = getattr(model, "loaded_path", None)
        if not model_path.exists() and not (fallback_path and Path(fallback_path).exists()):
            logger.error("Modelo indisponível em %s", model_path)
            raise HTTPException(status_code=503, detail="Model unavailable")

        if not settings.API_KEY:
            logger.error("API key não configurada no servidor")
            raise HTTPException(status_code=403, detail="API key missing")

        if not model.is_loaded():
            raise HTTPException(status_code=503, detail="Modelo não carregado")
        
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
        raise HTTPException(status_code=400, detail=str(err)) from err
    except Exception as e:
        logger.error(f"Erro no endpoint /predict: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@app.get("/model/info", dependencies=[Depends(verify_api_key)])
async def model_info():  # pragma: no cover - serialização simples
    """Retorna informações sobre o modelo"""
    if not model.is_loaded():
        raise HTTPException(status_code=503, detail="Modelo não carregado")
    
    return {
        "model_loaded": model.is_loaded(),
        "feature_names": model.feature_names,
        "class_labels": model.class_labels,
        "version": model.model_version,
        "metadata": model.metadata,
    }


@app.get("/metadata", dependencies=[Depends(verify_api_key)])
async def metadata():
    """Expõe metadados do modelo carregado."""
    if not model.is_loaded():
        raise HTTPException(status_code=503, detail="Modelo não carregado")

    return model.metadata or {"version": model.model_version}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )