import yfinance as yf
import random
import pandas as pd

# Fetch live stock universe dynamically
def fetch_stock_universe():
    try:
        # Replace with a live stock database or API in the future
        stock_universe = pd.read_csv('https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv')
        tickers = stock_universe['Symbol'].tolist()
        random.shuffle(tickers)  # Shuffle for randomness
        return tickers
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

# Generate buy, hold, or sell signals
def generate_signal(current_price, sma, ema):
    if current_price < ema:
        return "Sell"
    elif current_price > ema and current_price < sma:
        return "Hold"
    elif current_price > ema and current_price > sma:
        return "Buy"
    else:
        return "Hold"

# Calculate potential profit
def calculate_potential_profit(current_price, sma, ema):
    target_price = max(sma, ema)
    potential_profit = round(target_price - current_price, 2)
    return target_price, potential_profit

# Analyze stock data
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

        # Generate buy/hold/sell signal
        signal = generate_signal(current_price, sma, ema)

        # Calculate potential profit
        target_price, potential_profit = calculate_potential_profit(current_price, sma, ema)

        if potential_profit <= 0:  # Skip stocks with no profit potential
            return None

        return {
            "Ticker": ticker,
            "Current Price": current_price,
            "SMA": round(sma, 2),
            "EMA": round(ema, 2),
            "ATR (Volatility)": round(atr, 2) if atr else 'N/A',
            "Volume": volume,
            "Signal": signal,
            "Target Price": round(target_price, 2),
            "Potential Profit": f"${potential_profit} per share"
        }
    except Exception as e:
        print(f"Error analyzing {ticker}: {e}")
        return None

# Main function to pick and recommend one stock
def main():
    stock_universe = fetch_stock_universe()
    if not stock_universe:
        print("No stock universe available.")
        return

    # Iterate through shuffled tickers until we find a valid penny stock
    for ticker in stock_universe:
        best_stock = analyze_stock(ticker)
        if best_stock:  # Stop at the first valid recommendation
            print("\n=== Recommended Stock to Trade ===")
            for key, value in best_stock.items():
                print(f"{key}: {value}")
            return

    print("No strong Buy signals found among random stocks.")

# Run the app
if __name__ == "__main__":
    main()
