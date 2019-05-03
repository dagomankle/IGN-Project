# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 00:15:25 2019

@author: Dago
"""

'''for x in range(5):
    print(x)
    if x == 3:
        x = x-2'''
        
def lecturaIgn(name):
    listo = []
    # headers de lista
    # evol_id,esta_id_estacion,esta_code_estacion,evol_fecha,evol_fk_canal,evol_fecha_evento,evol_fecha_evento_p,evol_fecha_evento_s,evol_s_p,tevo_id_tipo,evol_coda,evol_amplitude_max,evol_amplitude_min,evol_unidad_amplitude,evol_rms,evol_polaridad,evol_peso,evol_frecuencia,evol_fk_estacion_canal,volc_id_volcan,evol_dr_cm2,evol_dr_sm2,evol_magnitud,evol_energia,evol_estado
    f = open(name,"r")
    for line in f:
        inner = []
        for word in line.split(","):
            inner.append(word)
            #print(word)
        inner = [inner[3], inner[5], inner[11]]
        listo.append(inner)
    f.close()
  
    return listo

def lecturaDago(name):
    listo = []
    # headers de lista
    # evol_id,esta_id_estacion,esta_code_estacion,evol_fecha,evol_fk_canal,evol_fecha_evento,evol_fecha_evento_p,evol_fecha_evento_s,evol_s_p,tevo_id_tipo,evol_coda,evol_amplitude_max,evol_amplitude_min,evol_unidad_amplitude,evol_rms,evol_polaridad,evol_peso,evol_frecuencia,evol_fk_estacion_canal,volc_id_volcan,evol_dr_cm2,evol_dr_sm2,evol_magnitud,evol_energia,evol_estado
    f = open(name,"r")
    for line in f:
        inner = []
        for word in line.split(","):
            inner.append(word)
            #print(word)
        if len(inner) > 1:
            listo.append(inner)
    f.close()
  
    return listo

def sortAmp(lista, minAmp):
    result = []
    for register in lista:
        if (abs(float(register[2])) >= minAmp):
            result.append(register)
            
    return result

def printo(name, listo):# se puede modificar para acomodar a los tokens deseados. 
    f = open(name + ".txt","w+")
    f.write("Tiempo inicio de picado,Tiempo Fin de picado, Amplitud\r\n" )
    for i in range(len(listo)):
        f.write(listo[i][0] + "," + listo[i][1] + ","+ listo[i][2] + "\r\n")
    f.close()

# headers necesarios index: 3 ti, 5 tf, 11 amp
ignResult = lecturaIgn("SmCotoEne2018.txt")
ignResult.pop(0)
ignSort = sortAmp(ignResult, 1000)
printo("comparaIgn.txt", ignSort)

dagoResult = lecturaDago("resultadosSub1000.txt")
dagoResult.pop(0)
dagoResult.pop(1)
dagoSort = sortAmp(dagoResult, 1000)
printo("comparaDago.txt", dagoSort)