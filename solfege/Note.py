#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from solfege.TCores import TC


class Note:
    """Classe définissant une note caractérisée par :
    - _nMidi : son numero midi
    - _nOcta : son numero d'octave
    - nomFr : son nom dans la convention française (do, ré, mi, fa)
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
        if len(kwargs) > 0 :
            self.reset(**kwargs)

    def reset(self, **kwargs):
        """définition de la note en fonction des paramètres donné a kwargs"""
        if 'nomFr' in kwargs.keys() and 'nMidi' in kwargs.keys():
            raise AttributeError("EREURE : Un objet note peut etre définit par"
                                 +"son nomFr (+ alt et nOcta en option) ou son"
                                 +"nMidi. pas les deux en même temps.")
        elif 'nMidi' in kwargs.keys():
            self.nMidi = kwargs.get('nMidi')
            self.midiToNom()
        else:
            self.nomFr = kwargs.get('nomFr', self.nomFr)
            self.alt = kwargs.get('alt', self.alt)
            self.nOcta = kwargs.get('nOcta', self.nOcta)
            self.nomToMidi()

    def midiToNom(self):
        """permet de générer le nom complet lorsque nMidi a été modifié.
        - lorsque l'atribut Tcores.systeme = modal : si la note n'est pas juste
            on lui ajoute un dièse"""
        ref = TC.tab_nMidi.index(self.nMidi)
        if TC.tab_nomFr[ref] == '':
            self.nomFr= TC.tab_nomFr[ref-1]
            self.alt = 'dièse'
            self.nOcta = TC.tab_nOcta[ref-1]
            """le nom devient celui de la note un demi ton en dessous"""
        else :
            self.nomFr = TC.tab_nomFr[ref]
            self.alt = ''
            self.nOcta = TC.tab_nOcta[ref]

    def nomToMidi(self):
        """défini le numéro midi, prend un objet solfege.Note en argument ou un
        tupple 0 : nomFr / 1 : alteration / 2 : octave"""
        for i in range(len(TC.tab_nOcta)):
            if TC.tab_nOcta[i] == self.nOcta:
                if TC.tab_nomFr[i] == self.nomFr:
                    ref = TC.tab_nMidi[i]
                    if self.alt == 'dièse':
                        ref = ref + 1
                    if self.alt == 'bémole':
                        ref = ref - 1
                    self.nMidi = TC.tab_nMidi[ref]

    def info(self):
        """print les info de la note"""
        print(str(self.degre)+' Midi = '+str(self.nMidi)+" / "+\
                    self.nomFr+' '+self.alt+' '+str(self.nOcta))

    def defAlt(self):
        """obtenir l'altération d'un degré"""
        ref = TC.tab_nMidi.index(self.nMidi)
        if TC.tab_nomFr[ref] == self.nomFr :
            self.alt = ''
        elif TC.tab_nomFr[ref+1] == self.nomFr :
            self.alt = 'bémole'
        elif TC.tab_nomFr[ref-1] == self.nomFr :
            self.alt = 'dièse'
