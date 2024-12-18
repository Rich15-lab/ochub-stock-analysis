import yfinance as yf
import pandas as pd

def fetch_stocks_under_5(profit_target=5, stop_loss_percent=10):
    """
    Dynamically scans all stocks for those priced under $5 and recommends one.
    Includes profit target and stop-loss suggestions for better risk management.
    """
    print(f"Scanning the market for stocks under $5 with a {profit_target}% profit target...\n")

    # Use a broad dataset of tickers (e.g., NASDAQ-listed stocks)
    try:
        nasdaq_url = "https://datahub.io/core/nasdaq-listings/r/nasdaq-listed-symbols.csv"
        tickers = pd.read_csv(nasdaq_url)["Symbol"].tolist()
    except Exception as e:
        print(f"Error fetching stock tickers: {e}")
        return

    recommendations = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period="6mo")  # Analyze last 6 months

            if data.empty:
                continue  # Skip stocks with no data

            live_price = data["Close"].iloc[-1]
            if live_price <= 5:
                # Analyze historical support levels
                recent_low = data["Low"].min()  # Lowest price in 6 months
                support_level = recent_low + (live_price - recent_low) * 0.2  # 20% rebound zone

                # Set buy, sell, and stop-loss prices
                buy_price = max(live_price, support_level)
                sell_price = buy_price * (1 + profit_target / 100)  # Target profit
                stop_loss_price = buy_price * (1 - stop_loss_percent / 100)  # Stop-loss limit

                recommendations.append({
                    "Ticker": ticker,
                    "Current Price": live_price,
                    "Support Level": support_level,
                    "Buy Price": buy_price,
                    "Sell Price": sell_price,
                    "Stop Loss": stop_loss_price
                })

                # Break if a stock is found
                if len(recommendations) == 1:
                    break
        except Exception as e:
            continue  # Skip problematic stocks

    if recommendations:
        print(f"Recommended Stock: {recommendations[0]['Ticker']}")
        print(f"Current Price: ${recommendations[0]['Current Price']:.2f}")
        print(f"Historical Support Level: ${recommendations[0]['Support Level']:.2f}")
        print(f"Recommended Buy Price: ${recommendations[0]['Buy Price']:.2f}")
        print(f"Recommended Sell Price: ${recommendations[0]['Sell Price']:.2f}")
        print(f"Stop Loss Price: ${recommendations[0]['Stop Loss']:.2f}")
    else:
        print("No stocks under $5 found.")

if __name__ == "__main__":
    # Adjust profit target (e.g., 5%, 10%) and stop-loss percentage as needed
    fetch_stocks_under_5(profit_target=10, stop_loss_percent=10)
