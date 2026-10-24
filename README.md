# IOF Gold Bot

**Institutional Order Flow** research framework for XAUUSD / Gold.

Based on the concepts from the article:  
[Institutional Order Flow](https://teletype.in/@sbrt/Institutional-Order-Flow) by @sbrt

## ⚠️ Disclaimer

This is a **research and educational** codebase.  
It is **NOT** a ready-to-deploy live trading system.

- Past performance ≠ future results  
- Always paper-trade and forward-test extensively  
- You are solely responsible for any capital you risk  
- The author of the original article is skeptical of Order Blocks — this code follows that spirit (OB is disabled by default)

## Core Concepts Implemented

- **POI + Trading Range** (key liquidity pools as range boundaries)
- **Fibonacci Premium / Discount / Equilibrium** zones
- **Fair Value Gap (FvG)** detection + grouping of consecutive imbalances
- **Sweep** (liquidity grab) detection
- **Break of Structure (BoS)**
- Entries **only** from correct zones:
  - Long → Discount only
  - Short → Premium only
- Prefer Sweep + (BoS or FvG reaction)

## Project Structure

```
iof-gold-bot/
├── config.py              # All parameters (risk, strategy, backtest)
├── main.py                # Runner
├── requirements.txt
├── src/
│   ├── data/loader.py     # yfinance + cache (replace with broker for prod)
│   ├── indicators/
│   │   ├── swings.py      # Swing highs/lows + equal levels
│   │   ├── fvg.py         # Fair Value Gaps + grouping
│   │   ├── structure.py   # BoS + Sweeps
│   │   └── fibo.py        # Trading range + Premium/Discount
│   ├── strategy/iof.py    # Signal engine
│   └── backtest/engine.py # Simple event backtester
└── tests/
```

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run unit tests
python tests/test_indicators.py

# Run research backtest
python main.py
```

## Important Notes on Data

- `yfinance` `GC=F` (Gold futures) has limited intraday history.
- For serious work use:
  - Broker historical data (MT5, cTrader, Interactive Brokers)
  - Paid providers (TickData, Databento, etc.)
- Daily timeframe works better with free data for long periods.

## Production Roadmap (what is still missing)

1. Real broker connector (MT5 Python / FIX / REST)
2. Proper position sizing + partial closes
3. Session filters + economic calendar
4. Higher-timeframe bias filter
5. Walk-forward optimization + Monte-Carlo
6. Live signal → Telegram / Discord
7. Robust error handling + reconnect logic

## License

MIT — use at your own risk.
