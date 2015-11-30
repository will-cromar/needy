# Luke
from pybrain.datasets import SupervisedDataSet, SequentialDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer, Trainer
from pybrain.structure.modules import TanhLayer, LinearLayer, MdrnnLayer, LSTMLayer, GaussianLayer, SoftmaxLayer
import matplotlib.pyplot as plt
import time
from normalizer import normalize
from normalizer import denormalize
from price_parsing import *
from util import *


# ticker = "GOOG"
# date = '11/24/15'

def graphNN(ticker, date, runs):

    print 'building dataset...'
    xTrain = []
    yTrain = []
    xTest = []
    yTest = []
    pred = []

    data = getStockPrices(ticker, frequency="daily", update=True)
    trainData, testData = splitByDate(data, date)
    xTrain, yTrain = preprocessStocks(trainData)
    xTest, yTest = preprocessStocks(testData)

    del xTrain[len(xTrain) - 1]
    del yTrain[len(yTrain) - 1]

    xTrain, yTrain, xTest, yTest, priceScaleFactor, timeScaleFactor = normalize(xTrain, yTrain, xTest, yTest)


    # build data set from x training data and y training data
    ds = SupervisedDataSet(1,1)
    for i in range(0, len(xTrain)):
       ds.appendLinked(xTrain[i], yTrain[i])

    # number of runs
    #runs = 5
    print 'complete.'
    print 'buidling netowrk...'
    rnn = buildNetwork(1, 3, 3, 3, 3, 3, 3, 3, 3, 1, bias=True, recurrent=True, hiddenclass=TanhLayer)
    trainer = BackpropTrainer(rnn, ds, learningrate=0.01)

    print 'complete'
    EpochNumber = []
    epochTimes = []
    ErrorValues = []
    percentError = []

    print 'training network...'
    totalTimeStart = time.time()
    for i in range(1,runs):
        print (str((i/(runs*1.0)) *100) + '% complete')
        startEpochTime = time.time()
        EpochNumber.append(i)
        ErrorValues.append(trainer.train())
        endEpochTime = time.time()
        epochTimes.append(endEpochTime - startEpochTime)

    totalTimeEnd = time.time()
    totalTime = (totalTimeEnd - totalTimeStart)

    timePerEpoch = sum(epochTimes)/len(epochTimes)

    print 'training network 100.0% complete.'
    print 'predicting...'
    # make predictions with network
    pred2 = []
    for i in xTrain:
        pred2.append(rnn.activate(i))

    for i in xTest:
        pred.append(rnn.activate(i))



    print 'predictions complete.'
    print 'generating graphs...'
    # denormalize
    xTrain, yTrain, xTest, yTest, pred, pred2 = denormalize(xTrain, yTrain, xTest, yTest, pred, pred2, priceScaleFactor, timeScaleFactor)

    # calculate percent error
    for i in range(0, len(yTest)):
        percentError.append((abs((yTest[i] - pred[i])/yTest[i]) *100))

    sumPercentError = sum(percentError)
    averageError = sumPercentError / len(percentError)

    plt.figure(1)
    #plt.xkcd()
    # plt.subplot(4, 1,1)
    # plt.plot(EpochNumber, ErrorValues, 'bo')
    # plt.xlabel('Epoch Number')
    # plt.ylabel('Error Value')

    plt.subplot(3, 1, 1)
    plt.plot(xTest, yTest, 'ro')
    plt.plot(xTest, pred, 'go')
    plt.xlabel('xTest')
    plt.ylabel('yTest')

    plt.subplot(3, 1, 2)
    plt.plot(xTrain, yTrain, 'ro')
    plt.plot(xTrain, pred2, 'go')
    plt.xlabel('xTrain')
    plt.ylabel('yTrain')

    plt.subplot(3, 1, 3)
    # plt.text(0.02, 0.85, 'Hello', fontsize=12)
    plt.text(0.02, 0.70, 'Number of Epochs  = ' + str(runs), fontsize=12)
    plt.text(0.02, 0.55, 'Number of Data Points  = ' + str(len(xTrain)), fontsize=12)
    plt.text(0.02, 0.40, 'Time per Epoch = ' + str(timePerEpoch) + 's   Total Time = ' + str(totalTime) + 's', fontsize=12)
    plt.text(0.02, 0.25, 'Average Percent Error Value = ' + str(averageError), fontsize=12)
    plt.text(0.02, 0.10, 'Minimum Percent Error Value = ' + str(min(percentError)), fontsize=12)

    #plt.show()
    plt.savefig(ticker+'.png')
    print 'graphs complete.'

    return

