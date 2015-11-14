from copper_prices import getCopperPrices, preprocessPrices
from sklearn import tree
from sklearn import svm
from sklearn.cross_validation import train_test_split
from sklearn import linear_model
from regression_graphs import graphRegressionsOverTime

#Takes an iterable containing tuples of the form (name, model, graph color)
def runRegressions(regs, X, y):
    results = []

    X_train, X_test, y_train, y_test = \
        train_test_split(X, y, test_size=.2, random_state = 42)

    for entry in regs:
        name, reg, color = entry

        print "Running", name
        reg.fit(X_train, y_train)
        print "Test score:", reg.score(X_test, y_test)
        print "Train score:", reg.score(X_train, y_train)

        regression = {}
        regression["name"] = name
        regression["testData"] = X_test
        regression["predictions"] = reg.predict(X_test)
        regression["graphColor"] = color
        results.append(regression)

    return results


rawData = getCopperPrices()
X, y = preprocessPrices(rawData)

regs = [("Decision tree", tree.DecisionTreeRegressor(min_samples_split=100, max_depth=10), "r"),
        ("Linear regression", linear_model.LinearRegression(), "b"),
        ("SVR", svm.SVR(), "g")]

regressions = runRegressions(regs, X, y)
graphRegressionsOverTime(X, y, regressions)