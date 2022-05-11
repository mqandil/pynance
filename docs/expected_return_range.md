# Expected Return Range

`expected_return_range(download=False, file_path=None)`

The Expected Return Range Function returns an interactive scatterplot displaying the annualized expected return with continuous error bands (1 standard deviation) by portfolio ID for portfolios along the efficient frontier.

## Arguments

**`download:`** download selected data to environment in html format to chosen location (see `file_path`). Valid arguments: `True`, `False`.

**`file_path:`** pathname of location and file name to download interactive scatterplot. String only.

## Examples of Valid Queries

```python
# create interactive scatterplot
ere_fig = portfolio.expected_return_range()
ere_fig.show()

# download interactive scatterplot
portfolio.expected_return_range(download=True, file_path='/Users/User/Desktop/Folder/file.html')
```