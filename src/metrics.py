import numpy as np
import pandas as pd

def annualized_sharpe(r: pd.Series, periods_per_year: int = 12) -> float:
    r = r.dropna()
    if r.std(ddof=1) == 0:
        return np.nan
    return (r.mean() / r.std(ddof=1)) * np.sqrt(periods_per_year)

def max_drawdown(equity: pd.Series) -> float:
    peak = equity.cummax()
    dd = equity / peak - 1.0
    return dd.min()
