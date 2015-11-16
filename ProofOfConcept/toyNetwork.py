class Neuron:
    'Represents a neuron'
    currentVal = 0
    threshold = 1
    connections = []
    identity = 0
    def displayVal(self):
        print(self.identity,":",self.currentVal)
        for c in self.connections:
            print(self.identity," connected to ",c.end.identity)

    def addSynapse(self,destination):
        print(self.identity," connecting to ",destination.identity)
        connection = Synapse()
        connection.start = self
        connection.end = destination
        self.connections.append(connection)

    def fire(self):
        if self.connections.__len__()==0 :
            print(self.currentVal)
        else:
            for connection in self.connections:
                print(self.identity," firing on ",connection.end.identity)
                connection.end.currentVal+=connection.modifier*self.currentVal
        self.currentVal = self.currentVal/2

    def go(self):
        if(self.currentVal>self.threshold):
            self.fire()
        self.currentVal-=.05
        if(self.currentVal<0):
            self.currentVal=0

class Synapse:
    start = Neuron()
    end = Neuron()
    modifier = .75

numLayers = 5
nodesPerLayer = 3
layers = []

first = Neuron()
firstlayer = [first]
layers.append(firstlayer)
for i in range(1, numLayers-1, 1):
    hiddenLayer = []
    for j in range(0, nodesPerLayer, 1):
        new = Neuron()
        new.identity = i*nodesPerLayer+j
        hiddenLayer.append(new)
        print(layers[len(layers)-1])
        for k in layers[i - 1]:
            k.addSynapse(new)
    layers.append(hiddenLayer)

finaLayer = []
final = Neuron()
final.identity=numLayers*nodesPerLayer+1
finaLayer.append(final)
for k in layers[layers.__len__()-1]:
    k.addSynapse(final)
layers.append(finaLayer)
all = []

for i in range(0,layers.__len__(),1):
    for j in layers[i]:
        all.append(j)

for i in range(0,10,1):
    first.currentVal+= input("Thing:")
    for n in all:
        n.go()
        n.displayVal()