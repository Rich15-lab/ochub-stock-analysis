import yfinance as yf
import random
import pandas as pd

# Fetch live stock universe dynamically (replace with API/screener for broader scope)
def fetch_stock_universe():
    try:
        # Example: S&P 500 tickers dataset; replace with a market-wide dataset
        stock_universe = pd.read_csv('https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv')
        tickers = stock_universe['Symbol'].tolist()

        # Remove problematic tickers with special characters
        valid_tickers = [ticker for ticker in tickers if "." not in ticker and "$" not in ticker]
        random.shuffle(valid_tickers)  # Shuffle for randomness
        return valid_tickers
    except Exception as e:
        print(f"Error fetching stock universe: {e}")
        return []

# Helper function to calculate ATR (volatility)
def calculate_atr(data):
    data['High-Low'] = data['High'] - data['Low']
    data['High-Close'] = abs(data['High'] - data['Close'].shift(1))
    data['Low-Close'] = abs(data['Low'] - data['Close'].shift(1))
    data['True Range'] = data[['High-Low', 'High-Close', 'Low-Close']].max(axis=1)
    data['ATR'] = data['True Range'].rolling(window=14).mean()
    return data['ATR'].iloc[-1] if not data['ATR'].isna().all() else None

# Analyze one stock
def analyze_stock(ticker):
    try:
        stock = yf.Ticker(ticker)
        live_data = stock.info
        current_price = live_data.get('regularMarketPrice', 0)

        # Validate price criteria before in-depth analysis
        if current_price > 5 or current_price <= 0:
            return None

        # Fetch historical data for further analysis
        hist = stock.history(period="1mo", interval="1d")
        if hist.empty:
            return None

        # Calculate SMA, EMA, ATR
        hist['SMA'] = hist['Close'].rolling(window=14).mean()
        hist['EMA'] = hist['Close'].ewm(span=14, adjust=False).mean()
        atr = calculate_atr(hist)

        volume = live_data.get('regularMarketVolume', 0)
        if volume < 1000000:  # Skip low-volume stocks
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

# Main function to analyze one random stock
def main():
    stock_universe = fetch_stock_universe()
    if not stock_universe:
        print("No stock universe available.")
        return

    for ticker in stock_universe:
        print(f"Analyzing {ticker}...")
        result = analyze_stock(ticker)
        if result:  # Stop at the first valid stock
            print("\n=== Recommended Stock to Trade ===")
            for key, value in result.items():
                print(f"{key}: {value}")
            return

    print("No strong Buy signals found among random stocks.")

# Run the app
if __name__ == "__main__":
    main()
