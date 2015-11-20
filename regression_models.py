from price_parsing import getCopperPrices, preprocessCopperPrices
from sklearn import tree
from sklearn import svm
from sklearn.cross_validation import train_test_split
from sklearn import linear_model
from regression_graphs import graphRegressionsOverTime


# Takes an iterable containing tuples of the form (name, model, graph color)
def runRegressions(regs, X, y):
    results = []

    #X_train = X[:-20]
    #y_train = y[:-20]

    X_train, X_test, y_train, y_test = \
        train_test_split(X, y, test_size=.33, random_state = 42)

    for entry in regs:
        name, reg, color = entry

        print "Running", name
        reg.fit(X_train, y_train)
        print "Test score:", reg.score(X_test, y_test)
        print "Train score:", reg.score(X_train, y_train)

        regression = {}
        regression["name"] = name
        regression["testData"] = X
        regression["predictions"] = reg.predict(X)
        regression["graphColor"] = color
        results.append(regression)

    return results

def test():
    rawData = getCopperPrices()
    X, y = preprocessCopperPrices(rawData)
    min_samples = .025 * len(X)

    regs = [("Decision tree", tree.DecisionTreeRegressor(min_samples_leaf=min_samples), "r"),
            ("Linear regression", linear_model.LinearRegression(), "b")
            ]
    #        ("SVR", svm.SVR(), "g")]

    regressions = runRegressions(regs, X, y)
    graphRegressionsOverTime(X, y, regressions)