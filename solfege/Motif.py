#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import solfege as SF
from solfege.TCores import TC



class Motif:
    def __init__(self, **kwargs):
        self.compo = None
        self.melo = None
        self.harmo = None
        self.mesure = None
        self.parent = None

        self.mode = TC.tonal_M
        self.tonique = SF.Note()
        self.nMidi = 60
        self.nOcta = 3
        self.nomFr = "do"
        self.alt = ""
        self.nbTps = 3
        self.nbSTps = 2

        self.probTotal = 80
        self.probTpsFo = 100
        self.probTpsFa = 25

        self.longMax = 2
        self.longMin = 1
        self.cible = [5,1]

        self.reset(**kwargs)

    def reset(self, **kwargs):

        if 'tonique' in kwargs.keys():
            if 'nMidi' in kwargs.keys()\
            or 'nOcta' in kwargs.keys()\
            or 'alt' in kwargs.keys()\
            or 'nomFr' in kwargs.keys():
                raise AttributeError("EREURE : Un objet Motif peut etre définit"
                                     +" par un objet solfege.Note mais dans ce"
                                     +" cas il ne prend pas les attribute nMidi"
                                     +", nOcta, alt ou nomFr")
            else:
                self.tonique = kwargs.get('tonique', self.tonique)
                self.nOcta = self.tonique.nOcta
                self.alt = self.tonique.alt
                self.nomFr = self.tonique.nomFr
                self.nMidi = self.tonique.nMidi

        else :
            if 'nMidi' in kwargs.keys():
                raise AttributeError("EREURE : Un objet Tonal ne peut pas etre"
                                     +" définit par un nMidi")
            else:

                self.nOcta = kwargs.get('nOcta', self.nOcta)
                self.alt = kwargs.get('alt', self.alt)
                self.nomFr = kwargs.get('nomFr', self.nomFr)
                self.tonique = SF.Note(nomFr = self.nomFr, alt = self.alt, nOcta = self.nOcta)
                self.nMidi = self.tonique.nMidi

        self.mode = kwargs.get('mode', self.mode)
        self.nbTps = kwargs.get('nbTps', self.nbTps)
        self.nbSTps = kwargs.get('nbSTps', self.nbSTps)

        self.probTotal = kwargs.get('probToal', self.probTotal)
        self.probTpsFo = kwargs.get('probTpsFo', self.probTpsFo)
        self.probTpsFa = kwargs.get('probTpsFa', self.probTpsFa)

        self.longMax = kwargs.get('longMax', self.longMax)
        self.longMin = kwargs.get('longMin', self.longMin)
        self.cible = kwargs.get('cible', self.cible)



        self.melo = SF.Melo(tonique = self.tonique)
        self.melo.parent = self

#        self.harmo = Harmo()
#        self.harmo.parent = self

        self.mesure = SF.Mesure(nbTps = self.nbTps,
                             nbSTps = self.nbSTps)
        self.mesure.parent = self

        self.compo = SF.Compo(probTotal = self.probTotal,
                              probaTpsFa = self.probTpsFa,
                              probaTpsFo = self.probTpsFo,
                              longMax = self.longMax,
                              longMin = self.longMin,
                              cible = self.cible)
        self.compo.parent = self
        self.compo.Comp1()

    def info(self):
        print("#### tonalité #########################")
        self.melo.tonal.info()
        print()
        print("#### mesure #########################")
        self.mesure.info()
        print()
        print("#### rythme #########################")
        print()
        self.melo.rythme.info()
        print()
        print("#### compo #########################")
        self.compo.info()
