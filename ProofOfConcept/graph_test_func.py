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
from nueral_network_functions import graphOutput

def graphNN(ticker, date, runs, verbose):

    if verbose: print 'Requesting data...'
    data = getStockPrices(ticker, frequency="daily", update=True)
    trainData, testData = splitByDate(data, date)
    xTrain, yTrain = preprocessStocks(trainData)
    xTest, yTest = preprocessStocks(testData)
    fucturePredictions = []
    trainingPredictions = []
    percentError = []
    if verbose: print 'complete.'

    if verbose: print 'Normalizing data...'
    xTrain, yTrain, xTest, yTest, priceScaleFactor, timeScaleFactor = normalize(xTrain, yTrain, xTest, yTest)
    if verbose: print 'compelte.'

    if verbose: print 'Building dataset...'
    ds = SupervisedDataSet(1,1)
    for i in range(0, len(xTrain)):
        ds.appendLinked(xTrain[i], yTrain[i])
    if verbose: print 'complete.'

    if verbose: print 'Buidling netowrk...'
    rnn = buildNetwork(1, 3, 3, 3, 3, 3, 3, 3, 3, 1, bias=True, recurrent=True, hiddenclass=TanhLayer)
    if verbose: print 'complete'

    if verbose: print 'Training network...'
    trainer = BackpropTrainer(rnn, ds, learningrate=0.01)
    totalTime, averageTimePerEpoch, trainerErrorValues, epochTimes = trainNetwork(trainer, runs, verbose)
    if verbose: print 'Training network 100.0% complete.'

    if verbose: print 'Predicting...'
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
    if verbose: print 'Predictions complete.'

    if verbose: print 'Generating graphs...'
    # denormalize
    xTrain, yTrain, xTest, yTest, fucturePredictions, trainingPredictions = denormalize(xTrain, yTrain, xTest, yTest, fucturePredictions, trainingPredictions, priceScaleFactor, timeScaleFactor)

    # calculate percent error
    for i in range(0, len(yTest)):
        percentError.append((abs((yTest[i] - fucturePredictions[i])/yTest[i]) *100))

    sumPercentError = sum(percentError)
    averageError = sumPercentError / len(percentError)
    numEpochs = runs
    numDataPoints = len(xTrain) + len(xTest)
    minPercentError = min(percentError)

    graphOutput(xTrain, yTrain, xTest, yTest, fucturePredictions, trainingPredictions, ticker)
    if verbose: print 'graphs complete.'

    return tomorrowPrice, numEpochs, numDataPoints, totalTime, averageError, minPercentError

