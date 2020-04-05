#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyo import *
import time


class Mess():

    def __init__(self, arg):

        self.AS = arg
        self.OSC = Osc(arg)
        self.ENV = Env(arg)
        self.osc = "simpleSine"
        self.env = "simpleAdsr"
        #self.AS.info(self)  
        self.millis = int(round(time.time() * 1000))

        
        
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
 
    ##    self.AS.info(self)  
            
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

#        self.AS.info(self)
            
    def putBasMess(self, typ ):
        print('PUT BASE MESAGE : ' + str(typ))
        for i in range(len(self.AS.IGVar['objPyoActif'][typ])):
            self.AS.qSon.put(self.AS.IGVar['objPyoActif'][typ][i])
            print('-----------------------------------------')
            print(self.millis - int(round(time.time() * 1000)), end = ' : ')
            print(self.AS.IGVar['objPyoActif'][typ][i])
            self.millis = int(round(time.time() * 1000))  
        
#        self.AS.info(self)
            
    def putSeqMess(self):
        
        
        if self.AS.IGVar['playing']== 1:
            

            if self.AS.IGVar['indiceMess'] >=  self.AS.IGVar['longLisMess'] :
                self.AS.IG.Stop()
            else:
                pas = self.AS.IGVar['listeMess'][self.AS.IGVar['indiceMess']]
#                print(self.millis - int(round(time.time() * 1000)))
#                self.millis = int(round(time.time() * 1000))
                if len(pas) > 0:
#                    print(self.millis - int(round(time.time() * 1000)))
#                    self.millis = int(round(time.time() * 1000))    
                    for i in range(len(pas)):
                        print('-----------------------------------------')
                        print(self.millis - int(round(time.time() * 1000)), end = ' : ')
                        print(pas[i])
                        self.millis = int(round(time.time() * 1000))  
                        self.AS.qSon.put(pas[i])
                          
                        
            self.AS.IGVar['indiceMess'] = self.AS.IGVar['indiceMess'] + 1

#            self.AS.info(self)
class Osc():

    def __init__(self, arg):

        self.AS = arg

        #self.AS.info(self)  
        
        
    def SimpleSine(self, voix):

#        .append('oscM = Sine(mul = envM)')  
#        .append('oscM = Sine(mul = LFO(type=7, freq= 500 ,mul =envM))')
#        .append('oscM = Sine(mul = RCOsc(mul =envM))')
#        .append('oscM = Sine(mul = Sine( mul =envM))')
#        .append('oscM = Phaser(Sine(mul = Sine( mul =envM)))')
#         .append('oscM = LFO(mul = envM, type=7)')
#        .append('oscM = SineLoop(mul = envM)')       
#        .append('oscM = Sine(freq = [440,440], mul = LFO(mul = envM, type=2, freq = 50))') 
        
#           .append('filtre = WGVerb(MoogLP(oscM,freq= oscM._freq[-1])).out()')
######################################################################################        
#        .append('filtre = Waveguide(Disto(MoogLP(oscM,freq= oscM._freq[0]))).out()')    
#        .append('filtre = STRev(Waveguide(Disto(MoogLP(oscM,freq= oscM._freq[0])))).out()')
#        .append('filtre = Waveguide(Chorus(Disto(MoogLP(oscM,freq= oscM._freq[0])))).out()')
#        .append('filtre = Waveguide(FreqShift(Disto(MoogLP(oscM,freq= oscM._freq[0])))).out()')
#        .append('filtre = Waveguide(WGVerb(Chorus(Disto(MoogLP(oscM,freq= oscM._freq[0]))))).out()')
#        .append('filtre = Waveguide(Harmonizer(Chorus(Disto(MoogLP(oscM,freq= oscM._freq[0]))))).out()')
#        .append('filtre = Waveguide(STRev(Chorus(Disto(MoogLP(oscM,freq= oscM._freq[0]))))).out()')

        
######################################################################################
#self.AS.IGVar['objPyoActif']['init']\
#.append('oscM = Sine(freq = [440,440], mul = LFO(mul = envM, type=7, freq = 200))')  
#.self.AS.IGVar['objPyoActif']['init']\
#.append('filtre = Waveguide(Harmonizer(Disto(MoogLP(oscM,freq= oscM._freq[0])))).out()')
#.append('filtre = STRev(Waveguide(Disto(MoogLP(oscM,freq= oscM._freq[0])))).out()')


######################################################################################
#        self.AS.IGVar['objPyoActif']['nom']\
 #       .append('oscM')
  #      self.AS.IGVar['objPyoActif']['init']\
   #     .append('oscM = Sine(freq = [440,600], mul = (LFO(mul = envM, type=2, freq = 200)))')  
    #    self.AS.IGVar['objPyoActif']['init']\
     #   .append('signal = MoogLP(oscM.mix(),oscM._freq[0])')
      #  self.AS.IGVar['objPyoActif']['init']\
       # .append('filtre = Waveguide(Harmonizer(Disto(signal))).out()')
        #self.AS.IGVar['objPyoActif']['kill']\
        #.append('oscM.stop()')

######################################################################################
        
        self.AS.IGVar['objPyoActif']['nom']\
        .append('oscM')
        self.AS.IGVar['objPyoActif']['init']\
        .append('oscM = Sine(freq = [440,600], mul = (LFO(mul = envM, type=2, freq = 200)))')  
        self.AS.IGVar['objPyoActif']['init']\
        .append('signal = MoogLP(oscM.mix(),oscM._freq[0])')
        self.AS.IGVar['objPyoActif']['init']\
        .append('filtre = Waveguide(Harmonizer(Disto(ComplexRes(signal)))).out()')
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
                        FREQ =  pas[j][1].nMidi

                        if pas[j][0] == 'note_on':
                            mess = str(OSC+'.setFreq(midiToHz([' + str(FREQ) +' , ' + str(FREQ+ 3) + ' , ' + str(FREQ+ 7) +']))')      
                            self.AS.IGVar['listeMess'][i].append(mess)
                            mess = str('signal.setFreq(oscM._freq[0]-50)')      
                            self.AS.IGVar['listeMess'][i].append(mess)



    ##    #self.AS.info(self)    

class Env():
    
    def __init__(self, arg):
        self.AS = arg

        #self.AS.info(self)  
        
    
    def simpleAdsr(self, voix):

        
        self.AS.IGVar['objPyoActif']['nom']\
        .append('adsrM')
        self.AS.IGVar['objPyoActif']['nom']\
        .append('envM')
        self.AS.IGVar['objPyoActif']['init']\
        .append('adsrM = Adsr(attack=.1, decay=.5, sustain=.2, release=.4, dur=0)')
        self.AS.IGVar['objPyoActif']['init']\
        .append('envM = Port(adsrM, risetime=2, falltime=1)')
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
            

        #self.AS.info(self)  
