import numpy as np
import pandas as pd
import logging

# Konfigurera loggning
logging.basicConfig(filename="macro_influence_decision.log", level=logging.INFO)

def analyze_macro_factors(macro_data):
    """
    Analyserar makroekonomiska faktorer och returnerar en påverkningspoäng.
    """
    try:
        interest_rate_impact = -macro_data["interest_rate_change"]  # Högre räntor påverkar negativt
        inflation_impact = -macro_data["inflation_rate"] * 0.5  # Hög inflation påverkar marknaden negativt
        gdp_growth_impact = macro_data["gdp_growth"] * 0.7  # Högre BNP-tillväxt är positivt
        
        macro_score = interest_rate_impact + inflation_impact + gdp_growth_impact
        logging.info(f"Makroekonomisk påverkan beräknad: {macro_score:.4f}")
        return macro_score
    except Exception as e:
        logging.error(f"Fel vid analys av makrofaktorer: {str(e)}")
        return None

def adjust_decision_based_on_macro(macro_data, trade_log, threshold=0.5):
    """
    Justerar handelsbeslut baserat på makroekonomiska faktorer.
    """
    try:
        macro_score = analyze_macro_factors(macro_data)
        if macro_score is None:
            return None
        
        adjusted_decision = pd.Series("HOLD", index=trade_log.index)
        adjusted_decision[(macro_score > threshold)] = "BUY"
        adjusted_decision[(macro_score < -threshold)] = "SELL"
        
        logging.info("Makroekonomiskt justerade beslut genererade.")
        return adjusted_decision
    except Exception as e:
        logging.error(f"Fel vid justering av beslut baserat på makrofaktorer: {str(e)}")
        return None

# Exempelanrop
if __name__ == "__main__":
    # Simulerad makrodata
    macro_data = pd.DataFrame({
        "interest_rate_change": [0.25],
        "inflation_rate": [2.5],
        "gdp_growth": [3.0]
    })
    
    # Simulerad handelslogg
    trade_log = pd.DataFrame({
        "symbol": ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL"],
        "entry_price": [150, 700, 250, 300, 2800],
        "exit_price": [155, 680, 270, 310, 2900],
        "trade_date": pd.date_range(start="2023-01-01", periods=5)
    })
    
    macro_adjusted_decision = adjust_decision_based_on_macro(macro_data, trade_log)
    print(f"Makroekonomiskt justerade beslut:")
    print(macro_adjusted_decision)
