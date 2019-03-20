# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 12:28:34 2019

@author: Dago
"""

#import Scripts.SegmenterAlfa3
import SegmenterAlfa3

def redo(l1,l2,l3) :
    
    e = False 
    
    if l1.getNumberELaps() == l2.getNumberELaps() == l3.getNumberELaps():
        e = True
        lf = timeChecker(l1,l2,l3)
    else:
        lf = timeChecker(l1,l2,l3, e)
    
    return lf

def timeCheckerS(l1,l2,l3):
    
# para usar mas de una fuente en la redundancia se podria usar args y listas para tener mayor cantidad ee variables se 
# usaria la misma estructura de ifs pero en los contenidos se llamaria a funciones en las que se trabajaria con foreachs 
# para definir bien la comparacion. no se puede usar una matriz grande puesto que no se tiene lapsos de tiempo definidos    
    
    lf = []
    
    eL1 = l1.getEventLaps()
    eL2 = l2.getEventLaps()
    eL3 = l3.getEventLaps()
   
     
    '''
    lm = []
    if len(eL1) >= len(eL2):#establece la lista que tiene el mayor numero de elementos para el funcionamiento
        lm = [eL1, eL2]
    else:
        lm = [eL2, eL1]
    
    if len(lm[0]) >= len(eL3):
        if len(lm[1]) >= len(eL3):
            lm.append(eL3)
        else:
            lm.insert(1, eL3)
    else:
        lm.insert(0, eL3)'''
     
    
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
        
        if len(eL1) < i:
            flag2 = False
        if len(eL2) < o:
            flag3 = False
        if len(eL3) < u:
            flag4 = False
        
        if flag2:
            if eL1[i].getTrace() == eL2[o].getTrace() == eL3[u].getTrace():
                lf.append(eL1[i])
                i += 1
                o += 1
                u += 1
            elif flag3 and eL1[i].getTrace() == eL2[o].getTrace():
                lf.append(eL1[i])
                i += 1
                o += 1
                if flag4 and eL1[i].getTrace() >= eL3[u].getTrace():# inicialt  >= finalt 
                    u += 1
            elif flag4 and eL1[i].getTrace() == eL3[u].getTrace():
                lf.append(eL1[i])
                i += 1
                u += 1
                if flag3 and eL1[i].getTrace() >= eL2[o].getTrace():# inicialt  >= finalt 
                    o += 1
            elif eL1[i].getTrace() <= eL2[o].getTrace() and eL1[i].getTrace() <= eL3[u].getTrace(): #revisar si no hay falla por index out of bounds
                i += 1 
                flag1 = True
            else:
                flag1 = True
        
        if flag1 and flag3 and flag4:
            if eL2[o].getTrace() == eL3[u].getTrace(): # arreglar para que no se repita, definir el flag
                lf.append(eL2[o])
                o += 1
                u += 1
            else: # como carajos usar diferencias de tiempo
                if eL3[u].getTrace() >= eL2[o].getTrace():# inicialt  >= finalt
                    o += 1
                if eL2[o].getTrace() >= eL3[u].getTrace():# inicialt  >= finalt
                    u += 1
        
        flag1 = False
            
        '''if len(eL1) + 1 == i and len(eL2) + 1 == o and len(eL3) + 1 == u:
            notDone = False'''
    
    return lf 
