# Cross-Sectional Momentum (Long-Only) with Volatility Targeting

## 1. Objective

The objective of this project is to build and analyze a simple systematic equity strategy based on **cross-sectional momentum**, and to understand how **risk management** affects its performance.

The project focuses on:
- selecting stocks using a momentum signal
- constructing a long-only portfolio
- evaluating performance using a realistic backtest
- improving the strategy through volatility-based position sizing

The goal is not to maximize returns, but to demonstrate a clear and correct **quant research workflow** from data to conclusions.

---

## 2. Data

- **Source:** Yahoo Finance (`yfinance`, adjusted prices)
- **Frequency:** Monthly (month-end prices)
- **Universe:** Fixed list of large-cap U.S. equities

### Notes
- The data source and universe are chosen for learning purposes.
- Survivorship bias may be present and is accepted for this project.
- The emphasis is on methodology rather than production-ready results.

---

## 3. Signal Definition: Momentum (12–1)

For each stock and each month \( t \), momentum is defined as:

\[
\text{Momentum}_{12-1}(t) = \frac{P(t-1)}{P(t-12)} - 1
\]

where \( P(t) \) is the month-end adjusted price.

### Interpretation
- Stocks with higher values have performed better over the past year.
- The most recent month is excluded to reduce short-term noise and avoid look-ahead bias.

---

## 4. Portfolio Construction (Long-Only)

The strategy is rebalanced monthly.

At each month-end:
1. Stocks are ranked by their momentum score.
2. The **top 10%** of stocks are selected.
3. Capital is allocated **equally** across the selected stocks.
4. All positions are long-only (no short selling).

This construction isolates stock selection skill and avoids leverage or market timing assumptions.

---

## 5. Backtest Methodology

### Look-ahead bias
Portfolio weights decided at month \( t \) are applied to returns realized in month \( t+1 \), ensuring that only information available at the time of decision is used.

### Transaction costs
Transaction costs are set to zero in the main experiments to focus on signal behavior and risk dynamics. Turnover is tracked for diagnostic purposes.

---

## 6. Risk Management: Volatility Targeting

The baseline long-only momentum strategy exhibits large drawdowns due to time-varying volatility.

To address this, **volatility targeting** is applied:
- Strategy volatility is estimated using a rolling 12-month window of past returns.
- Portfolio exposure is scaled so that expected volatility stays near a fixed target.

### Key idea
- When recent volatility is high, exposure is reduced.
- When volatility is low, exposure is increased.
- Stock selection remains unchanged; only **position size** is adjusted.

The final configuration targets **6% monthly volatility**, with a leverage cap of 2×.

---

## 7. Evaluation Metrics

Performance is evaluated using:
- Equity curve (growth of $1)
- Annualized Sharpe ratio
- Maximum drawdown
- Rolling volatility

Visual inspection of equity and drawdown curves is used alongside summary statistics.

---

## 8. Results and Observations

- The baseline long-only momentum strategy shows strong long-term performance but large drawdowns.
- Volatility targeting substantially smooths the equity curve and reduces drawdowns.
- At the chosen volatility target, the risk-controlled strategy achieves higher long-term performance than the unscaled baseline.
- Improvements come from **risk control**, not changes to the underlying signal.

---

## 9. Conclusions

This project shows that:
- Cross-sectional momentum is an effective stock selection signal.
- Long-only momentum captures most of the available alpha in this setting.
- Risk management is essential for making a strategy practically usable.
- Volatility targeting is a simple and effective way to stabilize returns without altering stock selection.

The final strategy represents a clean and interpretable baseline for further research.

---

## 10. Possible Extensions

- Market regime filters
- Sector-neutral portfolio construction
- Alternative momentum definitions
- Larger or cleaner datasets
- Machine learning models for stock ranking
