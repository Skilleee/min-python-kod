import numpy as np
import pandas as pd
import logging

# Konfigurera loggning
logging.basicConfig(filename="seasonality_decision.log", level=logging.INFO)

def analyze_seasonality(historical_data):
    """
    Analyserar säsongsmönster i marknaden baserat på historiska data.
    """
    try:
        historical_data["month"] = historical_data["date"].dt.month
        seasonal_performance = historical_data.groupby("month")["return"].mean()
        best_months = seasonal_performance.nlargest(3).index.tolist()
        worst_months = seasonal_performance.nsmallest(3).index.tolist()
        
        logging.info(f"Identifierade säsongsmönster. Bästa månader: {best_months}, Sämsta månader: {worst_months}")
        return best_months, worst_months
    except Exception as e:
        logging.error(f"Fel vid analys av säsongsmönster: {str(e)}")
        return None, None

def adjust_decision_based_on_seasonality(historical_data, trade_log):
    """
    Justerar handelsbeslut baserat på identifierade säsongsmönster.
    """
    try:
        best_months, worst_months = analyze_seasonality(historical_data)
        if best_months is None:
            return None
        
        trade_log["month"] = trade_log["trade_date"].dt.month
        adjusted_decision = pd.Series("HOLD", index=trade_log.index)
        adjusted_decision[trade_log["month"].isin(best_months)] = "BUY"
        adjusted_decision[trade_log["month"].isin(worst_months)] = "SELL"
        
        logging.info("Beslut justerade baserat på säsongsmönster.")
        return adjusted_decision
    except Exception as e:
        logging.error(f"Fel vid justering av beslut baserat på säsongsmönster: {str(e)}")
        return None

# Exempelanrop
if __name__ == "__main__":
    # Simulerad historisk data
    np.random.seed(42)
    dates = pd.date_range(start="2015-01-01", periods=2000, freq="D")
    returns = np.random.randn(2000) / 100
    historical_data = pd.DataFrame({"date": dates, "return": returns})
    
    # Simulerad handelslogg
    trade_log = pd.DataFrame({
        "symbol": ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL"],
        "entry_price": [150, 700, 250, 300, 2800],
        "exit_price": [155, 680, 270, 310, 2900],
        "trade_date": pd.date_range(start="2023-01-01", periods=5)
    })
    
    seasonal_adjusted_decision = adjust_decision_based_on_seasonality(historical_data, trade_log)
    print(f"Säsongsjusterade beslut:")
    print(seasonal_adjusted_decision)
