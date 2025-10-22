from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Dict, Optional


def _to_numpy(a) -> np.ndarray:
    if isinstance(a, (pd.Series, pd.DataFrame)):
        a = a.values
    return np.asarray(a, dtype=float).ravel()


def ratios(y_true, y_pred) -> np.ndarray:
    """
    Цена/оценка отношениями:
    ratio = y_pred / y_true  (как в большинстве рабочих пайплайнов)
    """
    yt = _to_numpy(y_true)
    yp = _to_numpy(y_pred)
    mask = np.isfinite(yt) & np.isfinite(yp) & (yt > 0)
    r = np.zeros_like(yp, dtype=float)
    r[mask] = yp[mask] / yt[mask]
    return r[mask]


def mape(y_true, y_pred) -> float:
    yt = _to_numpy(y_true)
    yp = _to_numpy(y_pred)
    mask = np.isfinite(yt) & np.isfinite(yp) & (yt > 0)
    return float(np.mean(np.abs(yp[mask] - yt[mask]) / yt[mask]) * 100.0)


def mdape(y_true, y_pred) -> float:
    yt = _to_numpy(y_true)
    yp = _to_numpy(y_pred)
    mask = np.isfinite(yt) & np.isfinite(yp) & (yt > 0)
    return float(np.median(np.abs(yp[mask] - yt[mask]) / yt[mask]) * 100.0)


def iaao_metrics(y_true, y_pred) -> Dict[str, float]:
    """
    Базовые IAAO-метрики:
      MR  – Median Ratio
      COD – Coefficient of Dispersion
      PRD – Price-Related Differential  = mean(ratio) / median(ratio)
      PRB – Price-Related Bias (наклон регрессии ratio ~ log(price)) * 100
    """
    r = ratios(y_true, y_pred)
    if r.size == 0:
        return {"MR": np.nan, "COD": np.nan, "PRD": np.nan, "PRB": np.nan}

    mr = float(np.median(r))
    mean_r = float(np.mean(r))
    # COD по IAAO: 100 * median(|r - median(r)|) / median(r)
    cod = float(100.0 * np.median(np.abs(r - mr)) / mr) if mr != 0 else np.nan
    prd = float(mean_r / mr) if mr != 0 else np.nan

    # PRB: наклон регрессии r ~ log(y_true)
    yt = _to_numpy(y_true)
    mask = np.isfinite(yt) & (yt > 0)
    x = np.log(yt[mask])
    y = r[: x.size]  # выравниваем длину на случай фильтра
    if x.size > 1 and y.size == x.size:
        # простая линейная регрессия через МНК
        x_ = np.vstack([x, np.ones_like(x)]).T
        beta, _, _, _ = np.linalg.lstsq(x_, y, rcond=None)
        prb = float(beta[0] * 100.0)  # в процентах на лог-шкале
    else:
        prb = np.nan

    return {"MR": mr, "COD": cod, "PRD": prd, "PRB": prb}


def full_report(y_true, y_pred) -> Dict[str, float]:
    """Удобный агрегат для README и логов."""
    yt = _to_numpy(y_true)
    yp = _to_numpy(y_pred)
    mask = np.isfinite(yt) & np.isfinite(yp)
    yt, yp = yt[mask], yp[mask]

    # классические
    mae = float(np.mean(np.abs(yp - yt)))
    # R2 по формуле 1 - SSE/SST
    sse = float(np.sum((yp - yt) ** 2))
    sst = float(np.sum((yt - yt.mean()) ** 2))
    r2 = 1.0 - sse / sst if sst > 0 else np.nan

    mape_v = mape(yt, yp)
    mdape_v = mdape(yt, yp)
    iaao = iaao_metrics(yt, yp)

    return {
        "R2": r2,
        "MAE": mae,
        "MAPE": mape_v,
        "MdAPE": mdape_v,
        **iaao,
    }
