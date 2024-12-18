import yfinance as yf

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
def analyze_stock(ticker):
    try:
        stock = yf.Ticker(ticker)

        # Fetch live data
        live_data = stock.info
        print(f"Debug: Raw data for {ticker}: {live_data}")

        # Extract key fields with flexible fallbacks
        current_price = live_data.get('regularMarketPrice') or live_data.get('currentPrice') or "N/A"
        volume = live_data.get('regularMarketVolume') or live_data.get('volume') or "N/A"
        day_high = live_data.get('dayHigh', "N/A")
        day_low = live_data.get('dayLow', "N/A")
        week_52_high = live_data.get('fiftyTwoWeekHigh', "N/A")
        week_52_low = live_data.get('fiftyTwoWeekLow', "N/A")
        market_cap = live_data.get('marketCap', "N/A")

        # Validate critical fields
        if current_price == "N/A" or volume == "N/A":
            return {
                "Error": f"Missing critical data for ticker: {ticker} (Price: {current_price}, Volume: {volume})"
            }

        # Fetch historical data
        hist = stock.history(period="1mo", interval="1d")
        if hist.empty:
            return {"Error": f"No historical data available for ticker: {ticker}"}

        # Calculate SMA, EMA, ATR, RSI
        hist['SMA'] = hist['Close'].rolling(window=14).mean()
        hist['EMA'] = hist['Close'].ewm(span=14, adjust=False).mean()
        atr = calculate_atr(hist)
        rsi = calculate_rsi(hist)

        sma = hist['SMA'].iloc[-1] if not hist['SMA'].isna().all() else "N/A"
        ema = hist['EMA'].iloc[-1] if not hist['EMA'].isna().all() else "N/A"

        # Calculate target price and profit potential
        target_price = max(sma, ema) if isinstance(sma, (float, int)) and isinstance(ema, (float, int)) else "N/A"
        potential_profit = (
            round((target_price - current_price) / current_price * 100, 2)
            if isinstance(target_price, (float, int)) and current_price
            else "N/A"
        )

        # Generate buy/hold/sell signal and detailed explanation
        explanation = []
        if rsi and rsi < 30:
            signal = "Buy (Oversold)"
            explanation.append("The RSI indicates oversold conditions. This is a potential buy opportunity.")
        elif rsi and rsi > 70:
            signal = "Sell (Overbought)"
            explanation.append("The RSI indicates overbought conditions. Consider selling to secure profits.")
        elif current_price and ema and current_price > ema:
            signal = "Buy (Uptrend)"
            explanation.append("The price is above the EMA, suggesting an uptrend. This may be a buy opportunity.")
        elif current_price and ema and current_price < ema:
            signal = "Sell (Downtrend)"
            explanation.append("The price is below the EMA, suggesting a downtrend. Selling may be prudent.")
        else:
            signal = "Hold (Stable)"
            explanation.append("The stock is in a stable range. Holding is recommended.")

        # Add a decision summary
        decision_summary = "\n".join(explanation)
        buy_recommendation = (
            f"Yes, consider buying at or below ${round(current_price - (atr or 0.1), 2)}."
            if "Buy" in signal
            else "No, not recommended to buy right now."
        )

        return {
            "Ticker": ticker.upper(),
            "Current Price": current_price,
            "Day High": day_high,
            "Day Low": day_low,
            "52-Week High": week_52_high,
            "52-Week Low": week_52_low,
            "Market Cap": f"${market_cap:,}" if isinstance(market_cap, (float, int)) else "N/A",
            "Volume": volume,
            "SMA": round(sma, 2) if isinstance(sma, (float, int)) else "N/A",
            "EMA": round(ema, 2) if isinstance(ema, (float, int)) else "N/A",
            "ATR (Volatility)": round(atr, 2) if atr else 'N/A',
            "RSI": round(rsi, 2) if isinstance(rsi, (float, int)) else "N/A",
            "Signal": signal,
            "Buy Recommendation": buy_recommendation,
            "Target Price": round(target_price, 2) if isinstance(target_price, (float, int)) else "N/A",
            "Potential Profit": f"{potential_profit}%" if isinstance(potential_profit, (float, int)) else "N/A",
            "Decision Summary": decision_summary,
        }
    except Exception as e:
        return {"Error": f"An error occurred while analyzing {ticker}: {e}"}

# Main function
def main():
    print("Welcome to the Enhanced Stock Analysis App!")
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
