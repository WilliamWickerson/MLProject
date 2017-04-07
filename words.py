import phonemes
import numpy

global phonetic, phonemes
phonetic = {}
phonemeArray = {}
#Open the formatted text file and add all words to the dictionary
with open('formatted words.txt', encoding='utf-8-sig') as file:
    lines = file.readlines()
    for line in lines:
        stripped = line.strip()
        parts = stripped.split(" ")
        if len(parts[1][1:-1]) > 0:
              phonetic[parts[0]] = (parts[1][1:-1], lines.index(line))

#Splits the phonetic word into its phonemes
def getPhonemes(phoneticWord):
    ret = []
    string = phoneticWord
    while len(string) > 0:
        #Check for double letter phonemes first
        if any([string[0:2] == sound for sound in phonemes.doubleLetters]):
            ret = ret + ["/" + string[0:2] + "/"]
            string = string[2:]
        else:
            ret = ret + ["/" + string[0] + "/"]
            string = string[1:]
    return ret

#Add all broken down phonetic arrays to the dictionary
for word in phonetic:
    phonemeArray[word] = getPhonemes(phonetic[word][0])
    
def removeDuplicates(phoneticArray):
    ret = list()
    ret.append(phoneticArray[0])
    for i in range(1, len(phoneticArray)):
        if phoneticArray[i] != phoneticArray[i-1]:
            ret.append(phoneticArray[i])
    return ret

#Calculates the levenshtein distance between the array and every word in phonemeArray dict
#Returns the minimum based on the levenshtein distance followed by most common
def closestWord(phoneticArray):
    minimum = ("NULL", 10000, 10000)
    phoneticArray = removeDuplicates(phoneticArray)
    print(phoneticArray)
    for word in phonemeArray:
        tempArray = phonemeArray[word]
        distanceMatrix = numpy.zeros((len(phoneticArray), len(tempArray)))
        #Calculate the levenshtein distance between arrays
        for i in range(len(phoneticArray)):
            distanceMatrix[i, 0] = i
        for j in range(len(tempArray)):
            distanceMatrix[0, j] = j
        for j in range(0, len(tempArray)):
            for i in range(0, len(phoneticArray)):
                if tempArray[j] == phoneticArray[i]:
                    substitutionCost = 0
                else:
                    substitutionCost = 1
                distanceMatrix[i, j] = min([distanceMatrix[i-1, j] + 1,
                                            distanceMatrix[i, j-1] + 1,
                                            distanceMatrix[i-1, j-1] + substitutionCost])
        distance = distanceMatrix[len(phoneticArray) - 1, len(tempArray) - 1]
        #If the distance is lower or a similar distance is found on a more common word, replace minimum
        if (distance < minimum[1]) or (distance == minimum[1] and phonetic[word][1] < minimum[2]):
            minimum = (word, distance, phonetic[word][1])
    return minimum