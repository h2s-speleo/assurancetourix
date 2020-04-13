 #!/usr/bin/env python3
# -*- coding: utf-8 -*-

from csv import reader

class TCores :
    def __init__(self):

        """définition des tonalité"""
        self.tonal_M = (2,2,1,2,2,2,1)
        self.tonal_m = (2,1,2,2,1,2,2)
        self.blues_M = (2,1,1,3,1)
        self.blues_m = (3,2,1,1,3)


        """écart de note entre les degrés d'une gamme"""
        self.inter = {'unisson':0,
                      'seconde':1,
                      'tierce':2,
                      'quarte':3,
                      'quinte':4,
                      'sixte':5,
                      'septieme':6,
                      'octave':7}

        """écart absolu en demi ton, correspond égallement a l'écart entre deux nMidi"""
        self.inter_a = {'secondem':1,
                      'secondeM':2,
                      'tiercem':3,
                      'tierceM':4,
                      'quarteJ':5,
                      'querteA':6,
                      'quinteJ':7,
                      'sixtem':8,
                      'sixteM':9,
                      'septiemem':10,
                      'septiemeM':11,
                       'octaveJ':12}

        self.do_re_mi = ('do',"ré",'mi','fa','sol','la','si')


        """charge le contenu d'un fichier csv dans des listes"""
        self.tab_nMidi = []
        self.tab_nomFr = []
        self.tab_nOcta = []
        with open('solfege/tableMidi.csv','r', encoding='utf-8-sig') as csvfile:
            tableMidi = reader(csvfile, delimiter=';')
            for row in tableMidi:
                self.tab_nMidi.append(int(row[0]))
                self.tab_nomFr.append(row[1])
                self.tab_nOcta.append(int(row[2]))

TC = TCores()
