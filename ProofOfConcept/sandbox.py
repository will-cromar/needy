from price_parsing import *
from regression_models import *
from regression_graphs import *
from util import *

from sklearn import tree, svm

#Will's example code

#Testing code. Run this once to make sure it works
def doesItWork():
    obj1 = "Less recent"
    obj2 = "More recent"

    savePickle(obj1, "stringtest")
    time.sleep(20)
    savePickle(obj2, "stringtest")

    print getMostRecentPickle("stringtest")

def test():
    data = getStockPrices("GOOG", frequency="daily")
    times, prices = preprocessStocks(data)
    dataset = Dataset(times, prices, "The GOOG", graphColor="k", mode="sklearn")

    min_samples = len(times) * .025

    regs = [("Decision tree", tree.DecisionTreeRegressor(min_samples_leaf=min_samples), "r")]
            #("Ouija board", svm.SVR(kernel="poly"), "g")]

    regressions = runRegressions(regs, times, prices)
    graphRegressionsOverTime(dataset, *regressions)

def test2():
    data = getStockPrices("GOOG", frequency="daily")
    times, prices = preprocessStocks(data)
    dataset = Dataset(times, prices, "The GOOG", graphColor="k", mode="sklearn")

    graphRegressionsOverTime(dataset)

def recentTrendTest():
    samples = 50
    lookback = 4 * samples

    data = getStockPrices("GOOG", frequency="daily")
    dates, prices = preprocessStocks(data[-lookback:])
    dataset = Dataset(dates, prices, mode="preformatted")
    recentTrend = graphRecentTrend(dataset, samples)

    graphRegressionsOverTime("GOOG", dataset, recentTrend, title="Test of recent trends")

getStockPrices("GOOGL", update=True, frequency="daily")
getStockPrices("AAPL", update=True, frequency="daily")
recentTrendTest()