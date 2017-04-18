import os
import numpy as np
import soundfile as sf
import time

def main():
    
    start = time.time()
    topDirectory = input("Choose a directory to convert: ")
    
    if os.path.isdir(topDirectory):
        convertFilesFromFlacToWav(topDirectory)
    else:
        print("Not a valid file directory")
    print(time.time() - start)

def convertFilesFromFlacToWav(topDirectory):
    #from the top directory of data, walk the directory 
    for root, dirs, files in os.walk(topDirectory): 
        for file in files:
            if ".flac" in file:
                data, samplerate = sf.read(root + "\\" + file)
                sf.write(root + "\\" + file[:-5] + ".wav", data, samplerate)
                        
if __name__ == "__main__":
    main()