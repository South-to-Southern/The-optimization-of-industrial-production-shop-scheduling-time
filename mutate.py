import random
from individual import Individual

def mutate(individual,JOB_NUM,maintenanceBound):
    chromosome = individual.chromosome
    # 两个工件之间互换
    # 一个工件插入另一个工件之后
    # 删除一次维护
    # 随机插入一次维护
    randomNum = random.random()

    if randomNum <= 0.5:
        exchange(chromosome,JOB_NUM)
    elif 0.5 < randomNum and randomNum <= 1:
        myInsert(chromosome,JOB_NUM)


# def mutate(individual,JOB_NUM,maintenanceBound):
#     chromosome = individual.chromosome
#     # 两个工件之间互换
#     # 一个工件插入另一个工件之后
#     # 删除一次维护
#     # 随机插入一次维护
#     randomNum = random.random()
#
#     if randomNum <= 0.5:
#         for i in range(int(JOB_NUM/2)):
#             exchange(chromosome,JOB_NUM)
#     else:
#         for i in range(int(JOB_NUM / 2)):
#             myInsert(chromosome,JOB_NUM)


def exchange(chromosome,JOB_NUM):
    indexList = [i for i in range(JOB_NUM)]
    job1 = random.choice(indexList)
    indexList.remove(job1)
    job2 = random.choice(indexList)

    for ind0,machine in enumerate(chromosome):
        for ind1,job in enumerate(machine):
            if job == job2:
                chromosome[ind0][ind1] = job1
            if job == job1:
                chromosome[ind0][ind1] = job2

def myInsert(chromosome,JOB_NUM):
    indexList = [i for i in range(JOB_NUM)]
    job1 = random.choice(indexList)
    indexList.remove(job1)
    job2 = random.choice(indexList)

    location = None
    for ind0,machine in enumerate(chromosome):
        for ind1,job in enumerate(machine):
            if job == job1:
                if ind1 == len(machine) - 1 and machine[ind1-1] == '@':
                    chromosome[ind0].pop()
                    chromosome[ind0].pop()
                    break
                if ind1 == 0 and len(machine) >= 2 and machine[ind1+1] == '@':
                    chromosome[ind0].remove(job1)
                    chromosome[ind0].remove('@')
                    break

                chromosome[ind0].pop(ind1)

    for ind0,machine in enumerate(chromosome):
        for ind1,job in enumerate(machine):
            if job == job2:
                location = (ind0,ind1)

    chromosome[location[0]].insert(location[1],job1)

def deleteMaintaince(chromosome):
    index = random.choice([i for i in range(len(chromosome)-1)])

    if '@' in chromosome[index]:
        chromosome[index].remove('@')

def insertMaintaince(chromosome,maintenanceBound):
    count = 0
    for ind0,machine in enumerate(chromosome):
        for ind1,job in enumerate(machine):
            if job == '@':
                count += 1

    locations = []
    if count < maintenanceBound:
        for ind0, machine in enumerate(chromosome):
            for ind1, job in enumerate(machine):
                if ind1 != 0 and job != '@' and machine[ind1-1] != '@' and ind0 != len(chromosome)-1:
                    locations.append((ind0,ind1))
    if len(locations) != 0:
        location = random.choice(locations)
    else:
        location = None
    if location:
        chromosome[location[0]].insert(location[1],'@')


def getPunishment(chromosome,JOB_NUM):
    indexJob = random.choice([i for i in range(JOB_NUM)])

    for ind0,machine in enumerate(chromosome):
        for ind1,job in enumerate(machine):
            if job == indexJob:

                if ind1 == len(machine) - 1 and machine[ind1-1] == '@':
                    chromosome[ind0].pop()
                    chromosome[ind0].pop()
                    break
                if ind1 == 0 and len(machine) >= 2 and machine[ind1+1] == '@':
                    chromosome[ind0].remove(indexJob)
                    chromosome[ind0].remove('@')
                    break

                chromosome[ind0].pop(ind1)
                break

    chromosome[-1].append(indexJob)