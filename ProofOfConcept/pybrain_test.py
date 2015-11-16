# luke

from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import TanhLayer, LinearLayer
from pybrain.structure import RecurrentNetwork, LinearLayer, FullConnection

import time

features = []
for i in range(0, 100):
    features.append(i)

labels = []
for i in range(0, 100):
    labels.append(i+1)

ds = SupervisedDataSet(1, 1)
for i in range(0, 100):
    ds.appendLinked( features[i], labels[i])

# for input, target in ds:
#    print input, target

# net = buildNetwork(1, 3, 1, bias=True, hiddenclass=TanhLayer)
# trainer = BackpropTrainer(net, ds)

rnn = RecurrentNetwork()
rnn.addInputModule(LinearLayer(1, 'in'));
rnn.addModule(LinearLayer(3,'hidden'));
rnn.addOutputModule(LinearLayer(1,'out'));
rnn.addConnection(FullConnection(rnn['in'],rnn['hidden'],'feed'));
rnn.addConnection(FullConnection(rnn['hidden'],rnn['out'],'give'));
rnn.addRecurrentConnection(FullConnection(rnn['hidden'],rnn['hidden'],'hide'));
rnn.sortModules();


trainer = BackpropTrainer(rnn, dataset=ds)
for i in range(1,1000):
    trainer.train()
    print i

for i in range(1, 10):
     print (i, " ", rnn.activate(i))
