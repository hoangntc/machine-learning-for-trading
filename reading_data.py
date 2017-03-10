"""Utility functions"""
"""
This function reads all stock dataframes and returns a dataframe with the information of stock we want to take (eg: Adj Close, Close)
Note: We use date as index to access rows of dataframe
"""

import os
import pandas as pd

def symbol_to_path(symbol, base_dir="data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        df_sym = pd.read_csv(symbol_to_path(symbol, base_dir="data"), index_col='Date',
                            parse_dates=True,usecols=['Date', 'Adj Close'], na_values='nan')
        df_sym = df_sym.rename(columns={'Adj Close': symbol})
        df = df.join(df_sym, how='inner')

    return df

def test_run():
    """This function shows how to use get_data function"""
    # Define a date range
    dates = pd.date_range('2010-01-22', '2010-01-26')

    # Choose stock symbols to read
    symbols = ['GOOG', 'IBM', 'GLD']
    
    # Get stock data
    df = get_data(symbols, dates)
    print(df)

    # Slice by row
    print(df.ix['2010-01-22': '2010-01-24'])

    # Slice by column
    print(df[['SPY', 'IBM']])
    # Slice by row and column
    print(df.ix['2010-01-22': '2010-01-24', ['SPY', 'IBM']])

#if __name__ == "__main__":
#    test_run()
