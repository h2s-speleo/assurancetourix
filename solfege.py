#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
module de solphege v 1
Created on Sat Feb  8 16:03:09 2020

@author: j
"""

from copy import deepcopy


class Tonalité:
    def __init__(self,*args):
        """création de la tonalité a partir d'un tuple, si le tupple est vide
        on utiles les valeurs par défaut définie si dessous. sinon on utilise
        les éléments du tupples dans cet odre :
            1 - mode
            2 - ton
            3 - altération
            4 - octave
        ces arguments permetent de créer une liste d'objet solfege.Note stoqué
        dans self.gamme qui comprend les octave i-1, i, i+1, i+2"""

        self.mode = (2,2,1,2,2,2,1) # = échelle d'interval, peut etre stoqué
        # dans des variables. des intervalles sont proposés dans TCores
        self.ton = 'do'
        self.alteration = ''
        self.nOctave = 3
        self.nMidi = 60
        """arguments par défaut"""
        self.gamme = list()
        """création de la liste de note"""


        if len(args) > 0:
            self.mode = args[0]
        if len(args) > 1:
            self.ton = args[1]
        if len(args) > 2:
            self.alteration = args[2]
        if len(args) > 3:
            self.nOctave = args[3]-1
        """on remplace les atributs par défaut en fonction de la longeure de
        l'argument donné"""
        self.nMidi = TC.nomCToMidi((self.ton, self.alteration, self.nOctave))
        """définition du nMidi a partir des atributs ton, alteration et
        octave"""

        ecartTotal = 0
        """initialisation de la variable ecartTotal qui décrit la distance
        entre les premiers degrés de deux octaves"""
        for i in range(len(self.mode)):
            """pour chaque écart du mode"""
            ecartTotal =ecartTotal + self.mode[i]
            """on ajoute la valeur de l'écart a ecartTotal"""
        self.nMidi = self.nMidi - ecartTotal
        """on redéfinit self.nMidi pour commencer la liste un ocatave plus bas"""


        listeDegre = list()
        debut = 0
        listeNom = list()
        compt = 0

        for j in range(4):
            """ permet de définir le nombre de note dans la gamme.
            pour les 4 octaves a construire"""
            for i in range(len(self.mode)):
                """pour chacun des écarts qui définnissent le mode"""
                listeDegre.append([self.nMidi])
                """on ajoute le Nmidi à la liste"""
                self.nMidi = self.nMidi + self.mode[i%len(self.mode)]
                """on ajoute nMidi + écart"""
        sauvegarde = deepcopy(listeDegre)
        """on sauvegarde la liste dans la variable sauvegarde"""
        try :
            """on tente de définire les note selon le système tonal"""
            for i in range(len(listeDegre)*2):
                """pour chaque degré de la liste * 2. permet de compenser le
                fait que l'on commence la recherche pas forcément au début de
                la liste"""
                listeNom.append(TC.doRémi[(i%len(self.mode))])
                """on ajoute la valeur de dorémi a la liste de nom"""
            for i in range(len(listeNom)):
                """ pour chaque element de la liste dorémi que l'on vient de créer"""
                if listeNom[i]== self.ton:
                    """lorsque l'on trouve la valeur qui définit le ton"""
                    debut = 1
                    """ on comence a compter"""
                if debut ==1:
                    """si on a commencé a compter"""
                    listeDegre[compt].append(listeNom[i])
                    """on atribue un nomFr a la liste de degré"""
                    compt = compt + 1
                if compt == len(listeDegre):
                    """si on a donné un nom FR a tous les degré"""
                    break
                    """on arrete l'itération"""
            for i in range(len(listeDegre)):
                """pour chaque degré de la liste"""
                ref = TC.ListeNMidi.index(listeDegre[i][0])
                """ref stoque l'index (int) du nMidi dans la table de
                correspondance accessible dans TCores"""
                octa =  TC.ListeNOctave[ref]
                """on définit l'octave du degré a parir de ref"""
                self.gamme.append(Note())
                """on crée une note qui est stoquée dans self.gamme"""
                self.gamme[i]._nMidi = listeDegre[i][0]
                self.gamme[i]._nOctave = octa
                self.gamme[i]._nomFr = listeDegre[i][1]
                """on redéfinit les atributs de la note"""
                self.gamme[i]._alteration = TC.defAlt(listeDegre[i])
                """on définit l'altération en fonction de la tonalité"""
                self.gamme[i]._degré = i - len(self.mode)+1
                """on définit le numéro du degré"""
                self.gamme[i]._gamme = self.gamme
                self.gamme[i]._mode = self.mode
                self.gamme[i]._ton = (self.ton, self.alteration)
                """on stoque les info sur la gamme en le mode"""
            print('tonal')
        except:
            """si on a échoué a définir la gamme de maniere tonale on bascule
            sur le modal"""
            listeDegre = deepcopy(sauvegarde)
            """on rétablit la listeDegre a partir de la sauvegarde"""
            self.gamme = list()
            """on vide la liste self.gamme"""

            for i in range(len(listeDegre)):
                """pour chaque degré de la liste"""
                self.gamme.append(Note())
                """on crée une note"""
                self.gamme[i].nMidi = listeDegre[i][0]
                """on modifie la note en fonction de son nMidi"""

                self.gamme[i]._degré = i - len(self.mode)+1
                """on définit le numéro du degré"""
                self.gamme[i]._gamme = self.gamme
                self.gamme[i]._mode = self.mode
                self.gamme[i]._ton = (self.ton, self.alteration)
                """on stoque les info sur la gamme en le mode"""
            print('modal')

    def info(self):
        """permet d'afficher dfes info sur la gamme"""
        for i in range(len(self.gamme)):
            """pour chaque note de la gamme"""
            self.gamme[i].info()
            """on lance la méthode info de la note"""
            if  self.gamme[i]._degré %  len(self.mode) == 0 :
                print('------------------------')
                """séparation entre les octaves"""




class Note: # Définition de notre classe Note
    """Classe définissant une note caractérisée par :
    - _nMidi : son numero midi
    - _nOctave : son numero d'octave
    - _nomFr : son nom dans la convention française (do, ré, mi, fa)
    - _alteration : bémole, diese, bécare, base
    - _degré : degré de la note en chiffre arabe
    - _gamme : nom de la gamme
    - _durée : durée de la note
    - _mode : nom du mode"""

    def __init__(self): # Notre méthode constructeur
        """tout les atribut sont vide car lils se calculent différament en
        fonction de l'atribut initial"""
        self._nMidi = 60
        self._nOctave = 3
        self._nomFr = "do"
        self._alteration = ""
        self._degré = int()
        self._gamme = str()
        self._mode = str()
        self._ton = ''
        self._durée = 1

    def _get_nMidi(self):
        """méthode pour récupérer le numero midi de la note"""
        return self._nMidi

    def _set_nMidi(self, arg):
        """ attrubution de valeur a _nMidi, _ nomFr, _alteration et _nOctave a
        partir du numero midi de la note. un objet TCores doit déja avoir été
        appelé pour que la methode fonctionne"""
        self._nMidi = arg
        TC.midiToNomC(self)
        """atribution d'une valeur nomFr la methode TCores.midiToNomC"""
        TC.midiToNomC(self)
        """atribution d'une valeur à _nOctave la methode TCores.midiToNomC"""
    nMidi = property(_get_nMidi, _set_nMidi)

    def _get_nomFr(self):
        """méthode pour récupérer le nom français de la note"""
        return self._nomFr

    def _set_nomFr(self,arg):
        """ attrubution de valeur a _nMidi, _ nomFr, _alteration et _nOctave a
        partir du nom français de la note. un objet TCores doit déja avoir été
        appelé pour que la methode fonctionne.
        on peut donner a la méthode soit un str() dans ce cas l'altération et
        l'octave restent inchangé, soit un tuple qui modifie l'altération et
        l'octave"""
        if type (arg) == tuple :
            self._nomFr = arg[0]
            if len(arg) > 1:
                self._alteration = arg[1]
                if len(arg) > 2:
                    self._nOctave = arg[2]
                    if len(arg) > 3:
                        print("erreure = _set_nomFr prend trois arguments max")
        if type(arg) == str :
            self._nomFr = arg
        TC.nomCToMidi(self)
    nomFr = property(_get_nomFr, _set_nomFr)

    def _get_nOctave(self):
        """méthode pour récupérer l'octave de la note"""
        pass

    def _set_nOctave(self,arg):
        """atribution changement de la valeur de nOctave et de nMidi en fonction"""
        self._nOctave = arg
        TC.nomCToMidi(self)

    def info(self):
        print(str(self._degré)+' Midi ='+str(self._nMidi)+" / "+\
                    self._nomFr+' '+self._alteration+' '+str(self._nOctave))


        """
        print("nMidi =      " + str(self._nMidi))
        print("nomFr =      " + str(self._nomFr))
        print("alteration = " + str(self._alteration))
        print("nOctave =    " + str(self._nOctave))
        """

class TCores :
    """ classe permetant de créer un ensemble de variable utilisés par le
    module. doit etre appelé au début du script pour que les autes classes
    fonctionent.les variable sont accessible via un objet. cet objet est déclaré
    comme variable global pour ettre accessible par les autres classe du module.
    pour etre accessible en dehors du module, l'objet doit etre stoqué dans une
    variable dans le script principal"""

    def __init__(self):
        """charge le contenu d'un fichier csv dans les attributs de l'objets"""
        import csv
        """ création des listes"""
        self.ListeNMidi = []
        self.ListenomFr = []
        self.ListeNOctave = []
        #self.systeme = 'modal'
        with open('tableMidi.csv','r') as csvfile:
            """ouverture du fichier csv"""
            tableMidi = csv.reader(csvfile, delimiter=';')
            """chargement du contenu dans la variable table Midi"""
            for row in tableMidi:
                """pour chaque ligne"""
                try :
                    """perment d'emecher le caractere de fin"""
                    self.ListeNMidi.append(int(row[0]))
                except :
                    pass
                self.ListenomFr.append(row[1])
                self.ListeNOctave.append(int(row[2]))
        self.ListeNMidi.reverse()
        self.ListenomFr.reverse()
        self.ListeNOctave.reverse()
        """inversion des listes pour que les valeurs de ListeMidi soit égal à
        l'indexe. tuple de tuple"""
        self.interN = (('unisson',0),('seconde',1),('tierce',2),('quarte',3),
                       ('quinte',4),('sixte',5),('septieme',6),('octave',7))
        """écart de note entre les degrés d'une gamme"""
        self.interM =(('secondem',1),('secondeM',2),('tiercem',3),('tierceM',4),
                      ('quarteJ',5),('querteA',6),('quinteJ',7),('sixtem,8'),
                      ('sixteM',9),('septiemem',10),('septiemeM',11),
                      ('octaveJ',12))
        """écart absolu en demi ton, correspond égallement a l'écart entre deux
        nMidi, tuple de tuple"""
        self.doRémi = ('do',"ré",'mi','fa','sol','la','si')

        """definition des tonalités"""
        self.tonalM = (2,2,1,2,2,2,1)
        self.tonalm = (2,1,2,2,1,2,2)

        self.bluesM = (2,1,1,3,1)
        self.bluesm = (3,2,1,1,3)

        global TC
        """déclaration de la variable globale TC. elle est désormai
        accessible par toutes les classe du module"""
        TC = self

    def midiToNomC(self, arg):
        """permet de générer le nom complet lorsque nMidi a été modifié.
        - lorsque l'atribut Tcores.systeme = modal : si la note n'est pas juste
            on lui ajoute un dièse"""
        if type(arg) == Note :
            ref = self.ListeNMidi.index(arg._nMidi)
            """récupération de l'indexe du numéro midi dans la liste. on pourait
            prendre directement le numero midi comme argument puisqu'il est
            théoriquement égal a son indexe"""
            if self.ListenomFr[ref] == '':
                """si le numéro ne renvoie pas a une note juste"""
                arg._nomFr= self.ListenomFr[ref-1]
                arg._alteration = 'dièse'
                arg._nOctave = self.ListeNOctave[ref-1]
                """le nom devient celui de la note un demi ton en dessous"""
            else :
                arg._nomFr = self.ListenomFr[ref]
                """atribution du nom a partir de la liste"""
                arg._alteration = ''
                arg._nOctave = self.ListeNOctave[ref]
        else :
            raise AttributeError('EREURE : nomCToMidi prend un objet solfege.Note en argument')



    def defAlt(self, arg):
        """obtenir l'altération d'un degré a partir d'une liste [nMidi, nomFr]"""

        if type(arg) == list:
            ref = self.ListeNMidi.index(arg[0])
            """récupération de l'indexe du numéro midi dans la liste. on pourait
            prendre directement le numero midi comme argument puisqu'il est
            théoriquement égal a son indexe"""
            if self.ListenomFr[ref] == arg[1]:
                alt = ''
            elif self.ListenomFr[ref+1] == arg[1]:
                alt = 'bémole'
            elif self.ListenomFr[ref-1] == arg[1]:
                alt = 'dièse'
            return alt
        else :
            raise AttributeError('EREURE : defAlt prend une liste [nMidi,nomFr]\
                                 en argument')


    def nomCToMidi(self, arg):
        """défini le numéro midi, prend un objet solfege.Note en argument ou un
        tupple 0 : nomFr / 1 : alteration / 2 : octave"""
        if type(arg) == Note :
            for i in range(len(self.ListeNOctave)):
                if self.ListeNOctave[i] == arg._nOctave:
                    if self.ListenomFr[i] == arg._nomFr:
                        ref = self.ListeNMidi[i]
                        if arg._alteration == 'dièse':
                            ref = ref + 1
                        if arg._alteration == 'bémole':
                            ref = ref - 1
                        arg._nMidi = ref

        if type(arg) == tuple :
            for i in range(len(self.ListeNOctave)):
                if self.ListeNOctave[i] == arg[2]:
                    if self.ListenomFr[i] == arg[0]:
                        ref = self.ListeNMidi[i]
                        if arg[1] == 'dièse':
                            ref = ref + 1
                        if arg[1] == 'bémole':
                            ref = ref - 1
                        return ref

        else :
            raise AttributeError('EREURE : nomCToMidi prend un objet \
                                 solfege.Note ou un tupple en argument (0 : \
                                 nomFr / 1 : alteration / 2 : octave)')