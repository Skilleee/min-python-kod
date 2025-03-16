import numpy as np
import pandas as pd
import logging

# Konfigurera loggning
logging.basicConfig(filename="execution_feedback.log", level=logging.INFO)

def evaluate_trade_performance(trade_log):
    """
    Utvärderar hur väl tidigare rekommendationer har presterat baserat på faktiska marknadsrörelser.
    """
    try:
        trade_log["return"] = (trade_log["exit_price"] - trade_log["entry_price"]) / trade_log["entry_price"]
        trade_log["win"] = trade_log["return"] > 0
        win_rate = trade_log["win"].mean()
        avg_return = trade_log["return"].mean()
        
        logging.info(f"✅ Handelsutvärdering klar: Win rate: {win_rate:.2%}, Genomsnittlig avkastning: {avg_return:.2%}")
        return {"win_rate": win_rate, "avg_return": avg_return}
    except Exception as e:
        logging.error(f"❌ Fel vid handelsutvärdering: {str(e)}")
        return None

def refine_trading_strategy(trade_log, threshold=0.02):
    """
    Förbättrar strategin genom att analysera vilka signaler som fungerade bäst och justera framtida beslut.
    """
    try:
        good_trades = trade_log[trade_log["return"] > threshold]
        bad_trades = trade_log[trade_log["return"] < -threshold]
        
        logging.info(f"✅ Strategianalys klar: {len(good_trades)} bra trades, {len(bad_trades)} dåliga trades")
        return {"good_trades": len(good_trades), "bad_trades": len(bad_trades)}
    except Exception as e:
        logging.error(f"❌ Fel vid strategianalys: {str(e)}")
        return None

# Exempelanrop
if __name__ == "__main__":
    # Simulerad handelslogg
    trade_log = pd.DataFrame({
        "symbol": ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL"],
        "entry_price": [150, 700, 250, 300, 2800],
        "exit_price": [155, 680, 270, 310, 2900],
        "trade_date": pd.date_range(start="2023-01-01", periods=5)
    })
    
    performance = evaluate_trade_performance(trade_log)
    print(f"Handelsutvärdering:
{performance}")
    
    strategy_refinement = refine_trading_strategy(trade_log)
    print(f"Justerad strategi:
{strategy_refinement}")
