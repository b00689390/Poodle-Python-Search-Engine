import urllib2
import string

class PageData:
    def __init__(self, url, rank, uniqueWordsCount, wordPositions, wordFound):
        self.url = url
        self.rank = rank
        self.uniqueWordsCount = uniqueWordsCount
        self.wordPositions = wordPositions
        self.wordFound = [wordFound, ]

    def getUrl(self):
        return self.url
    
    def getRank(self):
        return self.rank

    def getUniqueWordsCount(self):
        return self.uniqueWordsCount

    def getWordPositions(self):
        return self.wordPositions

    def getWordFound(self):
        return self.wordFound

    def addMoreSearchWord(self, searchWord, wordPositions):
        self.wordPositions.extend(wordPositions)
        self.wordFound.append(searchWord)
        self.uniqueWordsCount += 1

class SearchData:
    def __init__(self, numSearchWords):
        self.allWordsMatch = []
        self.someWordsMatch = []
        self.singleWordMatch = []
        self.numSearchWords = numSearchWords

    def addMatchingPage(self, pageData):
        if pageData.getUniqueWordsCount() == self.numSearchWords:
            self.allWordsMatch.append((pageData.getUrl(), pageData.getRank(), pageData.getWordFound()))
        elif pageData.getUniqueWordsCount() > 1:
            self.someWordsMatch.append((pageData.getUrl(), pageData.getRank(), pageData.getWordFound()))
        elif pageData.getUniqueWordsCount() == 1:
            self.singleWordMatch.append((pageData.getUrl(), pageData.getRank(), pageData.getWordFound()))

    def getRankMatches(self):
        self.allWordsMatch = sorted(self.allWordsMatch, reverse = True, key = lambda x: x[1])
        self.someWordsMatch = sorted(self.someWordsMatch, reverse = True, key = lambda x: x[1])
        self.singleWordMatch = sorted(self.singleWordMatch, reverse = True, key = lambda x: x[1])

        results = self.allWordsMatch
        results.extend(self.someWordsMatch)
        results.extend(self.singleWordMatch)

        return results

def printResults(results):
    if len(results) > 0:
        for result in results:
            print(("\nUrl: {0} \nRanks: {1} \nWords Matched: {2}").format(result[0], result[1], result[2]))
            print("Text Description: ")
            descrResult(result[0], result[2])
    else:
        print("\nNo results found")

def descrResult(url, matchedWords):
    response = urllib2.urlopen(url)
    html = response.read()
    html = html.strip(string.punctuation).split("\n")

    for l in html:
        l = l.lower().split(" ")
        for word in matchedWords:
            if word in l:
                pos = l.index(word)
                descrResultValidation(pos - 1, l)
                descrResultValidation(pos, l)
                descrResultValidation(pos + 1, l)
                print("")

def descrResultValidation(pos, l):
    if pos > 0 and pos < len(l):
        word = l[pos]
        if word.find("<") == -1:
            print word,

def search(userQueryList, urlPageRank, wordIndexData):
    searchEngineArray = {}

    for searchWord in userQueryList:
        if searchWord in wordIndexData:
            dictOfIndex = wordIndexData[searchWord]

            for url in dictOfIndex:
                wordPositions = dictOfIndex[url]
                pageRank =  urlPageRank[url]
                if url in searchEngineArray:
                    urlData = searchEngineArray[url]
                    urlData.addMoreSearchWord(searchWord, wordPositions)

                else:
                    urlData = PageData(url, pageRank, 1, wordPositions, searchWord)
                    searchEngineArray[url] = urlData

    searchResults = SearchData(len(userQueryList))
    for url in searchEngineArray:
        searchResults.addMatchingPage(searchEngineArray[url])

    results = searchResults.getRankMatches()
    printResults(results)
            