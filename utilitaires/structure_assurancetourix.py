#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Python 3.8.2 (default, Feb 26 2020, 22:21:03)"""

import os
from signal import SIGTERM, SIGKILL
from multiprocessing import Process, freeze_support, Queue

import pygame
from pygame.locals import *
from pyo import *

import assu
import solfege as SF
from solfege.TCores import TC

# serveur pyo. execute les commandes envoyée dans la queue en str()
# executé en parallèle
def ServPyo():
    import time
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
                exec(mes) #on execute la commande passée en str()
        time.sleep(0.001)#ralenti la boucle principale
    s.stop() #on coupe le serveur
    print('coupure Serveur Pyo')

class Core():
    def __init__(self):
        pygame.init() #on lance pygame
         #définition de la fenetre
        self.fenetre = pygame.display.set_mode((200, 200), RESIZABLE)
        fond = pygame.Surface(self.fenetre.get_size())
        fond = fond.convert()
        fond.fill((220,220,220))
        self.fenetre.blit(fond,(0,0))
        pygame.display.flip()
        #définition des attributs
        self.playing = 0 #sert a savoir si on joue ou pas
        self.tempo = 2000
        self.motif = SF.Motif()
        self.IG = assu.IGraph(self)
        self.OSC = assu.Osc(self)
        
        METRO = USEREVENT + 1 #création d'un pygame event métronome
        pygame.time.set_timer(METRO, self.tempo)
        print('############## server boot / start ##############\n')
        pygame.time.wait(2000)
        
        continuer = 1
        while continuer:
            for event in pygame.event.get():
                if event.type == QUIT :      
                    qSon.put('break') #on casse la boucle de ServPyo
                    continuer = False #on casse la boucle de ServPyo

                if event.type == METRO:
##############################################################################
######### exemple de message #################################################
                    if self.playing == 0 :
                        qSon.put('a = Sine(mul=0.1).out()') #on place le message dans la queue
                        self.playing = 1
                    
                    elif self.playing == 1 :
                        qSon.put('a.stop()')
                        self.playing = 0
##############################################################################
                
                pygame.time.wait(1) #ralenti la boucle principale
 
freeze_support()
qSon = Queue() #création de la queue du serveur pyo
SP = Process(target=ServPyo, daemon=True) #création du processus du serveur pyo
SP.start()
pidServPyo = SP.pid

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
#exit()
