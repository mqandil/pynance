# Capital Allocation

`capital_allocation(portfolio_id, download=False, file_name=None)`

The Capital Allocation Function returns a dataframe with the predicted portfolio allocations for the requested portfolio

## Arguments

**`portfolio_id:`** select a portfolio ID to return data on the portfolio's capital allocation strategy. See [expected_return_range()](expected_return_range.md) for portfolio ID's with interactive chart. ID's generally range from 0 to 1000. Integers only.

**`download:`** download selected data to environment in csv format with chosen name (see `file_name`). Valid arguments: `True`, `False`.

**`file_name:`** file name for download. String only.

## Examples of Valid Queries

```python
from pynance import portfolio_optimizer as po
ticker_list = ['MSFT', 'PG', 'HLI']
portfolio = po.PortfolioCalculations(ticker_list)

# return capital allocation dataframe
ca_df = portfolio.capital_allocation(42)
print(ca_df)

# download capital allocation dataframe
portfolio.capital_allocation(42, Download=True, file_name='portfolio42_capital_allocation.csv')
```