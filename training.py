from fastNetwork import FastNetwork
import wavFormatter
import phonemes
import random
import time
import os

def formatData(unformatted, formatted):
    #get all of the files in the folder's subdirectories
    folders = [x for x in os.listdir(unformatted)]
    filePaths = [unformatted + "/" + folder + "/" + x for folder in folders for x in os.listdir(unformatted + "/" + folder)]
    
    #If there are not folders in the output folder, make them
    if not os.path.exists(formatted):
        os.makedirs(formatted)
    for folder in folders:
        if not os.path.exists(formatted + "/" + folder):
            os.makedirs(formatted + "/" + folder)
            
    #Down sample the audio to a standard 16kHz
    for filePath in filePaths:
        newPath = formatted + filePath[len(unformatted):]
        wavFormatter.downSample(filePath, newPath)

def collectData(formatted):
    #get all of the files in the folder's subdirectories
    folders = [x for x in os.listdir(formatted)]
    filePaths = [formatted + "/" + folder + "/" + x  for folder in folders for x in os.listdir(formatted + "/" + folder)]
    
    #Make sure that all of the data is 16kHz
    for filePath in filePaths:
        assert wavFormatter.check16(filePath)
    
    trainingData = [(data, filePath.split('/')[2][:-4]) for filePath in filePaths for data in wavFormatter.collectData(filePath)]
    trainingData = [data for data in trainingData if phonemes.contains(data[1])]
    
    inputs = [data[0] for data in trainingData]
    targets = [phonemes.getTargets('/' + data[1] + '/') for data in trainingData]
    
    return inputs, targets

def trainEpoch(network, inputs, targets):
    combined = list(zip(inputs, targets))
    random.shuffle(combined)
    for inputData, targetData in combined:
        network.backPropagate(inputData, targetData)
    
formatData("unformatted data", "formatted data")
inputs, targets = collectData("formatted data")

network = FastNetwork([37, 80, 120, 161], learningRate=.001)

start = time.time()
for i in range(20):
    if i % 5 == 0:
        print(i)
    trainEpoch(network, inputs, targets)
print(time.time() - start)

network.writeToFile("trained weights.txt")