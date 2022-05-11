from pynance.datasources.data_retriever import TickerError
from pynance.portfolio_optimizer import PortfolioCalculations as pc

def main():
    
    while True:
        try:
            tickers = input('Please enter comma-separated list of stock tickers: \n')   
            ticker_list = tickers.split(', ')
            portfolio_optimizer_instance = pc(ticker_list)
            break
        except TickerError:
            print("Please enter valid ticker symbols. \n")
            continue
    
    continue_code = True
    while continue_code == True:

        # Request Validation
        validRequest = False
        while not validRequest:
            while True:
                try:
                    request = int(input(
                        '''Please choose one of the following options by inputting the appropriate number:
                        \n 1. Max Sharpe Portfolio \n 2. Min Variance Portfolio \n 3. Efficient Frontier  \n'''
                    ))
                    break
                except ValueError:
                    print('Please enter a valid response. \n')
                    continue

            if request == 1 or request == 2 or request == 3:
                validRequest = True
                continue
            else:
                print('Please enter a valid response. \n')

        # Get Request
        if request == 1:
            print('Maximum Sharpe Ratio Portfolio:')
            max_sharpe_portfolio = portfolio_optimizer_instance.max_sharpe_portfolio()
            print(max_sharpe_portfolio, '\n')
        elif request == 2:
            print('Minimum Variance Portfolio:')
            min_var_portfolio = portfolio_optimizer_instance.min_var_portfolio()
            print(min_var_portfolio, '\n')
        elif request == 3:
            print('Efficient Frontier and Capital Allocation Line:')
            portfolio_optimizer_instance.efficient_frontier()
        else:
            return

        # Data Validation
        validResponse = False
        while not validResponse:
            continue_code_input = int(input(
                '''Would you like to:
                \n 1. View another portfolio \n 2. End program \n'''
            ))
            if continue_code_input == 1 or continue_code_input == 2:
                validResponse = True
                continue
            else:
                print("Please enter a valid response. \n")
            
        if continue_code_input == 1:
            continue_code = True
        elif continue_code_input == 2:
            continue_code = False

main()