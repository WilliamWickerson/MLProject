import os
import numpy as np
import scipy.io.wavfile as wavfile
import phonemes
import time

def main():
    
    topDirectory = input("Choose a directory to combine: ")
    extractDirectory = input("Choose a directory to save to: ")
    
    if os.path.isdir(topDirectory):
        combinePhenomesIntoOneWavFile(topDirectory, extractDirectory)
    else:
        print("Not a valid file directory")
        exit()
        
def combinePhenomesIntoOneWavFile(topDirectory, extractDirectory):
    
    #from the top directory of data, walk the directory 
    for root, dirs, files in os.walk(topDirectory): 
        for phoneme in phonemes.phonemeDict:
            phon = phoneme[1:-1] #Strips /'s from phoneme
            
            print("Current phoneme: " + phon)
            
            summedData = np.ndarray()
            maxRate = 0
            numberOfRates = 0
            for file in files:
                if file[-4:] == ".wav" and file[:1 + len(phon)] == phon + "-":
                    data, rate = wavfile.read(root + "\\" + file)
                    summedData = np.append(summedData, data)
                    
                    if maxRate < rate:
                        maxRate = rate
                        numberOfRates = numberOfRates + 1
                    
                    if numberOfRates > 1:
                        raise ValueError('Too many rates given')
            
            newFileName = extractDirectory + "\\" + phon + ".wav"
            wavfile.write(newFileName, maxRate, summedData)
            
            print("Written to: " + newFileName)   
                        
if __name__ == "__main__":
    main()

