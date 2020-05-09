#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 19:04:55 2020

@author: j
"""

import time
import xmlrpc.client

class PyoClient():
    def __init__(self):
        print ('init')
        self.run()
    
    def run(self):
        self.server = xmlrpc.client.ServerProxy('http://127.0.0.1:1233')
        rep=self.server.is_pyostarted()
        
        if self.server.is_pyostarted():
            print('server run pyo is running')
        else:
            print('server run pyo is notrunning')
            self.server.pyoinitmessage()
            
    def send(self,cmd):
        self.server.pyocmd(cmd)
 
if __name__ == '__main__':
    pyo_rpc = PyoClient()
    
    #pyo_rpc.initMess.append('a = PWM(freq=100, phase=8, duty=0.5, damp=0, mul=1, add=1)')
    
    
    listeCommande = [ 
                      'spktrm =  Sine(500)',\
                      'excite = Noise(0.2)', \
                      # LFOs to modulated every parameters of the Vocoder object.
                      'lf1 = Sine(freq=0.1, phase=random()).range(60, 100)',\
                      'lf2 = Sine(freq=0.11, phase=random()).range(1.05, 1.5)',\
                      'lf3 = Sine(freq=0.07, phase=random()).range(1, 20)',\
                      'lf4 = Sine(freq=0.06, phase=random()).range(0.01, 0.99)',\
                      'voc = Vocoder(spktrm, excite, freq=lf1, spread=lf2, q=lf3, slope=lf4, stages=32).out()']


                      
                      

    for i in range(len(listeCommande)):
            x = pyo_rpc.send(listeCommande[i])
            
    time.sleep(20)
    pyo_rpc.send('voc.stop()')

