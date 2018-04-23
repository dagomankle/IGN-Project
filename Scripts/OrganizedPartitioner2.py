#python 3 || obspy || windows2010
# Hecho por Daniel Ginez

from obspy.core import read
from obspy.core import UTCDateTime
from obspy.clients.arclink import Client# para generar la coneccion con la base de datos

class Signal:
	#Es necesario optimizar el constructor utilizando pseudo sobrecargas
	def __init__(self, givenTrace,name1,name2,name3,name4,timeStart, hoursORtf, minimumPointEvent, analisisTimeLapse, frecuencia,type):
		if type == "a":# COnstructor que se conecta al servidor en la red local y obtiene un archivo determinado
			clienteArclink = Client('test', '192.168.1.7', 18001)# coneccion al stream
			self.__t = UTCDateTime(timeStart) # +5 horas para utc y poner la fecha deseada. Hay que automatizar esto
			self.__tf = self.__t + 3600*hoursORtf
			self.__trace= clienteArclink.get_waveforms(name1, name2, name3, name4,self.__t,self.__tf,route = False, compressed = False)[0] # se obtiene el trazo principal

		if type == "b":# constructor que recibe un parametro trace para construir e objeto
			self.__t = UTCDateTime(timeStart) # +5 horas para utc y poner la fecha deseada. Hay que automatizar esto,
			self.__tf = hoursORtf
			self.__trace = givenTrace

		if type == "c":# constructor que recibe uan direccion local para leer un archivo de disco
			self.__trace = read(name1)[0]# obtener tiempo t de alguna forma, cortando string talvez

		self.__frecuencia = frecuencia
		self.__minimumPointEvent = minimumPointEvent
		self.__trace.detrend()# funcion de la libreria stream que quita la media de un trazo para que este se encuentre encerado.
		self.__highestPoint = self.__trace.max()
		self.__analisisTimeLapse = analisisTimeLapse
		self.__eventTraceList = []
		self.__subSearchTimeTraces = []# se usa para el control de la recursion durante la construccion del objeto, al final almcenara espacios de busqueda con un filtro

		if type != "b":
			if self.__eventObteiner(self.__trace, self.__t, self.__frecuencia):
				self.__subTracesManager(self.__trace)
				self.__subSearchTimeTraces = self.__timesOrganizer()

	def __subTracesManager(self, trace):#funcion que gestiona la segmentacion del trazo para iniciar los analisis detallados
		aTime = self.__subSearchTimeTraces[-1][0]
		saTime = self.__timePicker(aTime, "a")
		bTime = self.__subSearchTimeTraces[-1][1]
		sbTime = self.__timePicker(bTime, "b")		
		
		if(aTime != saTime and self.__redundanceCheck(saTime,aTime)):
			subTraceA = trace.slice( saTime,aTime)		
			if self.__eventObteiner(subTraceA, saTime, self.__frecuencia):
				self.__subTracesManager(subTraceA)

		if(bTime != sbTime and self.__redundanceCheck(bTime,sbTime)):
			subTraceB = trace.slice(bTime,sbTime)

			if self.__eventObteiner(subTraceB, bTime, self.__frecuencia):
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

	def __eventObteiner(self, trace, t, frecuencia):
		topPoint = trace.max()
		if abs(topPoint) >= self.__minimumPointEvent:
			puntoAlto = self.__highestPointPosition(trace,topPoint)
			timei = t+(1/frecuencia)*puntoAlto - self.__analisisTimeLapse/2
			if timei < t:
				timei = t
			timef = t+(1/frecuencia)*puntoAlto + self.__analisisTimeLapse/2

			#mseed con valor variable de 1 dato obtenido 1/ X avo de segundo pilas !!!!!!!!!
			# mseed  100 muestras por segundo cada posicion del arreglo representa un dato obtenido en 1/100 de segundo 
			main = Signal(trace.slice(timei,timef) , "","","","",timei ,timef, self.__minimumPointEvent,self.__analisisTimeLapse,100, "b")# el segemento se toma como evento y se crea como nuevo Objeto signal !!!!!!!!!!!!!!1!!!!!
			self.__eventTraceList.append(main)
			#main.trace.plot()
			tiempos = [timei, timei+(1/frecuencia)*(main.__trace.count()-1), "E"]
			if tiempos not in self.__subSearchTimeTraces:
				self.__subSearchTimeTraces.append([timei, timei+(1/frecuencia)*(main.__trace.count()-1), "E"])# veremos si se usa !!!!!!!!!!!!!!!!!
			print("\nTiempos usados registrados")
			print(self.__subSearchTimeTraces[-1][0])
			print(self.__subSearchTimeTraces[-1][1])
			return True
		else:
			timei = t
			timef = t+(1/frecuencia)*(trace.count()-1)
			self.__subSearchTimeTraces.append([timei, timef, "G"])			
			return False

	def __timesOrganizer(self):# organiza los tiempos usados guardados en base a la existencia de eventos
		internal = []
		internal2 = []
		i = 0
		for x in range(0,len(self.__subSearchTimeTraces)):
			control = True
			if self.__subSearchTimeTraces[x][2] == "E":
				if x == 0:
					internal.append(self.__subSearchTimeTraces[0])
					internal2.append(self.__eventTraceList[0])
				else:
					for y in range(0,len(internal)):
						if self.__subSearchTimeTraces[x][1] <= internal[y][0]:
							internal.insert(y,self.__subSearchTimeTraces[x])
							internal2.insert(y,self.__eventTraceList[i])
							control = False
							break
					if control:
						internal.append(self.__subSearchTimeTraces[x])
						internal2.append(self.__eventTraceList[i])
				i = i+1

		self.__eventTraceList = internal2
		internal = self.__timesFiller(internal)
		return internal		

	def __timesFiller(self, internal):#llena los tiempos de la traza en las que no hay eventos los marca con n
		almacen = []
		i = 0
		for x in range(0,len(internal)):
			if x == 0:
				if internal[x][0] != self.__t:
					almacen.append([[ self.__t , internal[x][0],'N'], 0])
					i = i +1
			elif x == len(internal)-1:
				if internal[x][1] != self.__tf:
					almacen.append([[ internal[x][1], self.__tf , 'N'], 1+x+i])
			else:
				if internal[x][1] != internal[x+1][0]:
					almacen.append([[ internal[x][1] , internal[x+1][0]  , 'N'], x +i])
					i = i+1

		for x in range(0,len(almacen)):
			internal.insert(almacen[x][1], almacen[x][0])

		return internal

	def __highestPointPosition(self, trace, highestPoint):
		for x in range(0,trace.count()):
			if(trace[x] == highestPoint):
				return x# retorna la posicion de la diferencia mas alta que se puede encontrar

# LAS FUNCIONES SIGUIENTES NO SON PARTE FUNCIONAL DE LA CREACION DEL OBJETO; SON FUNCIONES DE MUESTREO U OBTENCION DE DATOS

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
		return self.__trace.stats()

	def getTrace(self):
		return self.__trace

	def getFrecuencia(self):
		return self.__frecuencia

	def getSTime(self):
		return self.__t

	def getETime(self):
		return self.__tf

	def getMaxAmp(self):
		return self.__highestPoint

	def getEventLaps(self):
		return self.__eventTraceList

	def plotEventLaps(self):
		for x in self.__eventTraceList:
			x.getTrace().plot()

	def plotNoEvents(self):
		for x in range(0,len(self.__subSearchTimeTraces)):
			if(self.__subSearchTimeTraces[x][2] == "N"):
				self.__trace.slice( self.__subSearchTimeTraces[x][0],self.__subSearchTimeTraces[x][1]).plot()	



print("Bienvenido a la primera clase de GeoDago")
print()

porfa = Signal("",'EC','CAYR','','SHZ','2017-01-24 00:00:00', 24, 1100, 320,100,"a")
#porfa = Signal("",'EC','BREF','','BHZ','2017-02-07 00:00:00', 24, 1100, 320,50,"a")
#porfa = Signal("",'EC','CHL1','','HHZ','2017-02-07 00:00:00', 24, 1100, 320,100,"a")
#porfa = Signal("",'EC','FLF1','','HHE','2017-02-07 00:00:00', 24, 1100, 320,130,"a")
