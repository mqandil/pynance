# Minimum Variance Portfolio

`min_var_portfolio(mode, download=False, file_path=None, file_name='min_var_portfolio')`

The Minimum Variance Portfolio Function returns the minimum risk portfolio for the given stock ticker list

## Arguments

`mode:` select one of three options to return data on the maximum sharpe portfolio:
- `rr:` **risk-return** | sentence describing annualized expected return and standard deviation for the portfolio
- `df:` **DataFrame** | DataFrame of chosen stocks and recommended portfolio allocation for maximum risk-reward tradeoff
- `pie:` **Interactive Pie Chart** | pie chart visualization of recommended portfolio allocation for maximum risk-reward tradeoff

`download:` download selected data to environment. Note download is in csv format for `rr` and `df`, and is in html format for `pie`. Valid arguments: `True`, `False`.

`file_path:` pathname of location and file name to download interactive pie chart with `pie` argument. Required argument for `pie` only.

`file_name:` file name to download for `df` argumnet. Required argument for `df` only.

## Examples of Valid Queries

```python
from PortfolioOptimizer.Portfolio_Calculator import PortfolioCalculations as pc
ticker_list = ['MSFT', 'PG', 'HLI']
portfolio = pc(ticker_list)

# get risk-return information
risk_return = portfolio.min_var_portfolio('rr')
print(risk_return)

# return capital allocation dataframe
ca_df = portfolio.min_var_portfolio('df')
print(ca_df.head(3))

# retreive interactive pie chart
ca_pie = portfolio.min_var_portfolio('pie')
ca_pie.show()

# save interactive pie chart
portfolio.min_var_portfolio('pie', download=True, file_path='/Users/User/Desktop/Folder/file.html')
```