from ns1 import ns1
from ns2 import ns2
from ns3 import ns3

def neighborhoodSearch(chromosome,DeteriorationProcessingTime,beta,ProcessingTime):
    count = 0
    while True:
        count += 1
        mark = 0

        mark += ns1(chromosome,DeteriorationProcessingTime,beta,ProcessingTime)
        # mark += ns2(chromosome, DeteriorationProcessingTime, beta, ProcessingTime)
        # mark += ns3(chromosome, DeteriorationProcessingTime, beta, ProcessingTime)
        if count <= 10:
            break

        if mark > 0:
            continue
        else:
            break