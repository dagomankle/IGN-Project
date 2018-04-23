#python 3 || obspy || windows2010
# Hecho por Daniel Ginez
#from sys import exit
from obspy.core import read, UTCDateTime
from datetime import datetime, date, time
from obspy.clients.arclink import Client# para generar la coneccion con la base de datos

class SignalDg:
	def __init__(self, *args):
		lArgs = []
		argNum = len(args)
		for arg in args:
			lArgs.append(arg)
		multiple = True

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
			self.__oTrace = lArgs[0]
			self.__trace = lArgs[0]
			self.__t = self.__trace.stats.starttime
			self.__tf = self.__trace.stats.endtime
			self.__minimumPointEvent = lArgs[1]
			self.__analisisTimeLapse = lArgs[2]

		elif argNum == 3:# falta poner una excepcion de archivo mal leido
			#seg = Signal('volcan.mseed', 1000, 320)
			self.__oTrace = read(lArgs[0])
			self.__trace = read(lArgs[0])[0]
			self.__t = self.__trace.stats.starttime
			self.__tf = self.__trace.stats.endtime
			self.__minimumPointEvent = lArgs[1]
			self.__analisisTimeLapse = lArgs[2]
		else:
			print("Argumentos no aceptables")
			sys.exit()

		self.__trace.detrend()# funcion de la libreria stream que quita la media de un trazo para que este se encuentre encerado.
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
					self.__subSegmenter()
					#self.__timeAranger()

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

		aTime = self.__subSearchTimeTraces[-1][0]#fin a
		saTime = self.__timePicker(aTime, "a")#inicio a
		bTime = self.__subSearchTimeTraces[-1][1]#inicio b
		sbTime = self.__timePicker(bTime, "b")#fin b

		if(aTime != saTime):#entra en el if si el tiempo inicial y final de la rama a del árbol son diferentes,evita que se envíe un trazo nulo
			print("A")
			print(saTime)
			print(aTime)
			subTraceA = trace.slice( saTime,aTime)#Envía el trazo seleccionado para cortarlo
			if(subTraceA.stats.starttime!=subTraceA.stats.endtime):#evita que se envíe un trazo nulo si después de cortar el trazo el tiempo inicial y final son iguales
				if self.__eventObteiner(subTraceA, saTime):
					self.__subTracesManager(subTraceA)

		if(bTime != sbTime):#entra en el if si el tiempo inicial y final de la rama b del árbol son diferentes,evita que se envíe un trazo nulo
			print("B")
			print(bTime)
			print(sbTime)
			subTraceB = trace.slice(bTime,sbTime)#Envía el trazo seleccionado para cortarlo
			if(subTraceB.stats.starttime!=subTraceB.stats.endtime):#evita que se envíe un trazo nulo si después de cortar el trazo el tiempo inicial y final son iguales
				if self.__eventObteiner(subTraceB, bTime):
					self.__subTracesManager(subTraceB)




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
		topPoint = trace.max()#obtiene el púnto maximo del trazo trace
		if abs(topPoint) >= self.__minimumPointEvent:#Ingresa si el puno maximo del trazo es mayor o igual que el punto mínimo para considerar que existe un evento
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
			return True
		else:#Ingresa aqui si el punto máximo del trazo es menor al punto mínimo para considerar evento, por lo cual no existe un evento
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
			if self.__subSearchTimeTraces[x][2] == "E":#entra en este if en caso de que en este periodo de tiempo haya un evento
				for y in range(0,len(internal)):
					if x == 0:
						internal.append(self.__subSearchTimeTraces[0])
						internal2.append(self.__eventTraceList[0])
						control = False
						break
					elif self.__subSearchTimeTraces[x][1] <= internal[y][0]:
						internal.insert(y,self.__subSearchTimeTraces[x])
						internal2.insert(y,self.__eventTraceList[i])
						control = False
						break
				if control:
					internal.append(self.__subSearchTimeTraces[x])
					internal2.append(self.__eventTraceList[i])
				i = i+1
			else:#entra en este elif en caso de que en este periodo de tiempo no haya un evento
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
		lista = [self.__eventTraceList[6]]
		self.__eventTraceList[6].getTrace().plot()
		toBeReplaced = self.__pikeSearcher(lista, 6)
		#toBeReplaced = self.__pikeSearcher(self.__eventTraceList, -1)

		# recuerda reconstruir  como se determina el punto inicial en el primer for  un for negativo
		d = 0
		for x in range(0,len(toBeReplaced)):
			pos = toBeReplaced[x][1]
			pos2 = toBeReplaced[x][2] 

			self.__eventTraceList.pop(pos + d)
			self.__subSearchTimeTraces. pop(pos2 +d)
			for y in range(0,  len(toBeReplaced[x][0])):
				self.__eventTraceList.insert(pos + d,toBeReplaced[x][0][y])
				self.__subSearchTimeTraces.insert(pos2 + d, [toBeReplaced[x][0][y].getTrace().stats.starttime, toBeReplaced[x][0][y].getTrace(), "E" ])
				d = d+1

	def __pikeSearcher(self, lista, numero):
		toBeReplaced = []
		positions = []

		if numero != -1:
			positions.append(numero)
		else:
			for y in range (0, len(self.__subSearchTimeTraces)):
				if(self.__subSearchTimeTraces[y][2] == "E"):
					positions.append(y)

		print(" En tiempos:  ", len(positions), "En trazos: ", len(lista))

		for x in range(0, len(lista)):
			print("\n PARA EL TRAZO:   ", x)
			trace = lista[x].getTrace()
			print(trace.stats)
			media = self.__localMean(trace)
			control = True
			exist = []
			sss = []
			
			d = 0
			u = 0
			pos = self.__highestPointPosition(trace, lista[x].getMaxAmp()) #Se plantea una venta de separacion entre los sismos de 20 

			'''print("\ndespues max es: ", len(trace) , "punto maximo es : = ", self.__minimumPointEvent ,":\n")
			control = True
			y = pos 
			while y > 0:
				if control:
					if self.__lineDefiner(trace, y , 15, 2*abs(media), media, "i"):
						print("\n original y = ", y)
						control = False
						d = y 
						y = d
						print("evol y=", y, " el otro d = ", d)
						print(trace.stats.starttime + (d/self.__frecuencia))
				elif trace[y] >= self.__minimumPointEvent:
					print("entro")
					control = True 
					print("y=", y, " el otro d = ", d)
					z = 0
					while True:
						print("Z :", z)
						if y+z  == d :
							break
						if self.__lineDefiner(trace, y + z , 15, 2*abs(media), media, "d"):
							u =  y + z
							break
						z = z + 5
					print(" con  u = ", u, "y d =", d)
					if u < d:
						exist.append(((d-u) /2) + u)
				y = y - 5   '''

			print("\ndespues max es: ", len(trace) , "punto minimo es : = ", self.__minimumPointEvent ,":\n")
			control = True
			y = pos
			while y < len(trace):
				if control:
					if self.__lineDefiner(trace, y , 15, 2*abs(media), media, "d"):
						control = False
						d = y 
						y = d
				elif trace[y] >= self.__minimumPointEvent:
					control = True 
					z = 0
					while True:
						if y-z  == d :
							break
						if self.__lineDefiner(trace, y - z , 15, 2*abs(media), media, "i"):
							u =  y - z
							break
						z = z + 5
					if u > d:
						exist.append(((u-d) /2) + d)
				y = y + 1				   

			print("\n Arreglo Exist:\n")
			for y  in exist:
				print(trace.stats.starttime + y/self.__frecuencia )

			print("\n tiempos del SS:\n" )
			timei = trace.stats.starttime
			for y in range(0, len(exist)):# poner el  tiempo final
				timef = trace.stats.starttime + exist[y]/self.__frecuencia
				
				print("inicio: ", timei)
				print("final:  ", timef, "\n")
				sTrace = trace.slice(timei,timef)
				main = SignalDg(sTrace , sTrace.stats.starttime ,sTrace.stats.endtime, self.__minimumPointEvent,self.__analisisTimeLapse)
				sss.append(main)
				timei = timef

			#sTrace = trace.slice(sss[-1].getTrace().stats.endtime,trace.stats.endtime) # hay que comentar esto para probar en serio 
			if len(sss) > 0:
				sTrace = trace.slice(sss[-1].getTrace().stats.endtime,trace.stats.endtime)
				sss.append(SignalDg(sTrace , sTrace.stats.starttime ,sTrace.stats.endtime, self.__minimumPointEvent,self.__analisisTimeLapse))
				#toBeReplaced.append([sss, x, positions[x]])
				toBeReplaced.append([sss, positions[x], positions[x]])
			print(len(trace))

		return toBeReplaced

	def __lineDefiner(self, trace, punto,cantidad, variacion, media, dir):
		resultado = True
		counter = 0
		if dir == "d":
			#print("\n PUnto de Control con el tiempo inicial aprox : ", trace.stats.starttime + punto/self.__frecuencia)
			for x in reversed(range( punto - cantidad, punto)):
				if (abs(trace[x]) - variacion) >= media:
					counter = counter + 1
				if counter > 0 :
					resultado = False 
					break 
				#print("punto de analisis :", x,  "el trace es : ", abs(trace[x])-variacion, " la media es ", media , "  contador ", counter)   
		else:
			print("\n PUnto de Control ")
			for x in range(punto, punto + cantidad):			
				if (abs(trace[x]) - variacion )>= media:
					counter = counter + 1
				if counter > 0 :
					resultado = False 
					break 
				print("punto de analisis :", x,  "el trace es : ", abs(trace[x])-variacion, " la media es ", media , "  contador ", counter)	

		return resultado
		
	def __localMean(serlf, trace):
		suma = 0
		for x in range(0, len(trace)):
			suma = suma + trace[x]
		return suma / len(trace)

	#busca si algun evento fue cortado  e identifica donde quedó la otra parte
	#identifica en que posición deberá insertarse dicho trazo
	#recibe los trazos cortados y los inserta en la lista de eventos y en el de los tiempos
	def __timeSearcher(self):
		posicion=0#la posición donde debería agregarse el evento
		t=0#para almacenar los nuevos tiempos de la union de dos trazos
		aux=[]#trazo auxiliar a analizar
		trazo=[]#trazo cortado para buscar un evento
		analizar=[]#union de dos trazos que se envía para cortar
		Trazos=self.__eventTraceList#lista de trazos que contiene los eventos
		Tiempos=self.__subSearchTimeTraces#lista de tiempos de todos los trazos
		timei=0#guarda el tiempo inicial para cortar el trazo
		timef=0#guarda el tiempo final para cortar el trazo
		bandera=False

		#recorre toda la lista de eventos
		for x in range(0,len(self.__eventTraceList)):
			aux=self.__eventTraceList[x].getTrace()
			bandera=False
			analizar=[]
			timei=aux.starttime#tiempo inicial del trazo
			timef=aux.starttime+((aux.endtime-aux.starttime)*0.1)#al tiempo inicial del trazo le sumo el 10% del total
			trazo=aux.slice(timei,timef)#evalúa si hay un evento al inicio del trazo
			topPoint = trazo.max()#toma el punto maximo del inicio del trazo
			if abs(topPoint) >= self.__minimumPointEvent:#entra en el if en caso de que deba considerarse como evento
			#busco en la lista de tiempos el trazo que tiene como tiempo final el inicial del trazo
				for y in range(0,len(Tiempos)):
					if(Tiempos[y][1]==trazo.starttime):#si el inicial es igual al final
						t=Tiempos[y][0]#almaceno el nuevo tiempo inicial
						self.__subSearchTimeTraces.pop(y)
						bandera=True
						break
			if(bandera):#continúa si encuentra un evento
				posicion=x
				analizar[0]=t
				analizar[1]=aux[1]
				analizar[2]="E"
				analizar=self.__pikeSearcher(analizar,x)#envío a analizar el nuevo trazo
				self.__eventTraceList.pop(x)
				for y in range(0,len(analizar)):
					self.__eventTraceList.insert(posicion,analizar[0][y])
					self.__subSearchTimeTraces.insert(posicion,[analizar[0][y].starttime,analizar[y].endtime, "E"])
					posicion=posicion+1
					x=posicion-1
				aux=self.__eventTraceList[x].getTrace()

			bandera=False
			analizar=[]
			timei=aux.endtime-((aux.endtime-aux.starttime)*0.1)#tiempo inicial del trazo
			timef=aux.timef#al tiempo inicial del trazo le sumo el 10% del total
			trazo=aux.slice(timei,timef)#evalúa si hay un evento al final del trazo
			topPoint = trazo.max()#toma el punto maximo del final del trazo
			if abs(topPoint) >= self.__minimumPointEvent:#entra en el if en caso de que deba considerarse como evento
			#busco en la lista de tiempos el trazo que tiene como tiempo final el inicial del trazo
				for y in range(0,Tiempos):
					if(Tiempos[y][0]==trazo.starttime):
						t=Tiempos[y][1]#almaceno el nuevo tiempo final
						self.__subSearchTimeTraces.pop(y)
						bandera=True
						break
			if(bandera):#continúa si encuentra un evento
				posicion=x
				analizar[0]=aux[0]
				analizar[1]=t
				analizar[2]="E"
				analizar=self.__pikeSearcher(analizar,x)#envío a analizar el nuevo trazo
				self.__eventTraceList.pop(x)
				for y in range(0,len(analizar)):
					self.__eventTraceList.insert(posicion,analizar[0][y])
					self.__subSearchTimeTraces.insert(posicion,[analizar[0][y].starttime,analizar[y].endtime, "E"])
					posicion=posicion+1
					x=posicion-1

	def __timeAranger(self):
		hola = 1

# LAS FUNCIONES SIGUIENTES NO SON PARTE FUNCIONAL DE LA CREACION DEL OBJETO; SON FUNCIONES DE MUESTREO U OBTENCION DE DATOS

# falta lograr encapsulacion :S a pesar del get se pasa la informacion; la solucion seria crear una nueva lista y copiar de uno en uno los datos o algo asi

	def getTimes(self, letra ):# imprime todos los tiempos analisados si se pone t de arugmento, con e solo tiempos de eventos si se pone n los trazos sin eventos
		times = []
		if letra == "T":#si se quiere imprimir todos los tiempos, haya evento(E) o no(N)
			for x in range(0,len(self.__subSearchTimeTraces)):
				times.append(self.__subSearchTimeTraces[x])
		elif letra == "E" or "N":#En caso de que se quiera imprimir únicamente los tiempos que tengan eventos(E) o los que no(N)
			for x in range(0,len(self.__subSearchTimeTraces)):
				if(self.__subSearchTimeTraces[x][2] == letra):
					times.append(self.__subSearchTimeTraces[x])
		else:
			print("Fracaso")

		return times

	def getStats(self):
		status = self.__trace.stats()
		return status

	def getMinPoint(self):
		min = self.__minimumPointEvent
		return trace

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

horai=datetime.now()
#tipo A ---- ( nombre1, nombre2, nombre3, nombre4, fechaInicio, horas a anlizar, amplitud minima, ventanas de tiempo) ---- 8 argumentos
seg = SignalDg('EC','CAYR','','SHZ','2017-01-24  00:00:00', 24, 1000, 320)
horaf=datetime.now()-horai
#2016-02-19
print("\n Contando con los segundos de coneccion el script tomo: ",horaf)

#tipo C ---- (direccion del archivo, amplitud minima, ventanas de tiempo)---- 3 argumentos
#seg = Signal('volcan.mseed', 1000, 320)



