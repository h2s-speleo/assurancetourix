#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python 3.8.2 (default, Feb 26 2020, 22:21:03)
#import sys
import os
import time
from signal import SIGTERM, SIGKILL
from multiprocessing import Process, freeze_support, Queue

import pygame
from pygame.locals import *
from pyo import *
 
import assu
import solfege as SF
#from solfege.TCores import TC

#
#import sys
#sys.stdout = open('stdout.log', 'w')



# serveur pyo. execute les commandes envoyée dans la queue en str()
# executé en parallèle
def ServPyo():
    

    
    
    s = Server() #instanciation du serveur
    x = None
    inputs, outputs = pa_get_devices_infos() #récupération de la liste des périphériques
    for index in sorted(outputs.keys()):
        if outputs[index]['name'] == 'pulse' : # nom de ton périférique son
            x = index
    if x == None : #en cas d'échec on se choisi au périphérique 0
        print('default device')
        x = 1
    s.setOutputDevice(x) #définition de la sortie audio du serveur
    s.boot()
    s.start()
    while True :
        if not qSon.empty(): #si on a quelquechose dans la queue
            mes = qSon.get()
            if mes == 'break':
                break #fin de la boucle infinie
            else :

#                print ('COMMAND' , end = ' : ')
                
#                print(mes)
                exec(mes) #on execute la commande passée en str()

        time.sleep(0.001)#ralenti la boucle principale
    s.stop() #on coupe le serveur
    print('coupure Serveur Pyo')

class Core():
    
    
    def __init__(self):
        self.info(self)
        
         #définition de la fenetre
        self.fenetre = pygame.display.set_mode((200, 200), RESIZABLE)
##############################################################################        
        fond = pygame.Surface(self.fenetre.get_size())
        fond = fond.convert()
        fond.fill((220,220,220))
        self.fenetre.blit(fond,(0,0))
        pygame.display.flip()
##############################################################################        
        

        
        self.METRO = USEREVENT + 1 #création d'un pygame event métronome
        #définition des attributs
        
        self.qSon = qSon
        self.motif = SF.Motif()
        self.MESS = assu.Mess(self)
        self.IG = assu.IGraph(self)
        self.info(self)


        pygame.time.set_timer(self.METRO, self.IGVar['tempo'])
        

        continuer = 1
        while continuer:
            for event in pygame.event.get():
                if event.type == QUIT :      
                    qSon.put('break') #on casse la boucle de ServPyo
                    continuer = False #on casse la boucle de ServPyo
                    
##############################################################################               
                if event.type == KEYDOWN and event.key == K_t:
                    qSon.put('a = Sine(mul=0.1).out()')
                    print('PLAY')
                    
                if event.type == KEYUP and event.key == K_t:
                    qSon.put('a.stop()')
                    print('STOP')   
##############################################################################
                    
                if event.type == KEYDOWN and event.key == K_DOWN:
                    self.IG.TempoMoins()

                if event.type == KEYDOWN and event.key == K_UP:
                    self.IG.TempoPlus()

                if event.type == KEYDOWN and event.key == K_RETURN:
                    self.IG.Stop()
                    
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.IG.PlayPause()
                
                
                if event.type == KEYDOWN and event.key == K_b:
                    self.IG.Boucle()
                
                if event.type == KEYDOWN and event.key == K_a:
                    self.IG.AutoReset()
                    
                if event.type == KEYDOWN and event.key == K_p:
                    self.IG.RandomParam()
                
                if event.type == KEYDOWN and event.key == K_r:
                    self.IG.ResetSequence()   
                
                    
                if event.type == self.METRO:
                    
                    self.MESS.putSeqMess()
                    
                
                pygame.time.wait(20) #ralenti la boucle principale
                
    def info(self, arg):
#        print('##############################################################')
#        print('INFO')
#        
#        for key, value in self.__dict__.items():
#            print(arg)
#            if type(value) == SF.Motif :
#                print('MOTIF :')
#                print(value.__dict__)
#                print()
#                
#            if key == 'IGVar' :
#                print('IGVar : ')
#                for key2, value2 in value.items():
#                    print(key2)
#                    
#                    if key2 == 'playing' or\
#                    key2 == 'indiceMess' or\
#                    key2 == 'longLisMess' or\
#                    key2 == 'objPyoActif':
#                        print(key2, end = ' : ')
#                        print(value2)
#                        print()
#                    print()
#                print()
#                
#            else :
#                print(key, end = ' : ')
#                print(value)
#            
#        print()
#        print('##############################################################')
        pass
        
 
freeze_support()
qSon = Queue() #création de la queue du serveur pyo
SP = Process(target=ServPyo, daemon=True) #création du processus du serveur pyo
SP.start()
pidServPyo = SP.pid



millis = int(round(time.time() * 1000))
print('############## server boot / start ##############\n')

#while millis + 3000 > int(round(time.time() * 1000)):
time.sleep(2)
      
      
pygame.init() #on lance pygame    
print('RUN')

AS = Core() #instanciation de AC. fait office de boucle principale
# fin de la boucle


pygame.quit() #fin de pygame
SP.join() #on attend la fin du processus du serveur pyo 
SP.terminate() #on supprime le processus du serveur pyo 
if SP.is_alive():
    os.kill(pidServPyo, SIGTERM)
    print('TERM signal')
if SP.is_alive():
    os.kill(pidServPyo, SIGKILL)
    print('KILL signal')
print('fin')
##stayingAlive = input()
#
exit()
