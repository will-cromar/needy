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
    # Initialize the plot with XKCD themes
    pyplot.figure()
    ax = pyplot.gca()
    ax.spines['bottom'].set_color('#91A2C4')
    ax.spines['top'].set_color('#91A2C4')
    ax.spines['left'].set_color('#91A2C4')
    ax.spines['right'].set_color('#91A2C4')
    ax.tick_params(axis='both', colors='#91A2C4')
    ax.xaxis.label.set_color('#91A2C4')
    ax.yaxis.label.set_color('#91A2C4')

    # Unpack the data from ground_truth
    dates = map(lambda date: datetime.fromordinal(date), ground_truth.dates) # Convert dates from ordinal form
    prices = ground_truth.prices

    # Scatter-plot the ground_truth data
    pyplot.plot(dates, prices, "w-")

    # Plot regression models
    for regression in regression_plots:
        pyplot.plot(regression.dates, regression.prices, "w--", linewidth=2)


    # Unpack kwargs
    title = kwargs.get("title", "Un-named graph")
    xlabel = kwargs.get("xlabel", "Dates")
    ylabel = kwargs.get("ylabel", "Prices")

    # Label, title, and save the graph
    pyplot.title(title)
    pyplot.xlabel(xlabel)
    pyplot.ylabel(ylabel)
    pyplot.savefig(ticker + ".png", transparent=True)