#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from multiprocessing import Process, freeze_support, Queue
import solfege as SF

class IGraph:
    
    def __init__(self):
        self.motif = SF.Motif() ##############################################
        
        self.job = {}
        freeze_support()
        self.qSolf = Queue()
    
    def ModifMotif(self, comm):
        exec(comm)
        self.qSolf.put((comm, self.motif))####################################

    def commandeMM(self, commande):
        self.job[commande] = Process(target=IG.ModifMotif,  args=(commande,), daemon=True)
        self.job[commande].start()
        
    def getQSolf(self):
        if not self.qSolf.empty() :
            mess = self.qSolf.get()
            self.motif = mess[1]##############################################
            self.job[mess[0]].join()
            self.job[mess[0]].terminate()
            del self.job[mess[0]]

IG = IGraph()
print(IG.motif.nomFr)
IG.commandeMM("IG.motif.reset(nomFr = 'ré', alt = '', nbTps = 2)")

time.sleep(0.5)

IG.getQSolf()
print(IG.motif.nomFr)
    
