import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


from src.config import Config
from src.data_download import download_adj_close
from src.data_clean import clean_prices, to_monthly_prices, monthly_returns
from src.signals import momentum_12_1
from src.backtest import make_ls_weights, backtest_monthly
from src.metrics import annualized_sharpe, max_drawdown
from src.plots import plot_equity, plot_drawdown, plot_returns_hist

import pandas as pd


def main():
    cfg = Config()

    # Create folders if they don't exist
    for p in [cfg.raw_dir, cfg.processed_dir, cfg.outputs_dir]:
        p.mkdir(parents=True, exist_ok=True)

    raw_path = cfg.raw_dir / "prices_daily.csv"

    tickers = [
        "AAPL","MSFT","AMZN","GOOGL","META","NVDA","JPM","XOM","UNH","JNJ",
        "PG","V","MA","HD","LLY","AVGO","CVX","COST","MRK","PEP",
        "KO","BAC","WMT","DIS","ADBE","CRM","CSCO","ACN","INTC","MCD",
        "TMO","ABT","PFE","LIN","ORCL","AMD","QCOM","TXN","NKE","UPS",
    ]

    # --- Load or download data ---
    if raw_path.exists():
        print("Loading cached price data...")
        prices = pd.read_csv(raw_path, index_col=0, parse_dates=True)
    else:
        print("Downloading price data...")
        prices = download_adj_close(tickers, cfg.start, cfg.end)
        prices.to_csv(raw_path)

    # --- Clean and process data ---
    prices = clean_prices(prices)

    mpx = to_monthly_prices(prices)
    mret = monthly_returns(mpx)


    # --- Signal ---
    signal = momentum_12_1(
       mpx,
        cfg.lookback_months,
        cfg.skip_months
    )

    # --- Portfolio weights ---
    weights = make_ls_weights(
        signal,
        cfg.long_quantile,
        cfg.short_quantile
    )

    # --- Backtest ---
    results = backtest_monthly(
        weights,
        mret,
        cfg.cost_per_turnover
    )

    # --- Metrics ---
    sharpe = annualized_sharpe(results["net_return"])
    mdd = max_drawdown(results["equity"])

    # --- Save results ---
    out_path = cfg.outputs_dir / "results.csv"
    results.to_csv(out_path)

    # --- Plots ---
    plot_equity(results)
    plot_drawdown(results)
    plot_returns_hist(results)

    # --- Print summary ---
    print(f"Sharpe (annualized): {sharpe:.2f}")
    print(f"Max drawdown: {mdd:.2%}")
    print(f"Saved results to: {out_path}")


if __name__ == "__main__":
    main()
