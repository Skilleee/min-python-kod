import schedule
import time
import logging
from datetime import datetime

# Importera nödvändiga moduler
from ai_trading_bot.data_collection.market_data import fetch_multiple_stocks
from ai_trading_bot.ai_decision_engine.strategy_generation import generate_trading_signal
from ai_trading_bot.notifications.telegram_alert import send_telegram_alert

# Konfigurera loggning
logging.basicConfig(filename="bot_scheduler.log", level=logging.INFO)

def trading_routine():
    """
    Huvudrutinen för AI-trading boten. Hämtar marknadsdata, genererar signaler och skickar aviseringar.
    """
    try:
        logging.info("⏳ Startar trading-rutin...")
        stocks = ["AAPL", "TSLA", "NVDA"]  # Exempelaktier att analysera
        market_data = fetch_multiple_stocks(stocks)
        
        signals = {}
        for stock, price in market_data.items():
            signals[stock] = generate_trading_signal(stock, price)
        
        send_telegram_alert(f"📢 AI-Trading Uppdatering: {signals}")
        logging.info("✅ Trading-rutin genomförd framgångsrikt.")
    except Exception as e:
        logging.error(f"❌ Fel i trading-rutin: {str(e)}")

# Schemaläggning av botens uppgifter
schedule.every().day.at("09:00").do(trading_routine)  # Körs varje dag kl 09:00
schedule.every(30).minutes.do(trading_routine)  # Uppdaterar var 30:e minut

if __name__ == "__main__":
    logging.info("🚀 Startar AI-Trading Bot Scheduler...")
    while True:
        schedule.run_pending()
        time.sleep(1)
