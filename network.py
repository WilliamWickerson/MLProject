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
                    node.theta = numpy.array([random() for x in range(len(self.network[rowNum + 1]))])
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
                    assert len(nodeData[dataRowCounter]) == len(self.network[rowNum + 1])
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
        outputs = [numpy.array(inputs)]
        for rowNum in reversed(range(0, len(self.network))):
            layorOutputs = [neuron.sigmoid(outputs[0]) for neuron in self.network[rowNum]]
            outputs = [layorOutputs] + outputs
        return outputs
    def classify(self, inputs):
        outputs = networkOutputs(inputs)
        maxValue, maxIndex = max(outputs[0])
        return maxIndex
    def backPropagate(self, inputs, targets):
        outputs = networkOutput(inputs)
        for rowNum in range(0, len(self.network)):
            if rowNum == 0:
                for neuronNum in range(0, len(self.network[rowNum])):
                    error = targets[neuronNum] - outputs[rowNum][neuronNum]
                    self.network[rowNum][neuronNum].updateDelta(outputs[rowNum + 1], error)
            else:
                for neuronNum in range(0, len(network[rowNum])):
                    error = 0
                    for neuron in self.network[rowNum - 1]:
                        error += neuron.theta[neuronNum + 1] * neuron.delta
                    self.network[rowNum][neuronNum].updateDelta(outputs[rowNum + 1], error)
        for rowNum in range(0, len(self.network)):
            for neuron in self.network[rowNum]:
                neuron.updateWeights(outputs[rowNum + 1])
        
network = Network([44,100,161])
network.startFromScratch()
network.writeToFile("test.txt")
network.startFromFile("test.txt")
network.writeToFile("test2.txt")