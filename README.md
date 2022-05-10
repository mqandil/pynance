# PortfolioOptimizer
## v0.0.2-beta.1 Release: May 10, 2022
See CHANGELOG.md for details (not yet updated)

`PortfolioOptimizer` optimizes portfolios of selected stock data using Markowitz's Modern Portfolio Theory. Portfolios can currently be optimized by maximum sharpe ratio or minimum standard deviation. A portfolio's capital allocation line may also be determined. This project is a work-in-progress and does not promise any results.

## Important Information
- This project draws requested stock data through Yahoo!Finance and uses their adjusted close prices
- Time period for data may be adjusted within the code but is currently not accessible from main.py

## Installation
Portfolio Optimizer may be installed via the repo:
```bash
git clone https://github.com/mqandil/PortfolioOptimizer
cd PortfolioOptimizer
pip install -e .
```
This is the most up-to-date version of `PortfolioOptimizer`

## Optimal Portfolios
### Maximum Sharpe Ratio Portfolio
Retreive a pie chart including stock portfolio weights and a chart of portfolio weights for chosen stocks with `pc(ticker_list).max_sharpe_portfolio()`. 
```python
>>> from PortfolioOptimizer import PortfolioCalculations as pc
>>> ticker_list = ['MSFT', 'PG', 'HLI']
>>> pc(ticker_list).max_sharpe_portfolio()

Maximum Sharpe Ratio Portfolio:
The Maximum Sharpe Ratio Portfolio's Expected Return is 27.41% and its Standard Deviation is 14.23%

      Portfolio Weight
MSFT            54.42%
PG              36.44%
HLI              9.13% 
[3 rows x 1 column]
```

### Minimum Variance Portfolio
Retreive a pie chart including stock portfolio weights and a chart of portfolio weights for chosen stocks with `pc(ticker_list).min_std_portfolio()`.
```python
>>> from PortfolioOptimizer import PortfolioCalculations as pc
>>> ticker_list = ['MSFT', 'PG', 'HLI']
>>> pc(ticker_list).min_std_portfolio()

Minimum Variance Portfolio:
The Minimum Variance Portfolio's Expected Return is 23.07% and its Standard Deviation is 13.12%

      Portfolio Weight
MSFT            29.23%
PG              57.19%
HLI             13.58% 
[3 rows x 1 column]
```

## Portfolio Graphics
### Efficient Frontier

### Expected Returns and Standard Deviation Error

### Final Capital Allocation
