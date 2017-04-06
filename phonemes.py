global phonemeDict
#A dictionary of the 37 phonemes we will be using
phonemeDict = {"/a/": 0,
               "/ä/": 1, #soft a as in 'fought'
               "/ā/": 2,
               "/b/": 3,
               "/ch/": 4,
               "/d/": 5,
               "/e/": 6,
               "/ē/": 7,
               "/f/": 8,
               "/g/": 9,
               "/h/": 10,
               "/i/": 11,
               "/ī/": 12,
               "/j/": 13,
               "/k/": 14,
               "/l/": 15,
               "/m/": 16,
               "/n/": 17,
               "/ŋ/": 18, #/'ng/ sound
               "/o/": 19, #/or/ sound, more closed mouth than /ä/
               "/ō/": 20,
               "/oi/": 21,
               "/ow/": 22,
               "/p/": 23,
               "/r/": 24,
               "/s/": 25,
               "/sh/": 26,
               "/t/": 27,
               "/th/": 28,
               "/u̇/": 29, #As in hood
               "/ü/": 30, #/oo/ sound as in boo
               "/uh/": 31,
               "/v/": 32,
               "/w/": 33,
               "/y/": 34,
               "/z/": 35,
               "/zh/": 36, #as in ver/zh/in (version)
               }

#The double letters are important for words.py's getPhonemes() function
global doubleLetters
doubleLetters = ["oi", "ow", "zh", "ch", "sh", "th", "u̇", "uh"]

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
            
def contains(phoneme):
    check = "/" + phoneme + "/"
    return check in phonemeDict