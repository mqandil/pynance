# Minimum Variance Portfolio

`min_var_portfolio(mode, download=False, file_path=None, file_name=None)`

The Minimum Variance Portfolio Function returns information on the minimum risk portfolio for the given stock ticker list

## Arguments

**`mode:`** select one of three options to return data on the minimum variance portfolio:
- `rr:` **risk-return** | sentence describing annualized expected return and standard deviation for the portfolio
- `df:` **DataFrame** | DataFrame of chosen stocks and recommended portfolio allocation for minimized risk
- `pie:` **Interactive Pie Chart** | pie chart visualization of recommended portfolio allocation for minimized risk

**`download:`** download selected data to environment; csv format for `rr` and `df` modes, html format for `pie` mode. Downloads to current working directory for `rr` and `df`, downloads to chosen location for `pie` (see `file_path`). Valid arguments: `True`, `False`.

**`file_path:`** pathname of location and file name to download interactive pie chart with `pie` argument. Required argument for `pie` only. String only.

**`file_name:`** file name for download with `rr` and `df` arguments. Required argument for `rr` and `df` only. String only.


## Examples of Valid Queries

```python
from pynance import portfolio_optimizer as po
ticker_list = ['MSFT', 'PG', 'HLI']
portfolio = po.PortfolioCalculations(ticker_list)

# return risk-return dataframe
rr_df = portfolio.min_var_portfolio('rr')
print(rr_df)

# download risk-return dataframe
portfolio.min_var_portfolio('rr', Download=True, file_name='rr_data.csv')

# return capital allocation dataframe
ca_df = portfolio.min_var_portfolio('df')
print(ca_df.head(3))

# create interactive pie chart
ca_pie = portfolio.min_var_portfolio('pie')
ca_pie.show()

# download interactive pie chart
portfolio.min_var_portfolio('pie', download=True, file_path='/Users/User/Desktop/Folder/file.html')
```