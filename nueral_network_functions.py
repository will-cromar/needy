_author_ = 'luke'

import time

def trainNetwork(trainer, runs, verbose):

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

import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib
from xkcd import xkcdify

def graphOutput(xTrain, yTrain, xTest, yTest, futurePredictions, trainingPredictions, ticker):
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
