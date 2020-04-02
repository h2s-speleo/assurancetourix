#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
from signal import SIGTERM, SIGKILL
from multiprocessing import Process, freeze_support, Queue
import time
import pygame
from pygame.locals import *
from pyo import *



# serveur pyo. execute les commandes envoyée dans la queue en str() et les execute
def ServPyo():
    s = Server()
    x = None
    inputs, outputs = pa_get_devices_infos()
    for index in sorted(outputs.keys()):
        if outputs[index]['name'] == 'pulse' : # nom de votre périférique son
            x = index
    if x == None :
        print('default device')
        x = 1
    s.setOutputDevice(x)
    s.boot()
    s.start()
    while True :
        if not qSon.empty():
            mes = qSon.get()
            if mes == 'break':
                break
            else :
                exec(mes)
        time.sleep(0.001)
    s.stop()
    print('exit')

class core():
    def __init__(self):
        pygame.init()
        self.fenetre = pygame.display.set_mode((200, 200), RESIZABLE)
        fond = pygame.Surface(self.fenetre.get_size())
        fond = fond.convert()
        fond.fill((220,220,220))
        self.fenetre.blit(fond,(0,0))
        pygame.display.flip()
        self.playing = 0
        METRO = USEREVENT + 1
        pygame.time.set_timer(METRO, 2000)
        print('############## server boot / start ##############\n')
        count = 3
        while count != 0 :
            print(count)
            time.sleep(0.5)
            count = count -1
        print('-> run')
        
        count = 0
        continuer = 1
        while continuer:
            for event in pygame.event.get():
                """pour chaque evenement pygame dans la liste d'attente"""
                if event.type == QUIT :      
                    qSon.put('break')
                    print('coupure SP')
                    continuer = False 

                if event.type == METRO:
                    if self.playing == 0 :
                        print(str(count) + ' - note on')
                        qSon.put('a = Sine(mul=0.1).out()')
                        self.playing = 1
                    
                    elif self.playing == 1 :
                        print(str(count) + ' - note off')
                        qSon.put('a.stop()')
                        self.playing = 0
                        count = count + 1
            pygame.time.wait(1)
 
freeze_support()
qSon = Queue()
SP = Process(target=ServPyo, daemon=True)
SP.start()
pidServPyo = SP.pid

AS = core()

# fin du procecuss
pygame.quit()
print('fin')
SP.join()
SP.terminate()
if SP.is_alive():
    os.kill(pidServPyo, SIGTERM)
    print('TERM signal')
if SP.is_alive():
    os.kill(pidServPyo, SIGKILL)
    print('KILL signal')
print('pid processus ServPyo : ', end = '')
print(pidServPyo)
exit()
