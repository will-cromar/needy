from datetime import datetime
from matplotlib import pyplot

def graphRegressionsOverTime(dates, prices, regressions):
    # Initialize the plot
    pyplot.figure()

    # Unpack dates and convert them to ordinals
    ordinalDates = [datetime.fromordinal(date[0]) for date in dates]
    pyplot.scatter(ordinalDates, prices, c="k", label = "data")

    for regression in regressions:
        name = regression.get("name")
        testData = regression.get("testData")
        predictions = regression.get("predictions")
        graphColor = regression.get("graphColor")
        pyplot.plot(testData, predictions, c=graphColor, label=name, linewidth=2)

    pyplot.title("Regression via ouija board")
    pyplot.xlabel("Time")
    pyplot.ylabel("Price")
    pyplot.legend()
    pyplot.show()