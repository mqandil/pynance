# Efficient Frontier

`efficient_frontier(download=False, file_path=None)`

The Efficient Frontier Function returns an interactive scatterplot displaying the efficient frontier and capital allocation line for the chosen stock portfolio

## Arguments

**`download:`** download selected data to environment in html format to chosen location (see `file_path`). Valid arguments: `True`, `False`.

**`file_path:`** pathname of location and file name to download interactive scatterplot. String only.

## Examples of Valid Queries

```python
# create interactive scatterplot
ef_fig = portfolio.efficient_frontier()
ef_fig.show()

# download interactive scatterplot
portfolio.efficient_frontier(download=True, file_path='/Users/User/Desktop/Folder/file.html')
```