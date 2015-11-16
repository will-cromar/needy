__author__ = 'tylervanharen'
from pybrain.structure import RecurrentNetwork, LinearLayer, FullConnection

rnn = RecurrentNetwork()
rnn.addInputModule(LinearLayer(1, 'in'));
rnn.addModule(LinearLayer(3,'hidden'));
rnn.addOutputModule(LinearLayer(1,'out'));
rnn.addConnection(FullConnection(rnn['in'],rnn['hidden'],'feed'));
rnn.addConnection(FullConnection(rnn['hidden'],rnn['out'],'give'));
rnn.addRecurrentConnection(FullConnection(rnn['hidden'],rnn['hidden'],'hide'));
rnn.sortModules();

