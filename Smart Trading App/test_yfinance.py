import yfinance as yf

# Test fetching data
def test_yfinance(ticker):
    try:
        stock = yf.Ticker(ticker)
        live_data = stock.info
        print(f"Current price of {ticker}: {live_data.get('regularMarketPrice', 'N/A')}")
        print(f"Volume: {live_data.get('regularMarketVolume', 'N/A')}")
        print(f"52-Week High: {live_data.get('fiftyTwoWeekHigh', 'N/A')}")
        print(f"52-Week Low: {live_data.get('fiftyTwoWeekLow', 'N/A')}")
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")

test_yfinance('AAPL')
