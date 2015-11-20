import util
import Quandl

COPPER_PRICES_NAME = "imf_copper_monthly"
STOCK_DATA_SOURCE = "YAHOO/" # Yahoo seems like a good source

#Deprecated -- Remove before turning in
def getCopperPrices(update=False):
    prices = None
    if update or not util.pickleExists(COPPER_PRICES_NAME):
        prices = Quandl.get("ODA/PCOPP_USD", returns="numpy", authtoken="xx_T2u2fsQ_MjyZjTb6E")
        util.savePickle(prices, COPPER_PRICES_NAME)
    else:
        prices = util.getMostRecentPickle(COPPER_PRICES_NAME)

    return prices
#Also deprecated
def preprocessCopperPrices(prices):
    X = [[entry[0].toordinal()] for entry in prices]
    y = [float(entry[1]) for entry in prices]

    return X, y

def getStockPrices(ticker, frequency="monthly", update=False):
    name = ticker + "_" + frequency
    prices = None
    if update or not util.pickleExists(name):
        prices = Quandl.get(STOCK_DATA_SOURCE + ticker, collapse=frequency, authtoken="xx_T2u2fsQ_MjyZjTb6E")
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