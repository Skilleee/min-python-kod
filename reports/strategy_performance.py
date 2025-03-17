import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="strategy_performance.log", level=logging.INFO)


def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
    """
    Beräknar Sharpe-kvoten för att mäta riskjusterad avkastning.
    """
    try:
        excess_returns = returns - risk_free_rate / 252
        sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns)
        logging.info(f"✅ Sharpe Ratio beräknad: {sharpe_ratio:.2f}")
        return sharpe_ratio
    except Exception as e:
        logging.error(f"❌ Fel vid beräkning av Sharpe Ratio: {str(e)}")
        return None


def calculate_sortino_ratio(returns, risk_free_rate=0.02):
    """
    Beräknar Sortino-kvoten, som fokuserar på nedsiderisk.
    """
    try:
        downside_returns = returns[returns < 0]
        downside_deviation = np.std(downside_returns)
        excess_returns = returns - risk_free_rate / 252
        sortino_ratio = np.mean(excess_returns) / downside_deviation
        logging.info(f"✅ Sortino Ratio beräknad: {sortino_ratio:.2f}")
        return sortino_ratio
    except Exception as e:
        logging.error(f"❌ Fel vid beräkning av Sortino Ratio: {str(e)}")
        return None


def plot_strategy_performance(trade_log, output_file="strategy_performance.png"):
    """
    Skapar en diagram över handelsstrategins avkastning.
    """
    try:
        trade_log["Cumulative Returns"] = (1 + trade_log["return"]).cumprod()
        plt.figure(figsize=(10, 5))
        plt.plot(
            trade_log["Cumulative Returns"], label="Strategins Avkastning", color="blue"
        )
        plt.axhline(y=1, color="gray", linestyle="--", label="Startvärde")
        plt.legend()
        plt.title("Strategins Prestanda")
        plt.xlabel("Handel")
        plt.ylabel("Avkastning")
        plt.savefig(output_file)
        plt.close()
        logging.info("✅ Strategins prestandadiagram genererat.")
    except Exception as e:
        logging.error(f"❌ Fel vid skapande av prestandadiagram: {str(e)}")


# Exempelanrop
if __name__ == "__main__":
    # Simulerad handelslogg
    trade_log = pd.DataFrame(
        {
            "symbol": ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL"],
            "entry_price": [150, 700, 250, 300, 2800],
            "exit_price": [155, 680, 270, 310, 2900],
            "return": [0.033, -0.028, 0.08, 0.033, 0.035],
            "trade_date": pd.date_range(start="2023-01-01", periods=5),
        }
    )

    sharpe = calculate_sharpe_ratio(trade_log["return"])
    sortino = calculate_sortino_ratio(trade_log["return"])
    print(f"📊 Sharpe Ratio: {sharpe:.2f}")
    print(f"📉 Sortino Ratio: {sortino:.2f}")

    plot_strategy_performance(trade_log)
    print("📈 Strategins prestandadiagram skapad: strategy_performance.png")
