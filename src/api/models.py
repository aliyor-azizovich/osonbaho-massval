from typing import Optional, Dict, List, Tuple
from pydantic import BaseModel, Field, conint, confloat

# ==== Вход =====
class PredictRequest(BaseModel):
    id_district: conint(ge=1) = Field(..., description="ID района")
    total_area_m2: confloat(gt=0) = Field(..., description="Общая площадь дома, м²")
    lot_area_sotka: Optional[confloat(ge=0)] = Field(None, description="Площадь участка, сотки")
    floors: conint(ge=1) = Field(..., description="Этажность")
    rooms: conint(ge=1) = Field(..., description="Количество комнат")
    house_class: Optional[str] = Field(None, description="Бюджетный | Комфорт | Премиум")
    year_built: Optional[conint(ge=1900, le=2100)] = Field(None, description="Год постройки")
    features: Optional[Dict[str, object]] = Field(None, description="Произвольные признаки")

# ==== Выход =====
class Metrics(BaseModel):
    R2: Optional[float] = None
    MAE: Optional[float] = None
    MAPE: Optional[float] = None
    MdAPE: Optional[float] = None
    MR: Optional[float] = None
    COD: Optional[float] = None
    PRD: Optional[float] = None
    PRB: Optional[float] = None

class PredictResponse(BaseModel):
    prediction_value: float
    confidence_interval: Tuple[float, float]
    model_version: str
    metrics: Optional[Metrics] = None
    explain: Optional[Dict[str, List[str]]] = None

class ErrorResponse(BaseModel):
    error: str
    details: Optional[Dict[str, object]] = None
