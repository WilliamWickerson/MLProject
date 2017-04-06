from random import uniform
import numpy

def sigmoidFunction(x):
    try:
        ret = 1 / (1 + numpy.exp(-x))
    except OverflowError:
        ret = 0
    return ret
        
global sigmoid
sigmoid = numpy.vectorize(sigmoidFunction)

class FastNetwork:
    def __init__(self, rowSizes, learningRate=1):
        self.weights = list()
        self.learningRate = learningRate
        for i in range(len(rowSizes)):
            if i == 0:
                r = numpy.sqrt(6 / (1 + rowSizes[i + 1]))
            elif i == len(rowSizes) - 1:
                r = numpy.sqrt(6 / (rowSizes[i - 1] + 1))
            else:
                r = numpy.sqrt(6 / (rowSizes[i - 1] + rowSizes[i + 1]))
            if i < len(rowSizes) - 1:
                tempArray = numpy.array([uniform(-r, r) for x in range(rowSizes[i]*(rowSizes[i+1] + 1))])
                tempArray = numpy.reshape(tempArray, (rowSizes[i], rowSizes[i+1] + 1))
            else:
                tempArray = numpy.array([uniform(-r, r) for x in range(rowSizes[i]*2)])
                tempArray = numpy.reshape(tempArray, (rowSizes[i], 2))
            self.weights.append(tempArray)
    def startFromFileOld(self, filename):
        with open(filename) as weightFile:
            rows = weightFile.readlines()
            rowData = [numpy.fromstring(row.strip()[2:-1], sep=' ') for row in rows]
            assert len(rowData) == sum(matrix.shape[0] for matrix in self.weights)
            for i in range(len(self.weights)):
                size = self.weights[i].shape[0]
                length = self.weights[i].shape[1]
                assert all([len(row) == length for row in rowData[:size]])
                newArray = numpy.stack(rowData[0:size])
                self.weights[i] = newArray
                rowData = rowData[size:]
    def startFromFile(self, filename):
        with open(filename) as weightFile:
            weightStrings = weightFile.readlines()
            assert len(weightStrings) == len(self.weights)
            for i in range(len(weightStrings)):
                weightString = weightStrings[i].strip()
                weightArray = numpy.fromstring(weightString[2:-1], sep=' ')
                assert weightArray.size == self.weights[i].size
                weightArray = numpy.reshape(weightArray, self.weights[i].shape)
                self.weights[i] = weightArray
    def writeToFile(self, filename):
        with open(filename, 'w') as weightFile:
            numpy.set_printoptions(threshold = numpy.inf, linewidth = numpy.inf)
            for matrix in self.weights:
                printable = numpy.reshape(matrix, (numpy.product(matrix.shape)))
                weightFile.write(numpy.array_str(printable) + "\n")
            numpy.set_printoptions(threshold = 10, linewidth = 75)
    def networkOutputs(self, inputs):
        assert len(inputs) == self.weights[len(self.weights) - 1].shape[0]
        outputs = list()
        for i in reversed(range(len(self.weights))):
            #Input Layer
            if i == len(self.weights) - 1:
                inputArray = numpy.array(inputs)
                inputArray = numpy.reshape(inputArray, (len(inputs), 1))
                onesArray = numpy.ones((len(inputs), 1))
                inputArray = numpy.concatenate((inputArray, onesArray), axis=1)
                #Row-wise dot product of inputs and weights
                output = numpy.einsum('ij, ij->i', self.weights[i], inputArray)
                output = sigmoid(output)
                outputs.append(output)
            #Otherwise
            else:
                inputArray = numpy.array(numpy.concatenate((outputs[0], [1])))
                #inputArray = 
                #Matrix multiplication of weights and input vector
                output = self.weights[i] @ inputArray
                output = sigmoid(output)
                outputs.insert(0, output)
        return outputs
    def classify(self, inputs):
        outputs = self.networkOutputs(inputs)
        maxValue = max(outputs[0])
        maxIndex = outputs[0].tolist().index(maxValue)
        return maxIndex, maxValue
    def backPropagate(self, inputs, targets):
        outputs = self.networkOutputs(inputs)
        targets = numpy.array(targets)
        inputs = numpy.array(inputs)
        deltas = list()
        changes = list()
        for i in range(len(self.weights)):
            #Output layer
            if i == 0:
                error = targets - outputs[i]
                delta = error * outputs[i] * (numpy.ones((self.weights[i].shape[0])) - outputs[i])
                deltas.append(delta)
                change = numpy.outer((self.learningRate * deltas[i]), numpy.array(numpy.concatenate((outputs[i+1], [1]))))
                changes.append(change)
            #Input layer
            elif i == len(self.weights) - 1:
                error = numpy.dot(deltas[i - 1], self.weights[i - 1][:,:-1])
                delta = error * outputs[i] * (numpy.ones((self.weights[i].shape[0])) - outputs[i])
                deltas.append(delta)
                doubleDelta = numpy.stack((delta, delta))
                inputArray = numpy.stack((inputs, numpy.ones(self.weights[i].shape[0])))
                change = numpy.transpose(doubleDelta * inputArray)
                changes.append(change)
            #Hidden layer
            else:
                error = numpy.dot(deltas[i - 1], self.weights[i - 1][:,:-1])
                delta = error * outputs[i] * (numpy.ones((self.weights[i].shape[0])) - outputs[i])
                deltas.append(delta)
                change = numpy.outer((self.learningRate * deltas[i]), numpy.array(numpy.concatenate((outputs[i+1], [1]))))
                changes.append(change)
        for i in range(len(self.weights)):
            self.weights[i] += changes[i]
                
"""
numpy.set_printoptions(threshold = numpy.inf, linewidth = numpy.inf)
network = FastNetwork([40,100,161])
#network.writeToFile("test.txt")
#network.startFromFile("test.txt")
network.startFromFileOld("old.txt")    
outputs = network.networkOutputs([1]*161)
print(outputs[0])
network.backPropagate([1]*161, [0] + [1] + [0]*38)

import time
start = time.time()
for i in range(1000):
    network.backPropagate([1]*161, [0] + [1] + [0]*38)
print(time.time() - start)
"""
"""
print(network.classify([1]*161))
print(network.networkOutputs([1]*161)[0])
"""
