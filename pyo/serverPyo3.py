#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 22:16:00 2020

@author: j
"""
import os
import time
from signal import SIGTERM, SIGKILL
from multiprocessing import Process, freeze_support, Queue
from pickle import dump
from io import BytesIO
import pika
from pyo import *


def ServPyo(self):
    s = Server() #instanciation du serveur
    x = None
    print(self.audioDevice)
    inputs, outputs = pa_get_devices_infos() #récupération de la liste des périphériques
    for index in sorted(outputs.keys()):
        if outputs[index]['name'] == self.audioDevice : # nom de ton périférique son
            x = index
    if x == None : #en cas d'échec on se choisi au périphérique 0
        print('default device')
        x = 1
    s.setOutputDevice(x) #définition de la sortie audio du serveur
    while True :
        if not self.qSonIN2.empty(): #si on a quelquechose dans la queue
            RETVALUE = 'test'
            mes2 = self.qSonIN2.get()
            if 'RETVALUE' in mes2 :
                loc = {}
                exec(mes2, locals(), loc)
                RETVALUE = loc.get('RETVALUE')
                self.qSonOUT.put(RETVALUE)
            else :
                if mes2 == 'break':
                    break
                else:
                    exec(mes2)
                    self.qSonOUT.put('NULL')
        time.sleep(0.001)#ralenti la boucle principale
    s.stop() #on coupe le serveur
    print('coupure Serveur Pyo')

class rpcServeurPyo():
    def __init__(self):
        self.etatCon = 0
        
        self.audioD()
        freeze_support()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='rpcPyo')
        self.channel.queue_purge(queue = 'rpcPyo')
        self.channel.basic_qos(prefetch_count=10)
        self.channel.basic_consume(queue='rpcPyo', on_message_callback=self.on_request)
        self.run()
        print('____________________________________________')
        self.channel.start_consuming()

    def run(self):
        self.qSonIN2 = Queue() #création de la queue du serveur pyo
        self.qSonOUT = Queue() #création de la queue du serveur pyo
        while not self.qSonIN2.empty():
            self.qSonIN2.get()
        while not self.qSonOUT.empty():
            self.qSonOUT.get()
        self.channel.queue_purge(queue = 'rpcPyo')
        self.SP = Process(target=ServPyo, daemon=True, args=(self,)) #création du processus du serveur pyo
        self.SP.start()
        self.pidServPyo = self.SP.pid
        print('#############################')
        print('PID serveur Pyo : ', end = '')
        print(self.pidServPyo)
        print('#############################')
        self.initmessage()
        self.etatCon = 1

        print('serveur initialisé')

    def kill(self):

        self.qSonIN2.put('break')
        self.etatCon = 0
        try :
            self.qSonIN2.close()
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
                print('TERM signal')
                os.kill(self.pidServPyo, SIGKILL)
                print('KILL signal')
            except:
                pass
        
        print('kill')
  
    def reboot(self):
        print('reboot serveur pyo')

        self.qSonIN2.put('break')
        self.etatCon = 0
        try:
            self.SP.terminate()
            self.SP.join()
            self.SP.close()
        except : 
            try:
                os.kill(self.pidServPyo, SIGTERM)
                print('TERM signal')
                os.kill(self.pidServPyo, SIGKILL)
                print('KILL signal')
            except:
                pass
        self.run()
     
    def initmessage(self):
        listeInit = ['s.boot()','s.start()']
        for i in range(len(listeInit)):
            print(listeInit[i], end = '  ')
            self.qSonIN2.put(listeInit[i])
            self.check_message()
            rep = self.qSonOUT.get()
            print('| rep', end = ' ')
            print(rep)

    def on_request(self, ch, method, props, body):
        mess = body.decode('ascii')
        print(mess, end = '  ')
        if mess == 'TESTCONNEX' :
            if self.etatCon == 1:
                self.qSonIN2.put('RETVALUE = s.getIsStarted()')
                self.check_message()
                rep = self.qSonOUT.get()
                print('| rep', end = ' ')
                print(rep)
                if rep == 0:
                    self.initmessage()

            time.sleep(0.1)
            DATA = self.serialiser([str(mess), self.etatCon])
            self.channel.basic_publish(exchange='',
                             routing_key=props.reply_to,
                             properties=pika.BasicProperties(),
                             body=DATA)
            self.channel.basic_ack(delivery_tag=method.delivery_tag)
        else :
            if self.etatCon == 1:
                self.qSonIN2.put(mess)
                if mess == 'break' :
                    self.kill()
                    DATA = self.serialiser([str(mess), 'SERVEUR_MORT'])
                    self.channel.basic_publish(exchange='',
                                     routing_key=props.reply_to,
                                     properties=pika.BasicProperties(),
                                     body=DATA)
                    self.channel.basic_ack(delivery_tag=method.delivery_tag)
                    self.channel.stop_consuming()
                    
                elif mess == 'REBOOT' :
#                    self.kill()
                    DATA = self.serialiser([str(mess), 'REBOOTING'])
                    self.channel.basic_publish(exchange='',
                                     routing_key=props.reply_to,
                                     properties=pika.BasicProperties(),
                                     body=DATA)
                    self.channel.basic_ack(delivery_tag=method.delivery_tag)
                    self.reboot()
                    
                else :
                    self.check_message()
                    rep = self.qSonOUT.get()           
                    DATA = self.serialiser([str(mess), rep])
                    self.channel.basic_publish(exchange='',
                                     routing_key=props.reply_to,
                                     properties=pika.BasicProperties(),
                                     body=DATA)
                    self.channel.basic_ack(delivery_tag=method.delivery_tag)
                    print('| rep', end = ' ')
                    print(rep)
                    if rep == 'CRASHSERVER':
                        self.reboot() 

    def check_message(self):
        temps = time.time() * 1000
        while self.qSonOUT.empty():
            time.sleep(0.001)  
            if (time.time() * 1000) - temps  > 500 :
                self.etatCon = 0
                self.qSonOUT.put('CRASHSERVER')
                break
        print('| delay', end = ' : ')
        print( str((time.time() * 1000) - temps  )[:4], end = ' ')

    def serialiser(self, data):
        buffer = BytesIO()
        res = dump(data, buffer)
        seq = buffer.getvalue()
        return seq
    
    def audioD(self):
        with open("./conf", "r") as f :
            fichier_entier = f.read()
            files = fichier_entier.split("\n")
        for line in files :
            if line.startswith('audio device ='):
                var = line.replace('audio device =', '')
                break
        while var.startswith(' '):
            var = var[1:]
        while var.endswith(' '):
            var = var[:-1]
        self.audioDevice =  var
    

     
if __name__ == '__main__':
    RPC = rpcServeurPyo()
    RPC.channel.queue_delete(queue='rpcPyo')
    RPC.channel.close()
    RPC.connection.close()
