import util

import Quandl
import sklearn
from sklearn import tree
from sklearn import svm
from sklearn.cross_validation import train_test_split
from sklearn import ensemble
from matplotlib import pyplot

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
    X = [[i[0].year, i[0].month] for i in prices]
    y = [float(i[1]) for i in prices]

    return X, y

#Tests out different regressors in regs
#not finished
def test(regs, X_train, X_test, y_train, y_test):
    for entry in regs:
        name = entry[0]
        reg = entry[1]

        print name
        reg.fit(X_train, y_train)
        print "Test score: ", reg.score(X_test, y_test)
        print "Train score: ", reg.score(X_train, y_train)

        print "Price on ", prices[-1][0], " was ", prices[-1][1]
        print "Predicted ", reg.predict([2015, 10])

        print "Plotting..."



prices = getCopperPrices()
X, y = preprocessPrices(prices) #Stop at end of 2014
X_train, X_test, y_train, y_test = \
    train_test_split(X, y, test_size=.2, random_state = 42)

#Initialize plot and scatter
pyplot.figure()
dates = [i[0] for i in prices]
print len(dates), len(y)
pyplot.scatter(dates, y, c="k", label = "data")
pyplot.show()

regs = [("Decision tree: ", tree.DecisionTreeRegressor()),
        ("Support vector regressor: ", svm.SVR())]
test(regs, X_train, X_test, y_train, y_test)