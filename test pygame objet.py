#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 18:26:10 2020

@author: j
"""

# la section qui suit est un peu chelou mais j'ai pas ajouté le module solfege
# au PATH.
import sys
import subprocess
import mido





pathSolfege = "./solfege"
pathIGraph = "./iGraph"
sys.path.append(pathSolfege)
sys.path.append(pathIGraph)

import iGraph
import solfege
TC = solfege.TCores()


###############################################################################



serveurSon=subprocess.Popen("./OK_serveurMidiPyo.py", shell=True )
"""lancement du serveur son en subprocess"""




IG = iGraph.Fenetre()
IG.start()




###############################################################################

subprocess.Popen.kill(serveurSon)
"""on tue le subprocess"""
exit()
"""on quitte la terminal"""



# définition d'une gamme
#a = solfege.Tonalité((2,1,1,3,1),'mi')

# info sur la gamme
#a.info()
