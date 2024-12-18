import yfinance as yf
import pandas as pd

def fetch_all_stocks(max_price):
    """
    Dynamically fetch all valid stock prices from NASDAQ and filter by a maximum price.
    """
    print(f"Scanning all NASDAQ stocks under ${max_price}...\n")

    # Step 1: Get NASDAQ tickers dynamically
    try:
        nasdaq_url = "https://datahub.io/core/nasdaq-listings/r/nasdaq-listed-symbols.csv"
        tickers = pd.read_csv(nasdaq_url)["Symbol"].tolist()
    except Exception as e:
        print("Error fetching NASDAQ stock tickers:", e)
        return

    # Step 2: Fetch and filter stocks
    results = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period="1d")
            if data.empty:
                continue  # Skip invalid or inactive stocks
            
            live_price = data["Close"].iloc[-1]
            if live_price <= max_price:
                results.append({"Ticker": ticker, "Price": round(live_price, 2)})
        except Exception:
            continue

    # Step 3: Display results
    if results:
        print(f"Stocks under ${max_price}:")
        for result in results:
            print(f"- {result['Ticker']}: ${result['Price']}")
    else:
        print("No valid stocks found in the given price range.")

# Run the script
if __name__ == "__main__":
    try:
        max_price = float(input("Enter your maximum price: "))
        fetch_all_stocks(max_price)
    except ValueError:
        print("Please enter a valid number.")
