import logging
from datetime import datetime

import requests
from textblob import TextBlob

# Konfigurera loggning
logging.basicConfig(filename="sentiment_analysis.log", level=logging.INFO)

# API-konfiguration för Twitter, Reddit eller nyhetskällor (valfri expansion)
TWITTER_API_URL = "https://api.twitter.com/2/tweets/search/recent"
REDDIT_API_URL = "https://www.reddit.com/r/stocks/new.json"
NEWS_API_URL = "https://newsapi.org/v2/everything"


# Funktion för att hämta tweets (Placeholder, API-nyckel behövs)
def fetch_tweets(keyword, count=10):
    """
    Hämtar de senaste tweets relaterade till en viss aktie eller marknad.
    """
    try:
        headers = {
            "Authorization": "Bearer YOUR_TWITTER_BEARER_TOKEN"
        }  # Ersätt med giltig API-nyckel
        params = {"query": keyword, "max_results": count, "tweet.fields": "text"}
        response = requests.get(TWITTER_API_URL, headers=headers, params=params)
        data = response.json()
        tweets = [tweet["text"] for tweet in data.get("data", [])]
        logging.info(
            f"[{datetime.now()}] ✅ Hämtade {len(tweets)} tweets för {keyword}"
        )
        return tweets
    except Exception as e:
        logging.error(
            f"[{datetime.now()}] ❌ Fel vid hämtning av tweets för {keyword}: {str(e)}"
        )
        return []


# Funktion för att hämta Reddit-inlägg
def fetch_reddit_posts(subreddit="stocks", count=10):
    """
    Hämtar de senaste inläggen från Reddit inom en viss subreddit.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(REDDIT_API_URL, headers=headers)
        data = response.json()
        posts = [
            post["data"]["title"]
            for post in data.get("data", {}).get("children", [])[:count]
        ]
        logging.info(
            f"[{datetime.now()}] ✅ Hämtade {len(posts)} Reddit-inlägg från {subreddit}"
        )
        return posts
    except Exception as e:
        logging.error(
            f"[{datetime.now()}] ❌ Fel vid hämtning av Reddit-inlägg: {str(e)}"
        )
        return []


# Funktion för att analysera sentiment
def analyze_sentiment(texts):
    """
    Använder TextBlob för att analysera sentiment i textdata.
    """
    if not texts:
        return "neutral"

    total_polarity = sum(TextBlob(text).sentiment.polarity for text in texts) / len(
        texts
    )
    sentiment = (
        "positivt"
        if total_polarity > 0
        else "negativt" if total_polarity < 0 else "neutral"
    )

    logging.info(
        f"[{datetime.now()}] 📊 Sentimentanalys: {sentiment} (Polarity: {total_polarity})"
    )
    return sentiment


# Funktion för att hämta och analysera sentiment
def fetch_and_analyze_sentiment(keyword):
    """
    Hämtar tweets och Reddit-inlägg för en aktie och analyserar sentimentet.
    """
    tweets = fetch_tweets(keyword)
    reddit_posts = fetch_reddit_posts()
    all_texts = tweets + reddit_posts
    sentiment = analyze_sentiment(all_texts)
    return sentiment


# Exempelanrop
if __name__ == "__main__":
    stock_sentiment = fetch_and_analyze_sentiment("AAPL")
    print(f"📢 Sentiment för AAPL: {stock_sentiment}")
