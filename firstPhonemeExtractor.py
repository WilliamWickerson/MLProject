import os
import wavFormatter
import words

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
    
def extractFirstPhonemesFromLibre(topDirectory, extractDirectory):
    missingWords = set([])
    
    for root, dirs, files in os.walk(topDirectory): #from the top directory of data, walk the directory 
        if directoryContainsTranscript(files): #If the directory conntains a transcript, then create firstPhenome .wav file
                      
            #extract transcripts from file
            currentTranscripts = getTranscripts(root + "\\" + getTranscriptFile(files))
            #extract the first phenome out of the file, and save it to a directory
            for file in files: 
                if file[-4:] == ".wav": #check for .wav extension
                    if file[:-4] not in currentTranscripts:
                        print("Error: " + root + file)
                        continue
                       
                       
                    firstWord = currentTranscripts[file[:-4]][0].lower() #remove .wav extension
                    if firstWord in words.phonemeArray:
                        firstPhoneme = words.phonemeArray[firstWord][0]
                        fileToExtractFrom = root + "\\" + file
                        #The [1:-1] strips the /s from the phenome
                        wavFormatter.extractFirstPhonemeToDirectory(fileToExtractFrom, extractDirectory, firstPhoneme[1:-1])
                    else:
                        #logged unkept word
                        missingWords.add(firstWord)
        
    #print missing words:
    target = open('missing-words-converter.txt', 'w')
    target.write("The words missing are:\n")
    for word in missingWords:
        target.write(word)
        target.write("\n")
    target.close()
                        


