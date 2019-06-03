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
from obspy.core import read, UTCDateTime

#Archivo en el que se hara los llamados a las clases que soportan todo el proyecto



def segmenter():
    horai= SegmenterAlfa3.datetime.now()
    #tipo A ---- ( nombre1, nombre2, nombre3, nombre4, fechaInicio, horas a anlizar, amplitud minima, ventanas de tiempo) ---- 8 argumentos
    #seg = SignalDg('EC','CAYR','','SHZ','2017-01-24  00:00:00', 24, 1000, 320)#2016-09-16  00:00:00
    segL = SegmenterAlfa3.SignalDg('ovolcan.mseed', 1000, 320)
    #segL = SegmenterAlfa3.SignalDg('ovolcan.mseed', 1000, 320)
    horaf= SegmenterAlfa3.datetime.now()-horai
    #2016-02-19
    print("\n Contando con los segundos de coneccion el script tomo: ",horaf)
    return segL
  

    
def partitioner(l1, l2, l3, seconds): # primero envia la señal al analizer y sobre los resultados realiza las pruebas de redundancia
    
    lf = Redunder.redo(l1,l2,l3,seconds)
    
    return lf

def partitionerSol(name, amp): # solo utiliza una señal no hay redundancia para pruebas de impresion o funcionalidad
    l1 = SegmenterAlfa3.SignalDg(name, amp, 320)
    l1 = Analizer.Partitioner(l1.getEventLaps(), l1.getMinPoint())
    
    return l1
 
def redundancy(l1,l2,l3, seconds):# segundos de diferencia aceptables para la redundancia / primero realiza pruebas de redundancia sobre la señal y posteriormente corre el analizer
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

#seg = SignalDg('EC','CAYR','','SHZ','2017-01-24  00:00:00', 24, 1000, 320)
def bigTimesManagerS(nombre1, nombre2, nombre3, nombre4, fechainit, dias, amp, ventana):
    #dgSignals = []
    added = 0 
    tiempox = UTCDateTime(fechainit)
    #superSignal = None
    superPartitioner = None
	
    for x in range(0, dias):
        seg = SegmenterAlfa3.SignalDg(nombre1,nombre2,nombre3,nombre4,str(tiempox + added), 24, amp, ventana)
        #dgSignals.append(seg)
        added = added + 86400
        if x == 0:
            #superSignal = dgSignals[0]
            superPartitioner = Analizer.Partitioner(seg.getEventLaps(), seg.getMinPoint())
        else:
            part = Analizer.Partitioner(seg.getEventLaps(), seg.getMinPoint())
            superPartitioner.addPartitioners(part)
            
    return superPartitioner

'''	superSignal = dgSignals[0]
	for x in range(1, len(dgSignals)):
		superSignal.addTimes(dgSignals[x].getTimes("T"))
		superSignal.addOTrace(dgSignals[x].getOTrace())
		superSignal.setETime(dgSignals[x].getETime())
		if superSignal.getMaxAmp() < dgSignals[x].getMaxAmp():
			superSignal.setMaxAmp(dgSignals[x].getMaxAmp())
		superSignal.addETime(dgSignals[x].getETime())
		superSignal.addNoDataTimes(dgSignals[x].getNoDataTimes())'''
    
    #return superSignal mode puede ser R o P en string define si se usa analisis o redundancia primero
def bigTimesManagerF(aNombre1, aNombre2, aNombre3, aNombre4, bNombre1, bNombre2, bNombre3, bNombre4, cNombre1, cNombre2, cNombre3, cNombre4, fechainit, dias, amp, ventana, seconds, mode):

    added = 0 
    tiempox = UTCDateTime(fechainit)
    superPartitioner = None
	
    if mode == "P":
        for x in range(0, dias):
            segA = SegmenterAlfa3.SignalDg(aNombre1, aNombre2, aNombre3, aNombre4, str(tiempox + added), 24, amp, ventana)
            segB = SegmenterAlfa3.SignalDg(bNombre1, bNombre2, bNombre3, bNombre4, str(tiempox + added), 24, amp, ventana)
            segC = SegmenterAlfa3.SignalDg(cNombre1, cNombre2, cNombre3, cNombre4, str(tiempox + added), 24, amp, ventana)
            added = added + 86400
            
            partA = Analizer.Partitioner(segA.getEventLaps(), segA.getMinPoint())
            partB = Analizer.Partitioner(segB.getEventLaps(), segB.getMinPoint())
            partC = Analizer.Partitioner(segC.getEventLaps(), segC.getMinPoint())
            
            if x == 0:
                superPartitioner = Redunder.redo(partA,partB,partC,seconds)
            else:
                part = Redunder.redo(partA,partB,partC,seconds)
                superPartitioner.addPartitioners(part)
    else:
        for x in range(0, dias): 
            segA = SegmenterAlfa3.SignalDg(aNombre1, aNombre2, aNombre3, aNombre4, str(tiempox + added), 24, amp, ventana)
            segB = SegmenterAlfa3.SignalDg(bNombre1, bNombre2, bNombre3, bNombre4, str(tiempox + added), 24, amp, ventana)
            segC = SegmenterAlfa3.SignalDg(cNombre1, cNombre2, cNombre3, cNombre4, str(tiempox + added), 24, amp, ventana)            
            added = added + 86400
            
            pmin = segA.getMinPoint()
            segA = segA.getEventLaps()
            segB = segB.getEventLaps()
            segC = segC.getEventLaps()
            
            part = Redunder.timeChecker(segA,segB,segC,seconds)
            
            if x == 0:
                superPartitioner = Analizer.Partitioner(part,pmin)
            else:
                part = Analizer.Partitioner(part,pmin)
                superPartitioner.addPartitioners(part)        
            
    return superPartitioner

    #return superSignal mode puede ser R o P en string define si se usa analisis o redundancia primero
def bigTimesManagerD(aNombre1, bNombre1, cNombre1, dias, amp, ventana, seconds, mode):

    added = 0 
    superPartitioner = None
    
    segA = read(aNombre1)
    segB = read(bNombre1)
    segC = read(cNombre1)
    
    segA = SegmenterAlfa3.SignalDg(segA, [amp, ventana])
    segB = SegmenterAlfa3.SignalDg(segB, [amp, ventana])
    segC = SegmenterAlfa3.SignalDg(segC, [amp, ventana])
	
    if mode == "P":
        for x in range(0, dias):
            added = added + 86400
            
            partA = Analizer.Partitioner(segA.getEventLaps(), segA.getMinPoint())
            partB = Analizer.Partitioner(segB.getEventLaps(), segB.getMinPoint())
            partC = Analizer.Partitioner(segC.getEventLaps(), segC.getMinPoint())
            
            if x == 0:
                superPartitioner = Redunder.redo(partA,partB,partC,seconds)
            else:
                part = Redunder.redo(partA,partB,partC,seconds)
                superPartitioner.addPartitioners(part)
    else:
        for x in range(0, dias):
            added = added + 86400
            
            pmin = segA.getMinPoint()
            segA = segA.getEventLaps()
            segB = segB.getEventLaps()
            segC = segC.getEventLaps()
            
            part = Redunder.timeChecker(segA,segB,segC,seconds)
            
            if x == 0:
                superPartitioner = Analizer.Partitioner(part,pmin)
            else:
                part = Analizer.Partitioner(part,pmin)
                superPartitioner.addPartitioners(part)        
            
    return superPartitioner

l1 = SegmenterAlfa3.SignalDg('EC.BVC2..BHZ.D.2018', 1000, 320)
l2 = SegmenterAlfa3.SignalDg('EC.BTAM..BHZ.D.2018', 1000, 320)
l3 = SegmenterAlfa3.SignalDg('EC.BREF..BHZ.D.2018', 1000, 320)

'''l1 = SegmenterAlfa3.SignalDg('EC.BVC2..BHZ.D.2018.002', 1000, 320)
l2 = SegmenterAlfa3.SignalDg('EC.BTAM..BHZ.D.2018.002',1000, 320)
l3 = SegmenterAlfa3.SignalDg('EC.BREF..BHZ.D.2018.002', 1000, 320)'''
    
#seg = segmenter()
#reds = redundancy(10)
part = partitioner(l1, l2, l3, 10)
#solPart = partitionerSol('EC.BREF..BHZ.D.2018.002',1000)

'''for x in range(2, 30):
    EC.BREF..BHZ.D.2018.015
    if x < 10:
        a = 'EC.BVC2..BHZ.D.2018.00' + str(x)
        b = 'EC.BTAM..BHZ.D.2018.00' + str(x) 
        c = 'EC.BREF..BHZ.D.2018.00' + str(x)
    else:
        a = 'EC.BVC2..BHZ.D.2018.0' + str(x)
        b = 'EC.BTAM..BHZ.D.2018.0' + str(x)
        c = 'EC.BREF..BHZ.D.2018.0' + str(x)
    a1 = SegmenterAlfa3.SignalDg(a, 1000, 320)
    b1 = SegmenterAlfa3.SignalDg(b, 1000, 320)
    c1 = SegmenterAlfa3.SignalDg(c, 1000, 320)
    
    part = partitioner(a1, b1, c1, 10)
    if x == 0:
        part.printResultTimes()
    else:
        part.addPrintResultTimes()'''
    