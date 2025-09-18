from random import randint

import heapq

import numpy as np

from simulatore.Model import Model
from simulatore.rngs import plantSeeds
from simulatore.rvgs import Exponential

N_MODELS = 2
INTERARRIVAL_TIMES = [0.05]
CLIENT_TYPES = 1

START = 0.0
STOP = 10000.0

class ClientType:
    FREE = 0
    PREMIUM = 1
class Arrival:
    def __init__(self, clientType, time):
        self.clientType = clientType
        self.time = time
    def __lt__(self, other):
        return self.time<other.time
def run_simulation(seed = 123456):
    plantSeeds(seed)
    current_time = 0
    n_arrivals = np.zeros(CLIENT_TYPES) #numero di arrivi per tipo cliente
    mean_time = np.zeros(CLIENT_TYPES)
    cost = np.zeros(CLIENT_TYPES)
    total_cost = 0
    models = [Model(0.08896,3.696 , 0), Model(0.08896, 10, 0)]
    arrivals_interval = [20,0.5]  #frequeenza arrivi per tipo di clienti

    eventList = [] #mantirne arrivi ordinati
    for i in range(CLIENT_TYPES): #crea una prima richiesta per ogni classe
        a = Arrival(i,current_time+Exponential(arrivals_interval[i]))
        heapq.heappush(eventList,a)

    while current_time < STOP:
        a = heapq.heappop(eventList)
        ct = a.clientType
        heapq.heappush(eventList,Arrival(ct,current_time+Exponential(arrivals_interval[ct])))
        n_arrivals[ct] += 1
        current_time = a.time

        # policy
        mod = randint(0,len(models)-1) #TODO mettere che prende le probabilità in base alla polici e tipo cliente
        response_time, c = models[mod].execute_request(current_time)
        mean_time[ct] += response_time
        cost[ct] += c
        total_cost += c
    print(mean_time[0]/n_arrivals[0])

run_simulation()