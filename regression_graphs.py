from datetime import datetime
from matplotlib import pyplot

# Takes one Datasets for ground truth and an arbitrary number of regression
# plots as Datasets
def graphRegressionsOverTime(ground_truth, title="Un-named graph", xlabel="Time", ylabel="Price", *regression_plots):
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
        name, testData, predictions, graphColor = regression.dumpData()
        pyplot.plot(testData, predictions, c=graphColor, label=name, linewidth=2)

    pyplot.title(title)
    pyplot.xlabel(xlabel)
    pyplot.ylabel(ylabel)
    pyplot.legend()
    pyplot.show()