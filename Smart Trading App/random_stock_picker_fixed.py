import yfinance as yf
import random
import pandas as pd

# Fetch live stock universe dynamically
def fetch_random_stock():
    try:
        # Replace with a live API or database if needed
        stock_universe = pd.read_csv('https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv')
        tickers = stock_universe['Symbol'].tolist()

        # Remove problematic tickers with special characters
        valid_tickers = [ticker for ticker in tickers if "." not in ticker and "$" not in ticker]
        random.shuffle(valid_tickers)  # Shuffle for randomness
        for ticker in valid_tickers:
            return ticker  # Return one random ticker
    except Exception as e:
        print(f"Error fetching stock universe: {e}")
        return None

# Helper function to calculate ATR (volatility)
def calculate_atr(data):
    data['High-Low'] = data['High'] - data['Low']
    data['High-Close'] = abs(data['High'] - data['Close'].shift(1))
    data['Low-Close'] = abs(data['Low'] - data['Close'].shift(1))
    data['True Range'] = data[['High-Low', 'High-Close', 'Low-Close']].max(axis=1)
    data['ATR'] = data['True Range'].rolling(window=14).mean()
    return data['ATR'].iloc[-1] if not data['ATR'].isna().all() else None

# Analyze one stock
def analyze_stock(ticker, period="1mo", min_volume=1000000):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval="1d")
        if hist.empty:
            return None

        # Calculate SMA, EMA, ATR
        hist['SMA'] = hist['Close'].rolling(window=14).mean()
        hist['EMA'] = hist['Close'].ewm(span=14, adjust=False).mean()
        atr = calculate_atr(hist)

        # Fetch live data
        live_data = stock.info
        current_price = live_data.get('regularMarketPrice', 0)
        if current_price > 5 or current_price <= 0:  # Skip invalid stocks
            return None

        volume = live_data.get('regularMarketVolume', 0)
        if volume < min_volume:  # Skip low-volume stocks
            return None

        sma = hist['SMA'].iloc[-1]
        ema = hist['EMA'].iloc[-1]

        # Calculate potential profit
        target_price = max(sma, ema)
        potential_profit = round(target_price - current_price, 2)

        if potential_profit <= 0:  # Skip stocks with no profit potential
            return None

        return {
            "Ticker": ticker,
            "Current Price": current_price,
            "SMA": round(sma, 2),
            "EMA": round(ema, 2),
            "ATR (Volatility)": round(atr, 2) if atr else 'N/A',
            "Volume": volume,
            "Signal": "Buy",
            "Target Price": round(target_price, 2),
            "Potential Profit": f"${potential_profit} per share"
        }
    except Exception as e:
        print(f"Error analyzing {ticker}: {e}")
        return None

# Main function to analyze only one stock
def main():
    random_stock = fetch_random_stock()
    if not random_stock:
        print("No random stock available.")
        return

    print(f"Analyzing {random_stock}...")
    result = analyze_stock(random_stock)

    if result:
        print("\n=== Recommended Stock to Trade ===")
        for key, value in result.items():
            print(f"{key}: {value}")
    else:
        print(f"No actionable recommendation for {random_stock}.")

# Run the app
if __name__ == "__main__":
    main()
