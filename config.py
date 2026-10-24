"""
Configuration for IOF Gold Bot
Institutional Order Flow strategy for XAUUSD
"""

from pathlib import Path
from pydantic import BaseModel, Field
from typing import Literal


class RiskConfig(BaseModel):
    risk_per_trade_pct: float = Field(default=0.5, ge=0.1, le=2.0, description="% of equity risked per trade")
    max_daily_loss_pct: float = Field(default=3.0, ge=1.0, le=10.0)
    max_open_trades: int = Field(default=2, ge=1, le=5)
    min_rr: float = Field(default=2.0, ge=1.5, le=5.0, description="Minimum Risk:Reward")
    partial_close_rr: float = Field(default=1.5, description="Close 50% at this RR")


class StrategyConfig(BaseModel):
    # Timeframes
    htf: str = "1d"          # Higher timeframe for POI / bias
    ltf: str = "1h"          # Working timeframe
    entry_tf: str = "15m"    # Optional entry refinement

    # Swing / Structure
    swing_lookback: int = 5          # bars left/right for swing detection
    structure_lookback: int = 20

    # FVG
    fvg_min_size_atr: float = 0.3    # minimum FVG size relative to ATR
    use_group_fvg: bool = True       # group consecutive FVGs as author prefers

    # Liquidity / Sweep
    sweep_tolerance_atr: float = 0.15
    require_bos_after_sweep: bool = True

    # Fibonacci / Zones
    fib_levels: list[float] = [0.0, 0.5, 1.0]
    premium_zone: tuple[float, float] = (0.5, 1.0)   # Short zone
    discount_zone: tuple[float, float] = (0.0, 0.5)  # Long zone

    # Filters
    use_session_filter: bool = True
    london_start: str = "07:00"
    ny_start: str = "13:00"
    avoid_news: bool = True          # placeholder, needs calendar integration

    # Order Block (low priority as per author)
    use_order_block: bool = False


class BacktestConfig(BaseModel):
    symbol: str = "GC=F"             # Gold futures (yfinance)
    start_date: str = "2022-01-01"
    end_date: str = "2026-10-01"
    initial_capital: float = 10_000.0
    commission_per_lot: float = 0.0  # set realistic for your broker
    slippage_pips: float = 0.3       # gold is quoted in USD


class Config(BaseModel):
    risk: RiskConfig = RiskConfig()
    strategy: StrategyConfig = StrategyConfig()
    backtest: BacktestConfig = BacktestConfig()
    data_dir: Path = Path("data")
    results_dir: Path = Path("results")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"


# Global instance
cfg = Config()
