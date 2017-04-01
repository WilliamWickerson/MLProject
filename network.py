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
        
network = Network([44,100,161])
network.startFromScratch()
network.writeToFile("test.txt")
network.startFromFile("test.txt")
network.writeToFile("test2.txt")