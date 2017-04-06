from random import random
import numpy

from sigmoidNode import SigmoidNode

class Network:
    def __init__(self, rowSizes):
        #Initialize the network's nodes
        self.network = list()
        for i in rowSizes:
            self.network += [[SigmoidNode() for x in range(i)]]
    def startFromScratch(self):
        #Iterates through the network giving a random vector of weights
        for rowNum in range(len(self.network)):
            if rowNum + 1 < len(self.network):
                for node in self.network[rowNum]:
                    node.theta = numpy.array([random() / len(self.network[rowNum + 1]) for x in range(len(self.network[rowNum + 1]) + 1)])
            else:
                for node in self.network[rowNum]:
                    node.theta = numpy.array([random() for x in range(2)])
    def startFromFile(self, fileName):
        #Read in the data from the file
        with open(fileName) as file:
            nodeStrings = file.readlines()
            file.close()
        nodeData = [numpy.fromstring(row[2:-1], sep=' ') for row in nodeStrings]
        #Assert that the data read in is equal to the network size
        assert len(nodeData) == sum([len(row) for row in self.network])
        #Give the data to the individual neurons
        dataRowCounter = 0
        for rowNum in range(len(self.network)):
            for nodeNum in range(len(self.network[rowNum])):
                #Assert that the number of inputs for that neuron is correct
                if rowNum + 1 < len(self.network):
                    assert len(nodeData[dataRowCounter]) == len(self.network[rowNum + 1]) + 1
                else:
                    assert len(nodeData[dataRowCounter]) == 2
                #Give the neuron the input data
                self.network[rowNum][nodeNum].theta = nodeData[dataRowCounter]
                dataRowCounter += 1
            
    def writeToFile(self, fileName):
        #Open the file, set print options, and iterate through the rows printing data
        file = open(fileName, 'w')
        numpy.set_printoptions(threshold = numpy.inf, linewidth = numpy.inf)
        for row in self.network:
            for node in row:
                file.write(numpy.array_str(node.theta) + "\n")
        numpy.set_printoptions(threshold = 10, linewidth = 75)
        file.close()
    def networkOutputs(self, inputs):
        assert len(inputs) == len(self.network[len(self.network) - 1])
        outputs = [inputs]
        for rowNum in reversed(range(0, len(self.network))):
            if rowNum + 1 < len(self.network):
                layorOutputs = [neuron.sigmoid(outputs[0]) for neuron in self.network[rowNum]]
                outputs = [layorOutputs] + outputs
            else:
                layorOutputs = [self.network[rowNum][i].sigmoid([outputs[0][i]]) for i in range(len(outputs[0]))]
                outputs = [layorOutputs] + outputs
        return outputs
    def classify(self, inputs):
        outputs = self.networkOutputs(inputs)
        maxValue = max(outputs[0])
        maxIndex = outputs[0].index(maxValue)
        return maxIndex, maxValue
    def backPropagate(self, inputs, targets):
        outputs = self.networkOutputs(inputs)
        for rowNum in range(0, len(self.network)):
            if rowNum == 0:
                for neuronNum in range(0, len(self.network[rowNum])):
                    error = targets[neuronNum] - outputs[rowNum][neuronNum]
                    self.network[rowNum][neuronNum].updateDelta(outputs[rowNum + 1], error)
            elif rowNum + 1 < len(self.network):
                for neuronNum in range(0, len(self.network[rowNum])):
                    error = 0
                    for neuron in self.network[rowNum - 1]:
                        error += neuron.theta[neuronNum + 1] * neuron.delta
                    self.network[rowNum][neuronNum].updateDelta(outputs[rowNum + 1], error)
            else:
                for neuronNum in range(0, len(self.network[rowNum])):
                    error = 0
                    for neuron in self.network[rowNum - 1]:
                        error += neuron.theta[neuronNum + 1] * neuron.delta
                    self.network[rowNum][neuronNum].updateDelta([outputs[rowNum + 1][neuronNum]], error)
        for rowNum in range(0, len(self.network)):
            if rowNum + 1 < len(self.network):
                for neuron in self.network[rowNum]:
                    neuron.updateWeights(outputs[rowNum + 1])
            else:
                for neuronNum in range(0, len(self.network[rowNum])):
                    self.network[rowNum][neuronNum].updateWeights([outputs[rowNum + 1][neuronNum]])
    
""" Some test usage
network = Network([40,100,161])
network.startFromFile("old.txt")
outputs = network.networkOutputs([1] * 161)
print(outputs[0])
#print(outputs[len(outputs) - 2])
#print(network.network[0][1].theta)

network.startFromScratch()
network.writeToFile("old.txt")
import time

network.backPropagate([1]*161, [0] + [1] + [0]*38)

start = time.time()
for i in range(1000):
    network.backPropagate([1]*161, [0] + [1] + [0]*38)
print(time.time() - start)
print(network.classify([1]*161))
print(network.networkOutputs([1]*161)[0])

network.writeToFile("test2.txt")
"""