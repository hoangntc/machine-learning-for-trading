"""Utility functions"""
"""
This function reads all stock dataframes and returns a dataframe with the information of stock we want to take (eg: Adj Close, Close)
Note: We use date as index to access rows of dataframe
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

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


def plot_data(df, title="Stock prices"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()


def plot_selected(df, columns, start_index, end_index):
    """Plot the desired columns over index values in the given range."""
    df_selected = df.ix[start_index: end_index, columns]
    return plot_data(df_selected, title='Selected stock prices')

def normalize_data(df):
    """Normalize data before plotting to scale all stock prices"""
    return df/df.ix[0,:]

def get_rolling_mean(values, window):
    """Return rolling mean of given values, using specified window size."""
    return values.rolling(window=window, center=False).mean()


def get_rolling_std(values, window):
    """Return rolling standard deviation of given values, using specified window size."""
    return values.rolling(window=window, center=False).std()


def get_bollinger_bands(rm, rstd):
    """Return upper and lower Bollinger Bands."""
    upper_band = rm + rstd*2
    lower_band = rm - rstd*2
    return upper_band, lower_band

def compute_daily_return(df):
    #return (df/df.shift(1)) - 1
    daily_returns = df.copy()
    daily_returns[1:] = (df[1:]/ df[:-1].values) - 1
    daily_returns.ix[0, :] = 0
    return daily_returns


def compute_cumulative_return(df):
    daily_returns = df.copy()
    daily_returns[1:] = (df[1:]/ df[:-1].values) - 1 #need to modify here
    daily_returns.ix[0, :] = 0
    return (df/df[0]) - 1


def fill_missing_values(df_data):
    """Fill missing values in data frame, in place."""
    df_data.fillna(method='ffill', inplace=True)
    df_data.fillna(method='bfill', inplace=True)

def test_run():
    """This function shows how to use utility functions"""
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

    # Slice and plot
    plot_selected(df, ['SPY', 'IBM'], '2010-03-01', '2010-04-01')


def test_run_01_04():
    # Compute Bollinger Bands
    # 1. Compute rolling mean
    rm_SPY = get_rolling_mean(df['SPY'], window=20)

    # 2. Compute rolling standard deviation
    rstd_SPY = get_rolling_std(df['SPY'], window=20)

    # 3. Compute upper and lower bands
    upper_band, lower_band = get_bollinger_bands(rm_SPY, rstd_SPY)
    
    # Plot raw SPY values, rolling mean and Bollinger Bands
    ax = df['SPY'].plot(title="Bollinger Bands", label='SPY')
    rm_SPY.plot(label='Rolling mean', ax=ax)
    upper_band.plot(label='upper band', ax=ax)
    lower_band.plot(label='lower band', ax=ax)

    # Add axis labels and legend
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')
    plt.show()


def test_run_01_05():
    """Function called by Test Run."""
    # Read data
    symbol_list = ["JAVA", "FAKE1", "FAKE2"]  # list of symbols
    start_date = "2005-12-31"
    end_date = "2014-12-07"
    dates = pd.date_range(start_date, end_date)  # date range as index
    df_data = get_data(symbol_list, dates)  # get data for each symbol

    # Fill missing values
    fill_missing_values(df_data)

    # Plot
    plot_data(df_data)

#if __name__ == "__main__":
#   test_run()
#   test_run_01_04()
#   test_run_01_05()   