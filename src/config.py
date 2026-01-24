from dataclasses import dataclass # clean way to store variables together
from pathlib import Path # safe way to handle file paths 

@dataclass(frozen=True)
class Config:
    start: str = "2010-01-01"
    end: str = "2025-12-31"
    rebalance_freq: str = "M"          # monthly, which means that once per month, we look at stock history and decide what to hold next month 
    lookback_months: int = 12          # to decide which stocks are doing well, we look back 12 months and ignore the most recent 1 month
    skip_months: int = 1
    long_quantile: float = 0.9         # buy top 20%
    short_quantile: float = 0.1        # sell or bet against bottom 20%
    cost_per_turnover: float = 0.0   # 10 bps

    data_dir: Path = Path("data")
    raw_dir: Path = Path("data/raw")
    processed_dir: Path = Path("data/processed")
    outputs_dir: Path = Path("data/outputs")
