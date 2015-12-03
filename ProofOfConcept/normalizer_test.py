# luke

from normalizer import normalize
from price_parsing import *

xTrain = []
yTrain = []
xTest = []
yTest = []
pred = []

data = getStockPrices("GOOG", frequency="daily")
trainData, testData = splitByDate(data, '9/21/2015')
xTrain, yTrain = preprocessStocks(trainData)
xTest, yTest = preprocessStocks(testData)

xTrain, yTrain, xTest, yTest, priceScaleFactor, timeScaleFactor = normalize(xTrain, yTrain, xTest, yTest)

print xTrain
print yTrain
print xTest
print yTest
print priceScaleFactor
print timeScaleFactor
