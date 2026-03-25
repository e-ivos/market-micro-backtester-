import pandas as pd

from metrics import compute_metrics


def test_metrics_has_expected_keys() -> None:
    df = pd.DataFrame({"portfolio_value": [100.0, 101.0, 100.5, 102.0]})
    stats = compute_metrics(df)
    assert set(stats) == {"final_value", "total_return", "volatility", "sharpe", "max_drawdown"}
