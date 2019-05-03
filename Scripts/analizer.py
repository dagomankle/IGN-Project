#import matplotlib.pyplot as plt
from obspy.core import read, UTCDateTime
from obspy.signal.trigger import plot_trigger, recursive_sta_lta, trigger_onset, ar_pick, classic_sta_lta, carl_sta_trig, delayed_sta_lta
#import SegmenterAlfa3
#from obspy.signal.trigger import classic_sta_lta # si se quiere clasico

class Partitioner:

	# recibe trazos en una lista conformada por  clases SignalDg; debe aumentarse para que reciba listas de trazos cualquiera! ( aunque no hay un prog q haga eso muhahahahahahahahahahah)
    def __init__(self, lSignalDg, puntoMinimo):  # talvez args aqui
        self.__minimo = puntoMinimo
        self.__lEventTimes = []
        self.__signalsDg = lSignalDg
        self.__finalTraces = []
        for x in range(0, len(lSignalDg)):
            print(x)
            self.__preOrganizer(lSignalDg[x])

	# desde esta funcion se  correran las funciones stalta y se decidira que curso tomar. Podria ser oportuno usar los subsegmenters en esta parte.
    def __preOrganizer(self, signalDg):
        trace = signalDg.getTrace()        
        trace = self.__autoStalta(trace)
        
        '''if self.__specialCases(trace):
            self.__autoStalta(trace)
            if len(cant) == 1 :
                self.__lEventTimes.extend(self.__defineTimes(cant))
            else:
                cant = self.__autoStalta(trace)	'''		     	

    def __specialCases(self, trace): #calcular la diferencia de tiempos entre puntos altos  si existen dos picos  es un caso espeical de  lo contrario no
        ans = False
        return ans

	#desarrollar metodos que permitan la automatizacion  de  los parametros optimos para elanalisis
    def __autoStalta(self, trace):
		#trace.filter("lowpass", freq=2.0, corners = 2, zerophase = False )  
        # osea la parametrizacion para cada segmento de preferencia aqui mismo no en otra funcion
		#wop = sta wend lta?
		
        return self.__analisiSTALTA( trace,5,0.4,2, 20)#como ajustar ... 1.6,0.5,2, 17/ full bien 3.5,0.5,2, 20 //5,0.4,2, 20 besto para 1000 // 4,0.3,2, 20 500?

    def __analisiSTALTA(self, trace, thr_on, thr_off, windowop, windowend): # falta controlar los piocs iniciales del alg !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        print("general villamil")
        print(trace.std())
        df = trace.stats.sampling_rate
        cft = recursive_sta_lta(trace.data, int(windowop*df), int(windowend*df)) # define los tmanios de ventana 
        #cft = classic_sta_lta(trace.data, int(windowop*df), int(windowend*df)) # define los tmanios de ventana 
        #cft = carl_sta_trig(trace.data, int(5 * df), int(10 * df), 0.8, 0.8)
        #cft = delayed_sta_lta(trace.data, int(windowop * df), int(windowend * df))
        #plot_trigger(trace, cft, 5, 10)
        #onOf = trigger_onset(cft, 1.6, 0.5)
        onOf = trigger_onset(cft, thr_on, thr_off)
        
        # como fucking tener bien marcado el s y p .... sacar los pilches 3 tipos de seniales.
        #p_pick, s_pick = ar_pick(tr1.data, tr2.data, tr3.data, df, 1.0, 20.0, 1.0, 0.1, 4.0, 1.0, 2, 8, 0.1, 0.2)
        #p_pick, s_pick = ar_pick(trace, trace, trace, df, 1.0, 20.0, 1.0, 0.1, 4.0, 1.0, 2, 8, 0.1, 0.2)
        #https://docs.obspy.org/tutorial/code_snippets/trigger_tutorial.html
        
        print("con fe")
        
        p_pick = 0
        #print(trace.stats.starttime + p_pick)
        #print(trace.stats.starttime + s_pick)
        
        self.__defineTimes(trace, onOf, p_pick)
        plot_trigger(trace,cft,thr_on,thr_off)

        '''print("que onda")
		# Plotting the results
        ax = plt.subplot(211)
        plt.plot(trace.data, 'k')
        ymin, ymax = ax.get_ylim()

        plt.vlines(onOf[:, 0], ymin, ymax, color='r', linewidth=2)
        plt.vlines(onOf[:, 1], ymin, ymax, color='b', linewidth=2)

        plt.subplot(212, sharex=ax)
        plt.plot(cft, 'k')
        plt.hlines([thr_on, thr_off], 0, len(cft), color=['r', 'b'], linestyle='--')
        plt.axis('tight')'''
        #plt.show()

    def __defineTimes(self, trace, onOf, p_pick):
        extra = 0
        for x in range(0, len(onOf)):
            print("esp cas")
            print(trace.std())
            start = trace.stats.starttime + onOf[x][0]*(1/trace.stats.sampling_rate)
            end = trace.stats.starttime +  onOf[x][1]*[1/trace.stats.sampling_rate][0] #porque demonios se construye una lista??! el 1 tiene mas datos?
            tupla = [start, end]
            print(start)
            print(end)
            
            novoTrace = trace.slice( start, end)
            
            '''if x == 0:
                p_pick = trace.stats.starttime + p_pick
                self.__lEventTimes.append([tupla, p_pick]) # se vera [[s pick, end], p pick]
                #novoTrace = trace.slice( p_pick, end)
            else:
                self.__lEventTimes.append([tupla, extra])
                #novoTrace = trace.slice( extra, end)'''
            self.__lEventTimes.append(tupla)
            novoTrace.plot()
            extra = end
            self.__finalTraces.append(novoTrace)

    def setExternalevTimes(self, times):
        self.__lEventTimes = times

    def getEventTimes(self):
        return self.__lEventTimes 

    def getSignalsDg(self):
        return self.__signalsDg 
    
    def getFinalTraces(self):
        return self.__finalTraces
    
    def setFinalTraces(self, lf):
        self.__finalTraces = lf

    def setSignalsDg(self, signal):
        self.__signalsDg = signal
        
    def addPartitioners(self, partitioner):
        self.__lEventTimes.extend(partitioner.getEventTimes())
        self.__signalsDg.extend(partitioner.getSingalsDg())
        self.__finalTraces.extend(partitioner.setFinalTraces())
        
    def plotEventLaps(self):# se debe hacer sobre carga con args para plotear solo uno
        num = 0 
        for x in self.__finalTraces:
            print(num)
            num =num + 1
            x.plot()
        
    def printResultTimes(self):# se puede modificar para acomodar a los tokens deseados. 
        f = open("resultados.txt","w+")
        #f.write("Resultados\r\n\n Tiempo p, Tiempo s, Tiempo Fin de picado \r\n" )
        f.write("Tiempo inicio de picado,Tiempo Fin de picado\r\n" )
        for i in range(len(self.__lEventTimes)):
            #f.write(str(self.__lEventTimes[i][1]) + ", " + str(self.__lEventTimes[i][0][0]) + ", " + str(self.__lEventTimes[i][0][1]) + "\r\n")
            f.write(str(self.__lEventTimes[i][0]) + "," + str(self.__lEventTimes[i][1]) + "\r\n")
        f.close()
        
    def addPrintResultTimes(self):# se puede modificar para acomodar a los tokens deseados. 
        f = open("resultados.txt","a+")
        for i in range(len(self.__lEventTimes)):
            #f.write(str(self.__lEventTimes[i][1]) + ", " + str(self.__lEventTimes[i][0][0]) + ", " + str(self.__lEventTimes[i][0][1]) + "\r\n")
            f.write(str(self.__lEventTimes[i][0]) + "," + str(self.__lEventTimes[i][1]) + "\r\n")
        f.close()
        
    def printResult(self):# se puede modificar para acomodar a los tokens deseados. 
        f = open("resultados.txt","w+")
        #f.write("Resultados\r\n\n Tiempo p, Tiempo s, Tiempo Fin de picado \r\n" )
        f.write("Tiempo inicio de picado,Tiempo Fin de picado,Amplitud\r\n" )
        for i in range(len(self.__lEventTimes)):
            #f.write(str(self.__lEventTimes[i][1]) + ", " + str(self.__lEventTimes[i][0][0]) + ", " + str(self.__lEventTimes[i][0][1]) + "\r\n")
            f.write(str(self.__lEventTimes[i][0]) + "," + str(self.__lEventTimes[i][1]) +","+str(abs(self.__finalTraces[i].max())) + "\r\n")
        f.close()
        
    def addPrintResult(self):# se puede modificar para acomodar a los tokens deseados. 
        f = open("resultados.txt","a+")
        for i in range(len(self.__lEventTimes)):
            #f.write(str(self.__lEventTimes[i][1]) + ", " + str(self.__lEventTimes[i][0][0]) + ", " + str(self.__lEventTimes[i][0][1]) + "\r\n")
            f.write(str(self.__lEventTimes[i][0]) + "," + str(self.__lEventTimes[i][1]) +","+str(abs(self.__finalTraces[i].max())) + "\r\n")
        f.close()

print("Entrando al analizador yeahhh!")
'''
lis = [seg.getEventLaps()[6]]

anatron = PreAnalisis(lis, seg.getMinimumPoint)'''
#anatron = PreAnalisis(seg.getEventLaps, seg.get)


# Obtener los espectros:

'''

para el ploteo sin condiciones :

trace.spectrogram()




'''

#std de 200 ? para excepcion de tremor?

