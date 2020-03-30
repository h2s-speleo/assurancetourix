#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 15:55:15 2020

@author: j
"""
import solfege as SF
from solfege.TCores import TC


class Tonal:
    """création de la tonalité a partir d'un tuple, si le tupple est vide
    on utiles les valeurs par défaut définie si dessous. sinon on utilise
    les éléments du tupples dans cet odre :
        1 - mode
        2 - ton
        3 - altération
        4 - octave
    ces arguments permetent de créer une liste d'objet solfege.Note stoqué
    dans self.gamme qui comprend les octave i-1, i, i+1, i+2"""

    def __init__(self,**kwargs):
        self.mode = kwargs.get('mode', TC.tonal_M) # = échelle d'interval
        self.parent = None
        self.tonique = SF.Note()
        self.gamme = list()
        """création de la liste de note"""

        self.reset(**kwargs)

    def reset(self, **kwargs):
        if 'tonique' in kwargs.keys():
            if 'nMidi' in kwargs.keys()\
            or 'nOcta' in kwargs.keys()\
            or 'alt' in kwargs.keys()\
            or 'nomFr' in kwargs.keys():
                raise AttributeError("EREURE : Un objet Tonal peut etre définit"
                                     +" par un objet solfege.Note mais dans ce"
                                     +" cas le seul autre argument accepté est mode")
            else:
                self.tonique = kwargs.get('tonique', self.tonique)
        else :
            if 'nMidi' in kwargs.keys():
                raise AttributeError("EREURE : Un objet Tonal ne peut pas etre"
                                     +" définit par un nMidi")
            else:
                self.tonique = SF.Note(**kwargs)

        ecartTotal = 0
        """initialisation de la variable ecartTotal qui décrit la distance
        entre les premiers degrés de deux octaves"""
        self.listeDegre = list()
        nMidi = self.tonique.nMidi

        for i in range(len(self.mode)):
            """pour chaque écart du mode"""
            ecartTotal =ecartTotal + self.mode[i]
            """on ajoute la valeur de l'écart a ecartTotal"""
        nMidi = self.tonique.nMidi - ecartTotal
        """on redéfinit self.nMidi pour commencer la liste un ocatave plus bas"""
        for j in range(4):
            """ permet de définir le nombre de note dans la gamme.
            pour les 4 octaves a construire"""
            for i in range(len(self.mode)):
                """pour chacun des écarts qui définnissent le mode"""
                self.listeDegre.append([nMidi])
                """on ajoute le Nmidi à la liste"""
                nMidi = nMidi + self.mode[i%len(self.mode)]
                """on ajoute nMidi + écart"""
        debut = 0
        compt = 0
        listeNom = list()
        self.gamme = list()
        for i in range(len(self.listeDegre)*2):
            """pour chaque degré de la liste * 2. permet de compenser le
            fait que l'on commence la recherche pas forcément au début de
            la liste"""
            listeNom.append(TC.do_re_mi[i%len(TC.do_re_mi)])
            """on ajoute la valeur de do_re_mi a la liste de nom"""



        for i in range(len(listeNom)):
            """ pour chaque element de la liste dorémi que l'on vient de créer"""
            if listeNom[i]== self.tonique.nomFr:

                """lorsque l'on trouve la valeur qui définit le ton"""
                debut = 1
                """ on comence a compter"""
            if debut ==1:
                """si on a commencé a compter"""
                self.listeDegre[compt].append(listeNom[i])
                """on atribue un nomFr a la liste de degré"""
                compt = compt + 1
            if compt == len(self.listeDegre):
                """si on a donné un nom FR a tous les degré"""
                break
                """on arrete l'itération"""


        for i in range(len(self.listeDegre)):
            """pour chaque degré de la liste"""
            ref = TC.tab_nMidi.index(self.listeDegre[i][0])
            """ref stoque l'index (int) du nMidi dans la table de
            correspondance accessible dans TCores"""
            nOcta =  TC.tab_nOcta[ref]
            """on définit l'octave du degré a parir de ref"""
            self.gamme.append(SF.Note())
            """on crée une note qui est stoquée dans self.gamme"""
            self.gamme[i].nMidi = self.listeDegre[i][0]
            self.gamme[i].nOcta = nOcta


            self.gamme[i].nomFr = self.listeDegre[i][1]
            """on redéfinit les atributs de la note"""
            self.gamme[i].defAlt()
            """on définit l'altération en fonction de la tonalité"""
            self.gamme[i].degre = i - len(self.mode)+1
            """on définit le numéro du degré"""
            self.gamme[i].tonal = self


    def info(self):
        """permet d'afficher dfes info sur la gamme"""
        for i in range(len(self.gamme)):
            """pour chaque note de la gamme"""
            self.gamme[i].info()
            """on lance la méthode info de la note"""
            if  self.gamme[i].degre % len(self.mode) == 0 :
                print('------------------------')
                """séparation entre les octaves"""