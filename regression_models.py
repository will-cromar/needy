from sklearn.cross_validation import train_test_split
from sklearn import linear_model

class Dataset:
    """
    Represent a dataset graphable by regression_graphs module
    """
    def __init__(self, dates, prices, label, graphColor="k", mode="sklearn"):
        # Extract data from sklearn format
        if mode == "sklearn":
            self.dates = [date[0] for date in dates] # Exctract date from one-element list
            self.prices = prices
        # Assume everything is in correct format
        elif mode == "preformatted":
            self.dates = dates
            self.prices = prices

        # Set graph kwargs
        self.label = label
        self.graphColor = graphColor

    def dumpData(self):
        """
        Dumps all data from the class in the following order for convenience
        :return: tuple of (ordinal dates, float prices, label to go in legend, color of the
         graphed points)
        """
        return self.dates, self.prices, self.label, self.graphColor

    def getXY(self, mode="sklearn"):
        """
        Extract data from the specified format. Currently only supports sklearn format.
        :param mode: string representing format mode
        :return: tuple representing (X, y)
        """
        # Wrap each date in a list
        if mode == "sklearn":
            return [[date] for date in self.dates], self.prices

def runRegressions(regs, X, y):
    """
    Use the regressors in regs to create regressions across dataset
    :param regs: list of tuples in form (label, model, color argument)
    :param X: ordinal dates
    :param y: float prices
    :return: list of Datasets for each regressor
    """
    results = []

    #Create training and testing sets
    X_train, X_test, y_train, y_test = \
        train_test_split(X, y, test_size=.33, random_state = 42)

    for entry in regs:
        # Extract data from tuple
        name, reg, color = entry

        # Fit and score each regressor
        print "Running", name
        reg.fit(X_train, y_train)
        print "Test score:", reg.score(X_test, y_test)
        print "Train score:", reg.score(X_train, y_train)

        # Feed data into regessor to draw the line
        y_pred = reg.predict(X)

        #Create dataset and add to results
        regression = Dataset(X, y_pred, name, graphColor=color)
        results.append(regression)

    return results

def extendGraphByN(X, n):
    """
    Extend the domain of X by n
    :param X: The current domain in sklearn format
    :param n: The number of units (usually ordinal dates) to extend the domain by
    :return: Extended domain
    """
    end = X[-1][0] + 1 # Starting point of extension
    extension = map(lambda i: [i], range(end + 1, end + n))
    return X + extension

def graphRecentTrend(X, y, samples):
    """
    Creates a linear regression across recent datapoints
    :param X: The domain to feed into regression model (sklearn format)
    :param y: The range to fit the regression model to (floats)
    :param samples: The number of days to use in the regression
    :return: Dataset representing the regression model
    """

    # Get sample recent points
    X = X[-samples:]
    y = y[-samples:]

    # Create regressor and fit data
    reg = linear_model.LinearRegression()
    reg.fit(X, y)

    # Extend domain and predict values across it
    domain = extendGraphByN(X, samples)
    pred = reg.predict(domain)

    return Dataset(domain, pred, "Recent trend")