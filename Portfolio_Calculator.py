from operator import index
import scipy
from Data_Aggregator import return_aggregator as ra
from scipy import optimize
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from Risk_Free_Rate import get_risk_free_rate as grfr
import plotly.express as px
import plotly.graph_objects as go


class PortfolioCalculations():
    
    def __init__(self, ticker_list):
        self.ticker_list = ticker_list
        self.ar = ra(self.ticker_list)
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

        risk_reward = f"The Maximum Sharpe Ratio Portfolio's Expected Return is {((1+max_sharpe_port_return)**12-1)*100:.2f}% and its Standard Deviation is {max_sharpe_port_sd*math.sqrt(12)*100:.2f}%"
        print(risk_reward)

        fig_max_sharpe_results = pd.DataFrame(
            data=max_sharpe_results["x"],
            index=self.ar.columns,
            columns=["Portfolio Weight"]
        )
        fig_max_sharpe_results=fig_max_sharpe_results.loc[~(fig_max_sharpe_results==0).all(axis=1)]

        max_sharpe_fig = px.pie(
            fig_max_sharpe_results,
            names=fig_max_sharpe_results.index,
            values='Portfolio Weight',
            color_discrete_sequence=px.colors.sequential.Bluyl
        )
        max_sharpe_fig.update_traces(textposition='inside')
        max_sharpe_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        max_sharpe_fig.show()

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

        risk_reward = f"The Minimum Variance Portfolio's Expected Return is {((min_std_port_return+1)**12-1)*100:.2f}% and its Standard Deviation is {min_std_port_std*math.sqrt(12)*100:.2f}%"
        print(risk_reward)

        fig_min_var_results = pd.DataFrame(
            data=min_std_results["x"],
            index=self.ar.columns,
            columns=["Portfolio Weight"]
        )
        fig_min_var_results=fig_min_var_results.loc[~(fig_min_var_results==0).all(axis=1)]

        min_var_fig = px.pie(
            fig_min_var_results,
            names=fig_min_var_results.index,
            values='Portfolio Weight',
            color_discrete_sequence=px.colors.sequential.Bluyl
        )
        min_var_fig.update_traces(textposition='inside')
        min_var_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        min_var_fig.show()

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
            stop = 0.1,
            num = 1000
        )

        # instantiate empty container for the objective values to be minimized
        obj_sd = []
        obj_port_weight = []
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
            obj_port_weight.append(min_result_object['x'].tolist())
            # End of for loop

        # Convert list to array
        obj_sd = np.array(obj_sd)
        # Rebind target to a new array object
        target = np.linspace(
        start = 0.0, 
        stop = 0.1,
        num = 1000
        )

        # Determine End of EF Line
        change_in_std = np.diff(obj_sd) / obj_sd[:-1] * 100
        change_in_std = np.round(change_in_std, 3)
        
        # Remove Datapoints outside efficient frontier
        zero_change_indices = []
        i = 0
        for percent in change_in_std:
            if percent == 0:
                zero_change_indices.append(i)
            i += 1
        zero_change_indices.append(obj_sd.size-1)

        obj_sd = np.delete(obj_sd, zero_change_indices)
        target = np.delete(target, zero_change_indices)

        # Removes Portfolio Weights for portfolios outside efficient frontier - new lst
        eff_front_port_weights = []
        i = 0
        for lst in obj_port_weight:
            if i not in zero_change_indices:
                eff_front_port_weights.append(lst)
            i += 1

        annual_obj_sd = obj_sd*math.sqrt(12)
        annual_target = (1+target)**12-1

        portfolio_weights_df = pd.DataFrame(
            data=eff_front_port_weights,
            columns=self.ticker_list
        )

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
        max_sharpe_port_return = (1+self.__portfolio_returns(max_sharpe_results["x"]))**12-1
        max_sharpe_port_std = (self.__portfolio_std(max_sharpe_results["x"]))*math.sqrt(12)

        #Formatting for Tangent Line
        tangent_y = [rfr, max_sharpe_port_return]
        tangent_x = [0, max_sharpe_port_std]
        
        #Insert and Format ER/STD
        portfolio_weights_df.insert(0, "Standard Deviation", annual_obj_sd)
        portfolio_weights_df.insert(0, "Expected Return", annual_target)
        portfolio_weights_df['Expected Return'] = portfolio_weights_df['Expected Return'].round(4)
        portfolio_weights_df['Standard Deviation'] = portfolio_weights_df['Standard Deviation'].round(4)

        column_end = len(portfolio_weights_df.columns)
        portfolio_weights_df['Stock 1 Pct'] = portfolio_weights_df.iloc[:, 2:column_end-1].apply(lambda x: x.nlargest(1).iloc[0], axis=1)
        portfolio_weights_df['Stock 2 Pct'] = portfolio_weights_df.iloc[:, 2:column_end-1].apply(lambda x: x.nlargest(2).iloc[-1], axis=1)
        portfolio_weights_df['Stock 3 Pct'] = portfolio_weights_df.iloc[:, 2:column_end-1].apply(lambda x: x.nlargest(3).iloc[-1], axis=1)
        portfolio_weights_df['Stock 1 Name'] = portfolio_weights_df.iloc[:, 2:column_end-1].idxmax(axis=1)
        portfolio_weights_df['Stock 2 Name'] = portfolio_weights_df.iloc[:, 2:column_end-1].apply(lambda x: x.nlargest(2).idxmin(), axis=1)
        portfolio_weights_df['Stock 3 Name'] = portfolio_weights_df.iloc[:, 2:column_end-1].apply(lambda x: x.nlargest(3).idxmin(), axis=1)
        
        portfolio_weights_df['Stock 1 Pct'] = (portfolio_weights_df['Stock 1 Pct']*100).round(2).astype(str)+'%'
        portfolio_weights_df['Stock 2 Pct'] = (portfolio_weights_df['Stock 2 Pct']*100).round(2).astype(str)+'%'
        portfolio_weights_df['Stock 3 Pct'] = (portfolio_weights_df['Stock 3 Pct']*100).round(2).astype(str)+'%'

        portfolio_weights_df['Stock 1'] = portfolio_weights_df["Stock 1 Name"] + ': ' + portfolio_weights_df["Stock 1 Pct"].astype(str)
        portfolio_weights_df['Stock 2'] = portfolio_weights_df["Stock 2 Name"] + ': ' + portfolio_weights_df["Stock 2 Pct"].astype(str)
        portfolio_weights_df['Stock 3'] = portfolio_weights_df["Stock 3 Name"] + ': ' + portfolio_weights_df["Stock 3 Pct"].astype(str)

        efficient_frontier_fig = px.scatter(
            data_frame=portfolio_weights_df,
            x='Standard Deviation', 
            y='Expected Return',
            title='Portfolio Efficient Frontier',
            color='Standard Deviation',
            color_continuous_scale='aggrnyl',
            hover_data=['Stock 1', 'Stock 2', 'Stock 3']
        )
        efficient_frontier_fig.update_traces(marker={'size': 3})
        efficient_frontier_fig.update_traces(mode='markers+lines')
        efficient_frontier_fig.add_shape(
            type='line',
            x0=0,
            y0=rfr/100,
            x1=max_sharpe_port_std,
            y1=max_sharpe_port_return
        )
        efficient_frontier_fig.add_annotation(
            x=max_sharpe_port_std,
            y=max_sharpe_port_return,
            text='Maximum Sharpe Ratio Portfolio',
            showarrow = True,
            arrowhead=2,
            yshift=10,
            xshift=0
        )

        efficient_frontier_fig.show()

    def capital_allocation(self):
        pass
        # cal_data = self.efficient_frontier
        # cal_data.rfr
        # cal_data.max_sharpe_port_return

if __name__ == '__main__':
    ticker_list = [
        "XOM", "SHW", "JPM", "AEP", 'SNAP', 'F', 'AAPL', 'MSFT', 'BP', 'ABNB', 'PFE', 'CHGG'
    ]
    # print(PortfolioCalculations(ticker_list).max_sharpe_portfolio())
    # print(PortfolioCalculations(ticker_list).min_std_portfolio())
    PortfolioCalculations(ticker_list).efficient_frontier()

#monthly = (1+annual)^(1/12)-1
#monthly+1 = (1+annual)^(1/12)
#(1/12)*ln(monthly+1) = 1+annual
#annual = (monthly+1)^12 - 1