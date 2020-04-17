#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 19:04:55 2020

@author: j
"""

import time
from pickle import load
from io import BytesIO
import pika

class PyoClient():
    def __init__(self):
        self.etatConn = 0
        self.crash = 0
        self.initMess = list()
        self.millisEnv = int(round(time.time() * 1000))
        self.enAttente = 0
        self.run()
    
    def run(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.channel.queue_purge(queue = 'rpcPyo')
        result = self.channel.queue_declare(queue='', exclusive=True)

        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)
        print('server run')

    def on_response(self, ch, method, props, body):
        self.response = body

    def initPypObject(self):
        self.etatConn = 1
        for i in range(len(self.initMess)):
            pyo_rpc.send(self.initMess[i])
            
    def testConnex(self):
        compt = 0
        while pyo_rpc.etatConn == 0:
            print ('TESTCONNEX', end = ' -> ')
            self.millisEnv = int(round(time.time() * 1000))
            self.channel.basic_publish(
                exchange='',
                routing_key='rpcPyo',
                properties=pika.BasicProperties(
                    reply_to=self.callback_queue),
                    body=str('TESTCONNEX'))
            self.response = 'en attente'
            self.enAttente = 1
            self.millisEnv = time.time() * 1000
            x = self.reception('TESTCONNEX')
            print(" -> %r" % x)
            if x[1] == 1:
                self.initPypObject()
                return x
                break
            compt = compt + 1
            if compt > 5 :
                print('impossible de se connecter')
                break
            time.sleep(0.2)
    
    def send(self, comm):
        if self.etatConn == 0:
            print('connexion morte, test de la connection')
            x =self.testConnex()
        else :
            print (comm, end = ' -> ')
            self.millisEnv = time.time() * 1000
            self.channel.basic_publish(
                exchange='',
                routing_key='rpcPyo',
                properties=pika.BasicProperties(
                    reply_to=self.callback_queue),
                    body=str(comm))
            self.response = 'en attente'
            self.enAttente = 1
            x = self.reception(comm)       
            print(" -> %r" % x)
            print("TU ME FAIS CHIER AVEC TON PUTAIN DE SERVEUR")
            if x[1] == 'CRASHSERVER':
                self.etatConn = 0
        return x
        
    def checkReponse(self):
        if self.enAttente == 1 :
            attente = (time.time() * 1000) - self.millisEnv
            if attente > 600 :
                print(str(attente)[:4], end = ' ')
                self.enAttente = 0 
                print('CRASHSERVER')
                return 'CRASHSERVER'
            elif self.response == 'en attente' :
                self.connection.process_data_events()
                return 'en attente'
            else :
                self.enAttente = 0
                print(str(attente)[:4], end = ' ')
                return self.response
        else :
            return 'rien a faire'
        
    def reception(self, comm):
        while True :
            response = self.checkReponse()
            if response != 'rien a faire' and response != 'en attente':
                if type(response) == bytes:
                    listeRep = self.deSerialiser(response)
                else:
                    listeRep = [comm, 'CRASHSERVER']
                return listeRep

    def deSerialiser(self, seq):
        buffer = BytesIO(seq)
        read = load(buffer)
        return read
    
    def kill(self):
        self.send('break')

        try :
            self.channel.close()
        except :
            pass
        try :
            self.connection.close()
        except :
            pass

if __name__ == '__main__':
    pyo_rpc = PyoClient()
    pyo_rpc.initMess.append('a = Sine()')
    pyo_rpc.testConnex()
    
    listeCommande = ['a.out()','RETVALUE= a._freq', 'a.stop()']
    for j in range(3):
        for i in range(len(listeCommande)):
            x = pyo_rpc.send(listeCommande[i])
            time.sleep(1)
    
    listeCommande = ['REBOOT', 'iusdfiougqsdfoiug']
    for j in range(2):
        for i in range(len(listeCommande)):
            x = pyo_rpc.send(listeCommande[i])
            time.sleep(1)
    
    listeCommande = ['a.out()','RETVALUE= a._freq', 'a.stop()']
    for j in range(3):
        for i in range(len(listeCommande)):
            x = pyo_rpc.send(listeCommande[i])
            time.sleep(1)

    pyo_rpc.kill()
