import pandas as pd
import yfinance as yf

def download_adj_close(tickers: list[str], start: str, end: str) -> pd.DataFrame:
    df = yf.download( 
        tickers,
        start=start,
        end=end,
        auto_adjust=True,     # uses adjusted prices
        progress=False
    )["Close"] # type: ignore
    if isinstance(df, pd.Series):
        df = df.to_frame()
    df = df.sort_index()
    return df
