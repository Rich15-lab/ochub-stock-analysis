import yfinance as yf

def find_stock(max_price):
    # List of stocks to analyze
    stocks = ["AAPL", "MSFT", "TSLA", "AMZN", "GOOGL"]
    best_stock = None
    highest_potential = 0

    print(f"Analyzing stocks under ${max_price}...\n")

    for ticker in stocks:
        stock = yf.Ticker(ticker)
        try:
            # Fetch recent price data
            data = stock.history(period="5d")
            live_price = data["Close"].iloc[-1]  # Most recent close price
            previous_close = data["Close"].iloc[0]  # Oldest close price in the range

            if live_price <= max_price:
                # Calculate potential gain
                potential_gain = (live_price - previous_close) / previous_close

                # Find the best stock
                if potential_gain > highest_potential:
                    highest_potential = potential_gain
                    best_stock = {
                        "ticker": ticker,
                        "live_price": round(live_price, 2),
                        "potential_gain": round(potential_gain * 100, 2),
                        "buy_price": round(live_price, 2),
                        "sell_price": round(live_price * 1.05, 2),  # Example: 5% target gain
                    }
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")

    # Display recommendation
    if best_stock:
        print(f"Best Stock Recommendation:")
        print(f"Ticker: {best_stock['ticker']}")
        print(f"Live Price: ${best_stock['live_price']}")
        print(f"Potential Gain: {best_stock['potential_gain']}%")
        print(f"Buy at: ${best_stock['buy_price']}")
        print(f"Sell at: ${best_stock['sell_price']}")
    else:
        print(f"No suitable stocks found under ${max_price}.")

if __name__ == "__main__":
    print("Welcome to the Stock Finder!")
    max_price = float(input("Enter your maximum stock price: "))
    find_stock(max_price)
