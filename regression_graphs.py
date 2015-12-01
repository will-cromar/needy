from datetime import datetime
from matplotlib import pyplot

import time

def graphRegressionsOverTime(ticker, ground_truth, *regression_plots, **kwargs):
    """
    Saves a png of the graph of the Dataset arguments representing a ground truth and regression models
    :param ticker: Name of company's ticker. Uses as the save ont
    :param ground_truth: Dataset representing the actual values
    :param regression_plots: Dataset representing an arbitrary number of regression plots
    :param kwargs: Keyword arguments to use with matplotlib
    :return: None
    """
    # Initialize the plot as XKCD
    pyplot.figure()
    pyplot.xkcd()

    # Unpack the data from ground_truth
    dates = map(lambda date: datetime.fromordinal(date), ground_truth.dates) # Convert dates from ordinal form
    prices = ground_truth.prices
    color = ground_truth.graphColor
    label = ground_truth.label

    # Scatter-plot the ground_truth data
    pyplot.scatter(dates, prices, c=color, label=label)

    # Plot regression models
    for regression in regression_plots:
        testData, predictions, name, graphColor = regression.dumpData()
        pyplot.plot(testData, predictions, c=graphColor, label=name, linewidth=2)


    # Unpack kwargs
    title = kwargs.get("title", "Un-named graph")
    xlabel = kwargs.get("xlabel", "Dates")
    ylabel = kwargs.get("ylabel", "Prices")

    # Label, title, and save the graph
    pyplot.title(title)
    pyplot.xlabel(xlabel)
    pyplot.ylabel(ylabel)
    pyplot.savefig(ticker + ".png")