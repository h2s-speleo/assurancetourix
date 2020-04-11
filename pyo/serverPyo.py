#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 22:16:00 2020

@author: j
"""
import os
import time
from signal import SIGTERM, SIGKILL
from multiprocessing import Process, freeze_support, JoinableQueue
import pika
from pyo import *

def ServPyo():
    s = Server() #instanciation du serveur
    x = None
    inputs, outputs = pa_get_devices_infos() #récupération de la liste des périphériques
    for index in sorted(outputs.keys()):
        if outputs[index]['name'] == 'pulse' : # nom de ton périférique son
            x = index
    if x == None : #en cas d'échec on se choisi au périphérique 0
        print('default device')
        x = 1
    s.setOutputDevice(x) #définition de la sortie audio du serveur
    
    while True :
        if not qSon.empty(): #si on a quelquechose dans la queue
            mes = qSon.get()
            print(mes)
            if mes == 'break':
                break #fin de la boucle infinie
            else :
                exec(mes) #on execute la commande passée en str()
            qSon.task_done()    
        time.sleep(0.001)#ralenti la boucle principale
        
    s.stop() #on coupe le serveur
    qSon.task_done()
    print('coupure Serveur Pyo')

def on_request(ch, method, props, body):
    mess = body.decode('ascii')
    qSon.put(mess)
    qSon.join()

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = props.correlation_id),
                     body=str('done : ' + str(mess)))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
    if mess == 'break' :
        channel.stop_consuming()

freeze_support()
qSon = JoinableQueue() #création de la queue du serveur pyo
SP = Process(target=ServPyo, daemon=True) #création du processus du serveur pyo
SP.start()
pidServPyo = SP.pid
while not qSon.empty():
    qSon.get()
listeInit = ['s.boot()','s.start()']
for i in range(len(listeInit)):
    qSon.put(listeInit[i])
    qSon.join() 

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='rpcPyo')
channel.queue_purge(queue = 'rpcPyo')
channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='rpcPyo', on_message_callback=on_request)
print('____________________________________________')
channel.start_consuming()

qSon.put('break')
SP.join() #on attend la fin du processus du serveur pyo 
SP.terminate() #on supprime le processus du serveur pyo 
if SP.is_alive():
    os.kill(pidServPyo, SIGTERM)
    print('TERM signal')
if SP.is_alive():
    os.kill(pidServPyo, SIGKILL)
    print('KILL signal')
print('fin')