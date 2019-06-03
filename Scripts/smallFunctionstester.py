# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 00:15:25 2019

@author: Dago
"""
from datetime import datetime, date, time
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
    f.write("Picado P, Picado S, Amplitud\r\n" )
    for i in range(len(listo)):
        f.write(listo[i][0] + "," + listo[i][1] + ","+ listo[i][2] + "\r\n")
    f.close()
    
def converDates(lista, tipo):
    lectorat = []
    if tipo == 0:
        for register in lista:#1/17/2018 17:55:57
            fecha = datetime.strptime(register[1], '%m/%d/%Y %H:%M:%S')
            lectorat.append(fecha)
    else:
        for register in lista:
            text = register[0].replace('T',' ')
            text = text.replace('Z','')
            fecha = [datetime.strptime(text, '%Y-%m-%d %H:%M:%S.%f'),register[3]]
            lectorat.append(fecha)
    
    return lectorat
    
def comparador(name,ign, geoDago, seconds):
    ignDates = converDates(ign,0)
    dgDates = converDates(geoDago,1) 
    resultati=[0,0,0,0,0]# 5 partes 0 = eventos ign, 1= eventos dg, 2= excepciones dg, 3 = faltas ign, 4 = faltas dg
    i = 0
    u = 0
    ronda = 1
    flag1 = True
    flag2 = True
    print(len(ignDates))
    print(len(dgDates))
    
    while flag1 or flag2:
        #print()
        #print(ronda)
        '''if flag1:
            print(ignDates[i])
            print(i)'''
        if flag2:
            print()
            print(ronda)
            print(dgDates[u][0])
            print(u)
            print(dgDates[u][1])
            print(len(dgDates[u][1]))
        '''if flag1 and flag2:
            print((ignDates[i] - dgDates[u][0]))
            print((ignDates[i] - dgDates[u][0]).total_seconds())'''
            
        
        
        '''print(flag1)
        print(flag2)'''
        
        if flag1 and flag2:
            if abs((ignDates[i] - dgDates[u][0]).total_seconds()) <= seconds:# ignDates -- dgDates 
                resultati[0] += 1
                resultati[1] += 1
                if len(dgDates[u])[1] == 4:
                    resultati[2] += 1
                i += 1
                u += 1
            elif (ignDates[i] - dgDates[u][0]).total_seconds() > 0 : # ignDates > dgDates
                print("holi")
                resultati[1] += 1
                resultati[4] += 1
                if len(dgDates[u][1]) == 4:
                    print("chau")
                    resultati[2] += 1
                u += 1
            else:
                resultati[0] += 1
                resultati[3] += 1
                if len(dgDates[u][1]) == 4:
                    print("chau")
                    resultati[2] += 1
                u += 1
                
        elif flag1:
            resultati[0] += 1
            resultati[3] += 1
            i +=1
        elif flag2:
            resultati[1] += 1
            resultati[4] += 1
            if len(dgDates[u][1]) == 4:
                resultati[2] += 1
            u += 1
            
        if i >= len(ignDates):
            flag1 = False
        if u >= len(dgDates):
            flag2 = False
        
        ronda +=1
    
    print(resultati[3])
    f = open(name + ".txt","w+")
    f.write("Total eventos Ign:"+ str(resultati[0])+"\r\n" )
    f.write("Total eventos GeoDago:"+ str(resultati[1])+"\r\n" )
    f.write("Total excepciones GeoDago:"+ str(resultati[2])+"\r\n" )
    f.write("Relacion: total eventos Ign a GeoDago ="+ str((resultati[0]*100) / resultati[1])+"%\r\n" )
    f.write("Relacion: total eventos GeoDago a Ign ="+ str((resultati[1]*100) / resultati[0])+"%\r\n" )
    f.write("Porcentaje de excepciones en GeoDago ="+ str((resultati[2]*100) / resultati[1])+"%\r\n" )
    f.write("Total eventos detectados por GeoDago y no Ign:"+ str(resultati[3])+"\r\n" )
    f.write("Total eventos detectados por Ign y no GeoDago:"+ str(resultati[4])+"\r\n" )
    f.close()    

# headers necesarios index: 3 ti, 5 tf, 11 amp
ignResult = lecturaIgn("SmCotoEne2018.txt")
ignResult.pop(0)
ignSort = sortAmp(ignResult, 1000)
printo("comparaIgn", ignSort)

dagoResult = lecturaDago("resultados.txt")
dagoResult.pop(0)
#dagoSort = sortAmp(dagoResult, 1000)
#printo("comparaDago.txt", dagoResult)

comparador("comparacionFinal",ignSort,dagoResult, 10)