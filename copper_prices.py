import util
import Quandl

COPPER_PRICES_NAME = "imf_copper_monthly"

def getCopperPrices(update=False):
    prices = None
    if update or not util.pickleExists(COPPER_PRICES_NAME):
        prices = Quandl.get("ODA/PCOPP_USD", returns="numpy", authtoken="xx_T2u2fsQ_MjyZjTb6E")
        util.savePickle(prices, COPPER_PRICES_NAME)
    else:
        prices = util.getMostRecentPickle(COPPER_PRICES_NAME)

    return prices

def preprocessPrices(prices):
    X = [[entry[0].toordinal()] for entry in prices]
    y = [float(entry[1]) for entry in prices]

    return X, y