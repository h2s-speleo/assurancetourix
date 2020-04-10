#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 22:16:00 2020

@author: j
"""
import pika
from signal import SIGTERM, SIGKILL
from multiprocessing import Process, freeze_support, Queue
import time
from pyo import *

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    print(body.decode('ascii'))
    qSon.put(body.decode('ascii'))

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
    s.boot()
    s.start()
    while True :
        if not qSon.empty(): #si on a quelquechose dans la queue
            mes = qSon.get()
            if mes == 'break':
                break #fin de la boucle infinie
            else :
                exec(mes) #on execute la commande passée en str()
        time.sleep(0.001)#ralenti la boucle principale
    s.stop() #on coupe le serveur
    print('coupure Serveur Pyo')



freeze_support()
qSon = Queue() #création de la queue du serveur pyo
SP = Process(target=ServPyo, daemon=True) #création du processus du serveur pyo
SP.start()
pidServPyo = SP.pid

channel.basic_consume(
    queue='hello', on_message_callback=callback, auto_ack=True)


print(' [*] Waiting for messages. To exit press CTRL+C')
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