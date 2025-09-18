import bisect
from rvgs import Exponential
class Model:
    def __init__(self, a, b, mean_cost):
        #Il numero di richieste concorrenti da la media per l'esponenziale che genera il tempo di completamento della richiesta
        self.a = a
        self.b = b

        self.mean_cost = mean_cost
        self.x = []  #cuncurrent request, salvo il tempo di completamento per rimuoverle quando sononoo

    def execute_request(self, now):
        #tolgo dalla lista le richieste già concluse
        idx = bisect.bisect_left(self.x,now)
        self.x=self.x[idx:]
        #il valore è preso dalla regressione del tempo di risposta quinndi il tempo di ccoda è già incluso

        mu = self.a*len(self.x)+self.b

        response_time = Exponential(mu)
        print("num req: "+str(len(self.x))+ " mu:"+str(mu)+" res time:"+str(response_time))
        request_time = response_time+now

        bisect.insort(self.x,request_time)

        cost = Exponential(self.mean_cost)
        return response_time, cost