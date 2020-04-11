#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 19:04:55 2020

@author: j
"""

import pika
import uuid
import time

class PyoClient(object):

    def __init__(self):
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
        
        self.millisEnv = int(round(time.time() * 1000))
        self.enAttente = 0

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
                correlation_id=self.corr_id,
            ),
            body=str(n))
        
        self.response = 'en attente'
        self.enAttente = 1
        self.millisEnv = int(round(time.time() * 1000))
        
    def checkReponse(self):
        if self.enAttente == 1 :
            attente = int(round(time.time() * 1000)) - self.millisEnv
            print(attente, end = ' ')
            if attente > 3000 :
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
        



###############################################################################
pyo_rpc = PyoClient()
print(" [x] Requesting : a = Sine().out()")
pyo_rpc.call('a = Sine().out()')

compt = 0
while True :
    response = pyo_rpc.checkReponse()
    
    if response != 'rien a faire' and response != 'en attente':
        print(" [.] Got %r" % response)
        break
    
    if response == 'erreur':
        print('tuer proprement le serveur et le redémarer')
        break
    

time.sleep(1)
print(" [x] Requesting : break")
pyo_rpc.call('break')

compt = 0
while True :
    response = pyo_rpc.checkReponse()
    
    if response != 'rien a faire' and response != 'en attente':
        print(" [.] Got %r" % response)
        break
    
    if response == 'erreur':
        print('tuer proprement le serveur et le redémarer')
        break
    
##############################################################################
