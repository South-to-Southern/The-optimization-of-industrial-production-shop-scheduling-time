import random
from individual import Individual
import copy

def crossover(elitePop,crossoverRatio,JOB_NUM,maintenanceBound):
    offspring = []

    indexTable  = [i for i in range(len(elitePop))]

    while indexTable:
        index1 = random.choice(indexTable)
        indexTable.remove(index1)
        index2 = random.choice(indexTable)
        indexTable.remove(index2)

        parent1 = elitePop[index1]
        parent2 = elitePop[index2]

        if random.random() < crossoverRatio:
            for _ in range(2):
                off = []
                for i in range(len(parent1.chromosome)):
                    ind = random.choice([1,2])
                    if ind == 1:
                        off.append(copy.deepcopy(parent1.chromosome[i]))
                    else:
                        off.append(copy.deepcopy(parent2.chromosome[i]))
                removeSurplus(off)
                insertAbsence(off,JOB_NUM)
                adjustMaintaince(off,maintenanceBound)


                offspring.append(Individual(off))

        else:
            offspring.append(copy.deepcopy(parent1))
            offspring.append(copy.deepcopy(parent2))

    return offspring


def removeSurplus(off):
    job_location = {}

    for index0,machine in enumerate(off):
        for index1,job in enumerate(machine):
            if job == '@':
                continue

            if job not in job_location.keys():
                job_location[job] = [index0]
            else:
                job_location[job].append(index0)

    for k,v in job_location.items():
        if len(v) == 1:
            continue

        ind = random.choice(v)

        off[ind].remove(k)

    return off

def insertAbsence(off,JOB_NUM):
    absenceJob = [i for i in range(JOB_NUM)]

    for machine in off:
        for job in machine:
            if job != '@':
                absenceJob.remove(job)

    for job in absenceJob:
        choiceMachine = random.choice([i for i in range(len(off) - 1)])

        if len(off[choiceMachine]) == 0:
            off[choiceMachine].append(job)
        else:

            location = random.choice([i for i in range(len(off[choiceMachine]))])

            off[choiceMachine].insert(location, job)


def adjustMaintaince(off,maintenanceBound):
    for ind0,machine in enumerate(off):
        while len(off[ind0]) > 0 and off[ind0][0] == '@':
            off[ind0].remove('@')

        while len(off[ind0]) > 0 and off[ind0][-1] == '@':
            off[ind0].pop()

        for ind1,i in enumerate(machine):
            if i == '@' and machine[ind1+1] == '@':
                off[ind0].pop(ind1)

    count = 0
    for ind0,machine in enumerate(off):
        for ind1,i in enumerate(machine):
            if i == '@':
                count += 1

    if count > maintenanceBound:
        for i in range(count - maintenanceBound):
            while True:
                machineIndex = random.choice([i for i in range(len(off)-1)])

                if '@' in off[machineIndex]:
                    off[machineIndex].remove('@')
                    break