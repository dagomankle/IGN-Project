#python 3 || obspy || windows2010
#Hecho por daniel Ginez

import statistics
from obspy.core import read
from obspy.core import UTCDateTime
from obspy.signal.trigger import plot_trigger# importaciones obligatiores menos read dependiendo
from obspy.clients.arclink import Client# para generar la coneccion con la base de datos
#from obspy.signal.trigger import classic_sta_lta # si se quiere clasico
from obspy.signal.trigger import recursive_sta_lta# si se quiere recursivo etc


class Signal:
	num = 0

	def __init__(self, givenTrace,name1,name2,name3,name4,timeStart, hoursORtf, minimumPointEvent, analisisTimeLapse, type):
		if type == "a":# COnstructor que se conecta al servidor en la red local y obtiene un archivo determinado
			clienteArclink = Client('test', '192.168.1.7', 18001)# coneccion al stream
			self.t = UTCDateTime(timeStart) # +5 horas para utc y poner la fecha deseada. Hay que automatizar esto
			self.tf = self.t + 3600*hoursORtf
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
		self.subSearchTimeTraces = []

		if type != "b":
			if self.eventObteiner(self.trace, self.t):
				print(self.tf)
				#self.trace.detrend()
				self.subTracesManager(self.trace)

	def subTracesManager(self, trace):
		print("submanager")
		print()

		aTime = self.subSearchTimeTraces[-1][0]
		saTime = self.timePicker(aTime, "a")
		bTime = self.subSearchTimeTraces[-1][1]
		sbTime = self.timePicker(bTime, "b")		

		self.num = self.num +1
		print("A" +str(self.num))
		print(saTime)
		print(aTime)
		
		if(aTime != saTime and self.redundanceCheck(saTime,aTime)):
			subTraceA = trace.slice( saTime,aTime)
			#subTraceA.plot()			
			if self.eventObteiner(subTraceA, saTime):
				self.subTracesManager(subTraceA)

		print()
		print("B"+str(self.num))
		print(bTime)
		print(sbTime)

		if(bTime != sbTime and self.redundanceCheck(bTime,sbTime)):
			subTraceB = trace.slice(bTime,sbTime)

			if self.eventObteiner(subTraceB, bTime):
				self.subTracesManager(subTraceB)

	def redundanceCheck(self, timei, timef):
		control = True
		for x in range(0,len(self.subSearchTimeTraces)):
			if(self.subSearchTimeTraces[x][0] == timei and self.subSearchTimeTraces[x][1] == timef):
				control = False
				break

		return control

	def timePicker(self, time, type):
		control = True
		dateReturn = UTCDateTime('1000-01-10 05:00:00')
		if type == "a":
			for x in range(0,len(self.subSearchTimeTraces)):
				print("TimePickingA")

				if(time > self.subSearchTimeTraces[x][1]):
					control = False
					if dateReturn < self.subSearchTimeTraces[x][1]:
						dateReturn = self.subSearchTimeTraces[x][1]

			if control:
				dateReturn = self.t
		else:
			for x in range(0,len(self.subSearchTimeTraces)):
				print("TimePickingB")

				if(time <= self.subSearchTimeTraces[x][0]):
					control = False
					if dateReturn < self.subSearchTimeTraces[x][0]:
						dateReturn = self.subSearchTimeTraces[x][0]

			if control:
				dateReturn = self.tf

		return dateReturn

	def eventObteiner(self, trace, t):
		topPoint = trace.max()
		'''if(trace.count() < 10 ):#tiempo minimo de referencia para un subtrazo, menor a 10 milisegundos se ignora
			return False'''

		if abs(topPoint) >= self.minimumPointEvent:
			puntoAlto = self.highestPointPosition(trace,topPoint)
			timei = t+0.01*puntoAlto - self.analisisTimeLapse/2
			if timei < t:
				timei = t
			timef = t+0.01*puntoAlto + self.analisisTimeLapse/2
			# mseed  100 muestras por segundo cada posicion del arreglo representa un dato obtenido en 1/100 de segundo
			main = Signal(trace.slice(timei,timef) , "","","","",timei ,timef, self.minimumPointEvent,self.analisisTimeLapse, "b")# el segemento se toma como evento y se crea como nuevo Objeto signal !!!!!!!!!!!!!!1!!!!!
			self.eventTraceList.append(main)
			#main.trace.plot()
			self.subSearchTimeTraces.append([timei, timei+0.01*(main.trace.count()-1)])# veremos si se usa !!!!!!!!!!!!!!!!!
			print("\nTiempos usados registrados")
			print(self.subSearchTimeTraces[-1][0])
			print(self.subSearchTimeTraces[-1][1])
			#self.subSearchTracesUsed.append(main)#veremos si se usa !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			return True
		else:
			timei = t
			timef = t+0.01*(trace.count()-1)
			self.subSearchTimeTraces.append([timei, timef])			
			return False

	def highestPointPosition(self, trace, highestPoint):
		for x in range(0,trace.count()):
			if(trace[x] == highestPoint):
				return x# retorna la posicion de la diferencia mas alta que se puede encontrar

	#centrar en las trazas para obetener datos reales.

		#Este centering modifica  los datos de muestreo de un tazo.
	'''def traceCentering(self, trace):
		media = statistics.mean(trace)
		for x in range(0, len(trace.data)):
			trace.data[x] = trace.data[x]-media
		return trace'''

	#desarrollar metodos que permitan la automatizacion  de  los parametros optimos para elanalisis

	def analisiSTALTA(self, thr_on,thr_off,windowop, windowend): # falta controlar los piocs iniciales del alg !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		df = self.trace.stats.sampling_rate
		cft = recursive_sta_lta(self.trace.data, int(windowop*df), int(windowend*df)) # define los tmanios de ventana 
		plot_trigger(self.trace,cft,thr_on,thr_off) # se define la variacion a marcar

print("hola")

porfa = Signal("",'EC','CAYR','','SHZ','2017-01-01 05:00:00', 24,1100, 320,"a")


