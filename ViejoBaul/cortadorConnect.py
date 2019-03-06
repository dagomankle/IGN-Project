import statistics
from obspy.core import read
from obspy.core import UTCDateTime
from obspy.signal.trigger import plot_trigger# importaciones obligatiores menos read dependiendo
from obspy.clients.arclink import Client# para generar la coneccion con la base de datos

thr_on = 1.1
thr_off = 0.99

clienteArclink = Client('test', '192.168.1.7', 18001)# coneccion al stream

#from obspy.signal.trigger import classic_sta_lta # si se quiere clasico
from obspy.signal.trigger import recursive_sta_lta# si se quiere recursivo etc

t = UTCDateTime('2017-01-23 05:00:00') # +5 horas para utc y poner la fecha deseada.
trace = clienteArclink.get_waveforms('EC', 'CAYR', '', 'SHZ',t,t+3600*2,route = False, compressed = False)[0] # tiempo adicional deseado en segundos 
df = trace.stats.sampling_rate

#cft = classic_sta_lta(trace.data, int(1*df), int ( 2.4 *df))
#plot_trigger(trace,cft,thr_on,thr_off)

#cambiar los valores de triggers de forma dinamica en relacion a un trace?

cft = recursive_sta_lta(trace.data, int(2.5*df), int(5*df)) # define los tmanios de ventana 
print("funca")
plot_trigger(trace,cft,thr_on,thr_off) # se define la variacion a marcar

#media = statistics.mean(trace)
#print(media)
#print(trace.data[4])

#trace.detrend()
#trace.plot()
#media = statistics.mean(trace)
#print(trace.data[4])

'''print(trace.data[4])

for x in range(0, len(trace.data)):
	trace.data[x] = trace.data[x]-media

print(trace.data[4])

#trace.data = [x-media for x in trace.data]

trace.plot()'''


#print(mean(trace))

# mseed  100 muestras por segundo cada posicion del arreglo representa un dato obtenido en 1/100 de segundo