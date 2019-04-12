# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 11:48:40 2019

@author: Dago
"""

#from Scripts import SegmenterAlfa3
import SegmenterAlfa3
#import Partitioner
import Redunder
import Analizer

#Archivo en el que se hara los llamados a las clases que soportan todo el proyecto



def segmenter():
    horai= SegmenterAlfa3.datetime.now()
    #tipo A ---- ( nombre1, nombre2, nombre3, nombre4, fechaInicio, horas a anlizar, amplitud minima, ventanas de tiempo) ---- 8 argumentos
    #seg = SignalDg('EC','CAYR','','SHZ','2017-01-24  00:00:00', 24, 1000, 320)#2016-09-16  00:00:00
    segL = SegmenterAlfa3.SignalDg('EC.BVC2..BHZ.D.2018.002', 1000, 320)
    #segL = SegmenterAlfa3.SignalDg('ovolcan.mseed', 1000, 320)
    horaf= SegmenterAlfa3.datetime.now()-horai
    #2016-02-19
    print("\n Contando con los segundos de coneccion el script tomo: ",horaf)
    return segL
  

    
def partitioner(seconds): # primero envia la señal al analizer y sobre los resultados realiza las pruebas de redundancia
    l1 = SegmenterAlfa3.SignalDg('EC.BVC2..BHZ.D.2018.002', 1000, 320)
    #l1 = Analizer.Partitioner(l1.getEventLaps(), l1.getMinPoint())
    l2 = SegmenterAlfa3.SignalDg('EC.BTAM..BHZ.D.2018.002', 1000, 320)
    #l2 = Analizer.Partitioner(l2.getEventLaps(), l2.getMinPoint())
    l3 = SegmenterAlfa3.SignalDg('EC.BREF..BHZ.D.2018.002', 1000, 320)
    #l3 = Analizer.Partitioner(l3.getEventLaps(), l3.getMinPoint())
    
    lf = Redunder.redo(l1,l2,l3,seconds)
    
    return lf

def partitionerSol(seconds): # solo utiliza una señal no hay redundancia para pruebas de impresion o funcionalidad
    l1 = SegmenterAlfa3.SignalDg('EC.BVC2..BHZ.D.2018.002', 1000, 320)
    l1 = Analizer.Partitioner(l1.getEventLaps(), l1.getMinPoint())
    
    return l1
 
def redundancy(seconds):# segundos de diferencia aceptables para la redundancia / primero realiza pruebas de redundancia sobre la señal y posteriormente corre el analizer
    l1 = SegmenterAlfa3.SignalDg('EC.BVC2..BHZ.D.2018.002', 1000, 320)
    #l2 = SegmenterAlfa3.SignalDg('EC.BVC2..BHZ.D.2018.002', 1000, 320)
    #l3 = SegmenterAlfa3.SignalDg('EC.BVC2..BHZ.D.2018.002', 1000, 320)
    #print(l1.getNumberELaps())
    #print("segunda----")
    l2 = SegmenterAlfa3.SignalDg('EC.BTAM..BHZ.D.2018.002', 1000, 320)
    #print(l2.getNumberELaps())
    #print("tercera-----")
    l3 = SegmenterAlfa3.SignalDg('EC.BREF..BHZ.D.2018.002', 1000, 320)
    #print(l3.getNumberELaps())
    
    pmin = l1.getMinPoint()
    l1 = l1.getEventLaps()
    l2 = l2.getEventLaps()
    l3 = l3.getEventLaps()
    
    '''l1.getEventLaps()[0].getTrace().plot()
    l3.getEventLaps()[0].getTrace().plot()
    print(l1.getEventLaps()[0].getStats().starttime)
    print(l3.getEventLaps()[0].getStats().starttime)
    x = (l1.getEventLaps()[0]).getStats().starttime - (l3.getEventLaps())[0].getStats().starttime
    print(x)'''
    lf = Redunder.timeChecker(l1,l2,l3,seconds)# cambiar el ultimo parametro para diferencia maxima entre sensores 
    
    lff = Analizer.Partitioner(lf,pmin)
    #lff= lf
    #lf = [l1,l2,l3]
    
    return lff

#seg = segmenter()
#reds = redundancy(10)
part = partitioner(10)
#solPart = partitionerSol(10)