import urllib2
import webScrape


#Create Graph
def getCrawlUrl():
    #Prompt user for a url
    while True:
        urlToCrawl = raw_input("Enter a URL >> ")
        #Remove Whitespace
        urlToCrawl = urlToCrawl.strip(" ")

        #Verify url starts with http:// or https://
        if urlToCrawl[:7] == "http://" or urlToCrawl[:8] == "https://":
            if urlToCrawl[-1] == "/":
                urlToCrawl = urlToCrawl[:-1]
            break
        else:
            print("\nInvalid Url\n")
        
    return [(urlToCrawl, 0)]

def getMaxCrawl():
    while True:
        #Limits the amount of pages to crawl
        try:
            maxCrawl = int(raw_input('\nEnter the Max urls to Crawl, between 0-10 >> '))
        except ValueError:
            #Error message if a non-number value is entered
            print 'Not a number! Try again.'
        else:
            #Checking if in range
            if 0 <= maxCrawl < 11:
                break
            else:
                print 'Out of range. Try again.'

    return maxCrawl

def getNewLinks(page, prevLinks):
    response = urllib2.urlopen(page)
    html = response.read()

    #Declaring Variables
    links, linksFound, pos, allFound = [], [], 0, False
    while not allFound:
        #Finding the start of href for new links
        aTag = html.find("<a href=", pos)
        if aTag > -1:
            #Finding start of url
            href = html.find('"', aTag + 1)
            #Finding end of url
            endHref = html.find('"', href + 1)
            #Declaring Url
            url = html[href + 1:endHref]

            #Verify url starts with http:// or https://
            if url[:7] == "http://" or url[:8] == "https://":
                #Removing / at end of url
                if url[-1] == "/":
                    url = url[:-1]
                if not url in links and not url in prevLinks:
                    links.append(url)
                if url not in linksFound:
                    linksFound.append(url)
            
            #Finding closing </a> tag
            closeTag = html.find("</a>", aTag)
            pos = closeTag + 1
        else:
            allFound = True
    return (links, linksFound)

def crawler():
    graph = {}

    toCrawl = getCrawlUrl()
    #List of crawled urls
    crawled = []
    #Get max urls to crawl from user
    maxDepth = getMaxCrawl()

    while len(toCrawl) > 0:
        top = toCrawl.pop()
        url = top[0]
        level = top[1]

        crawled.append(url)

        newLinks, linksFound = getNewLinks(url, crawled)
        #Checking level url was found is less than maxDepth
        if (level < maxDepth):
            for newLink in newLinks:
                toCrawl.append((newLink, level + 1))

        #Creating the list of links found at a given url
        graph[url] = linksFound

    #Printing url's found
    print ("\nUrl's Found: ")
    for url in graph:
        print url
    
    index, ranks = webScrape.pageScraper(graph)

    return (index, ranks, graph)