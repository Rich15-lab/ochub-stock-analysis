import yfinance as yf
from flask import Flask

app = Flask(__name__)

latest_recommendation = "No recommendations yet. Please wait for the app 
to scan stocks."

def analyze_stock():
    global latest_recommendation
    try:
        # Example: Fetch one stock under $5
        stock = yf.Ticker("EVO")  # Replace with a random stock logic 
later
        data = stock.history(period="5d")
        if data.empty:
            latest_recommendation = "No valid data found for the stock."
            return

        current_price = data["Close"].iloc[-1]
        if current_price <= 5:
            buy_price = current_price
            sell_price = current_price * 1.10  # Target 10% profit
            stop_loss = current_price * 0.90  # Stop loss at 10% lower

            latest_recommendation = (
                f"Recommended Stock: EVO<br>"
                f"Current Price: ${current_price:.2f}<br>"
                f"Buy Price: ${buy_price:.2f}<br>"
                f"Sell Price: ${sell_price:.2f}<br>"
                f"Stop Loss: ${stop_loss:.2f}"
            )
        else:
            latest_recommendation = "No stocks under $5 found."
    except Exception as e:
        latest_recommendation = f"Error: {e}"

@app.route("/")
def home():
    analyze_stock()
    return latest_recommendation

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

