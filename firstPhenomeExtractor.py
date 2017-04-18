import os
import soundfile as sf
from os.path import join, getsize
import wavFormatter
from words import getPhonemes, phonetic

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
    
def extractFirstPhonemes(topDirectory, extractDirectory):
    for root, dirs, files in os.walk(topDirectory): #from the top directory of data, walk the directory 
        if directoryContainsTranscript(files): #If the directory conntains a transcript, then create firstPhenome .wav file
                      
            #extract transcripts from file
            currentTranscripts = getTranscripts(root + "\\" + getTranscriptFile(files))
            #extract the first phenome out of the file, and save it to a directory
            print("You are here")
            for file in files: 
                if file[-4:] is '.wav': #check for .wav extension
                    firstWord = currentTranscripts[file[:-4]] #remove .wav extension
                    if firstWord in phonetic:
                        firstPhoneme = getPhonemes(phonetic[firstWord][0])
                        fileToExtractFrom = root + "\\" + file
                        wavFormatter.extractFirstPhonemeToWavFile(fileToExtractFrom, extractDirectory + firstPhoneme + ".wav")
                        print('reached')
                        return #temporary return
                    else:
                        #logged unkept word
                        print(firstWord + " is not in the dictionary")
                        
extractFirstPhonemes('C:\\REPO\\MLProject\\DataExtraction\\Libre-train-clean\\train-clean-100', 'C:\\REPO\\MLProject\\firstPhonemeTest\\')
                        
def getTranscripts(filepath):
    currentTranscripts = {}
    with open(filepath, encoding='utf-8-sig') as file:
        lines = file.readlines()
        for line in lines:
            stripped = line.strip()
            parts = stripped.split(" ")
            if len(parts[1:]) > 0:
                currentTranscripts[parts[0]] = parts[1:]
    return currentTranscripts
        
def getTranscriptFile(files):
    for file in files:
        if '.trans.txt' in file:
            return file
    
def directoryContainsTranscript(files):
    for file in files:
        if '.trans.txt' in file:
            return True
    return False

