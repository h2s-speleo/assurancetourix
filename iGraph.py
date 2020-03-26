#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 17:38:48 2020

@author: j
"""
import mido
from threading import Thread

import time
import pygame
from pygame.locals import *


import random



































pygame.init()
"""initialisation de pygame"""
BCD3000 = USEREVENT+1
"""création d'un nouveau type d'événement BCD3000 qui permet de communiquer
avec la BCD3000 de behringer"""

class ServeurMidi(Thread):
    """thread suportant le serveur midi"""
    def __init__(self,arg):
        Thread.__init__(self)
        self.parent = arg
        self.arret = 0
    def run(self):
        """lancement du thread"""
        self.blit()
        while self.arret  == 0:
            """tant que le thread n'a pas été éteint"""
            for msg in self.parent.inport.iter_pending(): # passe contenu 'inport' à 'msg'
                """pour chaque message dans la liste d'attente"""
                BCDEvent = pygame.event.Event(BCD3000, message=msg)
                """creation d'u nevenement pygame"""
                pygame.event.post(BCDEvent)
                """envoie de l'évenement"""
        self.blit()
    def blit(self):
        """allume et éteint toutes les leds du BCD3000 pour vérifier la
        conection"""
        for i in range (100):
            msg2 = mido.Message('control_change',value=65, control=i, time = 0)
            """création du message pour allumer les led"""
            self.parent.BCDOutput.send(msg2)
            """envoi du message"""
        time.sleep(0.5)
        for i in range (100):
            msg2 = mido.Message('control_change',value=60, control=i, time = 0)
            """création du message pour éteindre les led"""
            self.parent.BCDOutput.send(msg2)
            """envoi du message"""
    def stopthread(self):
        """permet de tuer le thread"""
        self.arret=1


class Fenetre:
    """fenetre principale de l'interface graphique"""

    def __init__(self):
        #Ouverture de la fenêtre Pygame
        self.fenetre = pygame.display.set_mode((900, 500), RESIZABLE)
        # création d'un fond de la meme taille que la fenetre
        fond = pygame.Surface(self.fenetre.get_size())
        fond = fond.convert()
        #on rempli le fond en blanc
        fond.fill((220,220,220))
        #on affiche le fond
        self.fenetre.blit(fond,(0,0))
        #rafraichissement de l'image
        pygame.display.flip()

        self.controleurMidi = 1
        """permet de savoir si le controleur midi est reconu"""
        self.outport = mido.open_output('Midi Through:Midi Through Port-0')
        """ouverture du port de communication avec le serveur son"""
        try :
            """on essaye d'ouvrir les ports midi de la BCD3000 et de lancer le
            thread du serveur midi"""
            self.inport = mido.open_input('BCD3000 MIDI 1')
            self.BCDOutput = mido.open_output('BCD3000 MIDI 1')
            self.midiThread_1 = ServeurMidi(self)
            self.midiThread_1.start()
        except :
            """on modifie l'atribut pour indiquer qu'il n'y a pas de BCD3000"""
            self.controleurMidi = 0
            print('controleur midi non reconnu')

    def start(self):

        def testJouer():
            nombreTemps = 3
            """nombre de temps d'une mesure"""
            nombreSTemps = 3
            """subdivision du temps"""
            nombreMesure = 1
            """nombre de mesure"""


            typeMesure = str()
            typeTemp = str()
            forceT = str()
            forceST = str()
            typeSTemps = str()
            compt = 0
            listeMesure = list()

            if nombreTemps % 3 == 0 :
                typeMesure = "ternaire"

            if nombreTemps % 2 == 0 :
                typeMesure = "binaire"

            if nombreSTemps % 3 == 0 :

                typeTemp = "ternaire"

            if nombreSTemps % 2 == 0 :
                typeTemp = "binaire"


            #print (nombreTemps)
            #print(typeMesure)

            for i in range(nombreTemps):
                #print("temps : " + str(i+1), end = " -> ")

                if typeMesure == "binaire" :
                    if i%2 == 0 :
                        forceT = "F"
                        #print(typeTemps)
                    else :
                        forceT = "f"
                        #print(typeTemps)

                if typeMesure == "ternaire" :
                    if i%3 == 0 :
                        forceT = "F"
                        #print(typeTemps)

                    else :
                        forceT = "f"
                        #print(typeTemps)



                for j in range(nombreSTemps):


                    #print("    sous-temps : " + str(j), end = " -> ")

                    if typeTemp == "binaire" :
                        if j%2 == 0 :
                            forceST = "F"
                            #print(typeSTemps)
                        else :
                            forceST = "f"
                            #print(typeSTemps)

                    if typeTemp == "ternaire" :
                        if j%3 == 0 :
                            forceST = "F"
                            #print(typeSTemps)
                        else :
                            forceST = "f"
                            #print(typeSTemps)


                    #print(compt)
                    listeMesure.append((compt,i,forceT,j,forceST))
                    compt = compt + 1


            print("mesure")

            for i in range(len(listeMesure)):
                print(listeMesure[i])

            print()
            print("-------------------------------------")
            print("rhytme")

            for j in range(3):
                for i in range(len(listeMesure)):
                    print(listeMesure[i][4], end = " ")
            print()
            ###############################################################################

            nombreNote = 8
            probTotal = 90
            probTF = 90 *probTotal/100
            probTf = 40 *probTotal/100
            listeSequence = list()

            compt = 0

            for i in range(nombreNote):



                suite = 0
                while suite == 0:

                    #print('_______________________________________________________')
                    #print( listeMesure[compt % len(listeMesure)])
                    #print(listeMesure[compt % len(listeMesure)][0])


                    if listeMesure[compt % len(listeMesure)][4] == 'F':
                        #print('F')
                        if random.randrange(100) + probTF > 100 :
                            print(i,end = " ")
                            listeSequence.append(i)
                            suite = 1
                        else :
                            print('-',end = " ")
                            listeSequence.append("-")

                    if listeMesure[compt % len(listeMesure)][4] == 'f':
                        #print('f')
                        if random.randrange(100) + probTf > 100 :
                            print(i,end = " ")
                            listeSequence.append(i)
                            suite = 1
                        else :
                            print('-',end = " ")
                            listeSequence.append('-')




                    compt = compt + 1

            print()
            print()
            #print(listeSequence)
            """

            print()
            print("-------------------------------------")
            print("durée")
            """
            noteActuel = int(-1)
            longMaxNote = 3
            noteJouée = 0
            compt = int()
            listeSequence2 = list()


            for i in range(longMaxNote):
                listeSequence.append('-')

            for i in range(len(listeSequence)):

                if type(listeSequence[i]) is int  :
                    noteJouée = 1
                    compt = i + random.randrange(longMaxNote+1)
                    noteActuel = listeSequence[i]
                    listeSequence2.append(noteActuel)

                elif i < compt :


                    listeSequence2.append(noteActuel)
                else :

                    listeSequence2.append("-")


            while listeSequence2[-1] == '-' :
                del listeSequence2[-1]
            listeSequence2.append("-")
            for i in range(len(listeSequence2)) :
                print(listeSequence2[i], end = ' ')

            print()


            hauteurNote = 55

            for i in range(len(listeSequence2)) :
                if type(listeSequence2[i]) is int  :
                    if i == 0 :

                        msg2 = mido.Message('note_on', channel=1, note=hauteurNote, velocity=127)

                        self.outport.send(msg2)
                        print('noteon', end = ' ')

                    else :
                        if listeSequence2[i] != listeSequence2[i-1]:
                            msg2 = mido.Message('note_off', channel=1, note=hauteurNote, velocity=127)
                            self.outport.send(msg2)
                            hauteurNote = hauteurNote + 2

                            msg2 = mido.Message('note_on', channel=1, note=hauteurNote, velocity=127)
                            self.outport.send(msg2)
                            print('noteon', end = ' ')



                else :
                    msg2 = mido.Message('note_off', channel=1, note=hauteurNote, velocity=127)
                    self.outport.send(msg2)
                    hauteurNote = hauteurNote - 6

                time.sleep(0.2)





























        """boucle principale de l'interface graphique"""
        #BOUCLE INFINIE
        continuer = 1
        while continuer:
            for event in pygame.event.get():
                """pour chaque evenement pygame dans la liste d'attente"""
                if event.type == QUIT :
                    if self.controleurMidi == 1:
                        """si BCD3000 est conecté"""
                        self.midiThread_1.stopthread()
                        """on tue le thread"""
                        self.midiThread_1.join()
                        """on attend la fin du thread"""
                        self.inport.close()
                        self.BCDOutput.close()
                        """on ferme les ports midi de la bcd3000"""
                    self.outport.close()
                    """on ferme le port midi du serveur son"""
                    continuer = False
                    """on casse la boucle"""

                if event.type == KEYDOWN and event.key == K_a:
                    """brouillon. envoie la portée V2"""
                    Portée2(self.fenetre).fond()

                if event.type == KEYDOWN and event.key == K_z:
                    testJouer()


                if event.type == KEYDOWN and event.key == K_SPACE:
                    """brouillon. envoie la portée V1"""
                    Portée(self.fenetre)

                if event.type == KEYDOWN and event.key == K_RETURN:
                    """brouillon. envoi d'une note pendant 0,1 seconde"""
                    msg2 = mido.Message('note_on', channel=1, note=60, velocity=127)
                    """création du message noteon"""
                    self.outport.send(msg2)
                    """envoi du message"""
                    time.sleep(0.1)
                    msg2 = mido.Message('note_off', channel=1, note=60, velocity=127)
                    self.outport.send(msg2)


                if event.type == BCD3000:
                    """brouillon. reception des evenement du serveur midi et
                    envoi d'un message au serveur son"""
                    print('------------------------------------------------')
                    print (event.message)
                    print (event.message.bytes())
                    if event.message == mido.Message("note_on", channel=0, note=18, velocity=127, time=0):
                        print (event.message.type)
                        print (event.message.note)
                        print (event.message.channel)
                        print (event.message.velocity)
                        print (event.message.time)

                        msg2 = mido.Message('note_on', channel=1, note=60, velocity=127)
                        self.outport.send(msg2)

                    if event.message == mido.Message("note_on", channel=0, note=18, velocity=0, time=0):
                        msg2 = mido.Message('note_off', channel=1, note=60, velocity=127)
                        self.outport.send(msg2)
        pygame.quit()
        """on quitte pygame"""


class Portée2:
    """objet modelisant la portée"""
    def __init__(self,arg):
        """prend en argument une surface pygame"""

        self.origineX = 10
        self.origineY = 10
        """origine de la surface pygame qui va dessiner la portée"""
        self.nombreTemps = 3
        """nombre de temps d'une mesure"""
        self.nombreSTemps = 4
        """subdivision du temps"""
        self.nombreMesure = 1
        """nombre de mesure de la portée"""
        self.largeurST = 70
        """largeur de la surface pygame dessinant le sous-temp"""
        self.hauteurPortée = 400
        """hauteur de la surface pygame de la portée"""
        self.longMesure = self.nombreTemps * self.nombreSTemps
        """nombre de sous-temps dans la mesure"""
        self.longSurfPortée = self.longMesure * self.nombreMesure * self.largeurST
        """longeur de la surface pygame qui dessine la portée"""
        self.PGSurface = pygame.Surface((self.longSurfPortée,self.hauteurPortée))
        """création de la surface pygame qui dessinne la portée"""
        self.parent = arg
        """atribut stoquant la surface pygame parente"""

    def fond(self):
        """dessin du fond de la portée"""
        compt= 0
        """initialisation du compteur"""
        for k in range(self.nombreMesure):
            """pour chaque mesure"""
            for i in range(self.nombreTemps):
                """pour chaque temps"""
                for j in range(self.nombreSTemps):
                    """pour chaque soustemps"""
                    x = compt * self.largeurST
                    """on redéfinit la valeur de x pour actualiser l'origine du
                    nouveaux sous temps"""
                    couleurBase = 255
                    """définition de la couleur de base 250 250 250 = blanc"""
                    couleurDecalage = 10
                    """décalage entre deux gradient de couleur"""
                    if i % 2 == 0 :
                        """si c'est un temps paire"""
                        if j % 2 == 0 :
                            """si c'est un sous-temps paire"""
                            couleur = couleurBase
                            """définitionde la couleur"""
                            self.PGSurface\
                            .subsurface(x,0,self.largeurST,self.hauteurPortée)\
                            .fill((couleur,couleur,couleur))
                            """créationd la surface et remplissage selon le
                            gradiant de couleur"""
                        if j % 2 == 1 :
                            """si c'est un sous-temps impaire"""
                            couleur = couleurBase-(couleurDecalage*1)
                            """définitionde la couleur"""
                            self.PGSurface\
                            .subsurface(x,0,self.largeurST,self.hauteurPortée)\
                            .fill((couleur,couleur,couleur))
                            """créationd la surface et remplissage selon le
                            gradiant de couleur"""
                    if i % 2 == 1 :
                        """si c'est un temps impaire"""
                        if j % 2 == 0 :
                            """si c'est un sous-temps paire"""
                            couleur = couleurBase-(couleurDecalage*3)
                            """définitionde la couleur"""
                            self.PGSurface\
                            .subsurface(x,0,self.largeurST,self.hauteurPortée)\
                            .fill((couleur,couleur,couleur))
                            """créationd la surface et remplissage selon le
                            gradiant de couleur"""
                        if j % 2 == 1 :
                            """si c'est un sous-temps impaire"""
                            couleur = couleurBase-(couleurDecalage*4)
                            """définitionde la couleur"""
                            self.PGSurface\
                            .subsurface(x,0,self.largeurST,self.hauteurPortée)\
                            .fill((couleur,couleur,couleur))
                            """créationd la surface et remplissage selon le
                            gradiant de couleur"""
                    compt = compt + 1
                    """incrémentation du compteur"""
                    yLigne = 140
                    """offset de la premiere ligne"""
                    for l in range(5):
                        """pour chacune des 5 lignes"""
                        self.PGSurface.subsurface(x,yLigne,self.largeurST,2)\
                        .fill((0,0,0))
                        """création dune surface noire"""
                        yLigne = yLigne + 30
                        """décalage de l'ofset pour la ligne suivante"""

            self.PGSurface.blit(pygame.image.load("image/dièseV2.png"),(0,213))
            """brouillon. blit d'une image a une position donnée"""



            x = compt * self.largeurST
            self.PGSurface.subsurface(x-6,140,6,120).fill((0,0,0))
            """dessin de la berz marquant la fin de la mesure"""


        scale = 1/2
        """définition du zoom"""
        scaleX = self.longSurfPortée * scale
        scaleY = self.hauteurPortée * scale
        """mise a l'échelle de la hauteur et de la largeur"""
        self.PGSurface = pygame.transform.scale(self.PGSurface, (int(scaleX), int(scaleY)))
        """mise a l'échelle de la surface pygame"""
        self.parent.blit(self.PGSurface,(self.origineX,self.origineY))
        pygame.display.flip()
        """affichage de la surface et rafraichissement"""



class Portée:
    def __init__(self,arg):
        # nombre de note de la portee
        totalNote = 19
        # on regle la longeur de la surface portée en fonction du nombre de note
        longeurPortee = 100*totalNote
        #création de la surface contenant la portée
        portee = pygame.Surface((longeurPortee,400))
        portee.fill((200,200,200))
        # offset de la premiere ligne
        x = 0
        ligne = list()

        # 19 : la note la plus haute qu'on peu jouer
        hauteurNote = 19

        for j in range(totalNote):
            #print(hauteurNote)
            # offset de la premiere ligne
            y = 140
            for i in range(5):
                ligne.append(portee.subsurface(x,y,100,2).fill((0,0,0)))
                #decalage entre deux lignes
                y = y + 30
            y = 140
            if hauteurNote > 15 :
                ligne.append(portee.subsurface(x+25,y-30,50,2).fill((0,0,0)))
            if hauteurNote > 17 :
                ligne.append(portee.subsurface(x+25,y-60,50,2).fill((0,0,0)))
            if hauteurNote < 5 :
                ligne.append(portee.subsurface(x+25,y+150,50,2).fill((0,0,0)))
            if hauteurNote < 3 :
                ligne.append(portee.subsurface(x+25,y+180,50,2).fill((0,0,0)))
            # offset de la note
            ynote = y + 91
            xnote = x + 10
            # modification de l'offset en fonction de la hauteur de la note
            for i in range(hauteurNote):
                ynote = ynote - 15
            note = pygame.image.load("image/blancheV2.png")
            portee.blit(note,(xnote,ynote))
            if j == 0:
                bemole =  pygame.image.load("image/bemole.png")
                portee.blit(bemole,(xnote-10,ynote+75))
            if j == 4:
                diese =  pygame.image.load("image/diese.png")
                portee.blit(diese,(xnote-10,ynote+85))
            if j == 6:
                becare =  pygame.image.load("image/becare.png")
                portee.blit(becare,(xnote-10,ynote+87))

            # décalage de l'offset pour la ligne suivante
            x = x + 100
            # accessoire, permet de changer de note
            hauteurNote = hauteurNote -1
        # definition de l'echele de la portee
        scale = 1/3

        scaleX = longeurPortee * scale
        scaleY = 400 * scale
        # mise a l'echelle de la surface portee
        portee = pygame.transform.scale(portee, (int(scaleX), int(scaleY)))



        arg.blit(portee,(10,10))
        pygame.display.flip()