from pydantic import BaseModel
from typing import List

class Factor(BaseModel):
    feature: str
    direction: str
    impact: str

class PredictResponse(BaseModel):
    risk_level: str
    summary: str
    top_factors: List[Factor]
    recommendation: str
    disclaimer: str

class ExplainResponse(BaseModel):
    top_factors: List[Factor]

class MetadataResponse(BaseModel):
    model_name: str
    version: str
    target: str
    inference_mode: str

class HealthResponse(BaseModel):
    status: str
    env: str
    version: str
