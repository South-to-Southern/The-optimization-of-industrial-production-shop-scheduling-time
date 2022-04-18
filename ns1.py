import numpy as np

def ns1(chromosome,DeteriorationProcessingTime,beta,ProcessingTime):
    for ind0,machine in enumerate(chromosome):
        if len(machine) <= 2 or ind0 == len(chromosome) - 1:
            continue

        degree1 = -1
        for ind1 in range(len(machine) - 1):
            if machine[ind1] == '@':
                degree1 = -1
                continue

            degree1 += 1
            degree2 = degree1
            label = False
            for ind2 in range(ind1+1,len(machine)):

                job2 = machine[ind2]

                if job2 == '@':
                    degree2 = -1
                    if '@' not in machine[ind2+1:]:
                        label = True
                    continue

                degree2 += 1

                job1 = machine[ind1]

                # print('job1',job1,degree1)
                # print(job2,degree2,label)

                timeDifference = 0
                if label: # job1与job2不在同一个组，并且job2是最后一组
                    originalTime = (1 + beta[ind0]) * (DeteriorationProcessingTime[ind0][job1][degree1] + ProcessingTime[ind0][job1]) + \
                                   DeteriorationProcessingTime[ind0][job2][degree2] + ProcessingTime[ind0][job2]
                    exchangedTime = (1 + beta[ind0]) * (DeteriorationProcessingTime[ind0][job2][degree1] + ProcessingTime[ind0][job2]) + \
                                    DeteriorationProcessingTime[ind0][job1][degree2] + ProcessingTime[ind0][job1]
                    timeDifference = originalTime - exchangedTime
                else: # 只用判断恶化时间增长前与增长后的差值即可判断
                    originalTime = DeteriorationProcessingTime[ind0][job1][degree1] + DeteriorationProcessingTime[ind0][job2][degree2]
                    exchangedTime = DeteriorationProcessingTime[ind0][job2][degree1] + DeteriorationProcessingTime[ind0][job1][degree2]
                    timeDifference = originalTime - exchangedTime
                if timeDifference > 0:
                    chromosome[ind0][ind1] = job2
                    chromosome[ind0][ind2] = job1
                    return 0

    return 1

# def evaluateOne(chromosome):
#     obj = 0
#     for ind0, machine in enumerate(chromosome):
#         if ind0 == len(chromosome) - 1:
#             item_obj = len(machine) * rejectionPenalty
#         else:
#             degree = -1
#             item_obj = 0
#             tmp = 0
#             for ind1, i in enumerate(machine):
#                 if i != '@':
#                     degree += 1
#                     tmp += (ProcessingTime[ind0][i] + DeteriorationProcessingTime[ind0][i][degree])
#                     item_obj += (ProcessingTime[ind0][i] + DeteriorationProcessingTime[ind0][i][degree])
#                 else:
#                     degree = -1
#                     item_obj += tmp * beta[ind0] + alpha[ind0]
#                     tmp = 0
#         obj += item_obj
#
#     return obj
#
# rejectionPenalty = 25
# alpha = np.load('./example/alpha.npy')
# ProcessingTime = np.load('./example/normalProcessingTime.npy')
# DeteriorationProcessingTime = np.load('./example/deteriorationProcessingTime.npy')
# beta = np.load('./example/beta.npy')
# c= [[9, 1, 10, 5], [17, 11, 19, 2], [12, 4, '@', 16, 18, 0], [15, 7, 3, '@', 6, 13, 14, 8], []]
# print(c,evaluateOne(c))
# ns1(c,DeteriorationProcessingTime,beta,ProcessingTime)
# print(c,evaluateOne(c))


