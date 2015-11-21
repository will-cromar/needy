from datetime import datetime
from matplotlib import pyplot
import time

# Takes one Datasets for ground truth and an arbitrary number of regression
# plots as Datasets
def graphRegressionsOverTime(ground_truth, *regression_plots, **kwargs):
    # Initialize the plot
    pyplot.figure()

    # Unpack the data from ground_truth
    dates = map(lambda date: datetime.fromordinal(date), ground_truth.dates)
    prices = ground_truth.prices
    color = ground_truth.graphColor
    label = ground_truth.label

    # Scatter-plot the ground_truth data
    pyplot.scatter(dates, prices, c=color, label=label)

    for regression in regression_plots:
        testData, predictions, name, graphColor = regression.dumpData()
        pyplot.plot(testData, predictions, c=graphColor, label=name, linewidth=2)


    # Unpack kwargs
    title = kwargs.get("title", "Un-named graph")
    xlabel = kwargs.get("xlabel", "Dates")
    ylabel = kwargs.get("ylabel", "Prices")

    # Label and display graph
    pyplot.title(title)
    pyplot.xlabel(xlabel)
    pyplot.ylabel(ylabel)
    pyplot.legend()
    pyplot.savefig(str(time.time()) + ".png")