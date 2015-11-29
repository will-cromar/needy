import util
import Quandl

# For the moment, we're using Yahoo Finance as our source
STOCK_DATA_SOURCE = "YAHOO/"

def getStockPrices(ticker, frequency="monthly", update=False):
    """
    Gets the closing prices for a given stock ticker at a given frequency
    :param ticker: Name of the company's ticker
    :param frequency: Frequency of returned time series. See Quandl.get()'s collapse param.
    :param update: Always updates instead of using cache if true
    :return: Pandas dataframe representing time series of ticker's closing prices
    """
    name = ticker + "_" + frequency # Name of data in cache
    prices = None
    # If there is no cached version of the pickle, or update flag is on, download price data and cache it
    if update or not util.pickleExists(name):
        prices = Quandl.get(STOCK_DATA_SOURCE + ticker, collapse=frequency, authtoken="xx_T2u2fsQ_MjyZjTb6E")
        util.savePickle(prices, name)
    # Otherwise, use most recent cache entry
    else:
        prices = util.getMostRecentPickle(name)

    # Return closing prices
    return prices.get("Close")

# TODO: Merge with getStockPrices
def getStockPriceDifferentials(ticker, frequency="monthly", update=False):
    """
    Gets the percent differential of the closing prices for a given ticker
    :param ticker: Name of the company's ticker
    :param frequency: Frequency of returned time series. See Quandl.get()'s collapse param.
    :param update: Always updates instead of using cache if true
    :return: Pandas dataframe representing a time series of the closing price differentials for a ticker
    """
    name = ticker + "_differentials_" + frequency # Name of data in cache
    prices = None
    # If there is no cached version of the pickle, or update flag is on, download price data and cache it
    if update or not util.pickleExists(name):
        prices = Quandl.get(STOCK_DATA_SOURCE + ticker, collapse=frequency, transform="rdiff", authtoken="xx_T2u2fsQ_MjyZjTb6E")
        util.savePickle(prices, name)
    # Otherwise, use most recent cache entry
    else:
        prices = util.getMostRecentPickle(name)

    return prices.get("Close")

def getDateRange(prices, before, after):
    """
    Takes a pandas dataframe and truncates it to include only dates between before and after
    :param prices: Pandas dataframe representing a time series
    :param before: Datetime-like object representing the lower limit
    :param after: Datetime-like object representing the upper limit
    :return: Truncated Pandas dataframe
    """
    return prices.truncate(before=before, after=after)

def splitByDate(prices, date):
    return prices.truncate(after=date), prices.truncate(before=(date))

def preprocessStocks(priceData):
    """
    Processes priceData into a format usable by sklearn
    :param priceData: Pandas dataframe representing a time series of prices
    :return: List of ordinal dates, list of float prices
    """
    timestamps = []
    prices = []

    # For every tuple of (date, price) in priceData...
    for row in priceData.iteritems():
        timestamps.append(row[0].toordinal()) # Convert date to ordinal
        prices.append(float(row[1]))            # Convert price to float

    # Return in form X, y
    return timestamps, prices
