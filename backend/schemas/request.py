from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

class PredictRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')

    age: int = Field(..., ge=18, le=120, description="Umur ekstrem dibatasi maksimal 120 tahun")
    gender: Literal["Male", "Female"]
    bmi: float = Field(..., ge=10.0, le=100.0, description="BMI ekstrem dibatasi maksimal 100")
    hba1c_level: float = Field(..., ge=3.0, le=20.0, description="HbA1c dibatasi maksimal 20")
    blood_glucose_level: int = Field(..., ge=40, le=500, description="Glukosa dibatasi maksimal 500")
    hypertension: Literal[0, 1]
    heart_disease: Literal[0, 1]
    smoking_history: Literal["never", "former", "current", "not_current", "unknown"]
