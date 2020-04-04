#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyo import *


class Mess():

    def __init__(self, arg):

        self.AS = arg
        self.OSC = Osc(arg)
        self.ENV = Env(arg)
        self.osc = "simpleSine"
        self.env = "simpleAdsr"
        self.AS.info(self)
        
        
    def ResetMess(self, **kwargs):
        print('RESET MESSAGE')
#        self.AS.IGVar['listeMess']=list()
        self.osc = kwargs.get('osc', self.osc)
        self.env = kwargs.get('osc', self.env)
        
        pas = self.AS.motif.melo.rythme.listeMessag
        self.AS.IGVar['listeMess'] = list()
        self.AS.IGVar['longLisMess'] = len(pas)
        self.AS.IGVar['indiceMess'] = 0
        for i in range(len(pas)):
            self.AS.IGVar['listeMess'].append(list())
            if len(pas[i]) > 0:
                for j in range(len(pas[i])):
                    if pas[i][j][2] not in self.AS.IGVar['listeVoix'] :
                        self.AS.IGVar['listeVoix'].append(pas[i][j][2])
                        
            
        self.AS.IGVar['longLisMess'] = len(self.AS.IGVar['listeMess'])
        
        self.AS.IGVar['objPyoActif'] = dict()
        if 'M' in self.AS.IGVar['listeVoix'] :
            self.ResMesM()
 
        self.AS.info(self)  
            
    def ResMesM(self):
        print('RESET MESSAGE MELODIE')
        # definition des message init/stop/pause/play
        self.AS.IGVar['objPyoActif']['init']=list()
        self.AS.IGVar['objPyoActif']['kill']=list()
        self.AS.IGVar['objPyoActif']['pause']=list()
        self.AS.IGVar['objPyoActif']['play']=list()
        self.AS.IGVar['objPyoActif']['nom']=list()

        if self.env == "simpleAdsr" :
            self.ENV.simpleAdsr('M')
        if self.osc == "simpleSine" :
            self.OSC.SimpleSine('M')

#        for key, value in self.AS.IGVar['objPyoActif'].items():
#            print('--------------------------------')
#            print(key)
#            print()
#            for i in range(len(value)):
#                print(value[i])   
#        print()
#        for i in range(len(self.AS.IGVar['listeMess'])):
#            for j in range(len(self.AS.IGVar['listeMess'][i])):
#                print(self.AS.IGVar['listeMess'][i][j])
#            print()

        self.AS.info(self)
            
    def putBasMess(self, typ ):
        print('PUT BASE MESAGE')
        for i in range(len(self.AS.IGVar['objPyoActif'][typ])):
            self.AS.qSon.put(self.AS.IGVar['objPyoActif'][typ][i])
        
        self.AS.info(self)
            
    def putSeqMess(self):
        
        
        if self.AS.IGVar['playing']== 1:

            if self.AS.IGVar['indiceMess'] >=  self.AS.IGVar['longLisMess'] :
                self.AS.IG.Stop()
            else:

    
                pas = self.AS.IGVar['listeMess'][self.AS.IGVar['indiceMess']]
                if len(pas) > 0:
                    for i in range(len(pas)):
                        
                        


                        self.AS.qSon.put(pas[i])
            self.AS.IGVar['indiceMess'] = self.AS.IGVar['indiceMess'] + 1

            self.AS.info(self)
class Osc():

    def __init__(self, arg):

        self.AS = arg

        self.AS.info(self)
        
        
    def SimpleSine(self, voix):

#        .append('oscM = Sine(mul = envM)')  
#        .append('oscM = Sine(mul = LFO(type=7, freq= 500 ,mul =envM))')
#        .append('oscM = Sine(mul = RCOsc(mul =envM))')
#        .append('oscM = Sine(mul = Sine( mul =envM))')
#        .append('oscM = Phaser(Sine(mul = Sine( mul =envM)))')
#         .append('oscM = LFO(mul = envM, type=7)')
        
        
        
        self.AS.IGVar['objPyoActif']['nom']\
        .append('oscM')
        self.AS.IGVar['objPyoActif']['init']\
        .append('oscM = SineLoop(mul = envM)')
        self.AS.IGVar['objPyoActif']['init']\
        .append('oscM.out()')
        self.AS.IGVar['objPyoActif']['kill']\
        .append('oscM.stop()')
#        self.AS.IGVar['objPyoActif']['pause']\
#        .append('oscM.setMul(0)')
#        self.AS.IGVar['objPyoActif']['play']\
#        .append('oscM.setMul(envM)')
        
        OSC = str("osc" + voix)
        ENV = str("env" + voix)
        
        
        for i in range(len(self.AS.motif.melo.rythme.listeMessag)):
            pas = self.AS.motif.melo.rythme.listeMessag[i]
            
            if len(pas) > 0:
                for j in range(len(pas)):
                    if pas[j][2] == voix :
                        FREQ =  str(pas[j][1].nMidi)

                        if pas[j][0] == 'note_on':
                            mess = str(OSC+'.setFreq(midiToHz(' + FREQ + '))')
                            self.AS.IGVar['listeMess'][i].append(mess)


        self.AS.info(self)  

class Env():
    
    def __init__(self, arg):
        self.AS = arg

        self.AS.info(self)
        
    
    def simpleAdsr(self, voix):

        
        self.AS.IGVar['objPyoActif']['nom']\
        .append('adsrM')
        self.AS.IGVar['objPyoActif']['nom']\
        .append('envM')
        self.AS.IGVar['objPyoActif']['init']\
        .append('adsrM = Adsr(attack=1, decay=.5, sustain=.5, release=.4, dur=0, mul=1)')
        self.AS.IGVar['objPyoActif']['init']\
        .append('envM = Port(adsrM, risetime=0.01, falltime=0.05)')
        self.AS.IGVar['objPyoActif']['kill']\
        .append('envM.stop()')
        self.AS.IGVar['objPyoActif']['kill']\
        .append('adsrM.stop()')
        self.AS.IGVar['objPyoActif']['pause']\
        .append('adsrM.stop()')


        

        ADSR = str("adsr" + voix)
        
        for i in range(len(self.AS.motif.melo.rythme.listeMessag)):
            pas = self.AS.motif.melo.rythme.listeMessag[i]
            if len(pas) > 0:
                for j in range(len(pas)):
                    if pas[j][2] == voix :
                        if pas[j][0] == 'note_on':
                            mess = str(ADSR+".play()")
                            self.AS.IGVar['listeMess'][i].append(mess)
                        if pas[j][0] == 'note_off':
                            mess = str(ADSR+".stop()")
                            self.AS.IGVar['listeMess'][i].append(mess)
            

        self.AS.info(self)