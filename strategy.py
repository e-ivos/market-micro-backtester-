from __future__ import annotations

import pandas as pd

from engine import BaseStrategy


class MeanReversionStrategy(BaseStrategy):
    def __init__(self, window: int = 5, threshold: float = 0.01) -> None:
        self.window = window
        self.threshold = threshold

    def generate_signal(self, prices_so_far: pd.DataFrame) -> str:
        if len(prices_so_far) < self.window:
            return "HOLD"

        recent = prices_so_far["price"].tail(self.window)
        moving_avg = float(recent.mean())
        current = float(recent.iloc[-1])

        if current < moving_avg * (1 - self.threshold):
            return "BUY"
        if current > moving_avg * (1 + self.threshold):
            return "SELL"
        return "HOLD"
