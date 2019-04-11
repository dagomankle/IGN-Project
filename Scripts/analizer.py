import matplotlib.pyplot as plt
from obspy.core import read, UTCDateTime
from obspy.signal.trigger import plot_trigger, recursive_sta_lta, trigger_onset, classic_sta_lta, ar_pick
import SegmenterAlfa3
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
        
        self.__lEventTimes.append(trace)
        self.__finalTraces.append(trace)

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
		
        return self.__analisiSTALTA( trace,1.6,0.5,5, 10)

    def __analisiSTALTA(self, trace, thr_on, thr_off, windowop, windowend): # falta controlar los piocs iniciales del alg !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        df = trace.stats.sampling_rate
        cft = recursive_sta_lta(trace.data, int(windowop*df), int(windowend*df)) # define los tmanios de ventana 
        #cft = classic_sta_lta(trace.data, int(windowop*df), int(windowend*df)) # define los tmanios de ventana 
        onOf = trigger_onset(cft, thr_on, thr_off)
        
        self.__defineTimes(trace, onOf)
        plot_trigger(trace,cft,thr_on,thr_off)
        
        # como fucking tener bien marcado el s y p .... sacar los pilches 3 tipos de seniales.
        #p_pick, s_pick = ar_pick(tr1.data, tr2.data, tr3.data, df, 1.0, 20.0, 1.0, 0.1, 4.0, 1.0, 2, 8, 0.1, 0.2)
        #https://docs.obspy.org/tutorial/code_snippets/trigger_tutorial.html
        
        #print(p_pick)
        #print(s_pick)

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

    def __defineTimes(self, trace, onOf):
        
        for x in range(0, len(onOf)):
            start = trace.stats.starttime + onOf[x][0]*(1/trace.stats.sampling_rate)
            end = trace.stats.starttime +  onOf[x][1]*[1/trace.stats.sampling_rate][0] #porque demonios se construye una lista??! el 1 tiene mas datos?
            tupla = [start, end]
            print(start)
            print(end)
            self.__lEventTimes.append(tupla)
            novoTrace = trace.slice( start, end)
            novoTrace.plot()
            self.__finalTraces.append(novoTrace)

    def setExternalevTimes(self):
        return True

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

