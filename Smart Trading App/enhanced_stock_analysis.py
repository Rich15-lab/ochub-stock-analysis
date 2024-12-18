import yfinance as yf
import pandas as pd

# Helper function to calculate ATR (volatility)
def calculate_atr(data):
    data['High-Low'] = data['High'] - data['Low']
    data['High-Close'] = abs(data['High'] - data['Close'].shift(1))
    data['Low-Close'] = abs(data['Low'] - data['Close'].shift(1))
    data['True Range'] = data[['High-Low', 'High-Close', 'Low-Close']].max(axis=1)
    data['ATR'] = data['True Range'].rolling(window=14).mean()
    return data['ATR'].iloc[-1] if not data['ATR'].isna().all() else None

# Helper function to calculate RSI
def calculate_rsi(data, window=14):
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if not rsi.isna().all() else None

# Analyze a stock
def analyze_stock(ticker, min_volume=1000000, min_profit=0.05):
    try:
        stock = yf.Ticker(ticker)

        # Fetch live data
        live_data = stock.info
        print(f"Debug: Raw data for {ticker}: {live_data}")  # Debugging line to inspect available fields

        # Fetch price and other fields with fallbacks
        current_price = (
            live_data.get('regularMarketPrice')
            or live_data.get('previousClose')
            or live_data.get('ask')
        )
        volume = live_data.get('regularMarketVolume', "N/A")
        day_high = live_data.get('dayHigh', "N/A")
        day_low = live_data.get('dayLow', "N/A")

        # Ensure valid live data is available
        if not current_price or volume == "N/A":
            return {"Error": f"No valid price or volume data found for ticker: {ticker}"}

        # Check volume threshold
        if volume < min_volume:
            return {"Error": f"Volume is too low for actionable trading: {volume}"}

        # Fetch historical data
        hist = stock.history(period="1mo", interval="1d")
        if hist.empty:
            return {"Error": f"No historical data available for ticker: {ticker}"}

        # Calculate SMA, EMA, ATR, RSI
        hist['SMA'] = hist['Close'].rolling(window=14).mean()
        hist['EMA'] = hist['Close'].ewm(span=14, adjust=False).mean()
        atr = calculate_atr(hist)
        rsi = calculate_rsi(hist)

        sma = hist['SMA'].iloc[-1]
        ema = hist['EMA'].iloc[-1]

        # Calculate potential profit
        target_price = max(sma, ema)
        potential_profit = round((target_price - current_price) / current_price * 100, 2)

        # Refined buy/hold/sell signal
        if rsi < 30:
            signal = "Buy (Oversold)"
        elif rsi > 70:
            signal = "Sell (Overbought)"
        elif current_price > ema and potential_profit > min_profit:
            signal = "Buy (Uptrend)"
        elif current_price < ema:
            signal = "Sell (Downtrend)"
        else:
            signal = "Hold (Stable)"

        return {
            "Ticker": ticker.upper(),
            "Current Price": current_price,
            "Day High": day_high,
            "Day Low": day_low,
            "Volume": volume,
            "SMA": round(sma, 2),
            "EMA": round(ema, 2),
            "ATR (Volatility)": round(atr, 2) if atr else 'N/A',
            "RSI": round(rsi, 2) if rsi else 'N/A',
            "Signal": signal,
            "Target Price": round(target_price, 2),
            "Potential Profit": f"{potential_profit}%"
        }
    except Exception as e:
        return {"Error": f"An error occurred while analyzing {ticker}: {e}"}

# Main function to handle user input
def main():
    print("Welcome to the Advanced Stock Analysis App!")
    ticker = input("Enter a stock ticker symbol (e.g., AAPL): ").strip()
    if not ticker:
        print("No ticker symbol entered. Exiting...")
        return

    min_volume = int(input("Enter minimum volume for actionable trades (e.g., 1000000): ").strip())
    min_profit = float(input("Enter minimum profit percentage for Buy signals (e.g., 0.05): ").strip())

    print(f"\nAnalyzing {ticker}...\n")
    result = analyze_stock(ticker, min_volume, min_profit)

    if "Error" in result:
        print(f"Error: {result['Error']}")
    else:
        print("\n=== Advanced Stock Analysis Result ===")
        for key, value in result.items():
            print(f"{key}: {value}")

# Run the app
if __name__ == "__main__":
    main()
