#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import pygame
from pygame.locals import *

import solfege as SF
from solfege.TCores import TC

class IGraph():

    def __init__(self, arg):
        self.AS = arg
        self.AS.IGVar = dict()
        self.AS.IGVar['listeVoix'] = list()
        self.AS.IGVar['objPyoActif'] = dict()
        self.AS.IGVar['tempo'] = 500
        self.AS.IGVar['playing']=0 #sert a savoir si on joue ou pas
        self.AS.IGVar['boucle']=0
        self.AS.IGVar['autoReset']=0
        self.AS.IGVar['listeMess'] = list()
        self.AS.IGVar['indiceMess'] = 0
        self.RandomParam()
        self.AS.IGVar['longLisMess'] = len(self.AS.IGVar['listeMess'])
        
        
        self.AS.IGVar['objPyoActif']['init']=list()
        self.AS.IGVar['objPyoActif']['kill']=list()
        self.AS.IGVar['objPyoActif']['pause']=list()
        self.AS.IGVar['objPyoActif']['play']=list()
        self.AS.IGVar['objPyoActif']['nom']=list()
        self.AS.MESS.ResetMess()
        self.AS.MESS.putBasMess('init')
        
    #   self.AS.info(self)  
        
    def Boucle(self):
        if self.AS.IGVar['boucle']==0:
            self.AS.IGVar['boucle']=1
            print('BOUCLE ON')
        else:
            self.AS.IGVar['boucle']=0
            print('BOUCLE OFF')
        
    #   self.AS.info(self)  
            
    def AutoReset(self):
        if self.AS.IGVar['autoReset']==0:
            self.AS.IGVar['autoReset']=1
            print('AUTORESTE ON')
        else:
            self.AS.IGVar['autoReset']=0
            print('AUTORESTE OFF')

    #   self.AS.info(self)  
        
    def TempoMoins(self):
        self.AS.IGVar['tempo']= int(self.AS.IGVar['tempo']* 1.1)
        if self.AS.IGVar['tempo']> 1000 :
            self.AS.IGVar['tempo']= 1000
        if self.AS.IGVar['tempo']< 530 and self.AS.IGVar['tempo']> 470 :
            self.AS.IGVar['tempo']= 500
        pygame.time.set_timer(self.AS.METRO, self.AS.IGVar['tempo'] )
        print('TEMPO : ', end = '')
        print (str(500/self.AS.IGVar['tempo'])[:4])
        
    #   self.AS.info(self)  

    def TempoPlus(self):
        self.AS.IGVar['tempo']= int(self.AS.IGVar['tempo']* 0.9)
        if self.AS.IGVar['tempo']< 250 :
            self.AS.IGVar['tempo']= 250
        if self.AS.IGVar['tempo']< 530 and self.AS.IGVar['tempo']> 470 :
            self.AS.IGVar['tempo']= 150
        pygame.time.set_timer(self.AS.METRO, self.AS.IGVar['tempo'] )
        print('TEMPO : ', end = '')
        print (str(500/self.AS.IGVar['tempo'])[:4])
        
    #   self.AS.info(self)  
        
    def RandomParam(self):
        print('RANDOM PARAM')

        NOMFR = random.choice(TC.do_re_mi)
        print('nomFr', end = ' : ')
        print(NOMFR)
        ALT = random.choice(['dièse',
                             '',
                             'bémole'])
        print('alt', end = ' : ')
        print(ALT)
        CIBLE = random.choice([[5, 1],
                              [5, 1, -3, 1],
                              [-3, 1],
                              [-3, 1, 5, 1]])
        print('cible', end = ' : ')
        print(CIBLE)
        MODE = random.choice([TC.blues_m,
                             TC.blues_M,
                             TC.tonal_m,
                             TC.tonal_M])
        print('mode', end = ' : ')
        print(MODE)
        NOCTA = random.randint(3, 4)
        print('nOcta', end = ' : ')
        print(NOCTA)
        NBTPS = random.randint(2, 4)
        print('nbTps', end = ' : ')
        print(NBTPS)
        NBSTPS = random.randint(1, 3)
        print('nbSTps', end = ' : ')
        print(NBSTPS)
        PROBTOTAL = random.randint(60, 100)
        print('probTotal', end = ' : ')
        print(PROBTOTAL)
        PROBTPSFA = random.randint(10, 50)
        print('brobTpsFa', end = ' : ')
        print(PROBTPSFA)
        print('brobTpsFo', end = ' : ')
        PROBTPSFO  = random.randint(60, 100)
        print(PROBTPSFO)
        self.AS.motif.mode = MODE
        self.AS.motif.nomFr = NOMFR
        self.AS.motif.alt = ALT
        self.AS.motif.nOcta = NOCTA
        self.AS.motif.nbTps = NBTPS
        self.AS.motif.nbSTps = NBSTPS
        self.AS.motif.cible = CIBLE
        self.AS.motif.probTotal = PROBTOTAL
        self.AS.motif.probTpsFa = PROBTPSFA
        self.AS.motif.probTpsFo = PROBTPSFO
        self.ResetSequence()
        

    #   self.AS.info(self)  
        
    def ResetSequence(self):
        print('RESET SEQUENCE')
        self.AS.motif.reset()
        self.AS.IGVar['indiceMess'] = 0
        self.AS.MESS.ResetMess()
        if self.AS.IGVar['playing'] == 1:
            if self.AS.IGVar['boucle']==0 :
                 
                self.Stop()

    #   self.AS.info(self)  
        
        
    def Stop(self):
        self.AS.IGVar['indiceMess'] = 0
        self.AS.MESS.ResetMess()
        if self.AS.IGVar['boucle']==0 :
            self.AS.IGVar['playing'] = 0

            self.AS.MESS.putBasMess('pause')
            print('STOP')
        
        else:
            if self.AS.IGVar['autoReset'] == 1:
                self.ResetSequence()

    #   self.AS.info(self)  
            
    def PlayPause(self):

        if self.AS.IGVar['playing'] == 0:
            self.AS.MESS.putBasMess('play')
            self.AS.IGVar['playing'] = 1
            print('PLAY')
        elif self.AS.IGVar['playing'] == 1:
            self.AS.IGVar['playing'] = 0
            self.AS.MESS.putBasMess('pause')
            print('PAUSE')

    #   self.AS.info(self)  