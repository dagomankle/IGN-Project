from obspy.core import UTCDateTime
from obspy.clients.arclink import Client

clienteArclink = Client('test', '192.168.1.7', 18001)
t = UTCDateTime('2017-01-01 05:00:00') # +5 horas para utc y poner la fecha deseada.
stream = clienteArclink.get_waveforms('EC', 'CAYR', '', 'SHZ',t,t+3600*12,route = False, compressed = False) # tiempo adicional deseado en segundos 
stream.plot()