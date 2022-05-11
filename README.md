# pynance
## v1.0.0 Release: May 11, 2022
See [CHANGELOG.md](CHANGELOG.md) for details

`pynance` creates various financial models and relevant graphics. This project is a work-in-progress and does not promise any results. See [docs](docs) for a comprehensive list of functions and functionality. 

## Important Information

This project currently draws requested stock data through Yahoo!Finance and uses their adjusted close prices for necessary computations

Time period for data and time horizon may be adjusted within the code but is currently not accessible from main functionality

## Installation
pynance may be installed via the repo:
```bash
git clone https://github.com/mqandil/pynance
cd pynance
pip install -e .
```
This is the most up-to-date version of `pynance`

## Portfolio Optimizer
`portfolio_optimizer` optimizes portfolios of selected stock data using Markowitz's Modern Portfolio Theory. Portfolios can currently be optimized by maximum sharpe ratio or minimum standard deviation. A portfolio's capital allocation line may also be determined.

### Maximum Sharpe Ratio Portfolio
Retreive a dataframe of expected returns and standard deviation, or a dataframe or pie chart including stock portfolio weights with `max_sharpe_portfolio()`. 
```python
>>> from pynance import portfolio_optimizer as po
>>> ticker_list = ['MSFT', 'PG', 'HLI']
>>> portfolio = po.PortfolioCalculations(ticker_list)
>>> risk_return = portfolio.max_sharpe_portfolio('rr')
>>> print(risk_return)

                   Max Sharpe Portfolio
Expected Return                  27.03%
Standard Deviation               14.28%

>>> max_sharpe_df = portfolio.max_sharpe_portfolio('df')
>>> print(max_sharpe_df.head(3))

      Portfolio Weight
MSFT            54.42%
PG              36.44%
HLI              9.13% 
[3 rows x 1 column]
```

### Minimum Variance Portfolio
Retreive a pie chart including stock portfolio weights and a chart of portfolio weights for chosen stocks with `min_std_portfolio()`.
```python
>>> from pynance import portfolio_optimizer as po
>>> ticker_list = ['MSFT', 'PG', 'HLI']
>>> portfolio = po.PortfolioCalculations(ticker_list)
>>> risk_return = portfolio.min_var_portfolio('rr')
>>> print(risk_return)

                   Min Var Portfolio
Expected Return               22.76%
Standard Deviation            13.17%

>>> min_var_df = portfolio.min_var_portfolio('df')
>>> print(min_var_df.head(3))

      Portfolio Weight
MSFT            29.23%
PG              57.19%
HLI             13.58% 
[3 rows x 1 column]
```
### Efficient Frontier
Return Scatterplot of Annualized Expected Returns and Standard Deviations for Optimized Portfolios with `efficient_frontier()`
```python
>>> from pynance import portfolio_optimizer as po
>>> ticker_list = ['MSFT', 'PG', 'HLI']
>>> portfolio = po.PortfolioCalculations(ticker_list)
>>> fig = portfolio.efficient_frontier()
>>> fig.show()
```
### Expected Returns and Standard Deviation Error
Return Continuous Error Bars (Standard Deviation) by Portfolio ID with `expected_return_range()`
```python
>>> from pynance import portfolio_optimizer as po
>>> ticker_list = ['MSFT', 'PG', 'HLI']
>>> portfolio = po.PortfolioCalculations(ticker_list)
>>> fig = portfolio.expected_return_range()
>>> fig.show()
```
### Final Capital Allocation
Returns Capital Allocation for selected Portfolio with `Portfolio_ID` argument with `capital_allocation()`
```python
>>> from pynance import portfolio_optimizer as po
>>> ticker_list = ['MSFT', 'PG', 'HLI']
>>> portfolio_ID = 56
>>> portfolio = po.PortfolioCalculations(ticker_list)
>>> portfolio_56_allocation = portfolio.capital_allocation(portfolio_ID)
>>> print(portfolio_56_allocation.head(3))

      Portfolio Weight
MSFT            37.48%
PG              50.38%
HLI             12.13%
[3 rows x 1 column]
```
## Valuation Virtuoso
`valuation_virtuoso` creates discounted cash flow models for selected publicly-traded firms and returns models, charts, and an estimated stock price valuation.

Coming Soon...