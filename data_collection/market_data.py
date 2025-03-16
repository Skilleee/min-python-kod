import yfinance as yf
import logging
from datetime import datetime

# Skapa en loggfil
logging.basicConfig(filename="market_data.log", level=logging.INFO)


# Funktion för att hämta aktiepriser från Yahoo Finance
def fetch_stock_price(symbol):
    """
    Hämtar den senaste aktiekursen för ett givet aktiesymbol (t.ex. 'AAPL', 'TSLA') från Yahoo Finance.
    """
    try:
        stock = yf.Ticker(symbol)
        latest_price = stock.history(period="1d")["Close"][-1]
        logging.info(
            f"[{datetime.now()}] ✅ Hämtade data för {symbol}: {latest_price} USD"
        )
        return latest_price
    except Exception as e:
        logging.error(f"[{datetime.now()}] ❌ Fel vid hämtning av {symbol}: {str(e)}")
        return None


# Funktion för att hämta flera aktier samtidigt
def fetch_multiple_stocks(symbols):
    """
    Hämtar senaste priser för en lista av aktier från Yahoo Finance.
    """
    stock_prices = {}
    for symbol in symbols:
        price = fetch_stock_price(symbol)
        if price:
            stock_prices[symbol] = price
    return stock_prices


# Funktion för att hämta valutakurser från Yahoo Finance
def fetch_forex_data(base_currency, quote_currency):
    """
    Hämtar realtids växelkurs mellan två valutor, t.ex. USD/SEK från Yahoo Finance.
    """
    try:
        forex_pair = f"{base_currency}{quote_currency}=X"
        forex_price = fetch_stock_price(forex_pair)
        logging.info(
            f"[{datetime.now()}] 💱 Växelkurs {base_currency}/{quote_currency}: {forex_price}"
        )
        return forex_price
    except Exception as e:
        logging.error(
            f"[{datetime.now()}] ❌ Fel vid hämtning av växelkurs {base_currency}/{quote_currency}: {str(e)}"
        )
        return None


# Funktion för att hämta råvarupriser från Yahoo Finance
def fetch_commodity_price(commodity):
    """
    Hämtar realtidspris för råvaror, t.ex. guld (XAU/USD) eller olja (WTI).
    """
    commodity_map = {"gold": "GC=F", "silver": "SI=F", "oil": "CL=F"}

    if commodity not in commodity_map:
        logging.error(f"[{datetime.now()}] ❌ Ogiltig råvara: {commodity}")
        return None

    return fetch_stock_price(commodity_map[commodity])


# Funktion för att hämta orderflöden (simulerad för Yahoo Finance)
def fetch_order_flow(symbol):
    """
    Simulerar analys av orderflöden och likviditet för en aktie.
    """
    try:
        # Simulerad data för orderflöde
        order_flow_data = {
            "buy_orders": 1200,
            "sell_orders": 800,
            "net_flow": 400,  # Positivt värde indikerar köparövertag
        }
        logging.info(
            f"[{datetime.now()}] 📊 Orderflöde för {symbol}: {order_flow_data}"
        )
        return order_flow_data
    except Exception as e:
        logging.error(
            f"[{datetime.now()}] ❌ Fel vid hämtning av orderflöde för {symbol}: {str(e)}"
        )
        return None


# Exempelanrop
if __name__ == "__main__":
    aktier = ["AAPL", "TSLA", "NVDA"]
    priser = fetch_multiple_stocks(aktier)
    print(f"📈 Senaste aktiepriser: {priser}")

    sek_usd_kurs = fetch_forex_data("USD", "SEK")
    print(f"💱 USD/SEK: {sek_usd_kurs}")

    guldpris = fetch_commodity_price("gold")
    print(f"🟡 Guldpris: {guldpris} USD")

    order_flow = fetch_order_flow("AAPL")
    print(f"📊 Orderflöde AAPL: {order_flow}")
