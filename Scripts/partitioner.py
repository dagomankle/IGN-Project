from obspy.core import read
from obspy.core import UTCDateTime
from obspy.signal.trigger import plot_trigger# importaciones obligatiores menos read dependiendo
from obspy.clients.arclink import Client# para generar la coneccion con la base de datos

thr_on = 1.1
thr_off = 0.99
tiempoSismo = 360

tiempoAntes = tiempoSismo/2
tiempoDespues = tiempoSismo/2

clienteArclink = Client('test', '192.168.1.7', 18001)# coneccion al stream

#from obspy.signal.trigger import classic_sta_lta # si se quiere clasico
from obspy.signal.trigger import recursive_sta_lta# si se quiere recursivo etc

t = UTCDateTime('2017-01-01 05:00:00') # +5 horas para utc y poner la fecha deseada.
trace5 = clienteArclink.get_waveforms('EC', 'CAYR', '', 'SHZ',t,t+3600*2,route = False, compressed = False)[0] # tiempo adicional deseado en segundos 

puntoAlto = 0

for x in range(0, trace5.count()):
	if(trace5[x] == trace5.max()):
		puntoAlto = x

trace5 = trace5.slice(t+0.01*puntoAlto -tiempoAntes, t+0.01*puntoAlto+tiempoDespues)
df5 = trace5.stats.sampling_rate
cft5 = recursive_sta_lta(trace5.data, int(2.5*df5), int(5*df5)) # define los tmanios de ventana 
plot_trigger(trace5,cft5,thr_on,thr_off) # se define la variacion a marcar


# mseed  100 muestras por segundo cada posicion del arreglo representa un dato obtenido en 1/100 de segundo