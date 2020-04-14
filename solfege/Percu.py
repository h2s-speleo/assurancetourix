#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import random

class Percu:
    def __init__(self, parent):
        self.parent = parent
        self.nbMesure = 2
        self.listeVoix = list()
        self.resListeRang()

    def resListeRang(self):
        mesure = self.parent.mesure.lisMes
        self.listeRang = list()
        for i in range(self.nbMesure):
            for j in range(len(mesure)):        
                if mesure[j][2] == 'F' and mesure[j][4] == 'F':
                    self.listeRang.append(1)
                elif mesure[j][2] == 'F':
                    self.listeRang.append(3)
                elif mesure[j][4] == 'F':
                    self.listeRang.append(2)
                else:
                    self.listeRang.append(4)
            
    def creerVoix(self,arg, **kwargs):
        numVoix = kwargs.get('numVoix', len(self.listeVoix))
        rangVoix = kwargs.get('rangVoix', [1])
        rangVoix = sorted(rangVoix)
        proba = kwargs.get('proba', 85)
        force = kwargs.get('forceMax', 100)
        forceMin = kwargs.get('forceMin', 80)
        longMax = kwargs.get('longMax', 100)
        longMin = kwargs.get('longMin', 50)
        if numVoix > len(self.listeVoix):
            numVoix = len(self.listeVoix)
        voix = {'numVoix' : numVoix,
                'rangVoix' : rangVoix,
                'proba' : proba,
                'forceMax' : force,
                'forceMin' : forceMin,
                'longMax' : longMax,
                'longMin' : longMin }
        if numVoix >= len(self.listeVoix):
            self.listeVoix.append(voix)
        else:
            self.listeVoix[numVoix]=voix
        self.resPattern()
        
    def delVoix(self, *args, **kwargs):
        mode = kwargs.get('mode', 'norm')
        if mode == 'norm':
            cible = list(args)
        if mode == 'inv':
            cible = list(range(len(self.listeVoix)))
            for i in range(len(args)):
                cible.remove(args[i])
        if mode == 'tout':
            cible = list(range(len(self.listeVoix)))
        cible2 = list()    
        for i in range(len(self.listeVoix)):
            if self.listeVoix[i]['numVoix'] in cible:
                cible2.append(self.listeVoix[i])
        for i in range(len(cible2)):
            self.listeVoix.remove(cible2[i])
        for i in range(len(self.pattern)):
            cible3 = list()
            for j in range(len(self.pattern[i])):
                if self.pattern[i][j][0] in cible:
                    cible3.append(tuple(self.pattern[i][j]))
            for k in range(len(cible3)):
                self.pattern[i].remove(cible3[k])
        self.resPattern()
               
    def resPattern(self):
        mesure = self.parent.mesure.lisMes
        self.pattern = list()
        for i in range(self.nbMesure):
            for j in range(len(mesure)):
                self.pattern.append(list())
        for i in range(len(self.listeVoix)):
            self.resPiste(self.listeVoix[i])
        
    def resPiste(self, voix):
        for i in range(len(self.pattern)):
            if self.listeRang[i] in voix['rangVoix']:
                prob = random.randint(1,100)
                if self.listeRang[i] >=1 :
                    prob = prob * self.listeRang[i] * 0.4
                prob = prob * len(voix['rangVoix'])
                if len(self.pattern[i]) > 0 :
                    prob = prob / len(self.pattern[i]) 
                if prob <= voix['proba']:
                    force = random.randint(voix['forceMin'],voix['forceMax'])
                    long = random.randint(voix['longMin'],voix['longMax'])
                    self.pattern[i].append((voix['numVoix'], force, long))
                    
    def basicPattern(self):
        self.creerVoix(1)
        self.creerVoix(2, rangVoix = [2])
        self.creerVoix(3, rangVoix = [2,3])
        self.creerVoix(4, rangVoix = [2,3,4])
                    
    def info(self):
        def printPas(index):
            maxNV = 0
            LV = list()
            for j in range(len(self.listeVoix)):
                LV.append(self.listeVoix[j]['numVoix'])
                if self.listeVoix[j]['numVoix'] > maxNV:
                    maxNV = self.listeVoix[j]['numVoix'] 
            for j in range(maxNV+1):
                if j in LV:
                    var = 0
                    for k in range(len(self.pattern[index])):
                        if self.pattern[index][k][0] == j:
                            print('#', end = ' ')
                            var = 1
                    if var == 0:
                        print(' ', end = ' ')

        print(self.__dict__)
        print('------------------------------------------')
        print('VOIX')
        print()
        for i in range(len(self.listeVoix)):
            print(self.listeVoix[i])
            print()
        
        print('------------------------------------------')
        print('PATERN')
        print()
        print('N  R | ', end = '')
        for i in range(len(self.listeVoix)):
            print(self.listeVoix[i]['numVoix'] , end = ' ')
        print()
        
        for i in range(len(self.pattern)):
            if i % len(self.parent.mesure.lisMes) ==0:
                print()
            print(i, end = ' ')
            
            if len(str(i)) == 1:
                print(' ', end='')
            print(self.listeRang[i] , end = ' | ')
            printPas(i)
            print()
   
        print('------------------------------------------')


