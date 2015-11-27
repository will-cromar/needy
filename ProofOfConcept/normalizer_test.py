# luke

from pybrain.datasets import SupervisedDataSet, SequentialDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer, Trainer
from pybrain.structure.modules import TanhLayer, LinearLayer, MdrnnLayer, LSTMLayer, GaussianLayer, SoftmaxLayer
import matplotlib.pyplot as plt
import time
from normalizer import normalize
from price_parsing import *
from util import *

xTrain = []
yTrain = []
xTest = []
yTest = []
pred = []

data = getStockPrices("GOOG", frequency="daily")
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