import numpy as np
import pandas as pd
import logging
from scipy.optimize import minimize

# Konfigurera loggning
logging.basicConfig(filename="portfolio_optimization.log", level=logging.INFO)


def optimize_portfolio(returns, risk_tolerance=0.5):
    """
    Optimerar portföljens viktning baserat på risk/reward.
    """
    try:
        cov_matrix = returns.cov()
        num_assets = len(returns.columns)
        weights = np.ones(num_assets) / num_assets

        def portfolio_volatility(weights):
            return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

        constraints = {"type": "eq", "fun": lambda w: np.sum(w) - 1}
        bounds = tuple((0, 1) for _ in range(num_assets))
        result = minimize(
            portfolio_volatility,
            weights,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )

        optimized_weights = result.x
        optimized_portfolio = dict(zip(returns.columns, optimized_weights))

        logging.info("✅ Portföljoptimering genomförd.")
        return optimized_portfolio
    except Exception as e:
        logging.error(f"❌ Fel vid portföljoptimering: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    np.random.seed(42)
    stock_returns = pd.DataFrame(
        np.random.randn(100, 4) / 100, columns=["AAPL", "TSLA", "NVDA", "MSFT"]
    )

    optimal_weights = optimize_portfolio(stock_returns)
    print("📢 Optimerad portföljviktning:", optimal_weights)
