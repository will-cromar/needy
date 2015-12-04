_author_ = 'luke'
import time
import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib
from xkcd import xkcdify

def trainNetwork(trainer, runs, verbose):
    """
    Trains the network for the given number of runs and returns statistics on the training
    :param trainer: the neural network trainer to train the network on
    :param runs: the number of times to train the network
    :param verbose: boolean value to indicate verbose output
    :return totalTime: the total amount of time it took to train the network
    :return averageTimePerEpoch: the amount of time it took on average to train the netwrok once
    :return trainerErrorValues: the raw error values from the neural network trainer
    :return epochTimes: list of amount of time it took for each training run
    """
    epochTimes = []
    trainerErrorValues = []
    globalStart = time.time()
    for i in range(1,runs):
        if verbose:  print (str((i/(runs*1.0)) *100) + '% complete')
        localStart = time.time()
        trainerErrorValues.append(trainer.train())
        localEnd = time.time()
        epochTimes.append(localEnd - localStart)
    globalEnd = time.time()
    totalTime = (globalEnd - globalStart)
    averageTimePerEpoch = sum(epochTimes)/len(epochTimes)

    return totalTime, averageTimePerEpoch, trainerErrorValues, epochTimes

def graphOutput(xTrain, yTrain, xTest, yTest, futurePredictions, trainingPredictions, ticker):
    """
    Graphs the data set and the predictions, styles the graph like xkcd, and saves the graph
    to the working directory
    :param xTrain: training data set of time values
    :param yTrain: training data set of price values
    :param xTest: testing data set of time values
    :param yTest: testing data set of price values
    :param futurePredictions: data set containing the predictions for the testing data
    :param trainingPredictions: data set containing the predictions for the training data
    :param ticker: the stock that the graphs are referencing
    :return: none
    """
    plt.figure(1)

    prop = font_manager.FontProperties(fname='Humor-Sans-1.0.ttf')
    matplotlib.rcParams['font.family'] = prop.get_name()

    plt.subplot(2, 1, 1)
    plt.tight_layout()
    l1, = plt.plot(xTest, yTest, 'w-', label='line1')
    l2, = plt.plot(xTest, futurePredictions, 'w--', label='line2')
    plt.xlabel('Time (days)')
    plt.ylabel('Price (USD)')
    ax = plt.gca()
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    leg = plt.legend([l1, l2], ['Actual Values', 'Predictions'], framealpha=0, loc='center left', bbox_to_anchor=(1, 0.5), borderaxespad=0.)
    for text in leg.get_texts():
        text.set_color('#91A2C4')
    xkcdify(plt)

    plt.subplot(2, 1, 2)
    plt.tight_layout()
    plt.plot(xTrain, yTrain, 'w-')
    plt.plot(xTrain, trainingPredictions, 'w--')
    plt.xlabel('Time (days)')
    plt.ylabel('Price (USD)')
    xkcdify(plt)

    # plt.show()
    plt.savefig(ticker + 'NN.png', transparent=True, bbox_extra_artists=(leg,), bbox_inches='tight', dpi=600)
    return
