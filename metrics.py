# computes sharpe ratio, volatility, and drawdown
from __future__ import annotations

import numpy as np
import pandas as pd


def compute_metrics(results: pd.DataFrame) -> dict[str, float]:
    values = results["portfolio_value"].astype(float)
    returns = values.pct_change().dropna()

    if len(values) == 0:
        raise ValueError("Results are empty")

    total_return = float(values.iloc[-1] / values.iloc[0] - 1)
    volatility = float(returns.std(ddof=0) * np.sqrt(max(len(returns), 1))) if len(returns) else 0.0
    sharpe = float((returns.mean() / returns.std(ddof=0)) * np.sqrt(len(returns))) if len(returns) and returns.std(ddof=0) != 0 else 0.0
    max_drawdown = _max_drawdown(values)

    return {
        "final_value": float(values.iloc[-1]),
        "total_return": total_return,
        "volatility": volatility,
        "sharpe": sharpe,
        "max_drawdown": max_drawdown,
    }


def _max_drawdown(values: pd.Series) -> float:
    running_max = values.cummax()
    drawdowns = values / running_max - 1
    return float(drawdowns.min())
