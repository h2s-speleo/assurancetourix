#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 22:16:00 2020

@author: j
"""
import os
from os import path
import time
import functools
from signal import SIGTERM, SIGKILL
from multiprocessing import Process, freeze_support, Queue
from pickle import dump,load
from io import BytesIO
from pyo64 import *
from pyotools import *
import logging
import configparser
import argparse
from random import random
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler


     
        

def ServPyo(self):

    s = Server() #instanciation du serveur Pyo
    print(' --------instanciation du serveur')
    x = None
#    print(self.audioDevice)
    inputs, outputs = pa_get_devices_infos() #récupération de la liste des périphériques
    for index in sorted(outputs.keys()):
        if outputs[index]['name'] == audioDevice : # nom de ton périférique son
            x = index
    if x == None : #en cas d'échec on se choisi au périphérique 0
        print('fallback to default device can not set audiodevice to %s'%self.audioDevice)
        x = 1
    s.setOutputDevice(Pyo_output) #définition de la sortie audio du serveur
    s.setVerbosity(Pyo_verbosity)
    s.setDuplex(Pyo_duplex)
    #Communication Loop With Pyo Server instance
    while True :
        #éviter les timeout on boucle en continu
        if not self.qSonIN.empty(): #si on a quelquechose dans la queue
            RETVALUE = 'test'
            mes2 = self.qSonIN.get()
            if 'RETVALUE' in mes2 :
                loc = {}
                exec(mes2, locals(), loc)
                RETVALUE = loc.get('RETVALUE')
                self.qSonOUT.put(RETVALUE)
            else :
                if mes2 == 'break':
                    break
                else :    
                    exec(mes2)
                    self.qSonOUT.put('NULL')
                    
        time.sleep(0.001)#ralenti la boucle principale
    s.stop() #on coupe le serveur
    print('coupure Serveur Pyo')
    
    
   
        
    
    
    

class ServeurPyo():
    
    _rpc_methods_= ['is_pyostarted','is_pyobooted','pyoinitmessage','pyocmd','pyoreboot','pyokill','get_pyopid']
    
    def __init__(self):
        self.etatCon = 0
        freeze_support()
        #créer le serveur pyo
        self.run()
        #créer le serveur RPC
        self._serv = SimpleXMLRPCServer(('0.0.0.0', xmlrpc_port),
                            logRequests=True,allow_none=True)
        for name in self._rpc_methods_:
            self._serv.register_function(getattr(self,name))
        # add kill server
        self._serv.register_function(lambda: os.kill(os.getpid(), signal.SIGTERM), 'rpcquit')
        self._serv.serve_forever()
        
        LOGGER.info('RPC sercver is started')
    
    def get_pyopid(self):
        return str(self.pidServPyo)

    def is_pyostarted(self):
        self.qSonIN.put('RETVALUE = s.getIsStarted()')
        LOGGER.info('Ask Pyo if it\'s started')
        self.check_message()
        rep=self.qSonOUT.get()
        LOGGER.info('Pyo Serv say %s'%rep)
        if(str(rep) == '1'):
            return True
        else:
            return False
    
    def is_pyobooted(self):
        
        self.qSonIN.put('RETVALUE = s.getIsBooted()()')
        LOGGER.info('Ask Pyo if it\'s booted')
        self.check_message()
        rep=self.qSonOUT.get()
        LOGGER.info('Pyo Serv say %s'%rep)
        if(str(rep) == '1'):
            return True
        else:
            return False
        
        
        
    def run(self):
        self.qSonIN = Queue() #création de la queue de commande pour le serveur pyo
        self.qSonOUT = Queue() #création de la queue pour le retour du serveur Pyo vers le client
        while not self.qSonIN.empty():
            self.qSonIN.get()
        while not self.qSonOUT.empty():
            self.qSonOUT.get()
        #instanciation du serveur Pyo
        self.SP = Process(target=ServPyo, daemon=True, args=(self,)) #création du processus du serveur pyo
        self.SP.start()
        self.pidServPyo = self.SP.pid
        writePidFile('/tmp/pyosnd.pid')
        LOGGER.info('PID serveur Pyo : %s' % self.pidServPyo)
        self.pyoinitmessage()
        LOGGER.info('Serveur Pyo initialisé')

    def pyokill(self):

        self.qSonIN.put('break')
        self.etatCon = 0
        try :
            self.qSonIN.close()
        except:
            pass
        try:
            self.qSonOUT.close()
        except:
            pass
        try:
            self.SP.terminate()
            self.SP.join()
            self.SP.close()
        except : 
            try:
                os.kill(self.pidServPyo, SIGTERM)
                LOGGER.info('sending TERM signal to pyoserv')
                os.kill(self.pidServPyo, SIGKILL)
                LOGGER.info('sending KILL signal to pyoserv')
            except:
                pass
        
        LOGGER.info('pyoserv killed dans ta gueule gros batard')

        return True
  
    def pyoreboot(self):
        LOGGER.info('reboot serveur pyo')

        self.qSonIN.put('break')
        self.etatCon = 0
        try:
            self.SP.terminate()
            self.SP.join()
            self.SP.close()
        except : 
            try:
                os.kill(self.pidServPyo, SIGTERM)
                LOGGER.info('sending TERM signal to pyoserv')
                os.kill(self.pidServPyo, SIGKILL)
                LOGGER.info('sending KILL signal to pyoserv')
            except:
                pass
        self.run()
        return True
     
    def pyoinitmessage(self):
        listeInit = ['s.boot()','s.start()']
        for i in range(len(listeInit)):
            #print(listeInit[i], end = '  ')
            LOGGER.info('initmessage - Serveur Pyo send command %s'%listeInit[i])
            self.qSonIN.put(listeInit[i])
            self.check_message()
            rep = self.qSonOUT.get()
            LOGGER.info('initmessage - Serveur Pyo response : %s'%rep)
            
            
            
    def pyocmd(self,commande):
        LOGGER.info('Serveur Pyo send command %s'%commande)
        self.qSonIN.put(commande)
        self.check_message()
        rep = self.qSonOUT.get()
        LOGGER.info('initmessage - Serveur Pyo response : %s'%rep)
        return rep
    
    
    def check_message(self):
        temps = time.time() * 1000
        while self.qSonOUT.empty():
            time.sleep(0.001)  
            if (time.time() * 1000) - temps  > 1500 :
                LOGGER.info("Put CRASHSERVER message : delay expiration is %s"% str((time.time() * 1000) - temps))
                self.etatCon = 0
                self.qSonOUT.put('CRASHSERVER')
                # pyo probably crashed
                # then stop & kill everybody
                hardkilling()                
                break
        print('| delay', end = ' : ')
        print( str((time.time() * 1000) - temps  )[:4], end = ' ')

    def serve_forever(self):
        try:
            print( 'Use Control-C to exit')
            self._serv.quit = 0
            while not self._serv.quit:
                self._serv.handle_request()
        except:
            print( 'Exiting')
            self.pyokill()
            print( 'kill rpc')
            self.killRPCServ()
            

    def killRPCServ(self):
        
        self._serv.rpcquit()
        return 1
   
#################

def writePidFile(pathpid):
    pid = str(os.getpid())
    try: 
        f = open(pathpid, 'w')
        f.write(pid)
        f.close()
    except:
        print ("error while trying to write pid file") 
        
def readpid(pathpid):
    if path.exists(pathpid):
        f = open(pathpid, "r")
        pid=f.readline()
        return int(pid)
    else:
        print ("pid file does not exist any more")

def delpidfile(pathpid):
    if path.exists(pathpid):
        os.remove(pathpid)
    else:
        print ("pid file does not exist any more")
        
        
def hardkilling():
        LOGGER.info('pyo is crashed hardkilling process and exit')    
        pidpyo=readpid('/tmp/pyosnd.pid')
        os.kill( pidpyo, 9 )
        delpidfile('/tmp/pyosnd.pid')
        pid=readpid('/tmp/pyorpc.pid')
        os.kill( pid, 9 )
        delpidfile('/tmp/pyorpc.pid')
        print("stoppping now...")
        
        sys.exit(0)

if __name__ == '__main__':
    #
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='config file for ServerPyo', dest='configfile')
    parser.add_argument('--action', help='start or stop the pyo-xmlrpcserver',
                        action='store', choices={'start','stop'}, required=True)
    
    args = parser.parse_args()
    if (args.action=='start'):
        #keep pid for main
        writePidFile('/tmp/pyorpc.pid')
        #ReadConfig(args.config)
        config = configparser.ConfigParser()
        print('config is %s'%args.configfile)
        try:
            config.read(args.configfile)
            audioDevice=config['DEFAULT']['audio device']
            logFile=config['DEFAULT']['log']
            Pyo_verbosity=int(config['PYO']['verbosity'])
            Pyo_output=int(config['PYO']['output'])
            Pyo_duplex=int(config['PYO']['duplex'])
            xmlrpc_port=int(config['xmlrpcServ']['port'])
            
        except: #handle other exceptions such as attribute errors
            print("Unexpected error:", sys.exc_info()[0])
            print(" can not read config file : fallback to default")
            audioDevice='pulse'
            logFile='./pyoserver.log'
            Pyo_verbosity=8
            Pyo_output=0
            Pyo_duplex=0
            xmlrpc_port=1233
    
        """Set Logger
        """
    
        LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
                      '-35s %(lineno) -5d: %(message)s')
        logging.basicConfig(format=LOG_FORMAT,filename=logFile,level=logging.INFO)
        LOGGER = logging.getLogger(__name__)
         
        #launch server
        RPC = ServeurPyo()
    
    if (args.action=='stop'):
        pidpyo=readpid('/tmp/pyosnd.pid')
        try:
            os.kill( pidpyo, 9 )
        except:
            print(" can not kill pid %i"%pidpyo)
        delpidfile('/tmp/pyosnd.pid')
        pid=readpid('/tmp/pyorpc.pid')
        try:
            os.kill( pid, 9 )
        except:
                print(" can not kill pid %i"%pid)
        delpidfile('/tmp/pyorpc.pid')
        print("stoppping now...")
    
        


