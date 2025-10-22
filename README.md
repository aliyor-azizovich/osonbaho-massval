# OsonBaho — MassVal (CAMA / ML Core)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](#)
[![Model](https://img.shields.io/badge/Model-CatBoost%20%2B%20LightGBM-green)](#)
[![API](https://img.shields.io/badge/API-FastAPI-lightgrey)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Status: Research](https://img.shields.io/badge/Status-Active-blueviolet)](#)

💡 **OsonBaho MassVal** — модуль массовой оценки недвижимости в Узбекистане (CAMA-подход).  
Использует ансамблевые ML-модели для расчёта рыночной стоимости объектов на основе открытых и собранных данных.

---

## 🎯 Цель
Создать воспроизводимую ML-архитектуру для **массовой оценки** (регрессионные модели по районам, классам и типам домов)  
с поддержкой API-эндпоинта `/v1/estimate/predict`, отчётных метрик и периодического переобучения.

---

## 🧩 Архитектура проекта
osonbaho-massval/
├─ data/ # публичные примеры (без приватных данных)
├─ notebooks/ # Jupyter ноутбуки для исследований и визуализаций
├─ src/
│ ├─ features/ # обработка и генерация признаков
│ ├─ models/ # CatBoost/LGBM ансамбли
│ ├─ metrics/ # расчёт MR, COD, PRD, PRB, R², MAPE, MdAPE
│ ├─ api/ # FastAPI эндпоинт /v1/estimate/predict
│ └─ utils/ # вспомогательные функции
├─ docs/
│ ├─ schemas/ # JSON-схемы входных/выходных данных
│ ├─ api_spec.md # описание эндпоинта
│ └─ examples/ # синтетические примеры запросов/ответов
├─ README.md
└─ LICENSE
### API (витрина)
Каталог `src/api` содержит **каркас FastAPI** с мок-эндпоинтом `/v1/estimate/predict`.
Бизнес-логика и обученные модели **приватны**; код предназначен для демонстрации структуры (Pydantic-модели синхронизированы с `docs/schemas`).


---

## ⚙️ Технологии
- **Python:** Pandas, NumPy, Scikit-learn  
- **ML:** CatBoost, LightGBM, XGBoost  
- **API:** FastAPI  
- **Data storage:** PostgreSQL / Parquet / S3  
- **Monitoring:** MLflow, Weights&Biases  
- **Automation:** Prefect / Airflow  
- **Infrastructure:** Docker, Ubuntu, AWS EC2  

---

## 📈 Метрики качества
| Метрика | Описание |
|----------|-----------|
| **R²** | Коэффициент детерминации |
| **MAE / MAPE / MdAPE** | Ошибки |
| **MR / COD / PRD / PRB** | IAAO-метрики |
| **Trend slope / p-value** | Проверка регрессивности |

---

## 🧠 Пример API запроса
```json
POST /v1/estimate/predict
{
  "id_district": 12,
  "total_area_m2": 250,
  "lot_area_sotka": 4.5,
  "floors": 2,
  "rooms": 5,
  "class": "Комфорт"
}

{
  "prediction_value": 4_250_000_000,
  "confidence_interval": [3_800_000_000, 4_700_000_000],
  "model_version": "v1.3.2",
  "metrics": { "R2": 0.68, "MAPE": 0.29, "COD": 34.2 }
}

🗺 Roadmap

 Завершить прототип FastAPI /v1/estimate/predict

 Автоматизировать ETL-поток (Prefect)

 Обучить 12 районных моделей (CatBoost + LGBM)

 Настроить MLflow мониторинг

 Добавить explainability (SHAP)

 Сгенерировать whitepaper по массовой оценке в Узбекистане

📬 Контакты

Автор: Абдусаматов Алиёр Азизович (Фергана, Узбекистан)
Email: aliyor.0276@gmail.com
 · Telegram: @a_azizovich



