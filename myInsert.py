# 将pop中的前ReservedNum个最优解插入到offspring中，并保持种群数目不变
def myInsert(offspring,pop,ReservedNum):
    for i in range(ReservedNum):
        offspring.pop()

    for i in range(ReservedNum):
        for ind,j in enumerate(offspring):
            if pop[i].fitness < j.fitness:
                offspring.insert(ind,pop[i])
                break

    if len(offspring) != len(pop):
        for i in range(len(pop) - len(offspring)):
            offspring.append(pop[i])