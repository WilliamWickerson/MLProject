from fastNetwork import FastNetwork
from wavFormatter import collectData
import words
import phonemes

network = FastNetwork([37,100,161])
network.startFromFile("training weights.txt")

print(phonemes.getTargets("/th/"))
