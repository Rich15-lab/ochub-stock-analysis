import yfinance as yf
import pandas as pd
import random
import threading
from flask import Flask

app = Flask(__name__)

latest_recommendation = "No recommendations yet. Please wait for the app to scan stocks."

def save_recommendation(ticker, current_price, buy_price, sell_price, stop_loss):
    global latest_recommendation
    latest_recommendation = (
        f"Recommended Stock: {ticker}<br>"
        f"Current Price: ${current_price:.2f}<br>"
        f"Buy Price: ${buy_price:.2f}<br>"
        f"Sell Price: ${sell_price:.2f}<br>"
        f"Stop Loss Price: ${stop_loss:.2f}<br>"
    )
    data = {
        "Ticker": [ticker],
        "Current Price": [current_price],
        "Buy Price": [buy_price],
        "Sell Price": [sell_price],
        "Stop Loss Price": [stop_loss],
    }
    df = pd.DataFrame(data)
    df.to_csv("stock_recommendations.csv", mode="a", header=False, index=False)
    print(latest_recommendation)

def fetch_random_stock_under_5():
    global latest_recommendation
    try:
        nasdaq_url = "https://datahub.io/core/nasdaq-listings/r/nasdaq-listed-symbols.csv"
        tickers = pd.read_csv(nasdaq_url)["Symbol"].tolist()
        random.shuffle(tickers)
    except Exception as e:
        latest_recommendation = f"Error fetching stock tickers: {e}"
        return

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period="5d")
            if data.empty:
                continue

            live_price = data["Close"].iloc[-1]
            if live_price <= 5:
                buy_price = live_price
                sell_price = buy_price * 1.10  # 10% profit target
                stop_loss_price = buy_price * 0.90  # 10% stop loss

                save_recommendation(ticker, live_price, buy_price, sell_price, stop_loss_price)
                return
        except Exception as e:
            print(f"Error processing ticker {ticker}: {e}")
            continue

    latest_recommendation = "No stocks under $5 found."

def run_stock_app():
    while True:
        fetch_random_stock_under_5()

@app.route('/')
def home():
    return latest_recommendation

if __name__ == "__main__":
    threading.Thread(target=run_stock_app).start()
    app.run(host="0.0.0.0", port=5000)
