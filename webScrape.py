import urllib2
import string
import pageRank


def getTextOnPage(url, index, wordCount=0):
    response = urllib2.urlopen(url)
    html = response.read()

    #Declaring variable and array
    pageText, pageWords = "", []
    #Finding all data in the body tag
    html = html[html.find("<body") + 5:html.find("</body")]

    #Finding Script Tags
    scriptStart = html.find("<script")
    while scriptStart > -1:
        scriptEnd = html.find("</script>")

        html = html[:scriptStart] + html[scriptEnd + len("</script>"):]
        scriptStart = html.find("<script")

    #Implementing Ignore List
    ignore = []
    fin = open("ignoreList.txt", "r")
    for word in fin:
        ignore.append(word.strip())
    fin.close()

    #Finding words in html page
    finished = False
    while not finished:
        nextClose = html.find(">")
        nextOpen = html.find("<")
        if nextOpen > -1:
            content = " ".join(html[nextClose + 1:nextOpen].strip().split())
            pageText = pageText + " " + content
            html = html[nextOpen + 1:]
        else:
            finished = True

    #Setting words to lower case and removing punctuation
    for word in pageText.split():
        word = word.lower()
        word = word.strip(string.punctuation)

        if word[0].isalnum() and not word in ignore:
            pageWords.append(word)
    
    for word in pageWords:
        wordCount += 1
        addWordPageToIndex(index, word, url, wordCount)

def addWordPageToIndex(index, keyword, url, wordCount):
    #Index structure
    if keyword in index:
        #Checks if keyword already exists
        dictionary = index[keyword]
        if url in dictionary:
            valuesArray = dictionary[url]
            valuesArray.append(wordCount)
        else:
            dictionary[url] = [wordCount]
    #Create new dictionary array and append index
    else:
        dictionary = {}
        dictionary[url] = [wordCount,]
        index[keyword] = dictionary

#Page Scraper main method
def pageScraper(graph):
    #Index dictionary array
    index = {}
    #Searches dictionary for url's, adds to completeUrlArray once scraped
    completeUrlArray = []
    for url in graph:
        if url not in completeUrlArray:
            #Gets the page text
            getTextOnPage(url, index)
            completeUrlArray.append(url)
    
    print ("\nData Generated")

    rank = pageRank.computeRanks(graph)

    return (index, rank)



