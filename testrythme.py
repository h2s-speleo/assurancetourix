#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 17:38:55 2020

@author: j
"""

import random
import time


nombreTemps = 3
"""nombre de temps d'une mesure"""
nombreSTemps = 2
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
probTotal = 80
probTF = 100 *probTotal/100
probTf = 25 *probTotal/100
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

for i in range(len(listeSequence2)) :
    print(listeSequence2[i], end = ' ')

print()



