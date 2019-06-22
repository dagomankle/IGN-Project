# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 12:28:34 2019

@author: Dago
"""

#import Scripts.SegmenterAlfa3
import Analizer
#import SegmenterAlfa3
print("Usando Redunder")

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
    lf.setFinalTypeTraces(lfl[2])
    
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
        print()
        print('flags: '+ str(flag1)+'/' +str(flag2)+'/'+str(flag3)+'/'+str(flag4))
        print('index: '+ str(i)+'/' +str(o)+'/'+str(u))
        if len(eL1) <= i:
            flag2 = False
        if len(eL2) <= o:
            flag3 = False
        if len(eL3) <= u:
            flag4 = False
# usar el timedelta en las comparaciones talvez o a nivel de cada elemento ... timedelta mejor.         
        if flag2:

            if flag3 and flag4:
                print(str(eL1[i].getStats().starttime) +'/' +str(eL2[o].getStats().starttime) +'/'+str(eL3[u].getStats().starttime))
                print(str(eL1[i].getStats().endtime) +'/' +str(eL2[o].getStats().endtime) +'/'+str(eL3[u].getStats().endtime))
            elif flag3:
                print(str(eL1[i].getStats().starttime) +'/' +str(eL2[o].getStats().starttime))
                print(str(eL1[i].getStats().endtime) +'/' +str(eL2[o].getStats().endtime))
            elif flag4:
                print(str(eL1[i].getStats().starttime)  +'/'+str(eL3[u].getStats().starttime))
                print(str(eL1[i].getStats().endtime)  +'/'+str(eL3[u].getStats().endtime))
            
            if flag3 and abs(eL1[i].getStats().starttime - eL2[o].getStats().starttime) <= seconds:
                lf.append(eL1[i])
                i += 1
                o += 1
                while True and flag4:
                    if abs(eL1[i-1].getStats().starttime - eL3[u].getStats().starttime) <= seconds:
                        u += 1
                        break
                    elif (eL1[i-1].getStats().starttime  >= eL3[u].getStats().endtime):# inicialt  >= finalt 
                        print('gg')
                        u += 1 
                    elif (eL3[u].getStats().starttime  >= eL1[i-1].getStats().endtime):
                        break
                    elif (eL1[i-1].getStats().starttime  <= eL3[u].getStats().endtime):
                        u += 1
                        break
            elif flag4 and abs(eL1[i].getStats().starttime - eL3[u].getStats().starttime) <= seconds:
                lf.append(eL1[i])
                i += 1
                u += 1
                while True and flag3:
                    if abs(eL1[i-1].getStats().starttime - eL2[o].getStats().starttime) <= seconds:
                        o += 1
                        break
                    elif (eL1[i-1].getStats().starttime >= eL2[o].getStats().endtime):# inicialt  >= finalt 
                        print('gg')
                        o += 1
                    elif (eL2[o].getStats().starttime >= eL1[i-1].getStats().endtime):
                        break
                    elif(eL1[i-1].getStats().starttime <= eL2[o].getStats().endtime):
                        o += 1
                        break
            elif flag3 and abs(eL1[i].getStats().endtime - eL2[o].getStats().endtime) <= seconds:
                lf.append(eL2[o])
                i += 1
                o += 1
            elif flag4 and abs(eL1[i].getStats().endtime - eL3[u].getStats().endtime) <= seconds:
                lf.append(eL3[u])
                i += 1
                u += 1
            elif flag3 and eL1[i].getStats().endtime >= eL2[o].getStats().endtime and eL1[i].getStats().starttime <= eL2[o].getStats().starttime:
                lf.append(eL2[o])
                i += 1
                o += 1
            elif flag4 and eL1[i].getStats().endtime >= eL3[u].getStats().endtime and eL1[i].getStats().starttime >= eL3[u].getStats().starttime:
                lf.append(eL3[u])
                i += 1
                u += 1 
            elif flag3 and (eL2[o].getStats().starttime >= eL1[i].getStats().endtime ):
                while True and flag4:
                    if abs(eL1[i].getStats().starttime - eL3[u].getStats().starttime) <= seconds:
                        lf.append(eL1[i])
                        u += 1
                        i += 1
                        break
                    elif eL1[i].getStats().endtime >= eL3[u].getStats().endtime and eL1[i].getStats().starttime < eL3[u].getStats().endtime:
                        lf.append(eL3[u])
                        i += 1
                        u += 1
                        break
                    elif eL1[i].getStats().endtime <= eL3[u].getStats().endtime and eL1[i].getStats().endtime > eL3[u].getStats().starttime:
                        lf.append(eL1[i])
                        i += 1
                        u += 1
                        break
                    elif (eL1[i].getStats().starttime  >= eL3[u].getStats().endtime):# inicialt  >= finalt 
                        u += 1 
                    elif (eL3[u].getStats().starttime  >= eL1[i].getStats().endtime):
                        i += 1
                        break 
                #flag1 = True
            elif flag4 and (eL3[u].getStats().starttime  >= eL1[i].getStats().endtime):
                while True and flag3:
                    if abs(eL1[i].getStats().starttime - eL2[o].getStats().starttime) <= seconds:
                        lf.append(eL1[i])
                        o += 1
                        i += 1
                        break
                    elif eL1[i].getStats().endtime >= eL2[o].getStats().endtime and eL1[i].getStats().starttime < eL2[o].getStats().endtime:
                        lf.append(eL2[o])
                        o += 1
                        i += 1
                        break
                    elif eL1[i].getStats().endtime <= eL2[o].getStats().endtime and eL1[i].getStats().endtime > eL2[o].getStats().starttime:
                        lf.append(eL1[i])
                        o += 1
                        i += 1
                        break
                    elif (eL1[i].getStats().starttime >= eL2[o].getStats().endtime):# inicialt  >= finalt 
                        o += 1
                    elif (eL2[o].getStats().starttime >= eL1[i].getStats().endtime):
                        i += 1
                        break 
                #flag1 = True
            elif flag3 and flag4:
                flag1 = True
            elif flag4 and (eL1[i].getStats().starttime  >= eL3[u].getStats().endtime):
                u += 1
            elif flag3 and (eL1[i].getStats().starttime >= eL2[o].getStats().endtime):
                o += 1
            else:
                flag2 = False
        if flag2 == False:
            flag1 = True
        
        if flag1 and flag3 and flag4:
            print('entra: '+str(eL2[o].getStats().starttime)+'/'+str(eL3[u].getStats().starttime))
            print('entra: '+str(eL2[o].getStats().endtime)+'/'+str(eL3[u].getStats().endtime))
            if abs(eL2[o].getStats().starttime - eL3[u].getStats().starttime) <= seconds:
                lf.append(eL2[o])
                o += 1
                u += 1
            elif abs(eL2[o].getStats().endtime - eL3[u].getStats().endtime) <= seconds:
                lf.append(eL2[o])
                o += 1
                u += 1
            elif eL2[o].getStats().endtime >= eL3[u].getStats().endtime and eL2[o].getStats().starttime <= eL3[u].getStats().starttime:
                lf.append(eL3[u])
                o += 1
                u += 1
            elif eL2[o].getStats().endtime <= eL3[u].getStats().endtime and eL2[o].getStats().starttime >= eL3[u].getStats().starttime:
                lf.append(eL2[o])
                o += 1
                u += 1
            elif eL2[o].getStats().endtime >= eL3[u].getStats().endtime and eL2[o].getStats().starttime < eL3[u].getStats().endtime:
                lf.append(eL3[u])
                o += 1
                u += 1
            elif eL2[o].getStats().endtime <= eL3[u].getStats().endtime and eL2[o].getStats().endtime > eL3[u].getStats().starttime:
                lf.append(eL2[o])
                o += 1
                u += 1
            else:
                if eL3[u].getStats().starttime >= eL2[o].getStats().endtime:
                    o += 1
                elif eL2[o].getStats().starttime >= eL3[u].getStats().endtime:
                    u += 1
        elif flag2 == False and flag3 == False:# se puede mejorar haciendo que toda la columna muera
            u += 1
        elif flag2 == False and flag4 == False:
            o += 1
        
        flag1 = False
    
    return lf 

def timeCheckerS(l1,l2,l3, seconds): #usa traces directamente no dgsignals pilas!

    lf = []
    times = []
    types = []    
    
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
        print()
        print('flags: '+ str(flag1)+'/' +str(flag2)+'/'+str(flag3)+'/'+str(flag4))
        print('index: '+ str(i)+'/' +str(o)+'/'+str(u))
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
            if flag3 and flag4:
                print(str(eL1[i].stats.starttime) +'/' +str(eL2[o].stats.starttime) +'/'+str(eL3[u].stats.starttime))
                print(str(eL1[i].stats.endtime) +'/' +str(eL2[o].stats.endtime) +'/'+str(eL3[u].stats.endtime))
            elif flag3:
                print(str(eL1[i].stats.starttime) +'/' +str(eL2[o].stats.starttime))
                print(str(eL1[i].stats.endtime) +'/' +str(eL2[o].stats.endtime))
            elif flag4:
                print(str(eL1[i].stats.starttime)  +'/'+str(eL3[u].stats.starttime))
                print(str(eL1[i].stats.endtime)  +'/'+str(eL3[u].stats.endtime))
            #print(' la fecha para l1: ' + str(eL1[i].stats.starttime))
            
            if flag3 and abs(eL1[i].stats.starttime - eL2[o].stats.starttime) <= seconds:
                lf.append(eL1[i])
                times.append(l1.getEventTimes()[i])
                types.append(l1.getEventTypes()[i])
                i += 1
                o += 1
                while True and flag4:
                    if flag4 and abs(eL1[i-1].stats.starttime - eL3[u].stats.starttime) <= seconds:
                        u += 1
                        break
                    elif (eL1[i-1].stats.starttime  >= eL3[u].stats.endtime):# inicialt  >= finalt 
                        u += 1 
                    elif (eL3[u].stats.starttime  >= eL1[i-1].stats.endtime):
                        break
                    elif (eL1[i-1].stats.starttime  <= eL3[u].stats.endtime):
                        u += 1
                        break
            elif flag4 and abs(eL1[i].stats.starttime - eL3[u].stats.starttime) <= seconds:
                lf.append(eL1[i])
                times.append(l1.getEventTimes()[i])
                types.append(l1.getEventTypes()[i])
                i += 1
                u += 1
                while True and flag3:
                    if abs(eL1[i-1].stats.starttime - eL2[o].stats.starttime) <= seconds:
                        o += 1
                        break
                    elif (eL1[i-1].stats.starttime >= eL2[o].stats.endtime):# inicialt  >= finalt 
                        o += 1
                    elif (eL2[o].stats.starttime >= eL1[i-1].stats.endtime):
                        break
                    elif (eL1[i-1].stats.starttime <= eL2[o].stats.endtime):
                        o += 1
                        break
            elif flag3 and abs(eL1[i].stats.endtime - eL2[o].stats.endtime) <= seconds:
                lf.append(eL2[o])
                times.append(l2.getEventTimes()[o])
                types.append(l2.getEventTypes()[o])
                i += 1
                o += 1
            elif flag4 and abs(eL1[i].stats.endtime - eL3[u].stats.endtime) <= seconds:
                lf.append(eL3[u])
                times.append(l3.getEventTimes()[u])
                types.append(l3.getEventTypes()[u])
                i += 1
                u += 1
            elif flag3 and eL1[i].stats.endtime >= eL2[o].stats.endtime and eL1[i].stats.starttime <= eL2[o].stats.starttime:
                lf.append(eL2[o])
                times.append(l2.getEventTimes()[o])
                types.append(l2.getEventTypes()[o])
                i += 1
                o += 1
            elif flag4 and eL1[i].stats.endtime >= eL3[u].stats.endtime and eL1[i].stats.starttime >= eL3[u].stats.starttime:
                lf.append(eL3[u])
                times.append(l3.getEventTimes()[u])
                types.append(l3.getEventTypes()[u])
                i += 1
                u += 1  
            elif flag3 and (eL2[o].stats.starttime >= eL1[i].stats.endtime ):
                while True and flag4:
                    if abs(eL1[i].stats.starttime - eL3[u].stats.starttime) <= seconds:
                        lf.append(eL1[i])
                        times.append(l1.getEventTimes()[i])
                        types.append(l1.getEventTypes()[i])
                        u += 1
                        i += 1
                        break
                    elif eL1[i].stats.endtime >= eL3[u].stats.endtime and eL1[i].stats.starttime < eL3[u].stats.endtime:
                        lf.append(eL3[u])
                        times.append(l3.getEventTimes()[u])
                        types.append(l3.getEventTypes()[u])
                        i += 1
                        u += 1
                        break
                    elif eL1[i].stats.endtime <= eL3[u].stats.endtime and eL1[i].stats.endtime > eL3[u].stats.starttime:
                        lf.append(eL1[i])
                        times.append(l1.getEventTimes()[i])
                        types.append(l1.getEventTypes()[i])
                        i += 1
                        u += 1
                        break                    
                    elif (eL1[i].stats.starttime  >= eL3[u].stats.endtime):# inicialt  >= finalt 
                        u += 1 
                    elif (eL3[u].stats.starttime  >= eL1[i].stats.endtime):
                        i += 1
                        break 
                #flag1 = True
            elif flag4 and (eL3[u].stats.starttime  >= eL1[i].stats.endtime):
                while True and flag3:
                    if abs(eL1[i].stats.starttime - eL2[o].stats.starttime) <= seconds:
                        lf.append(eL1[i])
                        times.append(l1.getEventTimes()[i])
                        types.append(l1.getEventTypes()[i])
                        o += 1
                        i += 1
                        break
                    elif eL1[i].stats.endtime >= eL2[o].stats.endtime and eL1[i].stats.starttime < eL2[o].stats.endtime:
                        lf.append(eL2[o])
                        times.append(l2.getEventTimes()[o])
                        types.append(l2.getEventTypes()[o])
                        o += 1
                        i += 1
                        break
                    elif eL1[i].stats.endtime <= eL2[o].stats.endtime and eL1[i].stats.endtime > eL2[o].stats.starttime:
                        lf.append(eL1[i])
                        times.append(l1.getEventTimes()[i])
                        types.append(l1.getEventTypes()[i])
                        o += 1
                        i += 1
                        break                    
                    elif (eL1[i].stats.starttime >= eL2[o].stats.endtime):# inicialt  >= finalt 
                        o += 1
                    elif (eL2[o].stats.starttime >= eL1[i].stats.endtime):
                        i += 1
                        break 
            elif flag3 and flag4:
                flag1 = True
            elif flag4 and (eL1[i].stats.starttime  >= eL3[u].stats.endtime):
                u += 1
            elif flag3 and (eL1[i].stats.starttime >= eL2[o].stats.endtime):
                o += 1
            else:
                flag2 = False
            '''elif flag3 and abs(eL1[i].stats.endtime - eL2[o].stats.starttime) <= seconds:  #revisar si no hay falla por index out of bounds
                i += 1 
                flag1 = True
            elif flag4 and abs(eL1[i].stats.endtime - eL3[u].stats.starttime) <= seconds:
                i += 1 
                flag1 = True'''
        if flag2 == False:
            flag1 = True
        
        if flag1 and flag3 and flag4:
            print('entra: '+str(eL2[o].stats.starttime)+'/'+str(eL3[u].stats.starttime))
            print('entra: '+str(eL2[o].stats.endtime)+'/'+str(eL3[u].stats.endtime))
            if abs(eL2[o].stats.starttime - eL3[u].stats.starttime) <= seconds:
                lf.append(eL2[o])
                times.append(l2.getEventTimes()[o])
                types.append(l2.getEventTypes()[o])
                o += 1
                u += 1
            elif abs(eL2[o].stats.endtime - eL3[u].stats.endtime) <= seconds:
                lf.append(eL2[o])
                times.append(l2.getEventTimes()[o])
                types.append(l2.getEventTypes()[o])
                o += 1
                u += 1
            elif eL2[o].stats.endtime >= eL3[u].stats.endtime and eL2[o].stats.starttime <= eL3[u].stats.starttime:
                lf.append(eL3[u])
                times.append(l3.getEventTimes()[u])
                types.append(l3.getEventTypes()[u])
                o += 1
                u += 1
            elif eL2[o].stats.endtime <= eL3[u].stats.endtime and eL2[o].stats.starttime >= eL3[u].stats.starttime:
                lf.append(eL2[o])
                times.append(l2.getEventTimes()[o])
                types.append(l2.getEventTypes()[o])
                o += 1
                u += 1
            elif eL2[o].stats.endtime >= eL3[u].stats.endtime and eL2[o].stats.starttime < eL3[u].stats.endtime:
                lf.append(eL3[u])
                times.append(l3.getEventTimes()[u])
                types.append(l3.getEventTypes()[u])
                o += 1
                u += 1
            elif eL2[o].stats.endtime <= eL3[u].stats.endtime and eL2[o].stats.endtime > eL3[u].stats.starttime:
                lf.append(eL2[o])
                times.append(l2.getEventTimes()[o])
                types.append(l2.getEventTypes()[o])
                o += 1
                u += 1
            else: # como carajos usar diferencias de tiempocon aproximados o exactidud hasta min? hmmm datatime.datatime class

                '''if abs(eL3[u].stats.starttime - eL2[o].stats.endtime) <= seconds:# inicialt  >= finalt
                    o += 1
                elif abs(eL2[o].stats.starttime - eL3[u].stats.endtime) <= seconds:# inicialt  >= finalt
                    u += 1'''
                if eL3[u].stats.starttime >= eL2[o].stats.endtime:
                    o += 1
                elif eL2[o].stats.starttime >= eL3[u].stats.endtime:
                    u += 1                
        elif flag2 == False and flag3 == False:# se puede mejorar haciendo que toda la columna muera
            u += 1
        elif flag2 == False and flag4 == False:
            o += 1
        
        flag1 = False
            
        '''if len(eL1) + 1 == i and len(eL2) + 1 == o and len(eL3) + 1 == u:
            notDone = False'''
    
    return [lf, times, types]