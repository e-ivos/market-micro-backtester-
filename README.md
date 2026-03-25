# market-micro-backtester

A small event-driven market backtester in Python. It simulates a simple mean-reversion strategy on historical price data and reports performance metrics like total return, volatility, Sharpe ratio, and max drawdown. Models transaction costs on buys and sells for more realistic performance evaluation

## Why this is useful
This project demonstrates:
- clean software structure
- data ingestion from CSV
- event-driven design
- performance analytics
- testing
- 

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run_backtest.py --csv sample_prices.csv
```

## CSV format
```csv
timestamp,price
2026-01-01T09:30:00,100.0
2026-01-01T09:31:00,100.4
```

## Files
- `engine.py` - core backtest engine
- `strategy.py` - mean-reversion strategy
- `metrics.py` - return and risk metrics
- `run_backtest.py` - CLI entry point
- `tests/` - basic tests

## Resume bullets
- Built an event-driven trading backtester in Python to simulate signals on historical time-series data
- Implemented portfolio performance metrics including Sharpe ratio, volatility, and max drawdown
- Structured the project with modular strategy, engine, and analytics components and added unit tests
