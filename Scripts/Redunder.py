# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 12:28:34 2019

@author: Dago
"""

import SegmenterAlfa3

def redo(l1,l2,l3) :
    
    if l1.getNumberELaps() == l2.getNumberELaps() == l3.getNumberELaps():
        if timeChecker(l1,l2,l3):
            lf = l1
    
    return lf

def timeChecker():
    
    check = False
    
    return check