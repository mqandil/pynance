import scipy
from Data_Aggregator import return_aggregator as ra
from scipy import optimize
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from Risk_Free_Rate import get_risk_free_rate as grfr

class PortfolioCalculations():
    def __init__(self):
        self.ar = ra()
        self.expected_return_data = self.ar.mean()
        self.covariance_matrix = self.ar.cov()

        self.stock_count = list(range(0, len(self.ar.columns)))
        self.portfolio_weights = []
        for value in self.stock_count:
            self.portfolio_weights.append(1/len(self.ar.columns))

        #Monte Carlo Simul
        portfolio_returns_list = []
        portfolio_std_list = []
        weights_list = []

        for p in range(10000):
            self.weights = np.random.random(size = len(self.ar.columns))
            self.weights /= np.sum(self.weights)

            portfolio_returns_list.append(self.__portfolio_returns(self.weights))
            portfolio_std_list.append(self.__portfolio_std(self.weights))

            port_returns = np.array(object=portfolio_returns_list)
            port_std = np.array(object=portfolio_std_list)


        #Optimal Portfolio
        
        self.constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        self.bounds = tuple(
        (0, 1) for w in self.weights
        )
        self.equal_weights = np.array(
        [1 / len(self.ar.columns)] * len(self.ar.columns)
        )

    def __sharpe_fun(self, weights):
            return - (self.__portfolio_returns(weights) / self.__portfolio_std(weights))

    def __portfolio_returns(self, weights):
        return np.dot(weights, self.expected_return_data)

    def __portfolio_std(self, weights):
        return math.sqrt(np.dot(weights, np.dot(self.covariance_matrix, weights)))

    def max_sharpe_portfolio(self):
    
        max_sharpe_results = optimize.minimize(
            # Objective function
            fun = self.__sharpe_fun, 
            # Initial guess, which is the equal weight array
            x0 = self.equal_weights, 
            method = 'SLSQP',
            bounds = self.bounds, 
            constraints = self.constraints
        )

        max_sharpe_port_return = self.__portfolio_returns(max_sharpe_results["x"])
        max_sharpe_port_sd = self.__portfolio_std(max_sharpe_results["x"])
        #max_sharpe_port_sharpe = max_sharpe_port_return / max_sharpe_port_sd

        max_sharpe_portfolio_results = [f'{value*100:.2f}%' for value in max_sharpe_results["x"]]

        max_sharpe_final_results = pd.DataFrame(
            data=max_sharpe_portfolio_results,
            index=self.ar.columns,
            columns=["Portfolio Weight"]
        )

        risk_reward = f"The Portfolio's Expected Return is {max_sharpe_port_return*100:.2f}%, and the Portfolio's Standard Deviation is {max_sharpe_port_sd*100:.2f}%"
        print(risk_reward)

        return max_sharpe_final_results

    def min_std_portfolio(self):
        
        min_std_results = optimize.minimize(
        # Objective function
        fun = self.__portfolio_std, 
        # Initial guess, which is the equal weight array
        x0 = self.equal_weights, 
        method = 'SLSQP',
        bounds = self.bounds, 
        constraints = self.constraints
        )

        min_std_port_return = self.__portfolio_returns(min_std_results["x"])
        min_std_port_std = self.__portfolio_std(min_std_results["x"])
        #min_sd_port_sharpe = min_sd_port_return / min_sd_port_sd

        min_std_portfolio_results = [f'{value*100:.2f}%' for value in min_std_results["x"]]

        min_std_final_results = pd.DataFrame(
            data=min_std_portfolio_results,
            index=self.ar.columns,
            columns=["Portfolio Weight"]
        )

        risk_reward = f"The Portfolio's Expected Return is {min_std_port_return*100:.2f}%, and the Portfolio's Standard Deviation is {min_std_port_std*100:.2f}%"
        print(risk_reward)

        return min_std_final_results

    def efficient_frontier(self):
        constraints = (
            {'type': 'eq', 'fun': lambda x: self.__portfolio_returns(x) - target}, 
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        )

        bounds = tuple(
            (0, 1) for w in self.weights
        )

        target = np.linspace(
            start = 0, 
            stop = 0.03,
            num = 100
        )

        # instantiate empty container for the objective values to be minimized
        obj_sd = []
        # For loop to minimize objective function
        for target in target:
            min_result_object = optimize.minimize(
                # Objective function
                fun = self.__portfolio_std, 
                # Initial guess, which is the equal weight array
                x0 = self.equal_weights, 
                method = 'SLSQP',
                bounds = bounds, 
                constraints = constraints
            )
            # Extract the objective value and append it to the output container
            obj_sd.append(min_result_object['fun'])
            # End of for loop

        # Convert list to array
        obj_sd = np.array(obj_sd)
        # Rebind target to a new array object
        target = np.linspace(
        start = 0.0, 
        stop = 0.03,
        num = 100
        )

        #Plot Efficient Frontier
        plt.scatter(
            x = obj_sd, 
            y = target,
            s = 2,
            c = obj_sd
        )
        plt.ylabel("Portfolio Expected Return")
        plt.xlabel("Portfolio Standard Deviation")
        plt.title("Portfolio Efficient Frontier")
        plt.xlim(left=0)
        plt.ylim(bottom=0)

        #Data for Tangent Line
        rfr = grfr()
        max_sharpe_results = optimize.minimize(
            # Objective function
            fun = self.__sharpe_fun, 
            # Initial guess, which is the equal weight array
            x0 = self.equal_weights, 
            method = 'SLSQP',
            bounds = self.bounds, 
            constraints = self.constraints
        )
        max_sharpe_port_return = self.__portfolio_returns(max_sharpe_results["x"])
        max_sharpe_port_std = self.__portfolio_std(max_sharpe_results["x"])

        #Formatting for Tangent Line
        tangent_y = [rfr, max_sharpe_port_return]
        tangent_x = [0, max_sharpe_port_std]

        plt.plot(
            tangent_x,
            tangent_y,
            color='purple'
        )
        plt.show()



if __name__ == '__main__':
    print(PortfolioCalculations().max_sharpe_portfolio())
    print(PortfolioCalculations().min_std_portfolio())
    PortfolioCalculations().efficient_frontier()
