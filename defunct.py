import scipy
from Data_Aggregator import return_aggregator as ra
from scipy import optimize
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd

#from Risk_Free_Rate import risk_free_rate

class PortfolioCalculations():
  def __init__(self):
    pass

  def max_sharpe_port():
    pass

  def min_std_results():
    pass

  def efficient_frontier():
    pass


ar = ra()
expected_return_data = ar.mean()
covariance_matrix = ar.cov()

stock_count = list(range(0, len(ar.columns)))
portfolio_weights = []
for value in stock_count:
    portfolio_weights.append(1/len(ar.columns))

portfolio_standard_deviation = math.sqrt(np.dot(portfolio_weights, np.dot(covariance_matrix, portfolio_weights)))
portfolio_expected_return = np.dot(portfolio_weights, expected_return_data)

def portfolio_returns(weights):
    return np.dot(weights, expected_return_data)

def portfolio_std(weights):
    return math.sqrt(np.dot(weights, np.dot(covariance_matrix, weights)))

#Monte Carlo Simul
portfolio_returns_list = []
portfolio_std_list = []
weights_list = []

for p in range(10000):
    weights = np.random.random(size = len(ar.columns))
    weights /= np.sum(weights)

    portfolio_returns_list.append(portfolio_returns(weights))
    portfolio_std_list.append(portfolio_std(weights))

    port_returns = np.array(object=portfolio_returns_list)
    port_std = np.array(object=portfolio_std_list)


#Optimal Portfolio
def sharpe_fun(weights):
    return - (portfolio_returns(weights) / portfolio_std(weights))

constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
bounds = tuple(
  (0, 1) for w in weights
)

equal_weights = np.array(
  [1 / len(ar.columns)] * len(ar.columns)
)

max_sharpe_results = optimize.minimize(
  # Objective function
  fun = sharpe_fun, 
  # Initial guess, which is the equal weight array
  x0 = equal_weights, 
  method = 'SLSQP',
  bounds = bounds, 
  constraints = constraints
)

#MAX SHARPE PORTFOLIO
max_sharpe_results["x"]
max_sharpe_port_return = portfolio_returns(max_sharpe_results["x"])
adj_max_sharpe_port_return = round(max_sharpe_port_return, 4)
max_sharpe_port_sd = portfolio_std(max_sharpe_results["x"])
adj_max_sharpe_port_sd = round(max_sharpe_port_sd, 4)
max_sharpe_port_sharpe = max_sharpe_port_return / max_sharpe_port_sd
adj_max_sharpe_port_sharpe = round(max_sharpe_port_sharpe, 4)


portfolio_results = [f'{value*100:.2f}%' for value in max_sharpe_results["x"]]

final_results = pd.DataFrame(
    data=portfolio_results,
    index=ar.columns,
    columns=["Portfolio Weight"]
)

print(final_results)

min_sd_results = optimize.minimize(
  # Objective function
  fun = portfolio_std, 
  # Initial guess, which is the equal weight array
  x0 = equal_weights, 
  method = 'SLSQP',
  bounds = bounds, 
  constraints = constraints
)

min_sd_port_return = portfolio_returns(min_sd_results["x"])
round(min_sd_port_return, 4)
min_sd_port_sd = portfolio_std(min_sd_results["x"])
round(min_sd_port_sd, 4)
min_sd_port_sharpe = min_sd_port_return / min_sd_port_sd
round(min_sd_port_sharpe, 4)


#Efficient Frontier

constraints = (
  {'type': 'eq', 'fun': lambda x: portfolio_returns(x) - target}, 
  {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
)

bounds = tuple(
  (0, 1) for w in weights
)

target = np.linspace(
  start = 0, 
  stop = 0.06,
  num = 100
)
# instantiate empty container for the objective values to be minimized
obj_sd = []
# For loop to minimize objective function
for target in target:
  min_result_object = optimize.minimize(
    # Objective function
    fun = portfolio_std, 
    # Initial guess, which is the equal weight array
    x0 = equal_weights, 
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
  stop = 0.06,
  num = 100
)

#print(target)

#plt.scatter(obj_sd, target)

print(max_sharpe_port_return, max_sharpe_port_sd)


