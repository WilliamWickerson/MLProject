from lxml import html
import requests

#A web scraper function that grabs pronunciations off of merriam webster
def getCommonPronunciations():
    with open("most common words.txt") as wordFile:
        words = wordFile.readlines()
        wordFile.close()
    
    writeFile = open("words with pronunciation.txt", 'w', encoding='utf-8')
    
    for word in words:
        word = word.strip()
        
        #Open the merriam webster page and get the html
        page = requests.get("https://www.merriam-webster.com/dictionary/" + word)
        tree = html.fromstring(page.content)
        #Look for the pronunciation and grab it    
        pronunciationContent = tree.xpath('//span[@class="pr"]//text()')
        if len(pronunciationContent) == 0:
            pronunciation = '""'
        elif pronunciationContent[0] != "\\":
            pronunciation = '"' + pronunciationContent[0] + '"'
        else:
            pronunciation = '""'
        
        writeFile.write(word + " " + pronunciation + "\n")
                                        
        print(pronunciation)
        
    writeFile.close()

#Gets the substring less than a set of characters
def endAtCharacter(string, characters):
    i = 0
    while (i < len(string)):
        if any([string[i] == c for c in characters]):
            break
        i += 1
    return string[:i]

#Gets the substring where anything inside parentheses is removed
#aka be(can)come -> become
def removeParentheses(string):
    ret = string
    try:
        while True:
            ret = ret[:ret.index("(")] + ret[ret.index(")") + 1:]
    except:
        return ret
    
#Removes any of the characters found in the array from the string
def removeCharacters(string, characters):
    ret = string
    for character in characters:
        ret = ret.replace(character, "")
    return ret

#Takes all of the raw merriam webster pronunciations and converts them to a
#single usable phonetic transcription for each word
def convertUsable():
    characterDict = {}
    writeFile = open('formatted words.txt', 'w', encoding='utf-8')
    
    with open("words.txt", encoding='utf-8') as wordFile:
        lines = wordFile.readlines()
        for line in lines:
            line = line.strip()
            pronunciation = line.split(" ")[1]
            if pronunciation.startswith('"\\') or pronunciation.startswith('"\ˌ'):
                pronunciation = pronunciation[2:]
            else:
                pronunciation = pronunciation[1:]
            pronunciation = endAtCharacter(pronunciation, [",", "\\", ";", '"'])
            pronunciation = removeParentheses(pronunciation)
            pronunciation = removeCharacters(pronunciation, ["-", "ˌ", "ˈ"])
            pronunciation = pronunciation.replace("ⁿ", "n")
            pronunciation = pronunciation.replace("ȯ", "o")
            pronunciation = pronunciation.replace("au̇", "ow")
            pronunciation = pronunciation.replace("ə", "uh")
            writeFile.write(line.split(" ")[0] + ' "' + pronunciation + '"\n')
                             
    for character in characterDict:
        print(character)
        
    writeFile.close()

#A helper function to allow a user to add phonetic transcriptions where missing
def addWords():
    writeFile = open('new words.txt', 'w', encoding='utf-8')
    
    with open("words.txt", encoding='utf-8') as wordFile:
        lines = wordFile.readlines()
        for line in lines:
            line = line.strip()
            pronunciation = line[line.index('"') + 1:]
            pronunciation = pronunciation[:pronunciation.index('"')]
            if len(pronunciation) == 0:
                print(line)
                selection = input()
                writeFile.write(line.split(" ")[0] + ' "' + selection + '"\n')
            else:
                writeFile.write(line + "\n")
    
    writeFile.close()

#This shouldn't need to be used, I just made a mistake
def fixFormatting():
    writer = open('new words.txt', 'w', encoding='utf-8')
    with open("words.txt", encoding='utf-8') as wordFile:
        lines = wordFile.readlines()
        for line in lines:
            line = line.strip()
            pronunc = line.split(" ")[1]
            if pronunc == '"':
                x = 1
            elif pronunc[0] != '"':
                writer.write(line.split(" ")[0] + ' "' + line.split(" ")[1] + "\n")
            else:
                writer.write(line + "\n")
    writer.close()

#Running this script just converts words.txt to formatted words.txt
convertUsable()