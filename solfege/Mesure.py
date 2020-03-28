#!/usr/bin/env python3
# -*- coding: utf-8 -*-



class Mesure:
    def __init__(self, **kwargs):
        self.parent = None
        self.nbTps = 3
        self.nbSTps = 2
        self.typeMes = str()
        self.typeTps = str()
        self.lisMes = list()
        self.reset(**kwargs)

    def reset(self, **kwargs):
        compt = 0
        self.nbTps = kwargs.get('nbTps', self.nbTps)
        self.nbSTps = kwargs.get('nbSTps', self.nbSTps)
        self.lisMes = list()

        if self.nbTps % 3 == 0 :
            self.typeMes = "ternaire"
        elif self.nbTps % 2 == 0 :
            self.typeMes = "binaire"
        else:
            self.typeMes = ""
        if self.nbSTps % 3 == 0 :
            self.typeTps = "ternaire"
        elif self.nbSTps % 2 == 0 :
            self.typeTps = "binaire"
        else:
            self.typeTps = ""

        for i in range(self.nbTps):
            if  self.typeMes == "binaire" :
                if i%2 == 0 :
                    forceT = "F"
                else :
                    forceT = "f"
            elif  self.typeMes == "ternaire" :
                if i%3 == 0 :
                    forceT = "F"
                else :
                    forceT = "f"
            else:
                if i == 0 :
                    forceT = "F"
                else:
                    forceT = "f"

            for j in range(self.nbSTps):
                if self.typeTps == "binaire" :
                    if j%2 == 0 :
                        forceST = "F"
                    else :
                        forceST = "f"
                elif self.typeTps == "ternaire" :
                    if j%3 == 0 :
                        forceST = "F"
                    else :
                        forceST = "f"
                else:
                    if j == 0:
                        forceST = "F"
                    else :
                        forceST = "f"

                self.lisMes.append((compt,i,forceT,j,forceST))
                compt = compt + 1

    def info(self):
        for i in range(len(self.lisMes)):
            print(self.lisMes[i])
