global phonemeDict
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
               "/o/": 24,
               "/ō/": 25,
               "/oo/": 26,
               "/u/": 27,
               "/ū/": 28,
               "/y/": 29,
               "/oi/": 30,
               "/ow/": 31,
               "/ə/": 32,
               "/ã/": 33,
               "/ä/": 34,
               "/û/": 35,
               "/ô/": 36,
               "/ēə/": 37,
               "/üə/": 38,
               "/zh/": 39,
               "/ch/": 40,
               "/sh/": 41,
               "/th/": 42,
               "/ng/": 43}

def getPhoneme(number):
    for key in phonemeDict:
        if phonemeDict[key] == number:
            return key
        
def getNumber(phoneme):
    return phonemeDict[phoneme]
            