import util

import Quandl
import sklearn
from sklearn import tree
from sklearn import svm
from sklearn.cross_validation import train_test_split
from sklearn import ensemble

COPPER_PRICES_NAME = "imf_copper_monthly"

def getCopperPrices():
    prices = None
    if not util.pickleExists(COPPER_PRICES_NAME):
        prices = Quandl.get("ODA/PCOPP_USD", returns="numpy", authtoken="xx_T2u2fsQ_MjyZjTb6E")
        util.savePickle(prices, COPPER_PRICES_NAME)
    else:
        prices = util.getMostRecentPickle(COPPER_PRICES_NAME)

    return prices

def preprocessPrices(prices):
    labels = [[i[0].year, i[0].month] for i in prices]
    features = [float(i[1]) for i in prices]

    return labels, features

#Tests out different regressors in regs
#not finished
def test(regs):
    prices = getCopperPrices()
    labels, features = preprocessPrices(prices)
    labels_train, labels_test, features_train, features_test = \
        train_test_split(labels, features, test_size=.2, random_state = 42)

    for entry in regs:
        name = entry[0]
        reg = entry[1]

    return None

regs = [("Decision tree: ", tree.DecisionTreeRegressor()),
        ("Support vector regressor: ", svm.SVR())]