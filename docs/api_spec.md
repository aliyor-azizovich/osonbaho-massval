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

