import pandas as pd

def momentum_12_1(monthly_prices: pd.DataFrame, lookback_months: int = 12, skip_months: int = 1) -> pd.DataFrame:
    # momentum = price(t-skip) / price(t-lookback) - 1
    p_end = monthly_prices.shift(skip_months)
    p_start = monthly_prices.shift(lookback_months)
    mom = (p_end / p_start) - 1.0
    return mom
