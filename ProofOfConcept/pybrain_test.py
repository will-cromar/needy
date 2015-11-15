# luke

from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import TanhLayer, SigmoidLayer, LinearLayer
from pybrain.tools.neuralnets import NNregression, Trainer
from util import savePickle
import time

features = []
for i in range (0,50):
    features.append(i)

labels = []
for i in range (0,50):
    labels.append(2*i)

ds = SupervisedDataSet(1, 1)
for i in range (0,50):
    ds.appendLinked( features[i], labels[i])

#for input, target in ds:
#    print input, target

#net = buildNetwork(1, 3, 1, bias=True, hiddenclass=TanhLayer)
#trainer = BackpropTrainer(net, ds)

nn = NNregression(ds)
nn.setupNN()


start = time.time()
#print trainer.train()
print nn.runTraining()
end = time.time()
nn.activate([9])
print (end - start)
savePickle(nn, 'nn')
