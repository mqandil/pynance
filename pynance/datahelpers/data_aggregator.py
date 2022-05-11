from pynance.datasources.data_retriever import dataretriever as dr
import pandas as pd

def return_aggregator(ticker_list):
    ticker_data_list = []
    data_count = 0
    ticker_data_indexes = []

    for ticker in ticker_list:
        ticker_data = dr(ticker)
        ticker_data_list.append(list(ticker_data))
        data_count = ticker_data.count()
        ticker_data_indexes = ticker_data.index

    aggregated_returns = pd.DataFrame(
        data=ticker_data_list,
        index=ticker_list,
        columns=ticker_data_indexes
    )

    aggregated_returns = aggregated_returns.transpose()
    return aggregated_returns

if __name__ == "__main__":
    print(return_aggregator(['AAPL', 'MSFT']))