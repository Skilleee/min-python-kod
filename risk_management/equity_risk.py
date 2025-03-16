import numpy as np
import pandas as pd
import logging
from scipy.stats import norm

# Konfigurera loggning
logging.basicConfig(filename="equity_risk.log", level=logging.INFO)

def calculate_volatility(price_series, window=30):
    """
    Beräknar volatilitet för aktier över ett valt tidsfönster.
    """
    try:
        volatility = price_series.pct_change().rolling(window=window).std()
        logging.info(f"✅ Volatilitet beräknad över {window} dagar.")
        return volatility
    except Exception as e:
        logging.error(f"❌ Fel vid beräkning av volatilitet: {str(e)}")
        return None

def calculate_max_drawdown(price_series):
    """
    Beräknar max drawdown för att mäta den största nedgången från en topp till en botten.
    """
    try:
        cumulative_returns = (1 + price_series.pct_change()).cumprod()
        peak = cumulative_returns.cummax()
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = drawdown.min()
        logging.info(f"✅ Max Drawdown beräknad: {max_drawdown:.2%}")
        return max_drawdown
    except Exception as e:
        logging.error(f"❌ Fel vid beräkning av max drawdown: {str(e)}")
        return None

def value_at_risk(price_series, confidence_level=0.95, window=30):
    """
    Beräknar Value at Risk (VaR) för att mäta potentiell förlust med en viss sannolikhet.
    """
    try:
        daily_returns = price_series.pct_change().dropna()
        var = np.percentile(daily_returns, (1 - confidence_level) * 100)
        logging.info(f"✅ Value at Risk (VaR) beräknad vid {confidence_level:.0%} konfidens: {var:.2%}")
        return var
    except Exception as e:
        logging.error(f"❌ Fel vid beräkning av Value at Risk: {str(e)}")
        return None

def risk_score(price_series, window=30):
    """
    Kombinerar volatilitet, max drawdown och VaR för att generera en riskpoäng.
    """
    try:
        vol = calculate_volatility(price_series, window)
        drawdown = calculate_max_drawdown(price_series)
        var = value_at_risk(price_series, confidence_level=0.95, window=window)
        
        if vol is not None and drawdown is not None and var is not None:
            risk_score = (vol.mean() + abs(drawdown) + abs(var)) / 3
            logging.info(f"✅ Riskpoäng beräknad: {risk_score:.2f}")
            return risk_score
        else:
            return None
    except Exception as e:
        logging.error(f"❌ Fel vid riskpoängsberäkning: {str(e)}")
        return None

# Exempelanrop
if __name__ == "__main__":
    # Simulerad aktieprisdata
    np.random.seed(42)
    simulated_prices = pd.Series(np.cumsum(np.random.randn(100)) + 100)
    
    volatility = calculate_volatility(simulated_prices)
    print(f"Volatilitet:
{volatility.tail()}")
    
    max_dd = calculate_max_drawdown(simulated_prices)
    print(f"Max Drawdown: {max_dd:.2%}")
    
    var = value_at_risk(simulated_prices)
    print(f"Value at Risk (VaR): {var:.2%}")
    
    risk = risk_score(simulated_prices)
    print(f"Riskpoäng: {risk:.2f}")
