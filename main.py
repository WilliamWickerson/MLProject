from network import Network
import phonemes

network = Network([44,100,161])
network.startFromScratch()

print(phonemes.getTargets("/th/"))
