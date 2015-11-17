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
trainer = BackpropTrainer(rnn, ds, learningrate=0.00005)

xAxisRuns = []
yAxisRuns = []
xAxisData = []
yAxisData = []

runs = 100
for i in range(1,runs):
    print ((i/(runs*1.0)) *100)
    #print trainer.train()
    rnn.reset()
    xAxisRuns.append(i)
    yAxisRuns.append(trainer.train())

for i in range(top,1,-1):
    #print (i,rnn.activate(i))
    xAxisData.append(i)
    yAxisData.append((((i/2.0) - rnn.activate(i))/(i/2.0)*100.0))


plt.figure(1)
plt.subplot(2, 1, 1)
plt.plot(xAxisRuns, yAxisRuns, 'bo')
plt.xlabel('Epoch Number')
plt.ylabel('Error Value')

plt.subplot(2, 1, 2)
plt.plot(xAxisData, yAxisData, 'ro')
plt.xlabel('Input Number')
plt.ylabel('Percent Error')
plt.ylim(-100, 100)

plt.show()
