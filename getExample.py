import numpy as np
import random

def getnormalProcessingTime(machineNum,jobNum):
    normalProcessingTime = np.random.randint(1,20,(machineNum,jobNum))

    np.save('./example/normalProcessingTime.npy',normalProcessingTime)

def getDeteriorationProcessingTime(machineNum,jobNum):
    deteriorationProcessingTime = np.zeros((machineNum,jobNum,jobNum))

    for m in deteriorationProcessingTime:
        for j in m:
            for ind,lo in enumerate(j):
                if ind == 0:
                    continue
                j[ind] = j[ind-1] + random.randint(1,3) * ind

    np.save('./example/deteriorationProcessingTime.npy', deteriorationProcessingTime)

def maintain_alpha(machineNum):
    alpha = np.random.randint(5,15,(machineNum))
    # alpha = np.random.randint(5, 15, (machineNum)) /10
    np.save('./example/alpha.npy',alpha)

def maintain_beta(machineNum):
    beta = np.random.randint(5,9,(machineNum)) / 10
    # beta = np.random.randint(5, 9, (machineNum)) / 100
    np.save('./example/beta.npy',beta)

def getExample(machineNum,jobNum):
    getnormalProcessingTime(machineNum,jobNum)
    getDeteriorationProcessingTime(machineNum,jobNum)
    maintain_alpha(machineNum)
    maintain_beta(machineNum)

getExample(4,20) #第一个参数为机器数目，第二个参数为工件数目。






