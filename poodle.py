import sys
import re
import webCrawl
import queryEngine
import pickle
import os

def menu(buildComplete):
    options = ["-build", "-restore", "-exit"]
    print("*****************************************************")
    print("*********Woof*Welcome to Poodle*Main Menu************")
    print("*****************************************************")
    print("\n")
    print ("-build   (Create the Poodle database)")
    print ("-restore (Retrieve last Poodle session)")
    print ("-exit    (Exit from Poodle)")

    if buildComplete:
        options.extend(["-dump", "-search", "-print"])
        print ("-dump    (Save the Poodle database)")
        print ("-search  (Search crawled pages)")
        print ("-print   (Show index, graph and ranks files)")
    return options

def dump(index, ranks, graph):
    dumpData = {}
    dumpData['graph'] = graph
    dumpData['pageRanks'] = ranks
    dumpData['index'] = index

    fout = open("dumpData.txt", "w")
    pickle.dump(dumpData, fout)
    fout.close()

    print("Data has been stored")

def restore():
    if os.path.exists("dumpData.txt"):
        fin = open("dumpData.txt", "r")
        dumpData = pickle.load(fin)
        fin.close()
    else:
        return False

    return dumpData

def printAll(graph, index, ranks):
    print("*****************************************************")
    print("*****************Woof*Graph*Woof*********************")
    print("*****************************************************")
    print("\n")
    print graph

    print("*****************************************************")
    print("*****************Woof*Index*Woof*********************")
    print("*****************************************************")
    print("\n")
    print index

    print("*****************************************************")
    print("*****************Woof*Ranks*Woof*********************")
    print("*****************************************************")
    print("\n")
    print ranks

def exitMenu():
    sys.exit()

def search(index, rank, buildComplete):
    print("*****************************************************")
    print("****************Woof*Search*Woof*********************")
    print("*****************************************************")
    print("\n")

    while True:
        userQuery = raw_input("Enter a word to search ('-menu' to exit) >> ")
        if len(userQuery) > 0:
            if userQuery == '-menu':
                break
            else:
                userQueryList = re.findall(r"[\w']+", userQuery.lower())
                queryEngine.search(userQueryList, rank, index)

        else:
            print"\nNothing has been entered"

def build():
    index, ranks, graph = webCrawl.crawler()

    return index, ranks, graph

def getUserInput(buildComplete):
    while True:
        optionsMenu = menu(buildComplete)
        userInput = raw_input("\nWhat next? ('-exit' to exit) >> ")

        userInput = userInput.strip(" ")

        if userInput in optionsMenu:
            break
        else:
            print"\nInvalid option, try again\n"

    return userInput

def main():
    buildComplete = False
    while True:
        userInput = getUserInput(buildComplete)
        if userInput == "-build":
            index, ranks, graph = build()
            buildComplete = True
        elif userInput == "-search" and buildComplete:
            search(index, ranks, buildComplete)
        elif userInput == "-dump" and buildComplete:
            dump(index, ranks, graph)
        elif userInput == "-restore":
            dumpData = restore()

            if dumpData == False:
                print("No data has been stored yet")

            else:
                index = dumpData['index']
                ranks = dumpData['pageRanks']
                graph = dumpData['graph']
                buildComplete = True
       
        elif userInput == "-print" and buildComplete:
            printAll(graph, index, ranks)
        elif userInput == "-exit":
            exitMenu()

if __name__ == '__main__':
    main()
    
