# Minimum Variance Portfolio

`min_var_portfolio(mode, download=False, file_path=None)`

The Maximum Sharpe Portfolio Function returns the optimal risk-reward tradeoff portfolio for the given stock ticker list

## Arguments

`mode:` select one of three options to return data on the maximum sharpe portfolio:
- `rr:` **risk-return** | sentence describing annualized expected return and standard deviation for the portfolio
- `df:` **DataFrame** | DataFrame of chosen stocks and recommended portfolio allocation for maximum risk-reward tradeoff
- `pie:` **Interactive Pie Chart** | pie chart visualization of recommended portfolio allocation for maximum risk-reward tradeoff

`download:` download selected data to environment. Note download is in csv format for `rr` and `df`, and is in html format for `pie`. Valid arguments: `True`, `False`.

`file_path:` pathname of location to download interactive pie chart with `pie` argument. Required argument for `pie`, optional argument for `df`.

## Examples of Valid Queries

```python
from PortfolioOptimizer.Portfolio_Calculator import PortfolioCalculations as pc
ticker_list = ['MSFT', 'PG', 'HLI']
portfolio = pc(ticker_list)

# get risk-return information
risk_return = portfolio.max_sharpe_portfolio('rr')
print(risk_return)

# return capital allocation dataframe
ca_df = portfolio.max_sharpe_portfolio('df')
print(ca_df.head(3))

# retreive interactive pie chart
ca_pie = portfolio.max_sharpe_portfolio('pie')
ca_pie.show()

# save interactive pie chart
portfolio.max_sharpe_portfolio('pie', download=True, file_path='/Users/User/Desktop/Folder/file.html')
```