# API Spec — /v1/estimate/predict

**Method:** `POST`  
**URL:** `/v1/estimate/predict`  
**Content-Type:** `application/json`  
**Auth:** (optional) Bearer token

## Request (JSON)
- `id_district` *(int, required)* — ID района
- `total_area_m2` *(number, required)* — общая площадь дома
- `lot_area_sotka` *(number, optional)* — площадь участка (сотки)
- `floors` *(int, required)*
- `rooms` *(int, required)*
- `house_class` *(string, optional)* — например: `Бюджетный | Комфорт | Премиум`
- `year_built` *(int, optional)*
- `features` *(object, optional)* — инженерные/качественные признаки (например, материал, состояние)

## Response (JSON)
- `prediction_value` *(number, required)* — оценочная стоимость, сум
- `confidence_interval` *(array[number, number], required)* — [low, high]
- `model_version` *(string, required)*
- `metrics` *(object, optional)* — основные метрики качества модели (на валидации)
- `explain` *(object, optional)* — важности признаков / contribs (агрегировано)

## Error (JSON)
- `error` *(string, required)*
- `details` *(object, optional)*

## Пример запроса
```json
{
  "id_district": 12,
  "total_area_m2": 250,
  "lot_area_sotka": 4.5,
  "floors": 2,
  "rooms": 5,
  "house_class": "Комфорт",
  "year_built": 2008
}

Пример ответа

{
  "prediction_value": 4250000000,
  "confidence_interval": [3800000000, 4700000000],
  "model_version": "v1.3.2",
  "metrics": {"R2": 0.68, "MAPE": 0.29, "COD": 34.2},
  "explain": {"top_features": ["id_district","total_area_m2","lot_area_sotka"]}
}
Пример ошибки
{
  "error": "validation_error",
  "details": {"field": "total_area_m2", "message": "must be > 0"}
}


---

## 2) Файл `docs/schemas/input.json`
**Путь:** `docs/schemas/input.json`  
**Содержимое:**
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "MassValPredictInput",
  "type": "object",
  "properties": {
    "id_district": { "type": "integer", "minimum": 1 },
    "total_area_m2": { "type": "number", "exclusiveMinimum": 0 },
    "lot_area_sotka": { "type": "number", "minimum": 0 },
    "floors": { "type": "integer", "minimum": 1 },
    "rooms": { "type": "integer", "minimum": 1 },
    "house_class": { "type": "string", "enum": ["Бюджетный","Комфорт","Премиум"] },
    "year_built": { "type": "integer", "minimum": 1900, "maximum": 2100 },
    "features": { "type": "object", "additionalProperties": true }
  },
  "required": ["id_district","total_area_m2","floors","rooms"],
  "additionalProperties": false
}

