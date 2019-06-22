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