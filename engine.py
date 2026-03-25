# Core event-driven engine for processing price data and executing trades
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
import pandas as pd


@dataclass
class PositionState:
    cash: float = 10_000.0
    units: int = 0


class BacktestEngine:
    def __init__(self, initial_cash: float = 10_000.0) -> None:
        self.initial_cash = initial_cash

    def run(self, prices: pd.DataFrame, strategy: "BaseStrategy") -> pd.DataFrame:
        required = {"timestamp", "price"}
        missing = required - set(prices.columns)
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

        df = prices.copy().sort_values("timestamp").reset_index(drop=True)
        state = PositionState(cash=self.initial_cash, units=0)
        records: list[dict] = []

        for idx, row in df.iterrows():
            price = float(row["price"])
            signal = strategy.generate_signal(df.iloc[: idx + 1])
            self._apply_signal(signal, price, state)
            portfolio_value = state.cash + state.units * price
            records.append(
                {
                    "timestamp": row["timestamp"],
                    "price": price,
                    "signal": signal,
                    "cash": state.cash,
                    "units": state.units,
                    "portfolio_value": portfolio_value,
                }
            )
        return pd.DataFrame(records)

    @staticmethod
    def _apply_signal(signal: str, price: float, state: PositionState) -> None:
        if signal == "BUY" and state.cash >= price:
            state.cash -= price
            state.units += 1
        elif signal == "SELL" and state.units > 0:
            state.cash += price
            state.units -= 1


class BaseStrategy:
    def generate_signal(self, prices_so_far: pd.DataFrame) -> str:
        raise NotImplementedError
