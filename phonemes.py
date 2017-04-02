global phonemeDict
#A dictionary of the 37 phonemes we will be using
phonemeDict = {"/b/": 0,
               "/d/": 1,
               "/f/": 2,
               "/g/": 3,
               "/h/": 4,
               "/j/": 5,
               "/k/": 6,
               "/l/": 7,
               "/m/": 8,
               "/n/": 9,
               "/p/": 10,
               "/r/": 11,
               "/s/": 12,
               "/t/": 13,
               "/v/": 14,
               "/w/": 15,
               "/y/": 16,
               "/z/": 17,
               "/a/": 18,
               "/ā/": 19,
               "/e/": 20,
               "/ē/": 21,
               "/i/": 22,
               "/ī/": 23,
               "/ō/": 24,
               "/o/": 25, #/or/ sound
               "/ü/": 26,
               "/y/": 27,
               "/oi/": 28,
               "/ow/": 29,
               "/ə/": 30,
               "/ä/": 31,
               "/u̇/": 32, #As in hood
               "/zh/": 33,
               "/ch/": 34,
               "/sh/": 35,
               "/th/": 36,
               "/ŋ/": 37} #/'ng/ sound

#The double letters are important for words.py's getPhonemes() function
global doubleLetters
doubleLetters = ["oi", "ow", "zh", "ch", "sh", "th", "u̇"]

#NETWORK HELPER FUNCTIONS
#Returns the sound from a given number
def getPhoneme(number):
    for key in phonemeDict:
        if phonemeDict[key] == number:
            return key
        
#Returns the number for a given sound
def getNumber(phoneme):
    return phonemeDict[phoneme]

#Returns the target vector for a particular phoneme
def getTargets(phoneme):
    targets = [0]*37
    targets[phonemeDict[phoneme]] = 1
    return targets
            