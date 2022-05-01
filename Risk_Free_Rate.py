import yfinance as yf

ticker_info = yf.Ticker("^TNX")
market_data = ticker_info.history()
risk_free_rate = market_data.iloc[-1, 3]