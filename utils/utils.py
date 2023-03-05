import pandas as pd
import numpy as np
import yfinance as yf


def read_tickers():
    with open("data/us_symbols.csv", "r") as f:
        lines = f.readlines()

    rows = [
        f"{line.split(',')[0]} - {line.split(',')[1]} ({line.split(',')[2].strip()})" for line in lines]

    return rows


def get_data(ticker_string, start, end):
    data = yf.download(ticker_string, start=start, end=end)
    return data['Close']


def moving_avg(data, days):
    return data.rolling(window=days).mean()


def add_avgs(data, short_avg, long_avg):
    short = moving_avg(data, short_avg)
    long = moving_avg(data, long_avg)
    df = pd.concat((short.rename("Short"), long.rename("Long"), data), axis=1)
    df.dropna(inplace=True)
    return df


def calc_percents(starting_price, prices):
    prices = prices['Close']
    percs = []
    last_price = starting_price
    for curr_price in prices:
        perc = (curr_price - last_price) / last_price
        percs.append(perc)
        last_price = curr_price

    return percs


def find_intersections(df):
    # find the intersections
    df['difference'] = df.Short - df.Long
    # when difference is <0, we sell
    # when difference is >0, we buy
    df['cross'] = np.sign(df.difference.shift(1)) != np.sign(df.difference)
    df['decision'] = df['difference'].apply(
        lambda x: 'sell' if x < 0 else 'buy')
    dates_where_cross = df[df.cross == True].index[1:]

    # remove the first buy (we'll buy at the start of the date)
    intersections = df[df.index.isin(dates_where_cross)]
    if intersections.shape[0] == 0:
        return pd.DataFrame(columns=["Close", 'decision'])
    if intersections['decision'].values[0] == 'buy':
        intersections = intersections.iloc[1:]
    intersections = intersections[['Close', 'decision']]

    # add the initial price
    initial_price = df.Close.values[0]
    intersections.index = pd.to_datetime(intersections.index)
    intersections.loc[df.index[0]] = [initial_price, 'buy']
    intersections = intersections.sort_index()

    return intersections


def get_margins(initial_investment, percs):
    margins = []
    # text = ""
    for _, row in percs.iterrows():
        if row['decision'] == 'sell':  # sell
            # text += f"Selling at price {row['Close']:.2f}, netted {initial_investment * row['percs']:.2f}\n"
            margins.append(initial_investment*row['percs'])
        else:
            # text += f"Investing ${initial_investment:.2f} at price: {row['Close']:.2f}\n"
            margins.append(0)
    return margins


# I need these columns:
# buy date, close on buy, sell date, close on sell, percent_diff, margin
def melt_intersections(intersection_dates, stock_data, initial_investment):
    # loop through dates
    rows = []
    for i, date in enumerate(intersection_dates):
        if i % 2 == 0:
            # we are buying
            buy_date = date
            buy_close_price = stock_data.loc[buy_date]
        elif i % 2 != 0:
            # we are selling
            sell_date = date
            sell_close_price = stock_data.loc[sell_date]

            # do the calculations (for every sell there must be a buy)
            percent = (sell_close_price - buy_close_price) / buy_close_price
            # margin
            margin = initial_investment * percent

            row = [buy_date, buy_close_price, sell_date,
                   sell_close_price, percent, margin]
            rows.append(row)

    cols = ["buy_date", "buy_price", "sell_date",
            "sell_price", "percent", "margin"]

    return pd.DataFrame(data=rows, columns=cols)
