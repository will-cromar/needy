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
    X = [[i[0].year, i[0].month] for i in prices]
    y = [float(i[1]) for i in prices]

    return X, y

#Tests out different regressors in regs
#not finished
def test(regs):
    prices = getCopperPrices()
    X, y = preprocessPrices(prices)
    X_train, X_test, y_train, y_test = \
        train_test_split(X, y, test_size=.2, random_state = 42)

    #print X_train
    #print X_test
    #print y_train
    #print y_test

    for entry in regs:
        name = entry[0]
        reg = entry[1]

        print name
        reg.fit(X_train, y_train)
        print "Test score: ", reg.score(X_test, y_test)
        print "Train score: ", reg.score(X_train, y_train)

regs = [("Decision tree: ", tree.DecisionTreeRegressor()),
        ("Support vector regressor: ", svm.SVR())]
test(regs)