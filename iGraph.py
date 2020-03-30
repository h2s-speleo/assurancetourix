#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 17:38:48 2020

@author: j
"""
import mido
from threading import Thread

import random
import pygame
from pygame.locals import *

import solfege as SF
from solfege.TCores import TC























class Fenetre:
    """fenetre principale de l'interface graphique"""

    def __init__(self):
        pygame.init()
        """initialisation de pygame"""
        #Ouverture de la fenêtre Pygame
        self.fenetre = pygame.display.set_mode((900, 500), RESIZABLE)
        # création d'un fond de la meme taille que la fenetre
        fond = pygame.Surface(self.fenetre.get_size())
        fond = fond.convert()
        #on rempli le fond en blanc
        fond.fill((220,220,220))
        #on affiche le fond
        imPlay = pygame.image.load("image/play.jpg")
        imPause = pygame.image.load("image/pause.jpg")

        self.fenetre.blit(fond,(0,0))
        self.fenetre.blit(imPause,(0,0))
        pygame.display.flip()

        self.outport = mido.open_output('Midi Through:Midi Through Port-0')
        """ouverture du port de communication avec le serveur son"""


        METRO = USEREVENT + 1
        pygame.time.set_timer(METRO, 0)

        self.resSeq()
        self.longeur = len(self.listMessag)
        self.indice = 0
        self.boucle = 0
        self.derNote = 60
        self.prog = 0
        self.playing = 0
        self.tempo = 150

        def resJouer() :
            pygame.time.set_timer(METRO, 0)
            msg2 = mido.Message("note_off",
                                channel = 1,
                                note = self.derNote,
                                velocity=127)
            self.outport.send(msg2)
            if self.prog ==  1:
                self.resSeq()
            self.playing  = 0
            self.longeur = len(self.listMessag)
            self.indice = 0
            self.fenetre.blit(fond,(0,0))
            self.fenetre.blit(imPause,(0,0))
            pygame.display.flip()
            if self.boucle == 1 :
                pygame.time.set_timer(METRO, self.tempo)
                self.fenetre.blit(fond,(0,0))
                self.fenetre.blit(imPlay
                                  ,(0,0))
                pygame.display.flip()


        def jouer() :
            if self.indice == self.longeur :
                resJouer()
                print()
            else:
                print(self.indice, end = ' / ')
                print(self.longeur - 1, end = ' - ')
                pas = self.listMessag[self.indice]
                if len(pas) > 0:
                    for i in range(len(pas)):
                        print(pas[i][0], end = ' : ')
                        print(pas[i][1], end = ' | ' )
                        msg2 = mido.Message(pas[i][1],
                                            channel = 1,
                                            note = pas[i][0],
                                            velocity=127)
                        self.outport.send(msg2)
                        self.derNote = pas[i][0]
                else:
                    print()
            self.indice = self.indice + 1


        """boucle principale de l'interface graphique"""
        #BOUCLE INFINIE
        continuer = 1

        while continuer:
            for event in pygame.event.get():
                """pour chaque evenement pygame dans la liste d'attente"""
                if event.type == QUIT :
                    self.outport.close()
                    """on ferme le port midi du serveur son"""
                    continuer = False
                    """on casse la boucle"""

                if event.type == METRO:
                    jouer()

                if event.type == KEYDOWN and event.key == K_SPACE:
                    pygame.time.set_timer(METRO, self.tempo)
                    self.fenetre.blit(fond,(0,0))
                    self.fenetre.blit(imPlay,(0,0))
                    pygame.display.flip()

                    print('PLAY')


                if event.type == KEYDOWN and event.key == K_RETURN:
                    print('STOP')
                    resJouer()

                if event.type == KEYDOWN and event.key == K_LALT:
                    pygame.time.set_timer(METRO, 0)
                    msg2 = mido.Message("note_off",
                                        channel = 1,
                                        note = self.derNote,
                                        velocity=127)
                    self.outport.send(msg2)
                    self.fenetre.blit(fond,(0,0))
                    self.fenetre.blit(imPause,(0,0))
                    pygame.display.flip()
                    print('PAUSE')

                if event.type == KEYDOWN and event.key == K_DOWN:
                    self.tempo = self.tempo + 25
                    if self.tempo > 500 :
                        self.tempo = 500
                    print('TEMPO : ', end = '')
                    print (150/self.tempo)

                if event.type == KEYDOWN and event.key == K_UP:
                    self.tempo = self.tempo - 25
                    if self.tempo < 50 :
                        self.tempo = 50
                    print('TEMPO : ', end = '')
                    print (150/self.tempo)

                if event.type == KEYDOWN and event.key == K_b:
                    if self.boucle == 1 :
                        self.boucle = 0
                        print('BOUCLE OFF')
                    elif self.boucle == 0 :
                        self.boucle = 1
                        print('BOUCLE ON')

                if event.type == KEYDOWN and event.key == K_n:
                    if self.prog == 1 :
                        self.prog = 0
                        print('PROGRESSION OFF')
                    elif self.prog == 0 :
                        self.prog = 1
                        print('PROGRESSION ON')


                if event.type == KEYDOWN and event.key == K_r:
                    print('RESET SEQUENCE')
                    resJouer()
                    self.resSeq()
                    resJouer()

                if event.type == KEYDOWN and event.key == K_p:
                    print('RESET PARAM')
                    resJouer()
                    self.resParam()
                    resJouer()

                if event.type == KEYDOWN and event.key == K_i:
                    self.motif.info()



        pygame.quit()
        """on quitte pygame"""

    def resSeq(self):
        self.motif = SF.Motif()
        self.listMessag = self.motif.melo.rythme.listeMessag

    def resParam(self):

        print('IGraph.resParam')
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
        NOCTA = random.randint(2, 4)
        print('nOcta', end = ' : ')
        print(NOCTA)
        NBTPS = random.randint(2, 4)
        print('nbTps', end = ' : ')
        print(NBTPS)
        NBSTPS = random.randint(2, 4)
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

        self.motif = SF.Motif(mode = MODE,
                              nomFr = NOMFR,
                              alt = ALT,
                              nOcta = NOCTA,
                              nbTps = NBTPS,
                              nbSTps = NBSTPS,
                              cible = CIBLE,
                              probTotal = PROBTOTAL,
                              probTpsFa = PROBTPSFA,
                              probTpsFo = PROBTPSFO)
        self.listMessag = self.motif.melo.rythme.listeMessag


