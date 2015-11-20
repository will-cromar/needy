# luke

from pybrain.datasets import SupervisedDataSet, SequentialDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer, Trainer
from pybrain.structure.modules import TanhLayer, LinearLayer
from pybrain.structure import RecurrentNetwork, LinearLayer, FullConnection, SigmoidLayer
import matplotlib.pyplot as plt

import time
top = 100
features = []
for i in range(0, top):
    features.append(i)

labels = []
for i in range(0, top):
    labels.append((i/2.0))


ds = SupervisedDataSet(1,1)
for i in range(0, top):
   ds.appendLinked(features[i], labels[i])


#TrainDS, TestDS = ds.splitWithProportion(0.8)

# for input, target in ds:
#    print input, target

# net = buildNetwork(1, 3, 1, bias=True, hiddenclass=TanhLayer)

# rnn = RecurrentNetwork()
rnn = buildNetwork(1, 25, 1, bias=True, recurrent=True, hiddenclass=SigmoidLayer)
# rnn.addInputModule(LinearLayer(1, 'in'));
# rnn.addModule(SigmoidLayer(25,'hidden'));
# rnn.addOutputModule(LinearLayer(1,'out'));
# rnn.addConnection(FullConnection(rnn['in'],rnn['hidden'],'feed'));
# rnn.addConnection(FullConnection(rnn['hidden'],rnn['out'],'give'));
# rnn.addRecurrentConnection(FullConnection(rnn['hidden'],rnn['hidden'],'hide'));
# rnn.sortModules();
trainer = BackpropTrainer(rnn, ds, learningrate=0.00001)

xAxisRuns = []
yAxisRuns = []
xAxisData = []
yAxisData = []

runs = 500
totalTimeStart = time.time()
for i in range(1,runs):
    print ((i/(runs*1.0)) *100)
    startEpochTime = time.time()
    rnn.reset()
    xAxisRuns.append(i)
    yAxisRuns.append(trainer.train())
    if i == 10:
        endEpochTime = time.time()
        timePerEpoch = (endEpochTime - startEpochTime)/10.0
totalTimeEnd = time.time()
totalTime = (totalTimeEnd - totalTimeStart)

for i in range(top,1,-1):
    #print (i,rnn.activate(i))
    xAxisData.append(i)
    yAxisData.append((((i/2.0) - rnn.activate(i))/(i/2.0)*100.0))

averageError = sum(yAxisData) / float(len(yAxisData))

plt.figure(1)
plt.subplot(3, 1, 1)
plt.plot(xAxisRuns, yAxisRuns, 'bo')
plt.xlabel('Epoch Number')
plt.ylabel('Error Value')

plt.subplot(3, 1, 2)
plt.plot(xAxisData, yAxisData, 'ro')
plt.xlabel('Input Number')
plt.ylabel('Percent Error')
plt.ylim(-100, 100)

plt.subplot(3,1,3)
plt.text(0.02, 0.85, 'Hello', fontsize=12)
plt.text(0.02, 0.70, 'Number of Epochs  = ' + str(runs), fontsize=12)
plt.text(0.02, 0.55, 'Number of Data Points  = ' + str(len(features)), fontsize=12)
plt.text(0.02, 0.40, 'Time per Epoch = ' + str(timePerEpoch) + 's   Total Time = ' + str(totalTime) + 's', fontsize=12)
plt.text(0.02, 0.25, 'Average Percent Error Value = ' + str(averageError), fontsize=12)
plt.text(0.02, 0.10, 'Minimum Error Value = ' + str(min(yAxisRuns)), fontsize=12)


plt.show()
