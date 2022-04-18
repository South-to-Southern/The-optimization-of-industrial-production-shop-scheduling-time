import numpy as np
import random
import time
import matplotlib.pyplot as plt
import copy
import sys

MACHINE_NUM = 3
JOB_NUM = 15
maintenanceBound = 2
rejectionPenalty = 25
GENERATION = 2000
eliteRatio = 0.4
crossoverRatio=0.6
mutationRatio = 0.06
POP_NUM = 50
ReservedNum = 0
# ProcessingTime = np.load('./example/normalProcessingTime.npy')
# DeteriorationProcessingTime1 = np.load('./example/deteriorationProcessingTime.npy')
# alpha = np.load('./example/alpha.npy')
# beta1 = np.load('./example/beta.npy')
ProcessingTime = np.load('normalProcessingTime.npy')
DeteriorationProcessingTime = np.load('deteriorationProcessingTime.npy')
alpha = np.load('alpha.npy')
beta = np.load('beta.npy')
# print(DeteriorationProcessingTime1)
# print(beta1)

from initPop import getPopulation
from mySort import mySort
from myInsert import myInsert
from probabilityModel import ProbabilityModel
from neighborhoodSearch import neighborhoodSearch
from mutate import mutate
from crossover import crossover
from getElitePop import getElitePop

# 加载概率模型
pModel = ProbabilityModel(MACHINE_NUM=MACHINE_NUM,JOB_NUM=JOB_NUM,eliteNum=POP_NUM*eliteRatio,
                          maintenanceBound=maintenanceBound,DeteriorationProcessingTime=DeteriorationProcessingTime,
                          alpha=alpha,beta=beta,ProcessingTime=ProcessingTime)


# 定义目标函数
def evaluateOne(chromosome):
    obj = 0
    for ind0, machine in enumerate(chromosome):
        if ind0 == len(chromosome) - 1:
            item_obj = len(machine) * rejectionPenalty
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
                    item_obj += tmp * beta[ind0] + alpha[ind0]
                    tmp = 0
        obj += item_obj

    return obj


# 定义主函数
def EDA():
    pic = []

    totalTime = time.perf_counter()

    # 生成初始化种群
    pop = getPopulation(MACHINE_NUM,JOB_NUM,maintenanceBound,
                        POP_NUM,rejectionPenalty,ProcessingTime,
                        DeteriorationProcessingTime,alpha,beta)

    # 计算初代种群的适应度
    for i in pop:
        i.fitness = evaluateOne(i.chromosome)

    # 迭代的代数
    generation = 0
    pop[:] = mySort(pop)

    while generation < GENERATION:
        generation += 1
        print('当前第 %d 代:' %generation)

        for index,ind in enumerate(pop):
            if index < len(pop) * eliteRatio:
                pModel.modelOneUpdate(ind.chromosome)
                pModel.modelTwoUpdate(ind.chromosome)


        offspring = pModel.getOffspring(POP_NUM)

        for ind in offspring:
            neighborhoodSearch(ind.chromosome,DeteriorationProcessingTime,beta,ProcessingTime)

        for individual in offspring:
            if random.random() < mutationRatio:
                mutate(individual,JOB_NUM,maintenanceBound) # 这里的变异需要在个体本身上去改变

        for i in offspring:
            i.fitness = evaluateOne(i.chromosome)

        offspring[:] = mySort(offspring)

        # 保留每一代的最优值
        myInsert(offspring,pop,ReservedNum)

        pop[:] = offspring[:]

        print("  Min %s" % pop[0].fitness)
        print("  Mid %s" % pop[POP_NUM//2].fitness)
        print("  Max %s" % pop[-1].fitness)
        print("\n")

        if generation % 1 == 0:
            pic.append(pop[0].fitness)

    print('totalTime',time.perf_counter() - totalTime)
    return pop[0],pic


p,draw = EDA()
print(p.chromosome)
print(evaluateOne(p.chromosome))
plt.scatter([i for i in range(len(draw))],draw)
plt.show()
np.set_printoptions(threshold=np.inf)
# print(pModel.modelOne,'\n')
# print(pModel.modelTwo,'\n')
# print(pModel.modelThree,'\n')
# print(pModel.modelFour,'\n')
# EDA [[1, 11, 9, 10], [19, 6, '@', 2, 8, 17, 13], [12, 0, '@', 16, 18, 14, 4], [5, 3, 7, 15], []]  Min 169.5
# GA [[1, 11, 9, 10], [2, 19, 17], [12, 0, '@', 16, 18, 14, 4], [15, 5, 7, '@', 3, 6, 13, 8], []] Min 166.6

# [[1, 11, 9, 10], [19, 6, 17], [2, 0, '@', 16, 18, 12, 4], [5, 7, 3, '@', 14, 8, 13, 15], []]
# [[1, 11, 9, 10], [2, 19, 17, 8], [12, 0, '@', 16, 18, 4], [5, 7, 3, '@', 14, 6, 13, 15], []]
