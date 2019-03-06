# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 12:28:34 2019

@author: Dago
"""

import Scripts.SegmenterAlfa3


def redo(l1,l2,l3) :
    
    e = False 
    
    if l1.getNumberELaps() == l2.getNumberELaps() == l3.getNumberELaps():
        e = True
        lf = timeChecker(l1,l2,l3)
    else:
        lf = timeChecker(l1,l2,l3, e)
    
    return lf

def timeChecker(l1,l2,l3,e):
    
    lf = []
    
    eL1 = l1.getEventLaps()
    eL2 = l2.getEventLaps()
    eL3 = l3.getEventLaps()
    
    if len(eL1) > len(eL2):  #establece la lista que tiene el mayor numero de partes
        asdf
    
    i = 0
    o = 0
    u = 0
    
    #for i in range(len(eL1)): #usar tiempos el subsearch times ni se que 
    while i < len(eL1):
        
        if eL1[i].getTrace() == eL2[i].getTrace():
            lf.append(eL1[i])
        elif eL1[i].getTrace() == eL3[i].getTrace():
            lf.append(eL1[i])
        elif eL2[i].getTrace() == eL3[i].getTrace():
            lf.append(eL2[i])    
    
    '''if e == True:        
        for i in range(len(eL1)): #usar tiempos el subsearch times ni se que 
            if eL1[i].getTrace() == eL2[i].getTrace():
                lf.append(eL1[i])
            elif eL1[i].getTrace() == eL3[i].getTrace():
                lf.append(eL1[i])
            elif eL2[i].getTrace() == eL3[i].getTrace():
                lf.append(eL2[i])
    else:
        asdf'''
    
    return lf 
