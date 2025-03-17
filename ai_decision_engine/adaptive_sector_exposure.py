import logging

import numpy as np
import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="adaptive_sector_exposure.log", level=logging.INFO)


def analyze_sector_performance(market_data):
    """
    Analyserar sektorer baserat på marknadsdata och returnerar rekommenderade sektorer.
    """
    try:
        sector_performance = (
            market_data.groupby("sector")["return"].mean().sort_values(ascending=False)
        )
        top_sectors = sector_performance.head(3).index.tolist()
        bottom_sectors = sector_performance.tail(3).index.tolist()
        logging.info(
            f"✅ Bästa sektorer: {top_sectors}, Sämsta sektorer: {bottom_sectors}"
        )
        return top_sectors, bottom_sectors
    except Exception as e:
        logging.error(f"❌ Fel vid sektoranalys: {str(e)}")
        return None, None


def adjust_sector_exposure(portfolio, top_sectors, bottom_sectors):
    """
    Justerar portföljens exponering genom att öka allokeringen i de starkaste sektorerna och minska i de svagaste.
    """
    try:
        portfolio["adjustment"] = portfolio["sector"].apply(
            lambda x: (
                0.05 if x in top_sectors else (-0.05 if x in bottom_sectors else 0)
            )
        )
        portfolio["new_allocation"] = portfolio["allocation"] + portfolio["adjustment"]
        portfolio["new_allocation"] = np.clip(
            portfolio["new_allocation"], 0, 1
        )  # Säkerställer att allokeringen ligger mellan 0-100%
        logging.info("✅ Sektorexponering justerad i portföljen.")
        return portfolio
    except Exception as e:
        logging.error(f"❌ Fel vid justering av sektorexponering: {str(e)}")
        return portfolio


# Exempelanrop
if __name__ == "__main__":
    # Simulerad marknadsdata
    market_data = pd.DataFrame(
        {
            "sector": ["Tech", "Finance", "Healthcare", "Energy", "Tech", "Finance"],
            "return": [0.12, 0.05, -0.02, 0.08, 0.15, 0.02],
        }
    )

    # Simulerad portfölj
    portfolio = pd.DataFrame(
        {
            "symbol": ["AAPL", "JPM", "PFE", "XOM", "GOOGL"],
            "sector": ["Tech", "Finance", "Healthcare", "Energy", "Tech"],
            "allocation": [0.20, 0.15, 0.10, 0.25, 0.30],
        }
    )

    top_sectors, bottom_sectors = analyze_sector_performance(market_data)
    portfolio = adjust_sector_exposure(portfolio, top_sectors, bottom_sectors)
    print("📊 Uppdaterad sektorexponering i portföljen:")
    print(portfolio)
