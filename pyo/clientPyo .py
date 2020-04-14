#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 19:04:55 2020

@author: j
"""
import os
from signal import SIGTERM, SIGKILL
import uuid
import time
import subprocess
from pickle import load
from io import BytesIO
import pika

class PyoClient():
    def __init__(self):
        self.etatConn = 0
        self.millisEnv = int(round(time.time() * 1000))
        self.enAttente = 0
        self.run()
    
    def run(self):
        self.RPC = subprocess.Popen('./serverPyo.py')
        time.sleep(1)
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
        self.pidRPC = self.RPC.pid
        temp = self.send("GETPID")
        self.pidServPyo = temp[1]
        self.etatConn = 1
        print('server run')

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpcPyo',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id),
                body=str(n))
        self.response = 'en attente'
        self.enAttente = 1
        self.millisEnv = int(round(time.time() * 1000))
        
    def checkReponse(self):
        if self.enAttente == 1 :
            attente = int(round(time.time() * 1000)) - self.millisEnv
            print(attente, end = ' ')
            if attente > 500 :
                self.enAttente = 0 
                print('erreur')
                return 'erreur'
            elif self.response == 'en attente' :
                self.connection.process_data_events()
                return 'en attente'
            else :
                self.enAttente = 0
                return self.response
        else :
            return 'rien a faire'
        
    def send(self, comm):
        print(comm, end = ' ')
        self.call(comm)
        while True :
            response = self.checkReponse()
            if response == 'erreur':
                listeRep = [comm, 'erreur']
                self.reboot
                break 
            elif response != 'rien a faire' and response != 'en attente':
                listeRep = self.deSerialiser(response)
                print(" [.] Got %r" % listeRep[1])
                break
            
        return listeRep
    
    def killServer(self):
        os.kill(self.pidServPyo, SIGTERM)
        os.kill(self.pidServPyo, SIGKILL)
        while self.RPC.poll() == None :
            self.RPC.terminate()
            self.RPC.wait()
        self.etatConn = 0    
        print('server kill')
        
    def reboot(self):
        print('reboot server')
        self.killServer()
        self.run()
        
    def deSerialiser(self, seq):
        buffer = BytesIO(seq)
        read = load(buffer)
        return read

if __name__ == '__main__':
    pyo_rpc = PyoClient()
    listeCommande = ['a = Sine()','a.out()','RETVALUE= a._freq', 'break']
    for i in range(len(listeCommande)):
        x = pyo_rpc.send(listeCommande[i])
        print(x)
        print('--------------------------------')

        time.sleep(1)


    
