import numpy as np
import pandas as pd
import logging
from datetime import datetime

# Konfigurera loggning
logging.basicConfig(filename="strategy_generation.log", level=logging.INFO)

# Funktion för att generera en enkel momentum-baserad strategi
def generate_momentum_strategy(data, short_window=20, long_window=50):
    """
    Genererar en momentum-baserad strategi genom att jämföra korta och långa glidande medelvärden.
    """
    try:
        data["short_ma"] = data["close"].rolling(window=short_window).mean()
        data["long_ma"] = data["close"].rolling(window=long_window).mean()
        data["signal"] = np.where(data["short_ma"] > data["long_ma"], 1, -1)
        
        logging.info(f"[{datetime.now()}] ✅ Momentum-strategi genererad med {short_window}/{long_window} glidande medelvärden.")
        return data[["close", "short_ma", "long_ma", "signal"]]
    except Exception as e:
        logging.error(f"[{datetime.now()}] ❌ Fel vid generering av momentum-strategi: {str(e)}")
        return None

# Funktion för att generera en mean reversion-strategi
def generate_mean_reversion_strategy(data, window=50, threshold=2):
    """
    Genererar en mean reversion-strategi genom att analysera Bollinger Bands.
    """
    try:
        data["moving_avg"] = data["close"].rolling(window=window).mean()
        data["std_dev"] = data["close"].rolling(window=window).std()
        data["upper_band"] = data["moving_avg"] + (threshold * data["std_dev"])
        data["lower_band"] = data["moving_avg"] - (threshold * data["std_dev"])
        data["signal"] = np.where(data["close"] < data["lower_band"], 1, np.where(data["close"] > data["upper_band"], -1, 0))
        
        logging.info(f"[{datetime.now()}] ✅ Mean reversion-strategi genererad med {window}-dagars Bollinger Bands.")
        return data[["close", "moving_avg", "upper_band", "lower_band", "signal"]]
    except Exception as e:
        logging.error(f"[{datetime.now()}] ❌ Fel vid generering av mean reversion-strategi: {str(e)}")
        return None

# Funktion för att kombinera strategier
def combine_strategies(momentum_data, mean_reversion_data):
    """
    Kombinerar momentum och mean reversion-strategier för att skapa en hybridstrategi.
    """
    try:
        combined_data = momentum_data.copy()
        combined_data["combined_signal"] = momentum_data["signal"] + mean_reversion_data["signal"]
        
        logging.info(f"[{datetime.now()}] ✅ Strategier kombinerade till en hybridmodell.")
        return combined_data[["close", "combined_signal"]]
    except Exception as e:
        logging.error(f"[{datetime.now()}] ❌ Fel vid kombination av strategier: {str(e)}")
        return None

# Exempelanrop
if __name__ == "__main__":
    # Simulerad prisdata
    np.random.seed(42)
    dates = pd.date_range(start="2023-01-01", periods=200, freq="D")
    prices = np.cumsum(np.random.randn(200) * 2 + 100)
    stock_data = pd.DataFrame({"date": dates, "close": prices})
    
    momentum_strategy = generate_momentum_strategy(stock_data)
    print(f"📈 Momentum-strategi:")
    print(momentum_strategy.tail())
    
    mean_reversion_strategy = generate_mean_reversion_strategy(stock_data)
    print(f"📊 Mean Reversion-strategi:")
    print(mean_reversion_strategy.tail())
    
    combined_strategy = combine_strategies(momentum_strategy, mean_reversion_strategy)
    print(f"🔀 Hybridstrategi:")
    print(combined_strategy.tail())
