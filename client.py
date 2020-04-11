#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 19:04:55 2020

@author: j
"""

import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='a = Sine().out()')
print(" [x] Sent ")
time.sleep(1)
print(" [x] Sent ")
channel.basic_publish(exchange='', routing_key='hello', body='break')
