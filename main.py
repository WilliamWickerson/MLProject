from fastNetwork import FastNetwork
import featureExtraction
import wavFormatter
import words
import phonemes

network = FastNetwork([37,100, 200, 40], softmax=True)
network.startFromFile("trained weights2.txt")

fileName = input("Type in the word's .wav file: ")

if not wavFormatter.checkRate(fileName, 8000):
    wavFormatter.downSample(fileName, "out8.wav", 8000)
    fileName = "out8.wav"
    
inputs = featureExtraction.extractFeatures(fileName)

outputs = network.networkOutputs(inputs[0])[0]
for i in range(0, len(outputs)):
    print(phonemes.getPhoneme(i), outputs[i])

phonemes = [phonemes.getPhoneme(network.classify(inp)[0]) for inp in inputs]

print(words.closestWord(phonemes))
