from __future__ import annotations

import argparse
import pandas as pd

from engine import BacktestEngine
from metrics import compute_metrics
from strategy import MeanReversionStrategy


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to CSV with timestamp,price columns")
    parser.add_argument("--window", type=int, default=5)
    parser.add_argument("--threshold", type=float, default=0.01)
    args = parser.parse_args()

    prices = pd.read_csv(args.csv)
    engine = BacktestEngine()
    strategy = MeanReversionStrategy(window=args.window, threshold=args.threshold)

    results = engine.run(prices, strategy)
    stats = compute_metrics(results)

    print("Backtest complete")
    for key, value in stats.items():
        print(f"{key}: {value:.6f}")


if __name__ == "__main__":
    main()
