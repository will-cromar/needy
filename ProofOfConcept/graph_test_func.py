# Luke
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import TanhLayer

from normalizer import normalize
from normalizer import denormalize
from price_parsing import *
from nueral_network_functions import trainNetwork
from nueral_network_functions import graphOutput

def graphNN(ticker, date, epochs, verbose):
    """
    The function builds a data set of stock prices, normalizes that data set, builds a linked data set to
    train the neural network, generates a neural network, trains the network, makes predictions, analyzes the
    predictions against testing data to generate statistics for comparison, and uses the statistics to
    generate graphs as a png file.
    :param ticker: the stock sticker to train and predict on
    :param date: the date to split the data on to create training and testing
    :param epochs: the number of times to train the network
    :param verbose: boolean value for verbose output
    :return tomorrowPrice: the price prediction for tomorrow
    :return totalTime: the total time in seconds it took to train the network on the data set
    :return averageTimePerEpoch: the average time per training run
    :return averagePercentError:the average percent error of the predictions and the testing data
    :return minPercentError:the minimum percent error of the predictions and the testing data
    """
    # request stock prices and split by the specified date to create training and testing data sets
    if verbose: print 'Requesting data...'
    data = getStockPrices(ticker, frequency="daily", update=True)
    trainData, testData = splitByDate(data, date)
    xTrain, yTrain = preprocessStocks(trainData)
    xTest, yTest = preprocessStocks(testData)
    # allocate space for predictions and error values
    fucturePredictions = []
    trainingPredictions = []
    percentError = []
    if verbose: print 'complete.'

    if verbose: print 'Normalizing data...'
    # normalize the values to a percentage of their max values to increase network training speed
    xTrain, yTrain, xTest, yTest, priceScaleFactor, timeScaleFactor = normalize(xTrain, yTrain, xTest, yTest)
    if verbose: print 'complete.'

    if verbose: print 'Building dataset...'
    # build a linked data set to allow for training and error calculation
    ds = SupervisedDataSet(1,1)
    for i in range(0, len(xTrain)):
        ds.appendLinked(xTrain[i], yTrain[i])
    if verbose: print 'complete.'

    if verbose: print 'Buidling network...'
    rnn = buildNetwork(1, 3, 3, 3, 3, 3, 3, 3, 3, 1, bias=True, recurrent=True, hiddenclass=TanhLayer)
    if verbose: print 'complete'

    if verbose: print 'Training network...'
    trainer = BackpropTrainer(rnn, ds, learningrate=0.01)
    totalTime, averageTimePerEpoch, trainerErrorValues, epochTimes = trainNetwork(trainer, epochs, verbose)
    if verbose: print 'Training network 100.0% complete.'

    if verbose: print 'Predicting...'
    # prime the network
    for i in xTrain:
        rnn.activate(i)

    # make predictions with network on the training data to show general shape of approximated function
    for i in xTrain:
        trainingPredictions.append(rnn.activate(i))
    # make predictions with the network on the testing data to validate the accuracy of the network
    for i in xTest:
        fucturePredictions.append(rnn.activate(i))

    # predict tomorrow's price
    tomorrowPrice = rnn.activate(xTest[len(xTest) - 1] + 1) * priceScaleFactor
    if verbose: print 'complete.'

    if verbose: print 'Generating graphs...'
    # denormalize
    xTrain, yTrain, xTest, yTest, fucturePredictions, trainingPredictions = denormalize(xTrain, yTrain, xTest, yTest, fucturePredictions, trainingPredictions, priceScaleFactor, timeScaleFactor)

    # calculate percent error
    for i in range(0, len(yTest)):
        percentError.append((abs((yTest[i] - fucturePredictions[i])/yTest[i]) *100))

    # calculates statistics on the analysis of the network
    sumPercentError = sum(percentError)
    averagePercentError = sumPercentError / len(percentError)
    numDataPoints = len(xTrain) + len(xTest)
    minPercentError = min(percentError)

    # generate the graphs and save them to the working directory
    graphOutput(xTrain, yTrain, xTest, yTest, fucturePredictions, trainingPredictions, ticker)
    if verbose: print 'complete.'

    # returns
    return tomorrowPrice, numDataPoints, totalTime, averageTimePerEpoch, averagePercentError, minPercentError

