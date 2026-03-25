# Core event-driven engine for processing price data and executing trades
from __future__ import annotations

from dataclasses import dataclass
import pandas as pd


@dataclass
class PositionState:
    cash: float = 10_000.0
    units: int = 0
    cumulative_transaction_costs: float = 0.0


class BacktestEngine:
    def __init__(
        self,
        initial_cash: float = 10_000.0,
        transaction_cost_rate: float = 0.001,
    ) -> None:
        self.initial_cash = initial_cash
        self.transaction_cost_rate = transaction_cost_rate

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

            transaction_cost = self._apply_signal(signal, price, state)

            portfolio_value = state.cash + state.units * price
            records.append(
                {
                    "timestamp": row["timestamp"],
                    "price": price,
                    "signal": signal,
                    "cash": state.cash,
                    "units": state.units,
                    "transaction_cost": transaction_cost,
                    "cumulative_transaction_costs": state.cumulative_transaction_costs,
                    "portfolio_value": portfolio_value,
                }
            )

        return pd.DataFrame(records)

    def _apply_signal(self, signal: str, price: float, state: PositionState) -> float:
        transaction_cost = 0.0

        if signal == "BUY":
            transaction_cost = price * self.transaction_cost_rate
            total_buy_cost = price + transaction_cost

            if state.cash >= total_buy_cost:
                state.cash -= total_buy_cost
                state.units += 1
                state.cumulative_transaction_costs += transaction_cost
            else:
                transaction_cost = 0.0

        elif signal == "SELL" and state.units > 0:
            transaction_cost = price * self.transaction_cost_rate
            net_sell_proceeds = price - transaction_cost

            state.cash += net_sell_proceeds
            state.units -= 1
            state.cumulative_transaction_costs += transaction_cost

        return transaction_cost


class BaseStrategy:
    def generate_signal(self, prices_so_far: pd.DataFrame) -> str:
        raise NotImplementedError
