import numpy as np
import random
from individual import Individual

def getPopulation(MACHINE_NUM,JOB_NUM,maintenanceBound,
                        POP_NUM,rejectionPenalty,ProcessingTime,
                        DeteriorationProcessingTime,alpha,beta):
    population = []
    for i in range(POP_NUM):
        chromosome = [[] for i in range(MACHINE_NUM+1)]

        jobs = [i for i in range(JOB_NUM)]
        while jobs:
            enterJob = random.choice(jobs)
            jobs.remove(enterJob)
            bestMachine = findBestLocation(chromosome,enterJob,rejectionPenalty,
                                           ProcessingTime,DeteriorationProcessingTime)
            chromosome[bestMachine].append(enterJob)

        insertMaintaince(chromosome,maintenanceBound,alpha,beta,DeteriorationProcessingTime,ProcessingTime)

        individual = Individual(chromosome)
        population.append(individual)

    return population

def insertMaintaince(chromosome,maintenanceBound,alpha,beta,DeteriorationProcessingTime,ProcessingTime):
    for i in range(maintenanceBound):

        arrayEarnings = []
        arrayLocation = []
        for ind0,machine in enumerate(chromosome):
            for ind1,i in enumerate(machine):

                if ind1 != 0  and machine[ind1] != '@' and ind0 != len(chromosome)-1 and machine[ind1-1] != '@':

                    arrayLocation.append((ind0,ind1))
                    arrayEarnings.append(reduceDeterioration(chromosome,(ind0,ind1),DeteriorationProcessingTime) - maintainceCost(chromosome,(ind0,ind1),alpha,beta,ProcessingTime,DeteriorationProcessingTime))

        if len(arrayEarnings) == 0:
            break

        if max(arrayEarnings) > 0:
            l_index = arrayEarnings.index(max(arrayEarnings))
            l = arrayLocation[l_index]
            chromosome[l[0]].insert(l[1],'@')
        else:
            break


def reduceDeterioration(chromosome,location,DeteriorationProcessingTime):
    res = 0

    deteriorationDegree = findDeteriorationDegree(chromosome, location)

    for i in range(location[1],len(chromosome[location[0]])):
        if chromosome[location[0]][i] == '@':
            break
        res += DeteriorationProcessingTime[location[0]][chromosome[location[0]][i]][deteriorationDegree] - \
               DeteriorationProcessingTime[location[0]][chromosome[location[0]][i]][deteriorationDegree - 1]
        deteriorationDegree += 1

    return res

def findDeteriorationDegree(chromosome, location):
    degree = -1
    for i in range(location[1],-1,-1):
        if chromosome[location[0]][i] == '@':
            break
        degree += 1

    return degree

def maintainceCost(chromosome,location,alpha,beta,ProcessingTime,DeteriorationProcessingTime):
    res = 0

    deteriorationDegree = findDeteriorationDegree(chromosome, location)
    for i in range(location[1],-1,-1):
        if chromosome[location[0]][i] == '@':
            break
        res += (ProcessingTime[location[0]][chromosome[location[0]][i]]
                + DeteriorationProcessingTime[location[0]][chromosome[location[0]][i]][deteriorationDegree])
        deteriorationDegree -= 1

    return res*beta[location[0]] + alpha[location[0]]


def findBestLocation(chromosome,enterJob,rejectionPenalty,ProcessingTime,
                        DeteriorationProcessingTime):
    tmp = []
    for machine,i in enumerate(chromosome):
        if machine == len(chromosome) - 1:
            tmp.append(rejectionPenalty)
        elif i:
            tmp.append(ProcessingTime[machine][enterJob]
                       + DeteriorationProcessingTime[machine][enterJob][len(i)])
        else:
            tmp.append(ProcessingTime[machine][enterJob]
                       + DeteriorationProcessingTime[machine][enterJob][0])

    return tmp.index(min(tmp))

# ProcessingTime = np.load('./example/normalProcessingTime.npy')
# DeteriorationProcessingTime = np.load('./example/deteriorationProcessingTime.npy')
# alpha = np.load('./example/alpha.npy')
# beta = np.load('./example/beta.npy')
# pop = getPopulation(4,20,2,10,25,ProcessingTime,DeteriorationProcessingTime,alpha,beta)
#
# for i in pop:
#     print(i.chromosome)





