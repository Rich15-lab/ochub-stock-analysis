import yfinance as yf
import pandas as pd
import random

def fetch_random_stock_under_5(profit_target=10, stop_loss_percent=10):
    """
    Dynamically scans the market for stocks under $5 and recommends a random one.
    Avoids repeated recommendations by randomizing selection.
    """
    print(f"Scanning the market for a random stock under $5 with a {profit_target}% profit target...\n")

    try:
        # Fetch stock tickers from NASDAQ
        nasdaq_url = "https://datahub.io/core/nasdaq-listings/r/nasdaq-listed-symbols.csv"
        tickers = pd.read_csv(nasdaq_url)["Symbol"].tolist()
        random.shuffle(tickers)  # Shuffle tickers to ensure randomness
    except Exception as e:
        print(f"Error fetching stock tickers: {e}")
        return

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period="6mo")

            if data.empty:
                continue

            live_price = data["Close"].iloc[-1]
            if live_price <= 5:
                recent_low = data["Low"].min()
                support_level = recent_low + (live_price - recent_low) * 0.2

                buy_price = max(live_price, support_level)
                sell_price = buy_price * (1 + profit_target / 100)
                stop_loss_price = buy_price * (1 - stop_loss_percent / 100)

                print(f"Recommended Stock: {ticker}")
                print(f"Current Price: ${live_price:.2f}")
                print(f"Historical Support Level: ${support_level:.2f}")
                print(f"Recommended Buy Price: ${buy_price:.2f}")
                print(f"Recommended Sell Price: ${sell_price:.2f}")
                print(f"Stop Loss Price: ${stop_loss_price:.2f}")
                return
        except Exception as e:
            continue

    print("No stocks under $5 found.")

if __name__ == "__main__":
    fetch_random_stock_under_5(profit_target=10, stop_loss_percent=10)
