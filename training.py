from fastNetwork import FastNetwork
import featureExtraction
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
        wavFormatter.downSample(filePath, newPath, 8000)

def collectData(formatted):
    #get all of the files in the folder's subdirectories
    folders = [x for x in os.listdir(formatted)]
    filePaths = [formatted + "/" + folder + "/" + x  for folder in folders for x in os.listdir(formatted + "/" + folder)]
    
    #Make sure that all of the data is 16kHz
    for filePath in filePaths:
        assert wavFormatter.checkRate(filePath)
    
    trainingData = [(data, filePath.split('/')[2][:-4]) for filePath in filePaths for data in wavFormatter.collectData(filePath)]
    trainingData = [data for data in trainingData if phonemes.contains(data[1])]
    
    inputs = [data[0] for data in trainingData]
    targets = [phonemes.getTargets('/' + data[1] + '/') for data in trainingData]
    
    return inputs, targets

def collectDataNew(formatted):
    #get all of the files in the folder's subdirectories
    folders = [x for x in os.listdir(formatted)]
    filePaths = [formatted + "/" + folder + "/" + x  for folder in folders for x in os.listdir(formatted + "/" + folder)]
    
    trainingData = [(data, filePath.split('/')[2][:-4]) for filePath in filePaths for data in featureExtraction.extractFeatures(filePath)]
    trainingData = [data for data in trainingData if phonemes.contains(data[1])]
    
    inputs = [data[0] for data in trainingData]
    targets = [phonemes.getTargets('/' + data[1] + '/') for data in trainingData]
    
    return inputs, targets

def shuffleTogether(list1, list2):
    assert len(list1) == len(list2)
    indices = list(range(len(list1)))
    random.shuffle(indices)
    return [(list1[i], list2[i]) for i in indices]

def trainEpoch(network, inputs, targets):
    for inputData, targetData in shuffleTogether(inputs, targets):
        network.backPropagate(inputData, targetData)
    
formatData("unformatted data", "formatted data")
inputs, targets = collectDataNew("formatted data")

network = FastNetwork([37, 37, 38, 38, 39, 39, 40, 40], learningRate=.1, softmax=True)

start = time.time() 
for i in range(100):
    print(i)
    trainEpoch(network, inputs, targets)
print(time.time() - start)

network.writeToFile("trained weights2.txt")