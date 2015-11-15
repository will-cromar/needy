from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
import numpy

# creating data set
#X_train = [[x] for x in range(0,100)]
#y_train = [[2*x] for x in range(0,100)]

#X_test = [[x] for x in range(75,125)]
#y_test = [[2*x] for x in range(75,125)]

X_train = numpy.zeros(shape=[5])
y_train = numpy.zeros(shape=[5])

X_test = numpy.zeros(shape=[5])
y_test = numpy.zeros(shape=[5])

model = Sequential()
# Dense(64) is a fully-connected layer with 64 hidden units.
# in the first layer, you must specify the expected input data shape:
# here, 20-dimensional vectors.
model.add(Dense(64, input_dim=1, init='uniform'))
model.add(Activation('tanh'))
model.add(Dropout(0.5))
model.add(Dense(64, init='uniform'))
model.add(Activation('tanh'))
model.add(Dropout(0.5))
model.add(Dense(2, init='uniform'))
model.add(Activation('softmax'))

sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='mean_squared_error', optimizer=sgd)

model.fit(X_train, y_train, nb_epoch=20, batch_size=16)
score = model.evaluate(X_test, y_test, batch_size=16)
