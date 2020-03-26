#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Note:
    """Classe définissant une note caractérisée par :
    - _nMidi : son numero midi
    - _nOcta : son numero d'octave
    - _nomFr : son nom dans la convention française (do, ré, mi, fa)
    - _alt : 'bémole', 'dièse', ''
    - _degre : degré de la note en chiffre arabe
    - _tonal : tonalité parente de la note"""

    def __init__(self, **kwargs):
        self.degre = int()
        self.tonal = None
        self.nMidi = 60
        self.nOcta = 3
        self.nomFr = "do"
        self.alt = ""
        self.reset(**kwargs)

    def reset(self, **kwargs):
        """définition de la note en fonction des paramètres donné a kwargs"""
        if 'nomFr' in kwargs.keys() and 'nMidi' in kwargs.keys():
            raise AttributeError("EREURE : Un objet note peut etre définit par"
                                 +"son nomFr (+ alt et nOcta en option) ou son"
                                 +"nMidi. pas les deux en même temps.")
        elif 'nMidi' in kwargs.keys():
            self.nMidi = kwargs.get('nMidi')
            #self.midiToNom()
        else:
            self.nomFr = kwargs.get('nomFr', self.nomFr)
            self.alt = kwargs.get('alt', self.alt)
            self.nOcta = kwargs.get('nOcta', self.nOcta)
            #self.nomToMidi()

    def info(self):
        """print les info de la note"""
        print(str(self.degre)+' Midi = '+str(self.nMidi)+" / "+\
                    self.nomFr+' '+self.alt+' '+str(self.nOcta))


