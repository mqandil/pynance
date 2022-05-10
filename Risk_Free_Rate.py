import yfinance as yf

def get_risk_free_rate():
    ticker_info = yf.Ticker("^TNX")
    market_data = ticker_info.history()
    annual_risk_free_rate = market_data.iloc[-1, 3]
    #monthly being phased out
    monthly_risk_free_rate = ((1+annual_risk_free_rate)**(1/12)-1)/100
    return annual_risk_free_rate

if __name__ == '__main__':
    print(get_risk_free_rate())