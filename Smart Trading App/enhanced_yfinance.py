import yfinance as yf
import pandas as pd

# Helper function to calculate volatility (ATR)
def calculate_atr(data):
    data['High-Low'] = data['High'] - data['Low']
    data['High-Close'] = abs(data['High'] - data['Close'].shift(1))
    data['Low-Close'] = abs(data['Low'] - data['Close'].shift(1))
    data['True Range'] = data[['High-Low', 'High-Close', 'Low-Close']].max(axis=1)
    data['ATR'] = data['True Range'].rolling(window=14).mean()
    return data['ATR'].iloc[-1]  # Return the latest ATR value

# Function to fetch and analyze stock data
def analyze_stock(ticker, days=30):
    try:
        # Fetch historical data
        stock = yf.Ticker(ticker)
        hist = stock.history(period=f"{days}d", interval="1d")
        
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

        # Generate insights
        trend = "Bullish" if current_price != 'N/A' and current_price > hist['EMA'].iloc[-1] else "Bearish"
        
        insights = {
            "Ticker": ticker,
            "Current Price": current_price,
            "SMA": round(hist['SMA'].iloc[-1], 2),
            "EMA": round(hist['EMA'].iloc[-1], 2),
            "Volatility (ATR)": round(atr, 2),
            "52-Week High (ATH)": ath,
            "52-Week Low (ATL)": atl,
            "Volume": volume,
            "Trend": trend
        }
        return insights
    except Exception as e:
        return {"Error": str(e)}

# Test the function with a sample stock
stock_analysis = analyze_stock('AAPL', days=30)

# Print results
for key, value in stock_analysis.items():
    print(f"{key}: {value}")
