import pandas as pd
import numpy as np
import logging

# Konfigurera loggning
logging.basicConfig(filename="live_market_analysis.log", level=logging.INFO)


def analyze_market_conditions(data):
    """
    Analyserar marknadens tillstånd baserat på volatilitet och trender.
    """
    try:
        data["volatility"] = data["close"].pct_change().rolling(window=20).std()
        data["market_trend"] = np.where(
            data["close"].rolling(window=50).mean()
            > data["close"].rolling(window=200).mean(),
            "Bullish",
            "Bearish",
        )

        logging.info("✅ Marknadsanalys genomförd.")
        return data[["date", "close", "volatility", "market_trend"]]
    except Exception as e:
        logging.error(f"❌ Fel vid marknadsanalys: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    df = pd.DataFrame(
        {
            "date": pd.date_range(start="2023-01-01", periods=300),
            "close": np.cumsum(np.random.randn(300) * 2 + 100),
        }
    )

    market_analysis = analyze_market_conditions(df)
    print("📢 Marknadsanalys:")
    print(market_analysis.tail())
