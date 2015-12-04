_author_ = 'Luke'

from price_parsing import *

def normalize(xTrain, yTrain, xTest, yTest):
    # time factor to normalize time data to
    firstTime = xTrain[0]


    for i in range(0, len(xTrain)):
        xTrain[i] = xTrain[i] - firstTime

    for i in range(0, len(xTest)):
        xTest[i] = xTest[i] - firstTime

    lastTime = xTest[len(xTest) - 1]
    lastTime = (lastTime * 1.20)

    for i in range(0, len(xTrain)):
        xTrain[i] = (xTrain[i]/lastTime)

    for i in range(0, len(xTest)):
        xTest[i] = (xTest[i]/lastTime)


    # price factor to normalize to upped to 120% so as to allow for prediciton of a price higher than previously seen
    maxPrice = max(yTrain)
    maxPrice = (maxPrice * 1.20)

    # convert all price to a percentage of the max possible price
    for i in range(0, len(yTrain)):
        yTrain[i] = (yTrain[i]/maxPrice)

    for i in range(0, len(yTest)):
        yTest[i] = (yTest[i]/maxPrice)

    return xTrain, yTrain, xTest, yTest, maxPrice, lastTime

def denormalize(xTrain, yTrain, xTest, yTest, pred, pred2, priceScaleFactor, timeScaleFactor):

    for i in range(0, len(xTrain)):
        xTrain[i] = (xTrain[i]*timeScaleFactor)

    for i in range(0, len(xTest)):
        xTest[i] = (xTest[i]*timeScaleFactor)

    # convert all price to a percentage of the max possible price
    for i in range(0, len(yTrain)):
        yTrain[i] = (yTrain[i]*priceScaleFactor)

    for i in range(0, len(yTest)):
        yTest[i] = (yTest[i]*priceScaleFactor)

    for i in range(0, len(pred)):
        pred[i] = (pred[i]*priceScaleFactor)

    for i in range(0, len(pred2)):
        pred2[i] = (pred2[i]*priceScaleFactor)

    return xTrain, yTrain, xTest, yTest, pred, pred2
