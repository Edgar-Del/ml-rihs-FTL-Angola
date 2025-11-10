from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from typing import Dict

from app.config import settings
from app.models import SustainabilityModel
from app.schemas import PredictionInput, PredictionOutput, HealthResponse

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
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instância global do modelo
model = SustainabilityModel()


@app.on_event("startup")
async def startup_event():
    """Carrega o modelo na inicialização"""
    logger.info(f"Iniciando {settings.APP_NAME} v{settings.VERSION}")
    
    success = model.load_model(settings.MODEL_PATH)
    if success:
        logger.info("Modelo carregado com sucesso")
    else:
        logger.error("Falha ao carregar o modelo")


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
async def predict(input_data: PredictionInput):
    """
    Endpoint para classificar sustentabilidade de hotel
    
    Recebe as características do hotel e retorna a classificação
    de sustentabilidade com probabilidades.
    """
    try:
        if not model.is_loaded():
            raise HTTPException(status_code=503, detail="Modelo não carregado")
        
        # Converte input para dict
        features = input_data.dict()
        
        # Faz predição
        prediction_result = model.predict(features)
        
        logger.info(f"Predição realizada: {prediction_result['prediction_label']}")
        
        return PredictionOutput(**prediction_result)
        
    except Exception as e:
        logger.error(f"Erro no endpoint /predict: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@app.get("/model/info")
async def model_info():
    """Retorna informações sobre o modelo"""
    if not model.is_loaded():
        raise HTTPException(status_code=503, detail="Modelo não carregado")
    
    return {
        "model_loaded": model.is_loaded(),
        "feature_names": model.feature_names,
        "class_labels": model.class_labels,
        "version": settings.VERSION
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )