import yfinance as yf
import pandas as pd

# Helper function to calculate volatility (ATR)
def calculate_atr(data):
    data['High-Low'] = data['High'] - data['Low']
    data['High-Close'] = abs(data['High'] - data['Close'].shift(1))
    data['Low-Close'] = abs(data['Low'] - data['Close'].shift(1))
    data['True Range'] = data[['High-Low', 'High-Close', 'Low-Close']].max(axis=1)
    data['ATR'] = data['True Range'].rolling(window=14).mean()
    return data['ATR'].iloc[-1] if not data['ATR'].isna().all() else None  # Return the latest ATR value

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

# Function to fetch and analyze stock data
def analyze_stock(ticker, period="1mo"):
    try:
        # Fetch historical data
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval="1d")
        
        if hist.empty:
            return {"Error": f"No data found for {ticker} in the period {period}"}
        
        # Calculate SMA and EMA
        hist['SMA'] = hist['Close'].rolling(window=14).mean()  # Simple Moving Average
        hist['EMA'] = hist['Close'].ewm(span=14, adjust=False).mean()  # Exponential Moving Average
        
        # Calculate ATR for volatility
        atr = calculate_atr(hist)

        # Fetch live data
        live_data = stock.info
        current_price = live_data.get('regularMarketPrice', live_data.get('ask', 'N/A'))
        ath = live_data.get('fiftyTwoWeekHigh', 'N/A')
        atl = live_data.get('fiftyTwoWeekLow', 'N/A')
        volume = live_data.get('regularMarketVolume', 'N/A')

        # Generate buy/hold/sell signal
        signal = generate_signal(current_price, hist['SMA'].iloc[-1], hist['EMA'].iloc[-1])

        # Generate insights
        insights = {
            "Ticker": ticker,
            "Current Price": current_price,
            "SMA": round(hist['SMA'].iloc[-1], 2) if not hist['SMA'].isna().all() else 'N/A',
            "EMA": round(hist['EMA'].iloc[-1], 2) if not hist['EMA'].isna().all() else 'N/A',
            "Volatility (ATR)": round(atr, 2) if atr else 'N/A',
            "52-Week High (ATH)": ath,
            "52-Week Low (ATL)": atl,
            "Volume": volume,
            "Trend": "Bullish" if signal == "Buy" else "Bearish" if signal == "Sell" else "Neutral",
            "Signal": signal
        }
        return insights
    except Exception as e:
        return {"Error": str(e)}

# Function to scan multiple stocks
def scan_stocks(tickers):
    results = []
    for ticker in tickers:
        print(f"Analyzing {ticker}...")
        result = analyze_stock(ticker)
        results.append(result)
    return results

# Example usage with a list of tickers
tickers_to_scan = ['AAPL', 'TSLA', 'MSFT', 'GOOGL']  # Add more tickers here
analysis_results = scan_stocks(tickers_to_scan)

# Display results
for result in analysis_results:
    if "Error" in result:
        print(f"Error with {result['Ticker']}: {result['Error']}")
    else:
        print("\n=== Stock Analysis ===")
        for key, value in result.items():
            print(f"{key}: {value}")

# Best actionable signal (if needed for priority)
buy_signals = [stock for stock in analysis_results if stock.get("Signal") == "Buy"]
if buy_signals:
    best_pick = max(buy_signals, key=lambda x: x.get("Volume", 0))  # Prioritize by volume
    print("\n=== Recommended Stock to Trade ===")
    for key, value in best_pick.items():
        print(f"{key}: {value}")
else:
    print("\nNo strong Buy signals found in the current scan.")
