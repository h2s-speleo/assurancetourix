#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class IGraph():

    def __init__(self, arg):
        self.AS = arg
    
    def test(self, arg):
        print('test')
        print(self.AS.a)
        r = 5 * arg
        return r
    
    def tempoMoins(self):
        self.AS.tempo = int(self.AS.tempo * 1.1)
        if self.AS.tempo > 500 :
            self.AS.tempo = 500
        if self.AS.tempo < 160 and self.AS.tempo > 140 :
            self.AS.tempo = 150
        print('TEMPO : ', end = '')
        print (str(150/self.AS.tempo)[:4])

    def tempoPlus(self):
        self.AS.tempo = int(self.AS.tempo * 0.9)
        if self.AS.tempo < 50 :
            self.AS.tempo = 50
        if self.AS.tempo < 160 and self.AS.tempo > 140 :
            self.AS.tempo = 150
        print('TEMPO : ', end = '')
        print (str(150/self.AS.tempo)[:4])