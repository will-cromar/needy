# luke

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

xTrain = []
yTrain = []
xTest = []
yTest = []
pred = []

data = getStockPrices("AXP", frequency="daily")
trainData, testData = splitByDate(data, '9/21/2015')
xTrain, yTrain = preprocessStocks(trainData)
xTest, yTest = preprocessStocks(testData)

# xTrain, yTrain = preprocessStocks(data)
# xTest = xTrain
# yTest = yTrain

xTrain, yTrain, xTest, yTest, priceScaleFactor, timeScaleFactor = normalize(xTrain, yTrain, xTest, yTest)
print xTrain
print yTrain
print xTest
print yTest
print priceScaleFactor
print timeScaleFactor

# build data set from x training data and y training data
ds = SupervisedDataSet(1,1)
for i in range(0, len(xTrain)):
   ds.appendLinked(xTrain[i], yTrain[i])

# number of runs
runs = 100

# # top of range of numbers to generate
# top = 100
#
# # generate x training data
# for i in range(0, top):
#     xTrain.append(i)
#
# # generate y training data
# for i in range(0, top):
#     yTrain.append((i/2.0))
#
# # generate x testing data
# for i in range(0, top, 0.5):
#     xTest.append(i)
#
# # generate y testing data
# for i in range(0, top, 0.5):
#     yTest.append(i/2.0)


rnn = buildNetwork(1, 10, 10, 10, 10, 10, 1, bias=True, recurrent=True, hiddenclass=TanhLayer)
trainer = BackpropTrainer(rnn, ds, learningrate=0.05)

EpochNumber = []
epochTimes = []
ErrorValues = []
percentError = []

totalTimeStart = time.time()
for i in range(1,runs):
    print ((i/(runs*1.0)) *100)
    startEpochTime = time.time()
    EpochNumber.append(i)
    ErrorValues.append(trainer.train())
    endEpochTime = time.time()
    epochTimes.append(endEpochTime - startEpochTime)

totalTimeEnd = time.time()
totalTime = (totalTimeEnd - totalTimeStart)

timePerEpoch = sum(epochTimes)/len(epochTimes)

# make predictions with network
for i in xTest:
    pred.append(rnn.activate(i))

pred2 = []
for i in xTrain:
    pred2.append(rnn.activate(i))

# denormalize
# xTrain, yTrain, xTest, yTest = denormalize(xTrain, yTrain, xTest, yTest, priceScaleFactor, timeScaleFactor)

# calculate percent error
for i in range(0, len(yTest)):
    percentError.append(abs((yTest[i] - pred[i])/yTest[i]))

sumPercentError = sum(percentError)
averageError = sumPercentError / len(percentError)

plt.figure(1)
plt.subplot(4, 1,1)
plt.plot(EpochNumber, ErrorValues, 'bo')
plt.xlabel('Epoch Number')
plt.ylabel('Error Value')

plt.subplot(4, 1, 2)
plt.plot(xTest, yTest, 'ro')
plt.plot(xTest, pred, 'go')
plt.xlabel('xTest')
plt.ylabel('yTest')

plt.subplot(4, 1, 3)
plt.plot(xTrain, yTrain, 'ro')
plt.plot(xTrain, pred2, 'go')
plt.xlabel('xTrain')
plt.ylabel('yTrain')

plt.subplot(4, 1, 4)
plt.text(0.02, 0.85, 'Hello', fontsize=12)
plt.text(0.02, 0.70, 'Number of Epochs  = ' + str(runs), fontsize=12)
plt.text(0.02, 0.55, 'Number of Data Points  = ' + str(len(xTrain)), fontsize=12)
plt.text(0.02, 0.40, 'Time per Epoch = ' + str(timePerEpoch) + 's   Total Time = ' + str(totalTime) + 's', fontsize=12)
plt.text(0.02, 0.25, 'Average Absolute Percent Error Value = ' + str(averageError), fontsize=12)
plt.text(0.02, 0.10, 'Minimum Error Value = ' + str(min(percentError)), fontsize=12)


plt.show()
