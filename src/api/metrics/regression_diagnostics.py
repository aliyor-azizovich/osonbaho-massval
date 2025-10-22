from __future__ import annotations
import numpy as np
from typing import Dict, Optional

def trend_on_ratio(y_true, y_pred) -> Dict[str, float]:
    """
    Диагностика регрессивности: регрессия ratio = y_pred/y_true на y_true.
    Возвращает наклон (slope) и R^2. p-value опционально (если есть scipy).
    """
    try:
        from scipy import stats  # type: ignore
        use_scipy = True
    except Exception:
        use_scipy = False

    yt = np.asarray(y_true, dtype=float).ravel()
    yp = np.asarray(y_pred, dtype=float).ravel()
    mask = np.isfinite(yt) & np.isfinite(yp) & (yt > 0)
    yt, yp = yt[mask], yp[mask]
    ratio = yp / yt

    if yt.size < 3:
        return {"slope": np.nan, "r2": np.nan, "p_value": np.nan}

    if use_scipy:
        res = stats.linregress(yt, ratio)
        return {"slope": float(res.slope), "r2": float(res.rvalue**2), "p_value": float(res.pvalue)}
    else:
        # fallback на чистом numpy
        x = yt
        y = ratio
        x_mean, y_mean = x.mean(), y.mean()
        cov = np.sum((x - x_mean) * (y - y_mean))
        var = np.sum((x - x_mean) ** 2)
        slope = cov / var if var > 0 else np.nan
        # R2
        sst = np.sum((y - y_mean) ** 2)
        sse = np.sum((y - (slope * x + (y_mean - slope * x_mean))) ** 2)
        r2 = 1.0 - sse / sst if sst > 0 else np.nan
        return {"slope": float(slope), "r2": float(r2), "p_value": np.nan}
