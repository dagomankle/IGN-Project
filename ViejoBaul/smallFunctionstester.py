# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 00:15:25 2019

@author: Dago
"""

'''for x in range(5):
    print(x)
    if x == 3:
        x = x-2'''
        
i = 1

flag2 = True #para el1
flag3 = True #para el2
flag4 = True #para el3


while flag2 or flag3 or flag4:
  print(i)

  i += 1
  if i == 3:
      flag2 = False
      
  if i == 4 :
      flag3 = False
      
  if i == 5 :
      flag4 = False
      
  print(flag2)
  print(flag3)
  print(flag4)
  
  if i == 10:
      break
