#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 23:09:28 2020

@author: j
"""

import solfege as SF
from solfege import TC

print("##############################################")

#a = SF.Note()
#a.reset(nomFr = "ré", alt = "bémole")
#a.info()
#print("##############################################")
#
#b = SF.Tonal(tonique = a, mode = TC.tonal_M)
#b.info()
#b.reset(nomFr = 'fa')
#b.info()
#print("##############################################")
#
#c = SF.Mesure(nbTps = 3, nbSTps = 4)
#c.info()
#print("##############################################")

d = SF.Motif(nomFr = "do", alt = '', nbTps = 2)
d.info()
print("##############################################")
