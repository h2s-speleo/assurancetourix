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

def audioD():
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

    return var

def ServPyo():
    s = Server() #instanciation du serveur
    x = None
    print(audioDevice)
    inputs, outputs = pa_get_devices_infos() #récupération de la liste des périphériques
    for index in sorted(outputs.keys()):
        if outputs[index]['name'] == audioDevice : # nom de ton périférique son
            x = index
    if x == None : #en cas d'échec on se choisi au périphérique 0
        print('default device')
        x = 1
    s.setOutputDevice(x) #définition de la sortie audio du serveur
    
    while True :
        if not qSonIN1.empty(): #si on a quelquechose dans la queue
            mes = qSonIN1.get()
            if mes == 'break':
                qSonIN1.task_done()
                break #fin de la boucle infinie
            else :
                exec(mes) #on execute la commande passée en str()
            qSonIN1.task_done()    
        
        if not qSonIN2.empty(): #si on a quelquechose dans la queue

            mes2 = qSonIN2.get()
            loc = {}
            exec(mes2, locals(), loc)
            RETVALUE = loc.get('RETVALUE')
            qSonOUT.put(RETVALUE)
            qSonIN2.task_done()   
        
            
        time.sleep(0.001)#ralenti la boucle principale
        
    s.stop() #on coupe le serveur
    
    print('coupure Serveur Pyo')

def on_request(ch, method, props, body):
    mess = body.decode('ascii')

    
    if mess == 'GETPID':
        rep = str(pidServPyo)
    elif mess.startswith('RETVALUE'):
        qSonIN2.put(mess)
        qSonIN2.join()
        rep = str(qSonOUT.get())
    else:
        qSonIN1.put(mess)
        qSonIN1.join()
        rep = 'NULL'
    
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = props.correlation_id),
                     body=str(str(mess) + '###' + rep))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
    if mess == 'break' :
        channel.stop_consuming()

audioDevice = audioD()

freeze_support()
qSonIN1 = JoinableQueue() #création de la queue du serveur pyo
while not qSonIN1.empty():
    qSonIN1.get()
qSonIN2 = JoinableQueue() #création de la queue du serveur pyo
while not qSonIN2.empty():
    qSonIN2.get()
qSonOUT = JoinableQueue() #création de la queue du serveur pyo
while not qSonOUT.empty():
    qSonOUT.get()
SP = Process(target=ServPyo, daemon=True) #création du processus du serveur pyo
SP.start()
pidServPyo = SP.pid

listeInit = ['s.boot()','s.start()']
for i in range(len(listeInit)):
    qSonIN1.put(listeInit[i])
    qSonIN1.join() 

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='rpcPyo')
channel.queue_purge(queue = 'rpcPyo')
channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='rpcPyo', on_message_callback=on_request)
print('____________________________________________')
channel.start_consuming()

qSonIN1.put('break')
SP.join() #on attend la fin du processus du serveur pyo 
SP.terminate() #on supprime le processus du serveur pyo 
if SP.is_alive():
    os.kill(pidServPyo, SIGTERM)
    print('TERM signal')
if SP.is_alive():
    os.kill(pidServPyo, SIGKILL)
    print('KILL signal')
print('fin')