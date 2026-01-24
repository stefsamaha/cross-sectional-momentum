import matplotlib.pyplot as plt
import pandas as pd


def plot_equity(res: pd.DataFrame, title: str = "Equity Curve"):
    """
    Plot growth of $1 over time.
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(res.index, res["equity"])
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Equity (growth of $1)")

    ax.grid(True)
    plt.tight_layout()
    plt.show()


def plot_drawdown(res: pd.DataFrame, title: str = "Drawdown"):
    """
    Plot drawdown over time.
    Drawdown = current equity / past peak - 1
    """
    equity = res["equity"]
    peak = equity.cummax()
    drawdown = equity / peak - 1.0

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(drawdown.index, drawdown)
    ax.axhline(0.0)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown")

    ax.grid(True)
    plt.tight_layout()
    plt.show()


def plot_returns_hist(res: pd.DataFrame, title: str = "Monthly Net Returns"):
    """
    Plot histogram of monthly net returns.
    """
    fig, ax = plt.subplots(figsize=(8, 4))

    ax.hist(res["net_return"], bins=40)
    ax.set_title(title)
    ax.set_xlabel("Monthly return")
    ax.set_ylabel("Frequency")

    ax.grid(True)
    plt.tight_layout()
    plt.show()
