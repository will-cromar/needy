# luke

from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import TanhLayer, LinearLayer

import time

features = []
for i in range(0, 50):
    features.append(i)

labels = []
for i in range(0, 50):
    labels.append(2*i)

ds = SupervisedDataSet(1, 1)
for i in range(0, 50):
    ds.appendLinked( features[i], labels[i])

# for input, target in ds:
#    print input, target

# net = buildNetwork(1, 3, 1, bias=True, hiddenclass=TanhLayer)
# trainer = BackpropTrainer(net, ds)

nn = buildNetwork(1, 5, 1, bias=True, hiddenclass=TanhLayer)
trainer = BackpropTrainer(nn, dataset=ds)


print trainer.train()

