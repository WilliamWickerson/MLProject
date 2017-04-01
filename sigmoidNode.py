import numpy

class SigmoidNode:
    def __init__(self, initialWeights = numpy.array([]), name = None):
        self.theta = initialWeights
        self.name = name
        self.delta = 0
    def sigmoid(self, inputs):
        #implements sigmoid with try/catch for huge input
        inputs = [1] + inputs
        sigma = numpy.dot(inputs, self.theta)
        try:
            ret = 1 / (1 + numpy.exp(-sigma))
        except OverflowError:
            ret = 0
        return ret
    def updateDelta(self, inputs, error):
        #stores the total error in the node
        output = self.sigmoid(inputs)
        self.delta = error * output * (1 - output)
    def updateWeights(self, inputs):
        #updates weights in accordance with stored error
        learningRate = 1
        inputs = [1] + inputs
        for i in range(len(inputs)):
            self.theta[i] += learningRate * self.delta * inputs[i]
        
