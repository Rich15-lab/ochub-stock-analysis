import yfinance as yf
import random

def scan_three_stocks():
    """
    Dynamically selects and analyzes three random stocks from the market,
    providing actionable recommendations: Buy, Hold, or Sell.
    """
    print("Scanning three random stocks...\n")

    # Example: Pulling a large list of stocks from a common index (S&P 500)
    stock_tickers = [
        "AAPL", "MSFT", "TSLA", "GOOGL", "AMZN", "META", "NVDA", "NFLX", "ADBE",
        "CRM", "PYPL", "INTC", "CSCO", "PEP", "KO", "WMT", "JPM", "BAC", "V"
    ]

    # Select 3 random stocks
    selected_tickers = random.sample(stock_tickers, 3)

    for ticker in selected_tickers:
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period="5d")
            
            if data.empty:
                print(f"No data available for {ticker}. Skipping.")
                continue

            live_price = data["Close"].iloc[-1]
            previous_price = data["Close"].iloc[0]
            change = ((live_price - previous_price) / previous_price) * 100

            # Provide actionable recommendations
            print(f"\nStock: {ticker}")
            print(f"Current Price: ${live_price:.2f}")
            print(f"5-Day Change: {change:.2f}%")

            if change > 5:
                print("Recommendation: SELL (Price increased significantly).")
            elif change < -5:
                print("Recommendation: BUY (Price dropped significantly).")
            else:
                print("Recommendation: HOLD (Stable price).")
        except Exception as e:
            print(f"Error analyzing {ticker}: {e}")

# Run the analysis
if __name__ == "__main__":
    scan_three_stocks()
