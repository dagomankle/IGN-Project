from obspy.core import read
from obspy.core import UTCDateTime
from obspy.signal.trigger import plot_trigger# importaciones obligatiores menos read dependiendo
from obspy.clients.arclink import Client# para generar la coneccion con la base de datos
#from obspy.signal.trigger import classic_sta_lta # si se quiere clasico
from obspy.signal.trigger import recursive_sta_lta# si se quiere recursivo etc


class Signal:
	def _init_(self, givenTrace,name1,name2,name3,name4, timeStart, hoursORtf, minimumPointEvent, analisisTimeLapse, type):
		if type == "a":# COnstructor que se conecta al servidor en la red local y obtiene un archivo determinado
			clienteArclink = Client('test', '192.168.1.7', 18001)# coneccion al stream
			self.t = UTCDateTime(timeStart) # +5 horas para utc y poner la fecha deseada. Hay que automatizar esto
			self.tf = self.t+3600*hoursORtf
			self.trace= clienteArclink.get_waveforms(name1, name2, name3, name4,self.t,self.tf,route = False, compressed = False)[0] # se obtiene el trazo principal

		if type == "b":# constructor que recibe un parametro trace para construir e objeto
			self.t = UTCDateTime(timeStart) # +5 horas para utc y poner la fecha deseada. Hay que automatizar esto,
			self.tf = hoursORtf
			self.trace = givenTrace

		if type == "c":# constructor que recibe uan direccion local para leer un archivo de disco
			self.trace = read(name1)[0]# obtener tiempo t de alguna forma, cortando string talvez

		self.minimumPointEvent = minimumPointEvent
		self.highestPoint = self.trace.max()
		self.analisisTimeLapse = analisisTimeLapse
		self.eventTraceList = []
		#self.subSearchTracesUsed = []
		self.subSearchTimeTraces = []

		if type != "b":
			if self.eventObteiner(self.trace, self.t):
				self.subTracesManager(self.trace)

	def subTracesManager(self, trace):
		stime = self.subSearchTimeTraces[subSearchTimeTraces.count() - 1][0]
		stTime = self.timePicker(stime, "a")
		subTraceA = self.trace.slice( stTime,stime)
		if self.eventObteiner(subTraceA, stTime):
			self.subTracesManager(subTrace)

		stime = self.subSearchTimeTraces[subSearchTimeTraces.count() - 1][1]
		subTraceB = self.trace.slice(stime,self.timePicker(stime, "b"))
		if self.eventObteiner(subTraceA, stime):
			self.subTracesManager(subTrace)

	def timePicker(self, time, type):
		control = True
		dateReturn = None
		if type == "a":
			for x in range(0,self.subSearchTimeTraces.count()):
				if(time > self.subSearchTimeTraces[x][0]):
					control = False
					dateReturn = self.subSearchTimeTraces[x][0]
					break
				elif(time > self.subSearchTimeTraces[x][1]):
					control = False
					dateReturn = self.subSearchTimeTraces[x][1]
					break

			if control:
				dateReturn = self.t
		else:
			for x in range(0,self.subSearchTimeTraces.count()):
				if(time > self.subSearchTimeTraces[x][0]):
					control = False
					dateReturn = self.subSearchTimeTraces[x][0]
					break
				elif(time > self.subSearchTimeTraces[x][1]):
					control = False
					dateReturn = self.subSearchTimeTraces[x][1]
					break

			if control:
				dateReturn = self.tf

		return dateReturn

	def eventObteiner(self, trace, t):
		topPoint = trace.max()
		if topPoint >= self.minimumPointEvent:
			puntoAlto = self.highestPointPosition(trace,topPoint)
			timei = t+0.01*puntoAlto - analisisTimeLapse/2
			timef = t+0.01*puntoAlto + analisisTimeLapse/2
			# mseed  100 muestras por segundo cada posicion del arreglo representa un dato obtenido en 1/100 de segundo
			main = Signal(trace.slice(timei,timef) , "","","","",timei ,timef, self.minimumPointEvent,self.analisisTimeLapse, "b")# el segemento se toma como evento y se crea como nuevo Objeto signal !!!!!!!!!!!!!!1!!!!!
			self.eventTraceList.append(main)
			self.subSearchTimeTraces.append([timei, timef])# veremos si se usa !!!!!!!!!!!!!!!!!
			#self.subSearchTracesUsed.append(main)#veremos si se usa !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			return True
		else:
			timei = self.t+0.01*puntoAlto - analisisTimeLapse/2
			timef = self.t+0.01*puntoAlto + analisisTimeLapse/2
			self.subSearchTimeTraces.append([timei, timef])			
			return False

	def highestPointPosition(self, trace, highestPoint):
		for x in range(0,trace.count()):
			if(trace[x] == highestPoint):
				return x# retorna la posicion de la diferencia mas alta que se puede encontrar

	def analiseSTALTA(self, thr_on,thr_off,windowop, windowend): # falta controlar los piocs iniciales del alg !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		df = self.trace.stats.sampling_rate
		cft = recursive_sta_lta(self.trace.data, int(windowop*df), int(windowend*df)) # define los tmanios de ventana 
		plot_trigger(self.trace,cft,thr_on,thr_off) # se define la variacion a marcar

print("hola")

porfa = Signal("","EC","CAYR","","SHZZ",'2017-01-10 05:00:00', 24,500, 360,"a")

# base partitioner script

'''
thr_on = 1.1
thr_off = 0.99
tiempoSismo = 360

tiempoAntes = tiempoSismo/2
tiempoDespues = tiempoSismo/2

clienteArclink = Client('test', '192.168.1.7', 18001)# coneccion al stream

t = UTCDateTime('2017-01-10 05:00:00') # +5 horas para utc y poner la fecha deseada.
trace5 = clienteArclink.get_waveforms('EC', 'CAYR', '', 'SHZ',t,t+3600*16,route = False, compressed = False)[0] # tiempo adicional deseado en segundos 

puntoAlto = 0

for x in range(0, trace5.count()):
	if(trace5[x] == trace5.max()):
		puntoAlto = x

trace5 = trace5.slice(t+0.01*puntoAlto -tiempoAntes, t+0.01*puntoAlto+tiempoDespues)
df5 = trace5.stats.sampling_rate
cft5 = recursive_sta_lta(trace5.data, int(2.5*df5), int(5*df5)) # define los tmanios de ventana 
plot_trigger(trace5,cft5,thr_on,thr_off) # se define la variacion a marcar'''



