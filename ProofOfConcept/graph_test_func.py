# Luke
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import TanhLayer
import matplotlib.pyplot as plt
from normalizer import normalize
from normalizer import denormalize
from price_parsing import *
from util import *
import matplotlib
import matplotlib.font_manager as font_manager

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
    # prime the network
    for i in xTrain:
        rnn.activate(i)

    # make predictions with network
    pred2 = []
    for i in xTrain:
        pred2.append(rnn.activate(i))

    for i in xTest:
        pred.append(rnn.activate(i))

    # predict tomorrow's price
    tPrice = rnn.activate(max(xTest) + 1) * priceScaleFactor

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

    prop = font_manager.FontProperties(fname='Humor-Sans-1.0.ttf')
    matplotlib.rcParams['font.family'] = prop.get_name()

    plt.subplot(2, 1, 1)
    plt.tight_layout()
    l1, = plt.plot(xTest, yTest, 'w-', label='line1')
    l2, = plt.plot(xTest, pred, 'w--', label='line2')
    plt.xlabel('Time (days)')
    plt.ylabel('Price (USD)')
    ax = plt.gca()
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    leg = plt.legend([l1, l2], ['Actual Values', 'Predictions'], framealpha=0, loc='center left', bbox_to_anchor=(1, 0.5), borderaxespad=0.)
    for text in leg.get_texts():
        text.set_color('#91A2C4')

    ax.spines['bottom'].set_color('#91A2C4')
    ax.spines['top'].set_color('#91A2C4')
    ax.spines['left'].set_color('#91A2C4')
    ax.spines['right'].set_color('#91A2C4')
    ax.tick_params(axis='both', colors='#91A2C4')
    ax.xaxis.label.set_color('#91A2C4')
    ax.yaxis.label.set_color('#91A2C4')


    plt.subplot(2, 1, 2)
    plt.tight_layout()
    plt.plot(xTrain, yTrain, 'w-')
    plt.plot(xTrain, pred2, 'w--')
    plt.xlabel('Time (days)')
    plt.ylabel('Price (USD)')
    ax = plt.gca()
    ax.spines['bottom'].set_color('#91A2C4')
    ax.spines['top'].set_color('#91A2C4')
    ax.spines['left'].set_color('#91A2C4')
    ax.spines['right'].set_color('#91A2C4')
    ax.tick_params(axis='both', colors='#91A2C4')
    ax.xaxis.label.set_color('#91A2C4')
    ax.yaxis.label.set_color('#91A2C4')



    # plt.subplot(3, 1, 3)
    # plt.tight_layout()
    # # plt.text(0.02, 0.85, 'Hello', fontsize=12)
    # plt.text(0.02, 0.70, 'Number of Epochs  = ' + str(runs), fontsize=12, color='#91A2C4')
    # plt.text(0.02, 0.55, 'Number of Data Points  = ' + str(len(xTrain)), fontsize=12, color='#91A2C4')
    # plt.text(0.02, 0.40, 'Time per Epoch = ' + str(timePerEpoch) + 's   Total Time = ' + str(totalTime) + 's', fontsize=12, color='#91A2C4')
    # plt.text(0.02, 0.25, 'Average Percent Error Value = ' + str(averageError), fontsize=12, color='#91A2C4')
    # plt.text(0.02, 0.10, 'Minimum Percent Error Value = ' + str(min(percentError)), fontsize=12, color='#91A2C4')
    # ax = plt.gca()
    # ax.spines['bottom'].set_color('#91A2C4')
    # ax.spines['top'].set_color('#91A2C4')
    # ax.spines['left'].set_color('#91A2C4')
    # ax.spines['right'].set_color('#91A2C4')
    # ax.tick_params(axis='both', colors='#91A2C4')
    # ax.xaxis.label.set_color('#91A2C4')
    # ax.yaxis.label.set_color('#91A2C4')


    #plt.show()
    plt.savefig(ticker + 'NN.png', transparent=True, bbox_extra_artists=(leg,), bbox_inches='tight', dpi=600)
    print 'graphs complete.'

    return tPrice

