#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from multiprocessing import Process, freeze_support, Queue
import solfege as SF

class IGraph:
    
    def __init__(self):
        self.motif = SF.Motif() ##############################################
        
        self.job = Process(target=self.ModifMotif,  args=(' ',), daemon=True)
        freeze_support()
        self.qSolf = Queue()

        self.busy = 0
    
    def ModifMotif(self, comm):
        exec(comm)
        self.qSolf.put((self.motif))####################################

    def commandeMM(self, commande):
        self.getResultMM()
        self.busy = 1
        self.job = Process(target=self.ModifMotif,  args=(commande,), daemon=True)
        self.job.start()


    def getResultMM(self):
        if self.busy == 1:
            self.job.join()
            self.job.terminate()
            while not self.qSolf.empty() :
                mess = self.qSolf.get()
                self.motif = mess
            self.busy=0
            


IG = IGraph()


print(IG.motif.nomFr)
millisEnv = time.time()

IG.commandeMM("IG.motif.reset(nomFr = 'ré', alt = '', nbTps = 2)")####################################
# pendant ce temps on fait d'autres trucs
IG.getResultMM()

print((time.time() - millisEnv ) * 1000 )
print(IG.motif.nomFr)
    
