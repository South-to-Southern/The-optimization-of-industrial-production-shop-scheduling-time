import random

def getElitePop(pop,POP_NUM):
    elitePop = []

    mid = (1 + POP_NUM) * POP_NUM / 2
    choiceProbability = [i/mid for i in range(POP_NUM,0,-1)]

    while len(elitePop) < POP_NUM:
        enterIndex = getEnterIndex(choiceProbability)
        elitePop.append(pop[enterIndex])

    return elitePop

def getEnterIndex(choiceProbability):
    randomNum = random.random()

    up = 0.0
    for ind, i in enumerate(choiceProbability):
        down = up
        up += i
        if randomNum > down and up > randomNum:
            return ind
    raise RuntimeError