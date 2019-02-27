# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 11:48:40 2019

@author: Dago
"""

import SegmenterAlfa2
#import partitioner

#Archivo en el que se hara los llamados a las clases que soportan todo el proyecto



def segmenter():
    horai=datetime.now()
    #tipo A ---- ( nombre1, nombre2, nombre3, nombre4, fechaInicio, horas a anlizar, amplitud minima, ventanas de tiempo) ---- 8 argumentos
    #seg = SignalDg('EC','CAYR','','SHZ','2017-01-24  00:00:00', 24, 1000, 320)#2016-09-16  00:00:00
    segLocal = SignalDg('ovolcan.mseed', 1000, 320)
    horaf=datetime.now()-horai
    #2016-02-19
    print("\n Contando con los segundos de coneccion el script tomo: ",horaf)
    return segLocal
    


def partitioner():
    return 0

def redundancy():
    return 0

seg = segmenter()