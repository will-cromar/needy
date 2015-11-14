import util
import Quandl

COPPER_PRICES_NAME = "imf_copper_monthly"

prices = None
if not util.pickleExists(COPPER_PRICES_NAME):
    prices = Quandl.Quandl.get("ODA/PCOPP_USD")
    util.savePickle(prices, COPPER_PRICES_NAME)
else:
    prices = util.getMostRecentPickle(COPPER_PRICES_NAME)

print prices