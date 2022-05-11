import yfinance as yf

period = "5y"
interval = "1mo"

def dataretriever(ticker, period = period, interval = interval):
    #get historical data for stock in period by interval
    ticker_info = yf.Ticker(ticker)
    market_data = ticker_info.history(period = period, interval = interval)

    #select adj close line, drop N/A values, and change to percent change, then drop first column (no data)
    adj_close_data = market_data.iloc[:, 3].dropna().pct_change().dropna()

    if adj_close_data.empty:
        print(f"'{ticker}' is not a valid ticker.")
        raise TickerError

    #remove last line if not updated to next month
    if adj_close_data[-1] == 0:
        adj_close_data = adj_close_data[0:-1]

    return adj_close_data

class TickerError(Exception):
    pass

if __name__ == "__main__":
    print(dataretriever('HLIS'))