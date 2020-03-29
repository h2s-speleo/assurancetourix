#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Rythme:
    def __init__(self):
        self.parent = None
        self.listNote = list()
        self.listRythme = list()
        self.listeMessag = list()

    def info(self):


        print('liste note')
        print()
        for i in range(len(self.listNote)):
            print(self.listNote[i].degre, end = ' - ')
            print(self.listNote[i].nomFr, end = ' ')
            print(self.listNote[i].alt)

        print()
        print('liste durée')
        print()
        for i in range(len(self.listRythme)):
            print(i, end = ' - ')
            print(self.listRythme[i]['note'].nomFr, end = ' p : ')
            print(self.listRythme[i]['position'], end = ' d : ')
            print(self.listRythme[i]['duree'], end = ' - ')
            print(self.listRythme[i]['methode'])

        print()
        print('liste message')
        print()
        for i in range(len(self.listeMessag)):
            print(i, end = ' : ')
            if self.listeMessag[i] == []:
                print([])
            else :
                for j in range(len(self.listeMessag[i])):
                    print(self.listeMessag[i][j])


