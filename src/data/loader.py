"""
Data loader for XAUUSD / Gold futures
Uses yfinance for research. For production replace with broker API (MT5, Interactive Brokers, etc.)
"""

from __future__ import annotations

import pandas as pd
import yfinance as yf
from pathlib import Path
from loguru import logger
from typing import Optional


def fetch_ohlcv(
    symbol: str = "GC=F",
    interval: str = "1h",
    start: str = "2022-01-01",
    end: Optional[str] = None,
    save_path: Optional[Path] = None,
) -> pd.DataFrame:
    """
    Download OHLCV data.
    Note: yfinance GC=F has limitations on intraday history depth.
    For serious backtests use broker data or paid providers.
    """
    logger.info(f"Fetching {symbol} {interval} from {start} to {end or 'now'}")

    ticker = yf.Ticker(symbol)
    df = ticker.history(start=start, end=end, interval=interval, auto_adjust=True)

    if df.empty:
        raise ValueError(f"No data returned for {symbol}")

    # Standardize columns
    df = df.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume",
    })
    df = df[["open", "high", "low", "close", "volume"]].copy()
    df.index = pd.to_datetime(df.index)
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)

    df = df.dropna()
    logger.info(f"Loaded {len(df)} bars | {df.index[0]} → {df.index[-1]}")

    if save_path:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            df.to_parquet(save_path.with_suffix(".parquet"))
            logger.info(f"Saved to {save_path.with_suffix('.parquet')}")
        except Exception:
            df.to_csv(save_path.with_suffix(".csv"))
            logger.info(f"Saved to {save_path.with_suffix('.csv')}")

    return df


def load_or_fetch(
    symbol: str,
    interval: str,
    start: str,
    end: Optional[str] = None,
    cache_dir: Path = Path("data"),
) -> pd.DataFrame:
    base = cache_dir / f"{symbol.replace('=', '_')}_{interval}_{start}_{end or 'latest'}"
    parquet_file = base.with_suffix(".parquet")
    csv_file = base.with_suffix(".csv")

    if parquet_file.exists():
        logger.info(f"Loading cached data from {parquet_file}")
        return pd.read_parquet(parquet_file)
    if csv_file.exists():
        logger.info(f"Loading cached data from {csv_file}")
        return pd.read_csv(csv_file, index_col=0, parse_dates=True)

    return fetch_ohlcv(symbol, interval, start, end, save_path=base)


def add_atr(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """Add ATR for volatility filters and sizing."""
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df = df.copy()
    df["atr"] = tr.rolling(period).mean()
    return df
