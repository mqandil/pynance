# CHANGELOG
## **v1.0.0 Release: May 11, 2022**
First full release of `pynance`!
### Functionality
- `portfolio_optimizer:` completed module for optimization of portfolio with selected stock data with the following functionality:
    - [max_sharpe_portfolio()](/pynance/docs/max_sharpe_portfolio.md)
    - [min_var_portfolio()](/pynance/docs/min_std_portfolio.md)
    - [efficient_frontier()](/pynance/docs/efficient_frontier.md)
    - [expected_return_range()](/pynance/docs/expected_return_range.md)
    - [capital_allocation()](/pynance/docs/capital_allocation.md)
- `valuation_virtuoso:` module for firm valuation is in production and will be released at a later date

### Other Updates
- Install `pynance` via the repo at https://github.com/mqandil/pynance (see [README.md](README.md) for full instructions on installation)
- [Docs](docs) now describe all functionality for `portfolio_optimizer`
- Updated `setup.py` to include all requirements
- Note that some errors may still occur for large requests or specific stock tickers. If a specific ticker does not work, try again in 24 hours.

## **v0.0.2-beta.1 Release: May 10, 2022**
### Updated User Interface
- `efficient_frontier`: Graph of Efficient Frontier denoting Max Sharpe Ratio Portfolio and CAL
- `expected_return_range`: Expected Return Range Graph (STD Error Bars and E(Rp) by Portfolio)
- `capital_allocation`: Full Capital Allocation Information by Portfolio ID

### Added Functionality
- `__portfolio_data`: Transfers Portfolio Allocation Data to internal-only Function

## **v0.0.1-beta.1 Release: May 3, 2022**
First beta test.