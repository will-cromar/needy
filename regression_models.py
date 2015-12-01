from sklearn.cross_validation import train_test_split
from sklearn import linear_model

class Dataset:
    """
    Represent a dataset graphable by regression_graphs module
    """
    def __init__(self, dates, prices, mode="preformatted"):
        # Extract data from sklearn format
        if mode == "sklearn":
            self.dates = [date[0] for date in dates] # Exctract date from one-element list
            self.prices = prices
        # Assume everything is in correct format
        elif mode == "preformatted":
            self.dates = dates
            self.prices = prices

    def getXY(self, mode="sklearn"):
        """
        Extract data from the specified format. Currently only supports sklearn format.
        :param mode: string representing format mode
        :return: tuple representing (X, y)
        """
        # Wrap each date in a list
        if mode == "sklearn":
            return [[date] for date in self.dates], self.prices

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

def graphRecentTrend(dataset, samples):
    """
    Creates a linear regression across recent datapoints
    :param X: The domain to feed into regression model (sklearn format)
    :param y: The range to fit the regression model to (floats)
    :param samples: The number of days to use in the regression
    :return: Dataset representing the regression model
    """

    # Get sample recent points
    X, y = dataset.getXY()
    X = X[-samples:]
    y = y[-samples:]

    # Create regressor and fit data
    reg = linear_model.LinearRegression()
    reg.fit(X, y)

    # Extend domain and predict values across it
    domain = extendGraphByN(X, samples)
    pred = reg.predict(domain)

    return Dataset(domain, pred)