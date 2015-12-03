_author_ = 'luke'

import time

def trainNetwork(trainer, runs):

    epochTimes = []
    trainerErrorValues = []
    globalStart = time.time()
    for i in range(1,runs):
        print (str((i/(runs*1.0)) *100) + '% complete')
        localStart = time.time()
        trainerErrorValues.append(trainer.train())
        localEnd = time.time()
        epochTimes.append(localEnd - localStart)
    globalEnd = time.time()
    totalTime = (globalEnd - globalStart)
    averageTimePerEpoch = sum(epochTimes)/len(epochTimes)

    return totalTime, averageTimePerEpoch, trainerErrorValues, epochTimes
