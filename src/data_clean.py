import pandas as pd


def clean_prices(prices: pd.DataFrame, min_coverage: float = 0.95) -> pd.DataFrame:
    """
    Basic cleaning:
    - drop tickers with too much missing data
    - forward-fill small gaps (up to 5 trading days)
    - drop rows where all tickers are missing
    """
    if prices.empty:
        raise ValueError("Prices dataframe is empty.")

    # Keep only tickers with enough non-missing data
    coverage = prices.notna().mean()
    keep_cols = coverage[coverage >= min_coverage].index
    prices = prices.loc[:, keep_cols]

    # Fill small gaps (e.g., holidays / small missing stretches)
    prices = prices.ffill(limit=5)

    # Drop rows where everything is missing (rare, but safe)
    prices = prices.dropna(how="all")

    return prices


def to_monthly_prices(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Convert daily prices to month-end prices (last available trading day of each month).
    """
    if prices.empty:
        raise ValueError("Prices dataframe is empty.")
    return prices.resample("ME").last()


def monthly_returns(monthly_prices: pd.DataFrame) -> pd.DataFrame:
    """
    Percentage change month-to-month.
    """
    if monthly_prices.empty:
        raise ValueError("Monthly prices dataframe is empty.")
    return monthly_prices.pct_change()
