from flask import Flask, request, render_template_string
import yfinance as yf
import math

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Welcome to OCHub: Your Stock Analysis Companion!</h1>
    <form action="/analyze" method="post">
        <label>Enter Stock Ticker (e.g., AAPL):</label><br>
        <input type="text" name="ticker" required><br><br>
        <button type="submit">Analyze</button>
    </form>
    """

@app.route("/analyze", methods=["POST"])
def analyze():
    ticker = request.form.get("ticker").strip().upper()
    try:
        stock = yf.Ticker(ticker)
        data = stock.info

        # Extract relevant stock information
        current_price = data.get('regularMarketPrice') or data.get('bid') or data.get('ask') or data.get('previousClose', 'N/A')
        day_high = data.get('dayHigh', 'N/A')
        day_low = data.get('dayLow', 'N/A')
        week_52_high = data.get('fiftyTwoWeekHigh', 'N/A')
        week_52_low = data.get('fiftyTwoWeekLow', 'N/A')
        market_cap = data.get('marketCap', 'N/A')
        volume = data.get('regularMarketVolume', 'N/A')

        # Calculate additional metrics
        sma = data.get('fiftyDayAverage', 'N/A')
        ema = data.get('twoHundredDayAverage', 'N/A')
        atr = round(data.get('beta', 1) * 2, 2)  # Placeholder for ATR calculation
        rsi = round((data.get('fiftyTwoWeekHigh', 1) - data.get('regularMarketPrice', 1)) * 10, 2)  # Placeholder for RSI calculation

        # Recommendation Logic
        recommendation = ""
        decision_summary = ""
        if current_price != 'N/A' and isinstance(current_price, (int, float)):
            if current_price < sma:
                recommendation = "Buy (Undervalued)"
                decision_summary = "The stock appears undervalued based on its SMA. Consider buying for potential upside."
            elif current_price > ema:
                recommendation = "Sell (Overvalued)"
                decision_summary = "The stock appears overvalued based on its EMA. Selling may secure profits."
            else:
                recommendation = "Hold (Stable)"
                decision_summary = "The stock is stable. Holding is recommended until further price action."

        else:
            recommendation = "No recommendation available."
            decision_summary = "The stock data is insufficient for a clear recommendation."

        return render_template_string(f"""
        <h1>OCHub Stock Analysis Result</h1>
        <p><strong>Ticker:</strong> {ticker}</p>
        <p><strong>Current Price:</strong> {current_price}</p>
        <p><strong>Day High:</strong> {day_high}</p>
        <p><strong>Day Low:</strong> {day_low}</p>
        <p><strong>52-Week High:</strong> {week_52_high}</p>
        <p><strong>52-Week Low:</strong> {week_52_low}</p>
        <p><strong>Market Cap:</strong> {market_cap:,} (if available)</p>
        <p><strong>Volume:</strong> {volume}</p>
        <p><strong>SMA:</strong> {sma}</p>
        <p><strong>EMA:</strong> {ema}</p>
        <p><strong>ATR (Volatility):</strong> {atr}</p>
        <p><strong>RSI:</strong> {rsi}</p>
        <p><strong>Recommendation:</strong> {recommendation}</p>
        <hr>
        <h2>Decision Summary</h2>
        <p>{decision_summary}</p>
        <a href="/">Analyze Another Stock</a>
        """)
    except Exception as e:
        return f"<h1>Error</h1><p>{e}</p><a href='/'>Try Again</a>"

if __name__ == "__main__":
    app.run(debug=True)
