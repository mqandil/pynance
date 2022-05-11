from pynance.datahelpers.data_aggregator import return_aggregator as ra
from scipy import optimize
import numpy as np
import math
import pandas as pd
from pynance.datasources.get_risk_free_rate import get_risk_free_rate as grfr
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

    def __portfolio_data(self):
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
        
        #Insert and Format ER/STD
        portfolio_weights_df.insert(0, "Standard Deviation", annual_obj_sd)
        portfolio_weights_df.insert(0, "Expected Return", annual_target)
        portfolio_weights_df['Expected Return'] = portfolio_weights_df['Expected Return'].round(4)
        portfolio_weights_df['Standard Deviation'] = portfolio_weights_df['Standard Deviation'].round(4)

        return portfolio_weights_df

    def __tangent_line_point(self):
        rfr = grfr() 
        #move tangent line data here from efficient frontier and expected return range

    def max_sharpe_portfolio(self, mode, download=False, file_path=None, file_name=None):
        
        #Ensures that mode is one of valid options
        valid = {'rr', 'df', 'pie'}
        if mode not in valid:
            raise ValueError("mode must be one of %r." % valid)

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

        if mode == 'rr':
            risk_reward_df = pd.DataFrame(
                data=[f'{((1+max_sharpe_port_return)**12-1)*100:.2f}%', f'{max_sharpe_port_sd*math.sqrt(12)*100:.2f}%'],
                index=['Expected Return', 'Standard Deviation'],
                columns=['Max Sharpe Portfolio']
            )

            if download == True:
                if file_name == None:
                    raise ValueError("file_name must be given: e.g. max_sharpe_rr.csv")
                else:
                    max_sharpe_final_results.to_csv(file_name)

            else:
                return risk_reward_df

        elif mode == 'df':
            max_sharpe_portfolio_results = [f'{value*100:.2f}%' for value in max_sharpe_results["x"]]

            max_sharpe_final_results = pd.DataFrame(
                data=max_sharpe_portfolio_results,
                index=self.ar.columns,
                columns=["Portfolio Weight"]
            )
            if download == True:
                if file_name == None:
                    raise ValueError("file_name must be given: e.g. max_sharpe_allocations.csv")
                else:
                    max_sharpe_final_results.to_csv(file_name)
            else:
                return max_sharpe_final_results

        elif mode == 'pie':
            # pie info
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
            
            if download == True:
                if file_path == None:
                    raise ValueError('file_path must be given: e.g. /Users/User/Desktop/Folder/file.html')
                
                else:
                    max_sharpe_fig.write_html(file_path)
            else:
                return max_sharpe_fig

    def min_var_portfolio(self, mode, download=False, file_path=None, file_name=None):
        
        valid = {'rr', 'df', 'pie'}
        if mode not in valid:
            raise ValueError("mode must be one of %r." % valid)

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

        if mode == 'rr':
            min_var_df = pd.DataFrame(
                data=[f'{((min_std_port_return+1)**12-1)*100:.2f}%', f'{min_std_port_std*math.sqrt(12)*100:.2f}%'],
                index=['Expected Return', 'Standard Deviation'],
                columns=['Min Var Portfolio']
            )
            if download == True:
                if file_name == None:
                    raise ValueError("file_name must be given: e.g. min_var_rr.csv")
                else:
                    min_var_df.to_csv(file_name)
            else:
                return min_var_df

        elif mode == 'df':
            min_std_portfolio_results = [f'{value*100:.2f}%' for value in min_std_results["x"]]

            min_std_final_results = pd.DataFrame(
                data=min_std_portfolio_results,
                index=self.ar.columns,
                columns=["Portfolio Weight"]
            )
            if download == True:
                if file_name == None:
                    raise ValueError("file_name must be given: e.g. min_var_allocations.csv")
                else:
                    min_std_final_results.to_csv(file_name)
            else:
                return min_std_final_results

        elif mode == 'pie':

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
            
            if download == True:
                if file_path == None:
                    raise ValueError('file_path must be given: e.g. /Users/User/Desktop/Folder/file.html')
                else:
                    min_var_fig.write_html(file_path)
            else:
                return min_var_fig

    def efficient_frontier(self, download=False, file_path=None):

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
        # tangent_y = [rfr, max_sharpe_port_return]
        # tangent_x = [0, max_sharpe_port_std]

        #Data for Portfolio Calcs
        portfolio_weights_df = PortfolioCalculations(self.ticker_list).__portfolio_data()
        print(portfolio_weights_df.head(20))

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

        #Edit this to make calculations for all stock rankings ^^

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
        efficient_frontier_fig.update_layout(yaxis_tickformat=',.2%')
        efficient_frontier_fig.update_layout(xaxis_tickformat=',.2%')

        if download == True:
                if file_path == None:
                    raise ValueError('file_path must be given: e.g. /Users/User/Desktop/Folder/file.html')
                
                else:
                    efficient_frontier_fig.write_html(file_path)

        else:
            return efficient_frontier_fig

    def expected_return_range(self, download=False, file_path=None):
        portfolio_data = PortfolioCalculations(self.ticker_list).__portfolio_data().iloc[:, 0:2]
        #add dot for minimum std and max sharpe ratio

        fig_expected_return_range = go.Figure([
            go.Scatter(
                name='E(Rp)',
                x=portfolio_data.index,
                y=portfolio_data['Expected Return'],
                mode='lines',
                line=dict(color='rgb(31, 119, 180)'),
            ),
            go.Scatter(
                name='μ+σ',
                x=portfolio_data.index,
                y=portfolio_data['Expected Return']+portfolio_data['Standard Deviation'],
                mode='lines',
                marker=dict(color='green'),
                line=dict(width=0.5),
                showlegend=True
            ),
            go.Scatter(
                name='μ-σ',
                x=portfolio_data.index,
                y=portfolio_data['Expected Return']-portfolio_data['Standard Deviation'],
                marker=dict(color="red"),
                line=dict(width=0.5),
                mode='lines',
                fillcolor='rgba(68, 68, 68, 0.3)',
                fill='tonexty',
                showlegend=True
            )
        ])
        fig_expected_return_range.update_layout(
            yaxis_title='Portfolio Expected Return',
            xaxis_title='Portfolio ID',
            title='Expected Return (+/- 1 Standard Deviation)',
            hovermode="x"
        )
        fig_expected_return_range.update_layout(yaxis_tickformat=',.2%')

        #add functionality for lines on max sharpe and min std portfolio points
        #put in new function and return datapoints + portfolio ID (x value)

        if download == True:
                if file_path == None:
                    raise ValueError('file_path must be given: e.g. /Users/User/Desktop/Folder/file.html')
                
                else:
                    fig_expected_return_range.write_html(file_path)
        else:
            return fig_expected_return_range

    def capital_allocation(self, portfolio_id, download=False, file_name='portfolio_id_data.csv'):
        portfolio_data = PortfolioCalculations(self.ticker_list).__portfolio_data().iloc[:, 2:]

        ####MUST ENSURE THAT ID IS VALID AND NUMERIC
        portfolio_index = int(portfolio_id)
        portfolio_ID_data = portfolio_data.iloc[portfolio_index, :]
        portfolio_data_pcts = [f'{i*100:.2f}%' for i in list(portfolio_ID_data)]
        portfolio_ID_data_df = pd.DataFrame(
            data=portfolio_data_pcts,
            index=list(portfolio_ID_data.index.values),
            columns=['Portfolio Weight']
        )

        if download == True:
                if file_name == None:
                    raise ValueError("file_name must be given: e.g. portfolio_id_allocations.csv")
                else:
                    portfolio_ID_data_df.to_csv(file_name)
        else:
            return portfolio_ID_data_df


if __name__ == '__main__':
    # ticker_list = [
    #     "XOM", "SHW", "JPM", "AEP", 'SNAP', 'F', 'AAPL', 'MSFT', 'BP', 'ABNB', 'PFE', 'CHGG'
    # ]
    ticker_list = ['MSFT', 'PG', 'HLI']
    # print(PortfolioCalculations(ticker_list).max_sharpe_portfolio())
    # print(PortfolioCalculations(ticker_list).min_std_portfolio())
    test = PortfolioCalculations(ticker_list).max_sharpe_portfolio('rr')
    print(test)
    # print(test.head(3))
    # test.show()