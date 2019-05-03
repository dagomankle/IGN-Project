#python 3 || obspy || windows2010
# Hecho por Daniel Ginez
#from sys import exit 
from obspy.core import read, UTCDateTime
from datetime import datetime, date, time
from obspy.clients.arclink import Client# para generar la coneccion con la base de datos
from obspy.signal.invsim import corn_freq_2_paz

class SignalDg:
    def __init__(self, *args):
        lArgs = []
        argNum = len(args)
        for arg in args:
            lArgs.append(arg)
        multiple = True
        starter = True

        if argNum == 8 :
            # ejemplo seg = Signal('EC','CAYR','','SHZ','2017-01-24 00:00:00', 24, 500, 320)
            try:
                print("Bienvenido a la primera clase de GeoDago")
                clienteArclink = Client('test', '192.168.1.7', 18001)# coneccion al stream
                self.__t = UTCDateTime(lArgs[4]) # +5 horas para utc y poner la fecha deseada. Hay que automatizar esto
                self.__tf = self.__t + 3600*lArgs[5]
                self.__oTrace = clienteArclink.get_waveforms(lArgs[0], lArgs[1], lArgs[2], lArgs[3],self.__t,self.__tf,route = False, compressed = False)
                self.__trace= clienteArclink.get_waveforms(lArgs[0], lArgs[1], lArgs[2], lArgs[3],self.__t,self.__tf,route = False, compressed = False)[0] # se obtiene el trazo principal
                self.__minimumPointEvent = lArgs[6]# amplitud minima 
                self.__analisisTimeLapse = lArgs[7]
                print("\nconeccion exitosa")
            except ValueError:
                print("Error en la coneccion")

        elif argNum == 5:
            #ejemplo : main = Signal(trace.slice(timei,timef) ,timei ,timef, self.__minimumPointEvent,self.__analisisTimeLapse)            
            self.__trace = lArgs[0]
            self.__t = lArgs[1] # +5 horas p^^ara utc y poner la fecha deseada. Hay que automatizar esto,
            self.__tf = lArgs[2]
            self.__minimumPointEvent = lArgs[3]
            self.__analisisTimeLapse = lArgs[4]

        elif argNum == 4:# se corre el script para un trazo unico
            #seg = SignalDg(self.__oTrace[x], self.__frecuencia, self.__analisisTimeLapse, "trace")
            multiple = False
            starter = False
            self.__oTrace = lArgs[0]
            self.__trace = lArgs[0]
            self.__t = self.__trace.stats.starttime
            self.__tf = self.__trace.stats.endtime
            self.__minimumPointEvent = lArgs[1]
            self.__analisisTimeLapse = lArgs[2]

        elif argNum == 3:# falta poner una excepcion de archivo mal leido
            #seg = Signal('volcan.mseed', 1000, 320)
            starter = False
            self.__oTrace = read(lArgs[0])
            self.__trace = read(lArgs[0])[0]
            self.__t = self.__trace.stats.starttime
            self.__tf = self.__trace.stats.endtime
            self.__minimumPointEvent = lArgs[1]
            self.__analisisTimeLapse = lArgs[2]
            
        elif argNum == 2 : # cuando se envia un trazo completo 
            #seg = Signal(trace, [1000, 320])
            starter = False
            self.__oTrace = lArgs[0]
            self.__trace = (lArgs[0])[0]
            self.__t = self.__trace.stats.starttime
            self.__tf = self.__trace.stats.endtime
            self.__minimumPointEvent = lArgs[1][0]
            self.__analisisTimeLapse = lArgs[1][1]
        else:
            print("Argumentos no aceptables")
            sys.exit()

        self.__trace.detrend()# funcion de la libreria stream que quita la media de un trazo para que este se encuentre encerado.
        paz = corn_freq_2_paz(1.0, damp=1)  #0.707
        paz['sensitivity'] = 1.0
        self.__trace.simulate( paz_simulate=paz)
        self.__frecuencia = self.__trace.stats.sampling_rate
        self.__eventTraceList = []
        self.__subSearchTimeTraces = []# se usa para el control de la recursion durante la construccion del objeto, al final almcenara espacios de busqueda con un filtro
        self.__highestPoint = self.__trace.max()
        self.__noDataTimes = []

        if argNum != 5:
            if self.__eventObteiner(self.__trace, self.__t):
                self.__subTracesManager(self.__trace)
                self.__subSearchTimeTraces = self.__timesOrganizer()
                if multiple:
                    self.__incomingTraces()    
                if starter: 
                    print("hey ho wtf")    
                    self.__subSegmenter()            

    def __incomingTraces(self):# dado que si se interrumpe la señal un trazo se compone de varios puestos en el objeto trazo de forma bidimensional
        if len(self.__oTrace) != 1:
            print ("\n Datos incompletos en relacion al tiempo")
            for x in range(1, len(self.__oTrace)):
                senial = SignalDg(self.__oTrace[x], self.__minimumPointEvent, self.__analisisTimeLapse, "trace")
                self.__eventTraceList.extend(senial.getEventLaps())
                self.__subSearchTimeTraces.extend(senial.getTimes("T"))
                if self.__highestPoint < senial.getMaxAmp():
                    self.__highestPoint = senial.getMaxAmp()
                self.__tf = senial.getETime()
        else:
            print("Datos Completos")

    def __gapSetter(self):
        tiempos = []
        for x in range(0, len(self.__oTrace)-1):
            self.__noDataTimes.append([self.__oTrace[x].stats.endtime, self.__oTrace[x+1].stats.starttime])
        if self.__oTrace[-1].stats.endtime < self.__tf:
            self.__noDataTimes.append([self.__oTrace[-1].stats.endtime, self.__tf])
        self.__tf = self.__oTrace[-1].stats.endtime

    def __subTracesManager(self, trace):#funcion que gestiona la segmentacion del trazo para iniciar los analisis detallados

        aTime = self.__subSearchTimeTraces[-1][0]
        saTime = self.__timePicker(aTime, "a")
        bTime = self.__subSearchTimeTraces[-1][1]
        sbTime = self.__timePicker(bTime, "b")        
        
        if(aTime != saTime and self.__redundanceCheck(saTime,aTime)):
            subTraceA = trace.slice( saTime,aTime)        
            if self.__eventObteiner(subTraceA, saTime):
                self.__subTracesManager(subTraceA)

        if(bTime != sbTime and self.__redundanceCheck(bTime,sbTime)):
            subTraceB = trace.slice(bTime,sbTime)

            if self.__eventObteiner(subTraceB, bTime):
                self.__subTracesManager(subTraceB)

    #es necesario optimizar esta funcion; incluirla en timpicker de alguna forma talvez
    def __redundanceCheck(self, timei, timef): # al usar la recursion bifurcada las hojas de la misma pueden sobreescribirse por ende se cehquea q nose ha analizado el segmento
        control = True
        for x in range(0,len(self.__subSearchTimeTraces)):
            if(self.__subSearchTimeTraces[x][0] == timei and self.__subSearchTimeTraces[x][1] == timef):
                control = False
                break

        return control

    def __timePicker(self, time, type):#regresa el siguiente tiempo elegible para determinar  una traza
        control = True
        dateReturn = UTCDateTime('1000-01-10 05:00:00')
        if type == "a": # si se tiene la fecha de inicio buscara la fecha de finalizacion
            for x in range(0,len(self.__subSearchTimeTraces)):
                if(time > self.__subSearchTimeTraces[x][1]):
                    control = False
                    if dateReturn < self.__subSearchTimeTraces[x][1]:
                        dateReturn = self.__subSearchTimeTraces[x][1]

            if control:
                dateReturn = self.__t
        else:# si se tiene la fecha de fin se buscara la de inicio
            for x in range(0,len(self.__subSearchTimeTraces)):
                if(time <= self.__subSearchTimeTraces[x][0]):
                    control = False
                    if dateReturn < self.__subSearchTimeTraces[x][0]:
                        dateReturn = self.__subSearchTimeTraces[x][0]

            if control:
                dateReturn = self.__tf

        return dateReturn

    def __eventObteiner(self, trace, t):
        topPoint = trace.max()
        if abs(topPoint) >= self.__minimumPointEvent:
            puntoAlto = self.__highestPointPosition(trace,topPoint)
            timei = t+(1/self.__frecuencia)*puntoAlto - self.__analisisTimeLapse/2
            if timei < t:
                timei = t
            timef = t+(1/self.__frecuencia)*puntoAlto + self.__analisisTimeLapse/2
            sTrace = trace.slice(timei,timef)
            main = SignalDg(sTrace , sTrace.stats.starttime ,sTrace.stats.endtime, self.__minimumPointEvent,self.__analisisTimeLapse)# el segemento se toma como evento y se crea como nuevo Objeto signal !!!!!!!!!!!!!!1!!!!!
            self.__eventTraceList.append(main)
            tiempos = [timei, timei+(1/self.__frecuencia)*(main.__trace.count()-1), "E"]
            if tiempos not in self.__subSearchTimeTraces:
                self.__subSearchTimeTraces.append([timei, timei+(1/self.__frecuencia)*(main.__trace.count()-1), "E"])# veremos si se usa !!!!!!!!!!!!!!!!!
            print("\nTiempos usados registrados")
            print(self.__subSearchTimeTraces[-1][0])
            print(self.__subSearchTimeTraces[-1][1])
            return True
        else:
            timei = t
            timef = t+(1/self.__frecuencia)*(trace.count()-1)
            self.__subSearchTimeTraces.append([timei, timef, "N"])            
            return False

    def __timesOrganizer(self):# organiza los tiempos usados guardados en base a la existencia de eventos
        internal = []
        internal2 = []
        i = 0                
       
        for x in range(0,len(self.__subSearchTimeTraces)):
            control = True
            o = -1
            if self.__subSearchTimeTraces[x][2] == "E":
                for y in range(0,len(internal)):
                    if internal[y][2] == "E":                        
                        o+=1
                    if x == 0:
                        internal.append(self.__subSearchTimeTraces[0])
                        internal2.append(self.__eventTraceList[0])
                        control = False
                        break
                    elif self.__subSearchTimeTraces[x][1] <= internal[y][0]:
                        internal.insert(y,self.__subSearchTimeTraces[x])
                        internal2.insert(o,self.__eventTraceList[i])
                        control = False
                        break
                if control:
                    internal.append(self.__subSearchTimeTraces[x])
                    internal2.append(self.__eventTraceList[i])
                i = i+1
                
            else:
                for y in range(0,len(internal)):
                    if x == 0:
                        internal.append(self.__subSearchTimeTraces[0])
                        control = False
                        break
                    elif self.__subSearchTimeTraces[x][1] <= internal[y][0]:
                        internal.insert(y,self.__subSearchTimeTraces[x])
                        control = False
                        break
                if control:
                    internal.append(self.__subSearchTimeTraces[x])
                               
        self.__eventTraceList = internal2
        return internal
    

    def __highestPointPosition(self, trace, highestPoint):
        for x in range(0,trace.count()):
            if(trace[x] == highestPoint):
                return x# retorna la posicion de la diferencia mas alta que se puede encontrar

    def __subSegmenter(self):# se trabaja ocn tipo de datos SignalDg
        toBeReplaced = []
        positions = []
        
        for y in range (0, len(self.__subSearchTimeTraces)):
            if(self.__subSearchTimeTraces[y][2] == "E"):
                positions.append(y)

        for x in range(0, len(self.__eventTraceList)):
            print("\n PARA EL TRAZO:   ", x)
            trace = self.__eventTraceList[x].getTrace()
            media = self.__localMean(trace)
            control = True
            exist = []
            sss = []
            
            d = 0
            u = 0
            pos = self.__highestPointPosition(trace, self.__eventTraceList[x].getMaxAmp()) #Se plantea una venta de separacion entre los sismos de 20 

            for y in range(0, int(pos -15*self.__frecuencia)):# en el segemento anterior se puede hacer un for para determinar el punto exacto en el que  las muestras salen de la media 
                if control:
                    if trace[y] <= media:
                        control = False
                        d = y + 3*self.__frecuencia
                        y = d
                elif trace[y] >= self.__minimumPointEvent:
                    control = True 
                    u =  y - 15*self.__frecuencia # 15 segundos completos antes del punto alto del sismo sera ?
                    exist.append((u-d) /2)

            for y in range(pos, len(trace)):
                if control:
                    if trace[y] <= media:
                        control = False
                        d = y + 3*self.__frecuencia
                        y = d
                elif trace[y] >= self.__minimumPointEvent:
                    control = True 
                    u =  y - 15*self.__frecuencia # 15 segundos completos antes del punto alto del sismo sera ?
                    exist.append((u-d) /2)

            print("\n Arreglo Exist:\n")
            for y  in exist:
                print(y)

            print("\n tiempos del SS:\n" )
            timei = trace.stats.starttime
            for y in range(0, len(exist)):# poner el  tiempo final
                timef = trace.stats.starttime + exist[y]/self.__frecuencia
                
                print("inicio: ", timei)
                print("final:  ", timef)
                sTrace = trace.slice(timei,timef)
                main = SignalDg(sTrace , sTrace.stats.starttime ,sTrace.stats.endtime, self.__minimumPointEvent,self.__analisisTimeLapse)
                sss.append(main)
                timei = timef

            sTrace = trace.slice(sss[-1].getTrace().stats.endtime,trace.stats.endtime)
            sss.append(SignalDg(sTrace , sTrace.stats.starttime ,sTrace.stats.endtime, self.__minimumPointEvent,self.__analisisTimeLapse))

            if len(sss) > 0:
                toBeReplaced.append(sss, x, positions[x])

        d = 0
        for x in range(0,len(toBeReplaced)):
            pos = toBeReplaced[x][1]
            pos2 = toBeReplaced[x][2] + d 

            self.__eventTraceList.pop([pos + d])
            self.__subSearchTimeTraces. pop([pos2])
            for y in range(0,  len(toBeReplaced[x][0])):
                self.__eventTraceList.insert(pos + d,toBeReplaced[x][0][y])
                self.__subSearchTimeTraces.insret(pos2 + d, [toBeReplaced[x][0][y].getTrace().stats.starttime, toBeReplaced[x][0][y].getTrace(), "E" ])
                d = d+1

    def __localMean(serlf, trace):
        suma = 0
        for x in range(0, len(trace)):
            suma = suma + trace[x]
        return suma / len(trace) 

    def __timeAranger(self): #arregla los eventos guardados por orden de tiempo, optimización seria incluir en el momento en que se va a guardar un trazo
        hola = 1

# LAS FUNCIONES SIGUIENTES NO SON PARTE FUNCIONAL DE LA CREACION DEL OBJETO; SON FUNCIONES DE MUESTREO U OBTENCION DE DATOS

# falta lograr encapsulacion :S a pesar del get se pasa la informacion; la solucion seria crear una nueva lista y copiar de uno en uno los datos o algo asi 

    def getTimes(self, letra ):# imprime todos los tiempos analisados si se pone t de arugmento, con e solo tiempos de eventos si se pone n los trazos sin eventos
        times = []
        if letra == "T":
            for x in range(0,len(self.__subSearchTimeTraces)):
                times.append(self.__subSearchTimeTraces[x])
        elif letra == "E" or "N":
            for x in range(0,len(self.__subSearchTimeTraces)):
                if(self.__subSearchTimeTraces[x][2] == letra):
                    times.append(self.__subSearchTimeTraces[x])
        else:
            print("Fracaso")

        return times

    def getStats(self):
        status = self.__trace.stats
        return status

    def getMinPoint(self):
        min = self.__minimumPointEvent
        return min

    def getTrace(self):
        trace = self.__trace
        return trace

    def getOTrace(self):
        trace = self.__oTrace
        return trace

    def getFrecuencia(self):
        frecuencia = self.__frecuencia
        return frecuencia

    def getSTime(self):
        sTime = self.__t
        return sTime

    def getETime(self):
        eTime = self.__tf
        return eTime

    def getMaxAmp(self):
        hp = self.__highestPoint
        return hp

    def getEventLaps(self): # se debe hacer sobre carga con args para obtener solo uno de los laps
        eLaps = self.__eventTraceList
        return eLaps

    def plotEventLaps(self):# se debe hacer sobre carga con args para plotear solo uno
        num = 0 
        for x in self.__eventTraceList:
            print(num)
            num =num + 1
            x.getTrace().plot()

    def getNumberELaps(self):
        return len(self.__eventTraceList)

    def plotNoEvents(self):
        for x in range(0,len(self.__subSearchTimeTraces)):
            if(self.__subSearchTimeTraces[x][2] == "N"):
                self.__trace.slice( self.__subSearchTimeTraces[x][0],self.__subSearchTimeTraces[x][1]).plot()    

    def getNoDataTimes(self): # se debe hacer sobre carga con args para obtener solo uno de los laps
        nodata = self.__noDataTimes
        return nodata
    
    def addEventLaps(self, moreEventLaps): # se debe hacer sobre carga con args para obtener solo uno de los laps
        self.__eventTraceList.extend(moreEventLaps)
        
    def addNoDataTimes(self, data): # se debe hacer sobre carga con args para obtener solo uno de los laps
        self.__noDataTimes.extend(data)

#horai=datetime.now()
#tipo A ---- ( nombre1, nombre2, nombre3, nombre4, fechaInicio, horas a anlizar, amplitud minima, ventanas de tiempo) ---- 8 argumentos
#seg = SignalDg('EC','CAYR','','SHZ','2016-02-19 00:00:00', 24, 1000, 320)
#seg = SignalDg('EC.BVC2..BHZ.D.2018.002', 1000, 320)
#seg = SignalDg('volcan.mseed', 1000, 320)
#horaf=datetime.now()-horai

#print("\n Contando con los segundos de coneccion el script tomo: ",horaf)

#tipo C ---- (direccion del archivo, amplitud minima, ventanas de tiempo)---- 3 argumentos
#seg = Signal('volcan.mseed', 1000, 320)



