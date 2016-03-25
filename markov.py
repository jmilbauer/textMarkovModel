import random, string, sys, os

class TextModel(object):
    def __init__(self, text):
        self.startingwords = self.getStartingWords(text) #allwords[text.split(' ')[0]]
        self.dictionary = self.buildDictionary(text)

    #getNextWord :: STATE -> String -> String
    def getNextWord(self, word):
        return random.choice(self.dictionary[word])

    #buildDictionary :: STATE -> String -> {String:[String]}
    def buildDictionary(self, text):
        result = {}
        words = self.tokenize(text)
        for i in range(len(words) - 1):
            word = words[i]
            if word in result.keys():
                result[word].append(words[i+1])
            else:
                result[word] = [words[i+1]]
        return result

    #getStartingWords :: STATE -> [String] -> [String]
    def getStartingWords(self,text):
        words = self.tokenize(text)
        result = [words[0]]
        for i in range(len(words) - 1):
            word = words[i]
            if word[-1] == '.' or word[-1] == '?' or word[-1] == '!':
                result.append(words[i+1])
        return result

    #getStart :: STATE -> String
    def getStart(self):
        return random.choice(self.startingwords)

    #tokenize :: STATE -> String -> [String]
    def tokenize(self, text):
        text = removeExcessiveWhitespace(text)
        lines = text.split('\n')
        tokens = []
        for line in lines:
            linelist = line.split(' ')
            #for i in range(len(linelist) - 1):
            #    if linelist[i] == '':
            #        linelist = linelist[:(i+1)] + linelist[(i+2):]
            tokens = tokens + linelist
        return removeEmptyStrings(tokens)

def removeExcessiveWhitespace(text):
    i = 0
    string = text
    while i < len(string) - 1:
        char = string[i]
        nextchar = string[i+1]
        if (char == ' ' and nextchar == ' '):
            string = string[:(i)] + string[(i+1):]
        elif (char == '\n' and nextchar == '\n'):
            string = string[:(i)] + string[(i+1):]
        else:
            i += 1
    return string

def removeEmptyStrings(listofstrings):
    i = 0
    stringlist = listofstrings
    while i < len(stringlist):
        if stringlist[i] == '':
            stringlist = stringlist[:(i)] + stringlist[(i+1):]
        else:
            i += 1
    return stringlist

def runMarkov(corpus):
    model = TextModel(corpus)
    firstword = model.getStart()

    sentence = [firstword]
    oldword = firstword
    while(oldword[-1] != '.'):
        newword = model.getNextWord(oldword)
        sentence.append(newword)
        oldword = newword

    sentence = ' '.join(sentence)
    return sentence

progname, filename = sys.argv
inputfile = open(filename)
inputtext = inputfile.read()

generatedSentences = []

for _ in range(20):
    generatedSentences.append(runMarkov(inputtext))

for sentence in generatedSentences:
    print
    print sentence
    print
