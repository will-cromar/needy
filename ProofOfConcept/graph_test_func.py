# Luke
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import TanhLayer
import matplotlib.pyplot as plt
from normalizer import normalize
from normalizer import denormalize
from price_parsing import *
import matplotlib
import matplotlib.font_manager as font_manager
from xkcd import xkcdify
from nueral_network_functions import trainNetwork

def graphNN(ticker, date, runs):

    print 'Requesting data...'
    data = getStockPrices(ticker, frequency="daily", update=True)
    trainData, testData = splitByDate(data, date)
    xTrain, yTrain = preprocessStocks(trainData)
    xTest, yTest = preprocessStocks(testData)
    fucturePredictions = []
    trainingPredictions = []
    percentError = []
    print 'complete.'

    print 'Normalizing data...'
    xTrain, yTrain, xTest, yTest, priceScaleFactor, timeScaleFactor = normalize(xTrain, yTrain, xTest, yTest)
    print 'compelte.'

    print 'Building dataset...'
    ds = SupervisedDataSet(1,1)
    for i in range(0, len(xTrain)):
        ds.appendLinked(xTrain[i], yTrain[i])
    print 'complete.'

    print 'Buidling netowrk...'
    rnn = buildNetwork(1, 3, 3, 3, 3, 3, 3, 3, 3, 1, bias=True, recurrent=True, hiddenclass=TanhLayer)
    print 'complete'

    print 'Training network...'
    trainer = BackpropTrainer(rnn, ds, learningrate=0.01)
    totalTime, averageTimePerEpoch, trainerErrorValues, epochTimes = trainNetwork(trainer, runs)
    print 'Training network 100.0% complete.'

    print 'Predicting...'
    # prime the network
    for i in xTrain:
        rnn.activate(i)

    # make predictions with network
    for i in xTrain:
        trainingPredictions.append(rnn.activate(i))

    for i in xTest:
        fucturePredictions.append(rnn.activate(i))

    # predict tomorrow's price
    tomorrowPrice = rnn.activate(xTest[len(xTest) - 1] + 1) * priceScaleFactor
    print 'Predictions complete.'

    print 'Generating graphs...'
    # denormalize
    xTrain, yTrain, xTest, yTest, fucturePredictions, trainingPredictions = denormalize(xTrain, yTrain, xTest, yTest, fucturePredictions, trainingPredictions, priceScaleFactor, timeScaleFactor)

    # calculate percent error
    for i in range(0, len(yTest)):
        percentError.append((abs((yTest[i] - fucturePredictions[i])/yTest[i]) *100))

    sumPercentError = sum(percentError)
    averageError = sumPercentError / len(percentError)

    plt.figure(1)

    prop = font_manager.FontProperties(fname='Humor-Sans-1.0.ttf')
    matplotlib.rcParams['font.family'] = prop.get_name()

    plt.subplot(2, 1, 1)
    plt.tight_layout()
    l1, = plt.plot(xTest, yTest, 'w-', label='line1')
    l2, = plt.plot(xTest, fucturePredictions, 'w--', label='line2')
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

    numEpochs = runs
    numDataPoints = len(xTrain) + len(xTest)
    # timePerEpoch
    # totalTime
    # averageError
    minPercentError = min(percentError)

    # plt.show()
    plt.savefig(ticker + 'NN.png', transparent=True, bbox_extra_artists=(leg,), bbox_inches='tight', dpi=600)
    print 'graphs complete.'

    return tomorrowPrice, numEpochs, numDataPoints, totalTime, averageError, minPercentError

