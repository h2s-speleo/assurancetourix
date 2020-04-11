#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 19:04:55 2020

@author: j
"""



import pika
import uuid
import time

class FibonacciRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        
        self.millisEnv = int(round(time.time() * 1000))
        self.enAttente = 0
        self.response = 'rien a faire'

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
#            self.channel.basic_ack(delivery_tag=method.delivery_tag)

    def call(self, n):
        self.response = 'en attente'
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        
        self.enAttente = 1
        self.millisEnv = int(round(time.time() * 1000))
        
    def checkReponse(self):
        if self.enAttente == 1 :
            if int(round(time.time() * 1000)) - self.millisEnv > 3000 :
                self.enAttente = 0 
                return 'erreur'
            elif self.response == 'en attente' :
                self.connection.process_data_events()
                return 'en attente'
                
            else :
                self.enAttente = 0
                return self.response
        else :
            return 'rien a faire'
        

fibonacci_rpc = FibonacciRpcClient()
print(" [x] Requesting fib(30)")
fibonacci_rpc.call(17)

compt = 0
while True :
    response = fibonacci_rpc.checkReponse()
    
    if response != 'rien a faire':
        print(" [.] Got %r" % response)
    
    if response == 'erreur':
        print('tuer proprement le serveur et le redémarer')
        break
    
    compt = compt + 1
    if compt > 100 :
        break
    time.sleep(0.001)
    
    
    
    
    
    
for i in range(25):

    time.sleep(1)