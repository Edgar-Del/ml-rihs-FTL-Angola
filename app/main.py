from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn

from app.config import settings
from app.models import SustainabilityModel
from app.schemas import PredictionInput, PredictionOutput, HealthResponse
from app.utils import (
    init_metrics,
    normalize_features,
    validate_feature_payload,
    verify_api_key,
)

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cria aplicação FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="API para classificação de sustentabilidade de hotéis",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

init_metrics(app)

# Instância global do modelo
model = SustainabilityModel()


@app.on_event("startup")
async def startup_event():
    """Carrega o modelo na inicialização"""
    logger.info(f"Iniciando {settings.APP_NAME} v{settings.VERSION}")
    
    success = model.load_model(
        registry_path=settings.MODEL_REGISTRY_PATH,
        version=settings.MODEL_VERSION,
        fallback_version=settings.MODEL_FALLBACK_VERSION,
        metadata_file=settings.METADATA_FILE,
    )
    if success:
        logger.info("Modelo carregado com sucesso")
    else:
        logger.error("Falha ao carregar o modelo")

    if settings.API_KEY is None:
        logger.warning("API_KEY não configurada. Endpoints protegidos irão retornar erro 500.")


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
        if not model.is_loaded():
            raise HTTPException(status_code=503, detail="Modelo não carregado")
        
        features = normalize_features(input_data.to_feature_dict())
        validate_feature_payload(features)

        # Faz predição
        prediction_result = model.predict(features)
        
        logger.info(f"Predição realizada: {prediction_result['prediction_label']}")
        
        return PredictionOutput(**prediction_result)
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