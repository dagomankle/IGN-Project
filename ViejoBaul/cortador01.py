from obspy.core import read
from obspy.core import UTCDateTime
from obspy.signal.trigger import plot_trigger# importaciones obligatiores menos read dependiendo

#from obspy.signal.trigger import classic_sta_lta # si se quiere clasico
from obspy.signal.trigger import recursive_sta_lta# si se quiere recursivo etc

trace = read("C:\\Users\dagom\Documents\Geofisico\DatosPrueba\EC.APED..HNZ.D.2016.107 ")[0]

ftime =  UTCDateTime("2016-04-16 23:58:00")
trace = trace.slice(ftime, ftime+120)

df = trace.stats.sampling_rate

#cft = classic_sta_lta(trace.data, int(5*df), int ( 10 *df))
#plot_trigger(trace,cft,1.5,0.5)

cft = recursive_sta_lta(trace.data, int(5*df), int(10*df)) # define los tmanios de ventana 
plot_trigger(trace,cft,1.2,0.5) # se define la variacion a marcar