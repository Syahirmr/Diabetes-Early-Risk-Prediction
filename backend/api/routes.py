from fastapi import APIRouter
from backend.schemas.request import PredictRequest
from backend.schemas.response import PredictResponse, ExplainResponse, MetadataResponse, HealthResponse
from backend.services.predict_service import get_prediction, get_explanation
from backend.startup.load_artifacts import ArtifactStore
from backend.utils.config import settings

router = APIRouter(prefix="/api/v1")

@router.get("/health", response_model=HealthResponse)
def health_check():
    return {"status": "ok", "env": settings.APP_ENV, "version": ArtifactStore.metadata.get("model_version", "1.0")}

@router.get("/metadata", response_model=MetadataResponse)
def metadata():
    m = ArtifactStore.metadata
    return MetadataResponse(
        model_name=m.get("model_name", "rf_diabetes"),
        version=m.get("model_version", "1.0"),
        target=m.get("target", "diabetes"),
        inference_mode=m.get("inference_mode", "risk_category")
    )

@router.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    return get_prediction(request)

@router.post("/explain", response_model=ExplainResponse)
def explain(request: PredictRequest):
    return get_explanation(request)
