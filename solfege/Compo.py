#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import solfege as SF

def setPhrase(cible, listeDegre):
    degre = listeDegre[-1]
    origine = degre
    while degre != cible :
        a = degre + random.randint(-2,2)
        if origine < cible:
            while a <= origine :
                a = degre + random.randint(-1,2)
            if degre > cible :
                a = degre + random.randint(-2,0)
        if origine > cible:
            while a >= origine :
                a = degre + random.randint(-2,1)
            if degre < cible :
                a = degre + random.randint(0,2)
        degre =  a
        listeDegre.append(degre)
    return listeDegre

class Compo:
    def __init__(self,**kwargs):
        self.parent = None
        self.probTotal = 80
        self.probTpsFo = 100
        self.probTpsFa = 25
        self.longMax = 2
        self.longMin = 1
        self.cible = [5,1]
        self.reset(**kwargs)

    def reset(self, **kwargs):
        self.probTotal = kwargs.get('probTotal', self.probTotal)
        self.probTpsFo = kwargs.get('probTpsFo', self.probTpsFo)
        self.probTpsFa = kwargs.get('probTpsFa', self.probTpsFa)
        self.longMax = kwargs.get('longMax', self.longMax)
        self.longMin = kwargs.get('longMin', self.longMin)
        self.cible = kwargs.get('cible', self.cible)

    def Comp1(self):
        self.CompN1()
        self.CompR1()
        self.resLMessage()

    def CompN1(self):
        self.parent.melo.rythme.listNote = list()
        listeDegre = [1]
        for i in range(len(self.cible)):
            listeDegre = setPhrase(self.cible[i], listeDegre)
        GAMME = self.parent.melo.tonal.gamme
        for i in range(len(listeDegre)):
            for j in range(len(GAMME)):
                if GAMME[j].degre == listeDegre[i]:
                    self.parent.melo.rythme.listNote.append(GAMME[j])

    def CompR1(self):
        self.parent.melo.rythme.listRythme = list()
        compt  = 0
        for i in range(len(self.parent.melo.rythme.listNote)):
            a = random.randint(1,100)
            if a <= self.probTotal :
                self.parent.melo.rythme.listRythme.append({'note' : self.parent.melo.rythme.listNote[i]})
            else:
                self.parent.melo.rythme.listRythme.append({'note' : SF.Silence()})
                self.parent.melo.rythme.listRythme.append({'note' : self.parent.melo.rythme.listNote[i]})

        for i in range(len(self.parent.melo.rythme.listRythme)):
            if self.parent.melo.rythme.listRythme[i]['note'].degre in self.cible  or self.parent.melo.rythme.listRythme[i]['note'].degre == 1 :
                self.parent.melo.rythme.listRythme[i]['methode'] = 'cible'
            else :
                if self.parent.melo.rythme.listRythme[i+1]['note'].degre in self.cible  or self.parent.melo.rythme.listRythme[i+1]['note'].degre == 1 :
                    self.parent.melo.rythme.listRythme[i]['methode'] = 'suivante cible'
                else :
                    self.parent.melo.rythme.listRythme[i]['methode'] = 'classique'

            compt = 0
        for i in range(len(self.parent.melo.rythme.listRythme)):
            if i < len(self.parent.melo.rythme.listRythme) :
                if self.parent.melo.rythme.listRythme[i]['methode'] == 'classique':
                    duree = self.durClassique(compt, i)
                    self.parent.melo.rythme.listRythme[i]['position'] = compt
                    self.parent.melo.rythme.listRythme[i]['duree'] = duree
                    compt = compt + duree
                if self.parent.melo.rythme.listRythme[i]['methode'] == 'suivante cible':
                    duree = self.durSuivCible(compt, i)
                    self.parent.melo.rythme.listRythme[i]['position'] = compt
                    self.parent.melo.rythme.listRythme[i]['duree'] = duree
                    compt = compt + duree
                if self.parent.melo.rythme.listRythme[i]['methode'] =='cible':
                    duree = self.durCible(compt, i)
                    self.parent.melo.rythme.listRythme[i]['position'] = compt
                    self.parent.melo.rythme.listRythme[i]['duree'] = duree
                    compt = compt + duree

    def durClassique(self, compt, i):
        duree = 1
        while True :
            a = random.randint(1,100)
            if self.parent.mesure.lisMes[(compt + duree) % len(self.parent.mesure.lisMes)][4] == 'f':
                if a <= self.probTpsFa :
                    break
                else :
                    duree = duree + 1
            if self.parent.mesure.lisMes[(compt + duree) % len(self.parent.mesure.lisMes)][4] == 'F':
                if a <= self.probTpsFo :
                    break
                else :
                    duree = duree + 1
        return duree

    def durSuivCible(self, compt, i):
        duree = 1
        continuer = 1
        while continuer == 1 :
            if self.parent.mesure.lisMes[(compt + duree) % len(self.parent.mesure.lisMes)][2] == 'F'\
            and self.parent.mesure.lisMes[(compt + duree) % len(self.parent.mesure.lisMes)][4] == 'F':
                continuer = 0
            else :
                duree = duree + 1
        return duree

    def durCible(self, compt, i):
        a = random.randint(1,self.parent.mesure.nbTps)
        duree = a * self.parent.mesure.nbSTps
        return duree


    def resLMessage(self):
        dureeTotal = 0
        for i in range(len(self.parent.melo.rythme.listRythme)):
            dureeTotal = dureeTotal + self.parent.melo.rythme.listRythme[i]['duree']
        dureeTotal = dureeTotal + 1
        for i in range(dureeTotal) :
            self.parent.melo.rythme.listeMessag.append(list())

        for i in range(len(self.parent.melo.rythme.listRythme)):
            if self.parent.melo.rythme.listRythme[i]['note'].nomFr != 'SIL' :
                debut = self.parent.melo.rythme.listRythme[i]['position']
                fin = self.parent.melo.rythme.listRythme[i]['position'] + self.parent.melo.rythme.listRythme[i]['duree']

                self.parent.melo.rythme.listeMessag[debut]\
                .append((
                        self.parent.melo.rythme.listRythme[i]['note'].nMidi,
                        "noteOn",
                        self.parent.melo.rythme.listRythme[i]['note']))

                self.parent.melo.rythme.listeMessag[fin]\
                .append((
                        self.parent.melo.rythme.listRythme[i]['note'].nMidi,
                        "noteOff",
                        self.parent.melo.rythme.listRythme[i]['note']))

    def info(self):
        print("probTotal : ", end = '')
        print(self.probTotal)
        print("probTpsFo : ", end = '')
        print(self.probTpsFo)
        print("probTpsFa : ", end = '')
        print(self.probTpsFa)
        print("cible : ", end = '')
        print(self.cible)



