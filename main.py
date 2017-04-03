from network import Network
import phonemes

network = Network([38,100,161])
network.startFromScratch()

print(phonemes.getTargets("/th/"))
