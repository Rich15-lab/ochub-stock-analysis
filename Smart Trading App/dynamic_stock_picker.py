import yfinance as yf
import pandas as pd
import random

# Function to dynamically fetch random stocks under $5
def get_dynamic_penny_stocks():
    # Use Yahoo Finance's penny stock screener or an external API in future versions
    # For now, a random sample of tickers as a placeholder
    all_stocks = [
        'AAPL', 'TSLA', 'BB', 'AMC', 'F', 'GME', 'NOK', 'SNDL', 'CCL', 'UAL', 'AAL', 'PLTR'
    ]
    random.shuffle(all_stocks)  # Randomize the selection
    return all_stocks[:10]  # Return the first 10 stocks as a random subset

# Helper function to calculate volatility (ATR)
def calculate_atr(data):
    data['High-Low'] = data['High'] - data['Low']
    data['High-Close'] = abs(data['High'] - data['Close'].shift(1))
    data['Low-Close'] = abs(data['Low'] - data['Close'].shift(1))
    data['True Range'] = data[['High-Low', 'High-Close', 'Low-Close']].max(axis=1)
    data['ATR'] = data['True Range'].rolling(window=14).mean()
    return data['ATR'].iloc[-1] if not data['ATR'].isna().all() else None

# Function to determine buy, hold, or sell
def generate_signal(current_price, sma, ema):
    if current_price < ema:
        return "Sell"
    elif current_price > ema and current_price < sma:
        return "Hold"
    elif current_price > ema and current_price > sma:
        return "Buy"
    else:
        return "Hold"

# Function to calculate potential profit
def calculate_potential_profit(current_price, sma, ema):
    target_price = max(sma, ema)
    potential_profit = round(target_price - current_price, 2)
    return target_price, potential_profit

# Function to fetch and analyze stock data
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
        current_price = live_data.get('regularMarketPrice', live_data.get('ask', 0))
        if current_price > 5 or current_price <= 0:  # Skip stocks above $5 or invalid prices
            return None

        volume = live_data.get('regularMarketVolume', 0)
        if volume < min_volume:  # Skip stocks below minimum volume
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
    except Exception:
        return None

# Function to pick the best stock
def pick_best_stock():
    tickers = get_dynamic_penny_stocks()
    best_stock = None

    for ticker in tickers:
        print(f"Analyzing {ticker}...")
        result = analyze_stock(ticker)
        if result and result["Signal"] == "Buy":  # Prioritize Buy signals
            if not best_stock or result["Potential Profit"] > best_stock["Potential Profit"]:  # Compare by profit
                best_stock = result

    return best_stock

# Main function
def main():
    best_stock = pick_best_stock()
    if best_stock:
        print("\n=== Recommended Stock to Trade ===")
        for key, value in best_stock.items():
            print(f"{key}: {value}")
    else:
        print("No strong Buy signals found among penny stocks.")

# Run the app
if __name__ == "__main__":
    main()
