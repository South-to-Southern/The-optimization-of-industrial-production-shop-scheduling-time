import numpy as np
import random
import copy
from individual import Individual


np.seterr(divide='ignore',invalid='ignore')

class ProbabilityModel:
    def __init__(self,MACHINE_NUM,JOB_NUM,eliteNum,maintenanceBound,DeteriorationProcessingTime,alpha,beta,ProcessingTime):
        self.MACHINE_NUM = MACHINE_NUM
        self.JOB_NUM = JOB_NUM
        self.eliteNum = eliteNum
        self.maintenanceBound = maintenanceBound
        self.DeteriorationProcessingTime = DeteriorationProcessingTime
        self.alpha = alpha
        self.beta = beta
        self.ProcessingTime = ProcessingTime
        self.modelOne = np.ones((MACHINE_NUM+1,JOB_NUM)) / (MACHINE_NUM)
        self.modelOne[-1,:] = 1/(MACHINE_NUM*10)
        self.modelOneNormaliza()

        self.modelTwo = np.ones((MACHINE_NUM,JOB_NUM+1,JOB_NUM))
        self.modelTwo[:, 0, :] = self.modelTwo[:, 0, :] / JOB_NUM
        self.modelTwo[:, 1:, :] = self.modelTwo[:, 1:, :] / (JOB_NUM-1)
        for i in range(JOB_NUM):
            self.modelTwo[:,i + 1,i] = 0

        # 为维护分配机器，如果落入最后一个虚拟机器则不必维护
        self.modelThree = np.ones((MACHINE_NUM+1)) / (MACHINE_NUM+1)

        # 其决定插入到哪个工件的前面
        self.modelFour = np.ones((MACHINE_NUM,JOB_NUM)) / JOB_NUM


    def getOffspring(self,POP_NUM):
        off = []
        for i in range(POP_NUM):
            off.append(self.makeIndividual())

        return off

    def makeIndividual(self):
        # t1 = time.time()

        # 先分组
        allocateMachine = [[] for i in range(self.MACHINE_NUM+1)]
        for i in range(self.JOB_NUM):
            probabilityArray = self.modelOne[:,i]
            enterMachine = self.roulette(probabilityArray)
            allocateMachine[enterMachine].append(i)

        # t2 = time.time()

        # 再排序
        # naiveChromosome = self.makeNaiveChromosome(allocateMachine)
        naiveChromosome = self.NewMakeNaiveChromosome(allocateMachine)

        # t3 = time.time()

        myMaintaince = [[] for i in range(self.MACHINE_NUM+1)]
        for i in range(self.maintenanceBound):
            enter = self.roulette(self.modelThree)
            if enter != self.MACHINE_NUM:
                myMaintaince[enter].append('@')
        # t4 = time.time()

        # 我们在得到排序的染色体之后，考虑将维护操作插入
        self.insertMaintaince(naiveChromosome,myMaintaince)

        # t5 = time.time()

        individual = Individual(naiveChromosome)

        # print('分组时间:',t2 - t1)
        # print('排序时间:',t3 - t2)
        # print('维护分组时间:',t4 - t3)
        # print('维护插入时间:',t5 - t4)
        # print('\n')

        return individual

    def insertMaintaince(self,naiveChromosome,myMaintaince):
        for ind0, machine in enumerate(naiveChromosome):
            # 虚拟机器和没有维护的机器都无需进入下面了
            if len(myMaintaince[ind0]) == 0:
                continue

            tmp = {} # 工件序号: 工件位置
            for ind1, job in enumerate(machine):
                if ind1 != 0 and machine[ind1] != '@':
                    tmp[job] = ind1

            # 如果可以插入的位子没有维护次数多，则在所有位置插入
            excursion = 0
            if len(tmp) <= len(myMaintaince[ind0]):
                for location in tmp.values():
                    naiveChromosome[ind0].insert(location+excursion,'@')
                    excursion += 1
            else:
                probabilityList = copy.deepcopy(self.modelFour[ind0,:])
                for ind, i in enumerate(probabilityList):
                    if ind not in tmp.keys():
                        probabilityList[ind] = 0
                probabilityList[:] = probabilityList[:] / probabilityList.sum()

                for _ in myMaintaince[ind0]:
                    lo = self.roulette(probabilityList) # 这个是工件序号
                    naiveChromosome[ind0].insert(naiveChromosome[ind0].index(lo),'@')
                    probabilityList[lo] = 0
                    probabilityList[:] = probabilityList[:]/probabilityList.sum()

    def makeNaiveChromosome(self,allocateMachine):
        naiveChromosome = [[] for i in range(self.MACHINE_NUM)]

        modelTwoCopy = copy.deepcopy(self.modelTwo)
        for ind0, machine in enumerate(modelTwoCopy):
            for job in range(self.JOB_NUM):
                if job not in allocateMachine[ind0]:
                    modelTwoCopy[ind0,:,job] = 0

        self.modelNormaliza(modelTwoCopy)

        for ind0,machine in enumerate(allocateMachine):
            if ind0 == len(allocateMachine)-1:
                break
            for ind1,job in enumerate(machine):
                if naiveChromosome[ind0]:
                    prevJob = naiveChromosome[ind0][-1]
                    probabilityArray = modelTwoCopy[ind0,prevJob+1,:]
                    enterJob = self.roulette(probabilityArray)
                    naiveChromosome[ind0].append(enterJob)
                    modelTwoCopy[ind0,:,enterJob] = 0
                    self.modelNormaliza(modelTwoCopy)
                else:
                    # 如果为空
                    probabilityArray = modelTwoCopy[ind0,0,:]
                    enterJob = self.roulette(probabilityArray)
                    naiveChromosome[ind0].append(enterJob)
                    modelTwoCopy[ind0,:,enterJob] = 0
                    self.modelNormaliza(modelTwoCopy)

        naiveChromosome.append(copy.deepcopy(allocateMachine[-1]))

        return naiveChromosome

    def NewMakeNaiveChromosome(self,allocateMachine):
        naiveChromosome = []

        modelTwoCopy = copy.deepcopy(self.modelTwo)

        for ind0,machine in enumerate(allocateMachine):
            if ind0 == len(allocateMachine)-1:
                break

            naiveChromosome.append(self.probabilitySort(modelTwoCopy[ind0],machine))

        naiveChromosome.append(copy.deepcopy(allocateMachine[-1]))

        return naiveChromosome

    def probabilitySort(self,machineProbability,JobList):
        if len(JobList) == 0:
            return []

        sortedList = []

        jobLength = len(JobList)
        while len(sortedList) < jobLength - 1:
            if len(sortedList) == 0:
                probabilityArray = machineProbability[0,JobList]
                enterJob = self.newRoulette(probabilityArray,JobList)
                sortedList.append(enterJob)
                JobList.remove(enterJob)
            else:
                probabilityArray = machineProbability[sortedList[-1]+1,JobList]
                enterJob = self.newRoulette(probabilityArray, JobList)
                sortedList.append(enterJob)
                JobList.remove(enterJob)

        sortedList.append(JobList[0])

        return sortedList

    def newRoulette(self,probabilityArray,JobList):
        randomNum = random.uniform(0.0, probabilityArray.sum())

        up = 0.0
        for ind, i in enumerate(probabilityArray):
            down = up
            up += i
            if randomNum > down and up > randomNum:
                return JobList[ind]
        raise RuntimeError

    def modelNormaliza(self,model):
        for machine in model:
            for line in machine:
                line[:] = line / line.sum()

    def roulette(self,probabilityArray):
        randomNum = random.random()

        up = 0.0
        for ind, i in enumerate(probabilityArray):
            down = up
            up += i
            if randomNum > down and up > randomNum:
                return ind
        raise RuntimeError

    def modelTwoUpdate(self,chromosome):
        add = np.zeros((self.MACHINE_NUM,self.JOB_NUM+1,self.JOB_NUM))
        addModelFour = np.zeros((self.MACHINE_NUM,self.JOB_NUM))
        for ind0, machine in enumerate(chromosome):
            if ind0 == len(chromosome) -4:
                break
            for ind1, i in enumerate(machine):
                if machine[ind1] == '@':
                    continue

                if machine[ind1+1]== '@':
                    addModelFour[ind0][machine[ind1+2]] = 1
                    continue

                if ind1 == 0:
                    add[ind0][0][i] = 1
                else:
                    add[ind0][machine[ind1+2]][i] = 1

        lower = addModelFour.min() / (self.eliteNum * 2)
        addModelFour = addModelFour * lower
        self.modelFour += addModelFour
        self.modelFourNormaliza(self.modelFour)


        lowerNum = self.modelTwo.max() / (self.eliteNum * 2)
        for i in self.modelTwo[0][0]:
            if i < lowerNum:
                lowerNum = i
        lowerNum = lowerNum

        add = add * lowerNum
        self.modelTwo += add

        self.modelTwoNormaliza()


    def modelTwoNormaliza(self):
        for machine in self.modelTwo:
            for line in machine:
                line[:] = line / line.sum()

    def modelOneUpdate(self,chromosome):
        add = np.zeros((self.MACHINE_NUM+1,self.JOB_NUM))
        addModelThree = np.zeros(self.MACHINE_NUM+1)
        maintenanceCount = 0
        for ind0, machine in enumerate(chromosome):
            for ind1, i in enumerate(machine):
                if i == '@':
                    addModelThree[ind0] += 1
                    maintenanceCount += 1
                else:
                    add[ind0][i] = 1

        addModelThree[-1] = self.maintenanceBound - maintenanceCount
        lower = self.modelThree.min() / (self.eliteNum)
        addModelThree = addModelThree * lower
        self.modelThree += addModelThree
        self.modelThreeNormaliza()

        # 非最后一行的最小数 / 精英个体的数目
        lowerNum = self.modelOne[:-1,:].min() / (self.eliteNum)
        add = add * lowerNum

        self.modelOne += add

        self.modelOneNormaliza()

    def modelOneNormaliza(self):
        for i in range(self.modelOne.shape[1]):
            self.modelOne[:,i] = self.modelOne[:,i]/self.modelOne[:,i].sum()

    def modelThreeNormaliza(self):
        self.modelThree[:] = self.modelThree[:] / self.modelThree.sum()

    def modelFourNormaliza(self,modelFour):
        for machine in modelFour:
            machine[:] = machine[:] / machine.sum()

# ProcessingTime = np.load('./example/normalProcessingTime.npy')
# DeteriorationProcessingTime = np.load('./example/deteriorationProcessingTime.npy')
# alpha = np.load('./example/alpha.npy')
# beta = np.load('./example/beta.npy')
# p = ProbabilityModel(2,4,10,1,DeteriorationProcessingTime,alpha,beta,ProcessingTime)
# # print(p.modelOne)
#
# c = [[0,1,3],[2],[]]
# p.makeIndividual()
