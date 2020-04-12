#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 17:42:55 2020

@author: j
"""

import subprocess
import time

print('debut')
test = subprocess.Popen('./client.py')
pid = test.pid

for i in range(5):
    print(i)
    
    print(pid)  
    time.sleep(1)


while test.poll() == None :
    print('alive')
    test.terminate()
    test.wait()
    print(test.poll())


print('dead')