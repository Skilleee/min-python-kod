import logging
from data_collection.market_data import fetch_market_data
from data_collection.portfolio_google_sheets import load_portfolio_data
from data_collection.sentiment_analysis import analyze_sentiment
from data_collection.macro_data import fetch_macro_data
from data_collection.news_analysis import analyze_market_news
from data_processing.normalization import normalize_data
from data_processing.volatility_analysis import analyze_volatility
from ai_decision_engine.strategy_generation import generate_trading_strategy
from ai_decision_engine.optimal_entry_exit import optimal_entry_exit_strategy
from ai_decision_engine.execution_feedback import refine_strategy
from risk_management.adaptive_stop_loss import adaptive_stop_loss
from risk_management.value_at_risk import calculate_var
from risk_management.monte_carlo_simulation import monte_carlo_simulation
from portfolio_management.rebalancing import rebalancing
from portfolio_management.hedging_strategies import hedging_strategies
from reports.generate_report import generate_report
from reports.weekly_market_report import generate_weekly_report
from reports.macro_event_impact import analyze_macro_event
from live_trading.live_signal_generator import generate_live_signals
from live_trading.telegram_signal_sender import send_telegram_alerts
from utils.bot_scheduler import schedule_tasks
from utils.process_manager import manage_processes

def main():
    logging.info("🚀 AI Trading Bot startar...")
    
    # Hämta och bearbeta data
    market_data = fetch_market_data()
    portfolio_data = load_portfolio_data()
    sentiment = analyze_sentiment()
    macro_data = fetch_macro_data()
    news = analyze_market_news()
    
    # Förbered data
    normalized_data = normalize_data(market_data)
    volatility = analyze_volatility(market_data)
    
    # AI Beslutsfattande
    strategy = generate_trading_strategy(normalized_data, sentiment, macro_data)
    optimal_entry = optimal_entry_exit_strategy(strategy)
    refined_strategy = refine_strategy(optimal_entry, execution_feedback=True)
    
    # Riskhantering
    stop_loss = adaptive_stop_loss(refined_strategy)
    var_analysis = calculate_var(market_data)
    monte_carlo_sim = monte_carlo_simulation(100000, 0.07, 0.2)
    
    # Portföljhantering
    rebalanced_portfolio = rebalancing(portfolio_data, refined_strategy)
    hedging_plan = hedging_strategies(rebalanced_portfolio)
    
    # Generera rapporter
    generate_report(rebalanced_portfolio)
    generate_weekly_report(market_data)
    analyze_macro_event(macro_data)
    
    # Live Trading Signalering
    live_signals = generate_live_signals(market_data)
    send_telegram_alerts(live_signals)
    
    # Systemhantering
    schedule_tasks()
    manage_processes()
    
    logging.info("✅ AI Trading Bot körs och analyserar marknaden.")

if __name__ == "__main__":
    main()
