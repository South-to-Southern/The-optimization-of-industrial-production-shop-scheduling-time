import numpy as np
import copy
ProcessingTime = np.load('D:/课程资料/smartcity_paper/programming code/programming code/GA/example/normalProcessingTime.npy')
DeteriorationProcessingTime = np.load('D:/课程资料/smartcity_paper/programming code/programming code/GA/example/deteriorationProcessingTime.npy')
alpha = np.load('D:/课程资料/smartcity_paper/programming code/programming code/GA/example/alpha.npy')
beta = np.load('D:/课程资料/smartcity_paper/programming code/programming code/GA/example/beta.npy')

def evaluateMachine(machine,ind0):
    degree = -1
    item_obj = 0
    tmp = 0
    for ind1, i in enumerate(machine):
        if i != '@':
            degree += 1
            tmp += (ProcessingTime[ind0][i] + DeteriorationProcessingTime[ind0][i][degree])
            item_obj += (ProcessingTime[ind0][i] + DeteriorationProcessingTime[ind0][i][degree])
        else:
            degree = -1
            item_obj += tmp * beta[ind0]
            tmp = 0
    return item_obj

def ns2(chromosome,DeteriorationProcessingTime,beta,ProcessingTime):
    for i in range(len(chromosome)):
        if len(chromosome[i])>2:
            for j in range(len(chromosome[i])):
                for k in range(len(chromosome[i]) - 1, -1, -1):
                    if k-j>=2:
                        if j!='@'and k!='@':
                        #     job1=chromosome[i][j]
                        #     job2=chromosome[i][k]
                        #     job3=chromosome[i][j+1]
                            timeDifference = 0
                            # if '@'in chromosome[i] and j+1<chromosome[i].index('@')<k:
                            #     originalTime=(1 + beta[i]) * (DeteriorationProcessingTime[i][job1][j] + ProcessingTime[i][job1]+DeteriorationProcessingTime[i][job3][j+1] + ProcessingTime[i][job3])
                            #     exchangedTime=(1 + beta[i]) * ((DeteriorationProcessingTime[i][job3][j] + ProcessingTime[i][job3])+DeteriorationProcessingTime[i][job1][k-chromosome[i].index('@')+1] + ProcessingTime[i][job1]
                            #     timeDifference = originalTime - exchangedTime
                            # else:
                            #     originalTime = DeteriorationProcessingTime[ind0][job1][degree1] +
                            #                    DeteriorationProcessingTime[ind0][job2][degree2]
                            #     exchangedTime = DeteriorationProcessingTime[ind0][job2][degree1] +
                            #                     DeteriorationProcessingTime[ind0][job1][degree2]
                            #     timeDifference = originalTime - exchangedTime
                            originalTime = evaluateMachine(chromosome[i],i)
                            temp1 = chromosome[i][j]
                            C1 = copy.deepcopy(chromosome)
                            del C1[i][j]
                            C1[i].insert(k, temp1)
                            exchangedTime = evaluateMachine(C1[i],i)
                            timeDifference = originalTime - exchangedTime
                            if timeDifference > 0:
                                temp1 = chromosome[i][j]
                                del chromosome[i][j]
                                chromosome[i].insert(k, temp1)
                                return 0
    return 1

def evaluateOne(chromosome):
    obj = 0
    for ind0, machine in enumerate(chromosome):
        if ind0 == len(chromosome) - 1:
            item_obj = len(machine) * 25
        else:
            degree = -1
            item_obj = 0
            tmp = 0
            for ind1, i in enumerate(machine):
                if i != '@':
                    degree += 1
                    tmp += (ProcessingTime[ind0][i] + DeteriorationProcessingTime[ind0][i][degree])
                    item_obj += (ProcessingTime[ind0][i] + DeteriorationProcessingTime[ind0][i][degree])
                else:
                    degree = -1
                    item_obj += tmp * beta[ind0]
                    tmp = 0
        obj += item_obj

    return obj

# rejectionPenalty = 25
# ProcessingTime = np.load('./example/normalProcessingTime.npy')
# DeteriorationProcessingTime = np.load('./example/deteriorationProcessingTime.npy')
# alpha = np.load('./example/alpha.npy')
# beta = np.load('./example/beta.npy')
# c= [[9, 1, 10, 5], [17, 2, 19, 11], [12, 4, '@', 16, 18, 0], [15, 7, 3, '@', 6, 13, 14, 8], []]
# print(c,evaluateOne(c))
# ns2(c,DeteriorationProcessingTime,beta,ProcessingTime)
# print(c,evaluateOne(c))


