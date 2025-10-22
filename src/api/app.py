from fastapi import FastAPI, HTTPException
from .models import PredictRequest, PredictResponse, Metrics

app = FastAPI(
    title="OsonBaho MassVal API",
    version="0.1.0",
    description="Витринный эндпоинт массовой оценки. Логика предикта приватна.",
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/v1/estimate/predict", response_model=PredictResponse)
def predict(payload: PredictRequest):
    # ---- MOCK: здесь могла бы быть загрузка модели и инференс ----
    # Для витрины вернем детерминированный демо-ответ на основе простых эвристик
    base = float(payload.total_area_m2) * 8_000_000  # эвристика: 8 млн сум за м² (пример)
    if payload.lot_area_sotka:
        base += float(payload.lot_area_sotka) * 120_000_000  # 120 млн за сотку (пример)
    if payload.house_class == "Премиум":
        base *= 1.25
    elif payload.house_class == "Бюджетный":
        base *= 0.9

    # confidence: +-12% как витринный диапазон
    low, high = base * 0.88, base * 1.12

    return PredictResponse(
        prediction_value=round(base, 2),
        confidence_interval=(round(low, 2), round(high, 2)),
        model_version="demo-v0.1",
        metrics=Metrics(R2=0.0, MAPE=0.0, COD=0.0),  # витрина; реальные метрики приватны
        explain={"top_features": ["total_area_m2", "lot_area_sotka", "house_class"]},
    )
