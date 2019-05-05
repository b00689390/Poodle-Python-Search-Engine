def computeRanks(graph):
    ranks = {}
    d = 0.85
    numLoops = 10
    numPages = len(graph)

    for page in graph:
        ranks[page] = 1.0 / numPages

    for i in range(0, numLoops):
        newRanks = {}
        for page in graph:
            newRank = (1 - d) / numPages
            for node in graph:
                if page in graph[node]:
                    newRank = newRank + d * (ranks[node] / len(graph[node]))
            newRanks[page] = newRank
        ranks = newRanks
    return ranks