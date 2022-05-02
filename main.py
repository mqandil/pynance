from Portfolio_Calculator import PortfolioCalculations as pc

ticker_list = [
        "XOM", "SHW", "JPM", "AEP", "UNH", "AMZN", 
        "KO", "BA", "AMT", "DD", "TSN", "SLG"
    ]

print(pc(ticker_list).max_sharpe_portfolio())
print(pc(ticker_list).min_std_portfolio())
pc(ticker_list).efficient_frontier()