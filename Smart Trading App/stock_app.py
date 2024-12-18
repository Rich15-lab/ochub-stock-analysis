import yfinance as yf
import pandas as pd  # Add this line to fix the issue

def fetch_stocks_under_5():
    """
    Dynamically scans all stocks for those priced under $5 and recommends one.
    Includes analysis of historical support levels for better buy/sell decisions.
    """
    print("Scanning the entire market for stocks under $5...\n")

    # Use a broad dataset of tickers (e.g., NASDAQ-listed stocks)
    try:
        nasdaq_url = "https://datahub.io/core/nasdaq-listings/r/nasdaq-listed-symbols.csv"
        tickers = pd.read_csv(nasdaq_url)["Symbol"].tolist()
    except Exception as e:
        print(f"Error fetching stock tickers: {e}")
        return

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period="6mo")  # Analyze last 6 months

            if data.empty:
                continue  # Skip stocks with no data

            live_price = data["Close"].iloc[-1]
            if live_price <= 5:
                # Analyze historical support levels
                recent_low = data["Low"].min()  # Lowest price in 6 months
                support_level = recent_low + (live_price - recent_low) * 0.2  # 20% rebound zone

                # Set buy and sell prices
                buy_price = max(live_price, support_level)  # Avoid buying above the support level
                sell_price = buy_price * 1.05  # Target 5% profit

                print(f"Recommended Stock: {ticker}")
                print(f"Current Price: ${live_price:.2f}")
                print(f"Historical Support Level: ${support_level:.2f}")
                print(f"Recommended Buy Price: ${buy_price:.2f}")
                print(f"Recommended Sell Price: ${sell_price:.2f}")
                return  # Stop after finding one valid stock
        except Exception as e:
            continue  # Skip problematic stocks

    print("No stocks under $5 found.")

if __name__ == "__main__":
    fetch_stocks_under_5()
