from sklearn import linear_model
from matplotlib import pyplot

from price_parsing import *
from ProofOfConcept.xkcd import xkcdify

from datetime import datetime

DEFAULT_SAMPLES = 50
DEFUALT_LOOKBACK = 200

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

def predictRecentTrend(X, y, samples):
    """
    Creates a linear regression across recent datapoints
    :param X: The domain to feed into regression model (sklearn format)
    :param y: The range to fit the regression model to (floats)
    :param samples: The number of days to use in the regression
    :return: Dataset representing the regression model
    """

    # Get sample recent points
    X = [[date] for date in X[-samples:]]
    y = y[-samples:]

    # Create regressor and fit data
    reg = linear_model.LinearRegression()
    reg.fit(X, y)

    # Extend domain and predict values across it
    domain = extendGraphByN(X, samples)
    pred = reg.predict(domain)

    return domain, pred

def graphRegression(ground_truth, regression):
    """
    Saves a png of the graph of the Dataset arguments representing a ground truth and regression models
    :param ticker: Name of company's ticker. Uses as the save ont
    :param ground_truth: (X,y) tuple representing the actual values
    :param regression_plots: (X,y) tuple representing a prediction
    :param kwargs: Keyword arguments to use with matplotlib
    :return: None
    """
    # Initialize the plot with XKCD themes
    pyplot.figure()
    xkcdify(pyplot)

    # Unpack the data from ground_truth
    dates = map(lambda date: datetime.fromordinal(date), ground_truth[0]) # Convert dates from ordinal form
    prices = ground_truth[1]

    # Scatter-plot the ground_truth data
    pyplot.plot(dates, prices, "w-")

    # Plot regression model
    X = [date[0] for date in regression[0]]
    y = regression[1]
    pyplot.plot(X, y, "w--", linewidth=2) # Line is thicker than ground-truth

    # Label, title, and save the graph
    pyplot.xlabel("Dates")
    pyplot.ylabel("Prices")

def graphRecentTrend(ticker, samples=DEFAULT_SAMPLES, lookback=DEFUALT_LOOKBACK):
    """
    Create a graph of a stocks recent trend.
    :param ticker: Company's ticker name
    :param samples: Number of samples to consider when graphing
    :param lookback: Number of previous points to include in graph
    :return: None
    """
    # Grab the stock prices
    data = getStockPrices(ticker, frequency="daily")
    dates, prices = preprocessStocks(data[-lookback:])

    # Pack the ground truth and the predicted values
    recentTrend = predictRecentTrend(dates, prices, samples)
    groundTruth = (dates, prices)

    # Graph the trend and save it
    graphRegression(groundTruth, recentTrend)
    pyplot.savefig(ticker + "linear.png", transparent=True)