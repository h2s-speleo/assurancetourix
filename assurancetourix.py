#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import subprocess
import iGraph


###############################################################################
serveurSon=subprocess.Popen("./serveurPyo.py", shell=True )
"""lancement du serveur son en subprocess"""

IG = iGraph.Fenetre()
###############################################################################

subprocess.Popen.kill(serveurSon)
"""on tue le subprocess"""
exit()
"""on quitte la terminal"""