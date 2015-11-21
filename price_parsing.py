import util
import Quandl

STOCK_DATA_SOURCE = "YAHOO/" # Yahoo seems like a good source

def getStockPrices(ticker, frequency="monthly", update=False):
    name = ticker + "_" + frequency
    prices = None
    if update or not util.pickleExists(name):
        prices = Quandl.get(STOCK_DATA_SOURCE + ticker, collapse=frequency, authtoken="xx_T2u2fsQ_MjyZjTb6E")
        util.savePickle(prices, name)
    else:
        prices = util.getMostRecentPickle(name)

    return prices.get("Close")

def getStockPriceDifferentials(ticker, frequency="monthly", update=False):
    name = ticker + "_differentials_" + frequency
    prices = None
    if update or not util.pickleExists(name):
        prices = Quandl.get(STOCK_DATA_SOURCE + ticker, collapse=frequency, transform="rdiff", authtoken="xx_T2u2fsQ_MjyZjTb6E")
        util.savePickle(prices, name)
    else:
        prices = util.getMostRecentPickle(name)

    return prices.get("Close")

# prices = pandas time series
# before = lower limit
# after = upper limit
def getDateRange(prices, before, after):
    return prices.truncate(before=before, after=after)

def preprocessStocks(priceData):
    timestamps = []
    prices = []
    for row in priceData.iteritems():
        timestamps.append([row[0].toordinal()])
        prices.append(float(row[1]))
    #timestamps = [[row[0].toordinal()] for row in priceData.iteritems()]
    #prices = [float(row[1]) for row in priceData.iteritems()]

    return timestamps, prices