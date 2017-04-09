from fastNetwork import FastNetwork
import wavFormatter
import words
import phonemes

network = FastNetwork([37,80,120,161], softmax=True)
network.startFromFile("trained weights.txt")

fileName = input("Type in the word's .wav file: ")

if not wavFormatter.check16(fileName):
    wavFormatter.downSample(fileName, "out16.wav")
    fileName = "out16.wav"
    
inputs = wavFormatter.collectData(fileName)

outputs = network.networkOutputs(inputs[0])[0]
for i in range(0, len(outputs)):
    print(phonemes.getPhoneme(i), outputs[i])

phonemes = [phonemes.getPhoneme(network.classify(input)[0]) for input in inputs]

print(words.closestWord(phonemes))
