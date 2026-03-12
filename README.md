# Cross-Sectional Momentum with Volatility Targeting

A clean, research-quality systematic equity strategy built on **cross-sectional momentum** -
with full backtest, drawdown analysis, and volatility-targeted risk control.

**Author:** Stefanie Samaha

---

## Key Results

| Strategy | Sharpe Ratio | Max Drawdown | Final Equity ($1 invested) |
|---|---|---|---|
| **Long-only (top 10%)** | **1.31** | **-23.5%** | **$56.93** |
| Long/Short (top/bottom 10%) | 0.28 | -66.7% | $1.83 |
| Short-only (bottom 10%) | -0.88 | -98.3% | $0.02 |

> **Key insight:** Long-only momentum captures nearly all available alpha with far lower risk than the long/short combination. Volatility targeting further improves the equity curve to ~$80 over the same period by dynamically scaling exposure.

*Universe: Large-cap U.S. equities | Period: 2010–2026 | Monthly rebalancing*

---

## Results

### Effect of Volatility Targeting
Long-only baseline vs. volatility-targeted strategy — 15-year equity curve.

![Volatility Targeting](data/outputs/Figure_4_Volatility_Targeting.png)

### Equity Curve (Long-only)
![Equity Curve](data/outputs/Figure_1_Equity_Curve.png)

### Drawdowns
![Drawdowns](data/outputs/Figure_2_Drawdowns.png)

### Monthly Return Distribution
![Return Distribution](data/outputs/Figure_3_Histogram.png)

---

## Strategy Overview

Each month:
1. Compute the **12–1 momentum signal** for each stock - past 12 months of returns, skipping the most recent month to reduce noise
2. Rank all stocks by signal
3. Go **long-only the top 10%**, equally weighted
4. Apply **volatility targeting** to scale exposure toward a fixed risk budget

Volatility targeting changes *how much capital is deployed*, not *which stocks are selected*.

---

## Signal Definition

```
Momentum_12-1(t) = P(t-1) / P(t-12) - 1
```

- Month-end adjusted prices
- Most recent month excluded (reduces short-term reversal noise)
- Signal at month `t` predicts returns at month `t+1` — no look-ahead bias

---

## Volatility Targeting

The baseline momentum strategy exhibits large time-varying drawdowns. Volatility targeting addresses this:

- Estimate realized strategy volatility using a rolling 12-month window
- Scale exposure so expected volatility stays near a **fixed 6% monthly target**
- Apply a **2× leverage cap** to prevent extreme positions
- Stock selection is unchanged - only position size adjusts

Result: substantially smoother equity curve and reduced drawdowns without altering the underlying signal.

---

## Portfolio Construction

| Parameter | Value |
|---|---|
| Rebalancing | Monthly |
| Selection | Top 10% by momentum signal |
| Weighting | Equal-weighted |
| Direction | Long-only |
| Transaction costs | 0 (diagnostic purposes) |
| Avg monthly turnover | ~49% |

---

## Repository Structure

```
├── src/
│   ├── data_clean.py       # Price cleaning, monthly conversion
│   ├── signals.py          # Momentum signal construction
│   ├── backtest.py         # Portfolio construction & backtest engine
│   └── metrics.py          # Sharpe ratio, max drawdown
├── scripts/
│   └── run_backtest.py     # End-to-end backtest runner
├── notebooks/              # Exploration and analysis
├── data/
│   ├── raw/
│   ├── processed/
│   └── outputs/            # Figures and results
├── reports/
│   └── report.md           # Full methodology report
├── README.md
└── requirements.txt
```

---

## Quickstart

```bash
pip install -r requirements.txt
python -m scripts.run_backtest
```

Outputs saved to `data/outputs/`.

---

## Limitations

- Yahoo Finance data (not institutional-grade)
- Fixed universe may introduce survivorship bias
- Zero transaction costs - real performance would be lower
- Results demonstrate correct methodology, not production performance

---

## Possible Extensions

- Sector-neutral portfolio construction
- Market regime filters (e.g. trend following overlay)
- Alternative signal definitions (earnings momentum, analyst revisions)
- ML-based ranking models - see [`ml-alpha-ranker`](https://github.com/stefsamaha/ml-alpha-ranker) which builds directly on this baseline