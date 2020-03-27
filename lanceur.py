#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 23:09:28 2020

@author: j
"""

import solfege as SF
from solfege.TCores import TC



print("##############################################")
a = SF.Note()
a.reset(nomFr = "ré", alt = "bémole")
a.info()
print("##############################################")
b = SF.Tonal(tonique = a)
b.info()
print("##############################################")