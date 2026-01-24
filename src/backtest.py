import numpy as np
import pandas as pd

def make_ls_weights(signal: pd.DataFrame, long_q: float, short_q: float) -> pd.DataFrame:
    # per date, go long top quantile, short bottom quantile
    def one_date_weights(s: pd.Series) -> pd.Series: # to do one month
        s = s.dropna()
        if len(s) < 20:
            return pd.Series(dtype=float)

        long_thr = s.quantile(long_q)
        short_thr = s.quantile(short_q)
 
        longs = s[s >= long_thr].index # longs becomes a list of tickers in the top group
        shorts = s[s <= short_thr].index # shorts becomes a list of tickers in the bottom group

        w = pd.Series(0.0, index=s.index)

        if len(longs) > 0:
            w.loc[longs] =  1.0 / len(longs)
        if len(shorts) > 0:
            w.loc[shorts] = -1.0 / len(shorts)
 
        return w

    weights = signal.apply(one_date_weights, axis=1)
    weights = weights.reindex_like(signal).fillna(0.0)
    return weights

def backtest_monthly(weights: pd.DataFrame, rets: pd.DataFrame, cost_per_turnover: float) -> pd.DataFrame:
    # Align
    weights = weights.reindex(rets.index).fillna(0.0)
    rets = rets.fillna(0.0)

    # Use weights decided at month t to earn returns at month t+1 (avoids lookahead)
    w_next = weights.shift(1).fillna(0.0)

    gross = (w_next * rets).sum(axis=1)

    # Turnover approximation: sum abs(delta weights)
    turnover = weights.diff().abs().sum(axis=1).fillna(0.0)
    costs = cost_per_turnover * turnover

    net = gross - costs

    out = pd.DataFrame({
        "gross_return": gross,
        "net_return": net,
        "turnover": turnover,
        "costs": costs,
    })
    out["equity"] = (1.0 + out["net_return"]).cumprod()
    
    return out
