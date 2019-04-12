# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 12:28:34 2019

@author: Dago
"""

#import Scripts.SegmenterAlfa3
import Analizer
import SegmenterAlfa3

def redo(l1,l2,l3, seconds) :#cuando se realiza la redundancia despues de el analisis se usa redo para armar partitioner y tener los tiempos listos.
    
    eL1 = Analizer.Partitioner(l1.getEventLaps(), l1.getMinPoint())
    eL2 = Analizer.Partitioner(l2.getEventLaps(), l2.getMinPoint())
    eL3 = Analizer.Partitioner(l3.getEventLaps(), l3.getMinPoint())
    
    lf = eL1
    lfl = timeCheckerS(eL1,eL2, eL3, seconds)
    #como esta no se puede imprimir imagenes exactas de los eventos se guarda todo el signal dago porsia //deberia ser solo una lista de trazos..... talvez del timechecker se los puede sacar
    lf.setSignalsDg([l1,l2,l3])
    lf.setFinalTraces(lfl[0])
    lf.setExternalevTimes(lfl[1])
    
    return lf

def timeChecker(eL1,eL2,eL3, seconds): #timeChecker(lista, seconds):
    
# para usar mas de una fuente en la redundancia se podria usar args mas que args solo  listas para tener mayor cantidad ee variables se 
# usaria la misma estructura de ifs pero en los contenidos se llamaria a funciones en las que se trabajaria con foreachs 
# para definir bien la comparacion. no se puede usar una matriz grande puesto que no se tiene lapsos de tiempo definidos    
    
    lf = []
    
    '''eL1 = l1.getEventLaps()
    eL2 = l2.getEventLaps()
    eL3 = l3.getEventLaps()'''
 
    i = 0
    o = 0
    u = 0
    #notDone = True
    
    flag1 = False# poner tres banderas mas para discriminar limites
    flag2 = True #para el1
    flag3 = True #para el2
    flag4 = True #para el3
    
    #for i in range(len(eL1)): #usar tiempos el subsearch times ni se que 
    while flag2 or flag3 or flag4: #notDone: 
        
        if len(eL1) <= i:
            flag2 = False
        if len(eL2) <= o:
            flag3 = False
        if len(eL3) <= u:
            flag4 = False
# usar el timedelta en las comparaciones talvez o a nivel de cada elemento ... timedelta mejor.         
        if flag2:
            '''if flag3 and flag4 and eL1[i].getStats().starttime == eL2[o].getStats().starttime == eL3[u].getStats().starttime:
                lf.append(eL1[i])
                i += 1
                o += 1
                u += 1'''
            if flag3 and abs(eL1[i].getStats().starttime - eL2[o].getStats().starttime) <= seconds:
                lf.append(eL1[i])
                i += 1
                o += 1
                if flag4 and abs(eL1[i-1].getStats().starttime - eL3[u].getStats().endtime) <= seconds:# inicialt  >= finalt 
                    u += 1
                elif abs(eL1[i-1].getStats().starttime - eL3[u].getStats().starttime) <= seconds:
                    u += 1
                    '''if flag3 and abs(eL1[i-1].getStats().starttime - eL2[o].getStats().endtime) <= seconds:# inicialt  >= finalt 
                        o += 1'''
            elif flag4 and abs(eL1[i].getStats().starttime - eL3[u].getStats().starttime) <= seconds:
                lf.append(eL1[i])
                i += 1
                u += 1
                if flag3 and abs(eL1[i-1].getStats().starttime - eL2[o].getStats().endtime) <= seconds:# inicialt  >= finalt 
                    o += 1
            elif flag3 and abs(eL1[i].getStats().endtime - eL2[o].getStats().starttime) <= seconds:  #revisar si no hay falla por index out of bounds
                i += 1 
                flag1 = True
            elif flag4 and abs(eL1[i].getStats().endtime - eL3[u].getStats().starttime) <= seconds:
                i += 1 
                flag1 = True
            else:
                flag1 = True
        
        if flag1 and flag3 and flag4:
            if abs(eL2[o].getStats().starttime - eL3[u].getStats().starttime) <= seconds:
                lf.append(eL2[o])
                o += 1
                u += 1
            else: # como carajos usar diferencias de tiempocon aproximados o exactidud hasta min? hmmm datatime.datatime class
                if abs(eL3[u].getStats().starttime - eL2[o].getStats().endtime) <= seconds:# inicialt  >= finalt
                    o += 1
                elif abs(eL2[o].getStats().starttime - eL3[u].getStats().endtime) <= seconds:# inicialt  >= finalt
                    u += 1
        elif flag2 == False and flag3 == False:# se puede mejorar haciendo que toda la columna muera
            u += 1
        elif flag2 == False and flag4 == False:
            o += 1
        
        flag1 = False
            
        '''if len(eL1) + 1 == i and len(eL2) + 1 == o and len(eL3) + 1 == u:
            notDone = False'''
    
    return lf 

def timeCheckerS(l1,l2,l3, seconds): 

    lf = []
    times = []    
    
    eL1 = l1.getFinalTraces()
    eL2 = l2.getFinalTraces()
    eL3 = l3.getFinalTraces()
 
    i = 0
    o = 0
    u = 0
    #notDone = True
    
    flag1 = False# poner tres banderas mas para discriminar limites
    flag2 = True #para el1
    flag3 = True #para el2
    flag4 = True #para el3
    
    #for i in range(len(eL1)): #usar tiempos el subsearch times ni se que 
    while flag2 or flag3 or flag4: #notDone: 
        
        if len(eL1) <= i:
            flag2 = False
        if len(eL2) <= o:
            flag3 = False
        if len(eL3) <= u:
            flag4 = False
# usar el timedelta en las comparaciones talvez o a nivel de cada elemento ... timedelta mejor.         
        if flag2:
            '''if flag3 and flag4 and eL1[i].getStats().starttime == eL2[o].getStats().starttime == eL3[u].getStats().starttime:
                lf.append(eL1[i])
                i += 1
                o += 1
                u += 1'''
            if flag3 and abs(eL1[i].getStats().starttime - eL2[o].getStats().starttime) <= seconds:
                lf.append(eL1[i])
                times.append(l1.getEventTimes()[i])
                i += 1
                o += 1
                if flag4 and abs(eL1[i-1].getStats().starttime - eL3[u].getStats().endtime) <= seconds:# inicialt  >= finalt 
                    u += 1
                elif abs(eL1[i-1].getStats().starttime - eL3[u].getStats().starttime) <= seconds:
                    u += 1
                    '''if flag3 and abs(eL1[i-1].getStats().starttime - eL2[o].getStats().endtime) <= seconds:# inicialt  >= finalt 
                        o += 1'''
            elif flag4 and abs(eL1[i].getStats().starttime - eL3[u].getStats().starttime) <= seconds:
                lf.append(eL1[i])
                times.append(l1.getEventTimes()[i])
                i += 1
                u += 1
                if flag3 and abs(eL1[i-1].getStats().starttime - eL2[o].getStats().endtime) <= seconds:# inicialt  >= finalt 
                    o += 1
            elif flag3 and abs(eL1[i].getStats().endtime - eL2[o].getStats().starttime) <= seconds:  #revisar si no hay falla por index out of bounds
                i += 1 
                flag1 = True
            elif flag4 and abs(eL1[i].getStats().endtime - eL3[u].getStats().starttime) <= seconds:
                i += 1 
                flag1 = True
            else:
                flag1 = True
        
        if flag1 and flag3 and flag4:
            if abs(eL2[o].getStats().starttime - eL3[u].getStats().starttime) <= seconds:
                lf.append(eL2[o])
                times.append(l2.getEventTimes()[o])
                o += 1
                u += 1
            else: # como carajos usar diferencias de tiempocon aproximados o exactidud hasta min? hmmm datatime.datatime class
                if abs(eL3[u].getStats().starttime - eL2[o].getStats().endtime) <= seconds:# inicialt  >= finalt
                    o += 1
                elif abs(eL2[o].getStats().starttime - eL3[u].getStats().endtime) <= seconds:# inicialt  >= finalt
                    u += 1
        elif flag2 == False and flag3 == False:# se puede mejorar haciendo que toda la columna muera
            u += 1
        elif flag2 == False and flag4 == False:
            o += 1
        
        flag1 = False
            
        '''if len(eL1) + 1 == i and len(eL2) + 1 == o and len(eL3) + 1 == u:
            notDone = False'''
    
    return [lf, times]