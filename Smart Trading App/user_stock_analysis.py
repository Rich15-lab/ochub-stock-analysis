import yfinance as yf

# Helper function to calculate ATR (volatility)
def calculate_atr(data):
    data['High-Low'] = data['High'] - data['Low']
    data['High-Close'] = abs(data['High'] - data['Close'].shift(1))
    data['Low-Close'] = abs(data['Low'] - data['Close'].shift(1))
    data['True Range'] = data[['High-Low', 'High-Close', 'Low-Close']].max(axis=1)
    data['ATR'] = data['True Range'].rolling(window=14).mean()
    return data['ATR'].iloc[-1] if not data['ATR'].isna().all() else None

# Analyze a stock
def analyze_stock(ticker):
    try:
        stock = yf.Ticker(ticker)

        # Fetch live data
        live_data = stock.info
        current_price = live_data.get('regularMarketPrice') or live_data.get('previousClose') or live_data.get('ask')
        if not current_price or current_price <= 0:
            return {"Error": f"No valid price data found for ticker: {ticker}"}

        # Fetch historical data
        hist = stock.history(period="1mo", interval="1d")
        if hist.empty:
            return {"Error": f"No historical data available for ticker: {ticker}"}

        # Calculate SMA, EMA, ATR
        hist['SMA'] = hist['Close'].rolling(window=14).mean()
        hist['EMA'] = hist['Close'].ewm(span=14, adjust=False).mean()
        atr = calculate_atr(hist)

        sma = hist['SMA'].iloc[-1]
        ema = hist['EMA'].iloc[-1]

        # Calculate potential profit
        target_price = max(sma, ema)
        potential_profit = round(target_price - current_price, 2)

        # Refined signal logic
        if current_price < ema:
            signal = "Sell"
        elif current_price > ema and target_price > current_price:
            signal = "Buy"
        else:
            signal = "Hold"

        return {
            "Ticker": ticker.upper(),
            "Current Price": current_price,
            "SMA": round(sma, 2),
            "EMA": round(ema, 2),
            "ATR (Volatility)": round(atr, 2) if atr else 'N/A',
            "Signal": signal,
            "Target Price": round(target_price, 2),
            "Potential Profit": f"${potential_profit} per share" if potential_profit > 0 else "No profit potential"
        }
    except Exception as e:
        return {"Error": f"An error occurred while analyzing {ticker}: {e}"}

# Main function to handle user input
def main():
    print("Welcome to the Stock Analysis App!")
    ticker = input("Enter a stock ticker symbol (e.g., AAPL): ").strip()
    if not ticker:
        print("No ticker symbol entered. Exiting...")
        return

    print(f"\nAnalyzing {ticker}...\n")
    result = analyze_stock(ticker)

    if "Error" in result:
        print(f"Error: {result['Error']}")
    else:
        print("\n=== Stock Analysis Result ===")
        for key, value in result.items():
            print(f"{key}: {value}")

# Run the app
if __name__ == "__main__":
    main()
