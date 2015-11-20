from sklearn.cross_validation import train_test_split

class Dataset:
    def __init__(self, dates, prices, label, graphColor="k", mode="sklearn"):
        if mode == "sklearn":
            self.dates = [date[0] for date in dates]
            self.prices = prices
        elif mode == "preformatted":
            self.dates = dates
            self.prices = prices

        self.label = label
        self.graphColor = graphColor

    def dumpData(self):
        return self.dates, self.prices, self.label, self.graphColor


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

        pred = reg.predict(X)

        regression = Dataset(X, pred, name, graphColor=color)
        results.append(regression)

    return results